import pytest_asyncio
import asyncio
import sys
from pathlib import Path

# Fix paths
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "src"))

# Import all services
import ImageService, EmbeddingService, DocumentDBService, VectorIndexService, upload

@pytest_asyncio.fixture(scope="module", autouse=True)
async def run_all_services():
    print("\n[FIXTURE] Initializing background services...")
    
    # We use asyncio.create_task to put these in the background
    service_tasks = [
        asyncio.create_task(ImageService.main(), name="ImageService"),
        asyncio.create_task(EmbeddingService.main(), name="EmbeddingService"),
        asyncio.create_task(DocumentDBService.main(), name="DocumentDBService"),
        asyncio.create_task(VectorIndexService.main(), name="VectorIndexService"),
        asyncio.create_task(upload.main(), name="UploadService")
    ]
    
    # CRITICAL: This sleep lets the services connect to Redis 
    # without blocking the main test execution.
    await asyncio.sleep(0.5)
    print("[FIXTURE] Services running in background. Starting tests...")
    
    yield  # The tests run here
    
    print("\n[FIXTURE] Cleaning up services...")
    for task in service_tasks:
        task.cancel()
    
    # Wait for everything to close
    await asyncio.gather(*service_tasks, return_exceptions=True)