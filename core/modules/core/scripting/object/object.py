import asyncio
from core.modules.core.scripting.execution.execution import *
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

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

    async def init(self, config, variables):
        self.variables = variables

        self.object = Json()
        await self.object.init()
        await self.object.create("settings")
        await self.object.write("settings", config)

        name = await self.object.get("settings/name")

        self.variables = variables
        await self.variables.create(name)
        obj = Variable()
        await obj.init(self)
        await self.variables.write(f"{name}/object", obj)

        self.config = config

        self.name = name
        self.version = await self.object.get("settings/version")
        self.type = await self.object.get("settings/type")

        if await self.object.exists("settings/module"):
            self.module = await self.object.get("settings/module")

        if await self.object.exists("settings/plugin"):
            self.plugin = await self.object.get("settings/plugin")

        if await self.object.exists("settings/requires/modules"):
            self.requires_modules = await self.object.get("settings/requires/modules")

        if await self.object.exists("settings/requires/plugins"):
            self.requires_plugins = self.object.get("settings/requires/plugins")

        if await self.object.exists("settings/requires/application"):
            self.requires_application = await self.object.get("settings/requires/application")

        execution = Execution()
        await execution.init(await self.object.get("settings/execution"), self.variables)
        self.execution = [execution]

        self.object_type = await self.object.get("settings/object_type")

        if await self.object.exists("settings/object_type/object_model"):
            self.object_model = await self.object.get("settings/object_type/object_model")