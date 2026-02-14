import asyncio
from core.modules.core.scripting.json.json import *

class Variable:
    def __init__(self):
        self.name = None
        self.value = None
        self.states = None

    async def init(self, states, name, value = None):
        self.name = name
        self.value = value

        self.states = states
        await self.states.create(name)
        await self.states.write(f"{name}/object", self)

    async def write(self, value):
        self.value = value

    async def get(self, path):
        return self.value