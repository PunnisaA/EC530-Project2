import asyncio
from messages import run_service, publish_message
from payload import ImageProcPayload, ImageAnnotatedPayload, DocumentDBPayload
from typing import List, Tuple

async def to_tuple(v):
    return (v["x"], v["y"])

async def do_work(payload: ImageProcPayload):
    print(f"Working on {payload.image_id}")
    print(f"\n>>> [IMAGE SERVICE] RECEIVED MESSAGE!")
    print(f">>> Image ID: {payload.image_id}")
    print(f">>> Timestamp: {payload.timestamp}")

    detected_labels = ["cat", "sofa"]
    detected_vertices = [
    [{"x": 10, "y": 20}, {"x": 15, "y": 25}],   # vertices for "cat"
    [{"x": 50, "y": 100}, {"x": 60, "y": 110}]  # vertices for "sofa"   
    ]

    annotated_objects = [
    {
        "label": label,
        "vertices": [(v["x"], v["y"]) for v in verts]
    }
    for label, verts in zip(detected_labels, detected_vertices)
    ]

    annotated_data = ImageAnnotatedPayload(
        image_id=payload.image_id,
        objects=annotated_objects

    )

    await publish_message(
        channel_name="annotation_channel", 
        payload=annotated_data
    )
    print(f">>> [IMAGE SERVICE] Sent annotations to 'annotation_channel'")

    await publish_message(
        channel_name="document_channel",
        payload=DocumentDBPayload(
            image_id=payload.image_id,
            db_name="Image_Database",
            table_name="images",
            storage_path=payload.path,
            objects=annotated_objects
        )
    )
    print(f">>> [IMAGE SERVICE] Sent annotations to 'document_channel'")

async def main():
    await run_service(
        service_name="ImageService",
        channel_name="upload_channel",
        payload_class=ImageProcPayload,
        callback=do_work
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("ImageService shutting down...")