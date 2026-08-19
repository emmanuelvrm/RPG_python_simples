"""Ponto de entrada do jogo.

Execute a partir da raiz do projeto:
    python main.py
"""

from rpg.jogo import iniciar_jogo

if __name__ == "__main__":
    try:
        iniciar_jogo()
    except KeyboardInterrupt:
        print("\n\nJogo encerrado pelo jogador.")
