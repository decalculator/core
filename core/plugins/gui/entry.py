import asyncio
from core.plugins.gui.gui import *

async def entry(**kwargs):
    # print("gui::entry > exec !")

    variables = None
    unique_object_id = None

    if "variables" in kwargs:
        variables = kwargs["variables"]

    if "unique_object_id" in kwargs:
        unique_object_id = kwargs["unique_object_id"]

    gui = Gui()
    await gui.init(variables, unique_object_id)