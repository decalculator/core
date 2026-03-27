# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : loader.py
# Rôle    : Ce fichier implémente la classe Template, qui est utile
#           pour définir des classes temporaires (dynamiquement),
#           qui utilisent les 4 méthodes primaires.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Template.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *

# Définition de la classe Template.
class Template:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        name: str | None = None,
        usoi: int | None = None,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        ppid: DynamicValue | None = None,
        content: Json | None = None,
    ) -> None:

        # Initialisation et assignation des attributs.
        self.usoi = 10 if usoi is None else usoi
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.name = name

        # Initialisation de l'attribut data.
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
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
        # courant dans la mémoire (parente).
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 1:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 0:
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