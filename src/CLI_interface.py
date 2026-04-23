import asyncio
import uuid
from messages import redis_client, run_service
from payload import QueryRequestPayload, CLIConfirmPayload, ImageUploadPayload
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

        elif cmd == "search": #fake data from AI to help test
            msg = QueryRequestPayload(
                image_id=f"SRCH-{uuid.uuid4().hex[:6]}",
                query_text="Find photos of orange cats",
                user_id="user_vader_99"
            )
            print(f"[CLI] Sending QueryRequestPayload to 'query_request_channel'...")
            await redis_client.publish("query_request_channel", msg.to_json())

async def handle_confirmation(payload: CLIConfirmPayload):
    print(f"[NOTIFY] Status: {payload.status} | {payload.message}")

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
        cli_loop() # The foreground interactive part
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")




# import asyncio
# import redis.asyncio as redis
# import json
# import ImageService
# import EmbeddingService
# import VectorIndexService
# import DocumentDBService
# import upload

# # used to check_availability but can be used later?
# # async def check_availability():
# #     r = redis.Redis(host='localhost', decode_responses=True)
# #     pubsub = r.pubsub()
# #     await pubsub.subscribe("service_status")
# #     await asyncio.sleep(0.5) 
    
# #     print("Publisher: Checking online services...")
# #     await r.publish("broadcast", "STATUS")
# #     print("Waiting for services to check in...")
# #     try:
# #         # async with asyncio.timeout(10): # 10 seconds before timeout
# #             async for message in pubsub.listen():
# #                 if message["type"] == "message":
# #                     try:
# #                         data = json.loads(message["data"])
# #                         print(f"Confirmed: {data['service']} is {data['status']}")
# #                     except json.JSONDecodeError:
# #                         print(f"Received non-JSON message: {message['data']}")
                    
# #     except asyncio.TimeoutError:
# #         print("Timeout Error")
# #     finally:
# #         await pubsub.unsubscribe("service_status")
# #         await r.aclose()

# async def main():
#     await asyncio.gather(ImageService.main(), EmbeddingService.main(), 
#                          DocumentDBService.main(), VectorIndexService.main(), 
#                          upload.main())
#                          #, check_availability())

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#         # asyncio.run(check_availability())
#     except KeyboardInterrupt:
#         pass
