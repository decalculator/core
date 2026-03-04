import requests
import asyncio
from git import Repo
from core.modules.json.json import *

class Communication:
    def __init__(self):
        self.communication = None

    async def init(self):
        self.communication = Json()
        await self.communication.init()
        await self.communication.create("url")
        await self.communication.create("status")

    async def get(self, mode):
        try:
            response = requests.get(await self.communication.get("url"))
            status = 1
        except:
            response = None
            status = 0

        await self.communication.write("status", status)

        if response:
            try:
                response_content = response.json()
                response_mode = 1
            except:
                if mode == 0:
                    response_content = response.text
                elif mode == 1:
                    response_content = response.content
                response_mode = 0

            await self.communication.write("response", {"content": response_content, "mode": response_mode})

    async def _get(self, path):
        return await self.communication.get(path)

    async def assign(self, url):
        await self.communication.write("url", url)

    async def get_json(self, path):
        return await self.communication.get(path)

    async def exists(self, path):
        return await self.communication.exists(path)

    async def git_clone(self, url, folder):
        Repo.clone_from(url, folder)