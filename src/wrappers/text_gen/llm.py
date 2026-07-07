import time
import re
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
    model: Literal["gemma", "gemini", "deepseek", "fanar", 'qwen-3.6'],
    response_schema: type[T] | None = None,
) -> T | str | None:
    match model:
        case "gemini":
            return call_gemini(prompt, response_schema)
        case "gemma":
            return call_gemma(prompt, response_schema)
        case "deepseek":
            return call_deepseek(prompt, response_schema)
        case "fanar":
            return call_fanar(prompt, response_schema)
        case "qwen-3.6":
            return call_qwen3dot6(prompt, response_schema)


def call_gemini(prompt: str, response_schema: type[T] | None = None) -> T | str | None:
    client = genai.Client(api_key=settings.google_gemini_api_key)
    base_delay = 5
    attempts = 5
    for attempt in range(attempts):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.2,
                ),
            )

            if not response.text:
                return None

            print("Raw Response - Gemini")
            print(response.text)

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

def call_qwen3dot6(
    prompt: str, response_schema: type[T] | None = None
) -> T | str | None:

    if response_schema:
        json_schema = json.dumps(response_schema.model_json_schema(), indent=2)
        prompt = (
            f"{prompt}\n"
            f"Respond ONLY with a single valid JSON object matching this exact schema:\n\n{json_schema}\n\n"
            f"No other text should be present in the response, return only the json object without any markdown formatting. "
            f"Avoid surrounding the json in backticks or '```json```'. Simply return the raw json."
        )
    client = OpenAI(
        api_key=settings.opencode_api_key, base_url="https://opencode.ai/zen/go/v1"
    )

    response = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=[{"role": "user", "content": prompt}],
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

def call_fanar(prompt: str, response_schema: type[T] | None = None) -> T | str | None:
    if response_schema:
        json_schema = json.dumps(response_schema.model_json_schema(), indent=2)
        prompt = (
            f"{prompt}\n"
            f"Respond ONLY with a single valid JSON object matching this exact schema:\n\n{json_schema}\n\n"
            f"CRITICAL: Ensure lists/arrays are single JSON arrays formatted as [\"item1\", \"item2\"]. "
            f"Do NOT break a single list into consecutive separate arrays like [\"item1\"],[\"item2\"]. "
            f"No other text should be present in the response, return only the json object without any markdown formatting. "
            f"Avoid surrounding the json in backticks or '```json```'. Simply return the raw json."
        )

    client = OpenAI(
        base_url="https://api.fanar.qa/v1",
        api_key=settings.fanar_api_key,
    )

    response = client.chat.completions.create(
        model="Fanar",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if not content:
        return None

    print("FANAR RESPONSE: ", content)
    
    if response_schema:
        # 1. First-pass: clean up the broken split arrays syntax if present
        content = re.sub(r'\]\s*,\s*\[', ', ', content)
        
        # 2. Extract ONLY the JSON object body to strip markdown backticks and trailing junk
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            content = content[start_idx : end_idx + 1]
            
        return response_schema.model_validate_json(content)
        
    return content
