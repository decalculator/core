import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Moment:
    def __init__(self):
        self.moment = None
        self.variables = None
        self.console = None

    async def init(self, variables, console = None):
        self.moment = Json()
        await self.moment.init()

        self.console = console
        if self.console != None:
            console_core = await self.console.get("core")
            console_core.append("console > ready")
            await self.console.write("core", console_core)

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