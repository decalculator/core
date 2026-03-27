# Présentation du modèle

## Présentation globale

Nous vous invitons à lire le fichier `docs/core - trame de recherche.md`, qui est assez précis sur le sujet.

## Présentation de l'équipe

Nous sommes donc deux dans le groupe, Marius et Côme.  
Côme développe assez rarement en python, alors Marius a été d'une grande aide.  

Concernant les rôles de chacuns, Marius a beaucoup travaillé sur `asyncio`, les threads, que nous connaissions peu.  
Il s'agissait de la partie clef, nous avons passé beaucoup de temps sur celle-ci (problèmes de compréhension, au début).  

Sinon, Côme a beaucoup réfléchit au projet sans écrire de code, au début (les premières documentations).  
Ensuite, nous nous sommes partagés les tâches : Côme s'est plus occupé des modules bas-niveau, et Marius des plugins, comme l'interface graphique avec DearPyGui. Cela n'a pas été chose aisée puisque nous ne connaissions pas DearPyGui auparavant.  

Et ensuite, nous avons imaginé un système de "bouteilles", où chaque objet peut se faire initialiser avec son propre objet, qui est son parent.  
Le système de PID, PPID, CPIDS a été réalisé par Marius et Côme, car les choses n'ont pas vraiment été faites dans le bon ordre :

Nous avons beaucoup fait de vas et vient, entre modules bas niveau, puis structure qui change, et donc malheureusement beaucoup de pertes de temps.  

Niveau gestion du temps, Marius a dû passer environ 31 heures sur le projet.  
Et Côme a passé environ 26 heures, Marius corrigeait les quelques erreurs d'inattention de Côme.  

## Étapes du projet

Tout d'abord, il y a eu l'idée principale, qui a été imaginée par Marius.  
Il s'agissait d'une application de simulation de vie informatique représentée en 3d sur une carte.  
Ce projet devait se nommer Zoé.  

Puis, Côme a commencé la documentation.  
Mais l'idée s'est plus tournée vers un moteur d'exécution d'objets asynchrones.  
Ce projet s'intitula core, idée de Marius.  

Pendant que Marius commençait à réfléchir à l'interface graphique, DearPyGui, l'asynchrone, etc.  
Côme a développé les modules bas-niveau.  

Et enfin, nous travaillons en symbiose sur ce projet en cours.  
Monsieur Nauleau, notre professeur de NSI a aussi été d'un grand soutient, car il lisait nos documentations et les validait,
et posait des questions sur ce qui lui semblait flou.

Enfin, core suivit de ses fonctionnalités est né.

## Validation de l’opérationnalité et du fonctionnement

Etat d'avancement du projet au moment du dépôt : core n'est pas terminé.  
En réalité, il n'est pas possible de terminer core.  
Puisque l'idée étant que c'est l'utilisateur qui développe les objets, alors les possibilités sont nombreuses.  
Mais même d'un point de vu interface graphique, des options ne sont encore pas disponibles ou instables, comme l'update etc.  

Pour vérifier l'absence de bugs, nous avons testé sur différents OS, avec des machines virtuelles.  
Mais le programme reste encore instable, des bugs sont sans doute possibles.

Les difficultés ont été surtout vis-à-vis de l'asynchronisme, nous avons quelque peu eut du mal pour comprendre.  
Nous nous sommes donc documentés, et de nombreux tests ont été effectués.  

Et un autre problème a été que certains modules bas-niveaux ont été développés trop tard, comme le module Path.  
A chaque fois que quelque chose de bas-niveau est implémenté trop tard, il faut repasser sur chaque objet, un par un.  
Nous avons donc appris à réfléchir avant de coder, penser aux possibilités avant de les écrire.

## Ouverture

Voici de potentielles idées pour améliorer le projet :
- Les modules sont plutôt complets, ce qu'il manque en général est une diversité d'objets.
Il faudrait des utilisateurs complétants des repos, en ligne, pour avoir beaucoup d'objets.

- Core est pour le moment uniquement ouvert au monde informatique.
- Pour l'instant, une machine seule doit exécuter tous les objets.
Cela signifie que pour un ensemble énorme, cela deviendrait compliqué.

- Analyse critique du projet :
Ce projet est pour nous assez poussé conceptuellement, mais largement perfectible.  
D'un point de vu performances, par exemple le système d'exécution d'objets pourrait largement être amélioré.  

- Compétences personnelles développées :
Nous avons appris à utiliser des interfaces graphiques comme DearPyGui, l'asynchronisme, la récursivité, les PIDs, PPIDs, CPIDs.  
La programmation orientée objets, puisque tous les objets sont des classes.  
Et à deux, nous avons réussi à adopter une harmonie dans notre duo pour travailler efficacement.  
Cela nous a permis de comprendre que nous pourrions travailler sur d'autres projets ensembles.

- Démarches d'inclusion :
Les couleurs sont neutres pour les daltoniens (noir et blanc).  
Pour les alophones, l'anglais est la langue universelle, elle est disponible.  
Pour les malentendants, core n'a pas besoin de son.  
Pour les personnes atteintes de dyslexie, le texte de l'UI est assez simple.

Mais nous n'avons pas tout réalisé, les utilisateurs peuvent développer objets relatifs à l'inclusion.