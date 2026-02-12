import asyncio
from core.modules.core.scripting.json.json import *

class Symbols:
    def __init__(self):
        self.symbols = None
        self.states = None

    async def init(self, states):
        self.symbols = Json()
        await self.symbols.init()
        self.states = states
        await self.states.create("symbols")
        await self.states.write("symbols/object", self)

    async def create(self, name):
        await self.symbols.create(name)

    async def write(self, path, value):
        await self.symbols.write(path, value)

    async def get(self, path):
        return await self.symbols.get(path)