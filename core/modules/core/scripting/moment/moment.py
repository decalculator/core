import asyncio
from core.modules.core.scripting.json.json import *

class Moment:
    def __init__(self):
        self.moment = None
        self.states = None

    async def init(self, states):
        self.moment = Json()
        await self.moment.init()
        self.states = states
        await self.states.create("moment")
        await self.states.write("moment/object", self)

    async def create(self, name):
        await self.moment.create(name)

    async def write(self, path, value):
        await self.moment.write(path, value)

    async def next_moment(self, path):
        await self.moment.write(path, await self.moment.get(path) + 1)

    async def previous_moment(self, path):
        await self.moment.write(path, await self.moment.get(path) - 1)

    async def get(self, path):
        return await self.moment.get(path)