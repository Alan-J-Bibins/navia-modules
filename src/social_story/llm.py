import json
from typing import Literal
from google import genai
from social_story.config import settings
from google.genai import types
from ollama import chat, ChatResponse

from social_story.model import SocialStorySchema


def call_llm(
    prompt: str, model: Literal["gemma", "gemini"]
) -> SocialStorySchema | None:
    match model:
        case "gemini":
            return call_gemini(prompt)
        case "gemma":
            return call_gemma(prompt)


def call_gemini(prompt: str) -> SocialStorySchema | None:
    client = genai.Client(api_key=settings.google_gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SocialStorySchema,
            temperature=0.2,
        ),
    )
    if response.text:
        print("Raw Response - Gemini")
        print(response.text)
        story_schema = SocialStorySchema.model_validate_json(response.text)
        return story_schema


def call_gemma(prompt: str) -> SocialStorySchema | None:

    json_schema = json.dumps(SocialStorySchema.model_json_schema(), indent=2)
    full_prompt = f"{prompt}\nRespond ONLY with valid JSON matching this exact schema:\n```json\n{json_schema}\n```"

    response: ChatResponse = chat(
        model="gemma4:e2b",
        messages=[{"role": "user", "content": full_prompt}],
        format="json",
    )
    if response.message.content:
        print("Raw Response - Gemma")
        print(response.message.content)
        story_schema = SocialStorySchema.model_validate_json(response.message.content)
        return story_schema
