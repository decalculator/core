# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : installator.py
# Rôle    : Ce fichier implémente la classe Installator, qui est utile
#           pour installer et désinstaller des objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Installator.
import asyncio
from zipfile import ZipFile

from core.modules.path.path import *
from core.modules.json.json import *

# Définition de la classe Installator.
class Installator:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        temp: Temp,
        communication: Communication,
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
            temp (Temp) :
                Description : L'objet Temp parent.

            communication (Communication) :
                Description : L'objet Communication parent.

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
            Il s'agit de la méthode d'initialisation de la classe Installator,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation de l'USOI de l'objet courant.
        self.usoi = 22

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
        self.temp = temp

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        self.filesystem = filesystem
        self.communication = communication

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

    # Déclaration de la signature de la méthode install.
    async def install(
        self,
        args: list,
        extracted_path: Path | None = None
    ) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrées :
            args (list) :
                Description : La liste des arguments de l'installation,
                    contenant dans l'ordre : le mode d'installation
                    (0 pour en ligne, 1 pour local), le type d'objet,
                    le numéro, et le chemin.

            extracted_path (Path | None) :
                Description : Le chemin d'extraction personnalisé. Si None,
                    un chemin temporaire est généré automatiquement.
                Valeur par défaut : None.

        Sortie :
            installed (bool) :
                Description : True si l'installation a réussi, False sinon.

        Rôle :
            Installe un objet depuis une source en ligne ou locale, en
            téléchargeant et extrayant l'archive, puis en déplaçant les
            fichiers vers leur emplacement final et en mettant à jour la
            configuration commune.
        """

        # 0 : en ligne
        # 1 : local

        # Extraction des arguments.
        mode = args[0]
        object_type = args[1]
        number = args[2]
        path = args[3]

        # Génération d'un identifiant temporaire.
        temp_id = self.temp.get_id()

        # Conversion du type d'objet en entier si nécessaire.
        if isinstance(object_type, str):
            objects_types = {"modules": 0, "plugins": 1, "objects": 2, "repos": 3}

            if object_type in objects_types:
                object_type = objects_types[object_type]

        # Installation depuis une source en ligne.
        if mode == 0:
            response = self.communication.get(url = path, mode = 1)

            if "content" in response:
                temp_path = Path(f"data/plugins/communication/{temp_id}.zip", mode = 1)

                # Définition du chemin d'extraction temporaire.
                if extracted_path is None:
                    temp_extracted_path = Path(f"data/plugins/communication/{temp_id}", mode = 1)

                else:
                    temp_extracted_path = extracted_path

                # Définition du chemin de base et de la configuration
                # commune selon le type d'objet.
                if object_type == 0:
                    object_base_path = Path("sources/core/modules", mode = 1)
                    common_config_path = Path(f"{object_base_path.path}/modules.json", mode = 1)

                elif object_type == 1:
                    object_base_path = Path("sources/core/plugins", mode = 1)
                    common_config_path = Path(f"{object_base_path.path}/plugins.json", mode = 1)

                elif object_type == 2:
                    object_base_path = Path("sources/core/objects", mode = 1)
                    common_config_path = Path(f"{object_base_path.path}/objects.json", mode = 1)

                elif object_type == 3:
                    object_base_path = Path("source/core/repos", mode = 1)

                # Écriture du contenu téléchargé dans le fichier temporaire.
                with open(temp_path.os_path, "wb") as file:
                    file.write(response["content"])

                # Extraction de l'archive dans le chemin temporaire.
                if extracted_path is None:
                    with ZipFile(temp_path.os_path, "r") as obj:
                        obj.extractall(temp_extracted_path.os_path)

                # Récupération du chemin de l'objet extrait.
                ls = self.filesystem.ls(temp_extracted_path, mode = 1)
                object_path = Path(f"{temp_extracted_path.path}/{ls[0]}", mode = 1)

                # Lecture de la configuration de l'objet et déplacement
                # vers son emplacement final.
                if "config.json" in self.filesystem.ls(object_path):
                    config_path = Path(f"{object_path.path}/config.json", mode = 1)
                    content = await self.filesystem.read(config_path, 2)

                    if "path" in content:
                        if "name" in content:
                            object_name = content["name"]
                            _in = Path(f"{object_path.path}/{content['path']}", mode = 1)
                            _out = Path(f"{object_base_path.path}/{object_name}", mode = 1)

                            await self.filesystem.mv(_in, _out)

                            # Mise à jour de la configuration commune.
                            if object_type in [0, 1, 2]:
                                common_config = await self.filesystem.read(common_config_path, 2)
                                common_config[object_name] = {"enabled": True}

                                await self.filesystem.write(common_config_path, json.dumps(common_config))

                # Suppression des fichiers temporaires.
                await self.filesystem.rm(temp_path)
                self.filesystem.rmdir(temp_extracted_path)

        # Installation depuis une source locale.
        elif mode == 1:

            # Définition du chemin d'extraction temporaire.
            if extracted_path is None:
                temp_extracted_path = Path(f"data/plugins/communication/{temp_id}", mode = 1)
            else:
                temp_extracted_path = extracted_path

            # Définition du chemin de base et de la configuration
            # commune selon le type d'objet.
            if object_type == 0:
                object_base_path = Path("sources/core/modules", mode = 1)
                common_config_path = Path(f"{object_base_path.path}/modules.json", mode = 1)

            elif object_type == 1:
                object_base_path = Path("sources/core/plugins", mode = 1)
                common_config_path = Path(f"{object_base_path.path}/plugins.json", mode = 1)

            elif object_type == 2:
                object_base_path = Path("sources/core/objects", mode = 1)
                common_config_path = Path(f"{object_base_path.path}/objects.json", mode = 1)

            elif object_type == 3:
                object_base_path = Path("data/repos", mode = 1)
                common_config_path = Path(f"{object_base_path.path}/repos.json", mode = 1)

            # Extraction de l'archive dans le chemin temporaire.
            if extracted_path is None:
                with ZipFile(path.os_path, "r") as obj:
                    obj.extractall(temp_extracted_path.os_path)

            # Récupération du chemin de l'objet extrait.
            ls = self.filesystem.ls(temp_extracted_path, mode = 1)
            object_path = Path(f"{temp_extracted_path.path}/{ls[0]}", mode = 1)

            # Lecture de la configuration de l'objet et déplacement
            # vers son emplacement final.
            if "config.json" in self.filesystem.ls(object_path):
                config_path = Path(f"{object_path.path}/config.json", mode = 1)
                content = await self.filesystem.read(config_path, 2)

                if "path" in content:
                    if "name" in content:
                        object_name = content["name"]
                        _in = Path(f"{object_path.path}/{content['path']}", mode = 1)
                        _out = Path(f"{object_base_path.path}/{object_name}", mode = 1)

                        await self.filesystem.mv(_in, _out)

                        # Mise à jour de la configuration commune.
                        if object_type in [0, 1, 2]:
                            common_config = await self.filesystem.read(common_config_path, 2)
                            common_config[object_name] = {"enabled": True}

                            await self.filesystem.write(common_config_path, json.dumps(common_config))

            # Suppression du répertoire temporaire.
            self.filesystem.rmdir(temp_extracted_path)

    # Déclaration de la signature de la méthode is_alreay_installed.
    async def is_alreay_installed(
        self,
        args
    ):
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            args (list) :
                Description : La liste des arguments, contenant dans l'ordre
                    le nom de l'objet et son type.

        Sortie :
            installed (bool) :
                Description : True si l'objet est déjà installé,
                    False sinon.

        Rôle :
            Vérifie si un objet est déjà installé en consultant la
            configuration commune correspondant à son type.
        """

        # Extraction des arguments.
        object_name = args[0]
        object_type = args[1]

        # Lecture de la configuration commune et vérification de la présence
        # de l'objet.
        objects_types = {0: "modules", 1: "plugins", 2: "objects", 3: "repos"}
        config = Path(f"sources/core/{objects_types[object_type]}/{objects_types[object_type]}.json", mode = 1)
        content = await self.filesystem.read(config, 2)

        return object_name in content

    # Déclaration de la signature de la méthode get_free_path.
    def get_free_path(self):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            path (Path) :
                Description : Un chemin temporaire libre dans le répertoire
                    de communication.

        Rôle :
            Génère et retourne un chemin temporaire libre, basé sur un
            identifiant unique fourni par l'objet Temp.
        """

        # Retourne un chemin temporaire libre.
        return Path(f"data/plugins/communication/{self.temp.get_id()}", mode = 1)

    # Déclaration de la signature de la méthode extract_object.
    def extract_object(
        self,
        args
    ):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            args (list) :
                Description : La liste des arguments, contenant dans l'ordre
                    le type de l'objet et le chemin de l'archive à extraire.

        Sortie :
            output_path (Path) :
                Description : Le chemin du répertoire dans lequel l'archive
                    a été extraite.

        Rôle :
            Extrait une archive ZIP vers un chemin temporaire libre, et
            retourne le chemin d'extraction.
        """

        # Extraction des arguments.
        object_type = args[0]
        object_path = args[1]
        output_path = self.get_free_path()

        # Extraction de l'archive vers le chemin de sortie.
        with ZipFile(object_path.os_path, "r") as obj:
            obj.extractall(output_path.os_path)

        # Retourne le chemin d'extraction.
        return output_path

    # Déclaration de la signature de la méthode get_object_name.
    async def get_object_name(
        self,
        path
    ):
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            path (Path) :
                Description : Le chemin du répertoire contenant l'objet
                    extrait.

        Sortie :
            result (str | None) :
                Description : Le nom de l'objet lu dans sa configuration,
                    ou None si la configuration est introuvable ou ne
                    contient pas de nom.

        Rôle :
            Récupère le nom d'un objet extrait en lisant son fichier de
            configuration.
        """

        # Initialisation du résultat.
        result = None

        # Récupération du chemin de l'objet extrait.
        ls = self.filesystem.ls(path)
        object_path = Path(f"{path.path}/{ls[0]}", mode = 1)

        # Lecture de la configuration de l'objet et extraction du nom.
        if "config.json" in self.filesystem.ls(object_path):
            config_path = Path(f"{object_path.path}/config.json", mode = 1)
            content = await self.filesystem.read(config_path, mode = 2)

            if "name" in content:
                result = content["name"]

        # Retourne le nom de l'objet.
        return result

    # Déclaration de la signature de la méthode uninstall.
    async def uninstall(
        self,
        args
    ):
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            args (list) :
                Description : La liste des arguments, contenant dans l'ordre
                    le nom de l'objet et son type.

        Sortie :
            None

        Rôle :
            Désinstalle un objet en supprimant son répertoire et en le
            retirant de la configuration commune correspondant à son type.
            Les étapes de la désinstallation sont consignées dans les logs.
        """

        # Initialisation des logs et du résultat.
        logs = []
        result = 1

        # Extraction des arguments.
        object_name = args[0]
        object_type = args[1]

        # Conversion du type d'objet en chaîne de caractères.
        object_types = {0: "modules", 1: "plugins", 2: "objects", 3: "repos"}
        object_type = object_types[object_type]

        logs.append(f"name : {object_name}, type : {object_type}")

        # Définition des chemins de configuration et de l'objet.
        config_path = Path(f"sources/core/{object_type}/{object_type}.json", mode = 1)
        object_path = Path(f"sources/core/{object_type}/{object_name}", mode = 1)

        # Suppression du répertoire de l'objet s'il existe.
        if await self.filesystem.exists(object_path):
            logs.append(f"{object_path.os_path} exists")

            logs.append(f"removing {object_path.os_path}")
            self.filesystem.rmdir(object_path)
        else:
            logs.append(f"{object_path.os_path} dont exists ?")
            result = 0

        # Suppression de l'objet dans la configuration commune.
        logs.append(f"removing object from {config_path.os_path}")
        content = await self.filesystem.read(config_path, 2)

        if object_name in content:
            logs.append("object found")
            del content[object_name]

            logs.append(f"writing new config to {config_path.os_path}")
            await self.filesystem.write(config_path, json.dumps(content))

        else:
            logs.append("object not found ?")
            result = 0

        # Consignation du résultat de la désinstallation.
        if result == 1:
            logs.append("uninstallation : sucess")
        elif result == 0:
            logs.append("uninstallation : fail")

        # Construction du payload de logs.
        payload = ""
        size = len(logs)

        for i in range(size):
            temp = logs[i]
            if i != size - 1:
                temp += "\n"

            payload += temp