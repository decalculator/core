from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Terminal_font:
    def __init__(self, uuid: int, gui):
        self.gui = gui
        self.terminal_font = Json()
        self.terminal_font.write(Path("settings/tags"), {"font": uuid}, mode = 1)

    def register(self):
        tag = self.terminal_font.get(Path("settings/tags/font"))

        with dpg.font_registry():
            terminal_font = dpg.add_font("sources/core/plugins/gui/fonts/ClarityCity-Light/ClarityCity-Light.ttf", 15, tag = tag)