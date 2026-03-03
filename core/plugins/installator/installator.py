import asyncio
import os
from zipfile import ZipFile

from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *
from core.modules.filesystem.filesystem import *
from core.plugins.communication.communication import *

class Installator:
    def __init__(self):
        self.installator = None
        self.filesystem = None
        self.path = None

    async def init(self, variables):
        self.variables = variables
        await self.variables.create("installator")
        obj = Variable()
        await obj.init(self)
        await self.variables.write("installator/object", obj)

        self.installator = Json()
        await self.installator.init()

        self.path = Path()
        await self.path.init()

        self.filesystem = Filesystem()
        await self.filesystem.init()

    async def install(self, args):
        mode = args[0]

        # mode 0 : en ligne
        # mode 1 : local

        object_type = args[1]
        number = args[2]
        path = args[3]

        if mode == 0:
            communication = Communication()
            await communication.init()
            await communication.assign(path)
            await communication.get(1)

            if await communication.exists("response/content"):
                path1 = "core/data/communication/temp/0.zip"
                path2 = "core/data/communication/temp/0"
                
                if object_type == 0:
                    path3 = "core/modules/core/scripting"
                    common_config_path = f"{path3}/modules.json"
                elif object_type == 1:
                    path3 = "core/plugins"
                    common_config_path = f"{path3}/plugins.json"
                elif object_type == 2:
                    path3 = "core/objects"
                    common_config_path = f"{path3}/objects.json"

                with open(path1, "wb") as file:
                    file.write(await communication.get_json("response/content"))

                with ZipFile(path1, "r") as obj:
                    obj.extractall(path2)

                ls = await self.path.ls(path2)
                object_path = f"{path2}/{ls[0]}"

                if "config.json" in await self.path.ls(object_path):
                    config_path = f"{object_path}/config.json"
                    content = self.filesystem.read_file(config_path, 2)

                    if "path" in content:
                        if "name" in content:
                            await self.filesystem.mv(f"{object_path}/{content['path']}", f"{path3}/{content['name']}")

                            common_config = await self.filesystem.read_file(common_config_path, 2)

                            if object_type == 0:
                                common_config["modules"][object_name] = {"enabled": True}
                            elif object_type == 1:
                                common_config["plugins"][object_name] = {"enabled": True}
                            elif object_type == 2:
                                common_config["objects"][object_name] = {"enabled": True}

                            await self.filesystem.write_to_file(common_config_path, json.dumps(common_config))

                os.remove(path1)
        elif mode == 1:
            path1 = "core/data/communication/temp/0"

            if object_type == 0:
                path2 = "core/modules/core/scripting"
                common_config_path = f"{path2}/modules.json"
            elif object_type == 1:
                path2 = "core/plugins"
                common_config_path = f"{path2}/plugins.json"
            elif object_type == 2:
                path2 = "core/objects"
                common_config_path = f"{path2}/objects.json"

            with ZipFile(path, "r") as obj:
                obj.extractall(path1)

            ls = await self.path.ls(path1)
            object_path = f"{path1}/{ls[0]}"

            if "config.json" in await self.path.ls(object_path):
                config_path = f"{object_path}/config.json"
                content = await self.filesystem.read_file(config_path, 2)

                if "path" in content:
                    if "name" in content:
                        object_name = content["name"]

                        await self.filesystem.mv(f"{object_path}/{content['path']}", f"{path2}/{object_name}")

                        common_config = await self.filesystem.read_file(common_config_path, 2)

                        if object_type == 0:
                            common_config["modules"][object_name] = {"enabled": True}
                        elif object_type == 1:
                            common_config["plugins"][object_name] = {"enabled": True}
                        elif object_type == 2:
                            common_config["objects"][object_name] = {"enabled": True}

                        await self.filesystem.write_to_file(common_config_path, json.dumps(common_config))