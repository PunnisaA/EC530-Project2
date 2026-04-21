import asyncio
import redis.asyncio as redis
import json
from typing import Type, Callable, Awaitable
from payload import BasePayload

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)

async def run_service(
    service_name: str, 
    channel_name: str, 
    payload_class: Type[BasePayload], 
    callback: Callable[[BasePayload], Awaitable[None]]
):
    """
    A generic listener for any service.
    :param service_name: Name for logging (e.g., "ImageService")
    :param channel_name: Redis channel to listen to
    :param payload_class: The Class to use for .from_json()
    :param callback: The async function to run when a message arrives
    """
    # Assuming redis_client is initialized elsewhere or passed in
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel_name)
    
    print(f"[{service_name}] Started. Listening on '{channel_name}'...")

    async for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                # 1. Unpack JSON into the specific object type
                raw_data = message['data'].decode('utf-8')
                payload = payload_class.from_json(raw_data)
                
                # 2. Pass the object to the specific service logic
                await callback(payload)
                
            except Exception as e:
                print(f"[{service_name}] Error processing message: {e}")

if __name__ == "__main__":
    asyncio.run(run_service())


# async def run_service(serviceName): #checking if the status of a service is ready and can just put name in
#     r = redis.Redis(host='localhost', decode_responses=True)
#     pubsub = r.pubsub()
#     await pubsub.subscribe("broadcast")

#     print(f"{serviceName} is ONLINE.")
#     async for message in pubsub.listen():
#         print(f"I just heard: {message['data']}") 
#         if message["type"] == "message" and message["data"] == "STATUS": 
#             payload = {"service": serviceName, "status": "ready"}
#             await r.publish("service_status", json.dumps(payload))
#             print("Sent status back to Central!")
