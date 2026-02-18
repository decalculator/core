import asyncio
import dearpygui.dearpygui as dpg

class Ui:
    def __init__(self):
        self.loop = None
        self.on = None
        self.variables = None
        self.unique_object_id = None

    async def init(self, variables, unique_object_id):
        self.loop = asyncio.get_running_loop()
        self.on = True
        self.variables = variables
        self.unique_object_id = unique_object_id

        dpg.create_context()

        await self.main_window(label = "core")

        dpg.create_viewport(title = "core", width = 1000, height = 1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running() and self.on:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

        dpg.destroy_context()

    async def main_window(self, label = None):
        with dpg.window(label = label):
            dpg.add_button(label = "tasks", callback = self.tasks_callback)
            dpg.add_button(label = "spaces", callback = self.exit_callback)
            dpg.add_button(label = "exit", callback = self.exit_callback)

    def tasks_callback(self):
        self.loop.create_task(self.tasks_function())

    def exit_callback(self):
        self.loop.create_task(self.exit_function())

    async def tasks_function(self):
        scheduler_var = await self.variables.get("scheduler/object")
        scheduler_obj = scheduler_var.value

        classic_running = {}
        complex_running = {}

        if await scheduler_obj.exists("classic_task/running"):
            classic_running = await scheduler_obj.get("classic_task/running")

        if await scheduler_obj.exists("complex_task/running"):
            complex_running = await scheduler_obj.get("complex_task/running")

        print(classic_running)
        print(complex_running)

    async def exit_function(self):
        self.on = False

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

asyncio.run(entry())