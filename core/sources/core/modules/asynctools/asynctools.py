# Projet  : core
# Auteurs : Marius NAULET, Côme PELLERIN-SPINGLER

# Fichier : asynctools.py
# Rôle    : Ce fichier implémente des fonctions utiles en asynchrone.

# Import du module asyncio.
import asyncio

# Déclaration de la signature de la fonction async_input.
async def async_input(prompt: str) -> str:
    """
    Type de fonction :
        Asynchrone.

    Entrée :
        prompt (str) :
            Description :
                Le texte à transmettre à la fonction input().

    Sortie:
        (str) :
            Description :
                Le texte saisi par l'utilisateur.

    Rôle :
        Appeler la fonction input() dans un thread géré par asyncio,
        pour ne pas bloquer l'exécution d'autres objets asynchrones.
    """

    # Attend le retour de la fonction input() qui s'exécute dans un thread
    # asyncio séparé, puis renvoie son résultat.
    return await asyncio.to_thread(input, prompt)
