import asyncio
from core.modules.executable.executable import *
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

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
        await self.execution.create(Path("execution"))
        await self.execution.write(Path("execution"), config)

        self.variables = variables
        # temporaire, il faut un nom unique (le nom de l'objet)
        await self.variables.create(Path("unique_name"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("unique_name/object"), obj)

        self.config = config
        self.macros = []
        self.methods = []

        if await self.execution.exists(Path("execution/macros")):
            for macro in await self.execution.get(Path("execution/macros")):
                executable = Executable()
                await executable.init(macro, self.variables)
                self.macros.append(executable)

        if await self.execution.exists(Path("execution/methods")):
            for method in await self.execution.get(Path("execution/methods")):
                executable = Executable()
                await executable.init(method, self.variables, self.macros)
                self.methods.append(executable)