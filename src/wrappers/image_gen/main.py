from typing import Literal
from wrappers.image_gen.gemini import generate_gemini_image
from wrappers.image_gen.comfyui import generate_comfyui_image
from wrappers.image_gen.fanar import generate_fanar_image


def generate_image(
    prompt: str,
    model: Literal["gemini", "comfyui", "fanar"],
    output_path: str = "generated.png",
    on_progress=None,
) -> str:
    match model:
        case "gemini":
            generate_gemini_image(prompt=prompt, output_path=output_path)
        case "comfyui":
            generate_comfyui_image(
                prompt=prompt, output_path=output_path, on_progress=on_progress
            )
        case "fanar":
            generate_fanar_image(prompt=prompt, output_path=output_path)
    return output_path
