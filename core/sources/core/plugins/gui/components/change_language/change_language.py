from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class ChangeLanguage:
    pass

# callbacks

def change_language_callback(sender, app_data, user_data):
    user_data[0].create_task(change_language_function(user_data, app_data))

async def change_language_function(args, value):
    uuid = dpg.generate_uuid()
    change_language = ChangeLanguage(uuid = uuid)
    await change_language.change_language_function(args, value)