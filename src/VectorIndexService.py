import asyncio
from messages import run_service, publish_message
from payload import VectorIndexPayload, CLIConfirmPayload

async def vector_space(payload: VectorIndexPayload):
    print(f"[Vector Index] Received data for {payload.image_id}")

    confirmation = CLIConfirmPayload(
        image_id=payload.image_id,
        status="SUCCESS",
        message=f"Image {payload.image_id} successfully indexed in {payload.table_name}"
    )

    await publish_message("cli_confirm_channel", confirmation)

async def main():
    await run_service(
        service_name="VectorIndexService",
        channel_name="vector_index_channel",
        payload_class=VectorIndexPayload,
        callback=vector_space
    )
    