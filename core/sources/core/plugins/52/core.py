"""
Rôle     : Ceci est un essai, l'idée étant de faire exécuter core, à core, en tant qu'objet (ici plugin)
Statut   : fonctionnel
Variante : core.json peut directement rediriger vers main() d'entry.py, les deux fonctionnent
"""

from __future__ import annotations

import asyncio

from main import *

async def entry(**kwargs):
    await main()