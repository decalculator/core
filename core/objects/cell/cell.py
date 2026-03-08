import asyncio
import random

from core.modules.variable.variable import *
from core.modules.json.json import *
from core.modules.path.path import *
from core.plugins.representation.representation import *

async def add(**kwargs):
    if "variables" in kwargs:
        variables = kwargs["variables"]

        if "unique_object_id" in kwargs:
            unique_object_id = kwargs["unique_object_id"]
            print(f"cell::add > unique object id : {unique_object_id}")

            # if await variables.exists(Path("objects")):
            if await variables.exists(Path(f"objects/{unique_object_id}")):
                var_var = await variables.get(Path(f"objects/{unique_object_id}"))
                var = var_var.value
                var["position"][0] += 1
                var["position"][1] += 1
            else:
                temp_var = Variable()
                await temp_var.init({"position": [random.randint(0, 100), random.randint(0, 100)], "animation": {"frames": ["core/objects/cell/frames/0.png", "core/objects/cell/frames/1.png", "core/objects/cell/frames/2.png"], "last": None}})
                await variables.write(Path(f"objects/{unique_object_id}"), temp_var)

            if await variables.exists(Path("representation/object")) and await variables.exists(Path("moment/object")) and await variables.exists(Path("objects")) and await variables.exists(Path(f"objects/{unique_object_id}")):
                moment_var = await variables.get(Path("moment/object"))
                moment = moment_var.value
                now = await moment.get(Path("time/value1"))

                memory = await variables.get(Path(f"objects/{unique_object_id}"))
                mem_data = memory.value

                representation_var = await variables.get(Path("representation/object"))
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

                        await representation.write(Path(f"objects/{unique_object_id}"), {
                            "mode": "image",
                            "render": 2,
                            "path": frames[last_frame],
                            "position": [mem_data["position"][0], mem_data["position"][1]],
                            "refresh": True,
                            "done": False
                        })

    return 1