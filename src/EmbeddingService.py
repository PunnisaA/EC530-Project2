import asyncio
from messages import run_service, publish_message
from payload import ImageAnnotatedPayload, VectorIndexPayload, QueryRequestPayload

async def create_embeddings(payload: ImageAnnotatedPayload):
    print(f"[EMBEDDING SERVICE] Received data for {payload.image_id}")
    print(f"[EMBEDDING SERVICE] Generating vectors for: {payload.image_id}")

    mock_vector = [0.12, 0.45, -0.08, 0.99]
    vector_data = VectorIndexPayload(
        image_id=payload.image_id,
        vector=mock_vector,
        db_name="image_vault",
        table_name="embeddings_v1"
    )

    await publish_message(
        channel_name="vector_index_channel", 
        payload=vector_data
    )
    print(f"[EMBEDDING SERVICE] Vectors sent to 'vector_index_channel'")

async def request_payload(payload: QueryRequestPayload):
    print(f"[EMBEDDING SERVICE] Received data for {payload.image_id}")

async def main():
    await asyncio.gather(
    run_service(
        service_name="EmbeddingService",
        channel_name="annotation_channel",
        payload_class=ImageAnnotatedPayload,
        callback=create_embeddings
    ),
    run_service(
        service_name="EmbeddingService",
        channel_name="query_request_channel",
        payload_class=QueryRequestPayload,
        callback=request_payload
    )
    )
    