import asyncio
import dearpygui.dearpygui as dpg

class Ui:
    def __init__(self):
        self.loop = None
        self.on = True

    async def init(self):
        self.loop = asyncio.get_running_loop()

        dpg.create_context()

        await self.main_window(label = "core")

        dpg.create_viewport(title = "core", width = 600, height = 600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running() and self.on:
            dpg.render_dearpygui_frame()
            await asyncio.sleep(0)

        dpg.destroy_context()

    async def main_window(self, label = None):
        with dpg.window(label = label):
            dpg.add_button(label = "exit", callback = self.exit_callback)

    def exit_callback(self):
        self.loop.create_task(self.exit_function())

    async def exit_function(self):
        self.on = False

async def entry(**kwargs):
    print("ui::entry > exec")

    ui = Ui()
    await ui.init()

asyncio.run(entry())