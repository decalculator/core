# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : loader.py
# Rôle    : Ce fichier implémente la classe Loader, qui est utile
#           pour charger des objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Settings.
import asyncio
import re

from core.modules.path.path import *
from core.modules.json.json import *

# Définition de la classe Settings.
class Settings:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        content: Json | None = None,
        ppid: DynamicValue | None = None
    ) -> None:

        """
        """

        # Initialisation et assignation des attributs.
        self.usoi = 9
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

        elif content is not None and isinstance(content, dict):
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

    # Déclaration de la signature de la méthode resolve.
    def resolve(self, pattern: str) -> None:
        """
        """

        # Nous obtenons les paramètres.
        content = self.data.get(Path(""))

        # Pour chaque nom de paramètre, et sa valeur.
        for key, value in content.items():

            # Si la valeur est un str.
            if isinstance(value, str):
                # Nous initialisons deux booléens sur False.
                done = False
                changed = False

                # Tant que done vaut False.
                while not done:
                    # Nous cherchons le pattern dans value.
                    match = re.search(pattern, value)

                    # Si le pattern est trouvé.
                    if match:
                        # Nous obtenons la partie à remplacer (avec les
                        # brackets), et la partie qui donne l'ID (sans
                        # les brackets).
                        replace = match.group()
                        variable = match.group(1)

                        # Si la variable est présente comme clef dans les
                        # paramètres actuels.
                        if self.data.exists(Path(variable)):
                            # Nous obtenons sa valeur,
                            # qui remplacera replace.
                            new_value = self.data.get(Path(variable))

                            # Tant que replace est dans value,
                            # nous remplaçons l'occurence par la valeur.
                            while replace in value:
                                value = value.replace(replace, new_value)

                            # Le bool changed prend pour valeur True.
                            changed = True

                    # Sinon, si le pattern n'est pas trouvé.
                    else:
                        # Nous quittons la boucle.
                        done = True

                # Si la valeur a changée, nous écrivons value au path key.
                if changed:
                    self.write(Path(key), value)