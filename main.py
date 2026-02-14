import asyncio
import re

from core.modules.core.scripting.loader.loader import *
from core.modules.core.scripting.states.states import *
from core.modules.core.scripting.symbols.symbols import *
from core.modules.core.scripting.json.json import *
from core.modules.core.scripting.settings.settings import *
from core.modules.core.scripting.moment.moment import *
from core.modules.core.scripting.scheduler.scheduler import *
from core.modules.core.scripting.identifier.identifier import *

from core.modules.core.scripting.variable.variable import *
from core.modules.core.scripting.variables.variables import *
from core.modules.core.scripting.memory.memory import *

async def main():
    states = States()
    await states.init()

    memory = Memory()
    await memory.init(states)
    await memory.create("objects")
    await memory.create("core")

    core_variables = Variables()
    await core_variables.init(states)
    await core_variables.create("variables")

    await memory.write("core/variables", core_variables)

    identifier = Identifier()
    await identifier.init(states)
    await identifier.create("objects_id")

    identifier_var = Variable()
    await identifier_var.init(states, "object", identifier)
    await core_variables.write("variables/identifier", identifier_var)

    print(memory.memory.json)
    print(memory.memory.json["core"]["variables"].variables.json)
    print(memory.memory.json["core"]["variables"].variables.json["variables"]["identifier"].name)
    print(memory.memory.json["core"]["variables"].variables.json["variables"]["identifier"].value)

    await states.create("app")
    await states.write("app/value", "on")

    json = Json()
    await json.init()
    await json.create("settings")
    await json.write("settings", await json.get_from_file("core/modules/core/json/settings.json"))

    symbols = Symbols()
    await symbols.init(states)
    await symbols.create("symbols")

    settings_value = await json.get("settings")
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
    await loader.init(states, await symbols.get("<module_folder>"), await symbols.get("<plugin_folder>"), await symbols.get("<object_folder>"))

    settings = Settings()
    await settings.init(states, loader)
    await settings.create("objects")
    await settings.create("plugins")

    await settings.write("objects/folder", await symbols.get("<object_folder>"))
    await settings.write("objects/path", await symbols.get("<object_config>"))
    await settings.write("objects/content", await settings.settings.get_from_file(await settings.get("objects/path")))

    await settings.write("plugins/folder", await symbols.get("<plugin_folder>"))
    await settings.write("plugins/path", await symbols.get("<plugin_config>"))
    await settings.write("plugins/content", await settings.settings.get_from_file(await settings.get("plugins/path")))

    for plg in await settings.get("plugins/content/plugins"):
        await settings.enable(f"plugins/content/plugins/{plg}/enabled")
        await settings.save("plugins/path", "plugins/content")

    for obj in await settings.get("objects/content/objects"):
        await settings.enable(f"objects/content/objects/{obj}/enabled")
        await settings.save("objects/path", "objects/content")

    for obj in await settings.get("objects/content/objects"):
        if await settings.get(f"objects/content/objects/{obj}/enabled") == True:
            await loader.load(obj, "object")

    for plg in await settings.get("plugins/content/plugins"):
        if await settings.get(f"plugins/content/plugins/{plg}/enabled") == True:
            await loader.load(plg, "plugin")

    moment = Moment()
    await moment.init(states)
    await moment.create("time")
    await moment.write("time/value1", 0)

    scheduler = Scheduler()
    await scheduler.init(states)
    await scheduler.create("classic_task")
    await scheduler.create("complex_task")
    await scheduler.settings("classic_task/mode", "classic")
    await scheduler.settings("classic_task/model", "")
    await scheduler.settings("complex_task/mode", "complex")

    while await states.get("app/value") == "on":
        print(f"moment {await moment.get("time/value1")} :")

        for obj_name in await loader.get("loader"):
            objects = await loader.get(f"loader/{obj_name}/objects")

            if objects[0].object_type == "classic":
                await scheduler.write(f"classic_task/{obj_name}", objects)
            elif objects[0].object_type == "complex":
                if not obj_name in await scheduler.get("complex_task/running"):
                    running = await scheduler.get("complex_task/running")
                    running.append(obj_name)

                    await scheduler.write("complex_task/running", running)
                    await scheduler.write(f"complex_task/to_run/{obj_name}", objects)

        #await scheduler.run("complex_task/to_run")
        #await scheduler.write("complex_task/to_run", {})

        await scheduler.run("classic_task")
        await scheduler.write("classic_task", {})

        print("=" * 50)

        await asyncio.sleep(5)
        choice = 1

        if choice == "exit":
            await states.write("app/value", "off")
        else:
            await moment.write("time/value1", await moment.get("time/value1") + choice)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    asyncio.set_event_loop(loop)
    loop.run_forever()