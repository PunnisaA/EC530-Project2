import asyncio
from messages import run_service, publish_message
import base64
from payload import ImageUploadPayload, ImageProcPayload

async def encode(file_path):
    with open(file_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return encoded_image

async def upload_request(payload: ImageUploadPayload):
    print(f"[UPLOAD SERVICE] Received data for {payload.image_id}")
    # print(f"[EMBEDDING SERVICE] Generating vectors for: {payload.image_id}")

    file_path = payload.path
    # print(file_path)
    encoded_images = await encode(file_path)
    # print(encoded_images)

    await publish_message(
        channel_name="upload_channel", 
        payload=ImageProcPayload(
            image_id=payload.image_id,
            encoded_image=encoded_images
        )
    )
    print(f"[UPLOAD SERVICE] Encoded Image sent to ImageService'")

async def main():
    await run_service(
        service_name="UploadService",
        channel_name="upload_request_channel",
        payload_class=ImageUploadPayload,
        callback=upload_request
    )
    