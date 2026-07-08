import sys
from google import genai
from google.genai import types
from config import settings

STYLE_PREFIX = (
    "heartwarming, minimalist illustration.The style is cozy slice-of-life, featuring simple cute character designs with dot eyes and rosy blush cheeks. Soft pastel color palette with muted blues, warm creams, and gentle peachy tones. Delicate, clean line art. Warm, nostalgic atmosphere, smooth gradients, subtle shading and texture, clean digital art."
)


def generate_gemini_image(
    prompt: str = "A serene sunset over a mountain lake",
    output_path: str = "generated.png",
):
    client = genai.Client(api_key=settings.google_gemini_api_key)

    response = client.models.generate_images(
        model="gemini-3.1-flash-image",
        prompt=f"{STYLE_PREFIX}\n{prompt}",
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/png",
            aspect_ratio="16:9"
        ),
    )

    if hasattr(response, "prompt_feedback"):
        print(f"[gemini] Prompt feedback: {response.prompt_feedback}")
    if hasattr(response, "generated_images") and not response.generated_images:
        print(f"[gemini] Full response: {response}")

    if not response.generated_images:
        raise RuntimeError(
            "No images were generated — prompt may have been blocked by safety filters"
        )

    if not response.generated_images:
        raise RuntimeError("No images were generated")

    generated = response.generated_images[0]
    if generated.image is None or generated.image.image_bytes is None:
        raise RuntimeError("Generated image data is missing")

    with open(output_path, "wb") as f:
        f.write(generated.image.image_bytes)


if __name__ == "__main__":
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "A serene sunset over a mountain lake with reflections of colorful clouds and pine trees"
    )
    generate_gemini_image(prompt)
