# Core

## Préambule

### Sujet

Il s'agit projet scolaire, les contraintes du sujet sont :
- Le langage de programmation utilisé doit être Python.
- Le thème est : la nature (mieux vaudrait éviter le hors-sujet).
- Le temps imparti est d'environ 2 mois et demi.
- L'utilisation de l'intelligence artificielle est autorisée mais doit être déclarée.
- C'est un projet que je réalise seul.

Tout ce que j'écris ici est le fruit de ma réflexion personnelle, **aucune** intelligence artificielle ne sera utilisée.

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

## Concepts

### Le moteur du portail

Le moteur du portail est (aussi) nommé `core`.  
Il est (ou sa plus grande part) `statique`.  
Il est présent dans `core/static`.  
Dans la hiérarchie du programme, le moteur est l'élément le plus bas niveau.

### Les paramètres statiques

Les paramètres statiques se trouvent dans `core/static/json/settings.json`.  
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

Un système est la chose la plus bas niveau qu'un utilisateur puisse créer.  
Un système est le fruit d'une complémentarité : il est composé d'un module, de plugins, et d'objets associés.  
Le dossier pour les systèmes est actuellement `core/`, en excluant `core/static/`, qui contient le moteur.  

#### Structure d'un système

Exemple : un système `time`
```
- core/modules/time : module
- core/plugins/time : plugin
- core/objects/time : objet
```

### JSON

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

- `files` (objet) : il s'agit d'un champ concernant les fichiers.
- `files/{filename}` (objet) : le champ principal concernant le fichier.
- `files/{filename}/methods` (objet) : un champ concernant les méthodes de `{filename}`.
- `files/{filename}/functions` (objet) : un champ concernant les fonctions de `{filename}`.

Nous appelerons `{action}` le choix, que ce soit une méthode ou une fonction, car la structure est la même.
- `files/{filename}/{action}/{action1_name}` (objet) : le champ principal concernant l'action (le nom de la méthode / fonction).
- `files/{filename}/{action}/{action1_name}/signature` (data) : la signature de l'action.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions` (objet) : les conditions qui permettent de savoir si l'action doit être exécutée ou non.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros` (objet) : un array contenant des macros utilisées pour déterminer l'exécution.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}` (objet) : il s'agit ici de déterminer si une macro peut être exécutée ou non.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload` (objet) : champ principal pour déterminer sur une macro peut être exécutée ou non.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/file` (data) : le nom du fichier qui contient la vérification d'exécution de la macro.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/process_type` (data) : ce que l'on fait avec ce fichier. Pour l'instant, le système supporte `import`.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/execution` (objet) : champ principal contenant les informations d'exécution du fichier `{macro_name}/execution_check_payload/file`.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/execution/mode` (data) : il s'agit du mode d'exécution du fichier contenant la vérification de la macro. Pour le moment, ce paramètre peut avoir pour valeur `exec`.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/execution/content` (data) : le contenu à exécuter. Cela peut être un nom de fonction / méthode, ou bien `all`, qui signifie le fichier sera exécuté comme un script.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/result` (objet) : le champ contenant l'interprétation des résultats.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/result/true` (data) : la valeur que doit retourner l'exécution pour que le système considère que la macro peut être exécutée.
- `files/{filename}/{action}/{action1_name}/signature/execution_conditions/macros/{macro_name}/execution_check_payload/result/false` (data) : la valeur que doit retourner l'exécution pour que le système considère que la macro ne peut pas être exécutée. Je ne sais pas si elle est vraiment utile pour le moment.

- `macros` (objet) : le champ principal de définition des macros.
- `macros/{macro_name}` (objet) : le champ principal de définition de la macro `{macro_name}`.
- `macros/{macro_name}/file` (data) : le path vers le fichier contenant la macro.
- `macros/{macro_name}/process_type` (data) : ce que l'on fait avec ce fichier. Pour l'instant, le système supporte `import`.
- `macros/{macro_name}/execution` (objet) : champ principal contenant les informations d'exécution du fichier `macros/{macro_name}/file`.
- `macros/{macro_name}/execution/mode` (data) : il s'agit du mode d'exécution du fichier contenant la macro. Pour le moment, ce paramètre peut avoir pour valeur `exec`.
- `macros/{macro_name}/execution/content` (data) : le contenu à exécuter. Cela peut être un nom de fonction / méthode, ou bien `all`, qui signifie le fichier sera exécuté comme un script.

Et pour finir, nous appelerons `type` le type d'objet implémenté (`objet`, `plugin`, `module`).
- `sub_{type}` (array) : un array contenant les noms des sous-objets implémentés (sous-objets, sous-plugins, sous-modules).

#### Le système d'objets

Un objet est la couche la plus basse dans la hiérarchie des systèmes.  
Il contient les classes, méthodes, etc, de l'objet.  
L'objet est nécessaire au plugin.  

##### Structure principale

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

##### Le fichier de configuration d'un objet

``` json
{
    "version": "x.x.x",
    "name": "plugin_name",
    "module": "plugin_associated_module",
    "plugin": "object_associated_plugin",
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
    "files":
    [
        "plugin_py_file_path":
        {
            "methods":
            {
                "method1_name":
                {
                    "signature": "method1_signature",
                    "execution_conditions":
                    {
                        "macros":
                        [
                            "macro1_name":
                            {
                                "execution_check_payload":
                                {
                                    "file": "macro_execution_check_payload_py_file_path",
                                    "process_type": "import",
                                    "execution" :
                                    {
                                        "mode": "exec",
                                        "content": "func_or_method_name"
                                    },
                                    "result":
                                    {
                                        "true": 1,
                                        "false": 0
                                    }
                                }
                            }
                        ]
                    }
                },
                "method2_name":
                {
                    "signature": "method2_signature",
                    "execution_conditions":
                    {
                        "macros":
                        [
                            "macro2_name":
                            {
                                "execution_check_payload":
                                {
                                    "file": "macro_execution_check_payload_py_file_path",
                                    "process_type": "import",
                                    "execution" :
                                    {
                                        "mode": "exec",
                                        "content": "all"
                                    },
                                    "result":
                                    {
                                        "true": 1,
                                        "false": 0
                                    }
                                }
                            }
                        ]
                    }
                },
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
        }
    ],
    "macros":
    {
        "macro1_name":
        {
            "file": "macro_py_file",
            "process_type": "import",
            "execution":
            {
                "mode": "exec",
                "content": "func1"
            }
        },
        "macro2_name":
        {
            "file": "macro_py_file",
            "process_type": "import",
            "execution":
            {
                "mode": "exec",
                "content": "all"
            }
        }
    },
    "sub_plugins":
    [
        "plugin_name1", "plugin_name2", "plugin_name3"
    ]
}
```

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
├── plugin1
│   └── plugin1.json
├── plugin2
│   └── plugin2.json
└── plugin3
    └── plugin3.json
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
    },
    "sub_plugins":
    [
        "plugin_name1", "plugin_name2", "plugin_name3", "..."
    ]
}
```

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
├── module1
│   └── module1.json
├── module2
│   └── module2.json
└── module3
    └── module3.json
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

Ce sous-système implémente le type d'objet `map`.  
Le plugin associé pourra donc créer un système de maps.  

Une map est un ensemble qui contient des zones.  

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

Ce sous-système implémente le type d'objet `zone`.  
Le plugin associé pourra donc créer un système de zones.  

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