import json
import asyncio
from core.modules.object.object import *
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Loader:
    def __init__(self):
        self.loader = None
        self.variables = None
        self.module_path = None
        self.plugin_path = None
        self.object_path = None
        self.console = None

    async def init(self, variables, module_path, plugin_path, object_path, console = None):
        self.loader = Json()
        await self.loader.init()
        self.module_path = module_path
        self.plugin_path = plugin_path
        self.object_path = object_path

        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("loader > ready")
            await self.console.write(Path("core"), console_core)

        await self.create(Path("loader"))

        self.variables = variables
        await self.variables.create(Path("loader"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("loader/object"), obj)

    async def create(self, name):
        await self.loader.create(name)

    async def get(self, path):
        return await self.loader.get(path)

    async def load(self, name, load_type, unique_object_id):
        path = None

        if load_type == "plugin":
            path = self.plugin_path
        elif load_type == "module":
            path = self.module_path
        elif load_type == "object":
            path = self.object_path

        main_config = Path(f"{path}/{name}/{name}.json", mode = 1)

        if not await self.loader.exists(Path(f"loader/{name}")):
            await self.loader.write(Path(f"loader/{name}"), {})

        if not await self.loader.exists(Path(f"loader/{name}/{unique_object_id}")):
            await self.loader.write(Path(f"loader/{name}/{unique_object_id}"), {})

        if not await self.loader.exists(Path(f"loader/{name}/{unique_object_id}/config")):
            await self.loader.write(Path(f"loader/{name}/{unique_object_id}/config"), await self.loader.get_from_file(main_config))

        current_object = Object()
        await current_object.init(await self.loader.get(Path(f"loader/{name}/{unique_object_id}/config")), self.variables, unique_object_id)

        if await self.loader.exists(Path(f"loader/{name}/{unique_object_id}/objects")):
            await self.loader.write(Path(f"loader/{name}/{unique_object_id}/objects"), await self.loader.get(Path(f"loader/{name}/{unique_object_id}/objects")).append(current_object))
        else:
            await self.loader.write(Path(f"loader/{name}/{unique_object_id}/objects"), [current_object])

    async def write(self, path, value):
        await self.loader.write(path, value)

    async def get(self, path):
        return await self.loader.get(path)

    async def unload(self, name, unload_type):
        pass