import asyncio
import base64
import json
import os
from fastapi import Body, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from activities.social_story.judge import judge_social_story
from activities.social_story.model import SocialStorySchema
from api.utils import create_mock_profile
from entities.learner import LearnerProfile
from wrappers.image_gen.fanar import generate_fanar_image
from activities.social_story.main import (
    create_social_story_schema,
    generate_story_visual_plan,
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
    profile: LearnerProfile = Depends(get_learner_profile),
    situation: str = Body(..., embed=True),
    generate_images: bool = Body(..., embed=True),
):
    async def event_stream():
        try:
            triggers = json.dumps(profile.sensoryTriggers)
            reading_level = profile.verbalAbility
            yield sse_event({"type": "status", "message": "Generating story..."})
            # 1. Story Generation
            try:
                story_schema = await asyncio.to_thread(
                    create_social_story_schema,
                    situation=situation,
                    trigger=triggers,
                    target_age=profile.age,
                    reading_level=reading_level,
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


@app.post("/activity/social_story/judge")
async def judge_social_story_handler(
    profile: LearnerProfile = Depends(get_learner_profile),
    story: SocialStorySchema = Body(..., embed=True),
):
    result = await asyncio.to_thread(
        judge_social_story, story_schema=story, age=profile.age, judge=2
    )
    if result is None:
        return {"error": "Failed to evaluate story - LLM returned invalid response"}
    return {
        "score": result.score,
        "remarks": result.remarks,
    }
