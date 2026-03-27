from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Default_font:
    def __init__(self, uuid: int, gui):
        self.gui = gui
        self.default_font = Json()
        self.default_font.write(Path("settings/tags/font"), uuid, mode = 1)

    def register(self):
        tag = self.default_font.get(Path("settings/tags/font"))

        with dpg.font_registry():
            default_font = dpg.add_font("sources/core/plugins/gui/fonts/ClarityCity-Light/ClarityCity-Light.ttf", 18, tag = tag)