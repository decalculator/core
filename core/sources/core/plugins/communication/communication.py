# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : communication.py
# Rôle    : Ce fichier implémente la classe Communication, qui est utile
#           pour effectuer des requêtes HTTP et des opérations Git.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Communication.
import asyncio
import requests
from git import Repo

from core.modules.path.path import *
from core.modules.json.json import *


# Définition de la classe Communication.
class Communication:

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
            Il s'agit de la méthode d'initialisation de la classe
            Communication, elle assigne aux attributs leurs valeurs, et
            s'écrit correctement comme instance dans la mémoire parente,
            ainsi que dans le gestionnaire de PIDs.
        """

        # Initialisation de l'USOI de l'objet courant.
        self.usoi = 20

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
        return self.data.write(path, value, mode = mode)

    # Déclaration de la signature de la méthode remove.
    def remove(self, path: Path) -> bool:
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

    # Déclaration de la signature de la méthode _get.
    def _get(self, path: Path):
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

    # Déclaration de la signature de la méthode get.
    def get(self, url: str, mode: int = 0):
        """
        Type de méthode :
            Synchrone.

        Entrées :
            url (str) :
                Description : L'URL cible de la requête HTTP GET.

            mode (int) :
                Description : Le mode de récupération du contenu de la
                    réponse. 0 pour le texte, 1 pour le contenu binaire.
                Valeur par défaut : 0.

        Sortie :
            result (dict) :
                Description : Un dictionnaire contenant le statut de la
                    requête, le contenu de la réponse, et le mode de
                    récupération utilisé.

        Rôle :
            Effectue une requête HTTP GET à l'URL donnée, et retourne
            le résultat sous forme de dictionnaire.
        """

        # Initialisation du dictionnaire de résultat.
        result = {}

        # Tentative d'envoi de la requête HTTP GET.
        try:
            response = requests.get(url)
            status = 1
        except:
            response = None
            status = 0

        # Assignation du statut de la requête dans le résultat.
        result["status"] = status

        # Si une réponse a été reçue, nous en extrayons le contenu.
        if response:
            try:
                response_content = response.json()
                response_mode = 1
            except:
                if mode == 0:
                    response_content = response.text
                elif mode == 1:
                    response_content = response.content
                response_mode = 0

            result["content"] = response_content
            result["mode"] = response_mode

        # Retourne le résultat.
        return result

    # Déclaration de la signature de la méthode exists.
    def exists(self, path: Path):
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

    # Déclaration de la signature de la méthode git_clone.
    def git_clone(self, url, folder):
        """
        Type de méthode :
            Synchrone.

        Entrées :
            url (str) :
                Description : L'URL du dépôt Git à cloner.

            folder (str) :
                Description : Le chemin du dossier de destination du clone.

        Sortie :
            None

        Rôle :
            Clone un dépôt Git depuis l'URL donnée vers le dossier
            de destination.
        """

        # Clone le dépôt Git depuis l'URL donnée.
        Repo.clone_from(url, folder)