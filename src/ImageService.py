import asyncio
import redis.asyncio as redis

async def run_service():
    r = redis.Redis(host='localhost', decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("broadcast")

    print("ImageService is ONLINE.")
    async for message in pubsub.listen():
        print(f"I just heard: {message['data']}") 
        if message["type"] == "message" and message["data"] == "REPORT_STATUS": 
            await r.publish("service_status", '{"service": "ImageService", "status": "ready"}')
            print("Sent status back to Central!")

if __name__ == "__main__":
    asyncio.run(run_service())