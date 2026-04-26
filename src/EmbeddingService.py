import asyncio
from messages import run_service, publish_message, run_service_req
from payload import ImageAnnotatedPayload, VectorIndexPayload, QueryRequestPayload, VectorIndexRequestPayload

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
    print(f"[EMBEDDING SERVICE] Received request for {payload.request_id}")
    
    mock_vector = [0.12, 0.45, -0.08, 0.99]

    vector_data = VectorIndexRequestPayload(
        request_id=payload.request_id,
        user_id=payload.user_id,
        vector = mock_vector,
        top_k=payload.top_k
    )
    await publish_message(
        channel_name="vector_index_request_channel",
        payload=vector_data
    )
    print(f"[EMBEDDING SERVICE] Vectors sent to 'vector_index_request_channel'")

async def main():
    await asyncio.gather(
    run_service(
        service_name="EmbeddingService",
        channel_name="annotation_channel",
        payload_class=ImageAnnotatedPayload,
        callback=create_embeddings
    ),
    run_service_req(
        service_name="EmbeddingService",
        channel_name="query_request_channel",
        payload_class=QueryRequestPayload,
        callback=request_payload
    )
    )
    