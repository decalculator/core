import asyncio
import os
from core.modules.json.json import *
from core.modules.path.path import *
from core.modules.filesystem.filesystem import *

class Path_utils:
    def __init__(self):
        self.path = None
        self.filesystem = None

    async def init(self):
        self.path = Json()
        await self.path.init()
        self.filesystem = Filesystem()
        await self.filesystem.init()

    async def create(self, name):
        await self.path.create(name)

    async def write(self, path, value):
        await self.path.write(path, value)

    async def resolve(self, path):
        pass

    async def ls(self, path, exclude = None, mode = 0):
        # mode 0 : dossiers et fichiers
        # mode 1 : dossiers
        # mode 2 : fichiers

        path = path.json_path

        result = []
        if mode == 0:
            if exclude == None:
                result = os.listdir(path)
            else:
                for element in os.listdir(path):
                    if element not in exclude:
                        result.append(element)
        elif mode == 1:
            for element in os.listdir(path):
                if exclude == None:
                    if not os.path.isfile(os.path.join(path, element)):
                        result.append(element)
                else:
                    if element not in exclude and not os.path.isfile(os.path.join(path, element)):
                        result.append(element)
        elif mode == 2:
            for element in os.listdir(path):
                if exclude == None:
                    if os.path.isfile(os.path.join(path, element)):
                        result.append(element)
                else:
                    if element not in exclude and os.path.isfile(os.path.join(path, element)):
                        result.append(element)

        return result

    async def subfiles(self, path, separator = '/'):
        # https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
        # je me suis aidé d'internet pour des raisons de performances, voici ce que j'allais faire :
        # une fonction récursive qui fonctionne avec path.ls pour chaque dossier / sous-dossier
        # c'est globalement ce que l'on fait, mais c'est plus simple ici

        path = path.os_path

        files_list = []

        for root, dirs, files in os.walk(path):
            for name in files:
                files_list.append(Path(root + os.sep + name, mode = 1))

        return files_list

    async def get(self, path):
        return await self.path.get(path)