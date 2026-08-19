"""Camada de entrada e saída (console).

Nenhum outro módulo deve chamar print() ou input() diretamente.
Assim é possível trocar o console por uma interface gráfica, web ou
por um mock nos testes sem alterar as regras do jogo.
"""

from typing import Iterable, Optional

LARGURA = 46


def exibir(mensagem: str = "") -> None:
    """Escreve uma mensagem para o jogador."""
    print(mensagem)


def titulo(texto: str) -> None:
    """Destaca uma mudança de cena (batalha, loja, criação...)."""
    print(f"\n{'=' * LARGURA}")
    print(texto.center(LARGURA))
    print("=" * LARGURA)


def ler_texto(mensagem: str) -> str:
    """Lê um texto não vazio."""
    while True:
        resposta = input(mensagem).strip()
        if resposta:
            return resposta
        exibir("Digite um valor válido.")


def ler_inteiro(
    mensagem: str,
    minimo: Optional[int] = None,
    maximo: Optional[int] = None,
) -> int:
    """Lê um inteiro dentro de um intervalo, repetindo até ser válido."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            exibir("Entrada inválida. Use apenas números.")
            continue

        if minimo is not None and valor < minimo:
            exibir(f"O valor mínimo é {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            exibir(f"O valor máximo é {maximo}.")
            continue
        return valor


def ler_opcao(mensagem: str, opcoes: Iterable[str]) -> str:
    """Lê uma das opções textuais aceitas (comparação sem diferenciar caixa)."""
    validas = [opcao.lower() for opcao in opcoes]
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in validas:
            return resposta
        exibir(f"Opções válidas: {', '.join(validas)}.")


def confirmar(mensagem: str) -> bool:
    """Pergunta sim/não e devolve um booleano."""
    return ler_opcao(f"{mensagem} (sim/nao) ", ("sim", "nao", "não")) == "sim"


def menu(titulo_menu: str, itens: list) -> int:
    """Exibe um menu numerado e devolve o índice escolhido (base 1)."""
    exibir(f"\n{titulo_menu}")
    for indice, item in enumerate(itens, start=1):
        exibir(f"  {indice}. {item}")
    return ler_inteiro("\nEscolha: ", minimo=1, maximo=len(itens))
