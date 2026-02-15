import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Moment:
    def __init__(self):
        self.moment = None
        self.variables = None

    async def init(self, variables):
        self.moment = Json()
        await self.moment.init()

        self.variables = variables
        await self.variables.create("moment")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("moment/object", obj)

    async def create(self, name):
        await self.moment.create(name)

    async def write(self, path, value):
        await self.moment.write(path, value)

    async def next_moment(self, path):
        await self.moment.write(path, await self.moment.get(path) + 1)

    async def previous_moment(self, path):
        await self.moment.write(path, await self.moment.get(path) - 1)

    async def get(self, path):
        return await self.moment.get(path)