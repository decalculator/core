# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : execution.py
# Rôle    : Ce fichier implémente la classe Execution, qui est utile
#           pour charger des exécutions d'objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Execution.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *
from core.modules.executable.executable import *

# Définition de la classe Execution.
class Execution:

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
        """

        # Initialisation et assignation des attributs.
        self.usoi = 13
        self.ppid = ppid
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.filesystem = filesystem
        self.pid_manager = pid_manager
        self.executables = None
        self.data = Json()

        # Initialisation de l'attribut data.
        initialized = False
        if (hasattr(content, "usoi") and content.usoi == 5) or isinstance(content, dict):
            self.data.write(Path("settings"), content if isinstance(content, dict) else content.get(Path("")))
            initialized = True

        if not initialized:
            self.data.write(Path("settings"), {})
            initialized = True

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
        # courant dans la mémoire (parente).
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

        # Initialisation de variables.
        settings = self.data.get(Path("settings"))
        register = self.data.get(Path("settings/register"))
        temp = self.data.get(Path("settings/register/execution"))

        done = False
        executables = []

        # Tant que done est False.
        while not done:
            # Le booléen last vaut False.
            last = False

            # Si temp contient "condition", et que register déclare cette
            # condition, nous l'obtenons.
            if "condition" in temp:
                condition = temp["condition"]

                if condition in register["conditions"]:
                    condition = register["conditions"][condition]

            # Sinon, la condition vaut temp, et last vaut True.
            # Cela signifie que c'est le dernier exécutable.
            else:
                condition = temp
                last = True

            # Nous initialisons l'USOI
            usoi = None
            if "usoi" in settings:
                usoi = settings["usoi"]

            # Si condition contient "execution".
            if "execution" in condition:
                # Nous obtenons les détails de cette exécution.
                execution = condition["execution"]
                content = execution["content"]
                execution_type = execution["type"]

                # Nous définissons le type d'exécution.
                if execution_type == "python":
                    executable_type = 0

                    # Si la méthode est bien dans registers/methods,
                    # execution_content prend son contenu.
                    if "methods" in register and content in register["methods"]:
                        execution_content = register["methods"][content]

                # Sinon, si c'est un exécutable, nous définissons les
                # variables en fonction.
                elif execution_type == "executable":
                    execution_content = register["executables"][content]
                    executable_type = 1

                else:
                    # Pour le moment, seuls les exécutables et les fichiers
                    # python sont pris en charge.
                    pass

                # Si tout le contenu doit être exécuté.
                if content == "{all}":
                    # Nous obtenons le fichier.
                    file = execution["file"]

                    # S'il est présent, dans register/files.
                    if file in register["files"]:
                        # Nous obtenons ensuite les informations de celui-ci.
                        file = register["files"][file]
                        path = file["path"]

                        classification = settings["object_type"]

                        call = None
                        if "call" in execution:
                            call = execution["call"]

                        # Nous appelons ensuite le constructeur d'Executable.

                        executable = Executable(
                            filesystem = self.filesystem,
                            pid_manager = self.pid_manager,
                            memory = memory,
                            logs = logs,
                            condition = None if last else condition,
                            content = content,
                            path = path,
                            ppid = ppid,
                            executable_type = executable_type,
                            classification = classification,
                            usoi = usoi,
                            call = call
                        )

                        # Et nous ajoutons l'exécutable à la liste
                        # d'exécutables.
                        executables.append(executable)

                        # Si temp contient "result".
                        if "result" in temp:
                            # Nous continuons à descendre dans le true.
                            if "true" in temp["result"]:
                                temp = temp["result"]["true"]

                        # Si temp ne contient plus "result", nous considérons
                        # que l'exécution est terminée (nous sommes au plus
                        # bas).
                        else:
                            # Nous quittons la boucle.
                            done = True

                # Si tout le contenu ne doit pas être exécuté.
                else:
                    # Nous obtenons les détails de l'exécution.
                    file = execution_content["file"]
                    mode = execution_content["mode"]
                    classification = execution_content["mode"]

                    # Si file est bien dans register/files.
                    if file in register["files"]:
                        file = register["files"][file]
                        path = file["path"]

                        # Nous obtenons les args, ainsi que les flags.

                        args = None
                        if "args" in file:
                            args = file["args"]

                        flags = None
                        if "flags" in file:
                            flags = file["flags"]

                        # Puis, nous pouvons appeler le constructeur d'Executable.

                        executable = Executable(
                            filesystem = self.filesystem,
                            pid_manager = self.pid_manager,
                            memory = memory,
                            logs = logs,
                            condition = None if last else condition,
                            content = content,
                            mode = mode,
                            path = path,
                            ppid = ppid,
                            executable_type = executable_type,
                            args = args,
                            flags = flags,
                            classification = classification,
                            usoi = usoi
                        )

                        # Et nous ajoutons l'exécutable à la liste
                        # d'exécutables.
                        executables.append(executable)

                        # Si temp contient "result".
                        if "result" in temp:
                            # Nous continuons à descendre dans le true.
                            if "true" in temp["result"]:
                                temp = temp["result"]["true"]

                        # Si temp ne contient plus "result", nous considérons
                        # que l'exécution est terminée (nous sommes au plus
                        # bas).
                        else:
                            # Nous quittons la boucle.
                            done = True

        # L'attribut executables prend pour valeur la liste d'exécutables.
        self.executables = executables

    # Déclaration de la signature de la méthode run.
    async def run(self):
        """
        """

        # Initialisation de variables.
        i = 0
        done = False

        # Tant que i est inférieur à la taille de la liste d'exécutables,
        # et que done est False.
        while i < len(self.executables) and not done:
            # Nous obtenons l'exécutable actuel.
            executable = self.executables[i]

            # Si il a une classification (obligatoire, normalement)
            if executable.exists(Path("settings/classification")):
                # Nous définissons mode en fonction de celle-ci.
                classification = executable.get(Path("settings/classification"))
                mode = 0 if classification == "classic" else 1

                # Puis, nous appelons executable.execute avec mode.
                result = await executable.execute(logs = True, mode = mode)

                # Si le résultat est True, nous quittons la boucle.
                if result == True:
                    done = True

            # Ajout d'un incrément de 1 à i.
            i += 1