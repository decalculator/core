from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

class Command:
    def __init__(self, command: str):
        splitted = command.split(" ")

        self.command = command
        self.splitted = splitted
        self.executable_name = splitted[0]
        self.args = splitted[1:]