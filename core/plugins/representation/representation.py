import asyncio
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Representation:
    def __init__(self):
        self.representation = None
        self.variables = None

    async def init(self, variables = None):
        self.representation = Json()
        await self.representation.init()

        self.variables = variables

        if self.variables != None:
            await self.variables.create(Path("representation"))
            obj = Variable()
            await obj.init(self)
            await self.variables.write(Path("representation/object"), obj)

    async def create(self, name):
        await self.representation.create(name)

    async def write(self, path, value):
        await self.representation.write(path, value)

    async def get(self, path):
        return await self.representation.get(path)

    async def exists(self, path):
        return await self.representation.exists(path)