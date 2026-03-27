from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.gui.applications.tasks_manager.tasks_manager import tasks_callback
from core.plugins.gui.applications.spaces.spaces import create_space_callback
from core.plugins.gui.applications.installator.installator import installator_callback
from core.plugins.gui.applications.updater.updater import updater_callback
from core.plugins.gui.applications.console.console import console_callback

from core.plugins.gui.components.change_language.change_language import change_language_callback

class ViewportMenuBar:
    def __init__(self, loop, pid_manager: PidManager, device: Device, scheduler: Scheduler, parent: Gui, languages: Languages, configuration: DynamicValue, filesystem: Filesystem, settings: Settings, repos: Repos):
        self.languages = languages
        self.loop = loop
        self.configuration = configuration
        self.filesystem = filesystem
        self.scheduler = scheduler
        self.device = device
        self.pid_manager = pid_manager
        self.gui = parent
        self.settings = settings
        self.repos = repos

        uuid = dpg.generate_uuid()
        self.data = Json()
        self.data.write(Path("settings/tags"), {"window": uuid}, mode = 1)

    async def menu_bar(self):
        if "applications" in self.configuration.data:
            applications = self.configuration.data["applications"]

            if applications:
                with dpg.viewport_menu_bar():
                    this = "viewport_menu_bar"

                    for application, value in applications.items():
                        if "path" in value:
                            content = await self.filesystem.read(Path(value["path"], mode = 1), mode = 2)

                            if "payloads" in content:
                                if this in content["payloads"]:
                                    payload = content["payloads"][this]

                                    if "path" in payload:
                                        payload_content = await self.filesystem.read(Path(payload["path"], mode = 1), mode = 0)
                                        exec(payload_content)

                        """
                        with dpg.menu(label = await self.languages.get_from_selected(Path("gui/tasks"))):
                            with dpg.menu(label = await self.languages.get_from_selected(Path("gui/tasks_manager"))):
                                dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui_open")), callback = tasks_callback, user_data = [self.loop, 0])
                        """

                    """
                    tag = dpg.generate_uuid()
                    await self.data.write(Path("settings/tags/spaces_menu"), tag)

                    with dpg.menu(label = await self.languages.get_from_selected(Path("gui/spaces")), tag = tag):
                        dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui/create")), callback = create_space_callback, user_data = [self.loop])

                    with dpg.menu(label = await self.languages.get_from_selected(Path("gui/console"))):
                        dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui/open")), callback = console_callback, user_data = [self.loop, 0])

                    with dpg.menu(label = await self.languages.get_from_selected(Path("gui/settings"))):
                        with dpg.menu(label = await self.languages.get_from_selected(Path("gui/language"))):
                            selected = await self.languages.get_selected()

                            for language in await self.languages.get(Path("")):
                                tag = dpg.generate_uuid()
                                value = language == selected.path
                                await self.data.write(Path(f"settings/tags/{language}_box"), tag)

                                dpg.add_checkbox(label = language, tag = tag, default_value = value, callback = change_language_callback, user_data = [self.loop, language])

                    with dpg.menu(label = await self.languages.get_from_selected(Path("gui/installator"))):
                        dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui/open")), callback = installator_callback, user_data = [self.loop])

                    dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui/updater")), callback = updater_callback, user_data = [self.loop])
                    dpg.add_menu_item(label = await self.languages.get_from_selected(Path("gui/exit")), callback = self.gui.exit_callback)
                    """