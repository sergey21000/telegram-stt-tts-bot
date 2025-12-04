import asyncio
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url='http://localhost:8080/v1',
    api_key='sk-no-key-required',
)

async def async_streaming_chat():
    response = await client.chat.completions.create(
        model='gemma-2-2b-it-Q8_0.gguf',
        messages=[
            {'role': "system", 'content': 'You are a helpful assistant.'},
            {'role': "user", 'content': 'Как дела?'}
        ],
        # стриминг
        stream=True,
        temperature=0.7,
        max_tokens=100,
    )
    print('Асинхронный стриминг:')
    full_response = ''
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            full_response += content
    return full_response

async def main():
    await async_streaming_chat()

if __name__ == '__main__':
    asyncio.run(main())
