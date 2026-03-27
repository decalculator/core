# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : json.py
# Rôle    : Ce fichier implémente la classe Json, qui est utile
#           pour travailler avec des données structurées.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Json.
import asyncio
import json
import aiofiles

from core.modules.path.path import *

# Définition de la classe Json.
class Json:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        memory: Memory | None = None,
        logs: Logs | None = None,
        pid_manager: PidManager | None = None,
        pid: Pid | None = None,
        content: dict | None = None,
        ppid: DynamicValue | None = None,
        references_manager: ReferencesManager | None = None
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            memory (Memory | None) :
                Description :
                    L'objet Memory parent.
                Valeur par défaut : None.

            logs (Logs | None) :
                Description :
                    L'objet Logs parent.
                Valeur par défaut : None.

            pid_manager (PidManager | None) :
                Description :
                    L'objet PidManager parent.
                Valeur par défaut : None.

            pid (Pid | None) :
                Description :
                    Le PID de l'objet.
                Valeur par défaut : None.

            content (dict | None) :
                Description :
                    Le contenu JSON de l'objet.
                Valeur par défaut : None.

            ppid (DynamicValue | None) :
                Description :
                    Le PID de l'objet parent.
                Valeur par défaut : None.

            references_manager (ReferencesManager | None) :
                Description :
                    L'objet ReferencesManager parent.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe Json,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation et assignation des attributs.
        self.usoi = 5
        self.references_manager = references_manager
        self.pid_manager = pid_manager
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid

        # Initialisation de l'attribut data.

        initialized = False
        if isinstance(content, dict):
            self.data = content
            initialized = True

        if not initialized:
            self.data = {}
            initialized = True

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if self.pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    self.pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Si l'attribut PPID n'est pas None, et que le gestionnaire de
        # références n'est pas None, nous ajoutons une référence de PPID
        # vers PID, et idem pour PPID vers :
        # references_manager, memory, logs, pid_manager.

        if self.ppid is not None:
            if self.references_manager is not None:
                self.references_manager.add_reference(self.ppid.data, self.pid.data)
                self.references_manager.add_reference(self.ppid.data, self.references_manager)

                if self.memory is not None:
                    self.references_manager.add_reference(self.ppid.data, self.memory.pid.data)

                if self.logs is not None:
                    self.references_manager.add_reference(self.ppid.data, self.logs.pid.data)

                if self.pid_manager is not None:
                    self.references_manager.add_reference(self.ppid.data, self.pid_manager.pid.data)

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
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
                Description : True si l'écriture a réussi, False sinon.

        Rôle :
            Écrit une valeur à un chemin donné dans l'objet courant.
        """

        # Initialisation du résultat sur None.
        result = False

        # Si le path est valide, et qu'il contient un attribut splitted_path.
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "splitted_path"):
            # Nous initialisons un compteur i à 0, et une variable
            # done à False pour la boucle while.

            i = 0
            done = False

            # La variable temp prend une référence vers l'attribut data.
            temp = self.data
            # Size contient le nombre d'étapes pour arriver à l'écriture.
            size = len(path.splitted_path)

            # Tant que i ne dépasse pas la taille du chemin, et que done
            # vaut False.
            while i < size and not done:
                # Nous obtenons l'élément à l'indice i.
                element = path.splitted_path[i]

                # Si c'est le dernier élément.
                if i == size - 1:
                    # Nous écrivons pour la clef element la valeur value.
                    temp[element] = value
                    # Nous quittons la boucle (avant d'avoir à faire i++)
                    result = True

                # Si ce n'est pas le dernier élément.
                else:
                    # Si l'élément actuel est dans temp (prochaine étape
                    # présente), temp prend la valeur à cette clef
                    # (nous avançons).
                    if element in temp:
                        temp = temp[element]

                    # Sinon, si mode vaut 1, nous procédons à la création
                    # d'un dict à cette clef.
                    elif mode == 1:
                        temp[element] = {}
                        temp = temp[element]

                    # Sinon, nous quittons la boucle.
                    else:
                        done = True

                # Incrémentation de 1 pour i.
                i += 1

        # Nous retournons le résultat.
        return result

    # Déclaration de la signature de la méthode remove.
    def remove(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à supprimer.

        Sortie :
            bool :
                Description : True si la suppression a réussi, False sinon.

        Rôle :
            Supprime la valeur située au chemin donné dans l'objet courant.
        """

        # Initialisation du résultat sur False.
        result = False

        # Si le path est valide, et qu'il contient un attribut splitted_path.
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "splitted_path"):
            # Nous initialisons un compteur i à 0, et une variable
            # done à False pour la boucle while.

            i = 0
            done = False

            # La variable temp prend une référence vers l'attribut data.
            temp = self.data
            # Size contient le nombre d'étapes pour arriver à l'écriture.
            size = len(path.splitted_path)

            # Tant que i ne dépasse pas la taille du chemin, et que done
            # vaut False.
            while i < size and not done:
                # Nous obtenons l'élément actuel.
                element = path.splitted_path[i]

                # Si c'est le dernier élément.
                if i == size - 1:
                    # Si l'élément est dans temp, et que temp est un dict,
                    # nous supprimons la référence qui pointe vers l'élément.
                    # Et nous quittons la boucle.

                    if element in temp:
                        if isinstance(temp, dict):
                            del temp[element]
                            result = True

                # Si ce n'est pas le dernier élément.
                else:
                    # Si l'élément actuel est dans temp (prochaine étape
                    # présente), temp prend la valeur à cette clef
                    # (nous avançons).

                    if element in temp:
                        temp = temp[element]

                    # S'il n'est pas présent, nous quittons la boucle.
                    else:
                        done = True

                # Nous incrémentons i de 1.
                i += 1

        # Nous retournons le résultat.
        return result

    # Déclaration de la signature de la méthode get.
    def get(self, path: Path, mode: int = 0):
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description : Le chemin de la valeur à récupérer.

            mode (int) :
                Description : Le mode de récupération.
                Valeur par défaut : 0.

        Sortie :
            any :
                Description : La valeur située au chemin donné.

        Rôle :
            Récupère la valeur située au chemin donné dans l'objet courant.
        """

        # Nous initialisons le résultat sur None.
        result = None

        # Si le path est valide, et qu'il contient un attribut splitted_path.
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "splitted_path"):
            # Nous obtenons la taille, ainsi que la première clef.
            size = len(path.splitted_path)
            first_key = path.splitted_path[0]

            # Si la première clef est bien dans self.data.
            if first_key in self.data:
                # Nous assignons la valeur à cette clef dans result.
                result = self.data[first_key]

                # Puis, pour chaque indice de 1 à size.
                for i in range(1, size):
                    # Nous obtenons l'élément actuel.
                    element = path.splitted_path[i]

                    # Si result est un dictionnaire.
                    if isinstance(result, dict):
                        # Et que l'élément est dans result, nous avançons.
                        if element in result:
                            result = result[element]

                    # Sinon, result devient None.
                    else:
                        result = None

                # Si le mode vaut 1, alors nous précédons à la création
                # d'un objet Json avec le contenu du résultat.
                if mode == 1:
                    temp = Json(content = result)
                    result = temp

        # Sinon, si le path est vide, nous assignons à result self.data.
        elif path.path == "":
            result = self.data

        # Nous renvoyons le résultat.
        return result

    # Déclaration de la signature de la méthode exists.
    def exists(self, path: Path) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin à vérifier.

        Sortie :
            bool :
                Description : True si le chemin existe, False sinon.

        Rôle :
            Vérifie si un chemin donné existe dans l'objet courant.
        """

        # Initialisation du résultat sur False.
        result = False

        # Si le path est valide, et qu'il contient un attribut splitted_path.
        if hasattr(path, "usoi") and path.usoi == 8 and hasattr(path, "splitted_path"):
            # Nous initialisons size, temp, i, et result.
            size = len(path.splitted_path)
            temp = self.data
            i = 0
            result = True

            # Tant que i est plus petit que le nombre d'étapes,
            # et que result vaut True.
            while i < size and result:
                # Nous obtenons l'élément actuel.
                element = path.splitted_path[i]

                # Si l'élément est dans temp, nous avançons.
                if element in temp:
                    temp = temp[element]

                # Sinon, nous quittons la boucle, et le résultat
                # renvoyé sera False.
                else:
                    result = False

                # Nous incrémentons i de 1.
                i += 1

        # Nous renvoyons le résultat.
        return result