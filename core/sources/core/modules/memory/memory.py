from __future__ import annotations

import asyncio

from core.modules.json.json import *
from core.modules.path.path import *

class Memory:
    def __init__(
        self,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        ppid: DynamicValue | None = None,
        content: Json | None = None,
        references_manager: ReferencesManager | None = None
    ) -> None:

        """
        """

        # Initialisation et assignation des attributs.
        self.usoi = 1
        self.references_manager = references_manager
        self.pid_manager = pid_manager
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if self.pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    self.pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Initialisation de l'attribut data.
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content, pid_manager = pid_manager, references_manager = self.references_manager, ppid = self.pid)
                initialized = True

        if not initialized:
            self.data = Json(pid_manager = pid_manager, references_manager = self.references_manager, ppid = self.pid)
            initialized = True

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