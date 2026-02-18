import asyncio
from core.modules.core.scripting.json.json import *

class Variable:
    def __init__(self):
        self.value = None
        self.states = None
        self.console = None

    async def init(self, value = None, console = None):
        self.console = console
        if self.console != None:
            console_core = await self.console.get("core")
            console_core.append("variable > ready")
            await self.console.write("core", console_core)

        self.value = value

    async def write(self, value):
        self.value = value

    async def get(self, path):
        return self.value