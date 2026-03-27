# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : math.py
# Rôle    : Ce fichier implémente la classe Math, qui est utile
#           pour effectuer des opérations mathématiques.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import des modules requis par la classe Math.
import asyncio
from zipfile import ZipFile

from core.modules.path.path import *
from core.modules.json.json import *


# Définition de la classe Math.
class Math:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        memory: Memory | None = None,
        pid_manager: PidManager | None = None,
        logs: Logs | None = None,
        pid: Pid | None = None,
        content: Json | None = None,
        ppid: DynamicValue | None = None
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            memory (Memory | None) :
                Description : L'objet Memory parent.
                Valeur par défaut : None.

            pid_manager (PidManager | None) :
                Description : L'objet PidManager parent.
                Valeur par défaut : None.

            logs (Logs | None) :
                Description : L'objet Logs parent.
                Valeur par défaut : None.

            pid (Pid | None) :
                Description : Le PID de l'objet.
                Valeur par défaut : None.

            content (Json | None) :
                Description : Le contenu JSON de l'objet.
                Valeur par défaut : None.

            ppid (DynamicValue | None) :
                Description : Le PID de l'objet parent.
                Valeur par défaut : None.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe Math,
            elle assigne aux attributs leurs valeurs, et s'écrit correctement
            comme instance dans la mémoire parente, ainsi que dans le
            gestionnaire de PIDs.
        """

        # Initialisation de l'USOI de l'objet courant.
        self.usoi = 23

        # Initialisation de l'attribut data.
        initialized = False
        if hasattr(content, "usoi"):
            if content.usoi == 5:
                self.data = Json(content = content)
                initialized = True

        if not initialized:
            self.data = Json()
            initialized = True

        # Initialisation et assignation des attributs.
        self.ppid = ppid

        # Si le PID est None, et que le gestionnaire de PIDs est valide,
        # nous générons un PID pour l'objet courant.
        if pid is None:
            if hasattr(pid_manager, "usoi"):
                if pid_manager.usoi == 1:
                    pid = pid_manager.get_pid(usoi = self.usoi, ppid = self.ppid)

        self.filesystem = filesystem
        self.communication = communication

        self.memory = memory
        self.logs = logs
        self.pid = pid

        # Si le pid et la mémoire sont valides, nous ajoutons l'objet
        # courant dans la mémoire (parente).
        if hasattr(self.pid, "usoi"):
            if self.pid.usoi == 3:
                if hasattr(self.memory, "usoi"):
                    if self.memory.usoi == 1:
                        self.memory.write(Path(f"proc/instances/modules/{self.usoi}/pids/{self.pid.data}"), {"object": self}, mode = 1)

    # Déclaration de la signature de la méthode write.
    def write(
        self,
        path: Path,
        value,
        mode: int = 0
    ) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (Path) :
                Description : Le chemin d'écriture.

            value (any) :
                Description : La valeur à écrire.

            mode (int) :
                Description : Le mode d'écriture.
                Valeur par défaut : 0.

        Sortie :
            written (bool) :
                Description : True si l'écriture a réussi, False sinon.

        Rôle :
            Écrit une valeur à un chemin donné dans la structure JSON.
        """

        # Écrit la valeur au chemin donné, et retourne le résultat.
        return self.data.write(path, value, mode = mode)

    # Déclaration de la signature de la méthode remove.
    def remove(
        self,
        path: Path
    ) -> bool:
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à supprimer.

        Sortie :
            removed (bool) :
                Description : True si la suppression a réussi, False sinon.

        Rôle :
            Supprime la valeur située au chemin donné dans la structure JSON.
        """

        # Supprime la valeur située au chemin donné, et retourne le résultat.
        return self.data.remove(path)

    # Déclaration de la signature de la méthode get.
    def get(
        self,
        path: Path
    ):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin de la valeur à récupérer.

        Sortie :
            value (any) :
                Description : La valeur située au chemin donné dans la
                    structure JSON.

        Rôle :
            Récupère la valeur située au chemin donné dans la structure JSON.
        """

        # Retourne la valeur au chemin donné.
        return self.data.get(path)

    # Déclaration de la signature de la méthode exists.
    def exists(
        self,
        path: Path
    ):
        """
        Type de méthode :
            Synchrone.

        Entrée :
            path (Path) :
                Description : Le chemin à vérifier.

        Sortie :
            exists (bool) :
                Description : True si le chemin existe dans la structure JSON,
                    False sinon.

        Rôle :
            Vérifie si un chemin donné existe dans la structure JSON.
        """

        # Renvoie l'existence du path en bool.
        return self.data.exists(path)

    # Déclaration de la signature de la méthode bresenham_low.
    def bresenham_low(x0, y0, x1, y1):
        """
        Type de méthode :
            Synchrone.

        Entrées :
            x0 (int) :
                Description : La coordonnée x du point de départ.

            y0 (int) :
                Description : La coordonnée y du point de départ.

            x1 (int) :
                Description : La coordonnée x du point d'arrivée.

            y1 (int) :
                Description : La coordonnée y du point d'arrivée.

        Sortie :
            points (list) :
                Description : La liste des points entiers constituant le
                    segment de droite, pour une pente faible (|dy| < |dx|).

        Rôle :
            Calcule les points d'un segment de droite entre deux coordonnées,
            en utilisant l'algorithme de Bresenham pour les pentes faibles.
        """

        # Initialisation de la liste de points avec le point de départ.
        points = [(x0, y0)]

        # Calcul des deltas et de la direction verticale.
        dy = y1 - y0
        dx = x1 - x0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy

        # Calcul des valeurs de décision.
        ddy = 2 * dy
        ddx = 2 * dx
        value = 2 * (dy - dx)
        d = value
        y = y0

        # Parcours des abscisses et calcul des ordonnées.
        for x in range(x0 + 1, x1 + 1):
            if d < 0:
                d += ddy
            else:
                d += value
                y += yi
            points.append((x, y))

        # Retourne la liste des points.
        return points

    # Déclaration de la signature de la méthode bresenham_high.
    async def bresenham_high(x0, y0, x1, y1):
        """
        Type de méthode :
            Asynchrone.

        Entrées :
            x0 (int) :
                Description : La coordonnée x du point de départ.

            y0 (int) :
                Description : La coordonnée y du point de départ.

            x1 (int) :
                Description : La coordonnée x du point d'arrivée.

            y1 (int) :
                Description : La coordonnée y du point d'arrivée.

        Sortie :
            points (list) :
                Description : La liste des points entiers constituant le
                    segment de droite, pour une pente élevée (|dy| >= |dx|).

        Rôle :
            Calcule les points d'un segment de droite entre deux coordonnées,
            en utilisant l'algorithme de Bresenham pour les pentes élevées.
        """

        # Initialisation de la liste de points avec le point de départ.
        points = [(x0, y0)]

        # Calcul des deltas et de la direction horizontale.
        dy = y1 - y0
        dx = x1 - x0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx

        # Calcul des valeurs de décision.
        ddy = 2 * dy
        ddx = 2 * dx
        value = 2 * (dx - dy)
        d = value
        x = x0

        # Parcours des ordonnées et calcul des abscisses.
        for y in range(y0 + 1, y1 + 1):
            if d < 0:
                d += ddx
            else:
                d += value
                x += xi
            points.append((x, y))

        # Retourne la liste des points.
        return points

    # Déclaration de la signature de la méthode bresenham.
    async def bresenham(x0, y0, x1, y1):
        """
        Type de méthode :
            Asynchrone.

        Entrées :
            x0 (int) :
                Description : La coordonnée x du point de départ.

            y0 (int) :
                Description : La coordonnée y du point de départ.

            x1 (int) :
                Description : La coordonnée x du point d'arrivée.

            y1 (int) :
                Description : La coordonnée y du point d'arrivée.

        Sortie :
            result (list) :
                Description : La liste des points entiers constituant le
                    segment de droite entre les deux coordonnées données.

        Rôle :
            Calcule les points d'un segment de droite entre deux coordonnées,
            en utilisant l'algorithme de Bresenham, en choisissant
            automatiquement entre la variante pour pentes faibles et la
            variante pour pentes élevées selon l'orientation du segment.
        """

        # Initialisation du résultat.
        result = []

        # Sélection de la variante de l'algorithme selon la pente du segment.
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                result = await bresenham_low(x1, y1, x0, y0)
            else:
                result = await bresenham_low(x0, y0, x1, y1)
        else:
            if y0 > y1:
                result = await bresenham_high(x1, y1, x0, y0)
            else:
                result = await bresenham_high(x0, y0, x1, y1)

        # Retourne la liste des points.
        return result