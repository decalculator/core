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
    memory = Memory()
    await memory.init()
    await memory.create("variables")

    variables = Variables()
    await variables.init()

    await memory.write("variables", variables)

    states = States()
    await states.init()

    identifier = Identifier()
    await identifier.init(variables)
    await identifier.create("objects_id")

    await variables.create("objects")
    # objects/{obj_unique_id}/object : l'objet
    # objects/{obj_unique_id}/memory : sa mémoire

    await variables.create("app")
    app_value = Variable()
    await app_value.init("on")
    await variables.write("app/value", app_value)

    json = Json()
    await json.init()
    await json.create("settings")
    await json.write("settings", await json.get_from_file("core/modules/core/json/settings.json"))

    symbols = Symbols()
    await symbols.init(variables)
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
    await loader.init(variables, await symbols.get("<module_folder>"), await symbols.get("<plugin_folder>"), await symbols.get("<object_folder>"))

    settings = Settings()
    await settings.init(variables, loader)
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
            unique_object_id = await identifier.generate_id("objects_id")
            await loader.load(obj, "object", unique_object_id)

    for plg in await settings.get("plugins/content/plugins"):
        if await settings.get(f"plugins/content/plugins/{plg}/enabled") == True:
            unique_object_id = await identifier.generate_id("objects_id")
            await loader.load(plg, "plugin", unique_object_id)

    moment = Moment()
    await moment.init(variables)
    await moment.create("time")
    await moment.write("time/value1", 0)

    scheduler = Scheduler()
    await scheduler.init(variables)
    await scheduler.create("classic_task")
    await scheduler.create("complex_task")
    await scheduler.settings("classic_task/mode", "classic")
    await scheduler.settings("classic_task/model", "")
    await scheduler.settings("complex_task/mode", "complex")

    exit_bool = False
    while not exit_bool:
        print(f"moment {await moment.get("time/value1")} :")

        for obj_name in await loader.get("loader"):
            objects = await loader.get(f"loader/{obj_name}/objects")

            for unique_object_id, value in objects.items():
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

        await scheduler.run("complex_task/to_run")
        await scheduler.write("complex_task/to_run", {})

        await scheduler.run("classic_task")
        await scheduler.write("classic_task", {})

        print("=" * 50)

        await asyncio.sleep(5)
        choice = 1

        _var = await variables.get("app/value")
        if _var.value == "off" or choice == "exit":
            await variables.write("app/value", "off")
            exit_bool = True
        else:
            await moment.write("time/value1", await moment.get("time/value1") + choice)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    asyncio.set_event_loop(loop)
    loop.run_forever()