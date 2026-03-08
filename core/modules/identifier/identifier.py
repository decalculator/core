import asyncio
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Identifier:
    def __init__(self):
        self.identifier = None
        self.variables = None
        self.console = None

    async def init(self, variables, console = None):
        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("identifier > ready")
            await self.console.write(Path("core"), console_core)

        self.variables = variables
        await self.variables.create(Path("identifier"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("identifier/object"), obj)

        self.identifier = Json()
        await self.identifier.init()

    async def create(self, name):
        await self.identifier.create(name)
        await self.identifier.write(Path(f"{name.json_path}/last_id"), -1)

    async def write(self, path, value):
        await self.identifier.write(path, value)

    async def generate_id(self, path):
        # path = await self.identifier.fix_path(path)
        new_id = await self.get_free_id(path)
        await self.identifier.write(Path(f"{path.json_path}/{new_id}"), {})
        await self.identifier.write(Path(f"{path.json_path}/last_id"), new_id)

        return new_id

    async def get_free_id(self, path):
        # path = await self.identifier.fix_path(path)
        return await self.identifier.get(Path(f"{path.json_path}/last_id")) + 1

    async def get(self, path):
        return await self.identifier.get(path)

    async def exists(self, path):
        return await self.identifier.exists(path)