"""Arquétipos de inimigos e geração escalada pelo nível do herói.

Em vez de valores fixos, cada inimigo é construído a partir dos atributos
atuais do jogador. Assim um Lobo continua sendo um Lobo no nível 1 e no
nível 12 — sempre um pouco acima do herói, nunca impossível.
"""

import random
from dataclasses import dataclass

from rpg import config
from rpg.models.monstro import Monstro


@dataclass(frozen=True)
class Arquetipo:
    """Multiplicadores aplicados sobre os atributos do herói."""

    nome: str
    mult_hp: float
    mult_ataque: float
    mult_defesa: float
    mult_recompensa: float
    peso: int = 10  # frequência relativa no sorteio


ARQUETIPOS: tuple[Arquetipo, ...] = (
    #          nome              hp    atk   def   recomp  peso
    Arquetipo("Lobo",           0.70, 0.95, 0.70, 0.80, peso=16),
    Arquetipo("Goblin",         0.80, 0.90, 0.80, 0.85, peso=16),
    Arquetipo("Orc",            1.05, 1.05, 1.00, 1.10, peso=12),
    Arquetipo("Troll",          1.40, 1.00, 0.80, 1.25, peso=9),
    Arquetipo("Mago sombrio",   0.70, 1.30, 0.55, 1.25, peso=8),
    Arquetipo("Elfo negro",     1.00, 1.15, 1.15, 1.45, peso=6),
    Arquetipo("Dragão",         1.55, 1.20, 1.15, 2.00, peso=3),
)

# Calibrado por simulação: ~41% de vitória de mãos vazias, ~78% com uma
# poção e ~96% com duas. Comprar poções antes do chefe é a decisão relevante.
CHEFE = Arquetipo("Dragão brilhante", 1.41, 0.95, 1.10, 4.00)

OURO_POR_MONSTRO = 18


def _construir(arquetipo: Arquetipo, jogador) -> Monstro:
    """Dimensiona o inimigo em função de quantos turnos a luta deve durar.

    - defesa: deixa passar EFICIENCIA_ATAQUE_HEROI do ataque do herói
    - hp:     o suficiente para sobreviver TURNOS_PARA_VENCER golpes
    - ataque: forte o bastante para derrubar o herói em TURNOS_PARA_PERDER
              golpes — por isso costuma superar o ataque do próprio herói
    """
    dano_do_heroi = max(1.0, jogador.ataque * config.EFICIENCIA_ATAQUE_HEROI)

    defesa_bruta = jogador.ataque * (1 - config.EFICIENCIA_ATAQUE_HEROI) * arquetipo.mult_defesa
    defesa = max(0, round(min(defesa_bruta, jogador.ataque * config.TETO_DEFESA_INIMIGO)))

    hp = max(10, round(dano_do_heroi * config.TURNOS_PARA_VENCER * arquetipo.mult_hp))

    dano_no_heroi = jogador.hp_maximo / config.TURNOS_PARA_PERDER * arquetipo.mult_ataque
    ataque = max(2, round(jogador.defesa + dano_no_heroi))

    return Monstro(
        nome=arquetipo.nome,
        hp=hp,
        ataque=ataque,
        defesa=defesa,
        ouro=round(OURO_POR_MONSTRO * arquetipo.mult_recompensa * (1 + 0.40 * (jogador.nivel - 1))),
        xp=round(config.XP_POR_MONSTRO * arquetipo.mult_recompensa),
    )


def sortear_monstro(jogador) -> Monstro:
    """Devolve sempre uma instância nova, dimensionada para o herói."""
    arquetipo = random.choices(ARQUETIPOS, weights=[a.peso for a in ARQUETIPOS])[0]
    return _construir(arquetipo, jogador)


def criar_chefe(jogador) -> Monstro:
    return _construir(CHEFE, jogador)
