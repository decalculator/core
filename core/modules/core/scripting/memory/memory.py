import asyncio
from core.modules.core.scripting.json.json import *

class Memory:
    def __init__(self):
        self.memory = None
        self.states = None

    async def init(self):
        self.memory = Json()
        await self.memory.init()

    async def create(self, name):
        await self.memory.create(name)

    async def write(self, path, value):
        await self.memory.write(path, value)

    async def get(self, path):
        return await self.memory.get(path)

    async def exists(self, path):
        return await self.memory.exists(path)