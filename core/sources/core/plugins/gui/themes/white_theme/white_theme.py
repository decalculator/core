import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class WhiteTheme:
    def __init__(self, uuid, gui):
        self.gui = gui
        self.white_theme = Json()
        self.white_theme.write(Path("settings/tags/theme"), uuid, mode = 1)

    def register(self):
        tag = self.white_theme.get(Path("settings/tags/theme"))
        
        with dpg.theme(tag = tag) as white_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (245, 245, 245, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (240, 240, 240, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))

                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (250, 250, 250, 255))

                # inputs
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (237, 237, 237, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (230, 230, 230, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (224, 224, 224, 255))

                # title
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (237, 237, 237, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (224, 224, 224, 255))

                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (237, 237, 237, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (230, 230, 230, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (224, 224, 224, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (220, 220, 220, 255))

                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255, 255))

                dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (250, 250, 250, 255))