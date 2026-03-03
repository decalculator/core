import asyncio
from core.modules.json.json import *
from core.plugins.communication.communication import *

class Updater:
    def __init__(self):
        self.updater = None

    async def init(self, url, config_url):
        self.updater = Json()
        await self.updater.init()

        communication = Communication()
        await communication.init()

        await self.updater.write("communication", communication)
        await self.updater.write("url", url)
        await self.updater.write("config_url", config_url)

    async def get_latest_version_number(self, version):
        result = None

        communication = await self.updater.get("communication")
        config_url = await self.updater.get("config_url")
        await communication.assign(config_url)
        await communication.get(1)

        if await communication.exists("response/content"):
            if await communication.get("response/mode") == 1:
                data = json.loads(await communication.get("response/content"))
                result = data["<version>"]

        return result

    async def update(self):
        # il faudra bien penser à reset le json de communication

        communication = await self.updater.get("communication")
        url = await self.updater.get("url")

        await communication.git_clone(url, "updater/temp")