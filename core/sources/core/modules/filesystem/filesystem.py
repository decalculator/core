# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : filesystem.py
# Rôle    : Ce fichier implémente la classe Filesystem, qui est utile
#           pour travailler avec le système de fichiers exécutant core.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Filesystem.
import asyncio
import aiofiles, aiofiles.os
import shutil
from pathlib import Path as _path

from core.modules.path.path import *
from core.modules.json.json import *

# Définition de la classe Filesystem.
class Filesystem:

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
        Type de méthode :
            Synchrone.

        Entrées :
            memory (Memory | None) :
                Description : L'objet de mémoire parent.
                Valeur par défaut : None.

            pid_manager (PidManager | None) :
                Description : L'objet gestionnaire de PIDs parent.
                Valeur par défaut : None.

            logs (Logs | None) :
                Description : L'objet de logs parent.
                Valeur par défaut : None.

            pid (DynamicValue | None) :
                Description : Le PID de l'objet.
                Valeur par défaut : None.

            ppid (DynamicValue | None) :
                Description : Le PID de l'objet parent.
                Valeur par défaut : None.

            content (Json | None) :
                Description : Le contenu à initialiser pour l'attribut data.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode asynchrone d'initialisation de la classe
            Filesystem, elle assigne aux attributs leurs valeurs, et
            s'écrit correctement comme instance dans la mémoire parente,
            ainsi que dans le gestionnaire de PIDs.
        """

        # Déclaration de l'USOI
        self.usoi = 4

        # Initialisation (ou assignation) de l'attribut data.
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content)
                initialized = True

        if not initialized:
            self.data = Json()
            initialized = True

        # Initialisation du PPID.
        self.ppid = ppid

        # Initialisation du PID.
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Assignation des attributs de mémoire, de logs, et PID.
        self.memory = memory
        self.logs = logs
        self.pid = pid

        # Ecriture de l'objet courant dans la mémoire, si celle-ci et
        # son PID sont disponibles.
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

    # Déclaration de la signature de la méthode mkdir.
    async def mkdir(self, path: Path) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            path (Path) :
                Description :
                    Le chemin du répertoire à créer.

        Sortie :
            result (bool) :
                Description :
                    True si la création a réussi, False sinon.

        Rôle :
            Crée un répertoire au chemin donné.
        """

        # Initialisation du résultat sur False.
        result = False

        # Si l'objet path a bien l'attribut os_path, que l'on obtient
        # avec mode = 1 à l'__init__ du Path.
        if hasattr(path, "os_path"):
            # Nous essayons de créer le dossier au path correspondant.
            # Si cela semble fonctionner, nous assignons True au résultat.
            try:
                await aiofiles.os.mkdir(path.os_path)
                result = True

            # Sinon, nous ne faisons rien pour le moment,
            # le résultat restera False.
            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode write.
    async def write(self, path: Path, value) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description :
                    Le chemin d'écriture.

            value (any) :
                Description :
                    La valeur à écrire.

            mode (int) :
                Description :
                    Le mode d'écriture.
                Valeur par défaut : 0.

        Sortie :
            bool :
                Description :
                    True si l'écriture a réussi, False sinon.

        Rôle :
            Écrit une valeur à un chemin donné.
        """

        # Initialisation du résultat sur False.
        result = False

        # Si l'objet path est bien de l'instance Path, et qu'il a bien un
        # attribut os_path.
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous essayons d'écrire le contenu au path.
            # Si cela semble fonctionner, nous assignons True au résultat.
            try:
                async with aiofiles.open(path.os_path, "w") as file:
                    await file.write(value)
                    result = True

            # Sinon, nous ne faisons rien pour le moment,
            # le résultat restera False.
            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode read.
    async def read(self, path: Path, mode: int = 0):
        """
        Type de méthode :
            Asynchrone.

        Entrées :
            path (Path) :
                Description : Le chemin de la valeur à lire.

            mode (int) :
                Description : Le mode de lecture.
                Valeur par défaut : 0.

        Sortie :
            result (any) :
                Description :
                    La valeur située au chemin donné.

        Rôle :
            Lit la valeur située au chemin donné.
        """

        # Nous initialisons le résultat sur None.
        result = None

        # Si c'est un Path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous essayons de lire son contenu.
            try:
                async with aiofiles.open(path.os_path, "r") as file:
                    # Si le mode est 0, alors nous renverrons le contenu en str.
                    if mode == 0:
                        result = await file.read()

                    # Si le mode est 1, nous renverrons le contenu en list[str].
                    elif mode == 1:
                        result = await file.readlines()

                    # Si le mode est 2, nous renverrons le contenu en JSON.
                    elif mode == 2:
                        result = json.loads(await file.read())

            # Si ça ne fonctionne pas, le résultat restera sur None.
            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode exists.
    async def exists(self, path: Path) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            path (Path) :
                Description :
                    Le chemin à vérifier.

        Sortie :
            result (bool) :
                Description :
                    True si le chemin existe, False sinon.

        Rôle :
            Vérifie si un chemin donné existe.
        """

        # Nous initialisons le résultat sur False.
        result = False

        # Si c'est un Path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous esseyons de vérifier si le path existe.
            # Si cela fonctionne, le booléen prendra pour valeur True.
            try:
                result = await aiofiles.os.path.exists(path.os_path)

            # Sinon, le résultat restera False.
            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode is_dir.
    async def is_dir(self, path: Path) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            path (Path) :
                Description :
                    Le chemin à vérifier.

        Sortie :
            result (bool) :
                Description :
                    True si le chemin correspond à un répertoire.

        Rôle :
            Vérifie si un chemin donné correspond à un répertoire.
        """

        # Nous initialisons le résultat sur False.
        result = False

        # Si c'est un Path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous esseyons de vérifier si le path est un dossier.
            # Si cela fonctionne, le booléen prendra pour valeur True.
            try:
                result = await aiofiles.os.path.isdir(path.os_path)

            # Sinon, le résultat restera False.
            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode mv.
    async def mv(self, in_path: Path, out_path: Path, overwrite: bool = False) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrées :
            in_path (Path) :
                Description :
                    Le chemin source du dossier à déplacer.

            out_path (Path) :
                Description :
                    Le chemin de destination du dossier à déplacer.

            overwrite (bool) :
                Description :
                    Si True, écrase le dossier de destination
                    s'il existe déjà.
                Valeur par défaut : False.

        Sortie :
            moved (bool) :
                Description :
                    True si le déplacement a réussi, False sinon.

        Rôle :
            Déplace un dossier d'un chemin source vers un chemin de
            destination dans le filesystem.
        """

        # Nous initialisons le résultat sur False.
        result = False

        # Si les deux paths sont valides (matériels).
        if hasattr(in_path, "usoi") and in_path.usoi == 8 and hasattr(in_path, "os_path"):
            if hasattr(out_path, "usoi") and out_path.usoi == 8 and hasattr(out_path, "os_path"):
                # Nous initialisons un booléen sur True.
                state = True

                # Si le path de desination existe, et que l'option
                # overwrite vaut True, nous le supprimons.
                if await self.exists(out_path):
                    state = False
                    if overwrite:
                        if await self.rmdir(out_path):
                            state = True

                # Si l'état booléen vaut True, c'est à dire que nous sommes
                # prêts pour la copie.
                if state:
                    # Nous effectuons le mv grâce à la fonction rename de
                    # pathlib.

                    try:
                        _path(in_path.os_path).rename(out_path.os_path)
                        # Le résultat vaut True.
                        result = True

                    except:
                        pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode rmdir.
    def rmdir(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description :
                    Le chemin du répertoire à supprimer.

        Sortie :
            result (bool) :
                Description :
                    True si la suppression a réussi, False sinon.

        Rôle :
            Supprime un répertoire au chemin donné dans le filesystem.
        """

        # Nous initialisons le résultat sur False.
        result = False

        # Si c'est un Path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous tentons de supprimer le dossier, avec shutil.rmtree.
            try:
                shutil.rmtree(path.os_path)
                result = True

            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode rm.
    async def rm(self, path: Path) -> bool:
        """
        Type de méthode :
            Asynchrone.

        Entrée :
            path (Path) :
                Description :
                    Le chemin du fichier à supprimer.

        Sortie :
            result (bool) :
                Description :
                    True si la suppression a réussi, False sinon.

        Rôle :
            Supprime un fichier au chemin donné dans le filesystem.
        """

        # Nous initialisons le résultat sur False.
        result = False

        # Si c'est un Path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):

            # Nous tentons de supprimer le fichier.
            try:
                await aiofiles.os.remove(path.os_path)
                result = True

            except:
                pass

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode ls.
    def ls(self, path: Path, exclude: list[str] | None = None, mode: int = 0) -> list[str]:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description :
                    Le chemin du répertoire à lister.

            exclude (list[str] | None) :
                Description :
                    La liste des éléments à exclure du résultat.
                Valeur par défaut : None.

            mode (int) :
                Description :
                    Le mode de listage.
                    0 : dossiers et fichiers.
                    1 : dossiers.
                    2 : fichiers.
                Valeur par défaut : 0.

        Sortie :
            entries (list[str]) :
                Description :
                    La liste des éléments présents au chemin donné.

        Rôle :
            Liste les éléments présents au chemin donné dans le filesystem.
        """

        # Initialisation d'une liste vide qui contiendra le résultat.
        result = []

        # Si c'est un path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):
            # Nous obtenons son path (str).
            path = path.path

            # Si le mode est 0, nous ajoutons tous les dossiers et fichiers
            # (sauf liste d'exclusion).
            if mode == 0:
                if exclude:
                    for element in os.listdir(path):
                        if element not in exclude:
                            result.append(element)
                else:
                    result = os.listdir(path)

            # Si le mode est 1, nous ajoutons tous les dossiers (sauf liste
            # d'exclusion).
            elif mode == 1:
                for element in os.listdir(path):
                    if exclude:
                        if element not in exclude and not os.path.isfile(os.path.join(path, element)):
                            result.append(element)
                    else:
                        if not os.path.isfile(os.path.join(path, element)):
                            result.append(element)

            # Si le mode est 2, nous ajoutons tous les fichiers (sauf liste
            # d'exclusion).
            elif mode == 2:
                for element in os.listdir(path):
                    if exclude:
                        if element not in exclude and os.path.isfile(os.path.join(path, element)):
                            result.append(element)
                    else:
                        if os.path.isfile(os.path.join(path, element)):
                            result.append(element)

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode subfiles.
    def subfiles(self, path: Path, separator: str = '/') -> list[Path]:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description :
                    Le chemin du répertoire dont les sous-fichiers
                    sont à récupérer.

            separator (str) :
                Description :
                    Le séparateur utilisé pour construire les
                    chemins des sous-fichiers.
                Valeur par défaut : '/'.

        Sortie :
            subfiles (list[Path]) :
                Description : La liste des chemins de tous les sous-fichiers
                    présents au chemin donné.

        Rôle :
            Récupère récursivement la liste des chemins de tous les
            sous-fichiers présents au chemin donné.
        """

        # https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
        # je me suis aidé d'internet pour des raisons de performances, voici ce que j'allais faire :
        # une fonction récursive qui fonctionne avec ls pour chaque dossier / sous-dossier
        # c'est globalement ce que l'on fait, mais c'est plus simple ici

        # Initialisation du résultat.
        subfiles = []

        # Si c'est un path valide (matériel).
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "os_path"):
            # Nous obtenons son path matériel.
            path = path.os_path

            # 
            for root, dirs, files in os.walk(path):
                for name in files:
                    if '\\' in root:
                        root = self.windows_path_to_normal(root)

                    subfiles.append(Path(root + separator + name, mode = 1))

        return subfiles

    def windows_path_to_normal(self, path: str) -> str:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (str) :
                Description :
                    Le chemin Windows à convertir.

        Sortie :
            path (str) :
                Description :
                    Le chemin converti au format Unix, avec les
                    séparateurs '\\' remplacés par '/'.

        Rôle :
            Convertit un chemin Windows en chemin Unix en remplaçant les
            séparateurs '\\' par '/'.
        """

        splitted = path.split('\\')
        result = ""

        for i in range(len(splitted)):
            if i == 0:
                result += splitted[i]
            else:
                result += f"/{splitted[i]}"

        return result