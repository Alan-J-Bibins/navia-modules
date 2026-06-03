import json
import os
from gradio_client import Client
from config import settings
import shutil

client = Client("evalstate/flux1_schnell", token=settings.hf_token)

def generate_social_narrative_image(prompt:str, output_filename:str):
    style_suffix = (
        ", flat 2D cartoon style, simple minimalist vector illustration, "
        "bold clean outlines, soft pastel colors, calm flat background, zero clutter"
    )
    final_prompt = prompt + style_suffix
    
    print(f"Sending prompt to ZeroGPU Space: {final_prompt}")
    
    try:
        # 3. Trigger the prediction endpoint of the space
        # Tip: You can check the specific API names of any space by clicking "Use via API" at the bottom of its web page.
        result = client.predict(
            prompt=final_prompt,
            seed=0,                  # 0 usually means random seed
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,   # Flux Schnell requires exactly 4 steps
            api_name="/infer"        # The standard endpoint name for this space
        )
        
        # The space returns a tuple: (temp_image_path, seed_used)
        print(json.dumps(result, indent=4))
        temp_image_path = result[0]

        # Move/Rename the temporary file to your preferred directory
        if os.path.exists(temp_image_path):
            # os.rename(temp_image_path, output_filename)
            shutil.move(temp_image_path, output_filename)
            print(f"Success! Image saved as {output_filename}")
            return output_filename
            
    except Exception as e:
        print(f"An error occurred during generation: {e}")
        return None

story_scene = "A young 6-year-old boy with short brown hair eating breakfast at a kitchen table"
generate_social_narrative_image(story_scene, "storybook_page1.png")
