"""Catálogo de itens da loja."""

from rpg.models.item import Item

CATALOGO: tuple[Item, ...] = (
    # A cura é percentual: continua relevante no nível 1 e no nível 15.
    Item("Poção de Cura", custo=30, atributo="hp", valor=40, consumivel=True, percentual=True),
    Item("Espada", custo=50, atributo="ataque", valor=6),
    Item("Escudo", custo=40, atributo="defesa", valor=5),
    Item("Armadura", custo=80, atributo="defesa", valor=10),
)
