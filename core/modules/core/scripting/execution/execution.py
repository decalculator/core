import asyncio
from core.modules.core.scripting.executable.executable import *
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Execution:
    def __init__(self):
        self.variables = None
        self.execution = None
        self.config = None
        self.macros = None
        self.methods = None

    async def init(self, config, variables):
        self.execution = Json()
        await self.execution.init()
        await self.execution.create("execution")
        await self.execution.write("execution", config)

        self.variables = variables
        # temporaire, il faut un nom unique (le nom de l'objet)
        await self.variables.create("unique_name")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("unique_name/object", obj)

        self.config = config
        self.macros = []
        self.methods = []

        if await self.execution.exists("execution/macros"):
            for macro in await self.execution.get("execution/macros"):
                executable = Executable()
                await executable.init(macro, self.variables)
                self.macros.append(executable)

        if await self.execution.exists("execution/methods"):
            for method in await self.execution.get("execution/methods"):
                executable = Executable()
                await executable.init(method, self.variables, self.macros)
                self.methods.append(executable)