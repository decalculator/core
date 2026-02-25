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
                if not await variables.exists(f"objects/{unique_object_id}"):
                    temp_var = Variable()
                    await temp_var.init({"animation": {"frames": ["core/objects/cell/frames/0.png", "core/objects/cell/frames/1.png", "core/objects/cell/frames/2.png"], "last": None}})
                    await variables.write(f"objects/{unique_object_id}", temp_var)

            if await variables.exists("representation/object") and await variables.exists("moment/object") and await variables.exists("objects") and await variables.exists(f"objects/{unique_object_id}"):
                moment_var = await variables.get("moment/object")
                moment = moment_var.value
                now = await moment.get("time/value1")

                memory = await variables.get(f"objects/{unique_object_id}")
                mem_data = memory.value

                representation_var = await variables.get("representation/object")
                representation = representation_var.value

                if "animation" in mem_data:
                    animation = mem_data["animation"]
                    if "frames" in animation and "last" in animation:
                        frames = animation["frames"]
                        last_frame = animation["last"]

                        if last_frame == None:
                            last_frame = 0
                        else:
                            if last_frame == len(frames) - 1:
                                last_frame = 0
                            else:
                                last_frame += 1

                        mem_data["animation"]["last"] = last_frame

                        await representation.write(f"objects/{unique_object_id}", {
                            "mode": "image",
                            "path": frames[last_frame],
                            "position": [100, 100]
                        })

    return 1