import asyncio
from messages import run_service, run_service_req
from payload import DocumentDBPayload

async def document(payload: DocumentDBPayload):
    print(f"[Document Service] Received data for {payload.image_id}")



async def main():
    await asyncio.gather(
        run_service(
            service_name="DocumentService",
            channel_name="document_channel",
            payload_class=DocumentDBPayload,
            callback=document
        ),
        run_service_req(
            service_name="DocumentService",
            channel_name="document_channel",
            payload_class=DocumentDBPayload,
            callback=document
        )
    )
    