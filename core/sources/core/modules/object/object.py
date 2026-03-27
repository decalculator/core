# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : object.py
# Rôle    : Ce fichier implémente la classe Object, qui est utile
#           pour charger des objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Object.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *
from core.modules.execution.execution import *

# Définition de la classe Object.
class Object:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        filesystem: Filesystem,
        pid_manager: PidManager,
        memory: Memory | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        ppid: DynamicValue | None = None,
        content: Json | None = None,
    ) -> None:

        """
        """

        # Initialisation et assignation des attributs.
        self.usoi = 12
        self.filesystem = filesystem
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.pid_manager = pid_manager

        self.data = Json()

        # Initialisation de l'attribut data.
        initialized = False
        if (hasattr(content, "usoi") and content.usoi == 5) or isinstance(content, dict):
            self.data.write(Path("settings"), content if isinstance(content, dict) else content.get(Path("")))
            initialized = True

        if not initialized:
            self.data.write(Path("settings"), {})
            initialized = True

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if self.pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    self.pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
        # courant dans la mémoire (parente).
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

        # 
        self.execution = Execution(filesystem = self.filesystem, pid_manager = self.pid_manager, content = self.data.get(Path("settings/execution"), mode = 1), memory = self.memory, logs = self.logs, ppid = self.pid)

    async def run(self):
        await self.execution.run()