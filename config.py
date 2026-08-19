"""Parâmetros de balanceamento do jogo.

Centralizar as constantes aqui permite ajustar a dificuldade sem
tocar nas regras de negócio nem na interface.
"""

# --- Personagem ---
HP_INICIAL = 50
PONTOS_DE_ATRIBUTO = 20

# --- Combate ---
CHANCE_CRITICO = 0.10          # 10% de chance de acerto crítico
BONUS_CRITICO = 0.5            # fração do ataque somada ao dano crítico
REDUCAO_AO_DEFENDER = 0.5      # fração do dano absorvida ao escolher "defender"
CHANCE_DE_FUGA = 0.30          # 30% de chance de fugir com sucesso

# --- Exploração ---
CHANCE_DE_ENCONTRO = 0.50      # chance de encontrar um monstro ao entrar no terreno
CHANCE_SUCESSO_MISSAO = 0.70
OURO_POR_MISSAO = (5, 20)      # intervalo (mínimo, máximo)
LIMITE_MISSOES_POR_TERRENO = 15
MISSOES_PARA_CHEFE = 5         # a cada N missões concluídas, aparece um chefe

# --- Recompensa por derrotar o chefe ---
BONUS_CHEFE = {"hp": 20, "ataque": 5, "defesa": 5}
