import asyncio
import os
from zipfile import ZipFile

from core.modules.json.json import *
from core.modules.variable.variable import *
from core.modules.path.path import *
from core.modules.path_utils.path_utils import *
from core.modules.filesystem.filesystem import *
from core.plugins.communication.communication import *

class Installator:
    def __init__(self):
        self.installator = None
        self.filesystem = None
        self.path_utils = None

    async def init(self, variables):
        self.variables = variables
        await self.variables.create(Path("installator"))
        obj = Variable()
        await obj.init(self)
        await self.variables.write(Path("installator/object"), obj)

        self.installator = Json()
        await self.installator.init()

        self.path_utils = Path_utils()
        await self.path_utils.init()

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

            if await communication.exists(Path("response/content")):
                path1 = Path("core/data/communication/temp/0.zip", mode = 1)
                path2 = Path("core/data/communication/temp/0", mode = 1)
                
                if object_type == 0:
                    path3 = Path("core/modules", mode = 1)
                    common_config_path = Path(f"{path3}/modules.json", mode = 1)
                elif object_type == 1:
                    path3 = Path("core/plugins", mode = 1)
                    common_config_path = Path(f"{path3}/plugins.json", mode = 1)
                elif object_type == 2:
                    path3 = Path("core/objects", mode = 1)
                    common_config_path = Path(f"{path3}/objects.json", mode = 1)
                elif object_type == 3:
                    path3 = Path("core/data/repo", mode = 1)

                with open(path1, "wb") as file:
                    file.write(await communication.get_json(Path("response/content")))

                with ZipFile(path1, "r") as obj:
                    obj.extractall(path2)

                ls = await self.path_utils.ls(path2)
                object_path = Path(f"{path2.json_path}/{ls[0]}")

                if "config.json" in await self.path_utils.ls(object_path):
                    config_path = Path(f"{object_path.json_path}/config.json", mode = 1)
                    content = self.filesystem.read_file(config_path, 2)

                    if "path" in content:
                        if "name" in content:
                            await self.filesystem.mv(Path(f"{object_path.json_path}/{content['path']}"), Path(f"{path3.json_path}/{content['name']}"))

                            if object_type in [0, 1, 2]:
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
            path1 = Path("core/data/communication/temp/0", mode = 1)

            if object_type == 0:
                path2 = Path("core/modules", mode = 1)
                common_config_path = Path(f"{path2.json_path}/modules.json", mode = 1)
            elif object_type == 1:
                path2 = Path("core/plugins", mode = 1)
                common_config_path = Path(f"{path2.json_path}/plugins.json")
            elif object_type == 2:
                path2 = Path("core/objects", mode = 1)
                common_config_path = Path(f"{path2.json_path}/objects.json", mode = 1)
            elif object_type == 3:
                path2 = Path("core/data/repo")

            with ZipFile(path.os_path, "r") as obj:
                obj.extractall(path1.os_path)

            ls = await self.path_utils.ls(path1)
            object_path = Path(f"{path1.json_path}/{ls[0]}", mode = 1)

            if "config.json" in await self.path_utils.ls(object_path):
                config_path = Path(f"{object_path.json_path}/config.json", mode = 1)
                content = await self.filesystem.read_file(config_path, 2)

                if "path" in content:
                    if "name" in content:
                        object_name = content["name"]

                        await self.filesystem.mv(Path(f"{object_path.json_path}/{content['path']}", mode = 1), Path(f"{path2.json_path}/{object_name}", mode = 1))

                        if object_type in [0, 1, 2]:
                            common_config = await self.filesystem.read_file(common_config_path, 2)
                            common_config[object_name] = {"enabled": True}

                            await self.filesystem.write_to_file(common_config_path, json.dumps(common_config))