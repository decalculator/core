# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : pid_manager.py
# Rôle    : Ce fichier implémente la classe PidManager, qui est utile
#           pour gérer les PIDs.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe PidManager.
import asyncio

from core.modules.json.json import *
from core.modules.path.path import *
from core.modules.dynamic_value.dynamic_value import *

# Définition de la classe PidManager.
class PidManager:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        ppid: DynamicValue | None = None,
        content: Json | None = None
    ) -> None:

        """
        """

        # Initialisation et assignation des attributs.
        self.usoi = 1
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid

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

    # Déclaration de la signature de la méthode set_get_pid.
    def set_get_pid(
        self,
        unused_path: Path,
        used_path: Path,
        maximum_path: Path
    ) -> bool:

        """
        """

        # Assignations des arguments aux attributs.
        self.unused_path = unused_path
        self.used_path = used_path
        self.maximum_path = maximum_path

        # Nous renvoyons True.
        return True

    # Déclaration de la signature de la méthode get_pid.
    def get_pid(
        self,
        usoi: int,
        ppid: DynamicValue | None = None
    ) -> DynamicValue:

        """
        """

        # Obtention des attributs des PIDs utilisés, libres, et maximum.
        unused = self.data.get(self.unused_path)
        used = self.data.get(self.used_path)
        maximum = self.data.get(self.maximum_path)

        # Si des PIDs sont inutilisés (liste non-vide).
        if unused:
            # Ici, nous assignons le minimum des PIDs inutilisés à
            # new_pid_value et nous supprimons la valeur des PIDs
            # inutilisés.

            # D'un point de vu performances, il serait légèrement plus
            # rapide de prendre le premier PID directement.
            # (Surtout si unused devient très grand).

            new_pid_value = min(unused)
            new_pid = DynamicValue(new_pid_value)
            unused.remove(new_pid_value)

            # Si le nouveau PID est supérieur au maximum,
            # il devient ce maximum.

            if maximum < new_pid_value:
                self.data.write(maximum, new_pid_value)

        # Si il n'y a pas de PIDs inutilisés.
        else:
            # Le nouveau PID est le maximum + 1.
            new_pid_value = maximum + 1
            new_pid = DynamicValue(new_pid_value)
            # Nous écrivons ensuite ce nouveau maximum.
            self.data.write(self.maximum_path, new_pid_value)

        # Nous initialisons la structure à écrire dans la mémoire.
        data = {"usoi": usoi}

        # Si un PPID a été passé comme argument.
        if ppid is not None:
            # Data prend ce PPID.
            data["ppid"] = ppid.data

            # Nous obtenons la liste des PIDs utilisés.
            used = self.data.get(self.used_path)

            # Si le PPID est dans les PIDs utilisés.
            if ppid.data in used:

                # Si ce PPID n'a pas de CPIDs, nous initialisons
                # sa liste de CPIDs à une liste vide.
                if not "cpids" in used[ppid.data]:
                    used[ppid.data]["cpids"] = []

                # Nous obtenons la liste des CPIDs du PPID.
                cpids = used[ppid.data]["cpids"]
                # Nous ajoutons le PID à la liste des CPIDs du PPID.
                cpids.append(new_pid_value)

        # Nous ajoutons data comme valeur au PID dans les PIDs utilisés.
        used[new_pid_value] = data

        # Nous retournons le nouveau PID (DynamicValue)
        return new_pid

    # Déclaration de la signature de la méthode free_pid.
    def free_pid(self, pid: DynamicValue | int) -> bool:
        """
        """

        # Nous obtenons la liste des PIDs utilisés.
        used = self.data.get(self.used_path)
        # Nous supprimons de cette liste le PID passé en argument.
        used.remove(pid.data)

        # Nous obtenons l'ancien maximum.
        maximum = self.data.get(self.maximum_path)

        # Si il était le PID que nous venons de retirer,
        # nous lui assignons pour valeur le maximum de la nouvelle liste.
        if maximum == pid.data:
            self.data.write(self.maximum_path, max(used))

        # Nous retournons True.
        return True