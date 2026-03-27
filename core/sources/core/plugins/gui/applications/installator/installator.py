from __future__ import annotations

import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

from core.plugins.temp.temp import *
from core.plugins.communication.communication import *
from core.plugins.installator.installator import *
from core.plugins.repos.repos import *

class Installator_gui:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)

        self.loop = None
        self.width = None
        self.height = None
        self.languages = None
        self.filesystem = None
        self.installator = None
        self.repos = None
        self.communication = None

    def run(self, args: list):
        loop = args[0]
        mode = args[1]
        device = args[2]
        languages = args[3]
        filesystem = args[4]
        settings = args[5]
        repos = args[6]

        self.loop = loop
        self.repos = repos

        temp = Temp(filesystem = filesystem)
        temp.write(Path("id"), {"used": [], "unused": [], "max": 1})
        temp.set_get_id(unused_path = Path("id/unused"), used_path = Path("id/used"), maximum_path = Path("id/max"))

        self.communication = Communication(filesystem = filesystem)

        installator = Installator(temp = temp, communication = self.communication, filesystem = filesystem)

        self.installator = installator

        window_tag = self.data.get(Path("settings/tags/window"))
        resolution = device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        self.width = width
        self.height = height
        self.languages = languages
        self.filesystem = filesystem

        with dpg.window(label = "installator", tag = window_tag, width = width // 3, height = height // 3):
            with dpg.menu_bar():
                with dpg.menu(label = languages.get_from_selected(Path("gui/install"))):
                    with dpg.menu(label = languages.get_from_selected(Path("gui/modules"))):
                        with dpg.menu(label = languages.get_from_selected(Path("gui/local"))):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.local_callback, user_data = [0, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.local_callback, user_data = [0, 1])
                        with dpg.menu(label = "online"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.url_callback, user_data = [0, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.url_callback, user_data = [0, 1])
                    with dpg.menu(label = "plugins"):
                        with dpg.menu(label = "local"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.local_callback, user_data = [1, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.local_callback, user_data = [1, 1])
                        with dpg.menu(label = "online"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.url_callback, user_data = [1, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.url_callback, user_data = [1, 1])
                    with dpg.menu(label = "objects"):
                        with dpg.menu(label = "local"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.local_callback, user_data = [2, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.local_callback, user_data = [2, 1])
                        with dpg.menu(label = "online"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.url_callback, user_data = [2, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.url_callback, user_data = [2, 1])
                    with dpg.menu(label = "repos"):
                        with dpg.menu(label = "local"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.local_callback, user_data = [3, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.local_callback, user_data = [3, 1])
                        with dpg.menu(label = "online"):
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/single")), callback = self.url_callback, user_data = [3, 0])
                            dpg.add_menu_item(label = languages.get_from_selected(Path("gui/pack")), callback = self.url_callback, user_data = [3, 1])

    def local_function(self, args):
        object_type = args[0]
        number = args[1]

        width = self.width
        height = self.height
        languages = self.languages

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/file_dialog"), tag)

        with dpg.file_dialog(directory_selector = False, show = False, callback = self.local_install_callback, tag = tag, width = width // 3, height = height // 3, user_data = [number, object_type]):
            dpg.add_file_extension(".zip", color = (150, 255, 150, 255), custom_text = "[Zip]")

        with dpg.window(label = languages.get_from_selected(Path("gui/local_install")), on_close = self.on_close_callback, width = width // 5, height = height // 5):
            dpg.add_button(label = languages.get_from_selected(Path("gui/select_file")), callback = lambda: dpg.show_item(tag))

    async def local_install_function(self, args):
        data = args[0]
        number = args[1]
        object_type = args[2]
        file_name = data["file_name"]
        file_path = data["file_path_name"]

        file_path_obj = Path(file_path, mode = 1)
        installator = self.installator

        extracted_path = installator.extract_object([object_type, file_path_obj])
        object_name = await installator.get_object_name(extracted_path)
        is_alreay_installed = await installator.is_alreay_installed([object_name, object_type])

        if is_alreay_installed:
            width = self.width
            height = self.height
            languages = self.languages

            tag = dpg.generate_uuid()
            self.data.write(Path("settings/tags/overwrite_object_installation_window"), tag)

            with dpg.window(label = languages.get_from_selected(Path("gui/prompt")), on_close = self.on_close_callback, tag = tag, width = width // 5, height = height // 5):
                dpg.add_text(languages.get_from_selected(Path("gui/overwrite_object")))
                with dpg.group(horizontal = True):
                    dpg.add_button(label = languages.get_from_selected(Path("gui/uninstall_and_install")), callback = self.uninstall_and_install_callback, user_data = [object_name, extracted_path, object_type, 1])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/cancel_installation")), callback = self.cancel_installation_callback)

        else:
            await self.installator.install([1, object_type, number, file_path_obj], extracted_path = extracted_path)

    def uninstall_and_install_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.uninstall_and_install_function(user_data))

    async def uninstall_and_install_function(self, args):
        object_name = args[0]
        extracted_path = args[1]
        object_type = args[2]
        mode = args[3]

        installator = self.installator
        await installator.uninstall([object_name, object_type])
        await installator.install([mode, object_type, 1, extracted_path], extracted_path = extracted_path)

        tag = self.data.get(Path("settings/tags/overwrite_object_installation_window"))
        dpg.delete_item(tag)

    def url_function(self, args):
        width = self.width
        height = self.height
        languages = self.languages

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/url_value"), tag)

        with dpg.window(label = languages.get_from_selected(Path("gui/url")), on_close = self.on_close_callback, width = width // 4, height = height // 4):
            with dpg.group(horizontal = True):
                dpg.add_text(languages.get_from_selected(Path("gui/ask_url")))
                dpg.add_input_text(tag = tag)
                dpg.add_button(label = languages.get_from_selected(Path("gui/install")), callback = self.install_callback, user_data = args)

            dpg.add_button(label = languages.get_from_selected(Path("gui/install_from_repo")), callback = self.install_from_repo_callback, user_data = args)

    async def install_from_repo_function(self, args):
        width = self.width
        height = self.height
        languages = self.languages

        with dpg.window(label = languages.get_from_selected(Path("gui/install_from_repo")), on_close = self.on_close_callback, width = width // 4, height = height // 4):
            repos = self.repos.get(Path("repos"))

            for repo, value in repos.items():
                with dpg.collapsing_header(label = repo):

                    if "url" in value:
                        value = self.communication.get(value["url"])["content"]

                    for object_type, data in value["content"].items():
                        with dpg.collapsing_header(label = languages.get_from_selected(Path(f"gui/{object_type}"))):
                            for obj, val in data.items():
                                with dpg.group(horizontal = True):
                                    dpg.add_text(obj)
                                    dpg.add_button(label = languages.get_from_selected(Path("gui/install")), callback = self.install_object_from_repo_callback, user_data = [obj, val, object_type])

    def install_object_from_repo_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.install_object_from_repo_function(user_data))

    async def install_object_from_repo_function(self, args):
        obj = args[0]
        obj_data = args[1]
        obj_type = args[2]

        # print(obj, obj_data, obj_type)
        # plg2 {'mode': 'online', 'url': 'https://raw.com/cell2.zip', 'type': 'raw_zip'} plugins

        await self.installator.install([0, obj_type, 1, obj_data["url"]])

    async def install_function(self, args):
        object_type = args[0]
        number = args[1]

        tag = self.data.get(Path("settings/tags/url_value"))
        url = dpg.get_value(tag)

        await self.installator.install([0, object_type, number, url])

    def install_from_repo_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.install_from_repo_function(user_data))

    def install_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.install_function(user_data))

    def local_install_callback(self, sender, app_data, user_data):
        user_data.insert(0, app_data)
        self.loop.create_task(self.local_install_function(user_data))

    def cancel_installation_callback(self, sender, app_data, user_data):
        self.cancel_installation_function()

    def cancel_installation_function(self):
        tag = self.data.get(Path("settings/tags/overwrite_object_installation_window"))
        if dpg.does_item_exist(tag):
            dpg.delete_item(tag)

    def local_callback(self, sender, app_data, user_data):
        self.local_function(user_data)

    def url_callback(self, sender, app_data, user_data):
        self.url_function(user_data)

    def on_close_function(self, sender):
        dpg.delete_item(sender)

    def on_close_callback(self, sender):
        self.on_close_function(sender)

# callbacks

def installator_callback(sender, app_data, user_data):
    installator_function(user_data)

def installator_function(args):
    uuid = dpg.generate_uuid()
    installator_app = Installator_gui(uuid = uuid)
    installator_app.run(args = args)