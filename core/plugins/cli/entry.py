import asyncio
from core.plugins.cli.cli import *

async def entry(**kwargs):
    # print("cli::entry > exec !")

    variables = None
    unique_object_id = None

    if "variables" in kwargs:
        variables = kwargs["variables"]

    if "unique_object_id" in kwargs:
        unique_object_id = kwargs["unique_object_id"]

    cli = Cli()
    await cli.init(variables, unique_object_id)