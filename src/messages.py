import asyncio
import redis.asyncio as redis
import json

async def run_service(serviceName): #checking if the status of a service is ready and can just put name in
    r = redis.Redis(host='localhost', decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("broadcast")

    print(f"{serviceName} is ONLINE.")
    async for message in pubsub.listen():
        print(f"I just heard: {message['data']}") 
        if message["type"] == "message" and message["data"] == "STATUS": 
            payload = {"service": serviceName, "status": "ready"}
            await r.publish("service_status", json.dumps(payload))
            print("Sent status back to Central!")

if __name__ == "__main__":
    asyncio.run(run_service())