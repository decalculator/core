import asyncio
from core.modules.json.json import *
from core.modules.path.path import *
from core.plugins.communication.communication import *

class Updater:
    def __init__(self):
        self.updater = None

    async def init(self, url, config_url):
        self.updater = Json()
        await self.updater.init()

        communication = Communication()
        await communication.init()

        await self.updater.write(Path("communication"), communication)
        await self.updater.write(Path("url"), url)
        await self.updater.write(Path("config_url"), config_url)

    async def get_latest_version_number(self, version):
        result = None

        communication = await self.updater.get(Path("communication"))
        config_url = await self.updater.get(Path("config_url"))
        await communication.assign(config_url)
        await communication.get(1)

        if await communication.exists(Path("response/content")):
            if await communication._get(Path("response/mode")) == 1:
                response = await communication._get(Path("response/content"))
                result = response["<version>"]

        return result

    async def update(self):
        # il faudra bien penser à reset le json de communication

        communication = await self.updater.get("communication")
        url = await self.updater.get(Path("url"))

        await communication.git_clone(url, Path("_core", mode = 1))