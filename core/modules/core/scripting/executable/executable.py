# executable.py
# Il s'agit du fichier implémentant la classe Executable.

import asyncio
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.variable.variable import *

class Executable:
    def __init__(self):
        self.executable = None
        self.macros = None
        self.name = None
        self.type = None
        self.file = None
        self.process_type = None
        self.execution_mode = None
        self.execution_content = None
        self.result_true = None
        self.result_false = None
        self.variables = None
        self.result_code = None

    async def init(self, config, variables, macros = None):
        self.executable = Json()
        await self.executable.init()
        await self.executable.create("executable")
        await self.executable.write("executable", config)

        self.macros = macros

        # la condition est temporaire (fragile)
        if await self.executable.exists("executable/type"):
            self.name = await self.executable.get("executable/name")
            self.type = await self.executable.get("executable/type")
            self.file = await self.executable.get("executable/file")
            self.process_type = await self.executable.get("executable/process_type")
            self.execution_mode = await self.executable.get("executable/execution/mode")
            self.execution_content = await self.executable.get("executable/execution/content")

            if await self.executable.exists("executable/execution/result/true"):
                self.result_true = await self.executable.get("executable/execution/result/true")
            if await self.executable.exists("executable/execution/result/false"):
                self.result_false = await self.executable.get("executable/execution/result/false")
        else:
            if await self.executable.exists("executable/macro"):
                value = await self.executable.get("executable/macro")

                found = False
                i = 0

                while i < len(self.macros) and not found:
                    macro = self.macros[i]
                    if macro.name == value:
                        found = True
                    i += 1

                if found:
                    self.name = await macro.executable.get("executable/name")
                    self.type = await macro.executable.get("executable/type")
                    self.file = await macro.executable.get("executable/file")
                    self.process_type = await macro.executable.get("executable/process_type")
                    self.execution_mode = await macro.executable.get("executable/execution/mode")
                    self.execution_content = await macro.executable.get("executable/executable/execution/content")
                    self.result_true = await self.executable.get("executable/execution/result/true")
                    self.result_false = await self.executable.get("executable/execution/result/false")

        self.variables = variables
        await self.variables.create(self.name)
        obj = Variable()
        await obj.init(self)
        await self.variables.write(f"{self.name}/object", obj)

        self.result_code = -1

    async def execute(self, logs = False, mode = 0, unique_object_id = None):
        data = []
        temp = await self.executable.get("executable")

        done = False
        while not done:
            executable = Executable()
            await executable.init(temp, self.variables, self.macros)
            data.append(executable)

            if "type" in temp:
                if "execution_conditions" in temp["execution"]:
                    # [0] : temporaire
                    temp = temp["execution"]["execution_conditions"][0]
                else:
                    done = True
            else:
                if "execution_conditions" in temp:
                    # [0] : temporaire
                    temp = temp["execution_conditions"][0]
                else:
                    done = True

        i = len(data) - 1
        done = False
        result_code = False

        while i >= 0 and not done:
            executable_object = data[i]

            if logs:
                print(f"execute : {executable_object.name}")
                print(f"expected result : {executable_object.result_true}")

            with open(executable_object.file, "r") as file:
                file_data = file.readlines()
                file.close()

            lines = [
                "import asyncio"
            ]

            if executable_object.execution_mode == "exec":
                if executable_object.execution_content == "all":
                    lines = file_data
                else:
                    if executable_object.process_type == "import":
                        path = executable_object.file

                        if ".py" in path:
                            path = path.replace(".py", "")
                        if "/" in path:
                            path = path.replace("/", ".")

                        lines.append(f"from {path} import *")

                    lines.append("async def bridge():")
                    lines.append("    try:")
                    lines.append(f"        return await {executable_object.execution_content}(variables = variables, unique_object_id = unique_object_id)")
                    lines.append("    except Exception as error:")
                    lines.append("        print(error)")
                    lines.append("    except:")
                    lines.append("        print('error')")

            if len(lines) > 0:
                result = await self._exec(lines, mode = mode, unique_object_id = unique_object_id)

                if mode == "classic":
                    if logs:
                        print(f"result : {result}")
                    if result == executable_object.result_true:
                        if i == 0:
                            result_code = True
                            done = True
                    else:
                        done = True
                else:
                    # ...
                    pass
            if logs:
                print()
            i -= 1

        self.result_code = result_code
        if logs:
            print(f"global result : {self.result_code}")

    async def _exec(self, code, mode = None, unique_object_id = None):
        payload = ""

        if type(code) == list:
            for line in code:
                payload += f"{line}\n"
        else:
            payload = code

        exec_vars = {"variables": self.variables, "unique_object_id": unique_object_id}
        exec(payload, exec_vars)

        bridge = exec_vars['bridge']

        if mode == "classic":
            result = await bridge()
        elif mode == "complex":
            result = asyncio.ensure_future(bridge())

        return result