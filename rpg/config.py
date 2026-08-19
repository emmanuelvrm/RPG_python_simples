"""Parâmetros de balanceamento do jogo.

Centralizar as constantes aqui permite ajustar a dificuldade sem
tocar nas regras de negócio nem na interface.
"""

# --- Personagem ---
HP_INICIAL = 50
PONTOS_DE_ATRIBUTO = 20

# --- Progressão (XP e nível) ---
XP_PARA_SUBIR = 40             # XP exigido = XP_PARA_SUBIR * nível atual
GANHO_POR_NIVEL = {"hp": 12, "ataque": 3, "defesa": 2}
CURA_TOTAL_AO_SUBIR = True     # subir de nível restaura todo o HP
XP_POR_MONSTRO = 18            # multiplicado pelo arquétipo do inimigo
XP_POR_MISSAO = 12

# --- Desafio: inimigos escalam junto com o herói ---
# O balanceamento é expresso em TURNOS, não em números soltos. O inimigo
# médio precisa de mais turnos para derrubar o herói do que o contrário —
# é daí que sai a vantagem, mesmo o inimigo batendo mais forte.
TURNOS_PARA_VENCER = 6         # turnos que o herói leva para derrubar o inimigo médio
TURNOS_PARA_PERDER = 5         # turnos que o inimigo leva para derrubar o herói
EFICIENCIA_ATAQUE_HEROI = 0.60 # fração do ataque do herói que atravessa a defesa inimiga
TETO_DEFESA_INIMIGO = 0.85     # o inimigo nunca anula mais que isso do ataque do herói
DANO_MINIMO = 1                # nenhum golpe é totalmente anulado

# --- Vantagens do herói (é o que eleva a taxa de vitória) ---
HEROI_ATACA_PRIMEIRO = True
CHANCE_CRITICO = 0.22
BONUS_CRITICO = 0.75           # fração do ataque somada ao dano crítico
REDUCAO_AO_DEFENDER = 0.60     # fração do dano absorvida ao defender
CHANCE_MONSTRO_DEFENDER = 0.28 # turnos em que o inimigo desperdiça a vez
CHANCE_DE_FUGA = 0.50

# --- Exploração ---
CHANCE_DE_ENCONTRO = 0.55
CHANCE_SUCESSO_MISSAO = 0.70
OURO_POR_MISSAO = (10, 25)
LIMITE_MISSOES_POR_TERRENO = 15
MISSOES_PARA_CHEFE = 5         # a cada N missões concluídas, aparece um chefe

# --- Derrota ---
# Com morte permanente e ~20% de derrota por combate, uma jornada dura cerca
# de 5 lutas: o herói nunca sairia do nível 1 e o sistema de XP seria inútil.
# Perder uma batalha custa caro, mas não encerra a aventura de imediato.
VIDAS_INICIAIS = 3
PERDA_DE_OURO_NA_DERROTA = 50  # % do ouro perdido ao ser resgatado

# --- Cidade ---
# Sem um jeito de recuperar HP entre as lutas, o dano acumulado mata o herói
# em poucas batalhas mesmo com alta taxa de vitória por combate.
CUSTO_DESCANSO_POR_NIVEL = 6   # custo da estalagem = valor * nível do herói
CURA_DO_DESCANSO = 100         # % do HP máximo recuperado ao descansar

# --- Recompensa extra por derrotar o chefe ---
BONUS_CHEFE = {"hp": 20, "ataque": 5, "defesa": 5}

# --- Ritmo da narração ---
PAUSAS_ATIVAS = True           # False acelera tudo (útil para testes)
RITMO = 1.0                    # multiplicador global das pausas
PAUSA_CURTA = 0.5
PAUSA_MEDIA = 0.9
PAUSA_LONGA = 1.4
