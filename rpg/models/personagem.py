"""Personagem controlado pelo jogador."""

from typing import Optional

from rpg.config import (
    CURA_TOTAL_AO_SUBIR,
    GANHO_POR_NIVEL,
    HP_INICIAL,
    PERDA_DE_OURO_NA_DERROTA,
    VIDAS_INICIAIS,
    XP_PARA_SUBIR,
)
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
        self.nivel = 1
        self.xp = 0
        self.vidas = VIDAS_INICIAIS
        self.inventario: list[Item] = []

    # ------------------------------------------------------------ consultas
    @property
    def vivo(self) -> bool:
        return self.hp > 0

    @property
    def xp_para_subir(self) -> int:
        """XP que falta acumular para alcançar o próximo nível."""
        return XP_PARA_SUBIR * self.nivel

    @property
    def poder(self) -> int:
        """Medida agregada usada para escalar os inimigos."""
        return self.ataque + self.defesa

    def consumiveis(self) -> list[Item]:
        return [item for item in self.inventario if item.consumivel]

    def pode_pagar(self, custo: int) -> bool:
        return self.ouro >= custo

    def status(self) -> str:
        return (
            f"{self.nome} — Nível {self.nivel}\n"
            f"  HP  {self._barra(self.hp, self.hp_maximo)}\n"
            f"  XP  {self._barra(self.xp, self.xp_para_subir)}\n"
            f"  Ataque {self.ataque} | Defesa {self.defesa} | "
            f"Ouro {self.ouro} | Poções {len(self.consumiveis())} | "
            f"Vidas {'@' * self.vidas}"
        )

    @staticmethod
    def _barra(atual: int, maximo: int, largura: int = 20) -> str:
        maximo = max(maximo, 1)
        cheio = round(largura * max(atual, 0) / maximo)
        return f"[{'#' * cheio}{'.' * (largura - cheio)}] {atual}/{maximo}"

    # --------------------------------------------------- alterações de estado
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
        if not self.pode_pagar(custo):
            return False
        self.ouro -= custo
        return True

    def ganhar_xp(self, quantidade: int) -> list[int]:
        """Acumula XP e sobe quantos níveis forem possíveis.

        Devolve a lista de níveis alcançados (ex.: [2, 3] quando o herói
        sobe dois de uma vez), para a interface anunciar um por um.
        """
        self.xp += quantidade
        alcancados: list[int] = []

        while self.xp >= self.xp_para_subir:
            self.xp -= self.xp_para_subir
            self.nivel += 1
            alcancados.append(self.nivel)
            self.hp_maximo += GANHO_POR_NIVEL["hp"]
            self.ataque += GANHO_POR_NIVEL["ataque"]
            self.defesa += GANHO_POR_NIVEL["defesa"]
            self.hp = self.hp_maximo if CURA_TOTAL_AO_SUBIR else self.hp

        return alcancados

    def ser_resgatado(self) -> tuple[bool, int]:
        """Consome uma vida após uma derrota.

        Devolve (foi_resgatado, ouro_perdido). Sem vidas restantes, o
        herói permanece caído e a aventura termina.
        """
        if self.vidas <= 0:
            return False, 0

        self.vidas -= 1
        perdido = round(self.ouro * PERDA_DE_OURO_NA_DERROTA / 100)
        self.ouro -= perdido
        self.hp = self.hp_maximo
        return True, perdido

    def adquirir(self, item: Item) -> None:
        """Guarda o item. Equipamentos valem na hora; consumíveis ficam no inventário."""
        self.inventario.append(item)
        if not item.consumivel:
            self._aplicar_efeito(item)

    def usar_consumivel(self) -> Optional[tuple[Item, int]]:
        """Consome o primeiro item consumível do inventário.

        Devolve (item, efeito) ou None se não houver nenhum.
        """
        for indice, item in enumerate(self.inventario):
            if item.consumivel:
                self.inventario.pop(indice)
                return item, self._aplicar_efeito(item)
        return None

    def evoluir(self, hp: int = 0, ataque: int = 0, defesa: int = 0) -> None:
        """Recompensa permanente fora da curva de XP (ex.: derrotar um chefe)."""
        self.hp_maximo += hp
        self.hp += hp
        self.ataque += ataque
        self.defesa += defesa

    # ------------------------------------------------------------ internos
    def _aplicar_efeito(self, item: Item) -> int:
        if item.atributo == "hp":
            pontos = round(self.hp_maximo * item.valor / 100) if item.percentual else item.valor
            return self.curar(pontos)
        if item.atributo == "ataque":
            self.ataque += item.valor
        elif item.atributo == "defesa":
            self.defesa += item.valor
        else:
            raise ValueError(f"Atributo desconhecido: {item.atributo}")
        return item.valor
