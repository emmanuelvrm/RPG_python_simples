"""Criação e distribuição de atributos do personagem."""

from rpg import config
from rpg.models.personagem import Personagem
from rpg.ui import console


def criar_personagem() -> Personagem:
    console.titulo("CRIAÇÃO DE PERSONAGEM")
    jogador = Personagem(console.ler_texto("Digite o nome do seu herói: "))
    distribuir_atributos(jogador)
    return jogador


def distribuir_atributos(jogador: Personagem, pontos: int = None) -> None:
    """Distribui os pontos iniciais entre Ataque e Defesa."""
    pontos = config.PONTOS_DE_ATRIBUTO if pontos is None else pontos

    console.narrar(
        "\nAtaque define o dano que você causa; Defesa reduz o dano que recebe.\n"
        "Um herói equilibrado costuma sobreviver mais no começo."
    )

    while pontos > 0:
        console.exibir(f"\nPontos restantes: {pontos}")
        ataque = console.ler_inteiro("Pontos em Ataque: ", minimo=0, maximo=pontos)
        defesa = console.ler_inteiro("Pontos em Defesa: ", minimo=0, maximo=pontos - ataque)

        jogador.ataque += ataque
        jogador.defesa += defesa
        pontos -= ataque + defesa

    console.narrar(
        f"\n{jogador.nome} está pronto! Ataque {jogador.ataque} | Defesa {jogador.defesa}",
        config.PAUSA_LONGA,
    )
    console.pausa("Pressione ENTER para começar a aventura...")
