# Image Generation requires additional authorization and is not allowed by default.

import base64
import sys
from openai import OpenAI
from config import settings


def generate_fanar_image(
    prompt: str = "A serene sunset over a mountain lake with reflections of colorful clouds and pine trees",
    output_path: str = "generated.png"
):
    client = OpenAI(
        base_url="https://api.fanar.qa/v1",
        api_key=settings.fanar_api_key,
    )

    response = client.images.generate(
        model="Fanar-Oryx-IG-2",
        prompt=prompt,
    )

    image_b64 = response.data[0].b64_json

    image_bytes = base64.b64decode(image_b64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)


if __name__ == "__main__":
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "A serene sunset over a mountain lake with reflections of colorful clouds and pine trees"
    )

    generate_fanar_image(prompt)
