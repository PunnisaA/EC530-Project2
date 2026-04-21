import asyncio
from messages import run_service
from payload import ImageProcPayload

async def do_work(payload: ImageProcPayload):
    print(f"Working on {payload.image_id}")
    print(f"\n>>> [IMAGE SERVICE] RECEIVED MESSAGE!")
    print(f">>> Image ID: {payload.image_id}")
    print(f">>> Timestamp: {payload.timestamp}")

async def main():
    await run_service(
        service_name="ImageService",
        channel_name="upload_channel",
        payload_class=ImageProcPayload,
        callback=do_work
    )
    