# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : temp.py
# Rôle    : Ce fichier implémente la classe Temp, qui est utile
#           pour la gestion d'identifiants temporaires.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Temp.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *


# Définition de la classe Temp.
class Temp:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        filesystem: Filesystem,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        content: Json | None = None,
        ppid: DynamicValue | None = None
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            filesystem (Filesystem) :
                Description : L'objet Filesystem parent.

            memory (Memory | None) :
                Description : L'objet Memory parent.
                Valeur par défaut : None.

            pid_manager (PidManager | None) :
                Description : L'objet PidManager parent.
                Valeur par défaut : None.

            logs (Logs | None) :
                Description : L'objet Logs parent.
                Valeur par défaut : None.

            pid (Pid | None) :
                Description : Le PID de l'objet.
                Valeur par défaut : None.

            content (Json | None) :
                Description : Le contenu JSON de l'objet.
                Valeur par défaut : None.

            ppid (DynamicValue | None) :
                Description : Le PID de l'objet parent.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe Temp,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation de l'USOI de l'objet courant.
        self.usoi = 27

        # Initialisation de l'attribut data.
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content)
                initialized = True

        if not initialized:
            self.data = Json()
            initialized = True

        # Initialisation et assignation des attributs.
        self.ppid = ppid

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        self.filesystem = filesystem
        self.memory = memory
        self.logs = logs
        self.pid = pid

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
        # courant dans la mémoire (parente).
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

    # Déclaration de la signature de la méthode write.
    def write(
        self,
        path: Path,
        value,
        mode: int = 0
    ) -> bool:
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
        return self.data.write(path, value, mode = mode)

    # Déclaration de la signature de la méthode remove.
    def remove(
        self,
        path: Path
    ) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à supprimer.

        Sortie :
            removed (bool) :
                Description : True si la suppression a réussi, False sinon.

        Rôle :
            Supprime la valeur située au chemin donné dans la structure JSON.
        """

        # Supprime la valeur située au chemin donné, et retourne le résultat.
        return self.data.remove(path)

    # Déclaration de la signature de la méthode get.
    def get(
        self,
        path: Path
    ):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à récupérer.

        Sortie :
            value (any) :
                Description : La valeur située au chemin donné dans la
                    structure JSON.

        Rôle :
            Récupère la valeur située au chemin donné dans la structure JSON.
        """

        # Retourne la valeur au chemin donné.
        return self.data.get(path)

    # Déclaration de la signature de la méthode exists.
    def exists(
        self,
        path: Path
    ):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin à vérifier.

        Sortie :
            exists (bool) :
                Description : True si le chemin existe dans la structure JSON,
                    False sinon.

        Rôle :
            Vérifie si un chemin donné existe dans la structure JSON.
        """

        # Renvoie l'existence du path en bool.
        return self.data.exists(path)

    # Déclaration de la signature de la méthode set_get_id.
    def set_get_id(
        self,
        unused_path: Path,
        used_path: Path,
        maximum_path: Path
    ) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            unused_path (Path) :
                Description : Le chemin vers la liste des identifiants
                    non utilisés.

            used_path (Path) :
                Description : Le chemin vers la liste des identifiants
                    utilisés.

            maximum_path (Path) :
                Description : Le chemin vers la valeur de l'identifiant
                    maximum actuel.

        Sortie :
            result (bool) :
                Description : True si la configuration a réussi.

        Rôle :
            Configure les chemins nécessaires à la gestion des identifiants
            temporaires, utilisés par la méthode get_id.
        """

        # Assignation des chemins de gestion des identifiants.
        self.unused_path = unused_path
        self.used_path = used_path
        self.maximum_path = maximum_path

        return True

    # Déclaration de la signature de la méthode get_id.
    def get_id(self) -> int:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            new_id (int) :
                Description : Un identifiant temporaire unique disponible.

        Rôle :
            Génère et retourne un identifiant temporaire unique, en
            réutilisant un identifiant non utilisé si disponible, ou en
            en créant un nouveau en incrémentant le maximum actuel. L'
            identifiant est ajouté à la liste des identifiants utilisés.
        """

        # Récupération des listes d'identifiants et du maximum actuel.
        unused = self.data.get(self.unused_path)
        used = self.data.get(self.used_path)
        maximum = self.data.get(self.maximum_path)

        # Réutilisation d'un identifiant non utilisé si disponible,
        # sinon création d'un nouvel identifiant.
        if unused:
            new_id = min(unused)
            unused.remove(new_id)
            if maximum < new_id:
                self.data.write(maximum, new_id)
        else:
            new_id = maximum + 1
            self.data.write(self.maximum_path, new_id)

        # Ajout de l'identifiant à la liste des identifiants utilisés.
        used.append(new_id)

        # Retourne le nouvel identifiant.
        return new_id

    # Déclaration de la signature de la méthode free_id.
    def free_id(
        self,
        id: int
    ) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            id (int) :
                Description : L'identifiant temporaire à libérer.

        Sortie :
            result (bool) :
                Description : True si la libération a réussi.

        Rôle :
            Libère un identifiant temporaire en le retirant de la liste
            des identifiants utilisés, et met à jour le maximum si
            nécessaire.
        """

        # Retrait de l'identifiant de la liste des identifiants utilisés.
        used = self.data.get(self.used_path)
        used.remove(id)

        # Mise à jour du maximum si l'identifiant libéré était le maximum.
        maximum = self.data.get(self.maximum_path)
        if maximum == id:
            self.data.write(self.maximum_path, max(used))

        return True