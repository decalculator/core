import asyncio
from core.modules.core.scripting.executable.executable import *
from core.modules.core.scripting.json.json import *

class Execution:
    def __init__(self):
        self.states = None
        self.execution = None
        self.config = None
        self.macros = None
        self.methods = None

    async def init(self, config, states):
        self.states = states

        self.execution = Json()
        await self.execution.init()
        await self.execution.create("execution")
        await self.execution.write("execution", config)

        # temporaire, il faut un nom unique (le nom de l'objet)
        await self.states.create("unique_name")
        await self.states.write("unique_name/object", self)

        self.config = config
        self.macros = []
        self.methods = []

        if await self.execution.exists("execution/macros"):
            for macro in await self.execution.get("execution/macros"):
                executable = Executable()
                await executable.init(macro, states)
                self.macros.append(executable)

        if await self.execution.exists("execution/methods"):
            for method in await self.execution.get("execution/methods"):
                executable = Executable()
                await executable.init(method, states, self.macros)
                self.methods.append(executable)