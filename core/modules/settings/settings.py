import asyncio
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Settings:
    def __init__(self):
        self.variables = None
        self.loader = None
        self.settings = None
        self.console = None

    async def init(self, variables, loader, console = None):
        self.variables = variables
        await self.variables.create(Path("settings"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("settings/object"), obj)

        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("settings > ready")
            await self.console.write(Path("core"), console_core)

        self.loader = loader
        self.settings = Json()
        await self.settings.init()

    async def create(self, name):
        await self.settings.create(name)

    async def remove(self, path):
        await self.settings.remove(path)

    async def get(self, path):
        return await self.settings.get(path)

    async def write(self, path, value, mode = 0):
        await self.settings.write(path, value, mode)

    async def enable(self, settings_path):
        await self.write(settings_path, True)

    async def disable(self, settings_path, disabled_name, disabled_type):
        await self.write(settings_path, False)

    async def save(self, path_param, content_path):
        path = await self.get(path_param)
        content = await self.get(content_path)

        with open(path, "w") as file:
            json.dump(content, file, indent = 4)