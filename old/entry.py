import json
import asyncio
import re

from core.modules.loader.loader import *
from core.modules.symbols.symbols import *
from core.modules.json.json import *
from core.modules.settings.settings import *
from core.modules.moment.moment import *
from core.modules.scheduler.scheduler import *
from core.modules.identifier.identifier import *
from core.modules.asynchrone.asynchrone import *
from core.modules.device.device import *

from core.modules.variable.variable import *
from core.modules.variables.variables import *
from core.modules.memory.memory import *

from core.modules.console.console import *

async def main():
    ENTRY_FILE = "core/data/entry/entry.json"

    with open(ENTRY_FILE, "r") as file:
        entry_file_data = json.load(file)

    for key, value in entry_file_data["text"].items():
        content = value["content"]
        hide = value["hide"]
        hide_title = value["hide_title"]

        if not hide:
            value_type = type(content)

            if value_type == list:
                if not hide_title:
                    print(f"{key} :")
                for line in content:
                    print(line)
            # elif value_type == dict:
                # nous verrons plus tard pour une recherche profonde
            else:
                text = ""
                if not hide_title:
                    text += f"{key} : "
                text += content
                print(text)

    memory = Memory()
    await memory.init()
    await memory.create("variables")

    variables = Variables()
    await variables.init()

    await memory.write("variables", variables)

    console = Console()
    await console.init(variables)
    await console.create("core")
    await console.write("core", ["memory > ready", "variables > ready"])

    identifier = Identifier()
    await identifier.init(variables, console = console)
    await identifier.create("objects_id")

    await variables.create("objects")

    await variables.create("app")
    app_value = Variable()
    await app_value.init("on", console = console)
    await variables.write("app/value", app_value)

    json_obj = Json()
    await json_obj.init(console = console)
    await json_obj.create("settings")
    await json_obj.write("settings", await json_obj.get_from_file("core/data/core/settings.json"))

    symbols = Symbols()
    await symbols.init(variables, console = console)
    await symbols.create("symbols")

    device = Device()
    await device.init(variables, console = console)
    await device.create("device")

    device_os = await device.get_os()
    await device.write("device/system", device_os[0])
    await device.write("device/release", device_os[1])
    await device.write("device/version", device_os[2])

    settings_value = await json_obj.get("settings")
    for key, value in settings_value.items():
        if key not in await symbols.get("symbols"):
            await symbols.write(f"symbols/{key}", value)

    pattern = "<[a-z/<>_]*>"

    for key in await symbols.get("symbols"):
        current_value = await symbols.get(f"symbols/{key}")
        done = False

        while not done:
            match = re.search(pattern, current_value)

            if match:
                to_replace = match.group()
                if to_replace in await symbols.get("symbols"):
                    replace_by = await symbols.get(f"symbols/{to_replace}")
                else:
                    replace_by = "<not_found>"

                current_value = current_value.replace(to_replace, replace_by)
            else:
                await symbols.write(key, current_value)
                done = True

    loader = Loader()
    await loader.init(variables, await symbols.get("<module_folder>"), await symbols.get("<plugin_folder>"), await symbols.get("<object_folder>"), console = console)

    settings = Settings()
    await settings.init(variables, loader, console = console)

    await settings.create("core")
    await settings.write("core/version", await symbols.get("<version>"))

    await settings.create("repo")
    await settings.write("repo/url", await symbols.get("<repo_url>"))
    await settings.write("repo/config_url", await symbols.get("<repo_config_url>"))

    await settings.create("objects")
    await settings.create("plugins")

    await settings.write("objects/folder", await symbols.get("<object_folder>"))
    await settings.write("objects/path", await symbols.get("<object_config>"))
    await settings.write("objects/content", await settings.settings.get_from_file(await settings.get("objects/path")))

    await settings.write("plugins/folder", await symbols.get("<plugin_folder>"))
    await settings.write("plugins/path", await symbols.get("<plugin_config>"))
    await settings.write("plugins/content", await settings.settings.get_from_file(await settings.get("plugins/path")))

    for plg in await settings.get("plugins/content/plugins"):
        await settings.enable(f"plugins/content/{plg}/enabled")
        await settings.save("plugins/path", "plugins/content")

    for obj in await settings.get("objects/content/objects"):
        await settings.enable(f"objects/content/{obj}/enabled")
        await settings.save("objects/path", "objects/content")

    entry = [[], []]

    for plg in await settings.get("plugins/content/plugins"):
        if await settings.get(f"plugins/content/plugins/{plg}/enabled") == True:
            if await settings.get(f"plugins/content/plugins/{plg}/entry") == True:
                entry[0].append(plg)

    for obj in await settings.get("objects/content/objects"):
        if await settings.get(f"objects/content/objects/{obj}/enabled") == True:
            if await settings.get(f"objects/content/objects/{obj}/entry") == True:
                entry[1].append(obj)

    size = len(entry[0]) + len(entry[1])

    if size == 0:
        print("no entry ?")
    else:
        print("objects :")
        for i in range(len(entry[1])):
            print(f"{i} : {entry[1][i]}")

        add = len(entry[1])

        print("plugins :")
        for i in range(len(entry[0])):
            print(f"{i + add} : {entry[0][i]}")

        all_entry = entry[1]
        all_entry.extend(entry[0])

        print("type numbers that you wan't to enable, and type \"done\", when done (\"*\" to enable all)")

        choices = []
        done = False
        while not done:
            choice = await ainput("> ")

            if choice == "done":
                done = True
            else:
                if choice.isdigit():
                    choice = int(choice)
                    if choice not in choices:
                        choices.append(choice)
                    else:
                        print("already enabled")
                elif choice == "*":
                    choices = []
                    for i in range(size):
                        choices.append(i)
                    done = True

        for i in range(len(choices)):
            obj = all_entry[choices[i]]
            unique_object_id = await identifier.generate_id("objects_id")

            if i < len(entry[0]):
                await loader.load(obj, "plugin", unique_object_id)
                await loader.write(f"loader/{obj}/{unique_object_id}/enabled", True)
            else:
                await loader.load(obj, "object", unique_object_id)
                await loader.write(f"loader/{obj}/{unique_object_id}/enabled", True)

    moment = Moment()
    await moment.init(variables, console = console)
    await moment.create("time")
    await moment.write("time/value1", 0)

    scheduler = Scheduler()
    await scheduler.init(variables, console = console)
    await scheduler.create("classic_task")
    await scheduler.create("complex_task")
    await scheduler.settings("classic_task/mode", "classic")
    await scheduler.settings("classic_task/model", "")
    await scheduler.settings("complex_task/mode", "complex")

    for obj_name in await loader.get("loader"):
        objects = await loader.get(f"loader/{obj_name}/objects")

        for unique_object_id, value in objects.items():
            if await loader.get(f"loader/{obj_name}/{unique_object_id}/enabled") == True:
                temp_objs = await loader.get(f"loader/{obj_name}/objects/{unique_object_id}/object/objects")
                if temp_objs[0].object_type == "classic":
                    if not await scheduler.exists(f"classic_task/{obj_name}"):
                        await scheduler.write(f"classic_task/{obj_name}", {})
                    await scheduler.write(f"classic_task/{obj_name}/{unique_object_id}", value)
                elif temp_objs[0].object_type == "complex":
                    if not await scheduler.exists(f"complex_task/to_run/{obj_name}"):
                        await scheduler.write(f"complex_task/to_run/{obj_name}", {})

                    if not await scheduler.exists(f"complex_task/running/{obj_name}/{unique_object_id}"):
                        await scheduler.write(f"complex_task/to_run/{obj_name}/{unique_object_id}", temp_objs)

                    if not await scheduler.exists(f"complex_task/running/{obj_name}"):
                        await scheduler.write(f"complex_task/running/{obj_name}", {})

                    if not await scheduler.exists(f"complex_task/running/{obj_name}/{unique_object_id}"):
                        await scheduler.write(f"complex_task/running/{obj_name}/{unique_object_id}", True)
            else:
                if await scheduler.exists(f"classic_task/{obj_name}/{unique_object_id}"):
                    await scheduler.write(f"classic_task/{obj_name}/{unique_object_id}", {})

    await scheduler.run("complex_task/to_run")
    await scheduler.write("complex_task/to_run", {})
    await scheduler.run("classic_task")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    asyncio.set_event_loop(loop)
    loop.run_forever()