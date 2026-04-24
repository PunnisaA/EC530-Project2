import asyncio
from messages import run_service, publish_message, run_service_req
from payload import VectorIndexPayload, CLIConfirmPayload, VectorIndexRequestPayload

async def vector_space(payload: VectorIndexPayload):
    print(f"[Vector Index] Received data for {payload.image_id}")

    confirmation = CLIConfirmPayload(
        image_id=payload.image_id,
        status="SUCCESS",
        message=f"Image {payload.image_id} successfully indexed in {payload.table_name}"
    )

    await publish_message("cli_confirm_channel", confirmation)

async def vector_request(payload: VectorIndexRequestPayload):
    print(f"[Vector Index] Received data for {payload.request_id}")

    image = [{"id":2}]
    db_info = VectorIndexPayload(
        request_id=payload.request_id,
        image_id=image
    )
    await publish_message(
        channel_name="document_db_request_channel",
        payload=db_info
    )
    print(f"[Vector Index] Sent info for {payload.request_id}")

async def main():
    await asyncio.gather(
        run_service(
        service_name="VectorIndexService",
        channel_name="vector_index_channel",
        payload_class=VectorIndexPayload,
        callback=vector_space
        ),
        run_service_req(
        service_name="VectorIndexService",
        channel_name="vector_index_request_channel",
        payload_class=VectorIndexRequestPayload,
        callback=vector_request
        )
    )

    