from __future__ import annotations

import asyncio
import re
import dearpygui.dearpygui as dpg
from PIL import Image

from core.modules.path.path import *
from core.modules.json.json import *
from core.modules.memory.memory import *
from core.modules.dynamic_value.dynamic_value import *
from core.modules.settings.settings import *
from core.modules.scheduler.scheduler import *
from core.modules.loader.loader import *

from core.plugins.math.math import *
from core.plugins.representation.representation import *
from core.plugins.spaces.spaces import *
from core.plugins.moment.moment import *

from core.modules.logs.logs import *
from core.modules.pid_manager.pid_manager import *
from core.modules.filesystem.filesystem import *
from core.modules.languages.languages import *
from core.modules.template.template import *

from core.plugins.device.device import *

from core.plugins.gui.applications.console.console import console_callback
from core.plugins.gui.applications.tasks_manager.tasks_manager import tasks_callback
from core.plugins.gui.applications.updater.updater import updater_callback
from core.plugins.gui.applications.spaces.applications.checkpoints.checkpoints import checkpoints_callback

class Spaces_app:
    def __init__(self, uuid: int):
        self.data = Json()
        self.data.write(Path("settings/tags/window"), uuid, mode = 1)
        self.var = {"view": {"items": {}, "items1": {"obj": {}, "plg": {}}}}

        self.loop = None
        self.width = None
        self.height = None
        self.languages = None
        self.filesystem = None
        self.spaces = None
        self.gui = None
        self.parent = None

        self.device = None

        self.pid_manager = None
        self.scheduler = None
        self.settings = None

    async def create_space_function(self, args: list):
        loop = args[0]
        mode = args[1]
        device = args[2]
        languages = args[3]
        filesystem = args[4]
        gui = args[5]
        parent = args[6]

        window_tag = self.data.get(Path("settings/tags/window"))
        resolution = device.get(Path("settings/resolution"))
        width = resolution[0]
        height = resolution[1]

        self.loop = loop
        self.width = width
        self.height = height
        self.languages = languages
        self.filesystem = filesystem
        self.gui = gui
        self.parent = parent
        self.device = device

        spaces = Spaces()
        self.spaces = spaces

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/create_space_window"), tag)

        with dpg.window(label = languages.get_from_selected(Path("gui/create_space")), tag = tag, on_close = self.on_close_callback, width = width // 4, height = height // 4):
            tag = dpg.generate_uuid()
            self.data.write(Path("settings/tags/space_name"), tag)

            dpg.add_input_text(label = languages.get_from_selected(Path("gui/space_name")), tag = tag)
            dpg.add_button(label = languages.get_from_selected(Path("gui/create")), callback = self.space_creation_callback)

    async def space_creation_function(self, space_name):
        languages = self.languages
        CONFIGURATION = Path("data/core/configuration.json", mode = 1)

        if not self.data.exists(Path("settings/tags/sub_open_space")):
            tag = dpg.generate_uuid()
            self.data.write(Path("settings/tags/sub_open_space"), tag)

            parent_tag = self.parent.data.get(Path("settings/tags/spaces_menu"))

            with dpg.menu(label = languages.get_from_selected(Path("gui/open")), parent = parent_tag, tag = tag):
                dpg.add_menu_item(label = space_name, callback = self.space_creation_specific_callback, user_data = [space_name])
        else:
            tag = self.data.get(Path("settings/tags/sub_open_space"))
            dpg.add_menu_item(label = space_name, parent = tag, callback = self.space_creation_specific_callback, user_data = [space_name])

        item = "create_space_window"
        if self.data.exists(Path(f"settings/tags/{item}")):
            tag = self.data.get(Path(f"settings/tags/{item}"))
            if dpg.does_item_exist(tag):
                dpg.delete_item(tag)

        #dpg.hide_item("create_space_window")
        #dpg.show_item("create_space_window")

        self.spaces.write(Path(f"{space_name}/objects"), {}, mode = 1)
        self.spaces.write(Path(f"{space_name}/modules"), {})

        pid_manager = PidManager()
        # pid_manager.init(ppid = pid, pid_manager = parent_pid_manager)
        pid_manager.write(Path("uuid"), {"used": {}, "unused": [], "max": 1})
        pid_manager.set_get_pid(unused_path = Path("uuid/unused"), used_path = Path("uuid/used"), maximum_path = Path("uuid/max"))

        core = DynamicValue(0)
        pid_manager_pid = DynamicValue(1)

        data = {
            core.data: {
                "usoi": -1,
                "ppid": -1,
                "cpids": [pid_manager_pid.data]
            },
            pid_manager_pid.data: {
                "usoi": pid_manager.usoi,
                "ppid": core.data
            }
        }

        self.pid_manager = pid_manager

        pid_manager.write(Path("uuid/used"), data)

        memory = Memory(pid_manager = pid_manager, ppid = pid_manager_pid)
        memory.write(Path("proc/instances/objects"), {}, mode = 1)
        memory.write(Path("proc/instances/plugins"), {})
        memory.write(Path("proc/instances/modules"), {})

        logs = Logs(memory = memory, pid_manager = pid_manager, ppid = pid_manager_pid)

        device = Device(memory = memory, pid_manager = pid_manager, ppid = pid_manager_pid)

        width, height = device.get_resolution()
        device.write(Path("settings/resolution"), [width, height], mode = 1)

        filesystem = Filesystem(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

        settings = Settings(memory = memory, pid_manager = pid_manager, logs = logs, content = await filesystem.read(CONFIGURATION, mode = 2), ppid = pid_manager_pid)
        settings.resolve(settings.get(Path("variables_pattern")))
        settings.write(Path("objects/content/objects"), {}, mode = 1)
        settings.write(Path("plugins/content/plugins"), {}, mode = 1)

        self.settings = settings

        path = settings.get(Path("objects_config"))
        content = await filesystem.read(Path(path, mode = 1), mode = 2)
        for obj, val in content.items():
            if "enabled" in val and val["enabled"] == True:
                settings.write(Path(f"objects/content/objects/{obj}"), {})

        path = settings.get(Path("plugins_config"))
        content = await filesystem.read(Path(path, mode = 1), mode = 2)
        for obj, val in content.items():
            if "enabled" in val and val["enabled"] == True:
                settings.write(Path(f"plugins/content/plugins/{obj}"), {})

        self.spaces.write(Path(f"{space_name}/modules/settings"), settings)

        languages = Languages()
        await languages.init(filesystem, settings, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        await languages.load_language("english")
        languages.select(Path("english"))

        signals = Template(name = "signals", memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

        loader = Loader(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        loader.write(Path("objects"), {})
        loader.write(Path("plugins"), {})
        loader.write(Path("modules"), {})

        self.spaces.write(Path(f"{space_name}/modules/loader"), loader)

        scheduler = Scheduler(loader, filesystem, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        scheduler.write(Path("scheduling"), {"to_run": {"objects": [], "plugins": [], "modules": []}}, mode = 1)

        self.scheduler = scheduler

        representation = Representation(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        representation.write(Path("objects"), {})
        representation.write(Path("settings/dx"), 0, mode = 1)
        representation.write(Path("settings/dy"), 0)
        representation.write(Path("settings/f"), 10)
        self.spaces.write(Path(f"{space_name}/modules/representation"), representation)

        dimension_x = 1000
        dimension_y = 1000

        default = []
        for i in range(dimension_x * dimension_y):
            for _ in range(4):
                default.append(0)

        representation.write(Path("objects/core"), {
            "dimensions": [
                dimension_x,
                dimension_y
            ],
            "color": [
                1, 1, 1, 1
            ],
            "position": [
                0, 0
            ],
            "render": 2,
            "mode": "pixel",
            "refresh": False,
            "done": False
        })

        item = f"{space_name}_representation_texture_tag"
        if not self.data.exists(Path(f"settings/tags/{item}")):
            with dpg.texture_registry():
                # dpg.add_static_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")
                # dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = texture_data, tag = f"{space_name}_representation_texture_tag")

                tag = dpg.generate_uuid()
                self.data.write(Path(f"settings/tags/{item}"), tag)
                dpg.add_dynamic_texture(width = dimension_x, height = dimension_y, default_value = default, tag = tag)

        self.data.write(Path("settings/variables/objects"), {}, mode = 1)
        app_value = DynamicValue("on")
        self.data.write(Path("settings/variables/app/value"), app_value, mode = 1)

        json = Json()

        content = await self.filesystem.read(Path("data/core/configuration.json", mode = 1), mode = 2)
        json.write(Path("settings"), content)
        self.data.write(Path(f"settings/{space_name}/modules/json"), json, mode = 1)

        moment = Moment(memory = memory, logs = logs, pid_manager = pid_manager, ppid = pid_manager_pid)
        moment.write(Path("time/value1"), 0, mode = 1)
        self.spaces.write(Path(f"{space_name}/modules/moment"), moment)

        await self.space_open_function(space_name)

    async def space_open_function(self, name):
        width = self.width
        height = self.height

        configuration = DynamicValue(await self.filesystem.read(Path("sources/core/plugins/gui/data/gui.json", mode = 1), mode = 2))

        with dpg.window(label = name, on_close = self.on_close_callback, width = width // 1.5, height = height // 1.5):
            """
            from core.plugins.gui.components.menu_bar.menu_bar import MenuBar

            menu_bar = MenuBar()
            uuid = await menu_bar.init(self.loop, pid_manager = self.pid_manager, device = self.device, scheduler = self.scheduler, parent = self, languages = self.languages, configuration = configuration, filesystem = self.filesystem, settings = self.settings)
            await menu_bar.menu_bar()
            """

            with dpg.menu_bar():
                dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/objects")), callback = self.space_objects_callback, user_data = name)
                dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/settings")), callback = self.space_settings_callback, user_data = name)

                with dpg.menu(label = self.languages.get_from_selected(Path("gui/moment"))):
                    dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/next")), callback = self.space_change_moment_callback, user_data = [name, 1, 0, -1])
                    dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/previous")), callback = self.space_change_moment_callback, user_data = [name, -1, 0, -1])

                dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/tasks")), callback = tasks_callback, user_data = [self.loop, 1, self.scheduler, self.device, self.languages, self.pid_manager, name])

                with dpg.menu(label = self.languages.get_from_selected(Path("gui/console"))):
                    dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/console")), callback = console_callback, user_data = [self.loop, 1, self.device, self.languages, self.filesystem, self.gui, self])

                with dpg.menu(label = self.languages.get_from_selected(Path("gui/representation"))):
                    with dpg.menu(label = self.languages.get_from_selected(Path("gui/1d"))):
                        dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/open")), callback = self.space_representation_visualisation_callback, user_data = [name, 0])

                    with dpg.menu(label = self.languages.get_from_selected(Path("gui/3d"))):
                        dpg.add_menu_item(label = self.languages.get_from_selected(Path("gui/open")))

                dpg.add_menu_item(label = "checkpoints", callback = checkpoints_callback, user_data = [self.loop])

    def space_representation_visualisation_function(self, args):
        space_name = args[0]
        mode = args[1]

        representation = self.spaces.get(Path(f"{space_name}/modules/representation"))
        objects = representation.get(Path("objects"))

        core_dimension_x = objects["core"]["dimensions"][0]
        core_dimension_y = objects["core"]["dimensions"][1]

        tag = self.data.get(Path(f"settings/tags/{space_name}_representation_texture_tag"))
        texture_data = dpg.get_value(tag)

        f = representation.get(Path("settings/f"))
        dx = representation.get(Path("settings/dx"))
        dy = representation.get(Path("settings/dy"))

        if representation.exists(Path("settings/_f")):
            _f = representation.get(Path("settings/_f"))
        else:
            _f = f

        if representation.exists(Path("settings/_dx")):
            _dx = representation.get(Path("settings/_dx"))
        else:
            _dx = dx

        if representation.exists(Path("settings/_dy")):
            _dy = representation.get(Path("settings/_dy"))
        else:
            _dy = dy

        for object_name, object_data in objects.items():
            if object_data["done"] == False:
                render_mode = object_data["mode"]
                render_dimensions = object_data["render"]

                # il faut maintenant ajouter un moyen pour supprimer les anciens pixels avant la prochaine frame

                if render_mode == "image" and render_dimensions == 2:
                    path = object_data["path"]
                    position_x = object_data["position"][0]
                    position_y = object_data["position"][1]

                    image = Image.open(path).convert("RGBA")

                    if "dimension" in object_data:
                        dimension_x = object_data["dimension"][0]
                        dimension_y = object_data["dimension"][1]
                    else:
                        dimension_x, dimension_y = image.size

                    dpg_image = []
                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            pixel = image.getpixel((x, y))
                            dpg_image.append(pixel[0] / 255)
                            dpg_image.append(pixel[1] / 255)
                            dpg_image.append(pixel[2] / 255)
                            dpg_image.append(255 / 255)

                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            tex_x = position_x + x
                            tex_y = position_y + y

                            global_index = (tex_y * core_dimension_x + tex_x) * 4
                            local_index = (y * dimension_x + x) * 4

                            for c in range(4):
                                texture_data[global_index + c] = dpg_image[local_index + c]

                elif render_mode == "pixel" and render_dimensions == 2:
                    dimension_x = object_data["dimensions"][0]
                    dimension_y = object_data["dimensions"][1]
                    position_x = object_data["position"][0]
                    position_y = object_data["position"][1]
                    color = object_data["color"]
                    color_size = len(color)

                    for y in range(dimension_y):
                        for x in range(dimension_x):
                            tex_x = position_x + x
                            tex_y = position_y + y

                            index = (tex_y * core_dimension_x + tex_x) * color_size

                            for c in range(color_size):
                                texture_data[index + c] = color[c]

                elif render_mode == "object" and render_dimensions == 3:
                    points = object_data["points"]
                    center = [core_dimension_x // 2, core_dimension_y // 2]
                    color = [0, 0, 0, 0]
                    color_size = len(color)

                    two_dim_points = []
                    for point in points:
                        x = point[0]
                        y = point[1]
                        z = point[2]

                        if z != 0:
                            position_x = round(((x - _dx) * _f) / z)
                            position_y = round(((y - _dy) * _f) / z)

                            tex_x = position_x + center[0]
                            tex_y = position_y + center[1]

                            two_dim_points.append([tex_x, tex_y])

                    for i in range(0, len(two_dim_points), 2):
                        point1 = two_dim_points[i]
                        point2 = two_dim_points[i + 1]

                        if point1 != point2:
                            _points = bresenham(point1[0], point1[1], point2[0], point2[1])
                            for point in _points:
                                index = (point[1] * core_dimension_x + point[0]) * color_size
                                for c in range(color_size):
                                    texture_data[index + c] = 1.0

                    two_dim_points = []
                    for point in points:
                        x = point[0]
                        y = point[1]
                        z = point[2]

                        if z != 0:
                            position_x = round(((x - dx) * f) / z)
                            position_y = round(((y - dy) * f) / z)

                            tex_x = position_x + center[0]
                            tex_y = position_y + center[1]

                            two_dim_points.append([tex_x, tex_y])

                    for i in range(0, len(two_dim_points), 2):
                        point1 = two_dim_points[i]
                        point2 = two_dim_points[i + 1]

                        if point1 != point2:
                            points = bresenham(point1[0], point1[1], point2[0], point2[1])
                            for point in points:
                                index = (point[1] * core_dimension_x + point[0]) * color_size
                                for c in range(color_size):
                                    texture_data[index + c] = color[c]
                        else:
                            index = (point1[1] * core_dimension_x + point1[0]) * color_size
                            for c in range(color_size):
                                texture_data[index + c] = color[c]

                if object_data["refresh"] == False:
                    object_data["done"] = True

        img_tag = self.data.get(Path(f"settings/tags/{space_name}_representation_texture_tag"))
        dpg.set_value(img_tag, texture_data)

        if mode == 0:
            languages = self.languages

            tag = dpg.generate_uuid()
            self.data.write(Path(f"settings/tags/{space_name}_space_representation_window"), tag)

            with dpg.window(label = f"{languages.get_from_selected(Path("gui/representation"))} : {space_name}", tag = tag, on_close = self.on_close_callback):
                dpg.add_image(img_tag)
                with dpg.group(horizontal = True):
                    dpg.add_button(label = languages.get_from_selected(Path("gui/key_left")), callback = self.space_change_moment_callback, user_data = [space_name, -1, 0, 0])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/key_right")), callback = self.space_change_moment_callback, user_data = [space_name, 1, 0, 0])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/refresh")), callback = self.refresh_space_representation_visualisation_callback, user_data = [space_name, 1])
                with dpg.group(horizontal = True):
                    dpg.add_button(label = languages.get_from_selected(Path("gui/up")), callback = self.space_change_moment_callback, user_data = [space_name, 1, 1, 2])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/down")), callback = self.space_change_moment_callback, user_data = [space_name, -1, 1, 2])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/left")), callback = self.space_change_moment_callback, user_data = [space_name, -1, 1, 1])
                    dpg.add_button(label = languages.get_from_selected(Path("gui/right")), callback = self.space_change_moment_callback, user_data = [space_name, 1, 1, 1])
                with dpg.group(horizontal = True):
                    dpg.add_slider_int(min_value = 0, max_value = 20, default_value = f, callback = self.zoom_slider_callback, user_data = space_name)
        elif mode == 1:
            # dpg.set_value(tag, img_tag) ?
            # dpg.set_value(tag, dpg.get_value(img_tag)) ?
            pass

    async def space_change_moment_function(self, args):
        space_name = args[0]
        value = args[1]
        mode = args[2]
        mode1 = args[3]

        representation = self.spaces.get(Path(f"{space_name}/modules/representation"))
        # console = self.spaces.get(Path(f"{space_name}/modules/console"))
        languages = self.languages

        if mode == 0:
            moment = self.spaces.get(Path(f"{space_name}/modules/moment"))
            loader = self.spaces.get(Path(f"{space_name}/modules/loader"))

            representation.write(Path("settings/dx"), representation.get(Path("settings/dx")) + value)
            # representation.write("settings/dy", representation.get("settings/dy") + value)

            moment.write(Path("time/value1"), moment.get(Path("time/value1")) + value)

            # console._print(f"{languages.get_from_selected(Path("gui/moment"))} {moment.get(Path("time/value1"))} ({languages.get_from_selected(Path("gui/start"))})", obj = "moment")

            #

            self.scheduler.run(path = Path("scheduling"), mode = 0)

            #

            # console._print(f"{languages.get_from_selected(Path("gui/moment"))} {moment.get(Path("time/value1"))} ({languages.get_from_selected(Path("gui/end"))})", obj = "moment")

        elif mode1 == 1:
            dx = representation.get(Path("settings/dx"))
            representation.write(Path("settings/_dx"), dx)
            representation.write(Path("settings/dx"), dx + value)

        elif mode1 == 2:
            dy = representation.get(Path("settings/dy"))
            representation.write(Path("settings/_dy"), dy)
            representation.write(Path("settings/dy"), dy + value)

        if mode1 != -1:
            self.space_representation_visualisation_function([space_name, 1])

    def space_objects_function(self, space_name):
        width = self.width
        height = self.height
        languages = self.languages

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/space_objects_window"), tag)

        with dpg.window(label = languages.get_from_selected(Path("gui/objects")), on_close = self.on_close_callback, tag = tag, width = width // 3, height = height // 3):
            dpg.add_text(f"{languages.get_from_selected(Path("gui/current_objects"))} :")
            for obj in self.spaces.get(Path(f"{space_name}/objects")):
                dpg.add_text(obj)
            dpg.add_button(label = "add objects", callback = self.space_add_objects_callback, user_data = space_name)

    def space_add_objects_function(self, space_name):
        settings = self.spaces.get(Path(f"{space_name}/modules/settings"))

        width = self.width
        height = self.height
        languages = self.languages

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/space_add_objects_window"), tag)

        with dpg.window(label = languages.get_from_selected(Path("gui/add_objects")), on_close = self.on_close_callback, tag = tag, width = width // 3, height = height // 3):
            dpg.add_text(languages.get_from_selected(Path("entry_objects_name")))

            self.var["view"]["items1"]["obj"] = {}
            self.var["view"]["items1"]["plg"] = {}

            # for obj in self.gui.data["path_utils"].ls(self.gui.data["path_utils"].get("objects"), mode = 1):
                # self.gui.data["view"]["items1"]["obj"][obj] = {}

            # for plg in self.gui.data["path_utils"].ls(self.gui.data["path_utils"].get("plugins"), mode = 1):
                # self.gui.data["view"]["items1"]["plg"][plg] = {}

            for obj in settings.get(Path("objects/content/objects")):
                self.var["view"]["items1"]["obj"][obj] = {}

            for plg in settings.get(Path("plugins/content/plugins")):
                self.var["view"]["items1"]["plg"][plg] = {}

            for obj in self.var["view"]["items1"]["obj"]:
                with dpg.group(horizontal = True):
                    dpg.add_text(obj)

                    tag = dpg.generate_uuid()
                    self.data.write(Path(f"settings/tags/{obj}_amount_input"), tag)

                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = tag)

            dpg.add_text("plugins :")
            for plg in self.var["view"]["items1"]["plg"]:
                with dpg.group(horizontal = True):
                    dpg.add_text(plg)

                    tag = dpg.generate_uuid()
                    self.data.write(Path(f"settings/tags/{plg}_amount_input"), tag)

                    dpg.add_input_int(default_value = 0, min_value = 0, max_value = 100, step = 1, tag = tag)

            dpg.add_button(label = "save", callback = self.space_save_objects_callback, user_data = [space_name])

    async def space_save_objects_function(self, args):
        space_name = args[0]

        settings = self.spaces.get(Path(f"{space_name}/modules/settings"))
        loader = self.spaces.get(Path(f"{space_name}/modules/loader"))

        obj_config = settings.get(Path("objects_config"))
        plg_config = settings.get(Path("plugins_config"))

        obj_config_content = await self.filesystem.read(Path(obj_config, mode = 1), mode = 2)
        plg_config_content = await self.filesystem.read(Path(plg_config, mode = 1), mode = 2)

        for obj in self.var["view"]["items1"]["obj"]:
            tag = self.data.get(Path(f"settings/tags/{obj}_amount_input"))
            amount = dpg.get_value(tag)

            for _ in range(amount):
                if not loader.exists(Path(f"objects/{obj}/content")):
                    if obj in obj_config_content:
                        obj_config = obj_config_content[obj]

                        if "config_path" in obj_config:
                            config_path = Path(obj_config["config_path"], mode = 1)

                        else:
                            config_path = Path(f"sources/core/objects/{obj}/{obj}.json", mode = 1)

                        content = await self.filesystem.read(config_path, mode = 2)
                        loader.write(Path(f"objects/{obj}/content"), content, mode = 1)

                content_path = Path(f"objects/{obj}/content")
                if loader.exists(content_path):
                    content = loader.get(content_path)
                    usoi = content["usoi"]

                    self.scheduler.add_to_queue(path = Path("scheduling"), object_type = "objects", usoi = obj)

        for plg in self.var["view"]["items1"]["plg"]:
            tag = self.data.get(Path(f"settings/tags/{plg}_amount_input"))
            amount = dpg.get_value(tag)

            for _ in range(amount):
                if not loader.exists(Path(f"plugins/{plg}/content")):
                    if plg in plg_config_content:
                        plg_config = plg_config_content[plg]

                        if "config_path" in plg_config:
                            config_path = Path(plg_config["config_path"], mode = 1)

                        else:
                            config_path = Path(f"sources/core/plugins/{plg}/{plg}.json", mode = 1)

                        content = await self.filesystem.read(config_path, mode = 2)
                        loader.write(Path(f"plugins/{plg}/content"), content, mode = 1)

                content_path = Path(f"plugins/{plg}/content")
                if loader.exists(content_path):
                    content = loader.get(content_path)
                    usoi = content["usoi"]

                    self.scheduler.add_to_queue(path = Path("scheduling"), object_type = "plugins", usoi = plg)

        item = self.data.get(Path("settings/tags/space_add_objects_window"))
        if dpg.does_item_exist(item):
            dpg.delete_item(item)

    def space_settings_function(self, name):
        width = self.width
        height = self.height
        languages = self.languages

        tag = dpg.generate_uuid()
        self.data.write(Path("settings/tags/space_settings_window"), tag)

        with dpg.window(label = languages.get_from_selected(Path("gui/settings")), tag = tag, on_close = self.on_close_callback, width = width // 2, height = height // 2):
            tag = dpg.generate_uuid()
            self.data.write(Path("settings/tags/space_settings_raw"), tag)

            dpg.add_input_text(multiline = True, default_value = self.spaces.get(Path(name)), tag = tag)
            dpg.add_button(label = languages.get_from_selected(Path("gui/save")), callback = self.space_config_save_callback, user_data = name)

    def space_config_save_function(self, name):
        tag = self.data.get(Path("settings/tags/space_settings_raw"))

        data = dpg.get_value(tag)
        self.spaces.write(Path(name), ast.literal_eval(data))

        item = self.data.get(Path("settings/tags/space_settings_window"))
        if dpg.does_item_exist(item):
            dpg.delete_item(item)

    def space_creation_callback(self):
        self.loop.create_task(self.space_creation_function_bridge())

    async def space_creation_function_bridge(self):
        tag = self.data.get(Path("settings/tags/space_name"))
        space_name = dpg.get_value(tag)
        await self.space_creation_function(space_name)

    def space_creation_specific_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_creation_specific_function(user_data))

    async def space_creation_specific_function(self, args):
        self.loop.create_task(self.space_creation_function(args[0]))

    def space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.space_representation_visualisation_function(user_data)

    def refresh_space_representation_visualisation_callback(self, sender, app_data, user_data):
        self.space_representation_visualisation_function(user_data)

    def space_change_moment_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_change_moment_function(user_data))

    def space_objects_callback(self, sender, app_data, user_data):
        self.space_objects_function(user_data)

    def space_add_objects_callback(self, sender, app_data, user_data):
        self.space_add_objects_function(user_data)

    def space_save_objects_callback(self, sender, app_data, user_data):
        self.loop.create_task(self.space_save_objects_function(user_data))

    def space_settings_callback(self, sender, app_data, user_data):
        self.space_settings_function(user_data)

    def space_config_save_callback(self, sender, app_data, user_data):
        self.space_config_save_function(user_data)

    def zoom_slider_callback(self, sender, app_data, user_data):
        self.zoom_slider_function(app_data, user_data)

    def zoom_slider_function(self, args, space_name):
        representation = self.spaces.get(Path(f"{space_name}/modules/representation"))
        f = representation.get(Path("settings/f"))
        representation.write(Path("settings/_f"), f)
        representation.write(Path("settings/f"), args)

        self.space_representation_visualisation_function([space_name, 1])

    def on_close_function(self, sender):
        dpg.delete_item(sender)

    def on_close_callback(self, sender):
        self.on_close_function(sender)

    def write(self, path: Path, value, mode: int = 0) -> bool:
        return self.data.write(path, value, mode = mode)

    def remove(self, path: Path) -> bool:
        return self.data.remove(path)

    def get(self, path: Path):
        return self.data.get(path)

    def exists(self, path: Path):
        return self.data.exists(path)

# callbacks

def create_space_callback(sender, app_data, user_data):
    user_data[0].create_task(create_space_function(user_data))

async def create_space_function(args):
    uuid = dpg.generate_uuid()
    spaces_app = Spaces_app(uuid = uuid)
    await spaces_app.create_space_function(args = args)