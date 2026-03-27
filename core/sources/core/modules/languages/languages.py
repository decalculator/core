# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : languages.py
# Rôle    : Ce fichier implémente la classe Languages, qui est utile
#           pour la gestion de langues.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Languages.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *

# Définition de la classe Languages.
class Languages:

    # Déclaration de la signature de la méthode __init__.
    def __init__(self) -> None:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe Languages,
            elle assigne aux attributs None.
        """

        # Initialisation et assignation des attributs.
        self.usoi = 6
        self.memory = None
        self.logs = None
        self.pid = None
        self.ppid = None

        self.filesystem = None
        self.settings = None
        self.selected = None

        self.data = None
        self.languages_config_content = None
        self.variable_pattern = None

    # Déclaration de la signature de la méthode init.
    async def init(
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
            Asynchrone.

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
            Il s'agit de la méthode asynchrone d'initialisation de la classe
            Languages, elle assigne aux attributs leurs valeurs, et s'écrit
            correctement comme instance dans la mémoire parente, ainsi que
            dans le gestionnaire de PIDs.
        """

        # Initialisation et assignation des attributs.
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.filesystem = filesystem
        self.settings = settings

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

        # Chargement du fichier de langues.
        if hasattr(self.filesystem, "usoi"):
            if self.filesystem.usoi == 4:
                if hasattr(self.settings, "usoi"):
                    if self.settings.usoi == 9:
                        languages_data_path = Path(self.settings.get(Path("modules_data_folder_path")), mode = 1)
                        languages_config = languages_data_path + "languages/languages.json"
                        content = await self.filesystem.read(languages_config, mode = 2)

                self.languages_config_content = content

        # Nous renvoyons le PID.
        return self.pid

    async def load_language(self, name):
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            name (str) :
                Description : Le nom de la langue à charger.

        Sortie :
            None

        Rôle :
            Charge une langue dans l'objet courant en lisant sa configuration
            depuis le filesystem, puis en écrivant son contenu dans la
            structure de données interne. Si la langue est déjà chargée,
            ou si sa configuration est introuvable, la méthode ne fait rien.
        """

        languages_config_content = self.languages_config_content
        languages_config_content_obj = Json(content = languages_config_content)
        language_configuration_path = Path(f"languages/{name}/configuration")
        if languages_config_content_obj.exists(language_configuration_path):
            language_config_file = Path(languages_config_content_obj.get(language_configuration_path), mode = 1)

            if not self.data.exists(Path(name)):
                content = await self.filesystem.read(language_config_file, mode = 2)
                self.data.write(Path(name), {})

                for segment, value in content.items():
                    if "path" in value:
                        content_path = await self.filesystem.read(Path(value["path"], mode = 1), mode = 2)
                        self.data.write(Path(f"{name}/{segment}"), content_path)

    def select(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la langue à sélectionner.

        Sortie :
            None

        Rôle :
            Sélectionne une langue en assignant son chemin à l'attribut
            selected de l'objet courant.
        """

        self.selected = path

    def get_from_selected(self, path: Path):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à récupérer, relatif
                    à la langue sélectionnée.

        Sortie :
            value (any) :
                Description : La valeur située au chemin donné, dans la
                    langue sélectionnée.

        Rôle :
            Récupère une valeur à un chemin donné, relatif à la langue
            sélectionnée dans l'objet courant.
        """

        return self.data.get(self.selected / path.path)

    def get_selected(self) -> Path:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            selected (Path) :
                Description : Le chemin de la langue actuellement
                    sélectionnée.

        Rôle :
            Renvoie le chemin de la langue actuellement sélectionnée dans
            l'objet courant.
        """

        return self.selected

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