from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import asyncio
import uvicorn

class Server:
    def __init__(self):
        self.ip = None
        self.port = None
        self.server = None
        self.app = None
        self.base_dir = None
        self.templates = None

    async def init(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = {}
        self.app = FastAPI()

        self.base_dir = Path(__file__).resolve().parent
        self.templates = Jinja2Templates(directory = f"{self.base_dir}/templates")

        self.app.mount("/static", StaticFiles(directory = f"{self.base_dir}/static"))
        self._register_routes()

    def _register_routes(self):
        @self.app.get("/", response_class = HTMLResponse)
        @self.app.post("/", response_class = HTMLResponse)
        async def main_menu(request : Request):
            action = None

            if request.method == "POST":
                form = await request.form()
                action = form.get("menu_action", None)

                if "world_name_local" in form:
                    self.informations["world_name"] = form.get("world_name_local")

            return self.templates.TemplateResponse("core.html", {"request": request, "menu": action, "ui": "css/core.css"})

        @self.app.get("/menu/configuration", response_class = HTMLResponse)
        @self.app.post("/menu/configuration", response_class = HTMLResponse)
        async def configuration_menu(request : Request):
            action = None

            if request.method == "POST":
                form = await request.form()
                action = form.get("menu_action", None)

                if "world_name_local" in form:
                    self.server["world_name"] = form.get("world_name_local")

            return self.templates.TemplateResponse("core.html", {"request": request, "menu": action, "ui": "css/core.css"})

    async def run(self):
        config = uvicorn.Config(self.app, host = self.ip, port = self.port, log_level = "info")
        server = uvicorn.Server(config)
        await server.serve()

async def entry(**kwargs):
    print("server::entry > exec !")

    if "variables" in kwargs:
        variables = kwargs["variables"]

        if "unique_object_id" in kwargs:
            unique_object_id = kwargs["unique_object_id"]
            print(f"server::entry > unique object id : {unique_object_id}")

    server = Server()
    await server.init("127.0.0.1", 4999)
    print("server::entry > ready")
    print("server::entry > starting")
    await server.run()