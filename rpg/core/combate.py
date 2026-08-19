"""Regras de combate por turnos.

Toda escolha é feita por número. Cada evento do turno é narrado com uma
pausa, para o jogador conseguir acompanhar a sequência.
"""

import random
from enum import Enum
from typing import Optional

from rpg import config
from rpg.models.monstro import Monstro
from rpg.models.personagem import Personagem
from rpg.ui import console

ATACAR, DEFENDER, POCAO, FUGIR = "atacar", "defender", "pocao", "fugir"


class Resultado(Enum):
    """Como a batalha terminou — o chamador decide o próximo passo."""

    VITORIA = "vitoria"
    DERROTA = "derrota"
    FUGA = "fuga"


def calcular_dano(atacante, defensor, critico: bool = False, defendendo: bool = False) -> int:
    """Dano final: inteiro e nunca menor que DANO_MINIMO."""
    dano = atacante.ataque - defensor.defesa
    if critico:
        dano += config.BONUS_CRITICO * atacante.ataque
    if defendendo:
        dano *= 1 - config.REDUCAO_AO_DEFENDER
    return max(int(dano), config.DANO_MINIMO)


def _montar_opcoes(jogador: Personagem) -> tuple[list[str], list[str]]:
    """Monta o menu do turno conforme o que o jogador tem disponível."""
    rotulos = ["Atacar", "Defender (reduz o dano recebido)"]
    acoes = [ATACAR, DEFENDER]

    pocoes = len(jogador.consumiveis())
    if pocoes:
        rotulos.append(f"Usar poção ({pocoes} disponível{'is' if pocoes > 1 else ''})")
        acoes.append(POCAO)

    rotulos.append(f"Fugir ({int(config.CHANCE_DE_FUGA * 100)}% de chance)")
    acoes.append(FUGIR)
    return rotulos, acoes


def batalhar(jogador: Personagem, monstro: Monstro) -> Resultado:
    """Executa a batalha até a morte de um dos lados ou a fuga do jogador."""
    console.titulo(f"Um {monstro.nome} apareceu!")

    while jogador.vivo and monstro.vivo:
        console.separador()
        console.exibir(jogador.status())
        console.exibir(f"\n{monstro.status()}")

        rotulos, acoes = _montar_opcoes(jogador)
        acao = acoes[console.menu("O que você faz?", rotulos) - 1]

        if acao == FUGIR:
            resultado = _tentar_fugir()
            if resultado is Resultado.FUGA:
                return resultado
            acao = ATACAR

        if acao == POCAO:
            _usar_pocao(jogador)

        acao_monstro = (
            DEFENDER if random.random() < config.CHANCE_MONSTRO_DEFENDER else ATACAR
        )

        if config.HEROI_ATACA_PRIMEIRO:
            _turno_do_heroi(jogador, monstro, acao, acao_monstro)
            if not monstro.vivo:
                break
            _turno_do_monstro(jogador, monstro, acao, acao_monstro)
        else:
            _turno_do_monstro(jogador, monstro, acao, acao_monstro)
            if not jogador.vivo:
                break
            _turno_do_heroi(jogador, monstro, acao, acao_monstro)

    return _encerrar(jogador, monstro)


# ------------------------------------------------------------------ turnos
def _turno_do_heroi(jogador, monstro, acao, acao_monstro) -> None:
    if acao != ATACAR:
        return
    critico = random.random() < config.CHANCE_CRITICO
    dano = calcular_dano(jogador, monstro, critico, acao_monstro == DEFENDER)
    monstro.receber_dano(dano)

    if critico:
        console.narrar(f"\n  >> ACERTO CRÍTICO! {dano} de dano no {monstro.nome}.", config.PAUSA_LONGA)
    elif acao_monstro == DEFENDER:
        console.narrar(f"\n  >> O {monstro.nome} se defendeu; você causou apenas {dano} de dano.")
    else:
        console.narrar(f"\n  >> Você causou {dano} de dano ao {monstro.nome}.")


def _turno_do_monstro(jogador, monstro, acao, acao_monstro) -> None:
    if acao_monstro != ATACAR:
        if acao == DEFENDER:
            console.narrar("  >> Ambos se protegeram. O turno passa em silêncio.")
        else:
            console.narrar(f"  >> O {monstro.nome} recuou e não atacou neste turno.")
        return

    dano = calcular_dano(monstro, jogador, defendendo=(acao == DEFENDER))
    jogador.receber_dano(dano)

    if acao == DEFENDER:
        console.narrar(f"  >> O {monstro.nome} atacou, mas sua guarda segurou: {dano} de dano.")
    else:
        console.narrar(f"  >> O {monstro.nome} te atingiu: {dano} de dano.")


# ------------------------------------------------------------------ ações
def _tentar_fugir() -> Optional[Resultado]:
    console.narrar("\n  >> Você tenta escapar...", config.PAUSA_LONGA)
    if random.random() < config.CHANCE_DE_FUGA:
        console.narrar("  >> Conseguiu! Você deixa a luta para trás.")
        console.pausa()
        return Resultado.FUGA
    console.narrar("  >> A fuga falhou! Sem saída, você parte para o ataque.")
    return None


def _usar_pocao(jogador: Personagem) -> None:
    usado = jogador.usar_consumivel()
    if usado is None:
        return
    item, recuperado = usado
    console.narrar(f"\n  >> Você bebe a {item.nome} e recupera {recuperado} de HP.", config.PAUSA_LONGA)


# --------------------------------------------------------------- desfecho
def _encerrar(jogador: Personagem, monstro: Monstro) -> Resultado:
    if not monstro.vivo:
        console.narrar(f"\n  >> O {monstro.nome} cai derrotado!", config.PAUSA_LONGA)
        jogador.ganhar_ouro(monstro.ouro)
        console.narrar(f"  >> Recompensa: {monstro.ouro} de ouro e {monstro.xp} de XP.")
        anunciar_xp(jogador, monstro.xp)
        console.pausa()
        return Resultado.VITORIA

    console.narrar("\n  >> Você foi derrotado!", config.PAUSA_LONGA)
    return Resultado.DERROTA


def anunciar_xp(jogador: Personagem, xp: int) -> None:
    """Concede XP e narra cada subida de nível."""
    for nivel in jogador.ganhar_xp(xp):
        console.titulo(f"NÍVEL {nivel} ALCANÇADO!")
        ganho = config.GANHO_POR_NIVEL
        console.narrar(
            f"  +{ganho['hp']} HP máximo | +{ganho['ataque']} Ataque | +{ganho['defesa']} Defesa",
            config.PAUSA_LONGA,
        )
        if config.CURA_TOTAL_AO_SUBIR:
            console.narrar("  Suas forças se renovam por completo.")
