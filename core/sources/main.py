# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : main.py
# Rôle    : Il s'agit du fichier principal, permettant de lancer core.

# Import des modules requis.

import asyncio

from core.modules.path.path import *
from core.modules.logs.logs import *
from core.modules.pid_manager.pid_manager import *
from core.modules.memory.memory import *
from core.modules.filesystem.filesystem import *
from core.modules.languages.languages import *
from core.modules.settings.settings import *
# from core.modules.template.template import *
from core.modules.loader.loader import *
from core.modules.scheduler.scheduler import *
from core.modules.dynamic_value.dynamic_value import *
from core.modules.asynctools.asynctools import *
from core.modules.references_manager.references_manager import *

# Déclaration de la signature de la fonction main.
async def main(**kwargs):
    """
    Type de fonction :
        Synchrone.

    Entrée :
        kwargs (**, dict) :
            Description :
                Les paramètres à passer à la fonction main, si ce fichier
                est utilisé comme objet.

    Sortie:
        None

    Rôle :
        Il s'agit de la fonction principale permettant de lancer core.
    """

    # Déclaration des paths vers les fichiers de configuration.

    CONFIGURATION = Path("data/core/configuration.json", mode = 1)
    ENTRY_FILE = Path("data/entry/entry.json", mode = 1)

    # Instanciation manuelle des PIDs pour core et pour le gestionnaire
    # de PIDs, car aucun module n'est encore actif.
    core = DynamicValue(0)
    pid_manager_pid = DynamicValue(1)

    # Instanciation de la classe ReferencesManager.
    references_manager = ReferencesManager()

    # Ecriture des premières références, pour les PIDs 0 et 1,
    # qui correspondent à core et au gestionnaire de PIDs.
    references_manager.write(Path("0/references/pids"), [], mode = 1)
    references_manager.write(Path("1/references/pids"), [], mode = 1)

    # Instanciation de la classe PidManager, avec son PID.
    pid_manager = PidManager(pid = DynamicValue(1))
    # Ecriture de la structure de base pour le gestionnaire de PIDs.
    pid_manager.write(Path("uuid"), {"used": {}, "unused": [], "max": 1})
    # Nous enregistrons les paths pour la méthode get_pid.
    pid_manager.set_get_pid(unused_path = Path("uuid/unused"), used_path = Path("uuid/used"), maximum_path = Path("uuid/max"))

    # Nous continuons l'initialisation manuelle pour core et PidManager.
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

    # Ecriture des deux PIDs utilisés (0 et 1) dans le gestionnaire de PIDs.
    pid_manager.write(Path("uuid/used"), data)

    # Instanciation de la mémoire, avec le gestionnaire de pid, le PID
    # du gestionnaire de PIDs comme PPID, et le gestionnaire de références.
    memory = Memory(pid_manager = pid_manager, ppid = pid_manager_pid, references_manager = references_manager)
    # Ecriture de la structure de base pour les trois types, dans memory.
    memory.write(Path("proc/instances/objects"), {}, mode = 1)
    memory.write(Path("proc/instances/plugins"), {})
    memory.write(Path("proc/instances/modules"), {})

    # Instanciation des logs, avec la mémoire, le gestionnaire de PIDs,
    # le PPID, et le gestionnaire de références.
    logs = Logs(memory = memory, pid_manager = pid_manager, ppid = pid_manager_pid, references_manager = references_manager)

    # Instanciation de Filesystem, avec la mémoire, le gestionnaire de PIDs,
    # le PPID, les logs.
    filesystem = Filesystem(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

    # Instanciation des paramètress, avec la mémoire, le gestionnaire de PIDs,
    # les logs, le PPID, et le contenu du fichier de configuration comme
    # valeur.
    settings = Settings(memory = memory, pid_manager = pid_manager, logs = logs, content = await filesystem.read(CONFIGURATION, mode = 2), ppid = pid_manager_pid)
    # Résolution des variables dans les valeurs des paramètres grâce au
    # pattern stocké dans settings "variables_pattern".
    settings.resolve(settings.get(Path("variables_pattern")))

    # Obtention et écriture du contenu de fichier de configuration
    # des différents types d'objets dans les paramètres.

    objects_config = settings.get(Path("objects_config"))
    objects_config = Path(objects_config, mode = 1)
    settings.write(Path("objects/content"), await filesystem.read(objects_config, mode = 2), mode = 1)

    plugins_config = settings.get(Path("plugins_config"))
    plugins_config = Path(plugins_config, mode = 1)
    settings.write(Path("plugins/content"), await filesystem.read(plugins_config, mode = 2), mode = 1)

    # Instanciation des langues.
    # Appel de la méthode init, avec les objets Filesystem,
    # Settings, Memory, PidManager, Logs, PPID.

    languages = Languages()
    await languages.init(filesystem, settings, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

    # Par défaut, nous chargeons l'anglais.
    await languages.load_language("english")
    # Puis, nous le sélectionnons.
    languages.select(Path("english"))

    # 
    # signals = Template(name = "signals", memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

    # Instanciation du loader, avec les arguments habituels.
    loader = Loader(memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)

    # Création de la structure interne de base pour le loader.
    loader.write(Path("objects"), {})
    loader.write(Path("plugins"), {})
    loader.write(Path("modules"), {})

    # Instanciation du scheduler, avec les arguments habituels, mais aussi
    # le loader ainsi que Filesystem.
    scheduler = Scheduler(loader, filesystem, memory = memory, pid_manager = pid_manager, logs = logs, ppid = pid_manager_pid)
    # Ecriture de la structure interne de base pour Scheduler.
    scheduler.write(Path("scheduling"), {"to_run": {"objects": [], "plugins": [], "modules": []}}, mode = 1)

    # Obtention du contenu du fichier data/entry/entry.json".
    entry_file_data = Json(content = await filesystem.read(ENTRY_FILE, mode = 2))
    entry_file_content = entry_file_data.get(Path("text"))

    # Pour chaque clef et valeur de ce fichier.
    for key, value in entry_file_content.items():
        # Obtention des valeurs de base : le contenu du texte, un bool
        # indiquant si il doit être caché, un bool indiquant si le titre
        # doit être caché, et un dernier bool indiquant si ce texte est
        # traduit avec Languages.

        content = value["content"]
        hide = value["hide"]
        hide_title = value["hide_title"]
        translated = value["translated"]

        # Si le texte n'est pas caché.
        if not hide:
            # Obtention du type de la valeur.
            value_type = type(content)

            # S'il s'agit d'une liste.
            if value_type == list:

                # Si le titre n'est pas à cacher, nous l'affichons.
                if not hide_title:
                    print(f"{key} :")

                # Pour chaque valeur de la liste.
                for line in content:

                    # Si le texte est traduit, nous le récupérons avec Languages.
                    if translated:
                        print(languages.get_from_selected(Path(f"entry/{line}")))

                    # Sinon, nous l'affichons simplement.
                    else:
                        print(line)

            # elif value_type == dict:
                # nous verrons plus tard pour une recherche profonde

            # S'il ne s'agit pas d'une liste.
            else:
                # Initialisation du texte à afficher.
                text = ""

                # Si le titre n'est pas à cacher, nous l'ajoutons au texte
                # à afficher.
                if not hide_title:
                    text += f"{key} : "

                # Si le texte est traduit, nous le récupérons avec Languages.
                if translated:
                    text += languages.get_from_selected(f"entry/{content}")

                # Sinon, nous l'ajoutons simplement au texte à afficher.
                else:
                    text += content

                # Puis, nous affichons le texte.
                print(text)

    # Initialisation de la structure de base des entrées.
    entries = {"objects": [], "plugins": []}

    # Initialisation des types disponibles (pour les entrées).
    objects_types = ["objects", "plugins"]

    files = []
    size = 0

    # Pour chaque type des types disponibles.
    for object_type in objects_types:
        # Pour chaque objet associé à ce type dans les paramètres.
        for obj in settings.get(Path(f"{object_type}/content")):
            # Si cet objet est activé (ses paramètres JSON n'indiquent pas
            # qu'il est désactivé).
            if settings.get(Path(f"{object_type}/content/{obj}/enabled")) == True:
                # Si un path est définit, config_path prend la valeur de ce path.
                if settings.exists(Path(f"{object_type}/content/{obj}/config_path")):
                    config_path = settings.get(Path(f"{object_type}/content/{obj}/config_path"))

                # Sinon, le path par défaut est :
                # "sources/core/{type}/{obj}/{obj}.json"
                else:
                    config_path = f"sources/core/{object_type}/{obj}/{obj}.json"

                # Instanciation d'un path matériel avec ce string.
                config_path = Path(config_path, mode = 1)

                # Ajout de l'objet et de son path dans les variables.
                entries[object_type].append(obj)
                files.append(config_path)

                # Incrémentation de la taille, pour ne pas avoir à faire un
                # len inutile.
                size += 1

    # Si size est différent de 0, cela signifie que des entrées sont
    # sélectionnées.
    if size:
        # Initialisation d'un incrément.
        add = 0

        # Pour chaque type d'objet.
        for object_type in objects_types:
            # Affiche du texte : "{type} :".
            print(languages.get_from_selected(Path(f"entry/{object_type}_name")))

            # Nous obtenons le type d'entrée ainsi que le nombre d'objets.
            entries_type = entries[object_type]
            entries_len = len(entries_type)

            # Pour chaque objet, nous l'affichons.
            for i in range(entries_len):
                print(f"{i + add} : {entries_type[i]}")

            # Ajout du nombre d'entrées à l'incrément.
            add += entries_len

        # all_entries contient un union de toutes les entrées.
        all_entries = entries["objects"].copy()
        all_entries.extend(entries["plugins"])

        # Affichage du message qui demande à l'utilisateur de choisir
        # les entrées.
        print(languages.get_from_selected(Path("entry/select_entries")))

        # Initialisation de variables.
        choices = []
        done = False

        # Tant que done vaut False.
        while not done:
            # Appel de la fonction async_input pour obtenir le choix de
            # l'utilisateur, sans bloquer.
            choice = await async_input("> ")

            # Si le choix est "done", nous quittons la boucle.
            if choice == "done":
                done = True

            # Sinon.
            else:
                # Si il s'agit d'un digit, nous faisons un cast de la valeur
                # de str vers int.
                if choice.isdigit():
                    choice = int(choice)

                    # Si le choix n'est pas déjà dans les choix d'entrées,
                    # nous l'ajoutons.
                    if choice not in choices:
                        choices.append(choice)

                    # Sinon, nous affichons le message qui explique que l'objet
                    # est déjà activé.
                    else:
                        print(languages.get_from_selected(Path("entry/object_already_enabled")))

                # Si le choix est "*"
                elif choice == "*":
                    # Nous initialisons une liste qui contiendra tous
                    # les indices des objets.
                    choices = []

                    for i in range(size):
                        choices.append(i)

                    # Nous quittons la boucle.
                    done = True

        # Pour chaque indice i des choix d'objets.
        for i in range(len(choices)):
            # Nous obtenons l'objet.
            obj = all_entries[choices[i]]

            # Nous obtenons son type, puis nous écrivons son contenu dans le
            # Loader.
            if choices[i] < len(entries["objects"]):
                loader.write(Path(f"objects/{obj}/content"), await filesystem.read(files[choices[i]], mode = 2), mode = 1)

            else:
                loader.write(Path(f"plugins/{obj}/content"), await filesystem.read(files[choices[i]], mode = 2), mode = 1)

    # Sinon, nous affichons qu'aucune entrée n'a été sélectionnée.
    else:
        print(languages.get_from_selected(Path("entry/no_entry_found")))

    # Pour chaque type d'objet.
    for object_type in objects_types:
        object_type_path = Path(f"{object_type}")

        # Pour chaque objet load de ce type.
        for obj in loader.get(object_type_path):
            content_path = object_type_path / obj / "content"

            # Si le path vers le content de l'objet existe dans le loader.
            if loader.exists(content_path):
                # Nous obtenons le contenu, l'usoi.
                content = loader.get(content_path)
                usoi = content["usoi"]

                # Puis, nous ajoutons l'objet dans la file de l'ordonnanceur.
                scheduler.add_to_queue(path = Path("scheduling"), object_type = object_type, usoi = obj)

    # Une fois que tous les objets ont été ajoutés, nous lançons l'exécution
    # de la file par Scheduler.
    scheduler.run(path = Path("scheduling"), mode = 0)

    # Et une fois l'exécution terminée, nous effectuons un nettoyage
    # de la file, ne pas passer d'argument "mode" signifie que toutes les
    # files de tous les types sont remises à 0 (une liste vide).
    scheduler.clean_queue(path = Path("scheduling"))

# Si le fichier main.py est lancé comme fichier principal.
if __name__ == "__main__":
    # Nous générons une event loop asyncio.
    loop = asyncio.new_event_loop()

    # Nous y ajoutons une task, la fonction main.
    # Ici, nous ne lui passons pas de **kwargs, car il s'agit de la première
    # exécution, nous ne l'utilisons pas comme objet.
    loop.create_task(main())

    # Nous assignons la boucle pour ce thread.
    asyncio.set_event_loop(loop)

    # Nous indiquons à asyncio qu'il doit tourner pour toujours.
    loop.run_forever()
