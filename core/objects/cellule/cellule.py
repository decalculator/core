import asyncio

class Cell:
    def __init__(self):
        self.size = 1

    def cellule_add(self):
        self.size += 1

    def cellule_get(self):
        return self.size

async def cellule_add():
    return 1