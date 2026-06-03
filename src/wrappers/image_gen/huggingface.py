from huggingface_hub import InferenceClient
from config import settings

def hf_create_image(prompt:str, output_path:str):
    client = InferenceClient(api_key=settings.hf_token)

    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-dev"
    )

    image.save(output_path)

if __name__ == "__main__":
    hf_create_image(prompt="A serene lake surrounded by mountains at sunset, photorealistic style", output_path="Gen.png")
