"""Orquestra o fluxo principal do jogo (menu de navegação numérico)."""

from rpg import config
from rpg.core.criacao import criar_personagem
from rpg.core.exploracao import explorar
from rpg.core.loja import visitar_cidade
from rpg.models.personagem import Personagem
from rpg.models.terreno import Terreno
from rpg.ui import console


def montar_mapa() -> list[Terreno]:
    """Terrenos exploráveis. Adicione novos locais aqui."""
    return [Terreno("Floresta"), Terreno("Montanha"), Terreno("Caverna")]


def iniciar_jogo() -> None:
    console.titulo("RPG SIMPLES")
    jogador = criar_personagem()
    terrenos = montar_mapa()

    opcoes = [f"Explorar {t.nome}" for t in terrenos] + ["Ir à Cidade (loja e estalagem)", "Encerrar a aventura"]
    indice_cidade = len(terrenos) + 1
    indice_sair = len(terrenos) + 2

    while jogador.vivo:
        console.separador()
        console.exibir(jogador.status())
        escolha = console.menu("Para onde você vai?", opcoes)

        if escolha == indice_sair:
            console.narrar("\nAté a próxima aventura!")
            return
        if escolha == indice_cidade:
            visitar_cidade(jogador)
        else:
            explorar(jogador, terrenos[escolha - 1])
            if not jogador.vivo and not _resgatar(jogador):
                break

    _fim_de_jogo(jogador)


def _resgatar(jogador: Personagem) -> bool:
    """Após uma derrota, mercadores encontram o herói caído — se ainda houver vidas."""
    resgatado, perdido = jogador.ser_resgatado()
    if not resgatado:
        return False

    console.titulo("VOCÊ FOI RESGATADO")
    console.narrar(
        "Mercadores encontram você caído na estrada e o levam de volta à cidade.",
        config.PAUSA_LONGA,
    )
    console.narrar(f"  Custo do socorro: {perdido} de ouro.")
    console.narrar(f"  Vidas restantes: {jogador.vidas}")
    console.pausa()
    return True


def _fim_de_jogo(jogador: Personagem) -> None:
    console.titulo("FIM DE JOGO")
    console.narrar(
        f"{jogador.nome} caiu em batalha no nível {jogador.nivel}, "
        f"com {jogador.ouro} moedas de ouro.",
        config.PAUSA_LONGA,
    )
