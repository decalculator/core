# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : dynamic_value.py
# Rôle    : Ce fichier implémente la classe DynamicValue, qui est utile
#           pour enregistrer des valeurs qui peuvent varier.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import du module asyncio.
import asyncio

# Import du module path.
from core.modules.path.path import *


# Définition de la classe DynamicValue.
class DynamicValue:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        value,
        memory: Memory | None=None,
        pid_manager: PidManager | None=None,
        logs: Logs | None=None,
        pid: Pid | None=None,
        ppid: DynamicValue | None=None
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            value (any) :
                Description : La valeur à assigner.

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

            loop (_UnixSelectorEventLoop | ...) :
                Description : La boucle d'événements asychrone.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode asynchrone d'initialisation de la classe
            DynamicValue, elle assigne aux attributs leurs valeurs, et
            s'écrit correctement comme instance dans la mémoire parente,
            ainsi que dans le gestionnaire de PIDs.
        """

        # Nous attribuons les arguments comme valeurs aux attributs,
        # à l'exception de pid_manager, qui ne sera pas utile.

        self.usoi = 3
        self.data = value
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.ppid = ppid

        # Si aucun PID n'a été passé en argument, que l'attribut
        # pid_manager a un attribut "usoi" (cela signifie au passage qu'il
        # n'est pas None), et que son attribut "usoi" est égal à 1.
        if self.pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    # Nous générons un PID grâce à la méthode asynchrone
                    # get_pid, de pid_manager, à laquelle nous passons l'USOI
                    # de l'objet courant, ainsi que son PPID.
                    # L'attribut pid prend ce résultat pour valeur.

                    self.pid = pid_manager.get_pid(
                        usoi=self.usoi,
                        ppid=self.ppid
                    )

        # Si l'attribut pid possède un attribut "usoi", et que cet
        # attribut a pour valeur 3.
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                # Si l'attribut memory possède un attribut "usoi",
                # et que cet attribut a pour valeur 1.
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        # Ecriture de l'objet dans la mémoire au path suivant :
                        # "proc/instances/{type}/{usoi}/pids/{pid}/object"

                        # Nous sommes conscients du fait que le nombre de
                        # caractères du path dépasse la limite autorisée par
                        # la pep8. Nous aurions pu choisir de construire
                        # le path en parties, avec les opérateurs de
                        # division, mais cela aurait coûté des performances
                        # en plus.

                        # Initialiser le path plus bas (en indentations)
                        # était possible, mais ce serait risquer de
                        # l'initialiser pour rien.

                        self.memory.write(
                            Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"),
                            {"object": self},
                            mode=1
                        )

        # Renvoie le PID de l'objet courant.
        return pid

    # Déclaration de la signature de la méthode write.
    def write(self, value) -> None:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            value (any) :
                Description :
                    La valeur à écrire.

        Sortie :
            None

        Rôle :
            Assigne une nouvelle valeur à l'attribut data de l'objet courant.
        """

        # L'attribut data de l'objet courant prend pour valeur value.
        self.data = value

    # Déclaration de la signature de la méthode get.
    def get(self):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            None

        Sortie :
            self.data (any) :
                Description :
                    La valeur de l'attribut data de l'objet courant.

        Rôle :
            Renvoie la valeur de l'attribut data de l'objet courant.
        """

        return self.data
