# USOI de l'entrée : 17
# USOI de gui : 19

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import du module asyncio.
import asyncio

# Import des modules requis par l'entrée.
from core.modules.path.path import *
from core.modules.logs.logs import *
from core.modules.pid_manager.pid_manager import *
from core.modules.memory.memory import *
from core.modules.filesystem.filesystem import *
from core.modules.languages.languages import *
from core.modules.settings.settings import *
from core.modules.template.template import *
from core.modules.loader.loader import *
from core.modules.scheduler.scheduler import *
from core.modules.dynamic_value.dynamic_value import *

from core.plugins.device.device import *
from core.plugins.gui.gui import *
from core.plugins.repos.repos import *

async def entry(**kwargs):
    """
    Type de méthode :
        Asynchrone.

    Entrée :
        kwargs (dict) :
            Description : Les arguments nommés de l'entrée, contenant
                notamment les variables du contexte parent.

    Sortie :
        None

    Rôle :
        Il s'agit du point d'entrée de l'application GUI. Lors de la
        première exécution, il initialise l'ensemble des modules, plugins
        et objets nécessaires au fonctionnement de l'interface graphique,
        puis lance la boucle principale. Les exécutions suivantes sont
        ignorées.
    """

    print("gui::entry > exec !")

    # Définition du chemin de configuration principale.
    CONFIGURATION = Path("data/core/configuration.json", mode = 1)

    # Récupération de l'objet self si présent dans les arguments.
    if "self" in kwargs:
        self = kwargs["self"]

    # Récupération de la mémoire et du gestionnaire de PIDs parents.
    parent_memory = kwargs["variables"]["memory"]
    parent_pid_manager = kwargs["variables"]["pid_manager"]

    # Récupération du PID si présent dans les variables.
    pid = None
    if "pid" in kwargs["variables"]:
        pid = kwargs["variables"]["pid"]

    # Récupération du PPID si présent dans les variables.
    ppid = None
    if "ppid" in kwargs["variables"]:
        ppid = kwargs["variables"]["ppid"]

    # Récupération de l'USOI si présent dans les variables.
    usoi = None
    if "usoi" in kwargs["variables"]:
        usoi = kwargs["variables"]["usoi"]

    # Initialisation du chemin de l'instance dans la mémoire parente.
    path = Path(f"proc/instances/modules/{usoi}")

    if not parent_memory.exists(path):
        parent_memory.write(path, {})

    # Récupération ou initialisation de la mémoire partagée.
    shared_memory_path = path / "shared_memory"

    if parent_memory.exists(shared_memory_path):
        parent_memory.write(shared_memory_path / "exec_count", parent_memory.get(shared_memory_path / "exec_count") + 1)
        shared_memory = parent_memory.get(shared_memory_path)

    else:
        shared_memory = {"exec_count": 0}
        parent_memory.write(shared_memory_path, shared_memory)

    # Récupération du nombre d'exécutions.
    execution_count = shared_memory["exec_count"]

    # Initialisation uniquement lors de la première exécution.
    if execution_count == 0:
        loop = asyncio.get_running_loop()

        # 1 : si on veut un sous-pid manager

        """
        pid_manager = PidManager(ppid = pid, pid_manager = parent_pid_manager)
        pid_manager.write(Path("uuid"), {"used": {}, "unused": [], "max": 1})
        pid_manager.set_get_pid(unused_path = Path("uuid/unused"), used_path = Path("uuid/used"), maximum_path = Path("uuid/max"))

        core = DynamicValue(0)
        pid_manager_pid = DynamicValue(1)

        data = {
            core.data: {
                "usoi": -1,
                "ppid": -1,
                "cpids": [pid_manager_pid.data]
            },
            pid_manager_pid.data: {
                "usoi": pid_manager.usoi,
                "ppid": core.data
            }
        }

        pid_manager.write(Path("uuid/used"), data)
        """

        # 2 : si on veut garder le même pid manager (global)

        pid_manager = parent_pid_manager
        pid_manager_pid = parent_pid_manager.pid

        # ça reprend ici

        # Initialisation de la mémoire et de ses chemins de base.
        memory = Memory(pid_manager = pid_manager, ppid = pid_manager_pid)
        memory.write(Path("proc/instances/objects"), {}, mode = 1)
        memory.write(Path("proc/instances/plugins"), {})
        memory.write(Path("proc/instances/modules"), {})

        # Initialisation des logs.
        logs = Logs(memory = memory, pid_manager = pid_manager, ppid = pid_manager_pid)

        # Initialisation du module device et récupération de la résolution.
        device = Device(memory = memory, pid_manager = pid_manager, ppid = pid_manager_pid)

        width, height = device.get_resolution()
        device.write(Path("settings/resolution"), [width, height], mode = 1)

        # Initialisation du filesystem.
        filesystem = Filesystem(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

        # Initialisation des paramètres et résolution des variables.
        settings = Settings(memory = memory, pid_manager = pid_manager, logs = logs, content = await filesystem.read(CONFIGURATION, mode = 2), ppid = pid_manager_pid)
        settings.resolve(settings.get(Path("variables_pattern")))

        # Initialisation du module de langues et chargement de l'anglais.
        languages = Languages()
        await languages.init(filesystem, settings, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        await languages.load_language("english")
        languages.select(Path("english"))

        # Initialisation du template de signaux.
        signals = Template(name = "signals", memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

        # Initialisation du loader et de ses chemins de base.
        loader = Loader(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        loader.write(Path("objects"), {})
        loader.write(Path("plugins"), {})
        loader.write(Path("modules"), {})

        # Initialisation du scheduler et lancement de la boucle classique.
        scheduler = Scheduler(loader, filesystem, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
        scheduler.write(Path("classic"), {"to_run": {}, "running": {}})
        scheduler.write(Path("complex"), {})
        scheduler.run(Path("classic"), mode = 0)

        # Initialisation des dépôts et chargement de leur contenu.
        repos = Repos(settings = settings)
        content = settings.get(Path("repos_config"))
        content = await filesystem.read(Path(settings.get(Path("repos_config")), mode = 1), mode = 2)

        for repo, value in content.items():
            if "path" in value:
                path = Path(value["path"], mode = 1)

            else:
                path = Path(f"{settings.get(Path("repos_folder_path"))}/{repo}/{repo}.json", mode = 1)

            repos.write(Path(f"repos/{repo}"), await filesystem.read(path, mode = 2), mode = 1)

        # Initialisation de la configuration GUI et lancement de l'interface.
        gui_configuration = Path("sources/core/plugins/gui/data/gui.json", mode = 1)
        gui_configuration = await filesystem.read(gui_configuration, mode = 2)
        gui_configuration = DynamicValue(gui_configuration)

        gui = Gui(configuration = gui_configuration, device = device, memory = memory, pid_manager = pid_manager, logs = logs, filesystem = filesystem, settings = settings, languages = languages, loader = loader, scheduler = scheduler, repos = repos)
        await gui.run(shared_memory = shared_memory)

    else:
        print("not available for the moment")