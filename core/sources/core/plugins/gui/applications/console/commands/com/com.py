import asyncio
import dearpygui.dearpygui as dpg

from core.modules.path.path import *
from core.modules.json.json import *

async def com(kwargs):
    command = kwargs["command"]
    window_tag = kwargs["window_tag"]
    parent = kwargs["parent"]
    gui = kwargs["gui"]

    args_size = len(command.args)

    if args_size == 0:
        messages = [
            "welcome to core objects manager !",
            "available types :",
            "\tobject",
            "\tplugin",
            "\tmodule",
            "\trepository (bridge)\n",
            "available modes :",
            "\tlocal",
            "\turl",
            "\trepo\n",
            "available commands :",
            "\tcom install [mode] {path or url} [type] {name}",
            "\tcom uninstall [type] [name]",
            "\tcom update [mode] {path or url} [type] [name]",
            "\tcom upgrade [mode] {path or url} [type] [name]"
        ]

        payload = ""
        size = len(messages)

        for i in range(size):
            temp = messages[i]
            if i != size - 1:
                temp += "\n"

            payload += temp

        dpg.add_text(payload, parent = window_tag)

    else:
        sub_cmd = command.args[0]
        installator = gui.data.get(Path("settings/objects/installator"))

        if sub_cmd == "install":
            if args_size >= 5:
                mode = command.args[1]

                object_types = {"module": 0, "plugin": 1, "object": 2, "repo": 3}

                if mode == "local":
                    path = command.args[2]
                    object_type = object_types[command.args[3]]

                    print(path, object_type)

                    file_path_obj = Path(path, mode = 1)
                    extracted_path = installator.extract_object([object_type, file_path_obj])
                    object_name = await installator.get_object_name(extracted_path)
                    is_alreay_installed = await installator.is_alreay_installed([object_name, object_type])

                    if is_alreay_installed:
                        if "overwrite" in command.args:
                            await installator.uninstall([object_name, object_type])
                            await installator.install([1, object_type, 1, Path(path, mode = 1)], extracted_path = extracted_path)

                        else:
                            pass
                            # ...

                    else:
                        await installator.install([1, object_type, 1, Path(path, mode = 1)], extracted_path = extracted_path)

                elif mode == "url":
                    url = command.args[2]
                    object_type = command.args[3]

                    await installator.install([0, object_types[object_type], 1, url])

                elif mode == "repo":
                    object_type = command.args[2]
                    object_name = command.args[3]

        elif sub_cmd == "uninstall":
            if args_size >= 3:
                object_type = command.args[1]
                object_name = command.args[2]

                object_types = {"module": 0, "plugin": 1, "object": 2, "repo": 3}

                await installator.uninstall([object_name, object_types[object_type]])

        elif sub_cmd == "list":
            pass