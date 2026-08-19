# RPG Simples — v3

Jogo de RPG por turnos em Python, organizado em camadas com responsabilidades
separadas. Toda navegação é feita **por número**, o ritmo é pausado entre as
ações e o herói evolui por **XP e níveis**.

## Como executar

```bash
cd rpg_projeto
python main.py
```

Para conferir o balanceamento sem jogar:

```bash
python ferramentas/balanceamento.py
```

## Estrutura

```
rpg_projeto/
├── main.py                    # ponto de entrada
├── ferramentas/
│   └── balanceamento.py       # simulador: mede taxa de vitória e duração da jornada
└── rpg/
    ├── config.py              # TODAS as constantes de balanceamento e ritmo
    ├── jogo.py                # menu principal e tratamento de derrota
    ├── models/                # DOMÍNIO: estado + comportamento próprio
    │   ├── personagem.py      # HP, XP, nível, vidas, inventário
    │   ├── monstro.py
    │   ├── item.py
    │   └── terreno.py
    ├── data/                  # CONTEÚDO: catálogos editáveis
    │   ├── bestiario.py       # arquétipos e escalonamento dos inimigos
    │   ├── itens.py
    │   └── missoes.py
    ├── core/                  # REGRAS: o que acontece e quando
    │   ├── criacao.py
    │   ├── combate.py
    │   ├── loja.py            # loja + estalagem
    │   └── exploracao.py
    └── ui/
        └── console.py         # ÚNICO lugar com print(), input() e as pausas
```

## O que mudou nesta versão

### 1. Navegação só por número

Não existe mais nenhum ponto onde o jogador digita palavras (`"atacar"`,
`"sim"`). Tudo passa por `console.menu()`, que numera as opções, valida a
faixa e repete a pergunta em caso de erro:

```
O que você faz?
  [1] Atacar
  [2] Defender (reduz o dano recebido)
  [3] Usar poção (2 disponíveis)
  [4] Fugir (50% de chance)
```

O menu de combate é montado dinamicamente: a opção de poção só aparece quando
há poção no inventário.

### 2. Pausas entre as ações

`rpg/ui/console.py` passou a controlar o ritmo:

- `narrar(texto)` — escreve e faz uma pausa cronometrada
- `aguardar(segundos)` — pausa sem texto
- `pausa()` — espera o ENTER do jogador, marcando o fim de uma cena

Cada golpe do combate, cada etapa de missão e cada resultado aparece separado
do próximo. Para acelerar (aula, teste, depuração), basta
`PAUSAS_ATIVAS = False` ou ajustar `RITMO` em `config.py`.

### 3. Sistema de XP e níveis

- XP para subir = `XP_PARA_SUBIR * nível atual` (40, 80, 120, ...)
- Cada nível concede +12 HP máximo, +3 Ataque, +2 Defesa e cura total
- Monstros e missões dão XP; o chefe dá 4x
- Barras visuais de HP e XP no status

### 4. Balanceamento calibrado por simulação

Os inimigos **não têm mais atributos fixos**: são construídos a partir dos
atributos atuais do herói, em função de quantos turnos a luta deve durar.

```python
TURNOS_PARA_VENCER = 6   # o herói derruba o inimigo médio em ~6 golpes
TURNOS_PARA_PERDER = 5   # o inimigo derruba o herói em ~5 golpes
```

O inimigo bate **mais forte** que o herói (ataque quase sempre superior, bem
visível na tela), mas tem menos defesa e menos HP. A vantagem do herói vem de
outro lugar: ataca primeiro, acerta crítico em 22% dos golpes, o inimigo perde
28% dos turnos se defendendo, e há poções e fuga.

Números medidos com 3.000 partidas por célula (`ferramentas/balanceamento.py`):

| build inicial | nv 1 | nv 3 | nv 6 | nv 10 | nv 15 |
|---|---|---|---|---|---|
| equilibrado (12/8) | 78,7% | 81,0% | 81,5% | 80,4% | 80,2% |
| ofensivo (18/2) | 80,9% | 78,7% | 81,7% | 81,1% | 79,2% |
| defensivo (4/16) | 79,3% | 78,6% | 79,2% | 82,3% | 82,5% |
| espalhado (10/10) | 78,3% | 82,1% | 79,6% | 81,1% | 81,3% |

A taxa fica estável em ~80% para qualquer build e qualquer nível — nenhuma
distribuição de pontos vira armadilha nem atalho.

**Chefe** (nível 5, build 12/8): 39% sem poção, 76% com uma, 96% com duas.
Comprar poções antes de enfrentá-lo é a decisão relevante do jogo.

**Combate**: 5,2 turnos em média, constante em todos os níveis.

### 5. Duas correções que só a simulação revelou

**a) Builds defensivas eram invencíveis.** O ataque do inimigo escalava a
partir do *ataque* do herói. Quem investia tudo em Defesa recebia sempre o dano
mínimo e vencia 100% das lutas. Agora o ataque inimigo é calculado a partir da
defesa e do HP do herói.

**b) Sem cura entre combates, o XP era inútil.** Com morte permanente e ~20% de
derrota por luta, a jornada durava ~5 combates por pura matemática — ninguém
saía do nível 1. Duas mudanças resolveram:

- **Estalagem** na cidade: troca ouro por HP (`6 * nível` de diária)
- **Vidas**: 3 derrotas até o fim de jogo; ao perder, o herói é resgatado e
  perde metade do ouro

Resultado: **23,7 combates vencidos** e **nível 4,3** em média por jornada,
contra 3 combates e nível 1,3 antes.

### 6. Poção percentual

Curava 50 HP fixos — cura total no nível 1, irrelevante no nível 15. Agora
recupera **40% do HP máximo**, útil em qualquer ponto da progressão.
Poções vão para o inventário e são usadas **durante o combate**, não na compra.

## Ajustando a dificuldade

Tudo está em `rpg/config.py`. Depois de mexer, rode
`python ferramentas/balanceamento.py` para ver o efeito antes de jogar.

| Quero... | Mexa em |
|---|---|
| Lutas mais longas | `TURNOS_PARA_VENCER` |
| Inimigos mais letais | `TURNOS_PARA_PERDER` (menor = mais letal) |
| Jogo mais fácil | `CHANCE_CRITICO`, `REDUCAO_AO_DEFENDER`, `VIDAS_INICIAIS` |
| Jornadas mais longas | `CUSTO_DESCANSO_POR_NIVEL` (menor = mais longa) |
| Progressão mais rápida | `XP_PARA_SUBIR` (menor = mais rápida) |
| Narração mais rápida | `RITMO`, ou `PAUSAS_ATIVAS = False` |
