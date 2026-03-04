à développer / continuer :
    "core":
        - updater : updater.update à continuer :
            ce que j'ai commencé à faire est un remplacement basique, nous pourrions choisir quoi keep (dossier data, objets, etc) et ne pas supprimer ce que l'user veut garder, c'est la version 1
            mais la meilleure version serait celle qui indique précisément quel fichier a été update, pour ne pas faire un "gros" remplacement, seulement ce qui est utile
            et parallèlement à cela, l'idéal de l'idéal (si j'avais le temps...) serait une update SANS MÊME avoir besoin de quitter l'app ensuite, désactiver temporairement le module, l'update, et le réactiver
        - pouvoir installer des packs d'objets
        - système de repos d'objets, pouvoir stocker des URL vers des ponts (par exemple en json ou txt) qui pointent vers des url github d'objets (tout type), ce sont littéralement des "librairies"
        - système d'installation d'un repo (c'est juste un url à stocker statiquement)
        - système d'installation d'objet sur un repo, avec recherche (dans le menu objects ? Peut-être)
        - système de communauté : je pense que c'est ce que je vais le moins prioriser, car le temps presse. Je pourrais toujours le développer une fois le projet rendu
        - système de mutation (un objet peut en devenir un autre)

    la nature ! (contexte) :
        - date : système de dates
        - season : système de saisons
        - weather : système de météo
        - probability : système de probabilités
        - consequence : système de conséquences (déterminisme)
        - aleatory : système d'aléatoire
        - rule : système de règles
        - possibilities (scénarios) : système de scénarios
        - save : système de sauvegardes
        - map : système de maps
        - zone : système de zones (une map contient des zones, un ensemble contient des maps)
        - entity : un système d'entités, mais est-ce que je vais vraiment le garder ? Car un objet classique ou complexe peut très bien faire ce que fait une entité, donc ça ne sert à rien ?

ce que j'aimerais personnellement ajouter :
    - un moyen d'exécuter un objet directement compilé, en C ou C++, par exemple.
    cet objet devrait être compilé pour l'architecture de l'ordinateur / l'OS qui fait tourner core.
    cela pourrait faire référence à "dynamiC", un autre projet réalisé qui permet de développer un launcher statique en C qui exécute un exécutable compilé qu'il ne connait pas à l'avance via des ponts.
    mais là, ce ne serait pas seulement exécuter, mais aussi une mémoire partagée etc (ce que je n'ai encore jamais réalisé, dynamiC était juste l'exécution d'un payload que l'on ne définit pas statiquement dans le launcher).

et c'est globalement tout ce que nous avons évoqué dans la documentation qui n'a pas encore été réalisé.
mais il manque une chose cruciale que j'ai évité jusqu'à maintenant : la "vie".

Qu'est-ce que nous voulons modéliser, vraiment ?
Car nous pouvons créer un objet cellule, qui fonctionne de la manière la plus proche d'une vraie cellule, avec un objet ADN etc.

Mais donc, mis à part les cellules, qu'est-ce que nous pourrions représenter ?
Si nous voulons représenter des fleurs, par exemple, il est impossible pour le temps qu'il nous reste de le faire de manière "chronologique" (partir de cellules, pour former x chose, qui elle-même forme x chose, qui forme au final la fleur).
Alors, nous devrions opter pour le choix "grossier et peu précis" : développer directement l'objet fleur, cela ne me plaît pas vraiment.

# autres modifications

## 1

je voudrais changer la structure du fichier `modules.json`, `plugins.json`, `objects.json` : le fait qu'un paramètre se nomme `modules`, `plugins`, `objects` à l'intérieur ajoute des conditions pour peu.
cela pourrait juste être :

``` json
{
    "object1":
    {
        "...": "..."
    }
}
```

pour tous, quelque soit le type d'objet. ce qui changerait serait donc uniquement le path.

## 2

Je dois fix toutes les classes, pour bien utiliser `Console`, `Variables`.
J'ai délaissé cela pour gagner du temps, mais c'est mieux d'être cohérent.

# réalisation

je vais commencer par le système de repo : j'aime l'idée, et c'est relativement simple à réaliser, il faut juste une syntaxe JSON pour les bridges.
`Repo` sera un module, ou bien un plugin, et il stockera les bridges dans core/data/repo/{repo_name}/{repo_name}.json
par exemple, bridge1.json :

``` json
{
    "repo":
    {
        "url": "https://raw.com/bridge1.json",
        "name": "repo1",
        "version": "1.0.0"
    },
    "content":
    {
        "objects":
        {
            "cell1":
            {
                "url": "https://github.com/decalculator/cell1",
                "type": "github_repo"
            },
            "cell2":
            {
                "url": "https://raw.com/cell2.zip",
                "type": "raw_zip"
            }
        },
        "plugins":
        {
            "...": "..."
        },
        "modules":
        {
            "...": "..."
        }
    }
}
```

on pourrait même imaginer un repo qui contient des repos (pont vers des ponts) ! Mais nous y reviendrons ::
j'opte ici pour le fait que `Repo` soit un plugin, car il ne semble être utilisé que par `Ui` pour le moment, qui est un plugin. J'essaye de rester à la même couche, car un module ne DOIT PAS avoir besoin d'un plugin (tout plugin peut (doit pouvoir) être désintallé sans souci, en théorie).

je vais terminer le système de repo plus tard, j'ai déjà bien avancé côté classe et UI.

j'ai trouvé la solution pour suivre l'exécution des objets complexes, voir tests/a.py