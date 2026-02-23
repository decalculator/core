import asyncio
import ast
import re
import dearpygui.dearpygui as dpg

from core.modules.core.scripting.loader.loader import *
from core.modules.core.scripting.states.states import *
from core.modules.core.scripting.symbols.symbols import *
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.settings.settings import *
from core.modules.core.scripting.moment.moment import *
from core.modules.core.scripting.scheduler.scheduler import *
from core.modules.core.scripting.identifier.identifier import *
from core.modules.core.scripting.variable.variable import *
from core.modules.core.scripting.variables.variables import *
from core.modules.core.scripting.memory.memory import *
from core.modules.core.scripting.console.console import *

from core.plugins.spaces.spaces import *
from core.plugins.representation.representation import *

class Ui:
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

        """
        loader = Loader()
        await loader.init(self.data["variables"], "core/modules", "core/plugins", "core/objects")
        self.data["loader"] = loader

        for obj in await self.data["settings"].get("objects/content/objects"):
            if await self.data["settings"].get(f"objects/content/objects/{obj}/enabled") == True:
                unique_object_id = await self.data["identifier"].generate_id("objects_id")
                await self.data["loader"].load(obj, "object", unique_object_id)
                await self.data["loader"].write(f"loader/{obj}/{unique_object_id}/enabled", True)

        for plg in await self.data["settings"].get("plugins/content/plugins"):
            if await self.data["settings"].get(f"plugins/content/plugins/{plg}/enabled") == True:
                unique_object_id = await self.data["identifier"].generate_id("objects_id")
                await self.data["loader"].load(plg, "plugin", unique_object_id)
                await self.data["loader"].write(f"loader/{plg}/{unique_object_id}/enabled", True)
        """

        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("core/plugins/ui/font/ClarityCity-Light.ttf", 18)

        #with dpg.window(label = "core", tag = "core_windows"):
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

            dpg.add_menu_item(label = "exit", callback = self.exit_callback)

        dpg.create_viewport(title = "core", width = 2560, height = 1440)

        # dpg.create_viewport(title = "core", width = 2560, height = 1440)
        # dpg.set_primary_window("core_windows", True)

        dpg.setup_dearpygui()
        dpg.show_viewport()

        """
        count = 0
        while dpg.is_dearpygui_running() and self.data["on"]:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

            if count - 100 == 0:
                if await self.data["loader"].get(f"loader/ui/{self.data["unique_object_id"]}/enabled") == True:
                    count = 0
                else:
                    self.data["on"] = False

            count += 1
        """

        while dpg.is_dearpygui_running():
            #dpg.configure_item("test", label = value)

            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

        dpg.destroy_context()

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

                            dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(f"loader/ui/{self.data["unique_object_id"]}/enabled"), tag = f"checkbox_{obj}:{unique_id}")
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

                            dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = user_data, default_value = await self.data["loader"].get(f"loader/ui/{self.data["unique_object_id"]}/enabled"), tag = f"checkbox_{obj}:{unique_id}")
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
            scheduler = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/scheduler")
            loader = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/loader")

        dpg.delete_item(f"remove_{obj}:{unique_id}")
        dpg.delete_item(f"checkbox_{obj}:{unique_id}")

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
            dpg.delete_item(f"{obj}_text")
            del self.data["view"]["items"][obj]

            await loader.loader.remove(f"loader/{obj}")

            if await scheduler.exists(f"classic_task/{obj}"):
                await scheduler.remove(f"classic_task/{obj}")

            if await scheduler.exists(f"complex_task/running/{obj}"):
                await scheduler.remove(f"complex_task/running/{obj}")

            if await scheduler.exists(f"complex_task/to_run/{obj}"):
                await scheduler.remove(f"complex_task/to_run/{obj}")

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
            scheduler = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/scheduler")

        if value == True:
            await scheduler.enable(obj, unique_id)
        else:
            await scheduler.disable(obj, unique_id)

    async def exit_function(self):
        self.data["on"] = False

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
            console = await self.data["spaces"].get(f"{space_name}/modules/{space_name}/console")

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

        dpg.delete_item("create_space_window")
        #dpg.hide_item("create_space_window")
        #dpg.show_item("create_space_window")

        self.data["loop"].create_task(self.space_creation_function(space_name))

    def space_creation_specific_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_creation_specific_function(user_data))

    async def space_creation_specific_function(self, args):
        self.data["loop"].create_task(self.space_creation_function(args[0]))

    async def space_creation_function(self, space_name):
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

        states = States()
        await states.init()
        await self.data["spaces"].write(f"{space_name}/modules/states", states)

        identifier = Identifier()
        await identifier.init(variables, console = console)
        await identifier.create("objects_id")
        await self.data["spaces"].write(f"{space_name}/modules/identifier", identifier)

        representation = Representation()
        await representation.init(variables)
        await representation.create("objects")
        await self.data["spaces"].write(f"{space_name}/modules/representation", representation)

        dimension_x = 500
        dimension_y = 500

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
            ]
        })

        if not dpg.does_item_exist(f"{space_name}_representation_texture_tag"):
            with dpg.texture_registry():
                # dpg.add_static_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                # dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = default, tag = f"{space_name}_representation_texture_tag")

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

    async def space_open_function(self, name):
        moment = await self.data["spaces"].get(f"{name}/modules/moment")

        with dpg.window(label = name, on_close = self.on_close_callback):
            with dpg.menu_bar():
                dpg.add_menu_item(label = "objects", callback = self.space_objects_callback, user_data = name)
                dpg.add_menu_item(label = "settings", callback = self.space_settings_callback, user_data = name)
                with dpg.menu(label = "moment"):
                    dpg.add_menu_item(label = "next", callback = self.space_change_moment_callback, user_data = [name, 1, 0])
                    dpg.add_menu_item(label = "previous", callback = self.space_change_moment_callback, user_data = [name, -1, 0])
                dpg.add_menu_item(label = "tasks", callback = self.tasks_callback, user_data = [1, name])
                with dpg.menu(label = "console"):
                    dpg.add_menu_item(label = "open", callback = self.console_callback, user_data = [1, name])
                with dpg.menu(label = "representation"):
                    dpg.add_menu_item(label = "open", callback = self.space_representation_visualisation_callback, user_data = [name, 0])

    def space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_representation_visualisation_function(user_data))

    async def space_representation_visualisation_function(self, args):
        space_name = args[0]
        mode = args[1]

        representation = await self.data["spaces"].get(f"{space_name}/modules/representation")
        objects = await representation.get("objects")

        core_dimension_x = objects["core"]["dimensions"][0]
        core_dimension_y = objects["core"]["dimensions"][1]

        color_size = 4
        texture_data = dpg.get_value(f"{space_name}_representation_texture_tag")

        for object_name, object_data in objects.items():
            dimension_x = object_data["dimensions"][0]
            dimension_y = object_data["dimensions"][1]
            position_x = object_data["position"][0]
            position_y = object_data["position"][1]
            color = object_data["color"]

            for y in range(dimension_y):
                for x in range(dimension_x):
                    tex_x = position_x + x
                    tex_y = position_y + y

                    index = (tex_y * core_dimension_x + tex_x) * color_size

                    for c in range(color_size):
                        texture_data[index + c] = color[c]

        dpg.set_value(f"{space_name}_representation_texture_tag", texture_data)

        if mode == 0:
            with dpg.window(label = f"representation : {space_name}", tag = f"{space_name}_space_representation_window", on_close = self.on_close_callback):
                dpg.add_image(f"{space_name}_representation_texture_tag")
                with dpg.group(horizontal = True):
                    dpg.add_button(label = "refresh", callback = self.refresh_space_representation_visualisation_callback, user_data = [space_name, 1])
                    dpg.add_button(label = "<--", callback = self.space_change_moment_callback, user_data = [space_name, -1, 1])
                    dpg.add_button(label = "-->", callback = self.space_change_moment_callback, user_data = [space_name, 1, 1])
        elif mode == 1:
            dpg.set_value(f"{space_name}_space_representation_window", f"{space_name}_representation_texture_tag")

    def refresh_space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_representation_visualisation_function(user_data))

    def space_change_moment_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_change_moment_function(user_data))

    async def space_change_moment_function(self, args):
        space_name = args[0]
        value = args[1]
        mode = args[2]

        moment = await self.data["spaces"].get(f"{space_name}/modules/moment")
        loader = await self.data["spaces"].get(f"{space_name}/modules/loader")
        scheduler = await self.data["spaces"].get(f"{space_name}/modules/scheduler")

        await moment.write("time/value1", await moment.get("time/value1") + value)

        print(f"moment {await moment.get("time/value1")} :")

        for obj_name in await loader.get("loader"):
            objects = await loader.get(f"loader/{obj_name}/objects")

            for unique_object_id, value in objects.items():
                if await loader.get(f"loader/{obj_name}/{unique_object_id}/enabled") == True:
                    temp_objs = await loader.get(f"loader/{obj_name}/objects/{unique_object_id}/object/objects")
                    if temp_objs[0].object_type == "classic":
                        if not await scheduler.exists(f"classic_task/{obj_name}"):
                            await scheduler.write(f"classic_task/{obj_name}", {})
                        await scheduler.write(f"classic_task/{obj_name}/{unique_object_id}", value)
                    elif temp_objs[0].object_type == "complex":
                        if not await scheduler.exists(f"complex_task/to_run/{obj_name}"):
                            await scheduler.write(f"complex_task/to_run/{obj_name}", {})

                        if not await scheduler.exists(f"complex_task/running/{obj_name}/{unique_object_id}"):
                            await scheduler.write(f"complex_task/to_run/{obj_name}/{unique_object_id}", temp_objs)

                        if not await scheduler.exists(f"complex_task/running/{obj_name}"):
                            await scheduler.write(f"complex_task/running/{obj_name}", {})

                        if not await scheduler.exists(f"complex_task/running/{obj_name}/{unique_object_id}"):
                            await scheduler.write(f"complex_task/running/{obj_name}/{unique_object_id}", True)
                else:
                    if await scheduler.exists(f"classic_task/{obj_name}/{unique_object_id}"):
                        await scheduler.write(f"classic_task/{obj_name}/{unique_object_id}", {})

        await scheduler.run("complex_task/to_run")
        await scheduler.write("complex_task/to_run", {})

        await scheduler.run("classic_task")

        print("=" * 50)

        if mode == 1:
            await self.space_representation_visualisation_function([space_name, 1])

    def space_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_objects_function(user_data))

    async def space_objects_function(self, space_name):
        with dpg.window(label = "objects", on_close = self.on_close_callback, tag = "space_objects_window"):
            dpg.add_text("current objects :")
            for obj in await self.data["spaces"].get(f"{space_name}/objects"):
                dpg.add_text(obj)
            dpg.add_button(label = "add objects", callback = self.space_add_objects_callback, user_data = space_name)

    def space_add_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_add_objects_function(user_data))

    async def space_add_objects_function(self, space_name):
        settings = await self.data["spaces"].get(f"{space_name}/modules/settings")

        with dpg.window(label = "add objects", on_close = self.on_close_callback, tag = "space_add_objects_window"):
            dpg.add_text("objects :")

            for obj in await settings.get("objects/content/objects"):
                with dpg.group(horizontal = True):
                    dpg.add_text(obj)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{obj}_amount_input")

            dpg.add_text("plugins :")

            for plg in await settings.get("plugins/content/plugins"):
                with dpg.group(horizontal = True):
                    dpg.add_text(plg)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{plg}_amount_input")

            dpg.add_button(label = "save", callback = self.space_save_objects_callback, user_data = [space_name])

    def space_save_objects_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_save_objects_function(user_data))

    async def space_save_objects_function(self, args):
        space_name = args[0]

        settings = await self.data["spaces"].get(f"{space_name}/modules/settings")
        loader = await self.data["spaces"].get(f"{space_name}/modules/loader")
        identifier = await self.data["spaces"].get(f"{space_name}/modules/identifier")

        for obj in await settings.get("objects/content/objects"):
            amount = dpg.get_value(f"{obj}_amount_input")
            for _ in range(amount):
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(obj, "object", unique_object_id)
                await loader.write(f"loader/{obj}/{unique_object_id}/enabled", True)

        for plg in await settings.get("plugins/content/plugins"):
            amount = dpg.get_value(f"{plg}_amount_input")
            for _ in range(amount):
                unique_object_id = await identifier.generate_id("objects_id")
                await loader.load(plg, "plugin", unique_object_id)
                await loader.write(f"loader/{plg}/{unique_object_id}/enabled", True)

        dpg.delete_item("space_add_objects_window")

    def space_settings_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_settings_function(user_data))

    async def space_settings_function(self, name):
        with dpg.window(label = "settings", tag = "space_settings_window", on_close = self.on_close_callback):
            dpg.add_input_text(multiline = True, default_value = await self.data["spaces"].get(name), tag = "space_settings_raw")
            dpg.add_button(label = "save", callback = self.space_config_save_callback, user_data = name)

    def space_config_save_callback(self, sender, app_data, user_data):
        self.data["loop"].create_task(self.space_config_save_function(user_data))

    async def space_config_save_function(self, name):
        data = dpg.get_value("space_settings_raw")
        await self.data["spaces"].write(name, ast.literal_eval(data))
        dpg.delete_item("space_settings_window")

    def on_close_callback(self, sender):
        self.data["loop"].create_task(self.on_close_function(sender))

    async def on_close_function(self, sender):
        dpg.delete_item(sender)

async def entry(**kwargs):
    print("ui::entry > exec !")

    variables = None
    unique_object_id = None

    if "variables" in kwargs:
        variables = kwargs["variables"]

    if "unique_object_id" in kwargs:
        unique_object_id = kwargs["unique_object_id"]

    ui = Ui()
    await ui.init(variables, unique_object_id)