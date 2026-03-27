from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.updater.updater import Updater as updater_obj

class Updater:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)

        self.loop = None
        self.settings = None
        self.updater = None
        self.parent = None
        self.gui = None

    def run(self, args: list):
        loop = args[0]
        scheduler = args[1]
        device = args[2]
        languages = args[3]
        pid_manager = args[4]
        settings = args[5]
        filesystem = args[6]
        parent = args[7]
        gui = args[8]

        self.parent = parent
        self.gui = gui
        self.loop = loop

        resolution = device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        version = settings.get(Path("version"))

        self.updater = updater_obj(filesystem = filesystem, settings = settings)

        latest_version_number = self.updater.get_latest_version_number()

        window_tag = self.data.get(Path("settings/tags/window"))

        with dpg.window(label = languages.get_from_selected(Path("gui/updater")), tag = window_tag, on_close = self.on_close_callback, width = width // 5, height = width // 5):
            dpg.add_text(f"version : {version}")
            dpg.add_text(f"latest version : {latest_version_number}")

        if float(version) < float(latest_version_number):
            if dpg.does_item_exist(window_tag):
                dpg.add_button(label = languages.get_from_selected(Path("gui/update")), parent = window_tag, callback = self.update_callback)

    def update_function(self):
        self.updater.update()

    def update_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.update_function())

    def on_close_function(self, sender):
        dpg.delete_item(sender)

    def on_close_callback(self, sender):
        self.on_close_function(sender)

# callbacks

def updater_callback(sender, app_data, user_data):
    updater_function(user_data)

def updater_function(args):
    uuid = dpg.generate_uuid()
    updater_app = Updater(uuid = uuid)
    updater_app.run(args = args)