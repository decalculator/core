# I - JSON

## I - Objet

Configuration d'un objet :

``` json
{
    "version": version,
    "name": object_name,
    "scripting":
    {
        "class_file": path_to_class_file,
        "class_name": class_name
    }
    "requires":
    {
        "plugins":
        [
            {
                "name": plugin_name,
                "minimum_version": plugin_minimum_version,
                "maximum_version": plugin_maximum_version
            }
        ],
        "core":
        {
            "minimum_version": core_minimum_version,
            "maximum_version": core_maximum_version
        }
    }
}
```

## II - Module

Configuration d'un module :

``` json
{
    "version": "1.0.0",
    "name": "core",
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
        "_entry": "core.py",
        "others": []
    },
    "sub_modules":
    [
        "communication", "configuration", "filesystem", "server", "states", "ui", "world"
    ]
}
```

Configuration des modules :

``` json
{
    "modules": {
        "core": {
            "enabled": true
        },
        "plugins_manager": {
            "enabled": true
        }
    }
}
```

## III - Plugin

Configuration d'un plugin :

``` json
{
    "version": "1.0.0",
    "name": "objets_classiques",
    "requires":
    {
        "modules":
        {
            "core":
            {
                "minimum_version": "eldest",
                "maximum_version": "latest"
            }
        },
        "plugins": [],
        "application":
        {
            "minimum_version": "eldest",
            "maximum_version": "latest"
        }
    },
    "files":
    {
        "_entry": "objets_classiques.py",
        "others": []
    },
    "sub_plugins": []
}
```

Configuration des plugins :

``` json
{
    "plugins": {
        "objets_classiques": {
            "enabled": true
        },
        "terre": {
            "enabled": true
        }
    }
}
```

## IV - Structure d'une sauvegarde (save.json)
``` json
{
    "global_configs":
    {
        "world_name": "world_name",
        "actual_time": "some_data",
        "current_position":
        {
            "zone": "some_zone_id",
            "position": "some_x_y_position"
        }
    },
    "program_configs":
    {
        "paths":
        {
            "objects": "objects",
            "map":
            {
                "config_file": "map/map.json",
                "zones": "map/zones"
            }
            "rules": "rules"
        }
    }
}
```

## V - Structure du fichier de configuration d'une zone (world_name/map/zones/0/config.json)
``` json
{
    "objects":
    {
        "entities":
        {
            "some_object_id1":
            {
                "in_life": true,
                "visible": true,
                "position": "some_x_y_position"
            },
            "some_object_id2":
            {
                "in_life": false,
                "visible": true,
                "position": "some_x_y_position"
            },
            "some_object_id3":
            {
                "in_life": false,
                "visible": false
            }
        },
        "others":
        {
            "some_object_id1":
            {
                "position": "some_x_y_position",
                "visible": true
            }
        }
    }
}
```

## VI - Structure du fichier de configuration d'une map (word_name/map/map.json)
``` json
{
    "zones":
    {
        "some_zone_id1":
        {
            "position": "some_x_y_position"
        },
        "some_zone_id2":
        {
            "position": "some_x_y_position"
        },
        "some_zone_id3":
        {
            "position": "some_x_y_position"
        },
    }
}
```

# II - Python

## I - Structure d'un objet simple

``` python
class Papillon:
    def __init__(self, name):
        self.name = name
        self.value = False

    def _entry(self):
        self.value = True

    def _round(self):
        if self.value:
            self.value = not self.value
        else:
            self.value = Avion("Papillon évolué")

class Cellule:
    def __init__(self, name):
        self.name = name
        self.value = False

    def _entry(self):
        self.value = True

    def _round(self):
        if self.value:
            self.value = not self.value
        else:
            self.value = Papillon("Cellule évoluée")
```

Cet exemple simple présente le principe d'évolution

## II - Structure d'un objet complexe

``` python
class Temps:
    def __init__(self):
        self.now = 0

    def next(self):
        return self.now + chaleur_cpu()
        # ou bien
        return self.now + graine_random()
        # ou bien
        return self.now + puissance()
        # ...
```

# III - Dossiers

## I - Structure du dossier d'un objet

```
*
├─── *.py
├─── ...
│   ├─── ...
│   ├─── ...
│   └─── ...
└─── *.json
```

## II - Structure du dossier d'un monde

```
word_name
├─── objects
│   ├─── 0
│   │   ├─── ...
│   │   └─── ...
│   ├─── 1
│   │   ├─── ...
│   │   └─── ...
│   └─── 2
│       ├─── ...
│       └─── ...
├─── map
│   ├─── zones
│   │   ├─── 0
│   │   │   ├─── ...
│   │   │   └─── config.json
│   │   ├─── 1
│   │   │   ├─── ...
│   │   │   └─── config.json
│   │   └─── 2
│   │       ├─── ...
│   │       └─── config.json
│   └─── map.json
├─── rules
│   ├─── 0
│   │   ├─── ...
│   │   └─── ...
│   ├─── 1
│   │   ├─── ...
│   │   └─── ...
│   └─── 2
│       ├─── ...
│       └─── ...
└─── save.json
```

## III - Structure du dossier d'un objet (word_name/objects/0)
``` json
```

## IV - Structure du dossier d'une règle (word_name/rules/0)
```
```