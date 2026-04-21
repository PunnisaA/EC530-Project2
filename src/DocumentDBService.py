import asyncio
from messages import run_service
from payload import DocumentDBPayload

async def document(payload: DocumentDBPayload):
    print(f"[Document Service] Received data for {payload.image_id}")
    # print(f"[EMBEDDING SERVICE] Generating vectors for: {payload.metadata}")

async def main():
    await run_service(
        service_name="DocumentService",
        channel_name="document_channel",
        payload_class=DocumentDBPayload,
        callback=document
    )
    