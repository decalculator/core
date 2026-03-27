# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : path.py
# Rôle    : Ce fichier implémente la classe Path, qui est utile
#           pour utiliser des paths.

# Import d'annotations, qui permet d'annoter des signatures de fonctions
# ou méthodes, en utilisant un type qui n'a pas besoin d'être importé.
from __future__ import annotations

# Import du module os
import os

# Définition de la classe Path.
class Path:

    # Déclaration de la signature de la méthode __init__.
    def __init__(
        self,
        path: str,
        separator: str = '/',
        mode: int = 0
    ) -> None:

        """
        Type de méthode :
            Synchrone.

        Entrées :
            path (str) :
                Description : La valeur du path.

            separator (str) :
                Description : Le séparateur utilisé dans path.
                Valeur par défaut : '/'.

            mode (int) :
                Description : Le mode à utiliser pour le path.
                              0 correspond à un path virtuel uniquement,
                              1 correspond à un path virtuel et matériel
                              (un path vers un fichier, par exemple).
                Valeur par défaut : 0.

        Sortie :
            None

        Rôle :
            Il s'agit de la méthode d'initialisation de la classe
            Path, elle initialise les attributs avec une valeur None
            (hors-USOI) puis appelle la méthode init, qui est asynchrone.
        """

        # Initialisation et assignation des attributs.
        self.usoi = 8
        self.path = path

        # Si self.path est un str.
        if isinstance(path, str):
            # Si il n'est pas vide.
            if self.path:
                # self.splitted_path contient une liste, qui est le path
                # délimité par le délimiteur.
                self.splitted_path = self.path.split(separator)

                # Si le mode est 1, l'attribut os_path prend pour
                # valeur self.splitted_path séparé par le séparateur d'OS
                # ('\' pour windows, '/' pour unix, par exemple).
                if mode == 1:
                    self.os_path = os.sep.join(self.splitted_path)

    # Déclaration d'une représentation avec division.
    def __truediv__(self, value: str):
        # Cette méthode permet d'initialiser un path depuis un autre,
        # en mode = 0 (virtuel).

        return Path(f"{self.path}/{value}")

    def __add__(self, value: str):
        # Cette méthode permet d'initialiser un path depuis un autre,
        # en mode = 1 (matériel).

        return Path(f"{self.path}/{value}", mode = 1)