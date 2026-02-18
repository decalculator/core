import asyncio
import dearpygui.dearpygui as dpg

class Ui:
    def __init__(self):
        self.loop = None
        self.on = None
        self.variables = None
        self.unique_object_id = None
        self.data = None

    async def init(self, variables, unique_object_id):
        self.loop = asyncio.get_running_loop()
        self.on = True
        self.variables = variables
        self.unique_object_id = unique_object_id
        self.data = {}

        loader_var = await self.variables.get("loader/object")
        self.data["loader"] = loader_var.value

        console_var = await self.variables.get("console/object")
        self.data["console"] = console_var.value

        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("core/plugins/ui/font/ClarityCity-Light.ttf", 18)

        with dpg.window(label = "core", tag = "core_windows"):
            with dpg.group(horizontal = True):
                dpg.add_button(label = "tasks", callback = self.tasks_callback)
                dpg.add_button(label = "spaces", callback = self.spaces_callback)
                dpg.add_button(label = "console", callback = self.console_callback)
                dpg.add_button(label = "settings", callback = self.settings_callback)
                dpg.add_button(label = "exit", callback = self.exit_callback)

            dpg.bind_font(default_font)

        dpg.create_viewport(title = "core", width = 1000, height = 1000)
        dpg.set_primary_window("core_windows", True)
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

    def spaces_callback(self):
        self.loop.create_task(self.spaces_function())

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

        with dpg.window(label = "tasks"):
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

    async def spaces_function(self):
        with dpg.window(label = "spaces"):
            dpg.add_button(label = "create space")
            dpg.add_button(label = "load space")

            dpg.add_text("current space folder : ")

    async def settings_function(self):
        with dpg.window(label = "settings"):
            dpg.add_text("settings")

    async def console_function(self):
        with dpg.window(label = "console"):
            for console_name, value in self.data["console"].console.json.items():
                for message in value:
                    dpg.add_text(f"[{console_name}] {message}")

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