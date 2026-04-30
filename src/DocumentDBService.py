import asyncio
from messages import run_service, run_service_req, publish_message
from payload import DocumentDBPayload, DocumentDBRequestPayload, ImagesFound
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Image_Database"]
collection = db["images"]

async def document(payload: DocumentDBPayload):
    print(f"[Document Service] Received data for {payload.image_id}")

    doc = {
        "image_id": payload.image_id,
        "db_name": payload.db_name,
        "table_name": payload.table_name,
        "storage_path": payload.storage_path,
        "objects": [
            {
                "label": obj["label"],
                "vertices": obj["vertices"]
            }
            for obj in payload.objects
        ]
    }

    database = client[payload.db_name]
    collection = database[payload.table_name]

    collection.insert_one(doc)
    print(f"[Document Service] Stored image {payload.image_id}")

async def document_request(payload: DocumentDBRequestPayload):
    print(f"[Document Service] Received data for {payload.request_id}")
    
    encoded_images = ['asjdaslkdjlasjdklajlds', 'skadjsakldjkalsjdlkasjlkd']
    image_found = ImagesFound(
        request_id=payload.request_id,
        user_id=payload.user_id,
        encoded_images=encoded_images
    )
    await publish_message(
        channel_name="request_complete",
        payload=image_found
    )
    print(f"[Document Service] Sent info for {payload.request_id}")

async def main():
    await asyncio.gather(
        run_service(
            service_name="DocumentService",
            channel_name="document_channel",
            payload_class=DocumentDBPayload,
            callback=document
        ),
        run_service_req(
            service_name="DocumentService",
            channel_name="documentdb_request_channel",
            payload_class=DocumentDBRequestPayload,
            callback=document_request
        )
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("DocumentDB shutting down...")
    