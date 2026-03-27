from core.plugins.gui.applications.spaces.spaces import create_space_callback

tag = dpg.generate_uuid()
self.data.data["settings"]["tags"]["spaces_menu"] = tag

with dpg.menu(label = "spaces", tag = tag):
    dpg.add_menu_item(label = "open", callback = create_space_callback, user_data = [self.loop, 0, self.device, self.languages, self.filesystem, self.gui, self])