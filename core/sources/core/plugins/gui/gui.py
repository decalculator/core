from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.gui.components.viewport.viewport import *
from core.plugins.gui.components.viewport_menu_bar.viewport_menu_bar import *

from core.plugins.communication.communication import *
from core.plugins.installator.installator import *
from core.plugins.temp.temp import *
from core.plugins.updater.updater import *

class Gui:
    def __init__(self, configuration: DynamicValue | None = None, device: Device | None = None, memory: Memory | None = None, filesystem: Filesystem | None = None, settings: Settings | None = None, languages: Languages | None = None, loader: Loader | None = None, scheduler: Scheduler | None = None, pid_manager: PidManager | None = None, logs: Logs | None = None, pid: Pid | None = None, content: Json | None = None, ppid: DynamicValue | None = None, repos: Repos | None = None) -> None:
        self.usoi = 18
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content)
                initialized = True

        if not initialized:
            self.data = Json()
            initialized = True

        self.data.write(Path("settings/objects"), {}, mode = 1)

        if languages is not None:
            self.data.write(Path("settings/objects/languages"), languages)

        if filesystem is not None:
            self.data.write(Path("settings/objects/filesystem"), filesystem)

        if scheduler is not None:
            self.data.write(Path("settings/objects/scheduler"), scheduler)

        if device is not None:
            self.data.write(Path("settings/objects/device"), device)

        if pid_manager is not None:
            self.data.write(Path("settings/objects/pid_manager"), pid_manager)

        if settings is not None:
            self.data.write(Path("settings/objects/settings"), settings)

        if repos is not None:
            self.data.write(Path("settings/objects/repos"), repos)

        temp = Temp(filesystem = filesystem)
        temp.write(Path("id"), {"used": [], "unused": [], "max": 1})
        temp.set_get_id(unused_path = Path("id/unused"), used_path = Path("id/used"), maximum_path = Path("id/max"))

        communication = Communication(filesystem = filesystem)

        installator = Installator(temp = temp, communication = communication, filesystem = filesystem)
        self.data.write(Path("settings/objects/installator"), installator)

        updater = Updater(filesystem = filesystem, settings = settings)
        self.data.write(Path("settings/objects/updater"), updater)

        self.configuration = configuration
        self.ppid = ppid
        loop = asyncio.get_running_loop()
        self.loop = loop

        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        self.memory = memory
        self.logs = logs
        self.pid = pid

        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

    async def run(self, shared_memory: dict | None = None):
        print("gui::run > exec !")

        languages = self.data.get(Path("settings/objects/languages"))
        filesystem = self.data.get(Path("settings/objects/filesystem"))
        scheduler = self.data.get(Path("settings/objects/scheduler"))
        device = self.data.get(Path("settings/objects/device"))
        pid_manager = self.data.get(Path("settings/objects/pid_manager"))
        settings = self.data.get(Path("settings/objects/settings"))
        repos = self.data.get(Path("settings/objects/repos"))

        dpg.create_context()

        this = "font_init"
        if "fonts" in self.configuration.data:
            for font, value in self.configuration.data["fonts"].items():
                if "path" in value:
                    content = await filesystem.read(Path(value["path"], mode = 1), mode = 2)

                    if "enabled" in content:
                        if content["enabled"] == True:
                            if "payloads" in content:

                                if this in content["payloads"]:
                                    if "path" in content["payloads"][this]:
                                        content = await filesystem.read(Path(content["payloads"][this]["path"], mode = 1), mode = 0)
                                        exec(content, globals())
                                        await bridge(self)

                                        # soit comme ça, et on est bien en async mais on a plus de contrôle sur self
                                        # ou bien alors on pense autrement : on abandonne l'async pour le payload, et on fait un loop.create_task dans le __init__ de default_font

                                        # ou bien un mix des deux : on reste comme cela en async mais on passe self en **kwargs ?
                                        # OUI ! c'est une solution possible
                                        # par contre, il faut bien avoir les arguments nécessaires dans self
                                        # on pourra toujours créer un self.arguments, au pire (mais moins élégant ?)

        this = "theme_init"
        if "themes" in self.configuration.data:
            for theme, value in self.configuration.data["themes"].items():
                if "path" in value:
                    content = await filesystem.read(Path(value["path"], mode = 1), mode = 2)

                    if "enabled" in content:
                        if content["enabled"] == True:
                            if "payloads" in content:

                                if this in content["payloads"]:
                                    if "path" in content["payloads"][this]:
                                        content = await filesystem.read(Path(content["payloads"][this]["path"], mode = 1), mode = 0)
                                        exec(content, globals())
                                        await bridge(self)

        viewport_menu_bar = ViewportMenuBar(self.loop, pid_manager = pid_manager, device = device, scheduler = scheduler, parent = self, languages = languages, configuration = self.configuration, filesystem = filesystem, settings = settings, repos = repos)
        await viewport_menu_bar.menu_bar()

        viewport = Viewport(device = device)
        viewport.register()

        done = False
        while dpg.is_dearpygui_running() and not done:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

        dpg.stop_dearpygui()
        dpg.destroy_context()

    def write(self, path: Path, value, mode: int = 0) -> bool:
        return self.data.write(path, value, mode = mode)

    def remove(self, path: Path) -> bool:
        return self.data.remove(path)

    def get(self, path: Path):
        return self.data.get(path)

    def exists(self, path: Path):
        return self.data.exists(path)

    def exit_callback(self):
        self.loop.create_task(self.exit_function())

    async def exit_function(self):
        pass