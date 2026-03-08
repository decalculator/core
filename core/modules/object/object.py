import asyncio
from core.modules.execution.execution import *
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Object:
    def __init__(self):
        self.variables = None
        self.object = None
        self.config = None
        self.name = None
        self.version = None
        self.type = None
        self.module = None
        self.plugin = None
        self.requires_modules = None
        self.requires_plugins = None
        self.requires_application = None
        self.execution = None
        self.object_type = None
        self.object_model = None

    async def init(self, config, variables, unique_object_id):
        self.variables = variables

        self.object = Json()
        await self.object.init()
        await self.object.create(Path("settings"))
        await self.object.write(Path("settings"), config)

        name = await self.object.get(Path("settings/name"))

        self.variables = variables
        await self.variables.create(Path(name))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path(f"{name}/object"), obj)

        self.config = config

        self.name = name
        self.version = await self.object.get(Path("settings/version"))
        self.type = await self.object.get(Path("settings/type"))

        if await self.object.exists(Path("settings/module")):
            self.module = await self.object.get(Path("settings/module"))

        if await self.object.exists(Path("settings/plugin")):
            self.plugin = await self.object.get(Path("settings/plugin"))

        if await self.object.exists(Path("settings/requires/modules")):
            self.requires_modules = await self.object.get(Path("settings/requires/modules"))

        if await self.object.exists(Path("settings/requires/plugins")):
            self.requires_plugins = self.object.get(Path("settings/requires/plugins"))

        if await self.object.exists(Path("settings/requires/application")):
            self.requires_application = await self.object.get(Path("settings/requires/application"))

        execution = Execution()
        await execution.init(await self.object.get(Path("settings/execution")), self.variables)
        self.execution = [execution]

        self.object_type = await self.object.get(Path("settings/object_type"))

        if await self.object.exists(Path("settings/object_type/object_model")):
            self.object_model = await self.object.get(Path("settings/object_type/object_model"))