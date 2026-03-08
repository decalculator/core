import asyncio
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Symbols:
    def __init__(self):
        self.symbols = None
        self.variables = None
        self.console = None

    async def init(self, variables, console = None):
        self.symbols = Json()
        await self.symbols.init()

        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("symbols > ready")
            await self.console.write(Path("core"), console_core)

        self.variables = variables
        await self.variables.create(Path("symbols"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("symbols/object"), obj)

    async def create(self, name):
        await self.symbols.create(name)

    async def write(self, path, value):
        await self.symbols.write(path, value)

    async def get(self, path):
        return await self.symbols.get(path)