import asyncio
from core.modules.core.scripting.json.json import *

class Identifier:
    def __init__(self):
        self.identifier = None
        self.states = None

    async def init(self, states):
        self.states = states
        await self.states.create("identifier")
        await self.states.write("identifier/object", self)

        self.identifier = Json()
        await self.identifier.init()

    async def create(self, name):
        await self.identifier.create(name)
        await self.identifier.write(f"{name}/last_id", -1)

    async def write(self, path, value):
        await self.identifier.write(path, value)

    async def generate_id(self, path):
        path = await self.identifier.fix_path(path)
        new_id = await self.get_free_id(path)
        await self.identifier.write(f"{path}/{new_id}", {})
        await self.identifier.write(f"{path}/last_id", new_id)

        return new_id

    async def get_free_id(self, path):
        path = await self.identifier.fix_path(path)
        return await self.identifier.get(f"{path}/last_id") + 1

    async def get(self, path):
        return await self.identifier.get(path)

    async def exists(self, path):
        return await self.identifier.exists(path)