"""Cidade: loja do mercador e estalagem."""

from rpg import config
from rpg.data.itens import CATALOGO
from rpg.models.item import Item
from rpg.models.personagem import Personagem
from rpg.ui import console


def custo_do_descanso(jogador: Personagem) -> int:
    return config.CUSTO_DESCANSO_POR_NIVEL * jogador.nivel


def visitar_cidade(jogador: Personagem) -> None:
    console.titulo("CIDADE")
    console.narrar("Poções ficam no inventário e podem ser usadas durante os combates.")

    while True:
        console.separador()
        console.exibir(jogador.status())

        opcoes = [str(item) for item in CATALOGO]
        opcoes.append(f"{'Descansar':<16} {custo_do_descanso(jogador):>3} ouro  (recupera todo o HP)")
        opcoes.append("Voltar à estrada")

        escolha = console.menu("O que você gostaria de fazer?", opcoes)

        if escolha == len(opcoes):
            console.narrar("\nAté logo, aventureiro!")
            return
        if escolha == len(opcoes) - 1:
            descansar(jogador)
        else:
            comprar(jogador, CATALOGO[escolha - 1])


def descansar(jogador: Personagem) -> bool:
    """Estalagem: troca ouro por HP. É o que sustenta uma jornada longa."""
    if jogador.hp >= jogador.hp_maximo:
        console.narrar("\n  >> Você já está em plena forma.")
        return False

    custo = custo_do_descanso(jogador)
    if not jogador.gastar_ouro(custo):
        console.narrar(f"\n  >> A diária custa {custo} de ouro e você não tem o bastante.")
        return False

    recuperado = jogador.curar(round(jogador.hp_maximo * config.CURA_DO_DESCANSO / 100))
    console.narrar(f"\n  >> Você dorme até o amanhecer e recupera {recuperado} de HP.", config.PAUSA_LONGA)
    return True


def comprar(jogador: Personagem, item: Item) -> bool:
    """Cobra o item e o entrega. Devolve False se faltar ouro."""
    if not jogador.gastar_ouro(item.custo):
        console.narrar("\n  >> Ouro insuficiente para essa compra.")
        return False

    jogador.adquirir(item)
    if item.consumivel:
        console.narrar(f"\n  >> {item.nome} guardada no inventário.")
    else:
        console.narrar(f"\n  >> {item.nome} equipada! {item.efeito}.")
    return True
