# Core

## Table des matières

- [Préambule](#préambule)
    - [Sujet](#sujet)
    - [Idée initiale](#idée-initiale)
- [Concepts](#concepts)
    - [Le moteur du portail](#le-moteur-du-portail)
    - [Les paramètres statiques](#les-paramètres-statiques)
    - [Les systèmes](#les-systèmes)
    - [Les objets](#les-objets)
    - [Valeurs JSON](#valeurs-json)
    - [Le système d'objets](#le-système-dobjets)
        - [Structure principale](#structure-principale)
        - [Le fichier de configuration d'un objet](#le-fichier-de-configuration-dun-objet)
        - [Le fichier de configuration général d'un objet](#le-fichier-de-configuration-général-dun-objet)
        - [Les packs d'objets](#les-packs-dobjets)
    - [Le système de plugins](#le-système-de-plugins)
        - [Structure principale](#structure-principale-1)
        - [Le fichier de configuration d'un plugin](#le-fichier-de-configuration-dun-plugin)
        - [Le fichier de configuration général d'un plugin](#le-fichier-de-configuration-général-dun-plugin)
        - [Les packs de plugins](#les-packs-de-plugins)
    - [Le système de modules](#le-système-de-modules)
        - [Structure principale](#structure-principale-2)
        - [Le fichier de configuration d'un module](#le-fichier-de-configuration-dun-module)
        - [Le fichier de configuration général d'un module](#le-fichier-de-configuration-général-dun-module)
- [Développement plus détaillé des concepts](#développement-plus-détaillé-des-concepts)
    - [Plugins par défaut](#plugins-par-défaut)
        - [communication](#communication)
        - [configuration](#configuration)
        - [filesystem](#filesystem)
        - [server](#server)
        - [ui](#ui)
        - [community](#community)
        - [menu](#menu)
        - [evolution](#evolution)
    - [Objets par défaut](#objets-par-défaut)
        - [moment](#moment)
        - [date](#date)
        - [season](#season)
        - [weather](#weather)
        - [probability](#probability)
        - [consequence](#consequence)
        - [aleatory](#aleatory)
        - [world](#world)
        - [rule](#rule)
        - [obligation_future](#obligation_future)
        - [possibilities](#possibilities)
        - [save](#save)
            - [Structure d'une save](#structure-dune-save)
        - [map](#map)
            - [Structure d'une map](#structure-dune-map)
        - [zone](#zone)
            - [Structure d'une zone](#structure-dune-zone)
        - [entity](#entity)
    - [Modules par défaut](#modules-par-défaut)
        - [executable](#executable)
        - [execution](#execution)
        - [states](#states)
            - [Créer une state](#créer-une-state)
            - [Assigner une valeur à une state](#assigner-une-valeur-à-une-state)
        - [loader](#loader)
        - [installator](#installator)
            - [Installer un module](#installer-un-module)
            - [Installer un plugin](#installer-un-plugin)
            - [Installer un objet](#installer-un-objet)
        - [object](#object)
        - [settings](#settings)
            - [Créer un paramètre](#créer-un-paramètre)
            - [Supprimer un paramètre](#supprimer-un-paramètre)
            - [Obtenir une valeur d'un paramètre](#obtenir-une-valeur-dun-paramètre)
            - [Ecrire une valeur dans un paramètre](#ecrire-une-valeur-dans-un-paramètre)
            - [Activer (booléen)](#activer-booléen)
            - [Désactiver (booléen)](#désactiver-booléen)
        - [symbols](#symbols)
    - [UI](#ui-1)
    - [Synchronisme](#synchronisme)
- [Idées moins claires](#idées-moins-claires)
    - [Dynamisme](#dynamisme)
    - [Template de création de système](#template-de-création-de-système)
- [Propriétés générales](#propriétés-générales)
    - [Principe de non-unicité de l'objet](#principe-de-non-unicité-de-lobjet)
    - [Exemple : l'objet temps](#exemple--lobjet-temps)

## Préambule

### Sujet

Il s'agit projet scolaire, les contraintes du sujet sont :
- Le langage de programmation utilisé doit être Python.
- Le thème est : la nature (mieux vaudrait éviter le hors-sujet).
- Le temps imparti est d'environ 2 mois et demi.
- L'utilisation de l'intelligence artificielle est autorisée mais doit être déclarée.
- C'est un projet que je réalise seul.

Tout ce que j'écris ici est le fruit de ma réflexion personnelle, **aucune** intelligence artificielle ne sera utilisée, ni aucun concept / tutoriel venant d'internet d'ailleurs. Les seules choses que je m'autorise à utiliser pour ce projet sont les modules et leurs documentations.

### Idée initiale

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

### Un petit peu de désabstraction

Dans cette documentation, voici la définition de ce que nous appelerons objets :

```
Tout est objet, mis à part le moteur.
```

Donc :
- toute chose, aussi abstraite soit elle, est un objet si elle n'est pas le moteur (ce que nous développons).
- le temps, la vie, l'espace, les mondes, les êtres, ..., sont objets.

## Concepts

### Le moteur du portail

Le moteur du portail est (aussi) nommé `core`.  
Il est (ou sa plus grande part) `statique`.  
C'est un `module`.  
Il est présent dans `core/modules/core`.  

L'utilité du moteur est assez simple : il permet de load des objets, de définir les classes requises au bon fonctionnement de l'application, de définir des symboles, etc.

### Les paramètres statiques

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

### Les systèmes

Un système est le fruit d'une complémentarité : il est composé de modules, de plugins, et d'objets.  
Le dossier pour les systèmes est actuellement `core/`.  

### Les objets

Les objets sont les "choses" que nous développons.  
Il en existe trois types :
- `object` : un objet de type `object`
- `plugin` : un objet de type `plugin`
- `module` : un objet de type `module`

Nous reviendrons prochainement sur les définitions et différences de ces types d'objets.

### Valeurs JSON

Voici tous les paramètres (communs) qui peuvent revenir dans les fichiers JSON, et leurs significations.  
Nous nommerons cela `objet`, puisqu'il peut s'agir d'un `module`, d'un `plugin`, ou d'un `objet` :

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

Et pour finir, nous appelerons `type` le type d'objet implémenté (`object`, `plugin`, `module`).
- `sub_{type}` (array) : un array contenant les noms des sous-objets implémentés (sous-objets, sous-plugins, sous-modules).

### Le système d'objets

Un objet est la couche la plus basse dans la hiérarchie des systèmes.  
Il contient son propre code d'implémentation.  
Un objet est plus bas qu'un plugin.

#### Structure principale

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

#### Le fichier de configuration d'un objet

``` json
{
    "version": "x.x.x",
    "name": "object_name",
    "module": "object_associated_module",
    "plugin": "object_associated_plugin",
    "type": "object",
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

#### Le fichier de configuration général d'un objet

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

#### Les packs d'objets

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

### Le système de plugins

Un plugin est un objet.  
Cependant, il est plus bas niveau qu'un objet.  

Pour le moment, la structure entre un objet de type `plugin` et `object` est la même.

#### Structure principale

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

#### Le fichier de configuration d'un plugin

``` json
{
    "version": "x.x.x",
    "name": "plugin_name",
    "module": "plugin_associated_module",
    "plugin": "plugin_associated_plugin",
    "type": "plugin",
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

#### Le fichier de configuration général d'un plugin

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

#### Les packs de plugins

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

### Le système de modules

Un module est différent des objets de type `plugin` ou `object`.  
Sa structure est beaucoup plus complexe et abstraite.

Nous allons prendre l'exemple du moteur (`core/modules/core`), puisqu'il n'existe pas de structure générale, pour le moment.

#### Structure principale

```
.
├── json
│   ├── settings.json
│   └── symbols
│       └── symbols.json
└── scripting
    ├── loader
    │   ├── loader.py
    ├── settings
    │   └── settings.py
    ├── states
    │   └── states.py
    └── symbols
        └── symbols.py
```

Pour le moment :
- `core/modules/core/json` contient les données statiques de l'application.
- `core/modules/core/scripting` contient les implémentations des sous-modules du moteur.

A noter que ce dossier se trouve dans `<module_folder>`, et que le fichier de configuration se trouve dans `<module_config>`.

#### Le fichier de configuration d'un module

``` json
```

#### Le fichier de configuration général d'un module

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

## Développement plus détaillé des concepts

### Plugins par défaut

Voici une liste plutôt précise des plugins par défaut.

#### communication

Ce plugin sert à la communication avec l'Internet.  
Il se trouve dans `core/plugins/communication`.

#### configuration

Il se trouve dans `core/plugins/configuration`.

#### filesystem

Il se trouve dans `core/plugins/filesystem`.

#### server

Il se trouve dans `core/plugins/server`.

#### ui

Il se trouve dans `core/plugins/ui`.

#### community

Une communauté est un espace publique qui regroupe des partages d'objets, de règles, de mondes, en ligne.  
Chaque objet, règle, monde, ou autre de la communauté a un identifiant unique de 10 chiffres : `0123456789`.  
Ce plugin permettra d'intéragir avec.

#### menu

Il y aura globalement deux options :
- Lancement local : on demande à l'utilisateur de sélectionner le dossier de son monde, si il ne se trouve pas dans le dossier par défaut.
- Lancement serveur : on demande à l'utilisateur de saisir l'identifiant unique de son monde, ainsi que l'url vers le serveur communautaire.

#### evolution

Un objet peut subir des évolutions (mutations).  
Le plugin evolution permet de faire évoluer des objets en d'autres objets (ou autres modifications).

### Objets par défaut

#### moment

Il s'agit d'un objet d'écoulement d'instants.  
Nous utilisons "instant" pour parler du temps.  
L'instant est un concept, le temps est un objet.  

L'idée est assez simple à comprendre.  
Chaque instant a une valeur, représentée par le temps, qui est un objet.  
L'instant suivant peut représenter le temps suivant, mais pas obligatoirement.  
Par contre, il devrait toujours y avoir un écoulement d'instants, je crois.  

Pour voir l'évolution de son monde, l'utilisateur doit donc pouvoir moduler les instants : passer tant d'instants, aller à un instant, etc.  

#### date

Cet objet permet d'implémenter un système de dates.  
Toutes les règles sont faisables, dans la limite du possible (performances de l'ordinateur, enjeux de mémoire, etc).  
Voici quelques idées de choses qui devraient être rendues possibles :  
- L'utilisateur pourra (par exemple) créer un système de dates où les jours sont deux par deux (1, 3, 5, ...), etc.  
- Il pourrait aussi créer un monde où, la date va à rebours : 31, 30, 29, ...  
- Ou bien encore imaginer un système de date totalement différent, qui repose sur des calculs aléatoires, pour définir quel jour nous sommes !
- Ou une boucle temporelle : nous revenons à la même date, en boucle

#### season

Cet objet implémente le type d'objet `season`.  

#### weather

Cet objet implémente le type d'objet `weather`, un système de météo.  
Nous pourrons y lier des objets de types `probability`, `consequence`, ...  
Par exemple, la probabilité de pluie en novembre pourrait être de 70%.  
Et pour les conséquences, la pluie fait monter les niveaux d'eau.

Voici quelques idées de choses qui devraient être rendues possibles :
- Il sera aisé de créer une nouvelle météo, par exemple un temps où il pleut de l'électricité
- Le sens n'est pas obligatoirement unidirectionnel. La plupart du temps, la météo vient de l'exterieur vers l'intérieur, mais ce n'est pas nécessairement le cas ici. Par exemple, une météo pourrait être une planète qui renvoie de l'eau qui monte au ciel (par une loi de type law)

#### probability

Cet objet implémente le type d'objet `probability`, un système de probabilité.  

Une représentation simple de probabilité pourrait être une valeur comprise entre 0 et 1.  

Voici quelques idées de choses qui devraient être rendues possibles :
- Les autres objets peuvent ensuite utiliser ce système de probabilités, pour les apparitions etc
- `probability` n'est qu'un nom, on peut très bien imaginer un faux système derrière cela
- Les méthodes de représentation peuvent changer, ce n'est pas obligatoirement une valeur entre 0 et 1. Par exemple : cela pourrait être des sentiments, un string, ou autre.

#### consequence

Cet objet implémente le type d'objet `consequence`, un système de conséquence (déterminisme).  

Cela pourrait globalement permettre d'implémenter ce qu'il se passe si [...].  

Voici quelques idées de choses qui devraient être rendues possibles :
- Une conséquence d'avant-apparition : ce qu'il se passe pour que l'évènement se produise. Par exemple : les fleurs poussent grâce à la pluie (en partie).
- Une conséquence d'après-apparition : ce qu'il se passe à la suite de l'évènement, ce qu'il engendre. Par exemple : les fleurs qui éclosent permettent aux bourdons de venir butiner.

#### aleatory

Cet objet implémente le type d'objet `aleatory`, un système d'aléatoire.  
L'aléatoire n'existant pas en informatique classique, il serait par exemple possible d'utiliser des API comme random.org, en cas de besoin.  

Cet objet pourrait implémenter plusieurs types d'aléatoires : les pseudo-aléatoires, etc.

#### world

Cet objet implémente le type d'objet `world`, un système de monde.  

Un monde pourrait par exemple être constitué :
- D'un ensemble de règles (rule)
- D'un ensemble d'objets
- D'un système d'écoulement d'instants
- D'un système de saison
- D'un système de météo
- ...

En fait, un monde n'est qu'une structure principale contenant tous les autres éléments. Alors, un monde devrait pouvoir contenir tous les objets (sauf lui-même).

#### rule

Cet objet implémente le type d'objet `rule`, un système de règles.  
Ce sont les propriétés fondamentales du monde, que l'on ne peut pas contredire.  
Par exemple : la gravité.

#### obligation_future

Cet objet implémente le type d'objet `obligation_future`, un système d'obligations futures.  
Les obligations futures sont des conditions faites pour altérer le futur du monde et des objets qui y vivent.  
L'objectif est de créer plusieurs scénarios possibles en fonction d'une obligation future, pour permettre à l'utilisateur de modeler le futur de son monde.  
Exemple : si nous avons un groupe d'entités qui vivent ensembles, et qu'une entité externe attaque une entité de ce groupe, alors il pourrait y avoir conflit.  
On peut forcer le conflit, pour voir ce qu'il va se passer, en posant cette obligation future : entité 1 attaque entité 2 tel jour.  
L'utilisateur peut donc forcer un objet (conscient et "libre") à faire une chose à un instant T.

#### possibilities

Cet objet implémente le type d'objet `possibilities`, un système de possibilités (scénarios).  

#### save

Cet objet implémente le type d'objet `save`, un système de sauvegarde.  

Par défaut, un monde pourra être sauvegardé de deux manières :
- Localement : le dossier de sauvegarde du monde sera enregistré sur le disque de l'utilisateur.
- En ligne : le dossier de sauvegarde du monde sera enregistré sur un serveur.

##### Structure d'une save

Voici la structure d'un objet JSON de type save, par défaut :

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

#### map

Cet objet implémente le type d'objet `map`, un système de maps.  
Une map est un ensemble qui contient des `zones`.  

##### Structure d'une map

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

#### zone

Cet objet implémente le type d'objet `zone`, un système de zones.  

##### Structure d'une zone

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

#### entity

Cet objet implémente le type d'objet `entity`, un système d'entités.  

Par défaut, il pourrait exister 3 types d'entités :
- L'entité consciente libre : il s'agit d'une entité qui a une conscience et qui est libre de ses mouvements. Par exemple : un oiseau.
- L'entité consciente : il s'agit d'une entité qui a une conscience, mais qui n'est pas vraiment libre de ses déplacements. Par exemple : une plante, bien qu'elle grandisse.
- L'entité non-consciente non-vivante : il s'agit d'une entité qui n'a ni conscience, ni liberté. Par exemple : une table.

### Modules par défaut

#### executable

Il s'agit d'une classe implémentant le type `Executable`.  
Pour initialiser un exécutable, on passe au constructeur un dict / json de configuration, et l'objet states.  

Pour le moment, nous ne faisons pas de réelle distinction entre une macro et une méthode, car la structure est très similaire.  
Si cela venait à changer, des classes `macro`, `method`, `function` pourraient être implémentées.  

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

#### execution

Il s'agit d'un objet plus haut qu'un exécutable.  
En fait, c'est globalement le contexte d'exécution d'un objet.  
Il contient tous les exécutables d'un objet.

#### states

Pour orchestrer le bon fonctionnement de l'application, une classe `States` est présente.  
Chaque classe aura comme attribut d'instance un objet commun de type `states`, pour y inscrire les états en cours.  

Principales méthodes :

#### Créer une state

``` python
States.create("name")
```

#### Assigner une valeur à une state

``` python
States.assign("name", "param1", "value1")
```

#### loader

Il s'agit du module principal permettant de load des objets non-définis à l'avance, dans le moteur.  
Son constructeur prend (pour le moment) comme paramètres :

``` python
loader = Loader(states, "module_path", "plugin_path", "object_path")
```

La méthode principale de ce fichier est `Loader.load()`, dont la signature est :

``` python
load(self, name, load_type)
```

Elle va charger le fichier principal de configuration de l'objet, initialiser un objet de type `Object` grâce au contenu de celui-ci.

#### installator

Ce module est assez semblable au `Loader`, je ne sais pas encore si nous le garderons dans la version finale.  
En tout cas, il se distingue du `Loader` en un point : il est fait pour `installer` un module, de manière permanente.

##### Installer un module

``` python
Installator.import(name, value_type)

# exemple : importer le module base
Installator.import("base", "modules")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_install.py".  
2) Dans ce fichier, se trouve une classe "_install", il l'exécute.  

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

##### Installer un plugin

``` python
# exemple : importer le plugin base
Installator.import("base", "plugins")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_install.py".  
2) Dans ce fichier, se trouve une classe "_install", il l'exécute.  

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

##### Installer un objet

``` python
# exemple : importer l'objet time
Installator.import("time", "objects")
```

1) Le moteur importe dynamiquement "{value_type}/{name}/_install.py".  
2) Dans ce fichier, se trouve une classe "_install", il l'exécute.  

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

#### object

Il est load par `Loader`, grâce au fichier de configuration d'un objet.  
Un objet de type `Object` contient globalement `Object.execution` (liste), qui contient des objets de type `Execution` (qui contiennent les objets de type `Executable`).  
Pour le moment, la seule "entrée d'exécution" est le paramètre "execution" du fichier de configuration d'un objet, mais nous avons prévu une liste (ou objet json) au cas où plusieurs champs venaient à être utilisés.

#### settings

Il s'agit d'un module permettant de créer / gérer des paramètres.  
Les principales méthodes sont :

##### Créer un paramètre

``` python
Settings.create("name")
```

##### Supprimer un paramètre

``` python
Settings.remove("name")
```

##### Obtenir une valeur d'un paramètre

``` python
Settings.get("name/param1")
```

##### Ecrire une valeur dans un paramètre

``` python
Settings.write("name/param2", "value", 1)
```

##### Activer (booléen)

``` python
Settings.enable("name/enabled", "name", "object")
```

(Il y a aussi un `Loader.load()` d'appelé).

##### Désactiver (booléen)

``` python
Settings.enable("name/disabled", "name", "object")
```

#### symbols

C'est un module permettant de gérer des `symboles`.  
Prenons un exemple pour comprendre ce qu'est un symbole, et son importance :

``` python
symbols = Symbols(states)

for key in app_config:
    if key not in symbols.symbols:
        symbols.create(key, app_config[key])

pattern = "<[a-z/<>_]*>"

for key in symbols.symbols:
    current_value = symbols.symbols[key]
    done = False

    while not done:
        match = re.search(pattern, current_value)

        if match:
            to_replace = match.group()
            if to_replace in symbols.symbols:
                replace_by = symbols.symbols[to_replace]
            else:
                replace_by = "<not_found>"

            current_value = current_value.replace(to_replace, replace_by)
        else:
            symbols.symbols[key] = current_value
            done = True

print(symbols.symbols)
```

``` python
{'<version>': '1.0.0', '<minimum_version>': '1.0.0', '<maximum_version>': '1.0.0', '<plugin_folder>': 'core/plugins', '<plugin_config>': 'core/plugins/plugins.json', '<module_folder>': 'core/modules', '<module_config>': 'core/modules/modules.json', '<object_folder>': 'core/objects', '<object_config>': 'core/objects/objects.json'}
```

Ce sont simplement des variables propres au bon fonctionnement du programme.

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

## Propriétés générales

Il s'agit d'une petite liste de propriétés générales que la version finale devrait adopter.

### Principe de non-unicité de l'objet

La propriété est simple : un objet peut apparaître autant de fois que nous le souhaitons dans un monde. Et ce, pour tout objet.  
Cela signifie que même pour des objets plus "abstraits", cela devrait être possible.  

(Sauf si une propriété de l'objet dit le contraire, bien entendu.)

#### Exemple : l'objet temps

Cela signifie donc qu'un monde peut avoir plusieurs temps, indépendants les uns des autres.  
Pour un monde qui développe plusieurs planètes, cela pourrait être assez courant.  

Cependant, même pour un monde qui n'en développe qu'une seule, nous pourrions imaginer que dans une certaine plage de coordonnées, l'objet temps n'est pas le même et fonctionne différement.  

Et nous ne parlons pas d'un simple décalage, comme on pourrait observer sur Terre entre une horloge en haut d'une montagne et une horloge plus basse.  
Nous parlons vraiment de définitions différentes, nous pourrions imaginer que dans une plage de coordonnées, le temps irait à rebours, quand dans une autre plage de coordonnées, il "tournerait" "normalement".