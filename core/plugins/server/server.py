import os
import signal
import asyncio
import uvicorn

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.modules.core.scripting.json.json import *

class Server:
    def __init__(self):
        self.ip = None
        self.port = None
        self.server = None
        self.app = None
        self.base_dir = None
        self.templates = None
        self.variables = None
        self.unique_object_id = None

    async def init(self, ip, port, variables = None, unique_object_id = None):
        self.ip = ip
        self.port = port
        self.server = {}
        self.app = FastAPI()
        self.variables = variables
        self.unique_object_id = unique_object_id

        self.base_dir = Path(__file__).resolve().parent
        self.templates = Jinja2Templates(directory = f"{self.base_dir}/templates")

        self.app.mount("/static", StaticFiles(directory = f"{self.base_dir}/static"))
        await self._register_routes()

    async def shutdown(self):
        # ici, il faudra plutôt commencer par mettre un signal à True dans Memory
        # et sleep jusqu'à ce qu'un booléen comme "can_exit" soit vrai, le temps de sauvegarder de potentielles données etc
        # mais pour le moment, nous laisserons simplement cela

        os.kill(os.getpid(), signal.SIGTERM)

    async def _register_routes(self):
        @self.app.get("/", response_class = HTMLResponse)
        @self.app.post("/", response_class = HTMLResponse)
        async def main_menu(request : Request):
            response = {"request": request, "ui": "css/core.css", "js": "js/core.js"}
            action = None
            data = None

            if request.method == "POST":
                form = await request.form()
                action = form.get("menu_action", None)

                print(form)
                print(action)

                if action == "exit":
                    await self.shutdown()
                elif action == "tasks":
                    scheduler_var = await self.variables.get("scheduler/object")
                    scheduler_obj = scheduler_var.value

                    classic_running = {}
                    complex_running = {}

                    if await scheduler_obj.exists("classic_task/running"):
                        classic_running = await scheduler_obj.get("classic_task/running")

                    if await scheduler_obj.exists("complex_task/running"):
                        complex_running = await scheduler_obj.get("complex_task/running")
                        
                    response["data"] = {"classic_running": classic_running, "complex_running": complex_running}

                response["menu"] = action

            return self.templates.TemplateResponse("core.html", response)

    async def run(self):
        config = uvicorn.Config(self.app, host = self.ip, port = self.port, log_level = "info")
        server = uvicorn.Server(config)
        await server.serve()

async def entry(**kwargs):
    print("server::entry > exec !")

    variables = None
    unique_object_id = None

    if "variables" in kwargs:
        variables = kwargs["variables"]

    if "unique_object_id" in kwargs:
        unique_object_id = kwargs["unique_object_id"]

    server = Server()
    await server.init("127.0.0.1", 4999, variables = variables, unique_object_id = unique_object_id)
    print("server::entry > ready")
    print("server::entry > starting")
    await server.run()