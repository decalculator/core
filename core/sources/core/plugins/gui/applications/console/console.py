from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.gui.applications.console.command.command import *

class Console:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)
        self.loop = None
        self.commands_dict = None

        self.gui = None
        self.parent = None

    async def run(self, args: list):
        loop = args[0]
        mode = args[1]
        device = args[2]
        languages = args[3]
        filesystem = args[4]
        gui = args[5]
        parent = args[6]

        commands_dict = {}

        self.gui = gui
        self.parent = parent

        commands = await filesystem.read(Path("sources/core/plugins/gui/applications/console/commands/commands.json", mode = 1), mode = 2)
        for command, value in commands.items():
            path = None
            method = None

            commands_dict[command] = {}

            if "path" in value:
                path = value["path"]
                content = await filesystem.read(Path(path, mode = 1), mode = 0)

                commands_dict[command]["content"] = content

                if "method" in value:
                    method = value["method"]
                    commands_dict[command]["method"] = method

        self.commands_dict = commands_dict
        self.loop = loop

        resolution = device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        window_tag = self.data.get(Path("settings/tags/window"))

        with dpg.window(label = languages.get_from_selected(Path("gui/console")), width = width // 2, height = height // 2, tag = window_tag):
            dpg.set_item_pos(window_tag, [width // 2 - ((width // 2) // 2), height // 2 - ((height // 2) // 2)])
            # dpg.bind_item_font(dpg.last_item(), self.gui.data["terminal_font"])
            # dpg.bind_item_theme(dpg.last_item(), self.gui.data["terminal_theme"])

            # ...

            tag = dpg.generate_uuid()
            self.data.write(Path("settings/tags/horizontal_group/1/horizontal_group"), tag, mode = 1)
            self.data.write(Path("settings/tags/horizontal_group_count"), 1, mode = 1)

            with dpg.group(horizontal = True, tag = tag):
                tag = dpg.generate_uuid()
                self.data.write(Path("settings/tags/horizontal_group/1/cmd_line"), tag)
                dpg.add_text("root@core $ ", tag = tag)

                tag = dpg.generate_uuid()
                self.data.write(Path("settings/tags/horizontal_group/1/command_input"), tag)
                dpg.add_input_text(tag = tag, on_enter = True, callback = self.console_command_execution_callback)

            dpg.focus_item(tag)

    def console_command_execution_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.console_command_execution_function())

    async def console_command_execution_function(self):
        window_tag = self.data.get(Path("settings/tags/window"))
        horizontal_group_count = self.data.get(Path("settings/tags/horizontal_group_count"))
        horizontal_group = self.data.get(Path(f"settings/tags/horizontal_group/{horizontal_group_count}/horizontal_group"))

        tag = self.data.get(Path(f"settings/tags/horizontal_group/{horizontal_group_count}/command_input"))
        cmd = dpg.get_value(tag)
        dpg.delete_item(tag)

        command = Command(command = cmd)

        if command.executable_name in self.commands_dict:
            content = self.commands_dict[command.executable_name]["content"]
            method = self.commands_dict[command.executable_name]["method"]

            exec_vars = {}
            exec(content, exec_vars)

            method = exec_vars[method]
            task = method(command = command, window_tag = window_tag, parent = self.parent, gui = self.gui)

            if task:
                await task

        dpg.add_text(cmd, parent = horizontal_group)

        tag = dpg.generate_uuid()
        this = horizontal_group_count + 1

        self.data.write(Path("settings/tags/horizontal_group_count"), this)
        self.data.write(Path(f"settings/tags/horizontal_group/{this}/horizontal_group"), tag, mode = 1)

        with dpg.group(horizontal = True, parent = window_tag, tag = tag):
            tag = dpg.generate_uuid()
            self.data.write(Path(f"settings/tags/horizontal_group/{this}/cmd_line"), tag)

            dpg.add_text("root@core $ ", tag = tag)

            tag = dpg.generate_uuid()
            self.data.write(Path(f"settings/tags/horizontal_group/{this}/command_input"), tag)
            dpg.add_input_text(tag = tag, on_enter = True, callback = self.console_command_execution_callback)

            dpg.focus_item(tag)

# callbacks

def console_callback(sender, app_data, user_data):
    user_data[0].create_task(console_function(user_data))

async def console_function(args):
    uuid = dpg.generate_uuid()
    console = Console(uuid = uuid)
    await console.run(args = args)