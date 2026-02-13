import asyncio

"""
def function():
    lines = [
        "a += 1"
    ]

    payload = ""
    for line in lines:
        payload += f"{line}\n"

    a = 1

    locals_var = locals()
    globals_var = globals()

    exec(payload, globals_var, locals_var)

    return locals_var["a"]

print(function())

lines = [
    "a += 1"
]

payload = ""
for line in lines:
    payload += f"{line}\n"

a = 1

exec(payload)

print(a)
"""

async def test():
    a = 1

async def function1():
    lines = [
        "import asyncio",
        "from test import *",
        "async def bridge():",
        "    return await test(gl0bals = globals())"
    ]

    payload = ""
    for line in lines:
        payload += f"{line}\n"

    global states
    states = {"Moment": 1, "app": "on"}

    var = globals()
    exec(payload, var)

    bridge = var['bridge']
    await bridge()

async def function2():
    lines = [
        "print(globals())"
    ]

    payload = ""
    for line in lines:
        payload += f"{line}\n"

    global a

    var = globals()
    exec(payload, var)

async def main():
    await test()
    await function1()
    await function2()

asyncio.run(main())