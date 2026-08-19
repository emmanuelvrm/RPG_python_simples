"""Locais exploráveis do mapa."""

from rpg.config import LIMITE_MISSOES_POR_TERRENO


class Terreno:
    """Controla apenas o progresso de missões do local."""

    def __init__(self, nome: str, limite_missoes: int = LIMITE_MISSOES_POR_TERRENO) -> None:
        self.nome = nome
        self.limite_missoes = limite_missoes
        self.missoes_completas = 0

    @property
    def tem_missao_disponivel(self) -> bool:
        return self.missoes_completas < self.limite_missoes

    def registrar_missao(self) -> None:
        self.missoes_completas += 1

    def __str__(self) -> str:
        return self.nome
