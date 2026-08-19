"""Ferramenta de balanceamento: mede a taxa de vitória sem abrir o jogo.

Uso (a partir da raiz do projeto):
    python ferramentas/balanceamento.py

Serve para conferir o efeito de qualquer mudança em rpg/config.py ou nos
arquétipos de rpg/data/bestiario.py antes de jogar.
"""

import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg import config

config.PAUSAS_ATIVAS = False

from rpg.core.combate import calcular_dano
from rpg.data import bestiario
from rpg.data.itens import CATALOGO
from rpg.models.personagem import Personagem

BUILDS = {
    "equilibrado (12/8)": (12, 8),
    "ofensivo (18/2)": (18, 2),
    "defensivo (4/16)": (4, 16),
    "espalhado (10/10)": (10, 10),
}


def heroi(nivel: int, ataque: int, defesa: int, pocoes: int = 0) -> Personagem:
    """Reconstrói um herói plausível no nível pedido."""
    p = Personagem("Simulacro")
    p.ataque, p.defesa = ataque, defesa
    for _ in range(nivel - 1):
        p.ganhar_xp(p.xp_para_subir)
    for _ in range(pocoes):
        p.adquirir(CATALOGO[0])
    p.hp = p.hp_maximo
    return p


def combate_automatico(jogador, monstro, usa_pocao: bool = False, pode_fugir: bool = False):
    """Reproduz batalhar() sem interface.

    Devolve (resultado, turnos), onde resultado é vitoria / derrota / fuga.
    """
    turnos = 0
    while jogador.vivo and monstro.vivo and turnos < 200:
        turnos += 1
        acao = "atacar"

        if usa_pocao and jogador.hp < jogador.hp_maximo * 0.45 and jogador.consumiveis():
            jogador.usar_consumivel()
            acao = "pocao"
        elif pode_fugir and jogador.hp < jogador.hp_maximo * 0.30:
            if random.random() < config.CHANCE_DE_FUGA:
                return "fuga", turnos

        acao_monstro = "defender" if random.random() < config.CHANCE_MONSTRO_DEFENDER else "atacar"

        if acao == "atacar":
            critico = random.random() < config.CHANCE_CRITICO
            monstro.receber_dano(calcular_dano(jogador, monstro, critico, acao_monstro == "defender"))
        if not monstro.vivo:
            break
        if acao_monstro == "atacar":
            jogador.receber_dano(calcular_dano(monstro, jogador))

    return ("vitoria" if not monstro.vivo else "derrota"), turnos


def medir(nivel, build, pocoes=0, amostras=3000):
    vitorias, turnos = 0, []
    for _ in range(amostras):
        j = heroi(nivel, *build, pocoes=pocoes)
        resultado, t = combate_automatico(j, bestiario.sortear_monstro(j), usa_pocao=bool(pocoes))
        vitorias += resultado == "vitoria"
        turnos.append(t)
    return 100 * vitorias / amostras, statistics.mean(turnos)


def simular_jornada(max_combates=60):
    """Jornada completa: luta, descansa quando ferido, estoca poções.

    Reproduz as recompensas que _encerrar() concede no jogo real:
    ouro e XP do monstro derrotado.
    """
    from rpg.core.loja import custo_do_descanso

    j = heroi(1, 12, 8)
    vitorias = 0

    for _ in range(max_combates):
        if j.hp < j.hp_maximo * 0.55 and j.ouro >= custo_do_descanso(j):
            j.ouro -= custo_do_descanso(j)
            j.hp = j.hp_maximo
        if j.ouro >= CATALOGO[0].custo + custo_do_descanso(j) and len(j.consumiveis()) < 2:
            j.ouro -= CATALOGO[0].custo
            j.adquirir(CATALOGO[0])

        monstro = bestiario.sortear_monstro(j)
        resultado, _ = combate_automatico(j, monstro, usa_pocao=True, pode_fugir=True)
        if resultado == "derrota":
            resgatado, _ = j.ser_resgatado()
            if not resgatado:
                return j.nivel, vitorias, "morreu"
            continue
        if resultado == "fuga":
            continue

        vitorias += 1
        j.ganhar_ouro(monstro.ouro)   # recompensas concedidas por _encerrar()
        j.ganhar_xp(monstro.xp)

    return j.nivel, vitorias, "sobreviveu"


def main() -> None:
    random.seed(4242)

    print("MONSTROS COMUNS — taxa de vitória (sem poções)")
    print(f"{'build':<20}" + "".join(f"{'nv ' + str(n):>8}" for n in (1, 3, 6, 10, 15)))
    print("-" * 60)
    for nome, build in BUILDS.items():
        print(f"{nome:<20}" + "".join(f"{medir(n, build)[0]:>7.1f}%" for n in (1, 3, 6, 10, 15)))

    print("\nCHEFE — vitória por quantidade de poções (nível 5, build 12/8)")
    for pocoes in (0, 1, 2, 3):
        vit = sum(
            combate_automatico(j := heroi(5, 12, 8, pocoes), bestiario.criar_chefe(j), True)[0] == "vitoria"
            for _ in range(3000)
        )
        print(f"  {pocoes} poção(ões): {100 * vit / 3000:>5.1f}%")

    print("\nJORNADA COMPLETA (com estalagem e poções, 3000 partidas)")
    niveis, vitorias, sobreviveu = [], [], 0
    for _ in range(3000):
        nv, vt, motivo = simular_jornada()
        niveis.append(nv)
        vitorias.append(vt)
        sobreviveu += motivo == "sobreviveu"
    print(f"  nível médio alcançado: {statistics.mean(niveis):.1f} (máximo {max(niveis)})")
    print(f"  combates vencidos:     {statistics.mean(vitorias):.1f} em média")
    print(f"  chegou a 60 combates:  {100 * sobreviveu / 3000:.1f}%")

    print("\nDURAÇÃO MÉDIA DO COMBATE")
    for nivel in (1, 5, 10, 15):
        print(f"  nível {nivel:>2}: {medir(nivel, (12, 8))[1]:.1f} turnos")


if __name__ == "__main__":
    main()
