"""Modelos de domínio: guardam estado e comportamento próprio,
sem conhecer interface (print/input) nem regras de fluxo do jogo.
"""

from rpg.models.item import Item
from rpg.models.monstro import Monstro
from rpg.models.personagem import Personagem
from rpg.models.terreno import Terreno

__all__ = ["Item", "Monstro", "Personagem", "Terreno"]
