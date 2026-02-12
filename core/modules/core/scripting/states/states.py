import asyncio
from core.modules.core.scripting.json.json import *

class States:
    def __init__(self):
        self.states = None

    async def init(self):
        self.states = Json()
        await self.states.init()

    async def create(self, name):
        await self.states.create(name)

    async def write(self, path, value):
        await self.states.write(path, value)

    async def get(self, path):
        return await self.states.get(path)

    async def exists(self, path):
        return await self.states.exists(path)