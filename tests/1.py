import asyncio

async def function(delay):
    print(delay)
    await asyncio.sleep(delay)

async def main():
    task1 = asyncio.create_task(function(1))
    task2 = asyncio.create_task(function(2))
    task3 = asyncio.create_task(function(3))

    tasks = [task1, task2, task3]

    for task in tasks:
        await task

asyncio.run(main())