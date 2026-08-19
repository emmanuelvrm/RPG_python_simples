"""Orquestra o fluxo principal do jogo (menu de navegação)."""

from rpg.core.criacao import criar_personagem
from rpg.core.exploracao import explorar
from rpg.core.loja import visitar_loja
from rpg.models.personagem import Personagem
from rpg.models.terreno import Terreno
from rpg.ui import console


def montar_mapa() -> list[Terreno]:
    """Terrenos exploráveis. Adicione novos locais aqui."""
    return [Terreno("Floresta"), Terreno("Montanha"), Terreno("Caverna")]


def iniciar_jogo() -> None:
    console.titulo("RPG Simples")
    jogador = criar_personagem()
    terrenos = montar_mapa()

    opcoes = [terreno.nome for terreno in terrenos] + ["Cidade", "Sair"]
    indice_cidade = len(terrenos) + 1
    indice_sair = len(terrenos) + 2

    while jogador.vivo:
        console.exibir(f"\n{jogador.status()}")
        escolha = console.menu("Onde você gostaria de ir?", opcoes)

        if escolha == indice_sair:
            console.exibir("\nAté a próxima aventura!")
            return
        if escolha == indice_cidade:
            visitar_loja(jogador)
        else:
            explorar(jogador, terrenos[escolha - 1])

    _fim_de_jogo(jogador)


def _fim_de_jogo(jogador: Personagem) -> None:
    console.titulo("Fim de jogo!")
    console.exibir(f"{jogador.nome} caiu em batalha com {jogador.ouro} moedas de ouro.")
