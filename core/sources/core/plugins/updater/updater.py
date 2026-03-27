# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : updater.py
# Rôle    : Ce fichier implémente la classe Updater, qui est utile
#           pour la gestion des mises à jour.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Updater.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *
from core.plugins.communication.communication import *


# Définition de la classe Updater.
class Updater:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        filesystem: Filesystem,
        settings: Settings,
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

            settings (Settings) :
                Description : L'objet Settings parent.

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
            Il s'agit de la méthode d'initialisation de la classe Updater,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation de l'USOI de l'objet courant.
        self.usoi = 28

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
        self.settings = settings

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

    # Déclaration de la signature de la méthode get_latest_version_number.
    def get_latest_version_number(self) -> float | None:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            result (float | None) :
                Description : Le numéro de la dernière version disponible,
                    ou None si la récupération a échoué.

        Rôle :
            Récupère le numéro de la dernière version disponible en
            interrogeant l'URL de configuration du dépôt distant.
        """

        # Initialisation du résultat.
        result = None

        # Création d'un objet Communication et récupération de l'URL
        # de configuration du dépôt.
        communication = Communication(filesystem = self.filesystem)
        url = self.settings.get(Path("repo_config_url"))
        response = communication.get(url)

        # Extraction du numéro de version depuis la réponse.
        if "content" in response:
            if "mode" in response and response["mode"] == 1:
                if "<version>" in response["content"]:
                    result = response["content"]["<version>"]

                    # Conversion du numéro de version en float si nécessaire.
                    if isinstance(result, str):
                        result = float(result)

        # Retourne le numéro de version.
        return result

    # Déclaration de la signature de la méthode update.
    def update(self):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            None

        Rôle :
            Lance la mise à jour en clonant le dépôt distant vers un
            répertoire local.
        """

        # il faudra bien penser à reset le json de communication

        # Création d'un objet Communication et récupération de l'URL
        # du dépôt distant.
        communication = Communication(filesystem = self.filesystem)
        url = self.settings.get(Path("repo_url"))
        out_path = Path("_core", mode = 1)

        # Clonage du dépôt distant vers le répertoire local.
        communication.git_clone(url, out_path.os_path)

        # à compléter
        # ...