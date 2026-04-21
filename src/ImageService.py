import asyncio
from messages import run_service, publish_message
from payload import ImageProcPayload, ImageAnnotatedPayload

async def do_work(payload: ImageProcPayload):
    print(f"Working on {payload.image_id}")
    print(f"\n>>> [IMAGE SERVICE] RECEIVED MESSAGE!")
    print(f">>> Image ID: {payload.image_id}")
    print(f">>> Timestamp: {payload.timestamp}")

    detected_labels = ["cat", "sofa"]
    detected_vertices = [{"x": 10, "y": 20}, {"x": 50, "y": 100}]

    annotated_data = ImageAnnotatedPayload(
        image_id=payload.image_id,
        labels=detected_labels,
        vertices=detected_vertices
    )

    await publish_message(
        channel_name="annotation_channel", 
        payload=annotated_data
    )
    print(f">>> [IMAGE SERVICE] Sent annotations to 'annotation_channel'")

async def main():
    await run_service(
        service_name="ImageService",
        channel_name="upload_channel",
        payload_class=ImageProcPayload,
        callback=do_work
    )