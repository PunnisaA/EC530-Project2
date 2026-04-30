from dataclasses import dataclass, asdict, field
import uuid
from datetime import datetime, timezone
import json
from typing import List, Tuple, Any

@dataclass
class ObjectAnnotation:
    vertices: List[Tuple[float, float]]
    label: str

# every other class will have the base payload and have unique event IDs
@dataclass(kw_only=True)
class UploadBasePayload:
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
    
@dataclass(kw_only=True)
class RequestBasePayload:
    user_id: None                     # ID for user to return it to the right user
    request_id: None
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
class ImageUploadPayload(UploadBasePayload):
    path: str
    file_type: str

@dataclass(kw_only=True)
class ImageProcPayload(UploadBasePayload):
    path: str
    encoded_image: str

# Embedding Service has two AIs, one to do the embedding from the image to vector space and the other is to detect 
# what the user is looking for and obtaining the embedding for that
# User's Query [CLI -> Embedding]
@dataclass(kw_only=True)
class QueryRequestPayload(RequestBasePayload):
    """CLI -> Embedding Service (Request Pathway)"""
    query_text: str
    top_k: int         # How many images to return

# Image Service [Image Service -> Embedding]
@dataclass(kw_only=True)
class ImageAnnotatedPayload(UploadBasePayload):
    objects: ObjectAnnotation

# Vector Index (Targeting Vector DB) [Embedding -> Vector Index]
@dataclass(kw_only=True)
class VectorIndexPayload(UploadBasePayload):
    vector: list[float]
    db_name: str         # shared database with document service
    table_name: str      # specific table for vector index

# Vector Index Request [Embedding -> Vector Index]
@dataclass(kw_only=True)
class VectorIndexRequestPayload(RequestBasePayload):
    vector: list[float]     # embedding of the requested query
    top_k: int              # number of images

# DocumentDBRequestPayload [Vector Index -> documentdb]
@dataclass(kw_only=True)
class DocumentDBRequestPayload(RequestBasePayload):
    image_id: list[dict]    # list of image ids because they should be the same number

# ImagesFound [documentdb -> CLI]
@dataclass(kw_only=True)
class ImagesFound(RequestBasePayload):
    encoded_images: list[str]   # list of encoded images

#  Document DB [image service -> document]
@dataclass(kw_only=True)
class DocumentDBPayload(UploadBasePayload):
    db_name: str         # shared database with vector index
    table_name: str      # specific table for document db
    storage_path: str
    objects: ObjectAnnotation

# CLI Confirmation
@dataclass(kw_only=True)
class CLIConfirmPayload(UploadBasePayload):
    status: str
    message: str

