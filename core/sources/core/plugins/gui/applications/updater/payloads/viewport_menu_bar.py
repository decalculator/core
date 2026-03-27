from core.plugins.gui.applications.updater.updater import updater_callback

with dpg.menu(label = "updater"):
    dpg.add_menu_item(label = "open", callback = updater_callback, user_data = [self.loop, self.scheduler, self.device, self.languages, self.pid_manager, self.settings, self.filesystem, self.gui, self])