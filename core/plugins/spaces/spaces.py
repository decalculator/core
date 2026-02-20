import asyncio
from core.modules.core.scripting.json.json import *

class Spaces:
    def __init__(self):
        self.spaces = None
        self.variables = None
        self.default_path = None

    async def init(self, variables):
        self.variables = variables
        self.spaces = Json()
        await self.spaces.init()

        self.default_path = "core/data/plugins/spaces/spaces"

    async def create(self, name):
        await self.spaces.create(name)

    async def write(self, path, value):
        await self.spaces.write(path, value)

    async def get(self, path):
        return await self.spaces.get(path)