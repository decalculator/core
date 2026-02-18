import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Console:
    def __init__(self):
        self.console = None

    async def init(self, variables):
        self.console = Json()
        await self.console.init()

        self.variables = variables
        await self.variables.create("console")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("console/object", obj)

    async def create(self, name):
        await self.console.create(name)

    async def write(self, path, value):
        await self.console.write(path, value)

    async def get(self, path):
        return await self.console.get(path)