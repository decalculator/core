from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Settings:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)

def settings_callback(sender, app_data, user_data):
    user_data[0].create_task(settings_function(user_data))

def settings_function(args):
    uuid = dpg.generate_uuid()
    settings = Settings(uuid = uuid)
    settings.run(args = args)