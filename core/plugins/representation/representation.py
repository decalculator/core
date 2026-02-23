import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Representation:
    def __init__(self):
        self.representation = None
        self.variables = None

    async def init(self, variables):
        self.representation = Json()
        await self.representation.init()

        self.variables = variables
        await self.variables.create("representation")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("representation/object", obj)

    async def create(self, name):
        await self.representation.create(name)

    async def write(self, path, value):
        await self.representation.write(path, value)

    async def get(self, path):
        return await self.representation.get(path)