from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Viewport:
    def __init__(self, device: Device):
        self.device = device
        uuid = dpg.generate_uuid()
        self.viewport = Json()
        self.viewport.write(Path("settings/tags"), {"view": uuid}, mode = 1)

    def register(self):
        resolution = self.device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        dpg.create_viewport(title = "core", width = width, height = height)
        dpg.set_viewport_clear_color((255, 255, 255, 255))

        # la ligne suivante fait crash une exécution parallèle de l'objet,
        # j'ai tout d'abord songé à analyser le comportement de dearpygui,
        # car je pensais qu'il s'agissait d'un scénario du style : dearpygui de gui1 écrit à un endroit,
        # mais dearpygui de gui2 écrit à ce même endroit, ou quelque chose de similaire
        # en réalité, il semble que simplement commenter cette ligne débloque l'exécution, sous macOS en tout cas
        # le principe de non-unicité de l'objet est ici respecté

        # edit : impossible de l'enlever, sinon les callbacks ne fonctionnent pas...

        dpg.setup_dearpygui()

        dpg.show_viewport()