import asyncio
import json

class Json:
    def __init__(self):
        self.json = None
        self.console = None

    async def init(self, console = None):
        self.json = {}
        self.console = console
        if self.console != None:
            console_core = await self.console.get("core")
            console_core.append("json > ready")
            await self.console.write("core", console_core)

    async def create(self, name):
        self.json[name] = {}

    async def remove(self, path):
        exec(f"del self.json{await self.path_to_json(await self.fix_path(path))}")

    async def fix_path(self, path):
        while path[-1] == '/':
            path = path[:-1]

        while path[0] == '/':
            path = path[1:]

        bad = False
        result = ""

        for i in range(len(path)):
            if path[i] == '/':
                if not bad:
                    result += path[i]
                    bad = True
            else:
                result += path[i]

                if bad:
                    bad = False

        return result

    async def get(self, path):
        path = await self.fix_path(path)

        splitted = path.split("/")
        result = self.json[splitted[0]]

        for i in range(1, len(splitted)):
            if splitted[i] in result:
                result = result[splitted[i]]

        return result

    async def exists(self, path):
        path = await self.fix_path(path)

        splitted = path.split("/")
        temp = self.json

        result = True
        i = 0
        while result and i < len(splitted):
            element = splitted[i]

            if element in temp:
                temp = temp[element]
            else:
                result = False

            i += 1

        return result

    async def path_to_json(self, path):
        path = await self.fix_path(path)

        splitted = path.split("/")
        result = ""

        for i in range(len(splitted)):
            result += f"[\"{splitted[i]}\"]"

        return result

    async def write(self, path, value, mode = 0):
        if mode == 1:
            splitted = path.split("/")
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
                    current_path += f"/{elem}"

                current_json_path = await self.path_to_json(current_path)
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
        with open(path, "r") as file:
            return json.load(file)