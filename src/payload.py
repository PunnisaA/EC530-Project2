from dataclasses import dataclass, asdict, field
import uuid
from datetime import datetime, timezone
import json

# every other class will have the base payload and have unique event IDs
@dataclass(kw_only=True)
class BasePayload:
    image_id: None     # ID of the image for both databases (must be provided from the CLI interface)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))      # unique ID for the specific event to auto-generate
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat()) # help of AI to generate this

    # asked AI to help create a way to change from object to JSON and vice versa (will be inherited by the other objects)
    def to_json(self) -> str:
        """Converts the object to a JSON string for Redis publishing."""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str: str):
        """Creates an object from a JSON string received from Redis."""
        data = json.loads(json_str)
        return cls(**data)

# Image Upload [CLI -> Payload]
@dataclass(kw_only=True)
class ImageUploadPayload(BasePayload):
    path: str
    file_type: str

@dataclass(kw_only=True)
class ImageProcPayload(BasePayload):
    encoded_image: str

# Embedding Service has two AIs, one to do the embedding from the image to vector space and the other is to detect 
# what the user is looking for and obtaining the embedding for that
# User's Query [CLI -> Embedding]
@dataclass(kw_only=True)
class QueryRequestPayload(BasePayload):
    """CLI -> Embedding Service (Request Pathway)"""
    query_text: str
    user_id: str          # ID for user to return it to the right user
    top_k: int = 5        # How many images to return

# Image Service [Image Service -> Embedding]
@dataclass(kw_only=True)
class ImageAnnotatedPayload(BasePayload):
    vertices: list[dict]
    labels: list[str]

# Vector Index (Targeting Vector DB) [Embedding -> Vector Index]
@dataclass(kw_only=True)
class VectorIndexPayload(BasePayload):
    vector: list[float]
    db_name: str         # shared database with document service
    table_name: str      # specific table for vector index
    
#  Document DB [image service -> document]
@dataclass(kw_only=True)
class DocumentDBPayload(BasePayload):
    metadata: dict       # The vertices and labels
    db_name: str         # shared database with vector index
    table_name: str      # specific table for document db
    storage_path: str

# CLI Confirmation
@dataclass(kw_only=True)
class CLIConfirmPayload(BasePayload):
    status: str
    message: str

# 1. img_upload req (with image)
# 2. image service will return the four points in an image 
# 3. payload for sending the four vertices to embedding 
# 4. payload for sending the vector index of the image to the vector index database?
# 5. payload for sending the image to the document database
# 4 and 5 needs to have the same ID corresponding between the image and vector embedding of that image?
# 6. payload to send information back to the CLI interface 

