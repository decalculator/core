import asyncio
import ast
import re

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
from core.modules.asynchrone.asynchrone import *

from core.plugins.spaces.spaces import *
from core.plugins.representation.representation import *
from core.plugins.installator.installator import *

class Cli:
    def __init__(self):
        self.data = None

    async def init(self, variables, unique_object_id):
        spaces = Spaces()

        self.data = {
            "loop": asyncio.get_running_loop(),
            "on": True,
            "variables": variables,
            "unique_object_id": unique_object_id,
            "spaces": spaces,
            "view": {"items": {}}
        }

        await self.data["spaces"].init(self.data["variables"])

        console_var = await self.data["variables"].get("console/object")
        self.data["console"] = console_var.value

        moment_var = await self.data["variables"].get("moment/object")
        self.data["moment"] = moment_var.value

        settings_var = await self.data["variables"].get("settings/object")
        self.data["settings"] = settings_var.value

        identifier_var = await self.data["variables"].get("identifier/object")
        self.data["identifier"] = identifier_var.value

        scheduler_var = await self.data["variables"].get("scheduler/object")
        self.data["scheduler"] = scheduler_var.value

        loader_var = await self.data["variables"].get("loader/object")
        self.data["loader"] = loader_var.value

        installator = Installator()
        await installator.init(self.data["variables"])
        self.data["installator"] = installator

        path_utils = Path_utils()
        await path_utils.init()
        self.data["path_utils"] = path_utils
        await path_utils.create("objects")
        await path_utils.write("objects", "core/objects")
        await path_utils.create("plugins")
        await path_utils.write("plugins", "core/plugins")
        await path_utils.create("modules")
        await path_utils.write("modules", "core/modules")

        await self.main_menu()

    async def main_menu(self):
        exit_main_menu_loop = False

        while not exit_main_menu_loop:
            print("0 : tasks manager")
            print("1 : create space")
            print("2 : open space")
            print("3 : console")
            print("4 : settings")
            print("5 : install")
            print("6 : exit")

            done = False
            possibilities = [0, 1, 2, 3, 4, 5, 6]

            while not done:
                choice = await ainput("your choice : ")
                if choice.isdigit():
                    choice = int(choice)
                    if choice in possibilities:
                        done = True

            if choice == 0:
                await self.tasks_manager(0)

            elif choice == 1:
                await self.create_space()

            elif choice == 2:
                pass

            elif choice == 3:
                await self.console(0)

            elif choice == 4:
                await self.settings(0)

            elif choice == 5:
                print("0 : single module")
                print("1 : module pack")
                print("2 : single plugin")
                print("3 : plugin pack")
                print("4 : single object")
                print("5 : object pack")

                done = False
                possibilities = [0, 1, 2, 3, 4, 5]

                while not done:
                    choice = await ainput("your choice : ")
                    if choice.isdigit():
                        choice = int(choice)
                        if choice in possibilities:
                            done = True

                url = await ainput("url : ")

                if choice == 0:
                    object_type = 0
                    value = 0
                elif choice == 1:
                    object_type = 0
                    value = 1

                elif choice == 2:
                    object_type = 1
                    value = 0
                elif choice == 3:
                    object_type = 1
                    value = 1

                elif choice == 4:
                    object_type = 2
                    value = 0
                elif choice == 5:
                    object_type = 2
                    value = 1

                await self.data["installator"].install(object_type, value, url)

            elif choice == 6:
                exit_main_menu_loop = True

    async def console(self, mode):
        if mode == 0:
            console = self.data["console"]
        elif mode == 1:
            space_name = args[1]
            console = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/console")

        for console_name, value in console.console.json.items():
            for message in value:
                print(f"[{console_name}] {message}")

    async def tasks_manager(self, mode):
        tab = " " * 4

        if mode == 0:
            scheduler = self.data["scheduler"]
        elif mode == 1:
            space_name = args[1]
            scheduler = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/scheduler")

        classic_running = {}
        complex_running = {}

        if await scheduler.exists("classic_task"):
            temp = await scheduler.get("classic_task")

            for obj_name in temp:
                if obj_name not in classic_running:
                    classic_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in classic_running[obj_name]:
                        classic_running[obj_name].append(unique_id)

        if await scheduler.exists("complex_task/running"):
            temp = await scheduler.get("complex_task/running")

            for obj_name in temp:
                if obj_name not in complex_running:
                    complex_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in complex_running[obj_name]:
                        complex_running[obj_name].append(unique_id)

        print("tasks :")
        for obj, value in classic_running.items():
            if not obj in ["running", "to_run"]:
                print(f"{tab}{obj}")
                self.data["view"]["items"][obj] = {}

                for unique_id in value:
                    user_data = [obj, unique_id, 0]

                    enabled = await self.data["loader"].get(f"loader/cli/{unique_id}/enabled")
                    print(f"{tab}{tab}{unique_id}, enabled : {enabled}")
                    # dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(f"loader/ui/{self.data["unique_object_id"]}/enabled"), tag = f"checkbox_{obj}:{unique_id}")
                    # dpg.add_button(label = "remove", tag = f"remove_{obj}:{unique_id}", callback = self.tasks_remove_object_callback, user_data = user_data)

                    self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"] = {"show": True}
                    self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"] = {"show": True}

        for obj, value in complex_running.items():
            if not obj in ["running", "to_run"]:
                print(f"{tab}{obj}")
                self.data["view"]["items"][obj] = {}

                for unique_id in value:
                    user_data = [obj, unique_id, 0]

                    enabled = await self.data["loader"].get(f"loader/cli/{unique_id}/enabled")
                    print(f"{tab}{tab}{unique_id}, enabled : {enabled}")
                    # dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(f"loader/ui/{self.data["unique_object_id"]}/enabled"), tag = f"checkbox_{obj}:{unique_id}")
                    # dpg.add_button(label = "remove", callback = self.tasks_remove_object_callback, user_data = user_data, tag = f"remove_{obj}:{unique_id}")

                    self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"] = {"show": True}
                    self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"] = {"show": True}

        done = False
        possibilities = ["remove", "disable", "enable", "exit"]

        while not done:
            command = await ainput("enter command (remove, disable, enable, exit) : ")
            if command in possibilities:
                done = True

        if command in ["remove", "disable", "enable"]:
            obj = await ainput("object name : ")

            done = False
            while not done:
                unique_id = await ainput("unique id : ")
                if unique_id.isdigit():
                    unique_id = int(unique_id)
                    # il faut vérifier ici qu'il existe
                    done = True

            if command == "remove":
                loader = self.data["loader"]
                del self.data["view"]["items"][obj][f"remove_{obj}:{unique_id}"]
                del self.data["view"]["items"][obj][f"checkbox_{obj}:{unique_id}"]

                await loader.loader.remove(f"loader/{obj}/{unique_id}")

                if await scheduler.exists(f"classic_task/{obj}/{unique_id}"):
                    await scheduler.remove(f"classic_task/{obj}/{unique_id}")

                if await scheduler.exists(f"complex_task/running/{obj}/{unique_id}"):
                    await scheduler.remove(f"complex_task/running/{obj}/{unique_id}")

                if await scheduler.exists(f"complex_task/to_run/{obj}/{unique_id}"):
                    await scheduler.remove(f"complex_task/running/{obj}/{unique_id}")

                if len(self.data["view"]["items"][obj]) == 0:
                    del self.data["view"]["items"][obj]

                    await loader.loader.remove(f"loader/{obj}")

                    if await scheduler.exists(f"classic_task/{obj}"):
                        await scheduler.remove(f"classic_task/{obj}")

                    if await scheduler.exists(f"complex_task/running/{obj}"):
                        await scheduler.remove(f"complex_task/running/{obj}")

                    if await scheduler.exists(f"complex_task/to_run/{obj}"):
                        await scheduler.remove(f"complex_task/to_run/{obj}")

            elif command == "disable":
                await scheduler.disable(obj, unique_id)

            elif command == "enable":
                await scheduler.enable(obj, unique_id)

    async def settings(self, mode):
        for name, value in self.data.items():
            print(f"{name} settings :")
            if hasattr(value, "__dict__"):
                for _name, _value in value.__dict__.items():
                    print(f"self.{_name} : {_value}")

    async def create_space(self):
        space_name = await ainput("space's name : ")

        await self.data["spaces"].create(space_name)
        await self.data["spaces"].write(f"{space_name}/objects", {})
        await self.data["spaces"].write(f"{space_name}/modules", {})

        memory = Memory()
        await memory.init()
        await memory.create("variables")
        await self.data["spaces"].write(f"{space_name}/modules/memory", memory)

        variables = Variables()
        await variables.init()
        await memory.write("variables", variables)
        await self.data["spaces"].write(f"{space_name}/modules/variables", variables)

        console = Console()
        await console.init(variables)
        await console.create("core")
        await console.write("core", ["memory > ready", "variables > ready"])
        await self.data["spaces"].write(f"{space_name}/modules/console", console)

        """
        states = States()
        await states.init()
        await self.data["spaces"].write(f"{space_name}/modules/states", states)
        """

        identifier = Identifier()
        await identifier.init(variables, console = console)
        await identifier.create("objects_id")
        await self.data["spaces"].write(f"{space_name}/modules/identifier", identifier)

        """
        representation = Representation()
        await representation.init(variables)
        await representation.create("objects")
        await representation.create("settings")
        await representation.write("settings/dx", 0)
        await representation.write("settings/dy", 0)
        await representation.write("settings/f", 10)
        await self.data["spaces"].write(f"{space_name}/modules/representation", representation)

        dimension_x = 1000
        dimension_y = 1000

        default = []
        for i in range(dimension_x * dimension_y):
            for _ in range(4):
                default.append(0)

        await representation.write("objects/core", {
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
                # dpg.add_static_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                # dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = default, tag = f"{space_name}_representation_texture_tag")
        """

        await variables.create("objects")
        await variables.create("app")
        app_value = Variable()
        await app_value.init("on", console = console)
        await variables.write("app/value", app_value)

        json = Json()
        await json.init(console = console)
        await json.create("settings")
        await json.write("settings", await json.get_from_file("core/modules/core/json/settings.json"))
        await self.data["spaces"].write(f"{space_name}/modules/json", json)

        symbols = Symbols()
        await symbols.init(variables, console = console)
        await symbols.create("symbols")
        await self.data["spaces"].write(f"{space_name}/modules/symbols", symbols)

        settings_value = await json.get("settings")
        for key, value in settings_value.items():
            if key not in await symbols.get("symbols"):
                await symbols.write(f"symbols/{key}", value)

        pattern = "<[a-z/<>_]*>"

        for key in await symbols.get("symbols"):
            current_value = await symbols.get(f"symbols/{key}")
            done = False

            while not done:
                match = re.search(pattern, current_value)

                if match:
                    to_replace = match.group()
                    if to_replace in await symbols.get("symbols"):
                        replace_by = await symbols.get(f"symbols/{to_replace}")
                    else:
                        replace_by = "<not_found>"

                    current_value = current_value.replace(to_replace, replace_by)
                else:
                    await symbols.write(key, current_value)
                    done = True

        loader = Loader()
        await loader.init(variables, await symbols.get("<module_folder>"), await symbols.get("<plugin_folder>"), await symbols.get("<object_folder>"), console = console)
        await self.data["spaces"].write(f"{space_name}/modules/loader", loader)

        settings = Settings()
        await settings.init(variables, loader, console = console)
        await settings.create("objects")
        await settings.create("plugins")
        await self.data["spaces"].write(f"{space_name}/modules/settings", settings)

        await settings.write("objects/folder", await symbols.get("<object_folder>"))
        await settings.write("objects/path", await symbols.get("<object_config>"))
        await settings.write("objects/content", await settings.settings.get_from_file(await settings.get("objects/path")))

        await settings.write("plugins/folder", await symbols.get("<plugin_folder>"))
        await settings.write("plugins/path", await symbols.get("<plugin_config>"))
        await settings.write("plugins/content", await settings.settings.get_from_file(await settings.get("plugins/path")))

        for plg in await settings.get("plugins/content/plugins"):
            await settings.enable(f"plugins/content/plugins/{plg}/enabled")
            await settings.save("plugins/path", "plugins/content")

        for obj in await settings.get("objects/content/objects"):
            await settings.enable(f"objects/content/objects/{obj}/enabled")
            await settings.save("objects/path", "objects/content")

        """
        for obj in await settings.get("objects/content/objects"):
            if await settings.get(f"objects/content/objects/{obj}/enabled") == True:
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(obj, "object", unique_object_id)
                await loader.write(f"loader/{obj}/{unique_object_id}/enabled", True)

        for plg in await settings.get("plugins/content/plugins"):
            if await settings.get(f"plugins/content/plugins/{plg}/enabled") == True:
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(plg, "plugin", unique_object_id)
                await loader.write(f"loader/{plg}/{unique_object_id}/enabled", True)
        """

        moment = Moment()
        await moment.init(variables)
        await moment.create("time")
        await moment.write("time/value1", 0)
        await self.data["spaces"].write(f"{space_name}/modules/moment", moment)

        scheduler = Scheduler()
        await scheduler.init(variables, console = console)
        await scheduler.create("classic_task")
        await scheduler.create("complex_task")
        await scheduler.settings("classic_task/mode", "classic")
        await scheduler.settings("classic_task/model", "")
        await scheduler.settings("complex_task/mode", "complex")
        await self.data["spaces"].write(f"{space_name}/modules/scheduler", scheduler)

        await self.space_open_function(space_name)

    async def space_open_function(self, space_name):
        done = False
        possibilities = [0, 1, 2, 3, 4, 5, 6]

        while not done:
            print(f"current space : {space_name}")
            print("0 : objects")
            print("1 : settings")
            print("2 : moment")
            print("3 : tasks")
            print("4 : console")
            print("5 : representation")
            print("6 : exit")

            choice = await ainput("your choice : ")
            if choice.isdigit():
                choice = int(choice)
                if choice in possibilities:
                    done = True

        if choice == 0:
            await self.space_objects_function(space_name)

        elif choice == 1:
            pass

        elif choice == 2:
            pass

        elif choice == 3:
            pass

        elif choice == 4:
            pass

        elif choice == 5:
            pass

        elif choice == 6:
            pass

    async def space_objects_function(self, space_name):
        print("current objects :")
        for obj in await self.data["spaces"].get(f"{space_name}/objects"):
            print(obj)

        print("add objects :")

        settings = await self.data["spaces"].get(f"{space_name}/modules/settings")

        for obj in await self.data["path_utils"].ls(await self.data["path_utils"].get("objects"), mode = 1):
            print(obj)

        print("add plugins :")

        for plg in await self.data["path_utils"].ls(await self.data["path_utils"].get("plugins"), mode = 1):
            print(plg)

        obj = await ainput("object name : ")
        unique_id = await ainput("unique id : ")