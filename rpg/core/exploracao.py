"""Exploração dos terrenos: encontros aleatórios e missões."""

import random

from rpg import config
from rpg.core.combate import Resultado, anunciar_xp, batalhar
from rpg.data import bestiario
from rpg.data.missoes import MISSOES
from rpg.models.personagem import Personagem
from rpg.models.terreno import Terreno
from rpg.ui import console


def explorar(jogador: Personagem, terreno: Terreno) -> None:
    """Um turno de exploração: possível batalha seguida de missão."""
    console.titulo(terreno.nome.upper())

    if random.random() < config.CHANCE_DE_ENCONTRO:
        console.narrar("Passos se aproximam entre as sombras...", config.PAUSA_LONGA)
        if batalhar(jogador, bestiario.sortear_monstro(jogador)) is Resultado.DERROTA:
            return
    else:
        console.narrar("O caminho segue tranquilo por enquanto.", config.PAUSA_LONGA)

    if jogador.vivo:
        oferecer_missao(jogador, terreno)


def oferecer_missao(jogador: Personagem, terreno: Terreno) -> None:
    if not terreno.tem_missao_disponivel:
        console.narrar(f"\nVocê já completou todas as missões de {terreno.nome}.")
        console.pausa()
        return

    console.separador()
    console.narrar(f"\n{random.choice(MISSOES)}", config.PAUSA_LONGA)

    if not console.confirmar("Aceitar a missão?", sim="Aceitar", nao="Recusar"):
        console.narrar("\nVocê agradece e segue seu caminho.")
        console.pausa()
        return

    console.narrar("\nVocê parte para cumprir a tarefa...", config.PAUSA_LONGA)
    console.narrar("As horas passam.", config.PAUSA_LONGA)

    if random.random() > config.CHANCE_SUCESSO_MISSAO:
        console.narrar("\n  >> A missão fracassou. Talvez em outra ocasião.", config.PAUSA_LONGA)
        console.pausa()
        return

    terreno.registrar_missao()
    ouro = random.randint(*config.OURO_POR_MISSAO)
    jogador.ganhar_ouro(ouro)

    console.narrar("\n  >> Missão concluída com sucesso!", config.PAUSA_LONGA)
    console.narrar(f"  >> Recompensa: {ouro} de ouro e {config.XP_POR_MISSAO} de XP.")
    anunciar_xp(jogador, config.XP_POR_MISSAO)
    console.pausa()

    if terreno.missoes_completas % config.MISSOES_PARA_CHEFE == 0:
        enfrentar_chefe(jogador)


def enfrentar_chefe(jogador: Personagem) -> None:
    console.narrar("\nO chão treme. Algo muito maior se aproxima...", config.PAUSA_LONGA)
    if batalhar(jogador, bestiario.criar_chefe(jogador)) is Resultado.VITORIA:
        jogador.evoluir(**config.BONUS_CHEFE)
        console.titulo("RECOMPENSA LENDÁRIA")
        bonus = config.BONUS_CHEFE
        console.narrar(
            f"  +{bonus['hp']} HP máximo | +{bonus['ataque']} Ataque | +{bonus['defesa']} Defesa",
            config.PAUSA_LONGA,
        )
        console.pausa()
