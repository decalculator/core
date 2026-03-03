# Core

## Concepts

### Concept général

Il s'agit d'un portail de simulation de vie en python.  
On emploie le terme "portail" car rien (ou le moins possible) doit être statique, tout doit être ouvert pour que l'utilisateur puisse créer son propre monde, ses propres objets.  
L'utilisateur doit pouvoir ajouter des objets, des règles, etc, sans modifier le code source du projet.  

Le but est d'observer l'évolution d'objets dans un monde spécifique à certaines règles.

### Le moteur

Le moteur est nommé `core`.  
Il est (ou sa plus grande part est) `statique`.  
Il est présent dans `core/static`.  
Dans la hiérarchie du programme, le moteur est l'élément le plus haut (ou le plus bas niveau).

### Les paramètres statiques

Ils se trouvent dans `core/static/json/settings.json`.  
- `<version>` : le numéro de version actuel du programme.
- `<minimum_version>` : le tout premier numéro de version du programme.
- `<maximum_version>` : le tout dernier numéro de version du programme.
- `<plugin_folder>` : le chemin vers le dossier contenant les plugins.
- `<plugin_config>` : le chemin vers le fichier contenant les configurations des plugins.
- `<module_folder>` : le chemin vers le dossier contenant les modules.
- `<module_config>` : le chemin vers le fichier contenant les configurations des modules.
- `<object_folder>` : le chemin vers le dossier contenant les objets.
- `<object_config>` : le chemin vers le fichier contenant les configurations des objets.

### Les systèmes

Un système est à la fois la chose la plus haute dans la hiérarchie et à la fois la chose la plus bas niveau de ce que l'utilisateur peut créer.  

Un système est le fruit d'une complémentarité : il est composé d'un module, de plugins, et d'objets associés.  

Le dossier pour les systèmes est actuellement `core/`, en excluant `static` qui contient le moteur.  

#### Le système d'objets

Un objet est la couche la plus basse dans la hiérarchie des systèmes.  
Il contient les classes, méthodes, etc, de l'objet.  
L'objet est nécessaire au plugin.  

##### Structure principale

```
.
    object1
        object1.json
    object2
        object2.json
    object3
        object3.json
    ...
```

A noter que ce dossier se trouve dans `<object_folder>`, et que le fichier de configuration se trouve dans `<object_config>`.

##### Le fichier de configuration

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<object_config>`.  

Il s'agit d'un index contenant les plugins du dossier, ainsi qu'un booléen indiquant si ils sont actifs ou non.  

Voici sa structure actuelle :

``` json
{
    "objects":
    {
        
    }
}
```

#### Le système de plugins

Un plugin contient la manière d'exécuter les objets (noms des méthodes, etc).  
Le plugin est nécessaire au module.  

##### Structure principale

```
.
    plugin1
        plugin1.json
    plugin2
        plugin2.json
    plugin3
        plugin3.json
    ...
```

A noter que ce dossier se trouve dans `<plugin_folder>`, et que le fichier de configuration se trouve dans `<plugin_config>`.

##### Le fichier de configuration d'un plugin

``` json
{
    "version": "x.x.x",
    "name": "plugin_name",
    "module": "plugin_associated_module",
    "requires":
    {
        "modules": {},
        "plugins": [],
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "files":
    {
        "others": [],
        "methods":
        {
            "method1_name":
            {
                "signature": "method1_signature"
            },
            "method2_name":
            {
                "signature": "method2_signature"
            }
        },
        "functions":
        {
            "function1_name":
            {
                "signature": "function1_signature"
            },
            "function2_name":
            {
                "signature": "function2_signature"
            }
        }
        "macros":
        {
            "macro1_name":
            {
                "file": "macro_py_file",
                "execution_check_payload":
                {
                    "file": "macro_execution_check_payload_py_file_path",
                    "process_type": "import",
                    "name": "func_or_method_name",
                    "result":
                    {
                        "true": 1,
                        "false": 0
                    }
                }
            },
            "macro2_name":
            {
                "file": "macro_py_file",
                "execution_check_payload":
                {
                    "file": "macro_execution_check_payload_py_file_path",
                    "process_type": "import",
                    "name": "func_or_method_name",
                    "result":
                    {
                        "true": 1,
                        "false": 0
                    }
                }
            }
        }
    },
    "sub_plugins":
    [
        "plugin_name1", "plugin_name2", "plugin_name3", "..."
    ]
}
```

- `name` : le nom du plugin implémenté
- `module` : le nom du module (type) associé au plugin
- `version` : la version de ce plugin
- `requires` : les requirements
- `sub_plugins` : les sous-plugins implémentés par le plugin
- `files[methods]` : objet contenant les méthodes du fichier principal
- `files[methods][method1_name][signature]` : la signature de la méthode (je ne sais pas réellement si cela va pouvoir nous servir, pour le moment)
- `files[macros]` : les macros d'exécution
- `files[macros][macro1_name][file]` : le chemin vers le fichier qui contient l'implémentation de la macro
- `files[macros][macro1_name][execution_check_payload]` : objet qui contient la vérification qui indique au moteur si il doit exécuter la macro
- `files[macros][macro1_name][execution_check_payload][file]` : le chemin vers le fichier qui contient une méthode / fonction de vérification pour l'exécution de la macro
- `files[macros][macro1_name][execution_check_payload][process_type]` : indique ce qu'il faut faire avec le fichier, `import` pour l'importer, `exec` pour l'exécuter directement
- `files[macros][macro1_name][execution_check_payload][name]` : le nom de la méthode / fonction à exécuter dans ce fichier, pour vérifier si il est temps d'exécuter la macro ou non
- `files[macros][macro1_name][execution_check_payload][result]` : objet qui contient l'interprétation du résultat de l'exécution de la méthode / fonction
- `files[macros][macro1_name][execution_check_payload][result][true]` : le résultat attendu pour dire que la macro doit être exécutée
- `files[macros][macro1_name][execution_check_payload][result][false]` : le résultat attendu pour dire que la macro ne doit pas être exécutée

Le lien entre objet et plugin est encore mitigé, il faut travailler dessus.

##### Le fichier de configuration

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<plugin_config>`.  

Il s'agit d'un index contenant les plugins du dossier, ainsi qu'un booléen indiquant si ils sont actifs ou non.  

Voici sa structure actuelle :

``` json
{
    "plugins":
    {
        "base":
        {
            "enabled": true
        },
        "core":
        {
            "enabled": true
        },
        "objets_classiques":
        {
            "enabled": true
        }
    }
}
```

#### Le système de modules

Un module contient les implémentations des types, nécessaires aux plugins.  

##### Structure principale

```
.
    module1
        module1.json
    module2
        module2.json
    module3
        module3.json
    ...
```

A noter que ce dossier se trouve dans `<module_folder>`, et que le fichier de configuration se trouve dans `<module_config>`.

##### Le fichier de configuration d'un module

``` json
{
    "version": "x.x.x",
    "name": "module_name",
    "requires":
    {
        "modules": {},
        "plugins": [],
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "sub_modules":
    [
        "module_name1", "module_name2", "module_name3", "..."
    ]
}
```

- `name` : le nom du module (type) implémenté
- `version` : la version de ce module
- `requires` : les requirements
- `sub_modules` : les sous-modules implémentés par le module

##### Le fichier de configuration

Ce fichier de configuration se trouve dans les paramètres statiques de l'application.  
Plus précisément, il s'agit de `<module_config>`.  

Il s'agit d'un index contenant les modules du dossier, ainsi qu'un booléen indiquant si ils sont actifs ou non.  

Voici sa structure actuelle :

``` json
{
    "modules":
    {
        "base" :
        {
            "enabled": true
        },
        "core":
        {
            "enabled": true
        },
        "plugins_manager":
        {
            "enabled": true
        }
    }
}
```

#### Structure d'un système

Exemple : un module time

```
- core/modules/time : contient la déclaration du type time
- core/plugins/time : contient les méthodes du type time
- core/objects/time : contient l'implémentation des objets de type time
```

## Développement plus détaillé des concepts

### Le système "core"

Voici une liste plutôt précise des concepts que devrait développer le système.  

#### communication

Ce sous-système sert à la communication avec l'Internet.  
Il se trouve dans `core/modules/core/communication`, ainsi que dans `core/plugins/core/communication`.

#### configuration

Il se trouve dans `core/modules/core/configuration`.

#### filesystem

Il se trouve dans `core/modules/core/filesystem`.

#### server

Il se trouve dans `core/modules/core/server`.

#### ui

Il se trouve dans `core/modules/core/ui`.

#### world

Il se trouve dans `core/modules/core/world`.

### Le système "base"

#### moment

Il s'agit d'un sous-système d'écoulement d'instants.  
Nous utilisons "instant" pour parler du temps.  
L'instant est un concept, le temps est un objet.  

L'idée est assez simple à comprendre.  
Chaque instant a une valeur, représentée par le temps, qui est un objet.  
L'instant suivant peut représenter le temps suivant, mais pas obligatoirement.  
Par contre, il devrait toujours y avoir un écoulement d'instants, je crois.  

Pour voir l'évolution de son monde, l'utilisateur doit donc pouvoir moduler les instants : passer tant d'instants, aller à un instant, etc.  

#### date

Ce sous-système permet d'apprendre au moteur à lire les dates, et à les implémenter.  
Par exemple, une méthode `__special_date()` tous les x instants peut y être spécifiée, etc.  
Le plugin associé pourra donc créer un système de date.  
Toutes les règles sont faisables, dans la limite du possible (performances de l'ordinateur, enjeux de mémoire, etc).  
Voici quelques idées de choses qui devraient être rendues possibles :  
- L'utilisateur pourra (par exemple) créer un système de dates où les jours sont deux par deux (1, 3, 5, ...), etc.  
- Il pourrait aussi créer un monde où, la date va à rebours : 31, 30, 29, ...  
- Ou bien encore imaginer un système de date totalement différent, qui repose sur des calculs aléatoires, pour définir quel jour nous sommes !
- Ou une boucle temporelle : nous revenons à la même date, en boucle

#### season

Ce sous-système implémente le type d'objet `season`.  

#### weather

Ce sous-système implémente le type d'objet `weather`.  
Le plugin associé pourra donc créer un système de météo.  
Nous pourrons y lier des objets de types `probability`, `consequence`, ...  
Par exemple, la probabilité de pluie en novembre pourrait être de 70%.  
Et pour les conséquences, la pluie fait monter les niveaux d'eau.

Voici quelques idées de choses qui devraient être rendues possibles :
- Il sera aisé de créer une nouvelle météo, par exemple un temps où il pleut de l'électricité
- Le sens n'est pas obligatoirement unidirectionnel. La plupart du temps, la météo vient de l'exterieur vers l'intérieur, mais ce n'est pas nécessairement le cas ici. Par exemple, une météo pourrait être une planète qui renvoie de l'eau qui monte au ciel (par une loi de type law)

#### probability

Ce sous-système implémente le type d'objet `probability`.  
Le plugin associé pourra donc créer un système de probabilité.  

Une représentation simple de probabilité pourrait être une valeur comprise entre 0 et 1.  

Voici quelques idées de choses qui devraient être rendues possibles :
- Les autres objets peuvent ensuite utiliser ce système de probabilités, pour les apparitions etc
- `probability` n'est qu'un nom, on peut très bien imaginer un faux système derrière cela
- Les méthodes de représentation peuvent changer, ce n'est pas obligatoirement une valeur entre 0 et 1. Par exemple : cela pourrait être des sentiments, un string, ou autre.

#### consequence

Ce sous-système implémente le type d'objet `consequence`.  
Le plugin associé pourra donc créer un système de conséquence (déterminisme).  

Cela pourrait globalement permettre d'implémenter ce qu'il se passe si [...].  

Voici quelques idées de choses qui devraient être rendues possibles :
- Une conséquence d'avant-apparition : ce qu'il se passe pour que l'évènement se produise. Par exemple : les fleurs poussent grâce à la pluie (en partie).
- Une conséquence d'après-apparition : ce qu'il se passe à la suite de l'évènement, ce qu'il engendre. Par exemple : les fleurs qui éclosent permettent aux bourdons de venir butiner.

#### aleatory

Ce sous-système implémente le type d'objet `aleatory`.  
Le plugin associé pourra donc créer un système d'aléatoire.  
L'aléatoire n'existant pas en informatique classique, il serait par exemple possible d'utiliser des API comme random.org, en cas de besoin.  

Ce système pourrait implémenter plusieurs types d'aléatoires : les pseudo-aléatoires, etc.

#### world

Ce sous-système implémente le type d'objet `world`.  
Le plugin associé pourra donc créer un système de monde.  

Un monde pourrait par exemple être constitué :
- D'un ensemble de règles (rule)
- D'un ensemble d'objets
- D'un système d'écoulement d'instants
- D'un système de saison
- D'un système de météo
- ...

En fait, un monde n'est qu'une structure principale contenant tous les autres éléments. Alors, un monde devrait pouvoir contenir tous les objets (sauf lui-même).

#### rule

Ce sous-système implémente le type d'objet `rule`.  
Le plugin associé pourra donc créer un système de règles.  
Ce sont les propriétés fondamentales du monde, que l'on ne peut pas contredire.  
Par exemple : la gravité.

#### obligation_future

Ce sous-système implémente le type d'objet `obligation_future`.  
Le plugin associé pourra donc créer un système d'obligations futures.  
Les obligations futures sont des conditions faites pour altérer le futur du monde et des objets qui y vivent.  
L'objectif est de créer plusieurs scénarios possibles en fonction d'une obligation future, pour permettre à l'utilisateur de modeler le futur de son monde.  
Exemple : si nous avons un groupe d'entités qui vivent ensembles, et qu'une entité externe attaque une entité de ce groupe, alors il pourrait y avoir conflit.  
On peut forcer le conflit, pour voir ce qu'il va se passer, en posant cette obligation future : entité 1 attaque entité 2 tel jour.  
L'utilisateur peut donc forcer un objet (conscient et "libre") à faire une chose à un instant T.

#### possibilities

Ce sous-système implémente le type d'objet `possibilities`.  
Le plugin associé pourra donc créer un système de possibilités (scénarios).  

#### save

Ce sous-système implémente le type d'objet `save`.  
Le plugin associé pourra donc créer un système de sauvegarde.  

Par défaut, un monde pourra être sauvegardé de deux manières :
- Localement : le dossier de sauvegarde du monde sera enregistré sur le disque de l'utilisateur.
- En ligne : le dossier de sauvegarde du monde sera enregistré sur un serveur.

#### zone

Ce sous-système implémente le type d'objet `zone`.  
Le plugin associé pourra donc créer un système de zones.  

#### moment

Ce sous-système implémente le type d'objet `moment`.  
Le plugin associé pourra donc créer un système d'instants, et d'écoulement d'instants.  

#### entity

Ce sous-système implémente le type d'objet `entity`.  
Le plugin associé pourra donc créer un système d'aléatoire.  

Par défaut, il pourrait exister 3 types d'entités :
- L'entité consciente libre : il s'agit d'une entité qui a une conscience et qui est libre de ses mouvements. Par exemple : un oiseau.
- L'entité consciente : il s'agit d'une entité qui a une conscience, mais qui n'est pas vraiment libre de ses déplacements. Par exemple : une plante, bien qu'elle grandisse.
- L'entité non-consciente non-vivante : il s'agit d'une entité qui n'a ni conscience, ni liberté. Par exemple : une table.

### Le système "community"

Une communauté est un espace publique qui regroupe des partages d'objets, de règles, de mondes, en ligne.  
Chaque objet, règle, monde, ou autre de la communauté a un identifiant unique de 10 chiffres : `0123456789`.  
Ce système permettra d'intéragir avec.

### Le système "menu"

Il y aura globalement deux options :
- Lancement local : on demande à l'utilisateur de sélectionner le dossier de son monde, si il ne se trouve pas dans le dossier par défaut.
- Lancement serveur : on demande à l'utilisateur de saisir l'identifiant unique de son monde, ainsi que l'url vers le serveur communautaire.

### Le système evolution

Un objet peut subir des évolutions (mutations).  
Le plugin evolution permet de faire évoluer des objets en d'autres objets (ou autres modifications).

### core/static

#### scripting

##### states

Pour orchestrer le bon fonctionnement de l'application, une classe `States` est présente.  
Chaque classe aura comme attribut d'instance un objet commun de type `states`, pour y inscrire les états en cours.

##### loader

1 - Module

``` python
Loader.import(name, value_type)

# exemple : importer le module base
Loader.import("base", "modules")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_entry.py".  
2) Dans ce fichier, se trouve une classe "_entry", il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_module"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _entry
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, le type a été importé dans le moteur.

2 - Plugin

``` python
# exemple : importer le plugin base
Loader.import("base", "plugins")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_entry.py".  
2) Dans ce fichier, se trouve une classe "_entry", il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_plugin"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _entry
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, le plugin a été importé dans le moteur, ainsi que les noms de méthodes des objets à exécuter, les règles, etc.

3 - Objet

``` python
# exemple : importer l'objet time
Loader.import("time", "objects")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_entry.py".  
2) Dans ce fichier, se trouve une classe "_entry", il l'exécute.  

Le constructeur de cette classe est le suivant :
``` python
def __init__(self, states):
    self.states = states
    self.system_name = "nom_du_système_object"

    self.states.create(system_name)
    self.states.assign(system_name, ..., ...)

    # code _entry
    # ajoute le type au moteur
    # ...
```

Après l'exécution de ce constructeur, l'objet a été importé dans le moteur.

##### settings

##### symbols

### UI

Pour l'UI, nous utiliserons très probablement `fastapi`, car il est plus fait pour le fonctionnement asynchrone que flask.  
Nous optons pour un render web car, tout doit être modelable, c'est probablement bien plus simple de modifier du code source HTML / CSS / JS qu'une application tkinter, par exemple.  

Car je ne l'ai pas forcément précisé, mais l'interface en elle-même devra être non-contextuelle.  

### Synchronisme
Les tâches s'exécutent de manière asynchrones, c'est à dire indépendamment les unes des autres, en même temps.  
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
states.assign("app", "status", "on")
```

On peut ensuite faire quelque chose comme cela :
``` python
while states.get("app", "status") != "off":
    # boucle principale de l'app
```

## Idées moins claires

### Dynamisme

Le principe est que le programme soit le moins contextuel possible, c'est pour cela que l'on parle de développement d'un portail.  
Pour cela, plusieurs fonctions dynamiques propres à python peuvent être utilisées :
- `exec()` : permet d'exécuter du code python, sans compilation
- `eval()` : permet d'évaluer une expression, sans compilation
- `write()` : permet de (ré)écrire le propre code du programme, sans compilation

Mais si la non-contextualité est correctement développée, nous pourrions ne pas avoir à utiliser ces fonctions.

### Template de création de système