import asyncio
import aiohttp
import random

prefix = 'http://192.168.0.106'
requests = ['/healthz', '', '/test', '/doc', '/healthz/']
count = 100


async def open_connect(url: str, session: aiohttp.ClientSession()):
    response = await session.get(url)
    if '/healthz' in url:
        assert response.status == 200
    else:
        assert response.status != 200
    print(response.status, url)


async def main():
    async with aiohttp.ClientSession() as session:
        urls = []
        for i in range(count):
            urls.append(prefix + random.choice(requests))
        for url in urls:
            await open_connect(url, session)


if __name__ == '__main__':
    asyncio.run(main())