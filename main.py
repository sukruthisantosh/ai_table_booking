import webpage
import uvicorn
import asyncio

async def main():
    print("hello")
    config = uvicorn.Config(webpage.app)
    server = uvicorn.Server(config)
    await server.serve()  # noqa: F704

asyncio.run(main())
