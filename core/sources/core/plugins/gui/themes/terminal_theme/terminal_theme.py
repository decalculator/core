import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Terminal_theme:
    def __init__(self, uuid, gui)):
        self.gui = gui
        self.terminal_theme = Json()
        self.terminal_theme.write(Path("settings/tags"), {"theme": uuid}, mode = 1)

    def register(self):
        tag = self.terminal_theme.get(Path("settings/tags/theme"))

        with dpg.theme(tag = tag) as terminal_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 255))

                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (0, 0, 0, 255))

                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (0, 0, 0, 0))

                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))