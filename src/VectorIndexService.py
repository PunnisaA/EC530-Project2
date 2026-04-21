import asyncio
from messages import run_service
from payload import VectorIndexPayload

async def vector_space(payload: VectorIndexPayload):
    print(f"[Vector Index] Received data for {payload.image_id}")
    # print(f"[EMBEDDING SERVICE] Generating vectors for: {payload.metadata}")

async def main():
    await run_service(
        service_name="VectorIndexService",
        channel_name="vector_index_channel",
        payload_class=VectorIndexPayload,
        callback=vector_space
    )
    