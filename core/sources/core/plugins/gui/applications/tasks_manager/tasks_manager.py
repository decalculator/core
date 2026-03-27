from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class TasksManager:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)

    def run(self, args):
        loop = args[0]
        mode = args[1]
        scheduler = args[2]
        device = args[3]
        languages = args[4]
        pid_manager = args[5]

        resolution = device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        window_tag = self.data.get(Path("settings/tags/window"))
        data = pid_manager.get(Path("uuid/used"))

        with dpg.window(label = languages.get_from_selected(Path("gui/tasks_manager")), width = width // 2, height = height // 2, tag = window_tag):
            for pid, value in data.items():
                dpg.add_text(f"pid : {pid}")

                for param, val in value.items():
                    dpg.add_text(f"    {param} : {val}")

                dpg.add_button(label = languages.get_from_selected(Path("gui/remove")))

                # ...

    def on_close_function(self, sender):
        dpg.delete_item(sender)

    def on_close_callback(self, sender):
        self.on_close_function(sender)

# callbacks

def tasks_callback(sender, app_data, user_data):
    tasks_function(user_data)

def tasks_function(args: list):
    uuid = dpg.generate_uuid()
    tasks_manager = TasksManager(uuid = uuid)
    tasks_manager.run(args = args)