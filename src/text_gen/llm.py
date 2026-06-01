import time
import json
from openai import OpenAI
from typing import Literal, TypeVar
from google import genai
from pydantic import BaseModel
from config import settings
from google.genai import types
from ollama import chat, ChatResponse

T = TypeVar("T", bound=BaseModel)


def call_llm(
    prompt: str,
    model: Literal["gemma", "gemini", "deepseek"],
    response_schema: type[T] | None = None,
) -> T | str | None:
    match model:
        case "gemini":
            return call_gemini(prompt, response_schema)
        case "gemma":
            return call_gemma(prompt, response_schema)
        case "deepseek":
            return call_deepseek(prompt, response_schema)


def call_gemini(prompt: str, response_schema: type[T] | None = None) -> T | str | None:
    client = genai.Client(api_key=settings.google_gemini_api_key)
    base_delay = 5
    attempts = 5
    for attempt in range(attempts):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.2,
                ),
            )

            if not response.text:
                return None

            # print("Raw Response - Gemini")
            # print(response.text)

            if response_schema:
                return response_schema.model_validate_json(response.text)
            return response.text
        except Exception as e:
            err_msg = str(e).lower()
            is_rate_limit = (
                "429" in err_msg
                or "503" in err_msg
                or "resource exhausted" in err_msg
                or "rate limit" in err_msg
                or "unavailable" in err_msg
            )
            if not is_rate_limit or attempt == attempts - 1:
                raise
            wait = base_delay * (2 * attempt)
            print(
                f"Rate limit hit, retrying in {wait}s (attempt {attempt + 1}/{attempts})..."
            )
            time.sleep(wait)

    return None


def call_gemma(prompt: str, response_schema: type[T] | None = None) -> T | str | None:

    if response_schema:
        json_schema = json.dumps(response_schema.model_json_schema(), indent=2)
        prompt = f"{prompt}\nRespond ONLY with valid JSON matching this exact schema:\n```json\n{json_schema}\n```"

    response: ChatResponse = chat(
        model="gemma4:e2b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    if not response.message.content:
        return None

    # print("Raw Response - Gemma")
    # print(response.message.content)

    if response_schema:
        return response_schema.model_validate_json(response.message.content)
    return response.message.content


def call_deepseek(
    prompt: str, response_schema: type[T] | None = None
) -> T | str | None:

    if response_schema:
        json_schema = json.dumps(response_schema.model_json_schema(), indent=2)
        prompt = f"{prompt}\nRespond ONLY with valid JSON matching this exact schema:\n```json\n{json_schema}\n```"

    client = OpenAI(
        api_key=settings.opencode_api_key, base_url="https://opencode.ai/zen/go/v1"
    )

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    content = response.choices[0].message.content
    if not content:
        return None

    # print("Raw Response - DeepSeek V4 (OpenCode)")
    # print(content)

    if response_schema:
        return response_schema.model_validate_json(content)
    return content
