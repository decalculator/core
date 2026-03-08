import asyncio
from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *

class Scheduler:
    def __init__(self):
        self.variables = None
        self.scheduler = None
        self.loader = None
        self.console = None

    async def init(self, variables, console = None):
        self.variables = variables
        await self.variables.create(Path("scheduler"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("scheduler/object"), obj)

        loader_var = await self.variables.get(Path("loader/object"))
        self.loader = loader_var.value

        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("symbols > ready")
            await self.console.write(Path("core"), console_core)

        self.scheduler = Json()
        await self.scheduler.init()
        await self.scheduler.create(Path("settings"))

    async def create(self, name):
        await self.scheduler.create(name)
        await self.scheduler.write(Path(f"{name.json_path}/running"), {})
        await self.scheduler.write(Path(f"{name.json_path}/to_run"), {})

    async def settings(self, path, value):
        await self.scheduler.write(Path(f"settings/{path.json_path}"), value, 1)

    async def write(self, path, value):
        await self.scheduler.write(path, value)

    async def get(self, path):
        return await self.scheduler.get(path)

    async def exists(self, path):
        return await self.scheduler.exists(path)

    async def run(self, path):
        json_path = path.json_path

        splitted = json_path.split("/")
        name = splitted[0]

        classic_task = []
        mode = None

        if await self.scheduler.exists(Path(f"settings/{name}")):
            if await self.scheduler.exists(Path(f"settings/{name}/mode")):
                mode = await self.scheduler.get(Path(f"settings/{name}/mode"))

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
        await self.loader.write(Path(f"loader/{object_name}/{object_id}/enabled"), False)

    async def enable(self, object_name, object_id):
        print(f"scheduler::enable > {object_name}:{object_id}")
        await self.loader.write(Path(f"loader/{object_name}/{object_id}/enabled"), True)

    async def remove(self, path):
        await self.scheduler.remove(path)