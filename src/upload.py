import asyncio
from messages import run_service, publish_message
import base64
from payload import ImageUploadPayload, ImageProcPayload
import os

async def encode(file_path):
    print(f"[UPLOAD DEBUG] Attempting to open file at: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File DOES NOT EXIST at the path: {file_path}")
        
    with open(file_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return encoded_image

async def upload_request(payload: ImageUploadPayload):
    # Wrapped the entire callback in a try/except to prevent silent crashes
    try:
        print(f"[UPLOAD SERVICE] Received data for {payload.image_id}")

        file_path = payload.path
        encoded_images = await encode(file_path)
        
        print(f"[UPLOAD DEBUG] Successfully encoded image. Publishing to ImageService...")

        await publish_message(
            channel_name="upload_channel", 
            payload=ImageProcPayload(
                image_id=payload.image_id,
                encoded_image=encoded_images
            )
        )
        print(f"[UPLOAD SERVICE] Encoded Image sent to ImageService")
        
    except Exception as e:
        # IF IT CRASHES, WE WILL FINALLY SEE IT HERE
        print(f"\n!!! [UPLOAD SERVICE CRASHED] !!!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}\n")

async def main():
    await run_service(
        service_name="UploadService",
        channel_name="upload_request_channel",
        payload_class=ImageUploadPayload,
        callback=upload_request
    )
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("upload shutting down...")