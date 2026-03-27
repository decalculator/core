from core.plugins.gui.applications.console.console import console_callback

with dpg.menu(label = "console"):
    dpg.add_menu_item(label = "open", callback = console_callback, user_data = [self.loop, 0, self.device, self.languages, self.filesystem, self.gui, self])