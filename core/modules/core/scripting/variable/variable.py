import asyncio
from core.modules.core.scripting.json.json import *

class Variable:
    def __init__(self):
        self.value = None
        self.states = None

    async def init(self, value = None):
        self.value = value

    async def write(self, value):
        self.value = value

    async def get(self, path):
        return self.value