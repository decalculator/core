import asyncio
import ast
import dearpygui.dearpygui as dpg
from core.plugins.spaces.spaces import *

class Ui:
    def __init__(self):
        self.loop = None
        self.on = None
        self.variables = None
        self.unique_object_id = None
        self.data = None
        self.spaces = None

    async def init(self, variables, unique_object_id):
        self.loop = asyncio.get_running_loop()
        self.on = True
        self.variables = variables
        self.unique_object_id = unique_object_id
        self.data = {}

        spaces = Spaces()
        await spaces.init(self.variables)
        self.spaces = spaces

        loader_var = await self.variables.get("loader/object")
        self.data["loader"] = loader_var.value

        console_var = await self.variables.get("console/object")
        self.data["console"] = console_var.value

        moment_var = await self.variables.get("moment/object")
        self.data["moment"] = moment_var.value

        settings_var = await self.variables.get("settings/object")
        self.data["settings"] = settings_var.value

        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("core/plugins/ui/font/ClarityCity-Light.ttf", 18)

        #with dpg.window(label = "core", tag = "core_windows"):
        dpg.bind_font(default_font)
        with dpg.viewport_menu_bar():
            with dpg.menu(label = "tasks"):
                with dpg.menu(label = "tasks manager"):
                    dpg.add_menu_item(label = "open", callback = self.tasks_callback)

            with dpg.menu(label = "spaces"):
                dpg.add_menu_item(label = "create", callback = self.create_space_callback)
                dpg.add_menu_item(label = "open")

            with dpg.menu(label = "console"):
                dpg.add_menu_item(label = "open", callback = self.console_callback)

            with dpg.menu(label = "settings"):
                dpg.add_menu_item(label = "open", callback = self.settings_callback)

            dpg.add_menu_item(label = "exit", callback = self.exit_callback)

        dpg.create_viewport(title = "core", width = 1000, height = 1000)
        #dpg.set_primary_window("core_windows", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        count = 0
        while dpg.is_dearpygui_running() and self.on:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

            if count - 100 == 0:
                if await self.data["loader"].get(f"loader/ui/{self.unique_object_id}/enabled") == True:
                    count = 0
                else:
                    self.on = False

            count += 1

        dpg.destroy_context()

    def tasks_callback(self):
        self.loop.create_task(self.tasks_function())

    def exit_callback(self):
        self.loop.create_task(self.exit_function())

    def settings_callback(self):
        self.loop.create_task(self.settings_function())

    def console_callback(self):
        self.loop.create_task(self.console_function())

    async def tasks_function(self):
        if not "scheduler" in self.data:
            scheduler_var = await self.variables.get("scheduler/object")
            scheduler_obj = scheduler_var.value
            self.data["scheduler"] = scheduler_obj

        classic_running = {}
        complex_running = {}

        if await self.data["scheduler"].exists("classic_task"):
            temp = await self.data["scheduler"].get("classic_task")

            for obj_name in temp:
                if obj_name not in classic_running:
                    classic_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in classic_running[obj_name]:
                        classic_running[obj_name].append(unique_id)

        if await self.data["scheduler"].exists("complex_task/running"):
            temp = await self.data["scheduler"].get("complex_task/running")

            for obj_name in temp:
                if obj_name not in complex_running:
                    complex_running[obj_name] = []

                for unique_id in temp[obj_name]:
                    if unique_id not in complex_running[obj_name]:
                        complex_running[obj_name].append(unique_id)

        with dpg.window(label = "tasks", on_close = self.on_close_callback):
            for obj, value in classic_running.items():
                if not obj in ["running", "to_run"]:
                    dpg.add_text(obj)
                    for unique_id in value:
                        dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = [obj, unique_id], default_value = await self.data["loader"].get(f"loader/ui/{self.unique_object_id}/enabled"))

            for obj, value in complex_running.items():
                if not obj in ["running", "to_run"]:
                    dpg.add_text(obj)
                    for unique_id in value:
                        dpg.add_checkbox(label = unique_id, callback = self.tasks_checkbox_callback, user_data = [obj, unique_id], default_value = await self.data["loader"].get(f"loader/ui/{self.unique_object_id}/enabled"))

    def tasks_checkbox_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.change_tasks_function(user_data, app_data))

    async def change_tasks_function(self, user_data, value):
        obj = user_data[0]
        unique_id = user_data[1]

        scheduler_obj = self.data["scheduler"]

        if value == True:
            await scheduler_obj.enable(obj, unique_id)
        else:
            await scheduler_obj.disable(obj, unique_id)

    async def exit_function(self):
        self.on = False

    async def settings_function(self):
        with dpg.window(label = "settings", on_close = self.on_close_callback):
            dpg.add_text("settings")

    async def console_function(self):
        with dpg.window(label = "console", on_close = self.on_close_callback):
            for console_name, value in self.data["console"].console.json.items():
                for message in value:
                    dpg.add_text(f"[{console_name}] {message}")

    def create_space_callback(self):
        self.loop.create_task(self.create_space_function())

    async def create_space_function(self):
        with dpg.window(label = "create space", tag = "create_space_window", on_close = self.on_close_callback):
            dpg.add_input_text(label = "space's name", tag = "space_name")
            dpg.add_button(label = "create", callback = self.space_creation_callback)

    def space_creation_callback(self):
        space_name = dpg.get_value("space_name")
        dpg.delete_item("create_space_window")
        #dpg.hide_item("create_space_window")
        #dpg.show_item("create_space_window")

        self.loop.create_task(self.space_creation_function(space_name))

    async def space_creation_function(self, space_name):
        await self.spaces.create(space_name)
        await self.spaces.write(f"{space_name}/objects", {})
        await self.space_open_function(space_name)

    async def space_open_function(self, name):
        with dpg.window(label = name, on_close = self.on_close_callback):
            with dpg.menu_bar():
                dpg.add_menu_item(label = "objects", callback = self.space_objects_callback, user_data = name)
                dpg.add_menu_item(label = "settings", callback = self.space_settings_callback, user_data = name)
                with dpg.menu(label = "moment"):
                    dpg.add_menu_item(label = "next")
                    dpg.add_menu_item(label = "previous")

    def space_objects_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_objects_function(user_data))

    async def space_objects_function(self, space_name):
        with dpg.window(label = "objects", on_close = self.on_close_callback, tag = "space_objects_window"):
            dpg.add_text("current objects :")
            for obj in await self.spaces.get(f"{space_name}/objects"):
                dpg.add_text(obj)
            dpg.add_button(label = "add objects", callback = self.space_add_objects_callback, user_data = space_name)

    def space_add_objects_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_add_objects_function(user_data))

    async def space_add_objects_function(self, space_name):
        with dpg.window(label = "add objects", on_close = self.on_close_callback, tag = "space_add_objects_window"):
            dpg.add_text("objects :")

            with dpg.group(horizontal = True):
                for obj in await self.data["settings"].get("objects/content/objects"):
                    dpg.add_text(obj)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{obj}_amount_input")

            dpg.add_text("plugins :")

            with dpg.group(horizontal = True):
                for plg in await self.data["settings"].get("plugins/content/plugins"):
                    dpg.add_text(plg)
                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = f"{plg}_amount_input")

            dpg.add_button(label = "save", callback = self.space_save_objects_callback)

    def space_save_objects_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_save_objects_function(user_data))

    async def space_save_objects_function(self, space_name):
        for obj in await self.data["settings"].get("objects/content/objects"):
            amount = dpg.get_value(f"{obj}_amount_input")
            if amount != 0:
                print(f"adding {obj} x{amount}")

        for plg in await self.data["settings"].get("plugins/content/plugins"):
            amount = dpg.get_value(f"{plg}_amount_input")
            if amount != 0:
                print(f"adding {plg} x{amount}")

    def space_settings_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_settings_function(user_data))

    async def space_settings_function(self, name):
        with dpg.window(label = "settings", tag = "space_settings_window", on_close = self.on_close_callback):
            dpg.add_input_text(multiline = True, default_value = await self.spaces.get(name), tag = "space_settings_raw")
            dpg.add_button(label = "save", callback = self.space_config_save_callback, user_data = name)

    def space_config_save_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_config_save_function(user_data))

    async def space_config_save_function(self, name):
        data = dpg.get_value("space_settings_raw")
        await self.spaces.write(name, ast.literal_eval(data))
        dpg.delete_item("space_settings_window")

    def on_close_callback(self, sender):
        self.loop.create_task(self.on_close_function(sender))

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