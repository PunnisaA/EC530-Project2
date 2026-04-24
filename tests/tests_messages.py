import asyncio
import uuid
from messages import redis_client
from payload import ImageProcPayload, QueryRequestPayload
import ImageService 

async def cli_loop():
    print("Commands: 'up' (Upload Test), 'search' (Query Test), 'exit'")

    while True:
        # to_thread keeps the input from blocking the ImageService logs
        cmd = await asyncio.to_thread(input, "\n[CLI] > ")
        cmd = cmd.strip().lower()

        if cmd == "exit": #does not quit the program fully until ^c
            break

        elif cmd == "up":
            msg = ImageProcPayload(
                image_id=f"IMG-{uuid.uuid4().hex[:6]}",
                path="./fake/path/cat.jpg",
                file_type="jpg"
            )
            print(f"[CLI] Sending ImageProcPayload to 'upload_channel'...")
            await redis_client.publish("upload_channel", msg.to_json())

        elif cmd == "search":
            msg = QueryRequestPayload(
                image_id=f"SRCH-{uuid.uuid4().hex[:6]}",
                query_text="Find photos of orange cats",
                user_id="user_vader_99"
            )
            print(f"[CLI] Sending QueryRequestPayload to 'query_request_channel'...")
            await redis_client.publish("query_request_channel", msg.to_json())

async def main():
    # This is the "Orchestrator" part
    # It starts the Image Service listener AND the CLI input loop
    print("🚀 Starting Image Service and CLI...")
    
    await asyncio.gather(
        ImageService.main(),  # The background listener
        cli_loop()           # The foreground interactive part
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")