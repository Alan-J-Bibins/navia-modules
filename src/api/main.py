import asyncio
import base64
import json
import os
from fastapi import Body, Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from activities.social_story.evaluation.main import evaluate_social_story_as_dict, evaluate_social_story_as_metrics
from activities.social_story.model import SocialStorySchema
from api.utils import create_mock_profile
from entities.learner import LearnerProfile
from wrappers.image_gen.fanar import generate_fanar_image
from activities.social_story.main import (
    create_social_story_schema,
    generate_story_visual_plan,
    regenerate_sentence_item,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_learner_profile():
    return create_mock_profile()


def sse_event(data: dict) -> str:
    """Helper to format SSE events consistently."""
    return f"data: {json.dumps(data)}\n\n"


@app.post("/activity/social_story/")
async def generate_social_story_stream(
    request: Request,
    profile: LearnerProfile = Body(..., embed=True),
    situation: str = Body(..., embed=True),
    generate_images: bool = Body(..., embed=True),
):
    async def event_stream():
        try:
            triggers = json.dumps(profile.sensoryTriggers)
            reading_level = profile.verbalAbility
            functional_word_range = str(profile.functionalWordRange)
            yield sse_event({"type": "status", "message": "Generating story..."})
            # 1. Story Generation
            try:
                story_schema = await asyncio.to_thread(
                    create_social_story_schema,
                    situation=situation,
                    trigger=triggers,
                    target_age=profile.age,
                    reading_level=reading_level,
                    functional_word_range=functional_word_range,
                )
            except Exception as e:
                yield sse_event(
                    {"type": "error", "stage": "story_generation", "message": str(e)}
                )
                return
            if story_schema is None:
                yield sse_event(
                    {
                        "type": "error",
                        "stage": "story_generation",
                        "message": "LLM returned invalid story schema",
                    }
                )
                return
            try:
                yield sse_event(
                    {"type": "story", "data": story_schema.model_dump_json()}
                )
            except Exception as e:
                yield sse_event(
                    {
                        "type": "error",
                        "stage": "serialization",
                        "message": f"Failed to serialize story: {str(e)}",
                    }
                )
                return
            if not generate_images:
                yield sse_event(
                    {"type": "status", "message": "Skipping illustrations..."}
                )
            else:
                yield sse_event(
                    {"type": "status", "message": "Planning illustrations..."}
                )
                try:
                    visual_plan = await asyncio.to_thread(
                        generate_story_visual_plan, story_schema
                    )
                except Exception as e:
                    yield sse_event(
                        {"type": "error", "stage": "visual_planning", "message": str(e)}
                    )
                    return
                if visual_plan is None:
                    yield sse_event(
                        {
                            "type": "error",
                            "stage": "visual_planning",
                            "message": "LLM returned invalid visual plan",
                        }
                    )
                    return

                for i, page in enumerate(visual_plan.pages):
                    if await request.is_disconnected():
                        print("Client disconnected. Aborting stream.")
                        return
                    yield sse_event(
                        {
                            "type": "status",
                            "message": f"Generating image {i+1}/{len(visual_plan.pages)}...",
                        }
                    )
                    image_path = f"generated_page{i}.png"
                    max_retries = 3
                    success = False
                    for attempt in range(max_retries):
                        if await request.is_disconnected():
                            return
                        try:
                            await asyncio.to_thread(
                                generate_fanar_image,
                                prompt=f"{page.visual_description}\n\n{visual_plan.style_preset}",
                                output_path=image_path,
                            )
                            if not os.path.exists(image_path):
                                raise FileNotFoundError(
                                    "Image generation completed but file was not created."
                                )
                            success = True
                            break
                        except Exception as e:
                            error_msg = str(e).lower()
                            is_rate_limit = (
                                "429" in error_msg
                                or "rate" in error_msg
                                or "limit" in error_msg
                            )
                            if is_rate_limit and attempt < max_retries - 1:
                                wait_time = 2**attempt
                                yield sse_event(
                                    {
                                        "type": "status",
                                        "message": f"Rate limited. Retrying image {i+1} in {wait_time}s...",
                                    }
                                )
                                await asyncio.sleep(wait_time)
                            else:
                                yield sse_event(
                                    {
                                        "type": "image_error",
                                        "page": i + 1,
                                        "message": f"Failed after {attempt+1} attempts: {str(e)}",
                                    }
                                )
                                break
                    if success:
                        try:
                            with open(image_path, "rb") as img_file:
                                encoded = base64.b64encode(img_file.read()).decode(
                                    "utf-8"
                                )
                            yield sse_event(
                                {"type": "image", "page": i + 1, "data": encoded}
                            )
                        except Exception as e:
                            yield sse_event(
                                {
                                    "type": "image_error",
                                    "page": i + 1,
                                    "message": f"Failed to encode image: {str(e)}",
                                }
                            )
            yield sse_event({"type": "complete"})
        except Exception as e:
            yield sse_event(
                {
                    "type": "error",
                    "stage": "stream",
                    "message": f"Unexpected stream failure: {str(e)}",
                }
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/activity/social_story/regenerate_sentence")
async def regenerate_sentence_stream(
    request: Request,
    story: SocialStorySchema = Body(..., embed=True),
    sentence_id: int = Body(..., embed=True),
    modification_prompt: str | None = Body(default=None, embed=True),
):
    async def event_stream():
        try:
            yield sse_event({"type": "status", "message": "Regenerating sentence..."})
            try:
                result = await asyncio.to_thread(
                    regenerate_sentence_item,
                    story_schema=story,
                    sentence_id=sentence_id,
                    modification_prompt=modification_prompt,
                )
            except Exception as e:
                yield sse_event(
                    {
                        "type": "error",
                        "stage": "sentence_regeneration",
                        "message": str(e),
                    }
                )
                return
            if result is None:
                yield sse_event(
                    {
                        "type": "error",
                        "stage": "sentence_regeneration",
                        "message": "Regeneration function returned invalid result",
                    }
                )
                return
            yield sse_event({"type": "sentence", "data": result.model_dump_json()})
            yield sse_event({"type": "complete"})
        except Exception as e:
            yield sse_event(
                {
                    "type": "error",
                    "stage": "stream",
                    "message": f"Unexpected stream failure: {str(e)}",
                }
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/activity/social_story/tier_evaluate")
async def tier_evaluate_social_story_handler(
    profile: LearnerProfile = Depends(get_learner_profile),
    story: SocialStorySchema = Body(..., embed=True),
    tier1_enabled: bool = Query(True, description="Run deterministic checks"),
    tier2_enabled: bool = Query(True, description="Run readability analysis"),
    tier3_enabled: bool = Query(True, description="Run qualitative review (LLM call)"),
):
    result = await asyncio.to_thread(
        evaluate_social_story_as_dict,
        story=story,
        target_age=profile.age,
        tier1_enabled=tier1_enabled,
        tier2_enabled=tier2_enabled,
        tier3_enabled=tier3_enabled,
    )
    return result


@app.post("/activity/social_story/evaluate")
async def evaluate_social_story_handler(
    profile: LearnerProfile = Depends(get_learner_profile),
    story: SocialStorySchema = Body(..., embed=True),
):
    result = await asyncio.to_thread(
        evaluate_social_story_as_metrics,
        story=story,
        target_age=profile.age,
    )
    return result
