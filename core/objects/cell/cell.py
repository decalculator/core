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

        if await variables.exists("moment/object"):
            _moment_var = await variables.get("moment/object")
            _moment_obj = _moment_var.value
            print(await _moment_obj.get("time/value1"))

    return 1