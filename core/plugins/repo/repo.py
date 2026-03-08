import asyncio
from core.modules.static_memory.static_memory import *
from core.modules.json.json import *
from core.modules.path.path import *

class Repo:
    def __init__(self):
        self.repo = None
        self.static_memory = None

    async def init(self, separator):
        self.repo = Json()
        await self.repo.init(separator = separator)

        self.static_memory = Static_memory()
        await self.static_memory.init()

        await self.static_memory._create(Path("repo"))
        await self.static_memory._write(Path("repo/path"), Path("core/data/repo", mode = 1))
        await self.static_memory.get_structure(Path("repo/path"), Path("repo/files"), mode = 1)

        repos = await self.static_memory._get(Path("repo/files"))
        repos = repos["core"]["data"]["repo"]

        await self.repo.create(Path("repo"))
        await self.repo.write(Path("repo"), repos)

    async def _get(self, path):
        return await self.repo.get(path)