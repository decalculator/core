# I - corə

Core est un moteur d'exécution d'objets asynchrones.  
Il est dit "ouvert", son code est axé sur la non-contextualité.  
Le rôle de l'utilisateur peut être de créer des objets, ou bien d'en installer puis de les exécuter.  

Ce projet est scindé en deux parties distinctes : le moteur (core), ainsi qu'une démonstration d'utilisation relative à la simulation de vie informatique.  
Elle contient des objets de base, comme l'interface graphique, les mondes, et autres.

## I - Pour commencer

### I - Etapes pour pouvoir exécuter core.

Tout d'abord, commencez par télécharger le projet sur Github à l'url : https://github.com/decalculation/core ou sur Gitlab.

#### I - Installer les requirements.txt

Pour lancer core, il faut tout d'abord installer python et pip.  
Une fois ceci réalisé, il faut se rendre à la racine du projet et exécuter :

``` shell
pip install -r requirements.txt
```

(Pour certaines distributions, il faudra peut-être créer un `venv`, ou bien utiliser `--break-system-packages`).

#### II - Installer Git.

##### I - Sous linux.

Pour cela, vous devez installer la commande `git` avec votre gestionnaire de packets.  
Pour les distributions comme debian, cela peut généralement être réalisé avec :

``` shell
sudo apt install git
```

##### II - Sous macOS.

Pour cela, vous pouvez utiliser `brew` :

``` shell
brew install git
```

##### III - Sous windows.

Vous devez télécharger git à l'url suivante : https://git-scm.com/install/windows.
Ou bien, vous pouvez l'installer via `winget` :

``` shell
winget install --id Git.Git -e --source winget
```

## II - Et voilà.

Tout devrait maintenant être opérationnel pour exécuter core depuis la racine :

``` shell
python sources/main.py
```

## II - Fabriqué avec.

Python pour le langage de programmation, JSON pour les structures de données.  
Aucune intelligence artificielle n'a été utilisée, mais des questions ont pu être cherchées
sur des forums comme StackOverflow. Quand c'est le cas, les liens ont été intégrés dans le code.  
Nous avons utilisé la vidéo suivante pour l'algorithme de Bresenham (et dda, mais non-utilisé) : https://www.youtube.com/watch?v=3_iZcoYrXOM.  

L'origine de cela est essentiellement notre imagination, ce qui peut expliquer certaines incohérences ou erreurs.  
Cependant, l'authenticité de core ne peut être contestée.

## Auteurs

NAULET Marius,
PELLERIN-SPINGLER Côme

## License

Ce projet est sous license GNU GENERAL PUBLIC LICENSE V3, voir le fichier LICENSE.