import asyncio
import json
import os

from core.modules.path.path import *

class Json:
    def __init__(self):
        self.json = None
        self.console = None
        self.separator = None

    async def init(self, console = None, separator = '/'):
        self.separator = separator
        self.json = {}
        self.console = console
        if self.console != None:
            console_core = await self.console.get(Path("core"))
            console_core.append("json > ready")
            await self.console.write(Path("core"), console_core)

    async def create(self, name):
        name = name.json_path
        self.json[name] = {}

    async def remove(self, path):
        exec(f"del self.json{await self.path_to_json(path)}")
        # exec(f"del self.json{await self.path_to_json(Path(path.json_path))}")

    async def get(self, path, separator = '/'):
        splitted = path.splitted
        if len(splitted) > 0:
            result = self.json[splitted[0]]

            for i in range(1, len(splitted)):
                if splitted[i] in result:
                    result = result[splitted[i]]
        else:
            result = self.json

        return result

    async def exists(self, path):
        splitted = path.splitted
        size = len(splitted)
        temp = self.json

        result = False
        i = 0

        if size > 0:
            result = True
            while result and i < size:
                element = splitted[i]

                if element in temp:
                    temp = temp[element]
                else:
                    result = False

                i += 1

        return result

    async def path_to_json(self, path):
        if isinstance(path, Path):
            splitted = path.splitted
        else:
            print(path, type(path))

        result = ""

        for i in range(len(splitted)):
            result += f"[\"{splitted[i]}\"]"

        return result

    async def write(self, path, value, mode = 0):
        if mode == 1:
            splitted = path.splitted
            current_path = ""
            last_path = ""
            current_json_path = ""
            last_json_path = ""

            for i in range(len(splitted)):
                elem = splitted[i]

                last_path = current_path
                last_json_path = current_json_path

                if i == 0:
                    current_path += elem
                else:
                    current_path += f"{self.separator}{elem}"

                current_json_path = await self.path_to_json(Path(current_path))
                input_data = {"elem": elem, "object": self.json}

                if last_json_path:
                    payload = f"if elem not in object{last_json_path}:\n    object{last_json_path}[elem] = {{}}"
                else:
                    payload = f"if elem not in object:\n    object[elem] = {{}}"

                exec(payload, input_data)

        path = await self.path_to_json(path)
        input_data = {"conf": self.json, "value": value}

        exec(f"conf{path} = value", input_data)

    async def get_from_file(self, path):
        with open(path.os_path, "r") as file:
            return json.load(file)