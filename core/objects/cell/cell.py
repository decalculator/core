import asyncio
import random

from core.modules.core.scripting.variable.variable import *
from core.modules.core.scripting.json.json import *
from core.plugins.representation.representation import *

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
                if await variables.exists(f"objects/{unique_object_id}"):
                    var_var = await variables.get(f"objects/{unique_object_id}")
                    var = var_var.value
                    var["position"][0] += 1
                    var["position"][1] += 1
                else:
                    temp_var = Variable()
                    await temp_var.init({"position": [random.randint(0, 100), random.randint(0, 100)]})
                    await variables.write(f"objects/{unique_object_id}", temp_var)

            if await variables.exists("representation/object") and await variables.exists("moment/object") and await variables.exists("objects") and await variables.exists(f"objects/{unique_object_id}"):
                moment_var = await variables.get("moment/object")
                moment = moment_var.value
                now = await moment.get("time/value1")

                memory = await variables.get(f"objects/{unique_object_id}")
                mem_data = memory.value

                representation_var = await variables.get("representation/object")
                representation = representation_var.value

                await representation.write(f"objects/{unique_object_id}", {
                    "dimensions": [
                        now * now,
                        now * now
                    ],
                    "color": [
                        0, 0, 0, 0
                    ],
                    "position": [
                        mem_data["position"][0], mem_data["position"][1]
                    ]
                })

    return 1