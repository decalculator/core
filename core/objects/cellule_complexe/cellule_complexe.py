import asyncio

async def entry(**kwargs):
    print("cellule_complexe > entry()\n")

    for i in range(10):
        await asyncio.sleep(3)
        print(f"cellule_complexe > {i}\n")