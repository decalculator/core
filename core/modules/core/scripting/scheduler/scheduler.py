import asyncio
from core.modules.core.scripting.json.json import *

class Scheduler:
    def __init__(self):
        self.states = None
        self.scheduler = None

    async def init(self, states):
        self.states = states
        await self.states.create("scheduler")
        await self.states.write("scheduler/object", self)
        self.scheduler = Json()
        await self.scheduler.init()
        await self.scheduler.create("settings")

    async def create(self, name):
        await self.scheduler.create(name)
        await self.scheduler.write(f"{name}/running", [])
        await self.scheduler.write(f"{name}/to_run", {})

    async def settings(self, path, value):
        await self.scheduler.write(f"settings/{path}", value, 1)

    async def write(self, path, value):
        await self.scheduler.write(path, value)

    async def get(self, path):
        return await self.scheduler.get(path)

    async def exists(self, path):
        return await self.scheduler.exists(path)

    async def run(self, path):
        splitted = path.split("/")
        name = splitted[0]

        classic_task = []
        mode = None

        if await self.scheduler.exists(f"settings/{name}"):
            if await self.scheduler.exists(f"settings/{name}/mode"):
                mode = await self.scheduler.get(f"settings/{name}/mode")

        task = await self.scheduler.get(path)
        async_task = []

        if mode == "classic":
            for objects_name, objects_value in task.items():
                async_task.append(asyncio.create_task(self.execute_objects(objects_value, mode)))

            await asyncio.gather(*async_task)

        elif mode == "complex":
            for objects_name, objects_value in task.items():
                await self.execute_objects(objects_value, mode)

    async def execute_objects(self, value, mode):
        for obj in value:
            for execution in obj.execution:
                for method in execution.methods:
                    await method.execute(logs = True, mode = mode)