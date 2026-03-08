import asyncio
from core.modules.json.json import *
from core.modules.path.path import *
from core.modules.variable.variable import *

class Signals:
    def __init__(self):
        self.signals = None
        self.variables = None

    async def init(self, variables):
        self.signals = Json()
        await self.signals.init()

        self.variables = variables
        await self.variables.create(Path("signals"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("signals/object"), obj)

    async def create(self, name):
        await self.signals.create(name)

    async def write(self, path, value):
        await self.signals.write(path, value)

    async def get(self, path):
        return await self.signals.get(path)