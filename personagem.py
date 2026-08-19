"""Personagem controlado pelo jogador."""

from rpg.config import HP_INICIAL
from rpg.models.item import Item


class Personagem:
    """Guarda o estado do herói e expõe operações sobre esse estado.

    Não decide *quando* atacar, curar ou comprar: isso é papel do
    pacote rpg.core.
    """

    def __init__(self, nome: str, hp: int = HP_INICIAL) -> None:
        self.nome = nome
        self.hp_maximo = hp
        self.hp = hp
        self.ataque = 0
        self.defesa = 0
        self.ouro = 0
        self.inventario: list[Item] = []

    # --- consultas ---
    @property
    def vivo(self) -> bool:
        return self.hp > 0

    def pode_pagar(self, custo: int) -> bool:
        return self.ouro >= custo

    def status(self) -> str:
        return (
            f"{self.nome} | HP: {self.hp}/{self.hp_maximo} | "
            f"Ataque: {self.ataque} | Defesa: {self.defesa} | Ouro: {self.ouro}"
        )

    # --- alterações de estado ---
    def receber_dano(self, dano: int) -> None:
        self.hp = max(self.hp - dano, 0)

    def curar(self, pontos: int) -> int:
        """Cura respeitando o HP máximo e devolve quanto foi recuperado."""
        anterior = self.hp
        self.hp = min(self.hp + pontos, self.hp_maximo)
        return self.hp - anterior

    def ganhar_ouro(self, quantidade: int) -> None:
        self.ouro += quantidade

    def gastar_ouro(self, custo: int) -> bool:
        """Debita o ouro. Devolve False se não houver saldo."""
        if not self.pode_pagar(custo):
            return False
        self.ouro -= custo
        return True

    def aplicar(self, item: Item) -> None:
        """Aplica o efeito de um item já pago."""
        if item.atributo == "hp":
            self.curar(item.valor)
        elif item.atributo == "ataque":
            self.ataque += item.valor
        elif item.atributo == "defesa":
            self.defesa += item.valor
        else:
            raise ValueError(f"Atributo desconhecido: {item.atributo}")

        if not item.consumivel:
            self.inventario.append(item)

    def evoluir(self, hp: int = 0, ataque: int = 0, defesa: int = 0) -> None:
        """Recompensa permanente (ex.: derrotar um chefe)."""
        self.hp_maximo += hp
        self.hp += hp
        self.ataque += ataque
        self.defesa += defesa
