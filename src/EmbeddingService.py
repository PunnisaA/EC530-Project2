import asyncio
from messages import run_service
from payload import ImageAnnotatedPayload

async def create_embeddings(payload: ImageAnnotatedPayload):
    print(f"[EMBEDDING SERVICE] Received data for {payload.image_id}")
    print(f"[EMBEDDING SERVICE] Generating vectors for: {payload.metadata}")

async def main():
    await run_service(
        service_name="EmbeddingService",
        channel_name="annotation_channel",
        payload_class=ImageAnnotatedPayload,
        callback=create_embeddings
    )
    