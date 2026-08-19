"""Camada de entrada e saída (console).

Nenhum outro módulo deve chamar print() ou input() diretamente.
Além de centralizar a validação, este módulo controla o RITMO da
narração: as pausas que separam uma ação da outra.
"""

import time
from typing import Optional

from rpg import config

LARGURA = 52


# ----------------------------------------------------------------- saída
def exibir(mensagem: str = "") -> None:
    print(mensagem)


def narrar(mensagem: str, pausa: Optional[float] = None) -> None:
    """Escreve uma linha e respira antes da próxima ação."""
    print(mensagem)
    aguardar(config.PAUSA_MEDIA if pausa is None else pausa)


def titulo(texto: str) -> None:
    print(f"\n{'=' * LARGURA}")
    print(texto.center(LARGURA))
    print("=" * LARGURA)
    aguardar(config.PAUSA_MEDIA)


def separador() -> None:
    print("-" * LARGURA)


def barra(atual: int, maximo: int, largura: int = 20) -> str:
    """Barra de progresso textual: [############--------] 30/50"""
    maximo = max(maximo, 1)
    cheio = round(largura * max(atual, 0) / maximo)
    return f"[{'#' * cheio}{'.' * (largura - cheio)}] {atual}/{maximo}"


# ----------------------------------------------------------------- ritmo
def aguardar(segundos: float = None) -> None:
    """Pausa cronometrada — o jogador acompanha o que aconteceu."""
    if not config.PAUSAS_ATIVAS:
        return
    time.sleep((config.PAUSA_MEDIA if segundos is None else segundos) * config.RITMO)


def pausa(mensagem: str = "Pressione ENTER para continuar...") -> None:
    """Pausa controlada pelo jogador — marca o fim de uma cena."""
    if not config.PAUSAS_ATIVAS:
        return
    input(f"\n{mensagem}")


# ---------------------------------------------------------------- entrada
def ler_texto(mensagem: str) -> str:
    while True:
        resposta = input(mensagem).strip()
        if resposta:
            return resposta
        exibir("Digite um valor válido.")


def ler_inteiro(mensagem: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> int:
    """Lê um inteiro dentro de um intervalo, repetindo até ser válido."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            exibir("Entrada inválida. Digite apenas o número da opção.")
            continue

        if minimo is not None and valor < minimo:
            exibir(f"O valor mínimo é {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            exibir(f"O valor máximo é {maximo}.")
            continue
        return valor


def menu(titulo_menu: str, itens: list) -> int:
    """Menu numerado — ÚNICA forma de escolha do jogo.

    Devolve o índice escolhido em base 1.
    """
    exibir(f"\n{titulo_menu}")
    for indice, item in enumerate(itens, start=1):
        exibir(f"  [{indice}] {item}")
    return ler_inteiro("\n> ", minimo=1, maximo=len(itens))


def confirmar(pergunta: str, sim: str = "Sim", nao: str = "Não") -> bool:
    """Confirmação também por número, para não misturar teclado e texto."""
    return menu(pergunta, [sim, nao]) == 1
