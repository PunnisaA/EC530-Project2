import pytest
import asyncio
import json
import uuid
from messages import redis_client
from payload import ImageUploadPayload

@pytest.mark.asyncio
async def test_upload_to_index_flow():
    # 1. Setup PubSub and Subscribe
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("cli_confirm_channel")
    
    # Give Redis a moment to register the subscription
    await asyncio.sleep(1) 
    
    test_image_id = f"IMG-{uuid.uuid4().hex[:6]}"
    upload_msg = ImageUploadPayload(
        image_id=test_image_id,
        path="test_image.jpg", # MUST EXIST in root folder
        file_type="jpg"
    )

    # 2. Define the listener coroutine
    async def get_confirmation():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                print(f"\n[TEST DEBUG] Caught on cli_confirm_channel: {data}")
                # Use a broad check to be safe
                if test_image_id in str(data):
                    return data
        return None

    # 3. Start the listener AND then publish
    # We use gather to ensure the listener is ready to catch the message
    try:
        # Trigger the message
        await redis_client.publish("upload_request_channel", upload_msg.to_json())
        print(f"[TEST] Sent {test_image_id} to upload_request_channel")

        # Wait for the result
        final_status = await asyncio.wait_for(get_confirmation(), timeout=7.0)
        
        # 4. Assertions
        assert final_status["status"] == "SUCCESS"
        assert test_image_id in final_status["message"]
        print(f"[TEST] Success! Verified {test_image_id} reached the end.")
        
    except asyncio.TimeoutError:
        pytest.fail("Relay race failed: Message never reached the end of the chain.")
    finally:
        await pubsub.unsubscribe("cli_confirm_channel")