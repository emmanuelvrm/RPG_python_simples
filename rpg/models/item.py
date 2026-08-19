"""Item comprável na loja."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Um item aplica um efeito sobre um atributo do personagem.

    atributo:   "hp", "ataque" ou "defesa".
    consumivel: se True, fica guardado no inventário para uso posterior.
    percentual: se True, `valor` é uma porcentagem do HP máximo em vez de
                um número fixo — assim a poção continua útil em qualquer nível.
    """

    nome: str
    custo: int
    atributo: str
    valor: int
    consumivel: bool = False
    percentual: bool = False

    @property
    def efeito(self) -> str:
        unidade = "% do HP máximo" if self.percentual else f" de {self.atributo}"
        return f"+{self.valor}{unidade}"

    def __str__(self) -> str:
        return f"{self.nome:<16} {self.custo:>3} ouro  ({self.efeito})"
