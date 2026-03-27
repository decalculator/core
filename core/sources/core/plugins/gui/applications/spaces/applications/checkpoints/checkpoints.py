from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.gui.applications.console.command.command import *

class Checkpoints:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)

        self.loop = None
        self.commands_dict = None

        self.gui = None
        self.parent = None

    async def run(self, args: list):
        pass

def checkpoints_callback(sender, app_data, user_data):
    checkpoints_function(user_data)

def checkpoints_function(args):
    uuid = dpg.generate_uuid()
    checkpoints = Checkpoints(uuid = uuid)
    checkpoints.run(args = args)