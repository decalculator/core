import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Scheduler:
    def __init__(self):
        self.variables = None
        self.scheduler = None
        self.loader = None

    async def init(self, variables):
        self.variables = variables
        await self.variables.create("scheduler")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("scheduler/object", obj)

        loader_var = await self.variables.get("loader/object")
        self.loader = loader_var.value

        self.scheduler = Json()
        await self.scheduler.init()
        await self.scheduler.create("settings")

    async def create(self, name):
        await self.scheduler.create(name)
        await self.scheduler.write(f"{name}/running", {})
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
                if not objects_name in ["running", "to_run"]:
                    for unique_object_id, value in objects_value.items():
                        if "objects" in value:
                            async_task.append(asyncio.create_task(self.execute_objects(objects_value[unique_object_id]["objects"], mode, unique_object_id)))

            await asyncio.gather(*async_task)

        elif mode == "complex":
            for objects_name, objects_value in task.items():
                if not objects_name in ["running", "to_run"]:
                    for unique_object_id in objects_value:
                        await self.execute_objects(objects_value[unique_object_id], mode, unique_object_id)

    async def execute_objects(self, value, mode, unique_object_id):
        for obj in value:
            for execution in obj.execution:
                for method in execution.methods:
                    await method.execute(logs = True, mode = mode, unique_object_id = unique_object_id)

    async def disable(self, object_name, object_id):
        print(f"scheduler::disable > {object_name}:{object_id}")
        await self.loader.write(f"loader/{object_name}/{object_id}/enabled", False)

    async def enable(self, object_name, object_id):
        print(f"scheduler::enable > {object_name}:{object_id}")
        await self.loader.write(f"loader/{object_name}/{object_id}/enabled", True)