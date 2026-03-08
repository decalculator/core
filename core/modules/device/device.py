import asyncio
import platform
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Device:
    def __init__(self):
        self.device = None
        self.variables = None
        self.console = None

    async def init(self, variables, console):
        self.device = Json()
        await self.device.init()

        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("console > ready")
            await self.console.write(Path("core"), console_core)

        self.variables = variables
        await self.variables.create(Path("device"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("device/object"), obj)

    async def create(self, name):
        await self.device.create(name)

    async def write(self, path, value):
        await self.device.write(path, value)

    async def get(self, path):
        return await self.device.get(path)

    async def get_os(self):
        return [platform.system(), platform.release(), platform.version()]

    async def get_separator(self):
        return os.sep