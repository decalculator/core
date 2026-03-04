import asyncio
import os
from core.modules.json.json import *
from core.modules.filesystem.filesystem import *
from core.modules.path.path import *

class Static_memory:
    def __init__(self):
        self.filesystem = None
        self.path = None
        self.static_memory = None

    async def init(self):
        self.filesystem = Filesystem()
        await self.filesystem.init()
        self.path = Path()
        await self.path.init()

        self.static_memory = Json()
        await self.static_memory.init()

    async def _create(self, name):
        await self.static_memory.create(name)
        await self.static_memory.write(f"{name}/files", {})

    async def _write(self, path, value):
        await self.static_memory.write(path, value)

    async def _get(self, path):
        return await self.static_memory.get(path)

    async def _exists(self, path):
        return await self.static_memory.exists(path)

    async def get_structure(self, in_path, out_path, mode = 0):
        path = await self.static_memory.get(in_path)
        if not await self.static_memory.exists(out_path):
            await self.static_memory.write(out_path, {}, 1)

        value = await self.static_memory.get(out_path)
        files = await self.path.subfiles(path)

        for file in files:
            path = f"{out_path}/{file}"
            if not await self.static_memory.exists(path):
                await self.static_memory.write(path, {}, 1)

            if mode == 1:
                await self.static_memory.write(f"{path}/content", await self.filesystem.read_file(file, 2))

    async def create(self, name, base_path = "core/data/static_memory"):
        main_directory_path = f"{base_path}/{name}"
        if not await self.filesystem.path_exists(main_directory_path):
            await self.filesystem.mkdir(main_directory_path)

    async def write(self, path, value):
        resolved_path = f"core/data/static_memory/{path}"
        splitted = path.split("/")

        temp_path = "core/data/static_memory"

        for i in range(len(splitted) - 1):
            temp_path += f"/{splitted[i]}"
            if not await self.filesystem.path_exists(temp_path):
                await self.filesystem.mkdir(temp_path)

        await self.filesystem.write_to_file(resolved_path, value)

    async def get(self, path, mode):
        return await self.filesystem.read_file(path, mode)