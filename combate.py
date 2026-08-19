"""Regras de combate por turnos."""

import random
from enum import Enum

from rpg.config import (
    BONUS_CRITICO,
    CHANCE_CRITICO,
    CHANCE_DE_FUGA,
    REDUCAO_AO_DEFENDER,
)
from rpg.models.monstro import Monstro
from rpg.models.personagem import Personagem
from rpg.ui import console

ACOES = ("atacar", "defender", "fugir")


class Resultado(Enum):
    """Como a batalha terminou — permite ao chamador decidir o próximo passo."""

    VITORIA = "vitoria"
    DERROTA = "derrota"
    FUGA = "fuga"


def calcular_dano(atacante, defensor, critico: bool = False, defendendo: bool = False) -> int:
    """Dano final, nunca negativo e sempre inteiro."""
    dano = atacante.ataque - defensor.defesa
    if critico:
        dano += BONUS_CRITICO * atacante.ataque
    if defendendo:
        dano *= 1 - REDUCAO_AO_DEFENDER
    return max(int(dano), 0)


def batalhar(jogador: Personagem, monstro: Monstro) -> Resultado:
    """Executa a batalha até a morte de um dos lados ou a fuga do jogador."""
    console.titulo(f"Um {monstro.nome} apareceu!")

    while jogador.vivo and monstro.vivo:
        console.exibir(f"\n{jogador.status()}")
        console.exibir(monstro.status())

        acao = console.ler_opcao("Atacar, Defender ou Fugir? ", ACOES)

        if acao == "fugir":
            if random.random() < CHANCE_DE_FUGA:
                console.exibir("\nVocê conseguiu fugir!")
                return Resultado.FUGA
            console.exibir("\nA fuga falhou! Você parte para o ataque.")
            acao = "atacar"

        acao_monstro = random.choice(("atacar", "defender"))

        if acao == "atacar":
            critico = random.random() < CHANCE_CRITICO
            dano = calcular_dano(jogador, monstro, critico, acao_monstro == "defender")
            monstro.receber_dano(dano)
            sufixo = " (acerto crítico!)" if critico else ""
            console.exibir(f"Você causou {dano} de dano ao {monstro.nome}.{sufixo}")

        if not monstro.vivo:
            break

        if acao_monstro == "atacar":
            dano = calcular_dano(monstro, jogador, defendendo=(acao == "defender"))
            jogador.receber_dano(dano)
            defesa = ", mas você se defendeu e recebeu apenas" if acao == "defender" else " e causou"
            console.exibir(f"{monstro.nome} te atacou{defesa} {dano} de dano.")
        elif acao == "defender":
            console.exibir("Ambos escolheram se defender. Nada aconteceu!")

    return _encerrar(jogador, monstro)


def _encerrar(jogador: Personagem, monstro: Monstro) -> Resultado:
    if not monstro.vivo:
        console.exibir(f"\nVocê derrotou o {monstro.nome}!")
        jogador.ganhar_ouro(monstro.ouro)
        console.exibir(f"Você ganhou {monstro.ouro} moedas de ouro!")
        return Resultado.VITORIA

    console.exibir("\nVocê foi derrotado!")
    return Resultado.DERROTA
