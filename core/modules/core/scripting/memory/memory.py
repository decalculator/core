import asyncio
from core.modules.core.scripting.json.json import *

class Memory:
    def __init__(self):
        self.memory = None
        self.states = None

    async def init(self, states):
        self.memory = Json()
        await self.memory.init()

        self.states = states
        await self.states.create("memory")
        await self.states.write("memory/object", self)

    async def create(self, name):
        await self.memory.create(name)

    async def write(self, path, value):
        await self.memory.write(path, value)

    async def get(self, path):
        return await self.memory.get(path)

    async def exists(self, path):
        return await self.memory.exists(path)