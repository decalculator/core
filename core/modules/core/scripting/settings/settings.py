import asyncio
from core.modules.core.scripting.json.json import *

class Settings:
    def __init__(self):
        self.states = None
        self.loader = None
        self.settings = None

    async def init(self, states, loader):
        self.states = states

        await self.states.create("settings")
        await self.states.write("settings/object", self)

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
        #await self.loader.load(enabled_name, enabled_type)

    async def disable(self, settings_path, disabled_name, disabled_type):
        await self.write(settings_path, False)
        # self.loader.unload(enabled_name, disabled_type)

    async def save(self, path_param, content_path):
        path = await self.get(path_param)
        content = await self.get(content_path)

        with open(path, "w") as file:
            json.dump(content, file, indent = 4)