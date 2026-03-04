import asyncio
from core.modules.json.json import *

class Temp:
    def __init__(self):
        self.temp = None

    async def init(self):
        self.temp = Json()
        await self.temp.init()

    async def create(self, name):
        await self.temp.create(name)

    async def write(self, path, value):
        await self.temp.write(path, value)

    async def generate_id(self, path):
        path = await self.temp.fix_path(path)
        new_id = await self.get_free_id(path)
        await self.temp.write(f"{path}/{new_id}", {})
        await self.temp.write(f"{path}/last_id", new_id)

        return new_id

    async def get_free_id(self, path):
        path = await self.temp.fix_path(path)
        return await self.temp.get(f"{path}/last_id") + 1

    async def get(self, path):
        return await self.temp.get(path)

    async def exists(self, path):
        return await self.temp.exists(path)