import asyncio
import os
import aiofiles
import aiofiles.os
import json
from pathlib import Path as _path
from core.modules.json.json import *

class Filesystem:
    def __init__(self):
        self.filesystem = None

    async def init(self):
        self.filesystem = Json()
        await self.filesystem.init()

    async def mkdir(self, path):
        await aiofiles.os.mkdir(path.os_path)

    async def write_to_file(self, path, value):
        value_type = type(value)

        path = path.os_path

        async with aiofiles.open(path, "w") as file:
            if value_type == str:
                await file.write(value)

    async def read_file(self, path, mode):
        result = None

        async with aiofiles.open(path.os_path, "r") as file:
            if mode == 0:
                result = await file.read()
            elif mode == 1:
                result = await file.readlines()
            elif mode == 2:
                result = json.loads(await file.read())

        return result

    async def path_exists(self, path):
        return await aiofiles.os.path.exists(path.os_path)

    async def path_is_dir(self, path):
        return await aiofiles.os.path.isdir(path.os_path)

    async def mv(self, path1, path2):
        _path(path1.os_path).rename(path2.os_path)