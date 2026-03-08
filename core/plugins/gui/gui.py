import asyncio
import ast
import re
import dearpygui.dearpygui as dpg
from PIL import Image

from core.modules.loader.loader import *
# from core.modules.states.states import *
from core.modules.symbols.symbols import *
from core.modules.json.json import *
from core.modules.settings.settings import *
from core.modules.moment.moment import *
from core.modules.scheduler.scheduler import *
from core.modules.identifier.identifier import *
from core.modules.variable.variable import *
from core.modules.variables.variables import *
from core.modules.memory.memory import *
from core.modules.console.console import *
from core.modules.path.path import *
from core.modules.path_utils.path_utils import *
from core.modules.device.device import *
from core.modules.filesystem.filesystem import *

from core.plugins.spaces.spaces import *
from core.plugins.representation.representation import *
from core.plugins.installator.installator import *
from core.plugins.updater.updater import *
from core.plugins.repo.repo import *
from core.plugins.math.math import *

class Gui:
    def __init__(self):
        self.data = None

    async def init(self, variables, unique_object_id):
        spaces = Spaces()

        self.data = {
            "loop": asyncio.get_running_loop(),
            "variables": variables,
            "unique_object_id": unique_object_id,
            "spaces": spaces,
            "view": {"items": {}, "items1": {"obj": {}, "plg": {}}}
        }

        await self.data["spaces"].init(self.data["variables"])

        variables = await self.data["variables"].get(Path(""))

        for variable, value in variables.items():
            if "object" in value:
                obj = value["object"]
                self.data[variable] = obj.value

        console = self.data["console"]
        variables = self.data["variables"]

        signals = self.data["signals"]
        await signals.write(Path(f"objects/{unique_object_id}"), {"on": True})

        device = Device()
        await device.init(variables, console = console)
        await device.create(Path("device"))

        device_os = await device.get_os()
        await device.write(Path("device/system"), device_os[0])
        await device.write(Path("device/release"), device_os[1])
        await device.write(Path("device/version"), device_os[2])
        self.data["device"] = device

        installator = Installator()
        await installator.init(variables)
        self.data["installator"] = installator

        updater = Updater()
        await updater.init(await self.data["settings"].get(Path("repo/url")), await self.data["settings"].get(Path("repo/config_url")))
        self.data["updater"] = updater

        repo = Repo()
        await repo.init(await device.get_separator())
        self.data["repo"] = repo

        path_utils = Path_utils()
        await path_utils.init()
        self.data["path_utils"] = path_utils
        await path_utils.create(Path("objects"))
        await path_utils.write(Path("objects"), Path("core/objects"))
        await path_utils.create(Path("plugins"))
        await path_utils.write(Path("plugins"), Path("core/plugins"))
        await path_utils.create(Path("modules"))
        await path_utils.write(Path("modules"), Path("core/modules"))

        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("core/plugins/gui/font/ClarityCity-Light.ttf", 18)

        dpg.bind_font(default_font)
        with dpg.viewport_menu_bar():
            with dpg.menu(label = "tasks"):
                with dpg.menu(label = "tasks manager"):
                    dpg.add_menu_item(label = "open", callback = self.tasks_callback, user_data = [0])

            with dpg.menu(label = "spaces", tag = "spaces_menu"):
                dpg.add_menu_item(label = "create", callback = self.create_space_callback)

            with dpg.menu(label = "console"):
                dpg.add_menu_item(label = "open", callback = self.console_callback, user_data = [0])

            with dpg.menu(label = "settings"):
                dpg.add_menu_item(label = "open", callback = self.settings_callback)

            with dpg.menu(label = "install"):
                with dpg.menu(label = "modules"):
                    with dpg.menu(label = "local"):
                        dpg.add_menu_item(label = "single", callback = self.local_callback, user_data = [0, 0])
                        dpg.add_menu_item(label = "pack", callback = self.local_callback, user_data = [0, 1])
                    with dpg.menu(label = "online"):
                        dpg.add_menu_item(label = "single", callback = self.url_callback, user_data = [0, 0])
                        dpg.add_menu_item(label = "pack", callback = self.url_callback, user_data = [0, 1])
                with dpg.menu(label = "plugins"):
                    with dpg.menu(label = "local"):
                        dpg.add_menu_item(label = "single", callback = self.local_callback, user_data = [1, 0])
                        dpg.add_menu_item(label = "pack", callback = self.local_callback, user_data = [1, 1])
                    with dpg.menu(label = "online"):
                        dpg.add_menu_item(label = "single", callback = self.url_callback, user_data = [1, 0])
                        dpg.add_menu_item(label = "pack", callback = self.url_callback, user_data = [1, 1])
                with dpg.menu(label = "objects"):
                    with dpg.menu(label = "local"):
                        dpg.add_menu_item(label = "single", callback = self.local_callback, user_data = [2, 0])
                        dpg.add_menu_item(label = "pack", callback = self.local_callback, user_data = [2, 1])
                    with dpg.menu(label = "online"):
                        dpg.add_menu_item(label = "single", callback = self.url_callback, user_data = [2, 0])
                        dpg.add_menu_item(label = "pack", callback = self.url_callback, user_data = [2, 1])
                with dpg.menu(label = "repos"):
                    with dpg.menu(label = "local"):
                        dpg.add_menu_item(label = "single", callback = self.local_callback, user_data = [3, 0])
                        dpg.add_menu_item(label = "pack", callback = self.local_callback, user_data = [3, 1])
                    with dpg.menu(label = "online"):
                        dpg.add_menu_item(label = "single", callback = self.url_callback, user_data = [3, 0])
                        dpg.add_menu_item(label = "pack", callback = self.url_callback, user_data = [3, 1])

            dpg.add_menu_item(label = "updater", callback = self.updater_callback)
            dpg.add_menu_item(label = "exit", callback = self.exit_callback)

        dpg.create_viewport(title = "core", width = 2560, height = 1440)

        dpg.setup_dearpygui()
        dpg.show_viewport()

        signal_path = Path(f"objects/{unique_object_id}/on")
        done = False

        while dpg.is_dearpygui_running() and not done:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

            if await signals.get(signal_path) == False:
                done = True

        dpg.destroy_context()

    def updater_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.updater_function())

    async def updater_function(self):
        settings = self.data["settings"]
        version = await settings.get(Path("core/version"))

        updater = self.data["updater"]
        latest_version_number = await updater.get_latest_version_number(version)

        with dpg.window(label = "updater", tag = "updater_window", on_close = self.on_close_callback):
            dpg.add_text(f"version : {version}")
            dpg.add_text(f"latest version : {latest_version_number}")

        # temporaire, il faut quelque chose comme : if version < latest_version_number
        if version != latest_version_number:
            if dpg.does_item_exist("updater_window"):
                dpg.add_button(label = "update", parent = "updater_window", callback = self.update_callback)

    def update_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.update_function())

    async def update_function(self):
        updater = self.data["updater"]
        await updater.update()

    def local_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.local_function(user_data))

    async def local_function(self, args):
        object_type = args[0]
        number = args[1]

        with dpg.file_dialog(directory_selector = False, show = False, callback = self.local_install_callback, id = "file_dialog_id", width = 700, height = 400, user_data = [number, object_type]):
            dpg.add_file_extension(".zip", color = (150, 255, 150, 255), custom_text = "[Zip]")

        with dpg.window(label = "local install", on_close = self.on_close_callback):
            dpg.add_button(label = "select file", callback = lambda: dpg.show_item("file_dialog_id"))

    def local_install_callback(self, sender, app_data, user_data):
        user_data.insert(0, app_data)
        self.data["loop"].create_task(self.local_install_function(user_data))

    async def local_install_function(self, args):
        data = args[0]
        number = args[1]
        object_type = args[2]
        file_name = data["file_name"]
        file_path = data["file_path_name"]

        file_path_obj = Path(file_path, mode = 1)

        # only .zip pour le moment
        # print(file_name, file_path)
        # core-main.zip C:\Users\Comes\Downloads\core-main.zip

        result_code = 1

        if result_code == 1:
            with dpg.window(label = "prompt", on_close = self.on_close_callback, tag = "overwrite_object_installation_window"):
                dpg.add_text("an object is already installed with the same name, would you like to overwrite it ?")
                with dpg.group(horizontal = True):
                    dpg.add_button(label = "uninstall old and install new object")
                    dpg.add_button(label = "cancel installation", callback = self.cancel_installation_callback)

        # await self.data["installator"].install([1, object_type, number, file_path_obj])

        # install va return un code si l'objet existe déjà : 0 = ok, 1 = already exists
        # si return == 1 : on affiche un popup qui demande si l'utilisateur veut overwrite ou abandonner
        # si il veut overwrite : on appelle install mais avec un mode spécial pour supprimer le dossier existant + installer
        # il faut aussi ajouter des fonctions de clean du dossier data

    def cancel_installation_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.cancel_installation_function())

    async def cancel_installation_function(self):
        if dpg.does_item_exist("overwrite_object_installation_window"):
            dpg.delete_item("overwrite_object_installation_window")

    def url_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.url_function(user_data))

    async def url_function(self, args):
        with dpg.window(label = "url", on_close = self.on_close_callback):
            with dpg.group(horizontal = True):
                dpg.add_text("url : ")
                dpg.add_input_text(tag = "url_value")
                dpg.add_button(label = "install", callback = self.install_callback, user_data = args)

            dpg.add_button(label = "install from repository", callback = self.install_from_repo_callback, user_data = args)

    def install_from_repo_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.install_from_repo_function(user_data))

    async def install_from_repo_function(self, args):
        with dpg.window(label = "install from repository", on_close = self.on_close_callback):
            repo_obj = self.data["repo"]
            repos = await repo_obj._get(Path("repo"))
            for repo, value in repos.items():
                with dpg.collapsing_header(label = repo):
                    for file, file_value in value.items():
                        repo_file_content = file_value["content"]
                        with dpg.collapsing_header(label = file):

                            with dpg.collapsing_header(label = "objects"):
                                objects = repo_file_content["content"]["objects"]
                                for obj, obj_value in objects.items():
                                    with dpg.group(horizontal = True):
                                        dpg.add_text(obj)
                                        dpg.add_button(label = "install")

                            with dpg.collapsing_header(label = "plugins"):
                                plugins = repo_file_content["content"]["plugins"]
                                for plg, plg_value in plugins.items():
                                    with dpg.group(horizontal = True):
                                        dpg.add_text(plg)
                                        dpg.add_button(label = "install")

                            with dpg.collapsing_header(label = "modules"):
                                modules = repo_file_content["content"]["modules"]
                                for mdl, mdl_value in modules.items():
                                    with dpg.group(horizontal = True):
                                        dpg.add_text(mdl)
                                        dpg.add_button(label = "install")

    def install_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.install_function(user_data))

    async def install_function(self, args):
        object_type = args[0]
        number = args[1]
        url = dpg.get_value("url_value")

        await self.data["installator"].install([0, object_type, number, url])

    def tasks_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.tasks_function(user_data))

    def exit_callback(self):
        self.data["loop"].create_task(self.exit_function())

    def settings_callback(self):
        self.data["loop"].create_task(self.settings_function())

    def console_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.console_function(user_data))

    async def tasks_function(self, args):
        mode = args[0]

        if mode == 0:
            scheduler = self.data["scheduler"]
        elif mode == 1:
            space_name = args[1]
            scheduler = await self.data["spaces"].get(Path(f"{space_name}/modules/{space_name}/scheduler"))

        classic_running = {}
        complex_running = {}

        if await scheduler.exists(Path("classic_task")):
            temp = await scheduler.get(Path("classic_task"))

            for obj_name in temp:
                if obj_name not in classic_running:
                    classic_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in classic_running[obj_name]:
                        classic_running[obj_name].append(unique_id)

        if await scheduler.exists(Path("complex_task/running")):
            temp = await scheduler.get(Path("complex_task/running"))

            for obj_name in temp:
                if obj_name not in complex_running:
                    complex_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in complex_running[obj_name]:
                        complex_running[obj_name].append(unique_id)

        with dpg.window(label = "tasks", on_close = self.on_close_callback):
            for obj, value in classic_running.items():
                if not obj in ["running", "to_run"]:
                    dpg.add_text(obj, tag = f"{obj}_text")
                    self.data["view"]["items"][obj] = {}

                    for unique_id in value:
                        with dpg.group(horizontal = True):
                            if mode == 0:
                                user_data = [obj, unique_id, mode]
                            elif mode == 1:
                                user_data = [obj, unique_id, mode, space_name]

                            dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(Path(f"loader/gui/{self.data["unique_object_id"]}/enabled")), tag = f"checkbox_{obj}:{unique_id}")
                            dpg.add_button(label = "remove", tag = f"remove_{obj}:{unique_id}", callback = self.tasks_remove_object_callback, user_data = user_data)

                        self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"] = {"show": True}
                        self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"] = {"show": True}

            for obj, value in complex_running.items():
                if not obj in ["running", "to_run"]:
                    dpg.add_text(obj, tag = f"{obj}_text")
                    self.data["view"]["items"][obj] = {}

                    for unique_id in value:
                        with dpg.group(horizontal = True):
                            if mode == 0:
                                user_data = [obj, unique_id, mode]
                            elif mode == 1:
                                user_data = [obj, unique_id, mode, space_name]

                            dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(Path(f"loader/gui/{self.data["unique_object_id"]}/enabled")), tag = f"checkbox_{obj}:{unique_id}")
                            dpg.add_button(label = "remove", callback = self.tasks_remove_object_callback, user_data = user_data, tag = f"remove_{obj}:{unique_id}")

                        self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"] = {"show": True}
                        self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"] = {"show": True}

    def tasks_remove_object_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.tasks_remove_object_function(user_data))

    async def tasks_remove_object_function(self, args):
        obj = args[0]
        unique_id = args[1]
        mode = args[2]

        if mode == 0:
            scheduler = self.data["scheduler"]
            loader = self.data["loader"]
        elif mode == 1:
            space_name = args[3]
            scheduler = await self.data["spaces"].get(Path(f"{space_name}/modules/{space_name}/scheduler"))
            loader = await self.data["spaces"].get(Path(f"{space_name}/modules/{space_name}/loader"))

        items = [f"remove_{obj}:{unique_id}", f"checkbox_{obj}:{unique_id}"]
        for item in items:
            if dpg.does_item_exist(item):
                dpg.delete_item(item)

        del self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"]
        del self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"]

        await loader.loader.remove(Path(f"loader/{obj}/{unique_id}"))

        if await scheduler.exists(Path(f"classic_task/{obj}/{unique_id}")):
            await scheduler.remove(Path(f"classic_task/{obj}/{unique_id}"))

        if await scheduler.exists(Path(f"complex_task/running/{obj}/{unique_id}")):
            await scheduler.remove(Path(f"complex_task/running/{obj}/{unique_id}"))

        if await scheduler.exists(Path(f"complex_task/to_run/{obj}/{unique_id}")):
            await scheduler.remove(Path(f"complex_task/running/{obj}/{unique_id}"))

        if len(self.data["view"]["items"][obj]) == 0:
            item = f"{obj}_text"
            if dpg.does_item_exist(item):
                dpg.delete_item(item)
                del self.data["view"]["items"][obj]

            await loader.loader.remove(Path(f"loader/{obj}"))

            if await scheduler.exists(Path(f"classic_task/{obj}")):
                await scheduler.remove(Path(f"classic_task/{obj}"))

            if await scheduler.exists(Path(f"complex_task/running/{obj}")):
                await scheduler.remove(Path(f"complex_task/running/{obj}"))

            if await scheduler.exists(Path(f"complex_task/to_run/{obj}")):
                await scheduler.remove(Path(f"complex_task/to_run/{obj}"))

        if unique_id == self.data["unique_object_id"] and mode == 0:
            signals = self.data["signals"]
            await signals.write(Path(f"objects/{self.data["unique_object_id"]}/on"), False)

    def tasks_checkbox_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.change_tasks_function(user_data, app_data))

    async def change_tasks_function(self, user_data, value):
        obj = user_data[0]
        unique_id = user_data[1]
        mode = user_data[2]

        if mode == 0:
            scheduler = self.data["scheduler"]
        elif mode == 1:
            space_name = args[3]
            scheduler = await self.data["spaces"].get(Path(f"{space_name}/modules/{space_name}/scheduler"))

        if value == True:
            await scheduler.enable(obj, unique_id)
        else:
            await scheduler.disable(obj, unique_id)

    async def exit_function(self):
        signals = self.data["signals"]
        await signals.write(Path(f"objects/{self.data["unique_object_id"]}/on"), False)

    async def settings_function(self):
        with dpg.window(label = "settings", on_close = self.on_close_callback):
            for name, value in self.data.items():
                dpg.add_text(f"{name} settings :")
                if hasattr(value, "__dict__"):
                    for _name, _value in value.__dict__.items():
                        dpg.add_text(f"self.{_name} : {_value}")

    async def console_function(self, args):
        mode = args[0]

        if mode == 0:
            console = self.data["console"]
        elif mode == 1:
            space_name = args[1]
            console = await self.data["spaces"].get(Path(f"{space_name}/modules/{space_name}/console"))

        with dpg.window(label = "console", on_close = self.on_close_callback):
            for console_name, value in console.console.json.items():
                for message in value:
                    dpg.add_text(f"[{console_name}] {message}")

    def create_space_callback(self):
        self.data["loop"].create_task(self.create_space_function())

    async def create_space_function(self):
        with dpg.window(label = "create space", tag = "create_space_window", on_close = self.on_close_callback):
            dpg.add_input_text(label = "space's name", tag = "space_name")
            dpg.add_button(label = "create", callback = self.space_creation_callback)

    def space_creation_callback(self):
        space_name = dpg.get_value("space_name")

        if not dpg.does_item_exist("sub_open_space"):
            with dpg.menu(label = "open", parent = "spaces_menu", tag = "sub_open_space"):
                dpg.add_menu_item(label = space_name, callback = self.space_creation_specific_callback, user_data = [space_name])
        else:
            dpg.add_menu_item(label = space_name, parent = "sub_open_space", callback = self.space_creation_specific_callback, user_data = [space_name])

        item = "create_space_window"
        if dpg.does_item_exist(item):
            dpg.delete_item(item)
        #dpg.hide_item("create_space_window")
        #dpg.show_item("create_space_window")

        self.data["loop"].create_task(self.space_creation_function(space_name))

    def space_creation_specific_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_creation_specific_function(user_data))

    async def space_creation_specific_function(self, args):
        self.data["loop"].create_task(self.space_creation_function(args[0]))

    async def space_creation_function(self, space_name):
        await self.data["spaces"].create(Path(space_name))
        await self.data["spaces"].write(Path(f"{space_name}/objects"), {})
        await self.data["spaces"].write(Path(f"{space_name}/modules"), {})

        memory = Memory()
        await memory.init()
        await memory.create(Path("variables"))
        await self.data["spaces"].write(Path(f"{space_name}/modules/memory"), memory)

        variables = Variables()
        await variables.init()
        await memory.write(Path("variables"), variables)
        await self.data["spaces"].write(Path(f"{space_name}/modules/variables"), variables)

        console = Console()
        await console.init(variables)
        await console.create(Path("core"))
        await console.write(Path("core"), ["memory > ready", "variables > ready"])
        await self.data["spaces"].write(Path(f"{space_name}/modules/console"), console)

        """
        states = States()
        await states.init()
        await self.data["spaces"].write(Path(f"{space_name}/modules/states"), states)
        """

        identifier = Identifier()
        await identifier.init(variables, console = console)
        await identifier.create(Path("objects_id"))
        await self.data["spaces"].write(Path(f"{space_name}/modules/identifier"), identifier)

        representation = Representation()
        await representation.init(variables)
        await representation.create(Path("objects"))
        await representation.create(Path("settings"))
        await representation.write(Path("settings/dx"), 0)
        await representation.write(Path("settings/dy"), 0)
        await representation.write(Path("settings/f"), 10)
        await self.data["spaces"].write(Path(f"{space_name}/modules/representation"), representation)

        dimension_x = 1000
        dimension_y = 1000

        default = []
        for i in range(dimension_x * dimension_y):
            for _ in range(4):
                default.append(0)

        await representation.write(Path("objects/core"), {
            "dimensions": [
                dimension_x,
                dimension_y
            ],
            "color": [
                1, 1, 1, 1
            ],
            "position": [
                0, 0
            ],
            "render": 2,
            "mode": "pixel",
            "refresh": False,
            "done": False
        })

        if not dpg.does_item_exist(f"{space_name}_representation_texture_tag"):
            with dpg.texture_registry():
                # dpg.add_static_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                # dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = default, tag = f"{space_name}_representation_texture_tag")

        await variables.create(Path("objects"))
        await variables.create(Path("app"))
        app_value = Variable()
        await app_value.init("on", console = console)
        await variables.write(Path("app/value"), app_value)

        json = Json()
        await json.init(console = console)
        await json.create(Path("settings"))
        await json.write(Path("settings"), await json.get_from_file(Path("core/data/core/settings.json", mode = 1)))
        await self.data["spaces"].write(Path(f"{space_name}/modules/json"), json)

        symbols = Symbols()
        await symbols.init(variables, console = console)
        await symbols.create(Path("symbols"))
        await self.data["spaces"].write(Path(f"{space_name}/modules/symbols"), symbols)

        settings_value = await json.get(Path("settings"))
        for key, value in settings_value.items():
            if key not in await symbols.get(Path("symbols")):
                await symbols.write(Path(f"symbols/{key}"), value)

        pattern = "<[a-z/<>_]*>"

        for key in await symbols.get(Path("symbols")):
            current_value = await symbols.get(Path(f"symbols/{key}"))
            done = False

            while not done:
                match = re.search(pattern, current_value)

                if match:
                    to_replace = match.group()
                    if to_replace in await symbols.get(Path("symbols")):
                        replace_by = await symbols.get(Path(f"symbols/{to_replace}"))
                    else:
                        replace_by = "<not_found>"

                    current_value = current_value.replace(to_replace, replace_by)
                else:
                    await symbols.write(Path(key), current_value)
                    done = True

        loader = Loader()
        await loader.init(variables, await symbols.get(Path("<module_folder>")), await symbols.get(Path("<plugin_folder>")), await symbols.get(Path("<object_folder>")), console = console)
        await self.data["spaces"].write(Path(f"{space_name}/modules/loader"), loader)

        settings = Settings()
        await settings.init(variables, loader, console = console)
        await settings.create(Path("objects"))
        await settings.create(Path("plugins"))
        await self.data["spaces"].write(Path(f"{space_name}/modules/settings"), settings)

        await settings.write(Path("objects/folder"), await symbols.get(Path("<object_folder>")))
        await settings.write(Path("objects/path"), await symbols.get(Path("<object_config>")))
        await settings.write(Path("objects/content"), await settings.settings.get_from_file(Path(await settings.get(Path("objects/path")), mode = 1)))

        await settings.write(Path("plugins/folder"), await symbols.get(Path("<plugin_folder>")))
        await settings.write(Path("plugins/path"), await symbols.get(Path("<plugin_config>")))
        await settings.write(Path("plugins/content"), await settings.settings.get_from_file(Path(await settings.get(Path("plugins/path")), mode = 1)))

        for plg in await settings.get(Path("plugins/content/plugins")):
            await settings.enable(Path(f"plugins/content/{plg}/enabled"))
            await settings.save(Path("plugins/path"), Path("plugins/content"))

        for obj in await settings.get(Path("objects/content/objects")):
            await settings.enable(Path(f"objects/content/{obj}/enabled"))
            await settings.save(Path("objects/path"), Path("objects/content"))

        """
        for obj in await settings.get("objects/content/objects"):
            if await settings.get(f"objects/content/{obj}/enabled") == True:
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(obj, "object", unique_object_id)
                await loader.write(f"loader/{obj}/{unique_object_id}/enabled", True)

        for plg in await settings.get("plugins/content/plugins"):
            if await settings.get(f"plugins/content/{plg}/enabled") == True:
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(plg, "plugin", unique_object_id)
                await loader.write(f"loader/{plg}/{unique_object_id}/enabled", True)
        """

        moment = Moment()
        await moment.init(variables)
        await moment.create(Path("time"))
        await moment.write(Path("time/value1"), 0)
        await self.data["spaces"].write(Path(f"{space_name}/modules/moment"), moment)

        scheduler = Scheduler()
        await scheduler.init(variables, console = console)
        await scheduler.create(Path("classic_task"))
        await scheduler.create(Path("complex_task"))
        await scheduler.settings(Path("classic_task/mode"), "classic")
        await scheduler.settings(Path("classic_task/model"), "")
        await scheduler.settings(Path("complex_task/mode"), "complex")
        await self.data["spaces"].write(Path(f"{space_name}/modules/scheduler"), scheduler)

        await self.space_open_function(space_name)

    async def space_open_function(self, name):
        with dpg.window(label = name, on_close = self.on_close_callback):
            with dpg.menu_bar():
                dpg.add_menu_item(label = "objects", callback = self.space_objects_callback, user_data = name)
                dpg.add_menu_item(label = "settings", callback = self.space_settings_callback, user_data = name)
                with dpg.menu(label = "moment"):
                    dpg.add_menu_item(label = "next", callback = self.space_change_moment_callback, user_data = [name, 1, 0, -1])
                    dpg.add_menu_item(label = "previous", callback = self.space_change_moment_callback, user_data = [name, -1, 0, -1])
                dpg.add_menu_item(label = "tasks", callback = self.tasks_callback, user_data = [1, name])
                with dpg.menu(label = "console"):
                    dpg.add_menu_item(label = "open", callback = self.console_callback, user_data = [1, name])
                with dpg.menu(label = "representation"):
                    with dpg.menu(label = "1D"):
                        dpg.add_menu_item(label = "open", callback = self.space_representation_visualisation_callback, user_data = [name, 0])
                    with dpg.menu(label = "3D"):
                        dpg.add_menu_item(label = "open")

    def space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_representation_visualisation_function(user_data))

    async def space_representation_visualisation_function(self, args):
        space_name = args[0]
        mode = args[1]

        representation = await self.data["spaces"].get(Path(f"{space_name}/modules/representation"))
        objects = await representation.get(Path("objects"))

        core_dimension_x = objects["core"]["dimensions"][0]
        core_dimension_y = objects["core"]["dimensions"][1]

        texture_data = dpg.get_value(f"{space_name}_representation_texture_tag")

        f = await representation.get(Path("settings/f"))
        dx = await representation.get(Path("settings/dx"))
        dy = await representation.get(Path("settings/dy"))

        if await representation.exists(Path("settings/_f")):
            _f = await representation.get(Path("settings/_f"))
        else:
            _f = f

        if await representation.exists(Path("settings/_dx")):
            _dx = await representation.get(Path("settings/_dx"))
        else:
            _dx = dx

        if await representation.exists(Path("settings/_dy")):
            _dy = await representation.get(Path("settings/_dy"))
        else:
            _dy = dy

        for object_name, object_data in objects.items():
            if object_data["done"] == False:
                render_mode = object_data["mode"]
                render_dimensions = object_data["render"]

                # il faut maintenant ajouter un moyen pour supprimer les anciens pixels avant la prochaine frame

                if render_mode == "image" and render_dimensions == 2:
                    path = object_data["path"]
                    position_x = object_data["position"][0]
                    position_y = object_data["position"][1]

                    image = Image.open(path).convert("RGBA")

                    if "dimension" in object_data:
                        dimension_x = object_data["dimension"][0]
                        dimension_y = object_data["dimension"][1]
                    else:
                        dimension_x, dimension_y = image.size

                    dpg_image = []
                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            pixel = image.getpixel((x, y))
                            dpg_image.append(pixel[0] / 255)
                            dpg_image.append(pixel[1] / 255)
                            dpg_image.append(pixel[2] / 255)
                            dpg_image.append(255 / 255)

                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            tex_x = position_x + x
                            tex_y = position_y + y

                            global_index = (tex_y * core_dimension_x + tex_x) * 4
                            local_index = (y * dimension_x + x) * 4

                            for c in range(4):
                                texture_data[global_index + c] = dpg_image[local_index + c]

                elif render_mode == "pixel" and render_dimensions == 2:
                    dimension_x = object_data["dimensions"][0]
                    dimension_y = object_data["dimensions"][1]
                    position_x = object_data["position"][0]
                    position_y = object_data["position"][1]
                    color = object_data["color"]
                    color_size = len(color)

                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            tex_x = position_x + x
                            tex_y = position_y + y

                            index = (tex_y * core_dimension_x + tex_x) * color_size

                            for c in range(color_size):
                                texture_data[index + c] = color[c]

                elif render_mode == "object" and render_dimensions == 3:
                    points = object_data["points"]
                    center = [core_dimension_x // 2, core_dimension_y // 2]
                    color = [0, 0, 0, 0]
                    color_size = len(color)

                    two_dim_points = []
                    for point in points:
                        x = point[0]
                        y = point[1]
                        z = point[2]

                        if z != 0:
                            position_x = round(((x - _dx) * _f) / z)
                            position_y = round(((y - _dy) * _f) / z)

                            tex_x = position_x + center[0]
                            tex_y = position_y + center[1]

                            two_dim_points.append([tex_x, tex_y])

                    for i in range(0, len(two_dim_points), 2):
                        point1 = two_dim_points[i]
                        point2 = two_dim_points[i + 1]

                        if point1 != point2:
                            _points = await bresenham(point1[0], point1[1], point2[0], point2[1])
                            for point in _points:
                                index = (point[1] * core_dimension_x + point[0]) * color_size
                                for c in range(color_size):
                                    texture_data[index + c] = 1.0

                    two_dim_points = []
                    for point in points:
                        x = point[0]
                        y = point[1]
                        z = point[2]

                        if z != 0:
                            position_x = round(((x - dx) * f) / z)
                            position_y = round(((y - dy) * f) / z)

                            tex_x = position_x + center[0]
                            tex_y = position_y + center[1]

                            two_dim_points.append([tex_x, tex_y])

                    for i in range(0, len(two_dim_points), 2):
                        point1 = two_dim_points[i]
                        point2 = two_dim_points[i + 1]

                        if point1 != point2:
                            points = await bresenham(point1[0], point1[1], point2[0], point2[1])
                            for point in points:
                                index = (point[1] * core_dimension_x + point[0]) * color_size
                                for c in range(color_size):
                                    texture_data[index + c] = color[c]
                        else:
                            index = (point1[1] * core_dimension_x + point1[0]) * color_size
                            for c in range(color_size):
                                texture_data[index + c] = color[c]

                if object_data["refresh"] == False:
                    object_data["done"] = True

        dpg.set_value(f"{space_name}_representation_texture_tag", texture_data)

        if mode == 0:
            with dpg.window(label = f"representation : {space_name}", tag = f"{space_name}_space_representation_window", on_close = self.on_close_callback):
                dpg.add_image(f"{space_name}_representation_texture_tag")
                with dpg.group(horizontal = True):
                    dpg.add_button(label = "<--", callback = self.space_change_moment_callback, user_data = [space_name, -1, 0, 0])
                    dpg.add_button(label = "-->", callback = self.space_change_moment_callback, user_data = [space_name, 1, 0, 0])
                    dpg.add_button(label = "refresh", callback = self.refresh_space_representation_visualisation_callback, user_data = [space_name, 1])
                with dpg.group(horizontal = True):
                    dpg.add_button(label = "up", callback = self.space_change_moment_callback, user_data = [space_name, 1, 1, 2])
                    dpg.add_button(label = "down", callback = self.space_change_moment_callback, user_data = [space_name, -1, 1, 2])
                    dpg.add_button(label = "left", callback = self.space_change_moment_callback, user_data = [space_name, -1, 1, 1])
                    dpg.add_button(label = "right", callback = self.space_change_moment_callback, user_data = [space_name, 1, 1, 1])
                with dpg.group(horizontal = True):
                    dpg.add_slider_int(min_value = 0, max_value = 20, default_value = f, callback = self.zoom_slider_callback, user_data = space_name)
        elif mode == 1:
            dpg.set_value(f"{space_name}_space_representation_window", f"{space_name}_representation_texture_tag")

    def zoom_slider_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.zoom_slider_function(app_data, user_data))

    async def zoom_slider_function(self, args, space_name):
        representation = await self.data["spaces"].get(Path(f"{space_name}/modules/representation"))
        f = await representation.get(Path("settings/f"))
        await representation.write(Path("settings/_f"), f)
        await representation.write(Path("settings/f"), args)

        await self.space_representation_visualisation_function([space_name, 1])

    def refresh_space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_representation_visualisation_function(user_data))

    def space_change_moment_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_change_moment_function(user_data))

    async def space_change_moment_function(self, args):
        space_name = args[0]
        value = args[1]
        mode = args[2]
        mode1 = args[3]

        representation = await self.data["spaces"].get(Path(f"{space_name}/modules/representation"))

        if mode == 0:
            moment = await self.data["spaces"].get(Path(f"{space_name}/modules/moment"))
            loader = await self.data["spaces"].get(Path(f"{space_name}/modules/loader"))
            scheduler = await self.data["spaces"].get(Path(f"{space_name}/modules/scheduler"))

            await representation.write(Path("settings/dx"), await representation.get(Path("settings/dx")) + value)
            # await representation.write("settings/dy", await representation.get("settings/dy") + value)

            await moment.write(Path("time/value1"), await moment.get(Path("time/value1")) + value)

            print(f"moment {await moment.get(Path("time/value1"))} :")

            for obj_name in await loader.get(Path("loader")):
                objects = await loader.get(Path(f"loader/{obj_name}/objects"))

                for unique_object_id, value in objects.items():
                    if await loader.get(Path(f"loader/{obj_name}/{unique_object_id}/enabled")) == True:
                        temp_objs = await loader.get(Path(f"loader/{obj_name}/objects/{unique_object_id}/object/objects"))
                        if temp_objs[0].object_type == "classic":
                            if not await scheduler.exists(Path(f"classic_task/{obj_name}")):
                                await scheduler.write(Path(f"classic_task/{obj_name}"), {})
                            await scheduler.write(Path(f"classic_task/{obj_name}/{unique_object_id}"), value)
                        elif temp_objs[0].object_type == "complex":
                            if not await scheduler.exists(Path(f"complex_task/to_run/{obj_name}")):
                                await scheduler.write(Path(f"complex_task/to_run/{obj_name}"), {})

                            if not await scheduler.exists(Path(f"complex_task/running/{obj_name}/{unique_object_id}")):
                                await scheduler.write(Path(f"complex_task/to_run/{obj_name}/{unique_object_id}"), temp_objs)

                            if not await scheduler.exists(Path(f"complex_task/running/{obj_name}")):
                                await scheduler.write(Path(f"complex_task/running/{obj_name}"), {})

                            if not await scheduler.exists(Path(f"complex_task/running/{obj_name}/{unique_object_id}")):
                                await scheduler.write(Path(f"complex_task/running/{obj_name}/{unique_object_id}"), True)
                    else:
                        if await scheduler.exists(Path(f"classic_task/{obj_name}/{unique_object_id}")):
                            await scheduler.write(Path(f"classic_task/{obj_name}/{unique_object_id}"), {})

            await scheduler.run(Path("complex_task/to_run"))
            await scheduler.write(Path("complex_task/to_run"), {})

            await scheduler.run(Path("classic_task"))

            print("=" * 50)

        elif mode1 == 1:
            dx = await representation.get(Path("settings/dx"))
            await representation.write(Path("settings/_dx"), dx)
            await representation.write(Path("settings/dx"), dx + value)

        elif mode1 == 2:
            dy = await representation.get(Path("settings/dy"))
            await representation.write(Path("settings/_dy"), dy)
            await representation.write(Path("settings/dy"), dy + value)

        if mode1 != -1:
            await self.space_representation_visualisation_function([space_name, 1])

    def space_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_objects_function(user_data))

    async def space_objects_function(self, space_name):
        with dpg.window(label = "objects", on_close = self.on_close_callback, tag = "space_objects_window"):
            dpg.add_text("current objects :")
            for obj in await self.data["spaces"].get(Path(f"{space_name}/objects")):
                dpg.add_text(obj)
            dpg.add_button(label = "add objects", callback = self.space_add_objects_callback, user_data = space_name)

    def space_add_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_add_objects_function(user_data))

    async def space_add_objects_function(self, space_name):
        settings = await self.data["spaces"].get(Path(f"{space_name}/modules/settings"))

        with dpg.window(label = "add objects", on_close = self.on_close_callback, tag = "space_add_objects_window"):
            dpg.add_text("objects :")

            self.data["view"]["items1"]["obj"] = {}
            self.data["view"]["items1"]["plg"] = {}

            # for obj in await self.data["path_utils"].ls(await self.data["path_utils"].get("objects"), mode = 1):
                # self.data["view"]["items1"]["obj"][obj] = {}

            # for plg in await self.data["path_utils"].ls(await self.data["path_utils"].get("plugins"), mode = 1):
                # self.data["view"]["items1"]["plg"][plg] = {}

            for obj in await settings.get(Path("objects/content/objects")):
                self.data["view"]["items1"]["obj"][obj] = {}

            for plg in await settings.get(Path("plugins/content/plugins")):
                self.data["view"]["items1"]["plg"][plg] = {}

            for obj in self.data["view"]["items1"]["obj"]:
                with dpg.group(horizontal = True):
                    dpg.add_text(obj)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{obj}_amount_input")

            dpg.add_text("plugins :")
            for plg in self.data["view"]["items1"]["plg"]:
                with dpg.group(horizontal = True):
                    dpg.add_text(plg)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{plg}_amount_input")

            dpg.add_button(label = "save", callback = self.space_save_objects_callback, user_data = [space_name])

    def space_save_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_save_objects_function(user_data))

    async def space_save_objects_function(self, args):
        space_name = args[0]

        settings = await self.data["spaces"].get(Path(f"{space_name}/modules/settings"))
        loader = await self.data["spaces"].get(Path(f"{space_name}/modules/loader"))
        identifier = await self.data["spaces"].get(Path(f"{space_name}/modules/identifier"))

        for obj in self.data["view"]["items1"]["obj"]:
            amount = dpg.get_value(f"{obj}_amount_input")
            for _ in range(amount):
                unique_object_id = await identifier.generate_id(Path("objects_id"))
                await loader.load(obj, "object", unique_object_id)
                await loader.write(Path(f"loader/{obj}/{unique_object_id}/enabled"), True)

        for plg in self.data["view"]["items1"]["plg"]:
            amount = dpg.get_value(f"{plg}_amount_input")
            for _ in range(amount):
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(plg, "plugin", unique_object_id)
                await loader.write(Path(f"loader/{plg}/{unique_object_id}/enabled"), True)

        item = "space_add_objects_window"
        if dpg.does_item_exist(item):
            dpg.delete_item(item)

    def space_settings_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_settings_function(user_data))

    async def space_settings_function(self, name):
        with dpg.window(label = "settings", tag = "space_settings_window", on_close = self.on_close_callback):
            dpg.add_input_text(multiline = True, default_value = await self.data["spaces"].get(Path(name)), tag = "space_settings_raw")
            dpg.add_button(label = "save", callback = self.space_config_save_callback, user_data = name)

    def space_config_save_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_config_save_function(user_data))

    async def space_config_save_function(self, name):
        data = dpg.get_value("space_settings_raw")
        await self.data["spaces"].write(Path(name), ast.literal_eval(data))

        item = "space_settings_window"
        if dpg.does_item_exist(item):
            dpg.delete_item(item)

    def on_close_callback(self, sender):
        self.data["loop"].create_task(self.on_close_function(sender))

    async def on_close_function(self, sender):
        dpg.delete_item(sender)