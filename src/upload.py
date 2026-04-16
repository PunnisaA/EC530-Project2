import asyncio
from messages import run_service

async def main():
    await run_service("upload")

if __name__ == "__main__":
    asyncio.run(main())