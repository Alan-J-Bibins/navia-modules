import asyncio
import base64
import json
import os
from fastapi import Body, Depends, FastAPI, File, Query, Request, UploadFile
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from activities.social_story import model
from activities.social_story.evaluation.main import (
    evaluate_social_story_as_dict,
    evaluate_social_story_as_metrics,
)
from activities.social_story.model import SocialStorySchema
from api.utils import create_mock_profile
from entities.learner import LearnerProfile
from wrappers.image_gen.fanar import generate_fanar_image
from activities.social_story.main import (
    create_social_story_schema,
    generate_story_visual_plan,
    regenerate_sentence_item,
)

import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from wrappers.image_gen.main import generate_image

OUTPUTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")


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
                    target_gender=profile.gender,
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
    story: SocialStorySchema = Body(..., embed=True),
):
    result = await asyncio.to_thread(
        evaluate_social_story_as_metrics,
        story=story,
        target_age=story.target_age,
        comprehensive_report=True
    )
    return result


@app.post("/generate-image")
async def generate_image_handler(
    request: Request,
    prompt: str = Body(..., embed=True),
):
    async def event_stream():
        try:
            progress_queue = asyncio.Queue()
            loop = asyncio.get_running_loop()

            def on_progress(event):
                """Sync callback from ComfyUI worker thread → async queue."""
                try:
                    asyncio.run_coroutine_threadsafe(progress_queue.put(event), loop)
                except Exception as e:
                    print(f"[on_progress] Failed to queue event: {e}")

            yield sse_event(
                {"type": "status", "message": "Queuing image generation..."}
            )

            image_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
            output_path = str(OUTPUTS_DIR / image_filename)

            max_retries = 3
            success = False

            for attempt in range(max_retries):
                if await request.is_disconnected():
                    print("Client disconnected. Aborting image generation.")
                    return

                yield sse_event(
                    {
                        "type": "status",
                        "message": f"Starting generation attempt {attempt + 1}...",
                    }
                )

                # Run generation wrapper in background thread
                gen_task = asyncio.create_task(
                    asyncio.to_thread(
                        generate_image,
                        model="comfyui_gemini",
                        prompt=prompt,
                        output_path=output_path,
                        on_progress=on_progress,
                    )
                )

                if model in ["gemini", "fanar"]:
                    while not gen_task.done():
                        if await request.is_disconnected():
                            print("Client disconnected. Aborting API generation.")
                            gen_task.cancel()
                            return
                        await asyncio.sleep(0.2)
                else:
                    while not gen_task.done():
                        if await request.is_disconnected():
                            print("Client disconnected. Aborting ComfyUI generation.")
                            return
                        try:
                            event = await asyncio.wait_for(
                                progress_queue.get(), timeout=0.5
                            )

                            stage = event.get("stage")
                            if stage == "executing":
                                node_id = event.get("node", "unknown")
                                node_messages = {
                                    "4": "Loading checkpoint...",
                                    "5": "Encoding prompt...",
                                    "6": "Loading VAE...",
                                    "7": "Preparing latent space...",
                                    "8": "Running sampler...",
                                    "10": "Decoding image...",
                                    "11": "Saving output...",
                                }
                                message = node_messages.get(
                                    node_id, f"Executing node {node_id}..."
                                )
                                yield sse_event(
                                    {
                                        "type": "progress",
                                        "stage": stage,
                                        "message": message,
                                    }
                                )

                            elif stage == "sampling":
                                value = event.get("value", 0)
                                max_val = event.get("max", 0)
                                percent = (
                                    int((value / max_val) * 100) if max_val > 0 else 0
                                )
                                yield sse_event(
                                    {
                                        "type": "progress",
                                        "stage": stage,
                                        "message": f"Sampling step {value}/{max_val} ({percent}%)",
                                        "value": value,
                                        "max": max_val,
                                        "percent": percent,
                                    }
                                )

                            elif stage == "error":
                                error_msg = event.get("message", "Unknown error")
                                yield sse_event(
                                    {
                                        "type": "progress",
                                        "stage": stage,
                                        "message": f"ComfyUI error: {error_msg}",
                                    }
                                )

                        except asyncio.TimeoutError:
                            continue

                try:
                    result_path = await gen_task
                    print(f"[generate_image] Task completed, result: {result_path}")

                    if not os.path.exists(output_path):
                        raise FileNotFoundError(
                            "Image generation completed but file was not created."
                        )
                    success = True
                    break
                except Exception as e:
                    print(f"[generate_image] Task failed on attempt {attempt + 1}: {e}")
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
                                "message": f"Rate limited. Retrying in {wait_time}s...",
                            }
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        yield sse_event(
                            {
                                "type": "error",
                                "stage": "image_generation",
                                "message": f"Failed after {attempt + 1} attempts: {str(e)}",
                            }
                        )
                        return

            if success:
                yield sse_event(
                    {
                        "type": "image",
                        "url": f"/outputs/{image_filename}",
                        "filename": image_filename,
                    }
                )

            yield sse_event({"type": "complete"})

        except Exception as e:
            print(f"[generate_image] Stream error: {e}")
            yield sse_event(
                {
                    "type": "error",
                    "stage": "stream",
                    "message": f"Unexpected stream failure: {str(e)}",
                }
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/upload-image")
async def upload_image_handler(file: UploadFile = File(...)):
    import shutil

    # Generate unique filename with "uploaded" prefix
    ext = Path(file.filename).suffix if file.filename else ".png"
    image_filename = f"uploaded_{uuid.uuid4().hex[:8]}{ext}"
    output_path = OUTPUTS_DIR / image_filename

    # Save the uploaded file
    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"/outputs/{image_filename}",
        "filename": image_filename,
    }
