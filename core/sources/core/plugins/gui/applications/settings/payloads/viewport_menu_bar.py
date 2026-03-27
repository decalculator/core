from core.plugins.gui.applications.settings.settings import settings_callback

with dpg.menu(label = "settings"):
    dpg.add_menu_item(label = "open", callback = settings_callback, user_data = [self.loop, 0, self.device, self.languages])