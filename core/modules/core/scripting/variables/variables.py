import asyncio
from core.modules.core.scripting.json.json import *

class Variables:
    def __init__(self):
        self.variables = None
        self.states = None

    async def init(self, states):
        self.variables = Json()
        await self.variables.init()

        self.states = states
        await self.states.create("variables")
        await self.states.write("variables/object", self)

    async def create(self, name):
        await self.variables.create(name)

    async def write(self, path, value):
        await self.variables.write(path, value)

    async def get(self, path):
        return await self.variables.get(path)

    async def exists(self, path):
        return await self.variables.exists(path)