"""Inimigos enfrentados em batalha."""

from dataclasses import dataclass


@dataclass
class Monstro:
    nome: str
    hp: int
    ataque: int
    defesa: int
    ouro: int
    xp: int = 0
    hp_maximo: int = 0

    def __post_init__(self) -> None:
        if not self.hp_maximo:
            self.hp_maximo = self.hp

    @property
    def vivo(self) -> bool:
        return self.hp > 0

    def receber_dano(self, dano: int) -> None:
        self.hp = max(self.hp - dano, 0)

    def status(self) -> str:
        largura = 20
        cheio = round(largura * max(self.hp, 0) / max(self.hp_maximo, 1))
        barra = f"[{'#' * cheio}{'.' * (largura - cheio)}] {self.hp}/{self.hp_maximo}"
        return f"{self.nome}\n  HP  {barra}\n  Ataque {self.ataque} | Defesa {self.defesa}"
