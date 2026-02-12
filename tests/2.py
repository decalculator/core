import asyncio

async def _exec(code):
    if type(code) == list:
        payload = ""

        for line in code:
            payload += f"{line}\n"
    else:
        payload = code

    exec_vars = {}
    exec(payload, exec_vars)

    bridge = exec_vars['bridge']
    asyncio.ensure_future(bridge())

async def main():
    script1 = [
        "import asyncio",
        "async def bridge():",
        "   print('script1')",
        "   await asyncio.sleep(5)",
        "   print('end')"
    ]

    script2 = [
        "import asyncio",
        "async def bridge():",
        "   print('script2')"
    ]

    scripts = [script1, script2]
    for script in scripts:
        await _exec(script)

loop = asyncio.new_event_loop()
loop.create_task(main())
asyncio.set_event_loop(loop)
loop.run_forever()