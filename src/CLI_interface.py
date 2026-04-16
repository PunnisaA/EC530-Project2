import asyncio
import redis.asyncio as redis
import json
import ImageService
import EmbeddingService
import VectorIndexService
import DocumentDBService
import upload

async def check_availability():
    r = redis.Redis(host='localhost', decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("service_status")
    await asyncio.sleep(0.5) 
    
    print("Publisher: Checking online services...")
    await r.publish("broadcast", "STATUS")
    print("Waiting for services to check in...")
    try:
        # async with asyncio.timeout(10): # 10 seconds before timeout
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        print(f"Confirmed: {data['service']} is {data['status']}")
                    except json.JSONDecodeError:
                        print(f"Received non-JSON message: {message['data']}")
                    
    except asyncio.TimeoutError:
        print("Timeout Error")
    finally:
        await pubsub.unsubscribe("service_status")
        await r.aclose()

async def main():
    await asyncio.gather(ImageService.main(), EmbeddingService.main(), 
                         DocumentDBService.main(), VectorIndexService.main(), 
                         upload.main(), check_availability())

if __name__ == "__main__":
    try:
        asyncio.run(main())
        # asyncio.run(check_availability())
    except KeyboardInterrupt:
        pass
