La nature du code de core est plutôt simple : notre imagination.  
Aucune intelligence artificielle n'a été utilisée, du début à la fin.  
Je vous invite à lire le dossier docs ainsi que le préambule pour constater que la recherche a été la partie la plus complexe dans la réalisation de core.  

Cependant, des modules ont été utilisés.  
Par exemple, nous n'avions pas le niveau pour développer notre propre interface graphique complète pour le temps donné,
alors nous avons employé DearPyGui, qui est wrapper Python de DearImGui.  
Même si il est nativement en C++, nous avons considéré que l'utilisation du wrapper était autorisée.  

En dehors de cela, quelques modules comme requests ou asyncio ont été utilisés.  
Core étant encore en développement, je vous invite à lire le fichier requirements.txt.  

Et pour terminer, quelques rares concepts peuvent provenir d'internet.  
Pour chacun d'entre-eux, le code contient un commentaire vers le code original, qui a été retravaillé la plupart du temps.  
Ces concepts sont rares, nous avons essayé d'utiliser internet le moins possible.  

Parmis ceux-ci se trouvent une vidéo expliquant Bresenham, pour les projections 3d, ainsi qu'une explication concernant l'exploration de sous-dossiers / fichiers d'un dossier.  

Toute utilisation est créditée dans le code.