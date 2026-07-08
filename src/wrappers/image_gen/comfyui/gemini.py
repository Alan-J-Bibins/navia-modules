import json
import uuid
import websocket
import requests
from config import settings
import random

COMFYUI_SERVER_ADDRESS = settings.comfyui_server_address
WORKFLOW_PATH = "gemini_comfyui_workflow.json"

STYLE_SUFFIX = "heartwarming, minimalist illustration.The style is cozy slice-of-life, featuring simple cute character designs with dot eyes and rosy blush cheeks. Soft pastel color palette with muted blues, warm creams, and gentle peachy tones. Delicate, clean line art. Warm, nostalgic atmosphere, smooth gradients, subtle shading and texture, clean digital art."


def _get_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    """Fetches the generated image bytes from the ComfyUI server."""
    print(
        f"[_get_image] Fetching filename={filename}, subfolder={subfolder}, type={folder_type}"
    )
    resp = requests.get(
        f"http://{COMFYUI_SERVER_ADDRESS}/view",
        params={"filename": filename, "subfolder": subfolder, "type": folder_type},
    )
    print(
        f"[_get_image] Response status: {resp.status_code}, size: {len(resp.content)} bytes"
    )
    return resp.content


def _get_output_image_bytes(prompt_id: str) -> bytes:
    """Retrieves the first generated image from ComfyUI history."""
    print(f"[_get_output_image_bytes] Fetching history for prompt_id={prompt_id}")
    history_resp = requests.get(f"http://{COMFYUI_SERVER_ADDRESS}/history/{prompt_id}")
    print(
        f"[_get_output_image_bytes] History response status: {history_resp.status_code}"
    )
    history = history_resp.json()

    if prompt_id not in history:
        print(f"[_get_output_image_bytes] ERROR: prompt_id {prompt_id} not in history!")
        raise RuntimeError(f"Prompt ID {prompt_id} not found in ComfyUI history")

    for node_id, node_output in history[prompt_id]["outputs"].items():
        if "images" in node_output:
            img = node_output["images"][0]
            return _get_image(img["filename"], img["subfolder"], img["type"])

    raise RuntimeError("Image generation completed but no output image was found.")


def comfyui_generate_gemini_image(
    prompt: str,
    output_path: str = "output.png",
    positive_prompt_node_id: str = "1",
    workflow_path: str = WORKFLOW_PATH,
    on_progress=None,
) -> str:
    """Generate an image via Gemini ComfyUI node and save it to disk."""
    print(f"[generate_comfyui_image] Starting generation...")

    client_id = str(uuid.uuid4())
    print(f"[generate_comfyui_image] Generated client_id: {client_id}")

    print(f"[generate_comfyui_image] Loading workflow from {workflow_path}")
    with open(workflow_path, "r") as f:
        workflow = json.load(f)

    print(
        f"[generate_comfyui_image] Injecting prompt into node {positive_prompt_node_id}"
    )
    workflow[positive_prompt_node_id]["inputs"]["prompt"] = f"{prompt}\n{STYLE_SUFFIX}"
    seed = random.sample(range(1000000, 9000000), 1)[0]
    print(
        f"[generate_comfyui_image] Injecting new seed into node {positive_prompt_node_id}: {seed}"
    )
    workflow[positive_prompt_node_id]["inputs"]["seed"] = seed

    print("[generate_comfyui_image] Connecting WebSocket before queuing...")
    ws = websocket.WebSocket()
    ws.settimeout(300.0)
    ws.connect(f"ws://{COMFYUI_SERVER_ADDRESS}/ws?clientId={client_id}")
    print("[generate_comfyui_image] WebSocket connected")

    try:
        print("[generate_comfyui_image] Queuing prompt...")
        payload = {"prompt": workflow, "client_id": client_id}
        resp = requests.post(
            f"http://{COMFYUI_SERVER_ADDRESS}/prompt",
            data=json.dumps(payload).encode("utf-8"),
        )
        prompt_response = resp.json()
        print(f"[generate_comfyui_image] Queue response: {prompt_response}")
        prompt_id = prompt_response["prompt_id"]

        print(
            f"[generate_comfyui_image] Waiting for completion of prompt_id={prompt_id}"
        )
        message_count = 0
        while True:
            msg = ws.recv()
            message_count += 1

            if isinstance(msg, str):
                data = json.loads(msg)
                msg_type = data["type"]

                if msg_type == "executing":
                    exec_data = data["data"]
                    if (
                        exec_data["node"] is None
                        and exec_data["prompt_id"] == prompt_id
                    ):
                        print("[generate_comfyui_image] Completion signal received!")
                        break
                    if on_progress:
                        on_progress({"stage": "executing", "node": exec_data["node"]})

                elif msg_type == "progress":
                    if on_progress:
                        on_progress(
                            {
                                "stage": "sampling",
                                "value": data["data"]["value"],
                                "max": data["data"]["max"],
                            }
                        )

                elif msg_type == "execution_error":
                    if on_progress:
                        on_progress(
                            {
                                "stage": "error",
                                "message": data["data"].get("exception_message", ""),
                            }
                        )
    finally:
        ws.close()

    print("[generate_comfyui_image] Retrieving image bytes...")
    image_bytes = _get_output_image_bytes(prompt_id)
    print(
        f"[generate_comfyui_image] Got {len(image_bytes)} bytes, saving to {output_path}"
    )
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"[generate_comfyui_image] Successfully saved to {output_path}")
    return output_path
