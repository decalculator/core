import asyncio
from core.modules.json.json import *
from core.modules.filesystem.filesystem import *
from core.modules.path.path import *

class Static_memory:
    def __init__(self):
        self.filesystem = None
        self.path = None

    async def init(self):
        self.filesystem = Filesystem()
        await self.filesystem.init()
        self.path = Path()
        await self.path.init()

    async def create(self, name):
        main_directory_path = f"core/data/static_memory/{name}"
        if not await self.filesystem.path_exists(main_directory_path):
            await self.filesystem.mkdir(main_directory_path)

    async def write(self, path, value):
        resolved_path = f"core/data/static_memory/{path}"
        splitted = path.split("/")

        temp_path = "core/data/static_memory/"

        for i in range(len(splitted) - 1):
            temp_path += f"/{splitted[i]}"
            if not await self.filesystem.path_exists(temp_path):
                await self.filesystem.mkdir(temp_path)

        await self.filesystem.write_to_file(resolved_path, value)

    async def get(self, path, mode):
        return await self.filesystem.read_file(path, mode)