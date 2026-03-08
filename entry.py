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
from core.modules.path.path import *
from core.modules.signals.signals import *

from core.modules.variable.variable import *
from core.modules.variables.variables import *
from core.modules.memory.memory import *

from core.modules.console.console import *

async def main():
    ENTRY_FILE = Path("core/data/entry/entry.json", mode = 1)

    with open(ENTRY_FILE.os_path, "r") as file:
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
    await memory.create(Path("variables"))

    variables = Variables()
    await variables.init()

    await memory.write(Path("variables"), variables)

    console = Console()
    await console.init(variables)
    await console.create(Path("core"))
    await console.write(Path("core"), ["memory > ready", "variables > ready"])

    signals = Signals()
    await signals.init(variables)
    await signals.create(Path("objects"))

    identifier = Identifier()
    await identifier.init(variables, console = console)
    await identifier.create(Path("objects_id"))

    await variables.create(Path("objects"))

    await variables.create(Path("app"))
    app_value = Variable()
    await app_value.init("on", console = console)
    await variables.write(Path("app/value"), app_value)

    json_obj = Json()
    await json_obj.init(console = console)
    await json_obj.create(Path("settings"))
    await json_obj.write(Path("settings"), await json_obj.get_from_file(Path("core/data/core/settings.json", mode = 1)))

    symbols = Symbols()
    await symbols.init(variables, console = console)
    await symbols.create(Path("symbols"))

    settings_value = await json_obj.get(Path("settings"))
    for key, value in settings_value.items():
        if key not in await symbols.get(Path("symbols")):
            await symbols.write(Path(f"symbols/{key}"), value)

    pattern = "<[a-z/<>_]*>"

    for key in await symbols.get(Path("symbols")):
        current_value = await symbols.get(Path(f"symbols/{key}"))
        done = False

        while not done:
            match = re.search(pattern, current_value)

            if match:
                to_replace = match.group()
                if to_replace in await symbols.get(Path("symbols")):
                    replace_by = await symbols.get(Path(f"symbols/{to_replace}"))
                else:
                    replace_by = "<not_found>"

                current_value = current_value.replace(to_replace, replace_by)
            else:
                await symbols.write(Path(key), current_value)
                done = True

    loader = Loader()
    await loader.init(variables, await symbols.get(Path("<module_folder>")), await symbols.get(Path("<plugin_folder>")), await symbols.get(Path("<object_folder>")), console = console)

    settings = Settings()
    await settings.init(variables, loader, console = console)

    await settings.create(Path("core"))
    await settings.write(Path("core/version"), await symbols.get(Path("<version>")))

    await settings.create(Path("repo"))
    await settings.write(Path("repo/url"), await symbols.get(Path("<repo_url>")))
    await settings.write(Path("repo/config_url"), await symbols.get(Path("<repo_config_url>")))

    await settings.create(Path("objects"))
    await settings.create(Path("plugins"))

    await settings.write(Path("objects/folder"), await symbols.get(Path("<object_folder>")))
    await settings.write(Path("objects/path"), await symbols.get(Path("<object_config>")))
    await settings.write(Path("objects/content"), await settings.settings.get_from_file(Path(await settings.get(Path("objects/path")), mode = 1)))

    await settings.write(Path("plugins/folder"), await symbols.get(Path("<plugin_folder>")))
    await settings.write(Path("plugins/path"), await symbols.get(Path("<plugin_config>")))
    await settings.write(Path("plugins/content"), await settings.settings.get_from_file(Path(await settings.get(Path("plugins/path")), mode = 1)))

    for plg in await settings.get(Path("plugins/content/plugins")):
        await settings.enable(Path(f"plugins/content/{plg}/enabled"))
        await settings.save(Path("plugins/path"), Path("plugins/content"))

    for obj in await settings.get(Path("objects/content/objects")):
        await settings.enable(Path(f"objects/content/{obj}/enabled"))
        await settings.save(Path("objects/path"), Path("objects/content"))

    entry = [[], []]

    for plg in await settings.get(Path("plugins/content/plugins")):
        if await settings.get(Path(f"plugins/content/{plg}/enabled")) == True:
            if await settings.get(Path(f"plugins/content/{plg}/entry")) == True:
                entry[0].append(plg)

    for obj in await settings.get(Path("objects/content/objects")):
        if await settings.get(Path(f"objects/content/{obj}/enabled")) == True:
            if await settings.get(Path(f"objects/content/{obj}/entry")) == True:
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

        print("select entry(ies) and type \"done\" (\"*\" to enable all)")

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
            unique_object_id = await identifier.generate_id(Path("objects_id"))

            if i < len(entry[0]):
                await loader.load(obj, "plugin", unique_object_id)
                await loader.write(Path(f"loader/{obj}/{unique_object_id}/enabled"), True)
            else:
                await loader.load(obj, "object", unique_object_id)
                await loader.write(Path(f"loader/{obj}/{unique_object_id}/enabled"), True)

    moment = Moment()
    await moment.init(variables, console = console)
    await moment.create(Path("time"))
    await moment.write(Path("time/value1"), 0)

    scheduler = Scheduler()
    await scheduler.init(variables, console = console)
    await scheduler.create(Path("classic_task"))
    await scheduler.create(Path("complex_task"))
    await scheduler.settings(Path("classic_task/mode"), "classic")
    await scheduler.settings(Path("classic_task/model"), "")
    await scheduler.settings(Path("complex_task/mode"), "complex")

    for obj_name in await loader.get(Path("loader")):
        objects = await loader.get(Path(f"loader/{obj_name}/objects"))

        for unique_object_id, value in objects.items():
            if await loader.get(Path(f"loader/{obj_name}/{unique_object_id}/enabled")) == True:
                temp_objs = await loader.get(Path(f"loader/{obj_name}/objects/{unique_object_id}/object/objects"))
                if temp_objs[0].object_type == "classic":
                    if not await scheduler.exists(Path(f"classic_task/{obj_name}")):
                        await scheduler.write(Path(f"classic_task/{obj_name}"), {})
                    await scheduler.write(Path(f"classic_task/{obj_name}/{unique_object_id}"), value)
                elif temp_objs[0].object_type == "complex":
                    if not await scheduler.exists(Path(f"complex_task/to_run/{obj_name}")):
                        await scheduler.write(Path(f"complex_task/to_run/{obj_name}"), {})

                    if not await scheduler.exists(Path(f"complex_task/running/{obj_name}/{unique_object_id}")):
                        await scheduler.write(Path(f"complex_task/to_run/{obj_name}/{unique_object_id}"), temp_objs)

                    if not await scheduler.exists(Path(f"complex_task/running/{obj_name}")):
                        await scheduler.write(Path(f"complex_task/running/{obj_name}"), {})

                    if not await scheduler.exists(Path(f"complex_task/running/{obj_name}/{unique_object_id}")):
                        await scheduler.write(Path(f"complex_task/running/{obj_name}/{unique_object_id}"), True)
            else:
                if await scheduler.exists(Path(f"classic_task/{obj_name}/{unique_object_id}")):
                    await scheduler.write(Path(f"classic_task/{obj_name}/{unique_object_id}"), {})

    await scheduler.run(Path("complex_task/to_run"))
    await scheduler.write(Path("complex_task/to_run"), {})
    await scheduler.run(Path("classic_task"))

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    asyncio.set_event_loop(loop)
    loop.run_forever()