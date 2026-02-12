# Core

## I - Préambule
Il s'agit d'un portail de simulation de vie en python.  
On emploie le terme "portail" car rien ne doit être statique, tout doit être ouvert pour que l'utilisateur puisse créer son propre monde, ses propres objets dans les bases de données communautaires.  
Il doit pouvoir créer des systèmes sans modifier le code source de notre projet.  
Le but est d'observer l'évolution d'objets dans un monde spécifique à certaines règles.  

## II - Systèmes

### I - Système d'écoulement du temps
On doit pouvoir voir (selon l'échelle choisie) :
- Le temps : seconde, minute, heure, jour, mois, année, ... (voir [IV - Système de dates](#ii---système-de-dates))
- La météo (voir [IV - Système de météo](#iv---système-de-météo))

### II - Système de dates
L'utilisateur redéfinit le système de dates, il peut par exemple complètement supprimer le système de mois, pour ne garder que l'année.  
Il peut par exemple modifier le système d'incrémentation, jour += 2 au lieu de jour += 1, par exemple.

### III - Système de saisons
Comme pour le temps, l'utilisateur peut tout modeler.  
Une année pourrait par exemple contenir 20 saisons, c'est l'utilisateur qui définit les règles.  
Chaque saison peut avoir des spécificités, par exemple en été température += 10 (très imagé et statique pour le moment, le but est de rendre cela beaucoup plus complexe pour être ouvert aux possibilités).

### IV - Système de météo
Comme pour les autres choses, l'utilisateur peut tout modeler.  
Notons que chaque météo a ses **probabilités** et ses **conséquences**.

### V - Système de probabilités
Un évènement peut avoir une probabilité d'apparition.  
Par exemple, on pourrait imaginer une probabilité de 70% de chance de pluie en novembre.

### VI - Système de conséquences (déterminisme)
Un évènement subit des conséquences.  
Il existe (pour le moment) deux types de conséquences :
- La conséquence d'avant apparition : ce sont les conséquences qui font que l'évènement arrive (par exemple, l'évènement "beau temps" est actif, et donc l'évènement "ouverture des tournesols" s'exécute à son tour).
- La conséquence d'après apparition : ce sont les conséquences que vont engendrer l'exécution de l'évènement (par exemple, les fleurs sont boostées grâce à la pluie).

### VII - Système d'aléatoire
L'aléatoire n'existant pas en informatique classique, nous pourrions (pour commencer) utiliser random.org (API simple) en cas de besoin (200 000 bits "aléatoires" gratuits par jours).

### VIII - Système d'objets
Un objet représente les entités du monde, il existe (pour le moment) trois types d'objets :
- L'entité consciente libre : il s'agit d'une entité qui a une conscience et qui est libre de ses mouvements, par exemple. (Exemple : un oiseau).
- L'entité consciente : il s'agit d'une entité qui a une conscience, mais qui n'est pas vraiment libre de ses déplacements, par exemple. (Exemple : une plante, bien qu'elle grandisse).
- L'entité non-consciente non-vivante : il s'agit d'une entité qui n'a ni conscience, ni liberté, par exemple. (Exemple : une table).  

C'est l'utilisateur qui créer et choisit les entités de son monde, cela pourrait être une fleur comme la terre par exemple.  
Un objet a aussi ses **probabilités** et ses **conséquences**.

### IX - Système de mondes
Un monde est (par défaut) constitué :
- D'un ensemble de règles (voir [X - Système de règles](#x---système-de-règles)).
- D'un ensemble d'objets (voir [VIII - Système d'objets](#viii---système-dobjets)).
- D'un système d'écoulement du temps (voir [I - Système d'écoulement du temps](#i---système-découlement-du-temps)).
- D'un système de saisons (voir [III - Système de saisons](#iii---système-de-saisons))
- D'un système de météo (voir [IV - Système de météo](#iv---système-de-météo))

### X - Système de règles
Les règles sont les propriétés fondamentales du monde.  
Par exemple : la gravité.

### XI - Système d'obligations futures
Une obligation future est une condition pour altérer le futur du monde et des objets qui y vivent.  
L'objectif est de créer plusieurs scénarios probables en fonction d'une obligation future, pour permettre à l'utilisateur de modeler le futur de son monde.  
Exemple : si nous avons un groupe d'entités qui vivent ensembles, et qu'une entité externe attaque une entité de ce groupe, alors il pourrait y avoir conflit.  
On peut forcer le conflit, pour voir ce qu'il va se passer, en posant cette obligation future : entité 1 attaque entité 2 tel jour.  
L'utilisateur peut donc forcer un objet (conscient et "libre") à faire une chose à un instant T.

### XII - Système de scénarios

### XIII - Système de sauvegardes d'un monde
Un monde peut être sauvegardé de deux manières :
- Localement : le dossier de sauvegarde du monde sera enregistré sur le disque de l'utilisateur.
- En ligne : le dossier de sauvegarde du monde sera enregistré sur les serveurs communautaires.

### XIV - Menu de lancement des mondes
Il y a globalement deux options :
- Lancement local : on demande à l'utilisateur de sélectionner le dossier de son monde, si il ne se trouve pas dans le dossier par défaut.
- Lancement serveur : on demande à l'utilisateur de saisir l'identifiant unique de son monde, ainsi que l'url vers le serveur communautaire.

### XV - Système de communauté
Une communauté est un espace publique qui regroupe des partages d'objets, de règles, de mondes, en ligne.  
Chaque objet, règle, monde, ou autre de la communauté a un identifiant unique de 10 chiffres : `0123456789`.

### XVI - Scripting d'un objet
Un objet est donc une entité (voir [VIII - Système d'objets](#viii---système-dobjets)).  
Nous voulons faire en sorte que le portail puisse s'adapter à tout type d'objet importé par l'utilisateur, tout en préservant les potentialités.  
L'objet doit donc définir son propre fonctionnement et comportement.  
Pour l'instant, voici une liste minimale de choses que devrait contenir les paramètres d'un objet :
- Est-ce une entité consciente libre, une entité consciente, ou bien une entité non-consciente non-vivante ?
- Conditions nécessaires à la vie (par exemple, pour une plante cela pourrait être les nutriments de la terre, la lumère, l'eau, etc).
- Que se passe-t-il quand l'une de ces conditions n'est plus remplie ?
- Que se passe-t-il quand l'objet meurt ? Est-ce que quelque chose reste apparent (un cadavre, par exemple, qui devient donc un autre objet), ou bien il se décompose ?
- Y a-t-il une évolution de l'objet ? Par exemple, il pourrait être entité 1 jusqu'à ce qu'une certaine condition soit réalisée, puis devenir entité 2.

### XVII - Système d'évolution d'objet
Comme mentionné dans [XVII - Scripting d'un objet](#xvii---scripting-dun-objet), un objet peut subir des évolutions (mutations).  

### XVIII - Système de zones
Pour ne pas surcharger le fichier map.json, nous allons utiliser un système de zones.  
Seules les zones proches seront chargées en mémoire, pour optimiser les performances de l'application.  
Cela peut être vu comme des sortes de régions du monde de l'utilisateur, si l'on veut.

### XIX - L'espace blanc
L'espace blanc est l'origine de tout, c'est ce qui se trouve à l'instant 0, avant que l'utilisateur ait créé des objets / des formules / des règles / etc.  
Comme son nom l'indique, il s'agit d'un espace vide, blanc.  
Rien ne s'y passe.

## IV - Dynamisme

### I - Ouvrir le champ des possibles
Le principe est que le programme soit le moins contextuel possible, c'est pour cela que l'on parle de développement d'un portail.  
Pour cela, plusieurs fonctions dynamiques propres à python peuvent être utilisées :
- `exec()` : permet d'exécuter du code python, sans compilation
- `eval()` : permet d'évaluer une expression, sans compilation
- `write()` : permet de (ré)écrire le propre code du programme, sans compilation

### II - Les objets
voir

### III - Moteur de gestion d'objets
voir

### IV - Les états
Pour orchestrer le bon fonctionnement de l'application, une classe `States` est présente dans `app/states/states.py`.  
Voici les principales fonctionnalités :
- `states.create(self, name)` : créer un état
- `states.remove(self, name)` : supprimer un état
- `states.assign(self, name, param, value)` : ajouter un paramètre param qui a pour valeur value à l'état name
- `states.unassign(self, name, param)` : supprimer la valeur value du paramètre param de l'état name
- `states.get(self, name, param)` : obtenir la valeur d'un param de name
- `states.append(self, name, param, value)` : append une valeur value au paramètre param de l'état name (si il s'agit d'une liste)
- `states.unappend(self, name, param, value)` : supprimer une valeur value du paramètre param de l'état name (si il s'agit d'une liste)
Chaque classe "système" du moteur ont comme attribu d'instantes un objet commun de type `states`, pour y inscrire les états en cours.  

### V - UI
Pour l'UI, nous utiliserons très probablement `fastapi`, car il est plus fait pour le fonctionnement asynchrone que flask.  
Nous optons pour un render web car, tout doit être modelable, c'est probablement bien plus simple de modifier du code source HTML / CSS / JS qu'une application tkinter, par exemple.  
La classe `server` est présente dans `app/server/server.py`, elle contient la logique du serveur :
- `Server(states, ip, port)`
- `server.run()` : permet de démarrer le serveur avec les paramètres séléctionnés.
La classe `ui` est présente dans `app/ui/ui.py`, elle contiendra la logique d'UI, je ne sais pas encore quoi exactement.  
En tout cas, le serveur est lié à l'ui, mais ils seront séparés.

### VI - Configurations
La classe principale liée aux configurations est `Configuration`, elle se situe dans `app/configuration/configuration.py`.  
Voici les méthodes principales de celle-ci :
- `Configuration(self, states)` : il s'agit d'une initialisation simple, car self.configuration peut en contenir plusieurs
- `configuration.create(self, name)` : permet de créer une configuration avec un nom choisi, dans self.configuration
- `configuration.assign(self, name, param, value)` : permet de définir une valeur pour un param de la configuration name
- `configuration.load(self, name, path_param, param)` : permet de load un path stocké à path_param, le contenu sera stocké dans param de name
- `configuration.unload(self, name, param)` : permet d'unload le contenu stocké dans param de name

### VII - Communication
La classe principale liée aux requêtes est `Communication`, elle se situe dans `app/communication/communication.py`.  
Les méthodes principales sont :
- `Communication(self, states)` : il s'agit d'une initialisation simple, car self.communication peut en contenir plusieurs
- `communication.create(self, name)` : permet de créer une communication avec un nom choisi, dans self.communication
- `communication.assign(self, name, param, value)` : permet de définir une valeur pour un param de la communication name
- `communication.get(self, name, url_param, param)` : permet de GET un url et de stocker la réponse en JSON si disposible, sinon HTML dans le param donné
- `communication.post(self, name, url_param, json_param, param)` : permet de POST à un url, en envoyant des paramètres JSON, et en stockant le résultat dans le param donné

### VIII - Synchronisme
Les taches s'exécutent de manière asynchrones, c'est à dire indépendamment les unes des autres, en même temps.  
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

## V - Les objets

### I - Objets simples

Pour que la gestion d'objets soit la moins contextuelle possible, mais fonctionnelle, un ensemble de règles simples doivent être respectées :
- Un objet est en réalité du code python avec une api simple que nous créérons, son format principal est donc `*.py`
- Un objet est une classe
- Le fichier contenant le code de l'objet doit avoir :
1) Une classe au nom de l'objet
2) Un contructeur pour la classe de l'objet : `__init__(self, ...)`  

(voir structures.md)

### II - Objets complexes

Certains objets sont appelés `objets complexes`.  
Ces objets sont moins statiques que les objets classiques, leur implémentation est plus compliquée.  
Par exemple, le temps pourrait être un objet complexe. En effet, son implémentation semble compliquée, car il est l'origine de tout.  
Comment définir le temps ? Car les autres objets pourront être basés sur un compteur de tour qui est lui-même basé sur le temps.  
Le temps n'est pas nécessairement une suite régulière, il pourrait par exemple être représenté par la chaleur du processeur, ou même la puissance de calcul à un instant T.  
Il pourrait être basé sur un incrément aléatoire.  

Par exemple : (voir structures.md)  

Le problème de ces objets reste leur incorporation au reste du système, car ils sont moins statiques.  
Et puis, comment savoir quand appeler cette méthode next ?  
La classe Temps ne doit pas définir quand appeler la fonction next, elle doit simplement la définir, pour le moment.

### III - Configuration d'un objet classique
Un objet est donc un dossier contenant une classe dans un fichier `*.py`.  
Mais ce fichier n'est pas seul, avec vient une configuration, dans un fichier `*.json`.  

Voici la structure principale d'un dossier objet : (voir structures.md)  

A noter que, pour un objet statique (qui n'évolue pas, ne bouge pas, etc), ces arrays peuvent rester vides, il n'y aura alors aucune évolution (aucun code exécuté).  

### IV - Dépendances
Les objets ont dans la plupart des cas des dépendances, elles se trouvent dans le paramètre `requires` du fichier de configuration de l'objet.  
Voici la structure générale de `requires` :
- `plugins` :
    - `name` : le nom du plugin requis
    - `minimum_version` : la version minimale du plugin requise pour l'objet
    - `maximum_version` : la version maximale du plugin requise pour l'objet
- `core` :
    - `minimum_version` : la version minimale du core (moteur) requise pour l'objet
    - `maximum_version` : la version maximale du core (moteur) requise pour l'objet

Tous ces paramètres peuvent prendre les valeurs suivantes :
- `{float}` : un float qui représente la version, au format x.x.x (1.0.0, 17.0.0, ...)
- `eldest` : la version la plus ancienne du package
- `latest` : la version la plus récente du package

### V - Plugins

Cette zone permettrait d'installer des sortes de plugins qui modifient et ajoutent des fonctionnements au moteur du système.

### VII - Configuration d'un objet complexe

Un objet complexe n'étant pas statique, il n'a pas de prérequis dans le fichier `*.json`.  
Cependant, le système doit être capable de le comprendre.  
C'est pour cela qu'une zone spéciale va être implémentée, qui sera une zone de partage entre le système (core) et l'utilisateur.  
L'utilisateur devra donc implémenter une partie du moteur, malgré tout, mais ce sera uniquement réservé aux utilisateurs qui savent ce qu'ils font.  
Pour les autres, des plugins seront déjà disponibles, pour les objets classiques, par exemple.  
Malgré tout, une API devra être proposée, avec des macros pour faire des choses complexes en peu de code.  

Un objet complexe contient donc bien un fichier `*.json`, ou tout autre format implémenté dans la zone de partage.  
L'utilisateur implémentera donc la partie du moteur qui décidé de quoi faire, à quel moment, vis à vis de cet objet complexe.  

### VIII - Modules

Un module est plus large qu'un plugin.  
Par exemple, le plugin manager est un module.  
Les modules sont dans core/modules.  