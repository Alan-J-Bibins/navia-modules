import os
import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, AutoencoderKL, EulerDiscreteScheduler

MODEL_FILE_PATH = os.path.abspath("./realvisxlV50_v50LightningBakedvae.safetensors")
SAMPLE_PROMPT = "children book illustration style, a happy friendly cat sitting on a desk waving hello, vector art, bright colors"

def generate_lightning_image(baked_checkpoint_path: str, prompt: str, output_path: str = "output.png"):
    print("🚀 Initializing clean SDXL framework...")
    
    # 1. Load components on CPU first to avoid instant VRAM spikes
    print("📦 Loading baked UNet and VAE components to CPU...")
    unet = UNet2DConditionModel.from_single_file(
        baked_checkpoint_path, 
        subfolder="unet", 
        torch_dtype=torch.float16
    )
    vae = AutoencoderKL.from_single_file(
        baked_checkpoint_path, 
        subfolder="vae", 
        torch_dtype=torch.float16
    )

    # 2. Build pipeline
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        unet=unet,
        vae=vae,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    
    print("⚙️ Adjusting inference scheduler layout...")
    pipe.scheduler = EulerDiscreteScheduler.from_config(
        pipe.scheduler.config, 
        timestep_spacing="trailing"
    )
    
    # 3. CRITICAL MEMORY OPTIMIZATIONS FOR 8GB VRAM
    # Do NOT use pipe.to("cuda") when using sequential offloading!
    print("🔒 Applying sequential CPU offloading and VRAM optimizations...")
    pipe.enable_sequential_cpu_offload() # Dynamically moves layers into VRAM on-the-fly
    pipe.enable_attention_slicing()      # Splits heavy attention matrices into chunks
    pipe.enable_vae_tiling()             # Decodes the image in tiles to prevent VAE OOMs

    print(f"🎨 Running fast inference (4 steps) for prompt: '{prompt}'")
    
    # Explicitly clear cached garbage allocations before firing inference
    torch.cuda.empty_cache()

    with torch.inference_mode():
        image = pipe(
            prompt=prompt,
            negative_prompt="blurry, low quality, distorted, dark background, scary, photorealistic, bad anatomy",
            num_inference_steps=4,   
            guidance_scale=1.0, 
            width=768,               
            height=768
        ).images[0]

    image.save(output_path)
    print(f"✨ Success! Saved asset to {output_path}")

def create_image(prompt:str = "", output_name="output.png"):
    image_prompt = ""
    if(prompt == ""):
        image_prompt = SAMPLE_PROMPT
    else:
        image_prompt = prompt
    generate_lightning_image(MODEL_FILE_PATH, image_prompt, output_name)

if __name__ == "__main__":
    generate_lightning_image(MODEL_FILE_PATH, SAMPLE_PROMPT, "story_cat_hello.png")
