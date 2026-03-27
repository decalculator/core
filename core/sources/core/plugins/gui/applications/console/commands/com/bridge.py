import asyncio
from core.plugins.gui.applications.console.commands.com.com import com as function

def com(**kwargs):
    loop = asyncio.get_running_loop()
    task = loop.create_task(function(kwargs = kwargs))

    return task