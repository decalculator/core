# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : loader.py
# Rôle    : Ce fichier implémente la classe Loader, qui est utile
#           pour charger des objets.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Loader.
import asyncio

from core.modules.path.path import *
from core.modules.json.json import *
from core.modules.asynctools import *

# Définition de la classe Executable.
class Executable:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        filesystem: Filesystem,
        classification: str,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        condition: dict | None = None,
        content: str | None = None,
        mode: str | None = None,
        path: str | None = None,
        ppid: DynamicValue | None = None,
        executable_type: int | None = None,
        args: list[str] | None = None,
        flags: list[str] | None = None,
        usoi: int | None = None,
        call: str | None = None,
        loop: Loop | None = None
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            filesystem (Filesystem) :
                Description :
                Une instance Filesystem.

            classification (str) :
                Description :
                    Le type de classification de l'exécutable,
                classique ou complexe.

            memory (Memory | None) :
                Description :
                    L'objet de mémoire parent.
                Valeur par défaut : None.

            pid_manager (PidManager | None) :
                Description :
                    L'objet gestionnaire de PIDs parent.
                Valeur par défaut : None.

            logs (Logs | None) :
                Description :
                    L'objet de logs parent.
                Valeur par défaut : None.

            pid (Pid | None) :
                Description :
                    Le PID de l'objet.
                Valeur par défaut : None.

            condition (dict | None) :
                Description :
                    Les conditions d'exécution de l'exécutable.
                Valeur par défaut : None.

            content (str | None) :
                Description :
                    Le contenu de l'exécutable.
                Valeur par défaut : None.

            mode (str | None) :
                Description :
                    Le mode d'exécution de l'exécutable.
                Valeur par défaut : None.

            path (str | None) :
                Description :
                    Le chemin de l'exécutable.
                Valeur par défaut : None.

            ppid (DynamicValue | None) :
                Description :
                    Le PID de l'objet parent.
                Valeur par défaut : None.

            executable_type (int | None) :
                Description :
                    Le type de l'exécutable.
                Valeur par défaut : None.

            args (list[str] | None) :
                Description :
                    La liste des arguments passés à l'exécutable.
                Valeur par défaut : None.

            flags (list[str] | None) :
                Description :
                    La liste des drapeaux passés à l'exécutable.
                Valeur par défaut : None.

            usoi (int | None) :
                Description :
                    L'USOI de l'objet courant.
                Valeur par défaut : None.

            call (str | None) :
                Description :
                    L'appel associé à l'exécutable.
                Valeur par défaut : None.

            loop (Loop | None) :
                Description :
                    La boucle d'événements asynchrone.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe Executable,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation et assignation des attributs.
        self.usoi = 14
        self.memory = memory
        self.logs = logs
        self.pid = pid
        self.filesystem = filesystem
        self.loop = loop
        self.pid_manager = pid_manager
        self.ppid = ppid

        # Vérification concernant la loop.
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        # Initialisation de l'attribut data.
        self.data = Json()
        self.data.write(Path("settings"), {})

        if condition is not None:
            self.data.write(Path("settings/condition"), condition)

        self.data.write(Path("settings/content"), content)
        self.data.write(Path("settings/mode"), mode)
        self.data.write(Path("settings/path"), path)

        if executable_type is not None:
            self.data.write(Path("settings/type"), executable_type)

        if args is not None and args:
            self.data.write(Path("settings/args"), args)

        if flags is not None and flags:
            self.data.write(Path("settings/flags"), flags)

        if classification is not None and classification:
            self.data.write(Path("settings/classification"), classification)

        if usoi is not None and usoi:
            self.data.write(Path("settings/usoi"), usoi)

        if call is not None and call:
            self.data.write(Path("settings/call"), call)

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

    # Déclaration de la signature de la méthode get.
    def get(self, path: Path):
        """
        Entrée :
            path (Path) :
                Description :
                    Le path vers la valeur à obtenir.

        Sortie :
            Any :
                Description :
                    La valeur obtenue.

        Rôle :
            Renvoyer la valeur présente à un Path.
        """

        # Renvoie la valeur obtenue.
        return self.data.get(path)

    # Déclaration de la signature de la méthode execute.
    async def execute(self, logs: bool = False, mode: int = 0):
        """
        """

        # Nous initialisons le code de retour de l'exécution sur False.
        result_code = False

        # Nous obtenons le type de l'exécutable que nous allons lancer.
        executable_type = self.data.get(Path("settings/type"))

        # Nous obtenons les arguments liés à son exécution.
        executable_args = None
        if self.data.exists(Path("settings/args")):
            executable_args = self.data.get(Path("settings/args"))

        # Nous obtenons les flags liés à son exécution.
        executable_flags = None
        if self.data.exists(Path("settings/flags")):
            executable_flags = self.data.get(Path("settings/flags"))

        # last vaut True si "settings/condition" n'existe pas.
        last = False
        if not self.data.exists(Path("settings/condition")):
            last = True

        # Si l'argument de logs vaut True.
        if logs:
            # Nous intialisons d'abord le deuxième texte, car il est commun
            # aux différents modes.
            text2 = f"path          : {self.data.get(Path("settings/path"))}"

            # Si le type d'exécutable vaut 0.
            if executable_type == 0:
                # Nous initialisons text1 avec content.
                text1 = f"execute       : {self.data.get(Path("settings/content"))}()"

            # Sinon, c'est un exécutable.
            else:
                # Nous affichons seulement pour le moment main.
                text1 = f"execute       : main()"

                # Si des args et des flags sont présents, nous les ajoutons
                # à text2.

                if executable_args is not None:
                    text2 += f"\nargs          : {", ".join(executable_args)}"

                if executable_flags is not None:
                    text2 += f"\nflags         : {", ".join(executable_flags)}"

            # Nous initialisons les textes 3 et 4
            text3 = f"mode          : {self.data.get(Path("settings/mode"))}"
            text4 = f"type          : {"python" if executable_type == 0 else "executable"}"

            # Puis, nous les affichons.
            print(text1)
            print(text2)
            print(text3)
            print(text4)

            # Si l'exécutable n'est pas le dernier, nous affichons
            # le résultat attendu (il fait partie d'une condition).
            if not last:
                print(f"expected result : {self.data.get(Path("settings/condition/execution/result/true"))}")

        # Nous commençons à initialiser le début du payload qui permettra
        # d'appeler l'objet.
        lines = ["import asyncio", "import importlib" if executable_type == 0 else "import subprocess"]

        # Si le mode est exec, ou bien que last vaut True (car ces paramètres
        # n'existent pas si last est True.
        if self.data.get(Path("settings/condition/execution/mode")) == "exec" or last:

            # Si tout le contenu doit être exécuté.
            if self.data.get(Path("settings/condition/execution/content")) == "{all}":
                # Le contenu est le contenu entier du fichier.
                content = await self.filesystem.read(Path(self.data.get(Path("settings/path")), mode = 1), mode = 1)
                lines = content

            # Sinon, tout le contenu ne doit pas être exécuté.
            else:
                # Nous obtenons le contenu du fichier.
                content = await self.filesystem.read(Path(self.data.get(Path("settings/file")), mode = 1), mode = 1)

                # Nous obtenons le path vers le fichier.
                path = self.data.get(Path("settings/path"))

                # Si le type de l'exécutable est 0 (python).
                if executable_type == 0:
                    # Nous transformons le path, pour en faire un import
                    # style python.

                    while ".py" in path:
                        path = path.replace(".py", "")

                    while "/" in path:
                        path = path.replace("/", ".")

                # Nous ajoutons un pont asynchrone au payload.
                lines.append("async def bridge():")
                lines.append("    try:")

                # Si l'exécutable est en python.
                if executable_type == 0:
                    # Nous ajoutons un import via importlib, car les USOI
                    # commencent par des chiffres, ce qui ne plaît pas à
                    # python initialement.
                    lines.append(f"        mod = importlib.import_module('{path}')")

                    # Puis, nous ajoutons un saut vers la fonction asynchrone.
                    lines.append(f"        return await mod.{self.data.get(Path("settings/content"))}(variables = variables)")

                # Sinon, si c'est un exécutable à lancer avec subprocess.
                elif executable_type == 1:
                    # Nous initialisons les arguments pour subprocess.
                    subprocess_arg = f"'{self.data.get(Path("settings/path"))}'"

                    # Nous initialisons aussi les arguments, si présents.
                    if executable_args is not None:
                        for arg in executable_args:
                            subprocess_arg += (f", '{arg}'")


                    # Idem pour les flags.
                    subprocess_flags = ""
                    if executable_flags is not None:
                        for arg in executable_flags:
                            subprocess_flags += (f", {arg}")

                    # Enfin, nous ajoutons la ligne subprocess complète.
                    lines.append(f"        process = subprocess.Popen([{subprocess_arg}]{subprocess_flags})")

                # Et pour terminer, nous ajoutons une gestion simple
                # des erreurs, pour que le crash d'un objet n'entraîne
                # pas la chute des autres.

                lines.append("    except Exception as error:")
                lines.append("        print(error)")
                lines.append("    except:")
                lines.append("        print('error')")

        # Si le payload contient plus de deux lignes,
        # (pour ne pas compter les imports).

        if len(lines) > 2:
            # Nous initialisons les variables d'exécution.
            exec_vars = {"memory": self.memory, "pid_manager": self.pid_manager}

            # Nous y ajoutons l'USOI, le PID, ainsi que le PID
            # de l'exécutable, si présents.
            if self.data.exists(Path("settings/usoi")):
                usoi = self.data.get(Path("settings/usoi"))
                exec_vars["usoi"] = usoi

                pid = self.pid_manager.get_pid(usoi = usoi, ppid = self.pid)
                exec_vars["pid"] = pid
                exec_vars["ppid"] = self.pid

            # Nous appelons la méthode d'exécution async_exec.
            result = await self.async_exec(lines, variables = exec_vars, mode = mode, usoi = usoi, pid = pid)

            # Si le mode est 0.
            if mode == 0:
                # Si logs vaut True, nous affichons le résultat.
                if logs:
                    print(f"result        : {result}")

                # Si cela correspond au "true" définit.
                if result == self.data.get(Path("settings/execution/result/true")):
                    # Si i vaut 0, le résultat global est True, et nous
                    # quittons la boucle.
                    if i == 0:
                        result_code = True
                        done = True

                # Sinon, nous quittons simplement la boucle.
                else:
                    done = True

            # Si ce n'est pas un simple exécutable python.
            else:
                # Pour le moment, nous n'avons pas encore développé cette partie.
                pass

        # Nous renvoyons le résultat global.
        return result_code

    # Déclaration de la signature de la méthode write.
    def write(self, path: Path, value, mode: int = 0) -> bool:
        """
        """

        # Renvoie le résultat de l'écriture.
        return self.data.write(path, value, mode = mode)

    # Déclaration de la signature de la méthode remove.
    def remove(self, path: Path) -> bool:
        """
        """

        # Renvoie le résultat de la supression.
        return self.data.remove(path)

    # Déclaration de la signature de la méthode get.
    def get(self, path: Path):
        """
        """

        # Renvoie la valeur obtenue.
        return self.data.get(path)

    # Déclaration de la signature de la méthode exists.
    def exists(self, path: Path):
        """
        """

        # Renvoie la valeur obtenue.
        return self.data.exists(path)

    # Déclaration de la signature de la méthode async_exec.
    async def async_exec(
        self,
        code,
        variables = None,
        mode = None,
        usoi = None,
        pid = None
    ):

        """
        """

        # 0 : classic
        # 1 : complex

        # Nous initialisons un bool sur False.
        state = False

        # S'il existe un paramètre "call".
        if self.data.exists(Path("settings/call")):
            # Nous initialisons un post-payload.
            payload1 = self.data.get(Path("settings/call"))
            # Le booléen devient True.
            state = True

        # Nous initialisons le payload.
        payload = ""

        # Si le code est une liste de lignes, nous le transformons en
        # un str.
        if isinstance(code, list):
            for line in code:
                payload += f"{line}"

                if not state:
                    payload += "\n"

        # Si c'est un str, nous le gardons comme tel.
        elif isinstance(code, str):
            payload = code

        # Nous préparons les variables d'exécution.
        exec_vars = {"variables": variables}
        # Nous exécutons le premier payload, avec les variables.
        exec(payload, exec_vars)

        # Nous obtenons l'adresse du pont, nommé bridge.
        bridge = exec_vars["bridge"]

        # Si le booléen state vaut True.
        if state:
            # Nous préparons de nouvelles variables d'exécution.
            exec_vars = {"self": self, "bridge": bridge, "variables": variables}
            # Puis exécutons le deuxième payload.
            exec(payload1, exec_vars)

            # Enfin, si "task" a été définit par l'exécution de payload1,
            # nous assignons à la variable task une référence vers celle-ci.
            if "task" in exec_vars:
                task = exec_vars["task"]

        # Sinon, si le booléen state vaut False.
        else:
            # task est la task créer par asyncio, qui point vers le premier
            # pont (bridge) du premier payload.
            task = self.loop.create_task(bridge())

        # Si le mode est 0, c'est à dire un objet classique,
        # nous faisons un await pour attendre la fin de l'exécution
        # de l'objet, avant de continuer.
        if mode == 0:
            result = await task

        # Si le mode n'est pas 1, cela signifie que nous lançons "dans le
        # vide", nous stockons donc la task dans la mémoire, au même endroit
        # que pour stocker les objets mais dans "task" (et non pas "object").
        else:
            self.memory.write(Path(f"proc/instances/modules/{usoi}/pids/{pid.data}"), {"task": task}, mode = 1)

        # Finalement, nous renvoyons le résultat du await, si mode vaut 0,
        # et sinon None (car la task est encore en cours, ça ne serait
        # pas le résultat).

        return result if mode == 0 else None