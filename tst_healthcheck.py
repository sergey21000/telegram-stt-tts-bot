import asyncio
import aiohttp
from llama_cpp_py import LlamaAsyncServer, LlamaAsyncClient, LlamaReleaseManager


openai_base_url = 'http://127.0.0.1:8080/v1'
llm_client = LlamaAsyncClient(openai_base_url=openai_base_url)

async def main():
    res = await llm_client.check_health()
    print('llm_client.check_health:')
    print(res)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(openai_base_url + '/health') as resp:
            data = await resp.json()
            print('aiohttp get:')
            print(data)

if __name__ == '__main__':
    asyncio.run(main())

