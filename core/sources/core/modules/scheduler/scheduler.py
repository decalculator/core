# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : scheduler.py
# Rôle    : Ce fichier implémente la classe Scheduler, qui est utile
#           pour exécuter des files d'objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Loader.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *
from core.modules.object.object import *

# Définition de la classe Loader.
class Scheduler:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        loader: Loader,
        filesystem: Filesystem,
        pid_manager: PidManager,
        memory: Memory | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        ppid: DynamicValue | None = None,
        content: Json | None = None,
        loop: Loop | None = None
    ) -> None:

        """
        """

        # Initialisation et assignation des attributs.
        self.usoi = 15
        self.loop = loop
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.ppid = ppid
        self.pid_manager = pid_manager
        self.filesystem = filesystem
        self.loader = loader
        self.selected_classic_path = None
        self.selected_complex_path = None

        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # Initialisation de l'attribut data.
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content)
                initialized = True

        if not initialized:
            self.data = Json()
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

    def write(self, path: Path, value, mode: int = 0) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description : Le chemin d'écriture.

            value (any) :
                Description : La valeur à écrire.

            mode (int) :
                Description : Le mode d'écriture.
                Valeur par défaut : 0.

        Sortie :
            written (bool) :
                Description : True si l'écriture a réussi, False sinon.

        Rôle :
            Écrit une valeur à un chemin donné dans la structure JSON.
        """

        # Écrit la valeur au chemin donné, et retourne le résultat.
        return self.data.write(path, value, mode=mode)

    def remove(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à supprimer.

        Sortie :
            (bool) :
                Description :
                    True si la suppression a réussi, False sinon.

        Rôle :
            Supprime la valeur située au chemin donné dans la structure JSON.
        """

        # Supprime la valeur située au chemin donné, et retourne le résultat.
        return self.data.remove(path)

    def get(self, path: Path):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à récupérer.

        Sortie :
            (any) :
                Description : La valeur située au chemin donné.

        Rôle :
            Récupère la valeur située au chemin donné dans la structure JSON.
        """

        # Retourne la valeur au chemin donné.
        return self.data.get(path)

    def exists(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin à vérifier.

        Sortie :
            (bool) :
                Description :
                    True si le chemin existe dans la structure JSON.

        Rôle :
            Vérifie si un chemin donné existe dans la structure JSON.
        """

        # Renvoie l'existence du path en bool.
        return self.data.exists(path)

    # Déclaration de la signature de la méthode active.
    async def active(self, content: dict):
        """
        """

        # Nous initialisons l'objets avec les attributs.
        obj = Object(
            filesystem = self.filesystem,
            pid_manager = self.pid_manager,
            memory = self.memory,
            logs = self.logs,
            content = content,
            ppid = self.pid
        )

        # Nous lançons l'objet.
        await obj.run()

        # Si l'objet a un type et un USOI.
        if "type" in content and "usoi" in content:
            object_type = content["type"]
            object_usoi = content["usoi"]

            # Si l'objet a déjà un path pids, nous y ajoutons son PID.
            if self.data.exists(Path(f"{object_type}s/{object_usoi}/pids")):
                pids = self.data.get(Path(f"{object_type}s/{object_usoi}/pids"))
                pids.append(obj.pid.data)

            # Sinon, nous y écrivons une liste contenant son unique PID.
            else:
                self.data.write(Path(f"{object_type}s/{object_usoi}/pids"), [obj.pid.data], mode = 1)

    # Déclaration de la signature de la méthode set_file.
    def set_file(self, classic_path: Path, complex_path: Path):
        """
        """

        # Nous assignons les arguments aux attributs.
        self.selected_classic_path = classic_path
        self.selected_complex_path = complex_path

    # Déclaration de la signature de la méthode run.
    def run(self, path: Path, mode: int = 0):
        """
        """

        # Si le mode est 0 (objets classiques).
        if mode == 0:
            # Nous intialisons le path vers la structure.
            to_run_path = path / "to_run"

            # Si ce path existe.
            if self.exists(to_run_path):
                # Nous obtenons la structure.
                to_run = self.get(to_run_path)

                # Pour chaque type d'objet et valeur, dans cette structure.
                for object_type, value in to_run.items():
                    # Pour chaque USOI.
                    for usoi in value:
                        # Nous initialisons le path vers son content.
                        content_path = Path(f"{object_type}/{usoi}/content")

                        # Si ce path existe, nous lançons l'exécution de
                        # Scheduler.active en async, avec le contenu de cet
                        # objet. Cela permet de lancer son exécution.
                        if self.loader.exists(content_path):
                            self.loop.create_task(self.active(self.loader.get(content_path)))

        # Sinon, si le mode est 1 (objet complexe).
        elif mode == 1:
            # Cette partie n'est pas encore implémentée pour le moment.
            pass

    # Déclaration de la signature de la méthode add_to_queue.
    def add_to_queue(
        self,
        path: Path,
        object_type: str,
        usoi: int,
        mode: int = 0
    ):

        """
        """

        # Si le mode est 0 (objet classique).
        if mode == 0:
            # Nous initialisons le path vers la structure.
            to_run_path = path / "to_run"

            # Si ce path existe.
            if self.exists(to_run_path):
                # Nous obtenons la structure.
                to_run = self.get(to_run_path / object_type)

                # Si l'usoi de l'objet n'est pas dans la structure.
                if usoi not in to_run:
                    # Nous l'ajoutons.
                    to_run.append(usoi)

    # Déclaration de la signature de la méthode clean_queue.
    def clean_queue(
        self,
        path: Path,
        object_type: str = "all",
        mode: int = 0
    ):

        """
        """

        # Si le mode est 0 (objet classique).
        if mode == 0:
            # Nous initialisons le path vers la structure.
            to_run_path = path / "to_run"

            # Si ce path existe.
            if self.exists(to_run_path):
                # Nous obtenons la structure.
                to_run = self.get(to_run_path)

                # Si le nettoyage concerne tous les types.
                if object_type == "all":
                    # Pour chaque type, nous écrivons une liste vide.
                    for object_type in to_run:
                        self.write(to_run_path / object_type, [])

                # Si le nettoyage est ciblé.
                else:
                    # Nous écrivons une liste vide au path indiqué.
                    self.write(to_run_path / object_type, [])

    """
    {
        "running":
        {
            "objects":
            {
                [PID1, PID2]
            },
            "plugins":
            {
                [PID1, PID2]
            },
            "modules":
            {
                [PID1, PID2]
            }
        },

        "to_run":
        {
            "objects":
            {
                [USOI1, USOI2]
            },
            "plugins":
            {
                [USOI1, USOI2]
            },
            "modules":
            {
                [USOI1, USOI2]
            }
        }
    }
    """