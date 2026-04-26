import asyncio
import uuid
from messages import redis_client, run_service, publish_message
from payload import QueryRequestPayload, CLIConfirmPayload, ImageUploadPayload, ImagesFound
import ImageService, EmbeddingService, DocumentDBService, VectorIndexService
import upload

async def cli_loop():
    print("Commands: 'up' (Upload Test), 'search' (Query Test), 'exit'")

    while True:
        # to_thread keeps the input from blocking the ImageService logs
        cmd = await asyncio.to_thread(input, "\n[CLI] > ")
        cmd = cmd.strip().lower()

        if cmd == "exit": #does not quit the program fully until ^c
            break

        elif cmd == "up": 
            path = input("File Path: ")
            file_type = input("File Type: ")
            # print(await upload.encode(path)) (testing if it works)

            image_id=f"IMG-{uuid.uuid4().hex[:6]}"
            
            msg = ImageUploadPayload(
                image_id=image_id,
                path=path,
                file_type=file_type
            )
            print(f"[CLI] Sending ImageUploadPayload to 'upload_request_channel'...")
            await redis_client.publish("upload_request_channel", msg.to_json())

        elif cmd == "search": 
            user = input("User: ")
            query = input("Query: ")
            image_count = input("Number of Images: ")
            

            await publish_message(
                channel_name="query_request_channel", 
                payload=QueryRequestPayload(
                request_id=f"REQ-{uuid.uuid4().hex[:6]}",
                query_text=query,
                user_id=user,
                top_k=image_count
            )
            )

            print(f"[CLI] Sending QueryRequestPayload to 'query_request_channel'...")
            # await redis_client.publish("query_request_channel", msg.to_json())

async def handle_confirmation(payload: CLIConfirmPayload):
    print(f"[NOTIFY] Status: {payload.status} | {payload.message}")

async def return_request(payload: ImagesFound):
    print(payload.encoded_images)

async def main():
    await asyncio.gather(
        ImageService.main(),  # The background listener
        EmbeddingService.main(),
        DocumentDBService.main(),
        VectorIndexService.main(),
        upload.main(),
        run_service(
            service_name="CLIListener",
            channel_name="cli_confirm_channel",
            payload_class=CLIConfirmPayload,
            callback=handle_confirmation
        ),
        run_service(
            service_name="CLIListener",
            channel_name="request_complete",
            payload_class=ImagesFound,
            callback=return_request
        ),     
        cli_loop() # The foreground interactive part
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")