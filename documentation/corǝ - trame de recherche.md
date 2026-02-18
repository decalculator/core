# I - corǝ

## I - Table des matières

- [I - corǝ](#i---corǝ)
    - [I - Table des matières](#i---table-des-matières)
    - [II - Préambule](#ii---préambule)
        - [I - Sujet](#i---sujet)
        - [II - Idée initiale](#ii---idée-initiale)
    - [III - Concepts](#iii---concepts)
        - [I - Le moteur du portail](#i---le-moteur-du-portail)
        - [II - Les paramètres statiques](#ii---les-paramètres-statiques)
        - [III - Les systèmes](#iii---les-systèmes)
        - [IV - Les objets](#iv---les-objets)
        - [V - Valeurs JSON](#v---valeurs-json)
        - [VI - Le système d'objets](#vi---le-système-dobjets)
            - [I - Structure principale](#i---structure-principale)
            - [II - Le fichier de configuration d'un objet](#ii---le-fichier-de-configuration-dun-objet)
            - [III - Le fichier de configuration général d'un objet](#iii---le-fichier-de-configuration-général-dun-objet)
            - [IV - Les packs d'objets](#iv---les-packs-dobjets)
        - [VII - Le système de plugins](#vii---le-système-de-plugins)
            - [I - Structure principale](#i---structure-principale-1)
            - [II - Le fichier de configuration d'un plugin](#ii---le-fichier-de-configuration-dun-plugin)
            - [III - Le fichier de configuration général d'un plugin](#iii---le-fichier-de-configuration-général-dun-plugin)
            - [IV - Les packs de plugins](#iv---les-packs-de-plugins)
        - [VIII - Le système de modules](#viii---le-système-de-modules)
            - [I - Structure principale](#i---structure-principale-2)
            - [II - Le fichier de configuration d'un module](#ii---le-fichier-de-configuration-dun-module)
            - [III - Le fichier de configuration général d'un module](#iii---le-fichier-de-configuration-général-dun-module)
    - [IV - Développement plus détaillé des concepts](#iv---développement-plus-détaillé-des-concepts)
        - [I - Plugins par défaut](#i---plugins-par-défaut)
            - [I - Communication](#i---communication)
            - [II - Configuration](#ii---configuration)
            - [III - Filesystem](#iii---filesystem)
            - [IV - Server](#iv---server)
            - [V - Ui](#v---ui)
            - [VI - Community](#vi---community)
            - [VII - Menu](#vii---menu)
            - [VIII - Evolution](#viii---evolution)
        - [II - Objets par défaut](#ii---objets-par-défaut)
            - [I - Date](#i---date)
            - [II - Season](#ii---season)
            - [V - Weather](#v---weather)
            - [IV - Probability](#iv---probability)
            - [V - Consequence](#v---consequence)
            - [VI - Aleatory](#vi---aleatory)
            - [VII - World](#vii---world)
            - [VIII - Rule](#viii---rule)
            - [IX - Obligation_future](#ix---obligation_future)
            - [X - Possibilities](#x---possibilities)
            - [XI - Save](#xi---save)
                - [I - Structure d'une save](#i---structure-dune-save)
            - [XII - Map](#xii---map)
                - [I - Structure d'une map](#i---structure-dune-map)
            - [XIII - Zone](#xiii---zone)
                - [I - Structure d'une zone](#i---structure-dune-zone)
            - [XIV - Entity](#xiv---entity)
        - [III - Modules par défaut](#iii---modules-par-défaut)
            - [I - Executable](#i---executable)
            - [II - Execution](#ii---execution)
            - [III - States](#iii---states)
            - [IV - Loader](#iv---loader)
            - [V - Installator](#v---installator)
                - [I - Installer un module](#i---installer-un-module)
                - [II - Installer un plugin](#ii---installer-un-plugin)
                - [III - Installer un objet](#iii---installer-un-objet)
            - [VI - Object](#vi---object)
            - [VII - Settings](#vii---settings)
            - [VIII - Symbols](#viii---symbols)
            - [IX - Json](#ix---json)
            - [X - Moment](#x---moment)
        - [IV - UI](#iv---ui)
        - [V - Synchronisme](#v---synchronisme)
    - [IV - Idées moins claires](#iv---idées-moins-claires)
        - [I - Dynamisme](#i---dynamisme)
        - [II - Template de création de système](#ii---template-de-création-de-système)
    - [V - Propriétés générales](#v---propriétés-générales)
        - [I - Principe de non-unicité de l'objet](#i---principe-de-non-unicité-de-lobjet)
            - [I - Exemple : l'objet temps](#i---exemple--lobjet-temps)
- [II - Développement](#ii---développement)
    - [I - corǝ](#i---corǝ-1)
        - [I - Avancement : première partie](#i---avancement--première-partie)
            - [I - Json](#i---json)
                - [I - Json.create](#i---jsoncreate)
                - [II - Json.remove](#ii---jsonremove)
                - [III - Json.get](#iii---jsonget)
                - [IV - Json.write](#iv---jsonwrite)
                - [V - Json.exists](#v---jsonexists)
                - [VI - Json.path_to_json](#vi---jsonpath_to_json)
                - [VII - Json.get_from_file](#vii---jsonget_from_file)
                - [VIII - Exemple d'utilisation](#viii---exemple-dutilisation)
            - [II - Settings](#ii---settings)
                - [I - Settings.create](#i---settingscreate)
                - [II - Settings.remove](#ii---settingsremove)
                - [III - Settings.get](#iii---settingsget)
                - [IV - Settings.write](#iv---settingswrite)
                - [V - Settings.enable](#v---settingsenable)
                - [VI - Settings.disable](#vi---settingsdisable)
                - [VII - Exemple d'utilisation](#vii---exemple-dutilisation)
            - [III - States](#iii---states-1)
                - [I - States.create](#i---statescreate)
                - [II - States.write](#ii---stateswrite)
                - [III - States.get](#iii---statesget)
                - [IV - States.exists](#iv---statesexists)
                - [V - Exemple d'utilisation](#vi---exemple-dutilisation)
            - [IV - Executable](#iv---executable)
                - [I - Executable.execute](#i---executableexecute)
                - [II - Exemple d'utilisation](#ii---exemple-dutilisation)
            - [V - Execution](#v---execution)
                - [I - Exemple d'utilisation](#i---exemple-dutilisation)
            - [VI - Object](#vi---object-1)
                - [I - Exemple d'utilisation](#i---exemple-dutilisation)
            - [VII - Loader](#vii---loader)
                - [I - Loader.load](#i---loaderload)
                - [II - Loader.get](#ii---loaderget)
                - [III - Exemple d'utilisation](#iii---exemple-dutilisation)
            - [VIII - Symbols](#viii---symbols-1)
                - [I - Symbols.create](#i---symbolscreate)
                - [II - Symbols.write](#ii---symbolswrite)
                - [III - Symbols.get](#iii---symbolsget)
                - [IV - Exemple d'utilisation](#iv---exemple-dutilisation)
            - [I - Installator](#i---installator)
            - [II - Moment](#ii---moment)
                - [I - Moment.create](#i---momentcreate)
                - [II - Moment.write](#ii---momentwrite)
                - [III - Moment.next_moment](#iii---momentnext_moment)
                - [IV - Moment.previous_moment](#iv---momentprevious_moment)
                - [V - Moment.get](#v---momentget)
                - [VI - Exemple d'utilisation](#vi---exemple-dutilisation)
            - [III - Scheduler](#iii---scheduler)
                - [I - Scheduler.create](#i---schedulercreate)
                - [II - Scheduler.write](#ii---schedulerwrite)
                - [III - Scheduler.get](#iii---schedulerget)
                - [IV - Scheduler.run](#iv---schedulerrun)
                - [V - Scheduler.execute_objects](#v---schedulerexecute_objects)
                - [VI - Exemple d'utilisation](#vi---exemple-dutilisation-1)
        - [II - Problème](#ii---problème)
            - [I - Ce qui est plutôt réussi](#i---ce-qui-est-plutôt-réussi)
            - [II - Ce qu'il manque](#ii---ce-quil-manque)
        - [III - Proposition de solution](#iii---proposition-de-solution)
            - [I - Objet classique](#i---objet-classique)
                - [I - Le modèle d'appel tour par tour](#i---le-modèle-dappel-tour-par-tour)
                - [II - Le modèle d'annulation tour par tour](#ii---le-modèle-dannulation-tour-par-tour)
            - [II - Objet complexe](#ii---objet-complexe)
                - [I - Fonctionnement](#i---fonctionnement)

## II - Préambule

### I - Sujet

Il s'agit d'un projet scolaire, les contraintes du sujet sont :
- Le langage de programmation utilisé doit être Python.
- Le thème est : la nature (mieux vaudrait éviter le hors-sujet).
- Le temps imparti est d'environ 2 mois et demi.
- L'utilisation de l'intelligence artificielle est autorisée mais doit être déclarée.
- C'est un projet que je réalise seul.

Tout ce que j'écris ici est le fruit de ma réflexion personnelle, **aucune** intelligence artificielle ne sera utilisée, ni aucun concept / tutoriel venant d'internet d'ailleurs. Les seules choses que je m'autorise à utiliser pour ce projet sont les modules et leurs documentations.

### II - Idée initiale

Le projet est de réaliser un portail de simulation de vie, en Python.  
Nous appelons cela un portail, car l'idée est de faire en sorte qu'il soit dynamique, et non statique.  
L'idée est donc de faire en sorte que l'utilisateur puisse créer ses propres mondes, en pouvant "absolument" tout modeler, sans pour autant avoir à se plonger dans le code source du projet.  
Par "absolument tout modeler", nous n'entendons pas une liste très grandes d'options, puisque c'est l'utilisateur qui créera les options.  
Par "c'est l'utilisateur qui créera les options", nous n'entendons pas une grande liste de propriétés qu'il peut séléctionner.  
L'utilisateur pourra créer quelque chose en partant de "zéro", mais nous y reviendrons.  

Le but de tout cela est simplement d'observer l'évolution d'objets dans un monde spécifique à certaines règles.  
C'est la véritable idée initiale. Elle est plutôt simple, mais nous l'avons complexifié grâce à la non-contextualité (ou dynamisme).  

Mais cette complexification a tout de même un but, ce n'est pas complexifier pour complexifier.  
L'idée est que tout pourrait être représentable dans cette application.  
C'est cette complexité qui fait que ce projet scolaire est relativement intéressant, le fait de se dire que l'humanité pourrait être représentée dans ce portail, par exemple.  

Le nom choisi pour ce projet est `core`.  
En anglais, il signifie `coeur`, ou encore `noyau`.  
Il semble approprié, puisque ce que nous développons est un `moteur`.  
Mais pour ne pas mélanger les concepts, nous appelerons cela un `portail`.

### III - Un petit peu de désabstraction

Dans cette documentation, voici la définition de ce que nous appelerons objets :

```
Tout est objet, mis à part le moteur.
```

Donc :
- toute chose, aussi abstraite soit elle, est un objet si elle n'est pas le moteur (ce que nous développons).
- le temps, la vie, l'espace, les mondes, les êtres, ..., sont objets.

## III - Concepts

### I - Le moteur du portail

Le moteur du portail est (aussi) nommé `core`.  
Il est (ou sa plus grande part) `statique`.  
C'est un `module`.  
Il est présent dans `core/modules/core`.  

L'utilité du moteur est assez simple : il permet de load des objets, de définir les classes requises au bon fonctionnement de l'application, de définir des symboles, etc.

### II - Les paramètres statiques

Les paramètres statiques se trouvent dans `core/module/core/json/settings.json` :
- `<version>` : le numéro de version actuel du programme.
- `<minimum_version>` : le tout premier numéro de version du programme.
- `<maximum_version>` : le tout dernier numéro de version du programme.
- `<plugin_folder>` : le chemin vers le dossier contenant les plugins.
- `<plugin_config>` : le chemin vers le fichier contenant les configurations des plugins.
- `<module_folder>` : le chemin vers le dossier contenant les modules.
- `<module_config>` : le chemin vers le fichier contenant les configurations des modules.
- `<object_folder>` : le chemin vers le dossier contenant les objets.
- `<object_config>` : le chemin vers le fichier contenant les configurations des objets.

Nous avons fait ce choix pour diluer le statisme en une sorte de non-contextualité.  
Avec cela, l'utilisateur pourra modeler le statisme (noms de champs, etc).

### III - Les systèmes

Un système est le fruit d'une complémentarité : il est composé de modules, de plugins, et d'objets.  
Le dossier pour les systèmes est actuellement `core/`.  

### IV - Les objets

Les objets sont les "choses" que nous développons.  
Il en existe trois types :
- `Object` : un objet de type `Object`.
- `Plugin` : un objet de type `Plugin`.
- `Module` : un objet de type `Module`.

Nous reviendrons prochainement sur les définitions et différences de ces types d'objets.

### V - Valeurs JSON

Voici tous les paramètres (communs) qui peuvent revenir dans les fichiers JSON, et leurs significations.  
Nous nommerons cela `objet`, puisqu'il peut s'agir d'un objet de type `Module`, `Plugin`, ou bien `Object` :

- `version` (data) : il s'agit de la version de l'objet.
- `name` (data) : il s'agit du nom de l'objet.
- `type` (data) : indique le type de l'objet. Actuellement, il peut s'agir d'un objet, d'un plugin, ou bien d'un module.
- `module` (data) : si présent, il indique le module associé.
- `plugin` (data) : si présent, il indique le plugin correspondant.

- `requires` (objet) : il s'agit des pré-requis pour l'exécution de l'objet.
- `requires/modules` (objet) : il s'agit des modules pré-requis pour l'exécution de l'objet.
- `requires/plugins` (objet) : il s'agit des plugins pré-requis pour l'exécution de l'objet.
- `requires/application` (objet) : il s'agit d'une configuration requise spécifique à l'application pour l'exécution de l'objet.
- `requires/application/minimum_version` (data) : la version minimale de l'application, pour exécuter l'objet.
- `requires/application/maximum_version` (data) : la version maximale de l'application, pour exécuter l'objet.

- `execution` (objet) : il s'agit d'un champ concernant les objets d'exécution.
- `execution/methods` (array) : un array contenant les méthodes de l'objet.
- `execution/macros` (array) : un array contenant les macros de l'objet.

Que ce soit une méthode ou une macro, ce sont des objets de configuration pour le type `Executable` (nous y reviendrons).  

Et pour finir, nous appelerons `type` le type d'objet implémenté (`Object`, `Plugin`, `Module`).
- `sub_{type}s` (array) : un array contenant les noms des sous-objets implémentés (sous-objets, sous-plugins, sous-modules).

### VI - Le système d'objets

Un objet est la couche la plus basse dans la hiérarchie des systèmes.  
Il contient son propre code d'implémentation.  
Un objet est plus bas qu'un plugin.

#### I - Structure principale

```
.
├── object1
│   ├── object1.json
│   └── object1.py
├── object2
│   ├── object2.json
│   └── object2.py
└── object3
    ├── object3.json
    └── object3.py
```

A noter que ce dossier se trouve dans `<object_folder>`, et que le fichier de configuration se trouve dans `<object_config>`.  
Il faut aussi prendre conscience du fait que les paths des fichiers `.py` ne sont en rien statiques, c'est un exemple.

#### II - Le fichier de configuration d'un objet

``` json
{
    "version": "x.x.x",
    "name": "object_name",
    "module": "object_associated_module",
    "plugin": "object_associated_plugin",
    "type": "Object",
    "requires":
    {
        "modules": {},
        "plugins": {},
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "execution":
    {
        "methods":
        [
            {
                "name": "name",
                "file": "object_py_file_path",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "method1_name",
                    "result":
                    {
                        "true": 1,
                        "false": 0
                    },
                    "execution_conditions":
                    [
                        {
                            "macro": "macro1_name",
                            "result":
                            {
                                "true": 1,
                                "false": 0
                            },
                            "execution_conditions":
                            [
                                {
                                    "name": "name",
                                    "file": "py_path_of_file_containing_check",
                                    "process_type": "import",
                                    "execution":
                                    {
                                        "mode": "exec",
                                        "content": "method_name",
                                        "result":
                                        {
                                            "true": 1,
                                            "false": 0
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ],
        "macros":
        [
            {
                "name": "name",
                "file": "macro_py_file",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "func1"
                }
            },
            {
                "name": "name",
                "file": "macro_py_file",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "all"
                }
            }
        ]
    },
    "sub_objects":
    [
        "object_name1", "object_name2", "object_name3"
    ]
}
```

#### III - Le fichier de configuration général d'un objet

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<object_config>`.  

Il s'agit d'un index contenant les objets du dossier, ainsi que de potentiels paramètres encore indéfinis.  

Voici sa structure actuelle :

``` json
{
    "objects":
    {
        "object1":
        {
            "param": "value"
        },
        "object2":
        {
            "param": "value"
        }
    }
}
```

#### IV - Les packs d'objets

Un pack d'objets permet d'installer plusieurs objets en une fois.  
Le format pour cela est un fichier `.zip` :

```
object_pack1.zip
├── object1
│   ├── object1.json
│   └── object1.py
├── object2
│   ├── object2.json
│   └── object2.py
└── object3
    ├── object3.json
    └── object3.py
```

### VII - Le système de plugins

Un plugin est un objet.  
Cependant, il est plus bas niveau qu'un objet de type `Object`.  

Pour le moment, la structure entre un objet de type `Plugin` et `Object` est la même.

#### I - Structure principale

```
.
├── plugin1
│   ├── plugin1.json
│   └── plugin1.py
├── plugin2
│   ├── plugin2.json
│   └── plugin2.py
└── plugin3
    ├── plugin3.json
    └── plugin3.py
```

A noter que ce dossier se trouve dans `<plugin_folder>`, et que le fichier de configuration se trouve dans `<plugin_config>`.  
Il faut aussi prendre conscience du fait que les paths des fichiers `.py` ne sont en rien statiques, c'est un exemple.

#### II - Le fichier de configuration d'un plugin

``` json
{
    "version": "x.x.x",
    "name": "plugin_name",
    "module": "plugin_associated_module",
    "plugin": "plugin_associated_plugin",
    "type": "Plugin",
    "requires":
    {
        "modules": {},
        "plugins": {},
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "execution":
    {
        "methods":
        [
            {
                "name": "name",
                "file": "plugin_py_file_path",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "method1_name",
                    "result":
                    {
                        "true": 1,
                        "false": 0
                    },
                    "execution_conditions":
                    [
                        {
                            "macro": "macro1_name",
                            "result":
                            {
                                "true": 1,
                                "false": 0
                            },
                            "execution_conditions":
                            [
                                {
                                    "name": "name",
                                    "file": "py_path_of_file_containing_check",
                                    "process_type": "import",
                                    "execution":
                                    {
                                        "mode": "exec",
                                        "content": "method_name",
                                        "result":
                                        {
                                            "true": 1,
                                            "false": 0
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ],
        "macros":
        [
            {
                "name": "name",
                "file": "macro_py_file",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "func1"
                }
            },
            {
                "name": "name",
                "file": "macro_py_file",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "all"
                }
            }
        ]
    },
    "sub_plugins":
    [
        "plugin_name1", "plugin_name2", "plugin_name3"
    ]
}
```

#### III - Le fichier de configuration général d'un plugin

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<plugin_config>`.  

Il s'agit d'un index contenant les plugins du dossier, ainsi que de potentiels paramètres encore indéfinis.  

Voici sa structure actuelle :

``` json
{
    "plugins":
    {
        "plugin1":
        {
            "param": "value"
        },
        "plugin2":
        {
            "param": "value"
        }
    }
}
```

#### IV - Les packs de plugins

Un pack de plugins permet d'installer plusieurs plugins en une fois.  
Le format pour cela est un fichier `.zip` :

```
plugin_pack1.zip
├── plugin1
│   ├── plugin1.json
│   └── plugin1.py
├── plugin2
│   ├── plugin2.json
│   └── plugin2.py
└── plugin3
    ├── plugin3.json
    └── plugin3.py
```

### VIII - Le système de modules

Un objet de type `Module` est différent des objets de type `Plugin` ou `Object`.  
Sa structure est beaucoup plus complexe et abstraite.

Nous allons prendre l'exemple du moteur (`core/modules/core`), puisqu'il n'existe pas de structure générale, pour le moment.

#### I - Structure principale

```
.
├── json
│   ├── settings.json
│   └── symbols
│       └── symbols.json
└── scripting
    ├── module1_name
    │   ├── module1_name.py
    ├── module2_name
    │   └── module2_name.py
    ├── module3_name
    │   └── module3_name.py
    └── module4_name
        └── module4_name.py
```

Pour le moment :
- `core/modules/core/json` contient les données statiques de l'application.
- `core/modules/core/scripting` contient les implémentations des sous-modules du moteur.

A noter que ce dossier se trouve dans `<module_folder>`, et que le fichier de configuration se trouve dans `<module_config>`.

#### II - Le fichier de configuration d'un module

``` json

```

#### III - Le fichier de configuration général d'un module

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<module_config>`.  

Il s'agit d'un index contenant les modules du dossier, ainsi qu'un booléen indiquant si ils sont actifs ou non.  

Voici sa structure actuelle :

``` json
{
    "modules":
    {
        "core":
        {
            "enabled": true
        }
    }
}
```

## IV - Développement plus détaillé des concepts

### I - Plugins par défaut

Voici une liste plutôt précise des plugins par défaut.

#### I - Communication

Ce plugin sert à la communication avec l'Internet.  
Il se trouve dans `core/plugins/communication`.

#### II - Configuration

Il se trouve dans `core/plugins/configuration`.

#### III - Filesystem

Il se trouve dans `core/plugins/filesystem`.

#### IV - Server

Il se trouve dans `core/plugins/server`.

#### V - Ui

Il se trouve dans `core/plugins/ui`.

#### VI - Community

Une communauté est un espace publique qui regroupe des partages d'objets, de règles, de mondes, en ligne.  
Chaque objet, règle, monde, ou autre de la communauté a un identifiant unique de 10 chiffres : `0123456789`.  
Ce plugin permettra d'intéragir avec.

#### VII - Menu

Il y aura globalement deux options :
- Lancement local : on demande à l'utilisateur de sélectionner le dossier de son monde, si il ne se trouve pas dans le dossier par défaut.
- Lancement serveur : on demande à l'utilisateur de saisir l'identifiant unique de son monde, ainsi que l'url vers le serveur communautaire.

#### VIII - Evolution

Un objet peut subir des évolutions (mutations).  
Le plugin evolution permet de faire évoluer des objets en d'autres objets (ou autres modifications).

### II - Objets par défaut

#### I - Date

Cet objet permet d'implémenter un système de dates.  
Toutes les règles sont faisables, dans la limite du possible (performances de l'ordinateur, enjeux de mémoire, etc).  
Voici quelques idées de choses qui devraient être rendues possibles :  
- L'utilisateur pourra (par exemple) créer un système de dates où les jours sont deux par deux (1, 3, 5, ...), etc.  
- Il pourrait aussi créer un monde où, la date va à rebours : 31, 30, 29, ...  
- Ou bien encore imaginer un système de date totalement différent, qui repose sur des calculs aléatoires, pour définir quel jour nous sommes !
- Ou une boucle temporelle : nous revenons à la même date, en boucle

#### II - Season

Cet objet implémente le type d'objet `Season`.  

#### III - Weather

Cet objet implémente le type d'objet `Weather`, un système de météo.  
Nous pourrons y lier des objets de types `Probability`, `Consequence`, ...  
Par exemple, la probabilité de pluie en novembre pourrait être de 70%.  
Et pour les conséquences, la pluie fait monter les niveaux d'eau.

Voici quelques idées de choses qui devraient être rendues possibles :
- Il sera aisé de créer une nouvelle météo, par exemple un temps où il pleut de l'électricité
- Le sens n'est pas obligatoirement unidirectionnel. La plupart du temps, la météo vient de l'exterieur vers l'intérieur, mais ce n'est pas nécessairement le cas ici. Par exemple, une météo pourrait être une planète qui renvoie de l'eau qui monte au ciel (par une loi de type law)

#### IV - Probability

Cet objet implémente le type d'objet `Probability`, un système de probabilité.  

Une représentation simple de probabilité pourrait être une valeur comprise entre 0 et 1.  

Voici quelques idées de choses qui devraient être rendues possibles :
- Les autres objets peuvent ensuite utiliser ce système de probabilités, pour les apparitions etc
- `Probability` n'est qu'un nom, on peut très bien imaginer un faux système derrière cela
- Les méthodes de représentation peuvent changer, ce n'est pas obligatoirement une valeur entre 0 et 1. Par exemple : cela pourrait être des sentiments, un string, ou autre.

#### V - Consequence

Cet objet implémente le type d'objet `Consequence`, un système de conséquence (déterminisme).  

Cela pourrait globalement permettre d'implémenter ce qu'il se passe si [...].  

Voici quelques idées de choses qui devraient être rendues possibles :
- Une conséquence d'avant-apparition : ce qu'il se passe pour que l'évènement se produise. Par exemple : les fleurs poussent grâce à la pluie (en partie).
- Une conséquence d'après-apparition : ce qu'il se passe à la suite de l'évènement, ce qu'il engendre. Par exemple : les fleurs qui éclosent permettent aux bourdons de venir butiner.

#### VI - Aleatory

Cet objet implémente le type d'objet `Aleatory`, un système d'aléatoire.  
L'aléatoire n'existant pas en informatique classique, il serait par exemple possible d'utiliser des API comme random.org, en cas de besoin.  

Cet objet pourrait implémenter plusieurs types d'aléatoires : les pseudo-aléatoires, etc.

#### VII - World

Cet objet implémente le type d'objet `World`, un système de monde.  
Un monde est un objet, d'un point de vu de type pur.  
Mais d'un point de vu "extérieur" (utilisateur), c'est une structure contenant d'autres objets.  

Un monde pourrait par exemple être constitué des objets suivants :
- D'un ensemble de règles (rule)
- D'un ensemble d'entités
- D'un système d'écoulement d'instants
- D'un système de saison
- D'un système de météo
- ...

Un objet de type `World` devrait pouvoir "contenir" tout objet.

#### VIII - Rule

Cet objet implémente le type d'objet `Rule`, un système de règles.  
Ce sont les propriétés fondamentales du monde, par exemple : la gravité.  

Ces règles ne sont pas contredites pas les objets, par défaut.  
Cependant, des paramètres spécifiques pourront être développés si un objet ne doit pas respecter une règle (ou plusieurs).  
Nous faisons ce choix en pensant avant tout au dynamisme, nous ne voulons pas ajouter de contraintes statiques (telle chose obligatoire pour tous les objets).  

#### IX - Obligation_future

Cet objet implémente le type d'objet `Obligation_future`, un système d'obligations futures.  
Les obligations futures sont des conditions faites pour altérer le futur du monde et des objets qui y vivent.  
L'objectif est de créer plusieurs scénarios possibles en fonction d'une obligation future, pour permettre à l'utilisateur de modeler le futur de son monde.  
Exemple : si nous avons un groupe d'entités qui vivent ensembles, et qu'une entité externe attaque une entité de ce groupe, alors il pourrait y avoir conflit.  
On peut forcer le conflit, pour voir ce qu'il va se passer, en posant cette obligation future : entité 1 attaque entité 2 tel jour.  
L'utilisateur peut donc forcer un objet (conscient et "libre") à faire une chose à un instant T.

#### X - Possibilities

Cet objet implémente le type d'objet `Possibilities`, un système de possibilités (scénarios).  

#### XI - Save

Cet objet implémente le type d'objet `Save`, un système de sauvegarde.  

Par défaut, un monde pourra être sauvegardé de deux manières :
- Localement : le dossier de sauvegarde du monde sera enregistré sur le disque de l'utilisateur.
- En ligne : le dossier de sauvegarde du monde sera enregistré sur un serveur.

##### I - Structure d'une save

Voici la structure JSON d'un objet de type `Save`, par défaut :

``` json
{
    "states":
    {
        "state1_name":
        {
            "state1_param1": "value1",
            "state1_param2":
            [
                "value2", 100
            ],
            "state1_param3":
            {
                "param1": 1.0
            }
        },
        "state2_name":
        {
            "state2_param1": "value1",
            "state2_param2":
            [
                "value2", 100
            ],
            "state2_param3":
            {
                "param1": 1.0
            }
        }
    }
}
```

- `states` : les states écrivent dans ce champ leurs données qui seront réstaurées à la prochaine exécution du programme.  
Attention : cela ne doit pas être des adresses d'objets, car elles sont dynamiques. Ce sont bien des données, en JSON par exemple.

#### XII - Map

Cet objet implémente le type d'objet `Map`, un système de maps.  
Une map est un ensemble qui contient des objets de type `Zone`.

##### I - Structure d'une map

Voici une potentielle structure d'une map :

``` json
{
    "zones":
    {
        "zone1_id":
        {
            "position":
            {
                "x": 1,
                "y": 1
            }
        },
        "zone2_id":
        {
            "position":
            {
                "x": 2,
                "y": 2
            }
        },
        "zone3_id":
        {
            "position":
            {
                "x": 3,
                "y": 3
            }
        },
    }
}
```

- `zones` : champ contenant les zones de la map.
- `zones/{id}` : les informations de la zone utiles à la map.
- `zones/{id}/position` : les informations concernant la position de la zone dans la map.
- `zones/{id}/position/x` : la position x de la zone dans la map.
- `zones/{id}/position/y` : la position y de la zone dans la map.

Ici, on observe que les coordonnées des zones formeraient une nouvelle "tuile" de map :

```
zone 1 (100x100) : x = 0, y = 0
zone 2 (100x100) : x = 0, y = 1
zone 3 (100x100) : x = 0, y = 2
```

Les zones n'utiliseraient donc pas les mêmes coordonnées que la map.  
Je ne sais pas vraiment si cela sera le cas dans la version développée, mais c'est probable.

#### XIII - Zone

Cet objet implémente le type d'objet `Zone`, un système de zones.  

##### I - Structure d'une zone

Voici ce qui pourrait être une structure de zone :

``` json
{
    "objects":
    {
        "object_type1":
        {
            "object1_id":
            {
                "in_life": true,
                "visible": true,
                "position":
                {
                    "x": 100,
                    "y": 200
                }
            },
            "object2_id":
            {
                "in_life": false,
                "visible": true,
                "position":
                {
                    "x": 100,
                    "y": 200
                }
            },
            "object3_id":
            {
                "in_life": false,
                "visible": false,
                "position":
                {
                    "x": 100,
                    "y": 200
                }
            }
        }
    }
}
```

- `objects` : les éléments présents dans la zone.
- `objects/{type}` : les éléments des mêmes types sont groupés.
- `objects/{type}/{id}` : les informations propres à un objet unique.
- `objects/{type}/{id}/in_life` : booléen indiquant si l'objet est en vie.
- `objects/{type}/{id}/visible` : booléen indiquant si l'objet est visible.
- `objects/{type}/{id}/position` : champ concernant la position de l'objet dans la zone.
- `objects/{type}/{id}/position/x` : la position x de l'objet dans la zone.
- `objects/{type}/{id}/position/y` : la position y de l'objet dans la zone.

Notons que pour le moment, ce fichier est très contextuel.  
En effet, une grande partie de ce schéma vient du premier fichier `old/preambule.md`.  
La structure doit être adaptée.

#### XIV - Entity

Cet objet implémente le type d'objet `Entity`, un système d'entités.  

Par défaut, il pourrait exister 3 types d'entités :
- L'entité consciente libre : il s'agit d'une entité qui a une conscience et qui est libre de ses mouvements. Par exemple : un oiseau.
- L'entité consciente : il s'agit d'une entité qui a une conscience, mais qui n'est pas vraiment libre de ses déplacements. Par exemple : une plante, bien qu'elle grandisse.
- L'entité non-consciente non-vivante : il s'agit d'une entité qui n'a ni conscience, ni liberté. Par exemple : une table.

### III - Modules par défaut

#### I - Executable

Il s'agit d'une classe implémentant le type `Executable`.  
Pour initialiser un exécutable, on passe au constructeur un dict / json de configuration, et l'objet states.  

Pour le moment, nous ne faisons pas de réelle distinction entre une macro et une méthode, car la structure est très similaire.  
Si cela venait à changer, des classes `Macro`, `Method`, `Function` pourraient être implémentées.  

Voici ce que doit contenir un dict de configuration :

``` json
{
    "type": "method",
    "name": "add_check_function",
    "file": "core/objects/cell/cell_check.py",
    "process_type": "import",
    "execution":
    {
        "mode": "exec",
        "content": "add_check_function_macro",
        "result":
        {
            "true": 1,
            "false": 0
        }
    }
}
```

Mais si le `type` est `macro`, alors `result` peut ne pas être passé : il sera implémenté par la config qui appelle la macro.  

Un paramètre `execution_conditions` peut être présent pour des checks de pré-exécution :

``` json
{
    "name": "name",
    "file": "plugin_py_file_path",
    "process_type": "import",
    "execution":
    {
        "mode": "exec",
        "content": "add",
        "result":
        {
            "true": 1,
            "false": 0
        },
        "execution_conditions":
        [
            {
                "macro": "macro1_name",
                "result":
                {
                    "true": 1,
                    "false": 0
                },
                "execution_conditions":
                [
                    {
                        "name": "name",
                        "file": "py_path_of_file_containing_check",
                        "process_type": "import",
                        "execution":
                        {
                            "mode": "exec",
                            "content": "method_name",
                            "result":
                            {
                                "true": 1,
                                "false": 0
                            }
                        }
                    }
                ]
            }
        ]
    }
}
```

Ici, cela signifie que `method_name()` de `py_path_of_file_containing_check` doit renvoyer `1` pour que `macro1_name` puisse s'exécuter, qui doit lui-même renvoyer `1` pour que `add()` de `plugin_py_file_path` puisse s'exécuter.  

La méthode `Executable::execute()` permet d'exécuter un objet de type `Executable`.  
Pour le moment, elle ne prend pas de paramètres supplémentaires :

``` python
executable = Executable(executable_config, states)
executable.execute()
```

`self.result_code` contient un booléen qui indique si le retour de la fonction est égal à `result/true`.

#### II - Execution

Il s'agit d'un objet plus haut qu'un exécutable.  
En fait, c'est globalement le contexte d'exécution d'un objet.  
Il contient tous les exécutables d'un objet.

#### III - States

Pour orchestrer le bon fonctionnement de l'application, une classe `States` est présente.  
Chaque classe aura comme attribut d'instance un objet commun de type `States`, pour y inscrire les états en cours.

#### IV - Loader

Il s'agit du module principal permettant de load des objets indéfinis à l'avance, dans le moteur.

#### V - Installator

Ce module est assez semblable au `Loader`, je ne sais pas encore si nous le garderons dans la version finale.  
En tout cas, il se distingue du `Loader` en un point : il est fait pour `installer` un module, de manière permanente.

##### I - Installer un module

``` python
Installator.import(name, value_type)

# exemple : importer le module base
Installator.import("base", "modules")
```

1) Le moteur importe dynamiquement `{value_type}/{name}/_install.py`.  
2) Dans ce fichier, se trouve une classe `_install`, il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_module"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _install
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, le type a été importé dans le moteur.

##### II - Installer un plugin

``` python
# exemple : importer le plugin base
Installator.import("base", "plugins")
```

1) Le moteur importe dynamiquement `{value_type}/{name}/_install.py`.  
2) Dans ce fichier, se trouve une classe `_install`, il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_plugin"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _install
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, le plugin a été importé dans le moteur, ainsi que les noms de méthodes des objets à exécuter, les règles, etc.

##### III - Installer un objet

``` python
# exemple : importer l'objet time
Installator.import("time", "objects")
```

1) Le moteur importe dynamiquement `{value_type}/{name}/_install.py`.  
2) Dans ce fichier, se trouve une classe `_install`, il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_object"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _install
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, l'objet a été importé dans le moteur.

#### VI - Object

Il est load par `Loader`, grâce au fichier de configuration d'un objet.  
Un objet de type `Object` contient globalement `Object.execution` (liste), qui contient des objets de type `Execution` (qui contiennent les objets de type `Executable`).  
Pour le moment, la seule "entrée d'exécution" est le paramètre "execution" du fichier de configuration d'un objet, mais nous avons prévu une liste (ou objet json) au cas où plusieurs champs venaient à être utilisés.

#### VII - Settings

Il s'agit d'un module permettant de créer / gérer des paramètres.

#### VIII - Symbols

C'est un module permettant de gérer des `symboles`.  
Ce sont simplement des variables propres au bon fonctionnement du programme.

#### IX - Json

Il s'agit du module principal pour intéragir avec des objets JSON.

#### X - Moment

Il s'agit d'un module d'écoulement d'instants.  
Nous utilisons "instant" pour parler du temps.  
L'instant est un concept, le temps est un objet.  

L'idée est assez simple à comprendre.  
Chaque instant a une valeur, représentée par le temps, qui est un objet.  
L'instant suivant peut représenter le temps suivant, mais pas obligatoirement.  
Par contre, il devrait toujours y avoir un écoulement d'instants, je crois.  

Pour voir l'évolution de son monde, l'utilisateur doit donc pouvoir moduler les instants : passer tant d'instants, aller à un instant, etc.

#### XI - Scheduler

Il s'agit d'un module d'ordonnancement pour l'exécution des objets à un `Moment`.  
L'idée est que des objets de type `Object` (les processus) sont tout d'abord ajoutés à une liste (tâches).  
Ensuite, ils sont tous exécutés de manière asynchrone, avec une éventuelle limite pour des raisons de performances.  
Grâce aux états de type `States`, nous attendrons que toutes les exécutions soient terminées avant de poursuivre d'éventuelles actions.

### IV - UI

Pour l'UI, nous utiliserons très probablement `fastapi`, car il est plus fait pour le fonctionnement asynchrone que flask.  
Nous optons pour un render web car, tout doit être modelable, c'est probablement bien plus simple de modifier du code source HTML / CSS / JS qu'une application tkinter, par exemple.  

Car je ne l'ai pas forcément précisé, mais l'interface en elle-même devra être non-contextuelle.  

### V - Synchronisme

Les tâches s'exécutent de manière asynchrone, c'est à dire indépendamment les unes des autres, en même temps.  
Pour cela, le module principal utilisé est `asyncio`, on déclare la fonction `main()` en `async def`.  
Par exemple, pour le serveur :
``` python
server = Server(states)
asyncio.run(server.run())

# les lignes suivantes seront exécutées en même temps
```
Puis, l'idée est de tout gérer avec states, pour coordonner les actions entre elles, même asynchrones.  
Voici la toute première state :
``` python
states = States()
states.create("app")
states.write("app/status", "on")
```

On peut ensuite faire quelque chose comme cela :
``` python
while states.get("app/status") != "off":
    # boucle principale de l'app
```

### VI - Asynchronisme : plan

Ce que l'on souhaite, c'est que chaque objet puisse être exécuté en même temps qu'un autre.  
C'est pour cela que chaque objet (classe) doit être déclaré en asynchrone. Voici ce que nous entendons par cela :
- la méthode `__init__` ne peut pas être asynchrone en Python, elle initialise donc uniquement des `self.<something> = None`.
- la véritable méthode d'init est nommée `init`, elle est requise pour tout objet (sauf si les self restent None ?).
- toutes les méthodes (sauf `__init__`) sont `async`.
- il faut utiliser le moins de fonctions / méthodes bloquantes dans ces méthodes.

## IV - Idées moins claires

### I - Dynamisme

Le principe est que le programme soit le moins contextuel possible, c'est pour cela que l'on parle de développement d'un portail.  
Pour cela, plusieurs fonctions dynamiques propres à python peuvent être utilisées :
- `exec()` : permet d'exécuter du code python, sans compilation
- `eval()` : permet d'évaluer une expression, sans compilation
- `write()` : permet de (ré)écrire le propre code du programme, sans compilation

Si la non-contextualité est correctement développée, nous pourrions ne pas avoir à utiliser ces fonctions.

### II - Template de création de système

## V - Propriétés générales

Il s'agit d'une petite liste de propriétés générales que la version finale devrait adopter.

### I - Principe de non-unicité de l'objet

La propriété est simple : un objet peut apparaître autant de fois que nous le souhaitons dans un monde. Et ce, pour tout objet.  
Cela signifie que même pour des objets plus "abstraits", cela devrait être possible.  

(Sauf si une propriété de l'objet dit le contraire, bien entendu.)

#### I - Exemple : l'objet temps

Cela signifie donc qu'un monde peut avoir plusieurs temps, indépendants les uns des autres.  
Pour un monde qui développe plusieurs planètes, cela pourrait être assez courant.  

Cependant, même pour un monde qui n'en développe qu'une seule, nous pourrions imaginer que dans une certaine plage de coordonnées, l'objet temps n'est pas le même et fonctionne différement.  

Et nous ne parlons pas d'un simple décalage, comme on pourrait observer sur Terre entre une horloge en haut d'une montagne et une horloge plus basse.  
Nous parlons vraiment de définitions différentes, nous pourrions imaginer que dans une plage de coordonnées, le temps irait à rebours, quand dans une autre plage de coordonnées, il "tournerait" "normalement".

# II - Développement

La documentation du moteur et de l'application étant déjà bien avancéee, nous allons pouvoir commencer à discuter du développement ici même.  

Je vais essayer garder un semblant de logique liée à la chronologie, même si j'ai en réalité commencé à tout développer dans le désordre pour avoir une idée de la structure.  
Les fichiers pythons existent déjà, mais ce sont des bétas.  
Si ils apparaissent plus bas, c'est que leur logique a été approuvée / refactorisée.

## I - corǝ

Tout d'abord, nous allons développer le module `core` (moteur).  

### I - Avancement : première partie

#### I - Json

``` python
__init__(self)
```

``` python
async init(self)
```

##### I - Json.create

``` python
async create(self, name)
```

##### II - Json.remove

``` python
async remove(self, path)
```

##### III - Json.get

``` python
async get(self, path)
```

##### IV - Json.write

``` python
async write(self, path, value, mode = 0)
```

##### V - Json.exists

``` python
async exists(self, path)
```

##### VI - Json.path_to_json

``` python
async path_to_json(self, path)
```

##### VII - Json.get_from_file

``` python
async get_from_file(self, path)
```

##### VIII - Exemple d'utilisation

``` python
json = Json()
await json.init()
await json.create("a")
await json.write("a/b", "test")

print(await json.path_to_json("a/b"))
# ["a"]["b"]

print(await json.get("a/b"))
# test

await json.remove("a/b")

print(await json.exists("a"))
# True

print(await json.exists("a/b"))
# False

await json.write("a/b", await json.get_from_file("core/modules/core/json/settings.json"))
```

#### II - Settings

``` python
__init__(self)
```

``` python
async init(self, states, loader)
```

##### I - Settings.create

``` python
async create(self, name)
```

##### II - Settings.remove

``` python
async remove(self, name)
```

##### III - Settings.get

``` python
async get(self, path)
```

##### IV - Settings.write

``` python
async write(self, path, value, mode = 0)
```

##### V - Settings.enable

``` python
async enable(self, settings_path, enabled_name, enabled_type)
```

##### VI - Settings.disable

``` python
async disable(self, settings_path, disabled_name, disabled_type)
```

##### VII - Exemple d'utilisation

``` python
settings = Settings()
await settings.init(states, loader)

await settings.create("a")
await settings.write("a/b", "value")

print(await settings.get("a"))
# {'b': 'value'}

await settings.write("a/enabled", "")

await settings.enable("a/enabled", "core", "module")
await settings.disable("a/enabled", "core", "module")

await settings.remove("a")
```

#### III - States

``` python
__init__(self)
```

``` python
async init(self)
```

##### I - States.create

``` python
async create(self, name)
```

##### II - States.write

``` python
async write(self, path, value)
```

##### III - States.get

``` python
async get(self, path)
```

##### IV - States.exists

``` python
async exists(self, path)
```

##### V - Exemple d'utilisation

``` python
states = States()
states.init()

await states.create("app")
await states.write("app/value", "on")

if await states.exists("app/value"):
    if await states.get("app/value") == "on":
        print("app is on !")
        # app is on !
```

#### IV - Executable

``` python
__init__(self)
```

``` python
async init(self, config, states, macros = None)
```

##### I - Executable.execute

``` python
async execute(self, logs = False)
```

##### II - Exemple d'utilisation

``` python
executable = Executable()
await executable.init(config, states)
await executable.execute()
```

#### V - Execution

``` python
__init__(self)
```

``` python
async init(self, config, states)
```

##### I - Exemple d'utilisation

``` python
execution = Execution()
await execution.init(config, states)
```

#### VI - Object

``` python
__init__(self)
```

``` python
async init(self, config, states)
```

##### I - Exemple d'utilisation

``` python
obj = Object()
await obj.init(config, states)
```

#### VII - Loader

``` python
__init__(self)
```

``` python
async init(self, states, module_path, plugin_path, object_path)
```

##### I - Loader.load

``` python
async load(self, name, load_type)
```

##### II - Loader.get

``` python
async get(self, path)
```

##### III - Exemple d'utilisation

``` python
loader = Loader()
await loader.init(states, "module_folder", "plugin_folder", "object_folder")
await loader.load("communication", "plugin")

print(await loader.get("communication/plugin"))
# [<core.modules.core.scripting.object.object.Object object at 0x10328acf0>]
```

#### VIII - Symbols

``` python
__init__(self)
```

``` python
async init(self, states)
```

##### I - Symbols.create

``` python
async create(self, name)
```

##### II - Symbols.write

``` python
async write(self, path, value)
```

##### III - Symbols.get

``` python
async get(self, path)
```

##### IV - Exemple d'utilisation

``` python
symbols = Symbols()
await symbols.init(states)
await symbols.create("symbols")
await symbols.write("symbols/<version>", "1.0.0")

print(await symbols.get("symbols/<version>"))
# 1.0.0
```

#### I - Installator

#### II - Moment

``` python
__init__(self)
```

``` python
async init(self, states)
```

##### I - Moment.create

``` python
async create(self, name)
```

##### II - Moment.write

``` python
async write(self, path, value)
```

##### III - Moment.next_moment

``` python
async next_moment(self, path)
```

##### IV - Moment.previous_moment

``` python
async previous_moment(self, path)
```

##### V - Moment.get

``` python
async get(self, path)
```

##### VI - Exemple d'utilisation

``` python
```

#### III - Scheduler

``` python
__init__(self)
```

``` python
async init(self, states)
```

##### I - Scheduler.create

``` python
async create(self, name)
```

##### II - Scheduler.write

``` python
async write(self, path, value)
```

##### III - Scheduler.get

``` python
async create(self, path)
```

##### IV - Scheduler.run

``` python
async run(self, path)
```

##### V - Scheduler.execute_objects

``` python
async execute_objects(self, value)
```

##### VI - Exemple d'utilisation

``` python
scheduler = Scheduler()
await scheduler.init(states)
await scheduler.create("task")

while await states.get("app/value") == "on":
    print("=" * 50)
    print(f"moment {await moment.get("time/value1")} : ")

    for obj_name in loader.loader.json:
        await scheduler.write(f"task/{obj_name}", await loader.get(f"{obj_name}/objects"))

    await scheduler.run("task")
    await scheduler.write("task", {})

    print("=" * 50)
    choice = input("time += ? : ")

    if choice == "exit":
        await states.write("app/value", "off")
    else:
        await moment.write("time/value1", await moment.get("time/value1") + int(choice))
```

### II - Problème

#### I - Ce qui est plutôt réussi

La forme actuelle est déjà plutôt bonne pour des objets simples, je ne vais pas remettre cela en question.  
Ce qui me semblait complexe, initialement, était de devoir exécuter des objets que nous ne connaissons pas à l'avance.  
Pour cela, il fallait rendre les objets en "totale" indépendance, pour qu'ils choisissent eux-même quoi exécuter.  
Réussir à exécuter des objets dynamiques (dont la structure n'est pas statique) me semblait compliqué.  
La configuration JSON "statique" plutôt bien pensée a résolu ce problème.  
Ce point est plutôt réussi : il est vrai que, `Moment` après `Moment`, le moteur peut maintenant exécuter des objets indépendants.  

#### II - Ce qu'il manque

Cependant, quelque chose manque.  
Initialement, la couche d'abstraction devait aller plus loin qu'une exécution de choses indéfinies à l'avance, `Moment` après `Moment`.  
La couche d'abstraction disait que tout est objet, sauf le moteur.  
Néanmoins, actuellement, un objet ne peut exister qu'entre les `Moment`, c'est l'origine du problème que je constate.  
Si le serveur `fastapi` permettant l'affichage graphique est un objet, (puisque c'est un objet de type `Plugin`), alors il est fragmenté par les `Moment`.  
Cela signifie que si l'utilisateur choisit de ne pas passer de `Moment`, alors le serveur est stoppé.  

Pourtant, le serveur est bien asynchrone, là n'est pas le problème.  
Le vrai problème vient de la logique actuelle, trop "tour par tour".  

Malheureusement, ce n'est pas le seul problème, car il est causé par quelque chose de plus haut encore.  
Le problème, ce n'est pas vraiment que `Scheduler` lance tour par tour.  
Le problème, c'est l'existence de `Scheduler`.  
Tant que `Scheduler` existe, alors les objets ne peuvent être indépendants.  
Tant que les objets sont exécutés à un moment choisi par le moteur, ils ne peuvent être indépendants.  
Ils sont indépendants, car ils déterminent si ils s'exécutent ou non, mais le problème est que c'est le moteur qui déclenche cette vérification.  

Ils sont donc en indépendance une fois appelés, pas avant.

### III - Proposition de solution

Je pense que pour répondre à ce besoin, il faudrait instaurer deux grands types d'objets.

#### I - Objet classique

Les objets classiques ne seraient pas en état d'indépendance totale.  
Leurs méthodes sont indépendantes, mais des règles strictes concernant l'appel de l'objet existent.  

Il existe ce que l'on appelle des `modèles`.  
Chaque objet classique définit le modèle à utiliser, dans sa configuration.

##### I - Le modèle d'appel tour par tour

Il s'agit du modèle utilisé actuellement.  
Nous appelons l'objet quand nous en avons besoin.

##### II - Le modèle d'annulation tour par tour

Définition simple :

```
Nous ne l'exécutons pas quand nous en avons besoin.
Nous le stoppons quand nous n'en avons plus besoin.
```

Ce serait idéal pour un serveur, par exemple :
- L'objet est load.
- Le moteur comprend qu'il s'agit d'un objet fonctionnant avec le modèle d'annulation tour par tour.
- `Scheduler` le traite différement, il le met dans un autre path.
- A chaque `Moment`, `Scheduler` regarde si les processus fonctionnant avec le modèle d'annulation tour par tour ont un signal d'arrêt (ou autre).
- Si c'est le cas, le processus est stoppé et supprimé du path.

Edit - Après rédaction du concept d'objet complexe :

Je le garde tout de même comme idée, mais je ne pense pas que nous l'utiliserons.  
En fait, je n'en vois pas trop l'utilité, autant utiliser un objet complexe ?

#### II - Objet complexe

Les objets complexes sont en état d'indépendance totale.  
Tous les objets ne peuvent pas être complexes, car cela prend plus de ressources (performances).  
Un objet complexe n'indique pas à `Scheduler` quand l'exécuter.  

##### I - Fonctionnement

Voici une définition :

```
Un objet complexe n'est appelé qu'une seule fois, car il ne termine jamais.
Il contient une boucle asynchrone qui tourne en permanence.
Cette boucle peut faire ses propres vérifications pour savoir si telle méthode doit être exécutée ou non.
```

### IV - Développement et modifications relatives à cette solution

#### I - Structure du fichier de configuration d'un objet

A la racine, deux paramètres sont ajoutés :

``` json
{
    "object_type": "value",
    "object_model": "value",
    ...
}
```

Pour un objet classique :
- `object_type` a pour valeur `classic`.
- `object_model` peut avoir pour valeur `cbc` (call by calling).

Pour un objet complexe :
- `object_type` a pour valeur `complex`.
- `object_model` n'est pas utilisé (pour le moment, il n'existe pas de modèles pour les objets complexes).

#### II - Scheduler

##### I - Scheduler.settings

``` python
async def settings(self, path, value)
```

``` python
scheduler = Scheduler()
await scheduler.init(states)
await scheduler.create("classic_task")
await scheduler.create("complex_task")
await scheduler.settings("classic_task/mode", "classic")
await scheduler.settings("classic_task/model", "")
await scheduler.settings("complex_task/mode", "complex")
```

##### II - Modifications Scheduler.run

Cette méthode contient maintenant des vérifications relatives aux paramètres de l'objet.

##### III - Executable

C'est le corps des changements importants.

###### I - Executable.execute

Cette méthode est maintenant plus longue.  
Elle contient des vérifications relatives aux paramètres de l'objet.  
Si il est classique, alors elle l'exécute avec des `await`.  
Si il est complexe, alors elle l'exécute, mais n'attendra pas qu'il termine (elle l'exécute puis retourne directement, il continue de vivre en background).

###### II - Executable._exec

C'est un pont vers `exec()`, qui permet d'exécuter une liste de strings, ou bien un string directement.  
Si l'objet est complexe :  
Elle définit une fonction avec `exec()` puis sort de celui-ci pour obtenir une coroutine vers la fonction.  
Ensuite, elle lance cette coroutine en arrière plan et retourne.
Si l'objet est classique :
Elle fait la même chose mais avec un `await`, elle ne lance pas en background.

###### III - Résumé simple du processus actuel

Executable.execute :
- obtient l'objet à exécuter
- obtient le contenu de son fichier JSON
- créer un payload (bridge) en fonction de celui-ci (voir plus bas)
- `self._exec(payload, mode = mode)`
- si le mode est classique : cherche à interpréter / stocker les résultats

Voici le bridge actuel utilisé pour `Executable._exec` :

``` python
lines = [
    "import asyncio"
]

# ...

lines.append(f"from {path} import *")

# ...

lines.append("async def bridge():")
lines.append(f"    return await {executable_object.execution_content}()")
```

### V - Résultats

Cela fonctionne toujours bien pour les objets classiques, car "rien ne change pour ceux-ci".  
Le fonctionnement tour-par-tour est toujours bon.  

Nous allons maintenant pouvoir tester avec des objets complexes, il faut commencer par en développer un.  
Mais j'ai pensé à une potentielle question en faisant la séparation entre classique et complexe :  
Un objet complexe ne peut pas contenir de vérifications dans son fichier JSON, comme un objet classique ?  
Car actuellement, un objet complexe est lancé "dans le vide" (background).  
Son comportement est "indéfinit" (d'un point de vu moteur).  
On ne sait pas quand il terminera.  
Mais, en est-il de même pour ses méthodes de vérifications ? Car si c'est le cas, cela serait plus complexe car nous ne pouvons pas `await` le résultat.  
Cependant, si nous partons du principe qu'un objet complexe est en totale indépendance et se gère totalement seul, alors nous pouvons aussi affirmer qu'il n'a pas vraiment besoin d'une telle structure JSON concernant les vérifications.  
Tout ce dont il aurait besoin, c'est d'un point d'entrée.  
Donc la structure JSON d'un objet complexe pourrait ne contenir qu'une seule méthode asynchrone : l'entrée.  
Cette entrée est lancée dans le vide (background) par le moteur, puis tout est géré par l'objet : il est indépendant.  

Sinon, nous aurions pu partir du principe qui dit que les méthodes de vérifications retournent toujours, même pour un objet complexe, mais je pense que la solution précédente est plus adaptée.

### VI - Structure d'un objet complexe

Exemple :

``` json
{
    "version": "1.0.0",
    "object_type": "complex",
    "name": "cellule_complexe",
    "type": "Object",
    "requires":
    {
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "execution":
    {
        "methods":
        [
            {
                "type": "method",
                "name": "entry",
                "file": "core/objects/cellule_complexe/cellule_complexe.py",
                "process_type": "import",
                "execution":
                {
                    "mode": "exec",
                    "content": "entry"
                }
            }
        ]
    }
}
```

Je ne l'ai pas forcément précisé, mais cela fonctionne maintenant bien pour les objets complexes.  
Ils sont pleinement fonctionnels, ils sont bien exécutés en même temps que les objets classiques et sont lancés "dans le vide".

### VI - Code

Une partie du code a été upload.  
C'est la partie qui est considérée comme plutôt "stable" et fonctionnelle.  
Elle a été retravaillée, mais peut toujours contenir des incohérences et des erreurs.  
C'est pour le moment uniquement du code "fonctionnel", je l'ai fais le plus rapidement possible.

### VII - Amélioration(s)

#### I - L'accès aux variables moteur

Il manque une partie importante pour les objets : un objet ne peut actuellement pas accéder aux variables du moteur.  
Par exemple, il ne peut pas accéder aux states.  

Une solution serait `tests/3/3.py`, mais ça nous oblige à mettre les variables importantes en `global`, et elles sont définies dans le moteur, c'est donc statique (`global states`).  

Une autre potentielle solution serait que chaque objet implémente son propre pont, en déclarant en `global` ce qu'il souhaite obtenir.  
Mais cela me semble compliqué pour peu.  

Une dernière possibilité serait d'implémenter une classe `Variables` dans le moteur.  
Cette classe servirait donc à créer des variables et stocker leurs valeurs.  
Il faudrait qu'une seule instance soit partagée / utilisée pour avoir toutes les variables importantes en un seul objet (argument) que l'on pourrait passer au pont.  
En fait, c'est peut-être un petit peu comme mettre toutes les variables en `global`, mais cela me semble plus modelable etc.  
Et en plus, cela pourrait éviter de "polluer" les variables globales (je ne sais pas vraiment si cela affecte les performances générales).  

C'est personnellement l'option qui m'intéresse le plus.  
Je pense en réalité que nous aurions pu faire autrement en réfléchissant autour d'exec, mais je pense que cette classe `Variables` pourra toujours servir.  
Reste à décider ce qui sera des variables de ce type.  
Je pense au moins que tous les objets de modules (du moteur) seront de ce type de variables partagées.

Pour le moment, je n'ai mis que la variable `states` car elle contient déjà tous les objets.  
La structure serait peut-être à revoir : il vaudrait peut-être mieux définir tous les objets comme des `Variable`, puis créer une seule `State` nommée `variable` (par exemple).  
Mais pour le moment, je ne cherche pas vraiment à faire un programme "parfait" (de toute façon, ça ne sera jamais vraiment le cas) : uniquement un programme qui répond aux fonctions que je lui impose.  

C'est donc fonctionnel, les sous-objets (classiques mais surtout complexes) peuvent maintenant accéder aux states.  
Et via ces states, ils peuvent accéder à tous les objets (modules moteur) en direct.  
Par contre, cela implique que leur point d'entré (pointé par le pont) doit avoir pour signature `**kwargs`.  
Mais c'est un statisme contrôlé, et encore une fois l'unique chose cherchée pour le moment est la fonctionnalitée.  
Cela fonctionne.  

Voici un exemple de point d'entré (très simple) :

``` python
async def entry(**kwargs):
    print("server > entry()")

    if "states" in kwargs:
        states_object = kwargs["states"]
        states_json_object = states_object.states.json
        print(states_json_object)

    server = Server()
    await server.init("127.0.0.1", 4999)
    print("server > ready")
    print("server > start")
    await server.run()
```

Je pense qu'il reste encore deux grandes questions qui pourraient être liées.

#### II - Et les erreurs ? Stabilité du programme

##### I - Objets classiques

###### I - Scénario "idéal"

Pour les objets classiques, voici le scénario que j'imagine comme étant "idéal" :

1) L'objet classique "crash" (accès à une variable inexistante, par exemple).
2) L'erreur remonte au pont, mais ne fait pas crash la boucle principale (`Moment`).
3) Puis, au prochain tour, tout recommence normalement.

Les crash pourraient donc faire partie du processus sans problème.  
Cela pourrait même être un moyen pour quitter l'exécution d'un objet actuel (peu propre, certes...).

###### II - Réalité

Voici ce qu'il se passe actuellement si nous faisons crash un objet classique :

```
moment 0 :
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
Task exception was never retrieved
future: <Task finished name='Task-1' coro=<main() done, defined at /Users/mi/Desktop/share/développement/core/main.py:13> exception=NameError("name 'undefined_var' is not defined")>
Traceback (most recent call last):
  File "/Users/mi/Desktop/share/développement/core/main.py", line 127, in main
    await scheduler.run("classic_task")
  File "/Users/mi/Desktop/share/développement/core/core/modules/core/scripting/scheduler/scheduler.py", line 52, in run
    await asyncio.gather(*async_task)
  File "/Users/mi/Desktop/share/développement/core/core/modules/core/scripting/scheduler/scheduler.py", line 62, in execute_objects
    await method.execute(logs = True, mode = mode)
  File "/Users/mi/Desktop/share/développement/core/core/modules/core/scripting/executable/executable.py", line 132, in execute
    result = await self._exec(lines, mode = mode)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/mi/Desktop/share/développement/core/core/modules/core/scripting/executable/executable.py", line 169, in _exec
    result = await bridge()
             ^^^^^^^^^^^^^^
  File "<string>", line 4, in bridge
  File "/Users/mi/Desktop/share/développement/core/core/objects/cell/cell.py", line 14, in add
    print(undefined_var)
          ^^^^^^^^^^^^^
NameError: name 'undefined_var' is not defined
```

###### III - Réalisation

Pour cela, une solution simple me semble être de modifier directement le code du pont :

``` python
async def bridge():
    try:
        return await {executable_object.execution_content}(states = states)
    except Exception as error:
        print(error)
    except:
        print('error')
```

Notons que je me suis documenté concernant les try / except en Python, car je ne connais que peu ce langage de programmation.  
Ici, j'ai tout d'abord placé un `except Exception as error` qui est censé intercepter les erreurs pour permettre de les afficher.  
Mais j'ai tout de même laissé une couche plus basse avec un except classique (général), car certains disent que `except Exception as error` pourrait ne pas capturer toutes les erreurs.  
Je ne sais pas vraiment si c'est toujours d'actualité, mais c'est une petite sécurité, pour le moment.

###### IV - Résultats

Les résultats sont ceux qui étaient attendus :

```
moment 0 :
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
name 'undefined_var' is not defined
result : None

global result : False
==================================================
moment 1 :
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
name 'undefined_var' is not defined
result : None

global result : False
==================================================
```

#### III - Des objets classiques sans mémoire...

##### I - Résumé du problème

Il y a tout de même un autre problème, ou en tout cas une piste d'amélioration possible.  
Actuellement, pour un objet classique, l'état est "réinitialisé" entre chaque tour : le point d'entré est ré-exécuté, et tous les tours sont "similaires" (même si des conditions concernant les `Moment` peuvent être créées, par exemple).  
Mais un objet classique n'a pas de mémoire entre les tours, et c'est un problème.  
Pourquoi ? Car à chaque fois il doit ré-initialiser les states, obtenir le JSON, etc, etc.  

A chaque tour, un objet classique repart de zéro, comme s'il s'agissait de son premier instant de "vie".

##### II - Proposition de solution

Une solution plutôt simple à mettre en oeuvre me semble être la classe `Variable` (qui est déjà créée !).  
Chaque objet classique pourrait créer un champ à la racine de l'objet commun `variable` à son nom, et y stocker ses variables.  

Deux points me semblent problématiques dans ce que je propose :
- Tout d'abord, la structure de données deviendrait potentiellement très grande si beaucoup d'objets classiques sont en exécution.
- Et finalement, il ne faudrait pas les stocker à un nom mais plutôt à un identifiant unique (pensons au principe de non-unicité de l'objet !).

Alors voici des sous-propositions à cette proposition :

###### I - La classe système Identifier

Il pourrait s'agir d'un simple compteur d'objets (+= 1 à chaque fois, par exemple).  
Elle permettrait donc d'attribuer des IDs uniques à des objets, ainsi qu'à libérer les IDs des objets supprimés.  
Cela répond parfaitement au principe de non-unicité de l'objet.

###### II - Un système encore plus large : Memory

Nouveau système : `Memory` contient des `Variables` qui contiennent des `Variable`.

###### III - Réalisation : Identifier

Cette classe est fonctionnelle.  
Pour le moment, la possibilité de supprimer des objets (et par la même occasion des objets) n'existe pas.  
C'est seulement un compteur.  

Voici comment l'utiliser :

``` python
identifier = Identifier()
await identifier.init(variables)
await identifier.create("objects_id")
```

###### IV - Réalisation : Memory

La logique a donc complètement été repensée : `States` n'est plus utilisé.  
Les méthodes qui utilisaient précédement `States` utilisent maintenant `Variables`.  
La mémoire contient des variables qui contiennent des variables qui contiennent des valeurs.

``` python
async def add(**kwargs):
    if "variables" in kwargs:
        variables = kwargs["variables"]

        if await variables.exists("moment/object"):
            _moment_var = await variables.get("moment/object")
            _moment_obj = _moment_var.value
            print(await _moment_obj.get("time/value1"))

    return 1
```

```
0
```

Maintenant, avec tous ces éléments, il est possible de créer ce que nous souhaitions : le système de mémoire pour les objets.

##### III - Résultats

Voici les résultats, tout sera très bientôt rédigé proprement, il me faut un petit peu de temps.  

``` python
async def add(**kwargs):
    if "variables" in kwargs:
        variables = kwargs["variables"]

        if "unique_object_id" in kwargs:
            unique_object_id = kwargs["unique_object_id"]
            print(f"cell::add > unique object id : {unique_object_id}")

            if await variables.exists("objects"):
                temp_var = Variable()
                await temp_var.init({"value": 1})
                await variables.write(f"objects/{unique_object_id}", temp_var)

            if await variables.exists("objects"):
                if await variables.exists(f"objects/{unique_object_id}"):
                    memory = await variables.get(f"objects/{unique_object_id}")
                    print(f"cell::add > memory : {memory.value}")
                else:
                    print("cell::add > I don't remember anything, [...]")

        if await variables.exists("moment/object"):
            _moment_var = await variables.get("moment/object")
            _moment_obj = _moment_var.value
            print(f"cell::add > current moment : {await _moment_obj.get("time/value1")}")

    return 1
```

Si nous exécutons ce code :

```
cell::add > unique object id : 0
cell::add > memory : {'value': 1}
cell::add > current moment : 0
```

Si nous l'exécutons sans le bloc qui écrit dans la mémoire :

```
cell::add > unique object id : 0
cell::add > I don't remember anything, [...]
cell::add > current moment : 0
```

Et j'ai oublié de préciser que le système d'IDs uniques est fonctionnel.  
Nous pouvons load plusieurs objets (qui ont le même code), ils auront un ID différent, et une mémoire unique à cet ID.  

Imaginons écrire trois fois les objets au lieu d'une seule :

``` python
for obj in await settings.get("objects/content/objects"):
    if await settings.get(f"objects/content/objects/{obj}/enabled") == True:
        unique_object_id = await identifier.generate_id("objects_id")
        await loader.load(obj, "object", unique_object_id)

        unique_object_id = await identifier.generate_id("objects_id")
        await loader.load(obj, "object", unique_object_id)

        unique_object_id = await identifier.generate_id("objects_id")
        await loader.load(obj, "object", unique_object_id)
```

Avec ce code pour cell :

``` python
async def add(**kwargs):
    if "variables" in kwargs:
        variables = kwargs["variables"]

        if "unique_object_id" in kwargs:
            unique_object_id = kwargs["unique_object_id"]
            print(f"cell::add > unique object id : {unique_object_id}")

            if await variables.exists("objects"):
                temp_var = Variable()
                if unique_object_id == "0":
                    await temp_var.init({"value": "a"})
                elif unique_object_id == "1":
                    await temp_var.init({"value": "b"})
                else:
                    await temp_var.init({"value": "?"})

                await variables.write(f"objects/{unique_object_id}", temp_var)

            if await variables.exists("objects"):
                if await variables.exists(f"objects/{unique_object_id}"):
                    memory = await variables.get(f"objects/{unique_object_id}")
                    print(f"cell::add > memory : {memory.value}")
                else:
                    print("cell::add > I don't remember anything, [...]")

        if await variables.exists("moment/object"):
            _moment_var = await variables.get("moment/object")
            _moment_obj = _moment_var.value
            print(f"cell::add > current moment : {await _moment_obj.get("time/value1")}")

    return 1
```

Les résultats sont bien :

```
moment 0 :
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
cell::add > unique object id : 0
cell::add > memory : {'value': 'a'}
cell::add > current moment : 0
result : 1

global result : True
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
cell::add > unique object id : 1
cell::add > memory : {'value': 'b'}
cell::add > current moment : 0
result : 1

global result : True
execute : add_macro_check_check
expected result : 1
result : 1

execute : add_macro_check
expected result : 1
result : 1

execute : add
expected result : 1
cell::add > unique object id : 2
cell::add > memory : {'value': '?'}
cell::add > current moment : 0
result : 1

global result : True
```

##### IV - Ajout restant concernant la mémoire : un système de suppression

Nous y reviendrons quand le problème apparaîtra.

#### IV - Mémoire commune entre les objets

Nous y reviendrons quand le problème apparaîtra.

#### V - Des accès aux objets contrôlés

Nous y reviendrons quand le problème apparaîtra.

#### VI - Arrêter un objet complexe

Un autre problème est arrivé quand j'ai commencé à développer l'UI, et le `tasks manager`.  
En fait, pour le moment j'ai brodé quelque chose de fonctionnel pour arrêter un objet classique, c'est assez simple.  
Un système de booléen a pour cela été mis en place.  
Si l'objet est `enabled`, alors la boucle principale le considère comme activé, et inversement si ce n'est pas le cas.  
Et donc si il n'est pas considéré comme actif, on ne l'ajoute pas à `Scheduler` dans `to_run`.  

Cependant, c'est plus compliqué pour un objet complexe, car nous ne l'exécutons qu'une seule fois.  
Donc, nous ne pouvons pas empêcher sa prochaine exécution, puisqu'il n'y en a pas.  

J'ai donc pensé à deux solutions :

##### I - Première solution

Cette première solution est la plus propre.  
Elle dit que c'est l'objet complexe lui-même qui a un état interne, comme `self.on` pour l'ui qui lui indique si son objet est actuellement actif.  
Et si `self.on` vaut `False`, alors il se ferme lui-même.  

C'est ce que fait l'ui actuellement, de manière très simple :

``` python
count = 0
while dpg.is_dearpygui_running() and self.on:
    dpg.render_dearpygui_frame()
    await asyncio.sleep(0)

    if count - 100 == 0:
        if await self.data["loader"].get(f"loader/ui/{self.unique_object_id}/enabled") == True:
            count = 0
        else:
            self.on = False

    count += 1

dpg.destroy_context()
```

Mais le problème, c'est que cela nous force à faire des tests à chaque frame, c'est probablement mauvais.  
Alors, j'ai aussi pensé à fonctionner via des signaux, comme en C++.  
Nous y reviendrons

##### II - Deuxième solution

Celle-ci est probablement moins propre.  
Elle dit que nous pourrions garder une trace de l'exécution déclenchée par `_exec`, puis que nous pourrions la "kill", mais cela me semble un petit peu brutal.  
Ce qu'il faudrait, c'est que le programme puisse obtenir le message / signal AVANT d'être kill, pour pouvoir terminer proprement ses tâches.

### VIII - Transition : de modules vers plugins, objets

Cette partie repose sur une idée simple : il y a trop de modules à mon goût.  
Pourquoi est-ce un problème (personnel, en tout cas) ? Car cela réduit une partie importante du programme au statisme.  
Pour le moment, j'ai développé une grande partie dans `modules` car il s'agissait de la simplicité, mais maintenant que le moteur est bien avancé, j'aimerais changer cela.  

Mais c'est chose plutôt compliquée, car ce qui est actuellement présent dans `modules` sont les éléments directeurs (en incluant `main.py`).  
Cependant, `plugins` et `objects` ne contiennent normalement pas d'éléments directeurs.  

Prenons un exemple : `Moment`.  
Je trouve personnellement qu'il n'a pas sa place en tant que module.  
Le problème, c'est que si nous le plaçons en tant que plugin, alors le moteur ne devrait pas l'utiliser de manière statique.  
Car ce qui est dans le dossier `plugins` est modifiable par l'utilisateur (par définition), donc si le moteur utilise `Moment` mais que l'utilisateur le supprime, ça ne va pas.  

#### I - Proposition de solution

Je vois une solution possible.  
Cette solution dirait que le moteur est en fait un plugin, et que le véritable "moteur" (au sens du statisme) sont les APIs comme `Json`, `Executable`, etc.  

Et en fait, cela change beaucoup de choses.  
Cela signifie donc que nous pouvons ensuite développer un plugin nommé `Moment`, et nous pouvons l'utiliser de manière statique dans ce moteur, puisqu'il est dédié à l'utilisateur.  
Mais sauf que `Moment` ne serait toujours pas un objet "normal", comme `cell` par exemple.  
Alors, je suis mitigé.  

Ce que j'aimerais vraiment, ce serait que même `Moment` soit une sorte d'objet "vivant", exactement comme `cell`, qu'il ne soit en rien différent, mais c'est encore flou.  
Mais la différence fondamentale, c'est que `cell` se dirige seul, pas `Moment`.  
Alors, comment trouver un équilibre ?  
Peu importe ! La date approche, mieux vaut se concentrer sur la nature, les détails pourront être réglés pour "parfaire" le tout, une fois le projet rendu.

## II - corǝ : partie plus axée sur la nature

Revenons au thème principal du sujet !  
Le moteur étant bien commencé, nous pouvons entamer (ou plutôt factoriser, puisque les choses sont souvent faites dans le désordre...) la partie sur la nature !  
C'est à dire, le moteur de simulation de vie.  

C'est donc à partir de maintenant que nous allons pouvoir quitter peu à peu le dossier `modules` pour les dossiers `objects`, ainsi que `plugins`.  
D'un point de vu chronologique, il me semblerait plus judicieux de continuer en allant du plus bas niveau au plus haut niveau.  
C'est à dire : `modules`, puis `plugins`, et pour finir `objects`.  

Pour le moment, le rapport à la nature n'est pas encore très grand dans le dossier `plugins`, mais cela ne saurait tarder (avec `objects`) !

# Attention

Je n'ai pas vraiment le temps d'update cette trame en même temps que le code, elle contient donc des incohérences.  
Je vais le faire très prochainement, il me faut un petit peu de temps pour avancer puis bien rédiger proprement.