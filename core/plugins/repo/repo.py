import asyncio
from core.modules.static_memory.static_memory import *
from core.modules.json.json import *

class Repo:
    def __init__(self):
        self.repo = None
        self.static_memory = None

    async def init(self):
        self.repo = Json()
        await self.repo.init()

        self.static_memory = Static_memory()
        await self.static_memory.init()

        await self.static_memory._create("repo")
        await self.static_memory._write("repo/path", "core/data/repo")
        await self.static_memory.get_structure("repo/path", "repo/files", mode = 1)

        repos = await self.static_memory._get("repo/files")
        repos = repos["core"]["data"]["repo"]

        await self.repo.create("repo")
        await self.repo.write("repo", repos)

    async def _get(self, path):
        return await self.repo.get(path)