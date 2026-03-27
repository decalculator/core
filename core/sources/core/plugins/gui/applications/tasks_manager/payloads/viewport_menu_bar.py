from core.plugins.gui.applications.tasks_manager.tasks_manager import tasks_callback

with dpg.menu(label = "tasks"):
    dpg.add_menu_item(label = "open", callback = tasks_callback, user_data = [self.loop, 0, self.scheduler, self.device, self.languages, self.pid_manager])