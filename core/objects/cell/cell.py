import asyncio
from core.modules.core.scripting.variable.variable import *
from core.modules.core.scripting.json.json import *

class Cell:
    def __init__(self):
        self.size = 1

    def add(self):
        self.size += 1

    def get(self):
        return self.size

async def add(**kwargs):
    if "variables" in kwargs:
        variables = kwargs["variables"]

        if "unique_object_id" in kwargs:
            unique_object_id = kwargs["unique_object_id"]
            print(f"cell::add > unique object id : {unique_object_id}")

            if await variables.exists("objects"):
                temp_var = Variable()
                await temp_var.init({"a": "b"})
                await variables.write(f"objects/{unique_object_id}", temp_var)

            if await variables.exists("objects"):
                if await variables.exists(f"objects/{unique_object_id}"):
                    memory = await variables.get(f"objects/{unique_object_id}")
                    print(f"cell::add > memory : {memory.value}")
                else:
                    print("cell::add > I don't remember anything, [...]")

        if await variables.exists("moment/object"):
            _moment_var = await variables.get("moment/object")
            _moment_obj = _moment_var.value
            print(f"cell::add > current moment : {await _moment_obj.get("time/value1")}")

    return 1