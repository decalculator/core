import asyncio

async def ainput(prompt):
    return await asyncio.to_thread(input, prompt)