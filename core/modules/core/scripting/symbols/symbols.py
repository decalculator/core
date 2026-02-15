import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Symbols:
    def __init__(self):
        self.symbols = None
        self.variables = None

    async def init(self, variables):
        self.symbols = Json()
        await self.symbols.init()

        self.variables = variables
        await self.variables.create("symbols")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("symbols/object", obj)

    async def create(self, name):
        await self.symbols.create(name)

    async def write(self, path, value):
        await self.symbols.write(path, value)

    async def get(self, path):
        return await self.symbols.get(path)