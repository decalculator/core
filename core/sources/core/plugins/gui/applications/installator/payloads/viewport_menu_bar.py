from core.plugins.gui.applications.installator.installator import installator_callback

with dpg.menu(label = "installator"):
    dpg.add_menu_item(label = "open", callback = installator_callback, user_data = [self.loop, 0, self.device, self.languages, self.filesystem, self.settings, self.repos])