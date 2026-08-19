<div align="center">

```
██████╗ ██████╗  ██████╗     ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗███████╗
██╔══██╗██╔══██╗██╔════╝     ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝██╔════╝
██████╔╝██████╔╝██║  ███╗    ███████╗██║██╔████╔██║██████╔╝██║     █████╗  ███████╗
██╔══██╗██╔═══╝ ██║   ██║    ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝  ╚════██║
██║  ██║██║     ╚██████╔╝    ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗███████║
╚═╝  ╚═╝╚═╝      ╚═════╝     ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚══════╝
```

**Um RPG de turnos em Python — com arquitetura em camadas e balanceamento calibrado por simulação.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Dependências](https://img.shields.io/badge/dependências-nenhuma-2ea44f?style=flat-square)](#instalação)
[![Arquitetura](https://img.shields.io/badge/arquitetura-em%20camadas-8957e5?style=flat-square)](#arquitetura)
[![Balanceamento](https://img.shields.io/badge/vitória-~80%25%20medido-d8a657?style=flat-square)](#balanceamento-medido-não-chutado)
[![Licença](https://img.shields.io/badge/licença-MIT-blue?style=flat-square)](#licença)

[Instalação](#instalação) · [Como jogar](#como-jogar) · [Arquitetura](#arquitetura) · [Balanceamento](#balanceamento-medido-não-chutado) · [Personalizar](#ajustando-a-dificuldade)

</div>

---

## O que é

Um RPG de texto jogado no terminal: você cria um herói, distribui 20 pontos
entre Ataque e Defesa, explora três terrenos, aceita missões, enfrenta monstros
por turnos e sobe de nível até encarar um chefe.

Por baixo do jogo, o projeto é um **estudo de organização de código**: o mesmo
RPG que caberia em um único arquivo foi separado em camadas com fronteiras
explícitas, e o balanceamento foi definido por **simulação de diversas de
partidas** em vez de tentativa e erro.

---

## Demonstração

Saída real de uma partida — combate por turnos, barras de estado e menus numerados:

```
====================================================
                Um Goblin apareceu!
====================================================
----------------------------------------------------
Kaeltar — Nível 1
  HP  [#########...........] 23/50
  XP  [....................] 0/40
  Ataque 12 | Defesa 8 | Ouro 0 | Poções 0 | Vidas @@@

Goblin
  HP  [#####...............] 8/35
  Ataque 17 | Defesa 4

O que você faz?
  [1] Atacar
  [2] Defender (reduz o dano recebido)
  [3] Fugir (50% de chance)

> 1

  >> Você causou 8 de dano ao Goblin.

  >> O Goblin cai derrotado!
  >> Recompensa: 15 de ouro e 15 de XP.
```

Repare no `Ataque 17` do Goblin contra o `Ataque 12` do herói: **os inimigos
batem mais forte que você**. A vantagem vem de outro lugar — veja
[Balanceamento](#balanceamento-medido-não-chutado).

<details>
<summary><b>Ver missões e subida de nível</b></summary>

```
====================================================
                      FLORESTA
====================================================
O caminho segue tranquilo por enquanto.
----------------------------------------------------

Mulher desconhecida: minha filha sofre de uma doença terrível.
Por favor, encontre uma planta que possa curá-la.

Aceitar a missão?
  [1] Aceitar
  [2] Recusar

> 1

Você parte para cumprir a tarefa...
As horas passam.

  >> Missão concluída com sucesso!
  >> Recompensa: 14 de ouro e 12 de XP.

====================================================
                 NÍVEL 2 ALCANÇADO!
====================================================
  +12 HP máximo | +3 Ataque | +2 Defesa
  Suas forças se renovam por completo.
----------------------------------------------------
Kaeltar — Nível 2
  HP  [####################] 62/62
  XP  [###.................] 11/80
  Ataque 15 | Defesa 10 | Ouro 34 | Poções 0 | Vidas @@
```

</details>

---

## Recursos

| | |
|---|---|
| **Navegação 100% numérica** | Nenhum comando digitado. Todo menu valida a faixa e repete a pergunta em caso de erro. |
| **Ritmo narrado** | Pausas cronometradas entre cada golpe e cada etapa de missão. Desligáveis por configuração. |
| **XP e níveis** | Curva progressiva, ganho de atributos e cura total a cada nível. |
| **Inimigos que escalam** | Monstros construídos a partir dos seus atributos — relevantes no nível 1 e no nível 15. |
| **Poções em combate** | Compradas na loja, guardadas no inventário, usadas na hora do aperto. |
| **Estalagem e vidas** | Troque ouro por HP; três derrotas até o fim de jogo. |
| **Simulador embutido** | Meça o efeito de qualquer ajuste antes de jogar. |
| **Zero dependências** | Só a biblioteca padrão do Python. |

---

## Instalação

Requer **Python 3.10 ou superior**. Nada além disso.

```bash
git clone https://github.com/emmanuelvrm/rpg-simples.git
cd rpg-simples
python main.py
```

Sem `pip install`, sem ambiente virtual, sem arquivo de dependências.

---

## Como jogar

1. **Nomeie seu herói** e distribua 20 pontos entre Ataque e Defesa
   *(builds equilibradas, ofensivas e defensivas são todas viáveis — isso foi medido)*
2. **Explore** Floresta, Montanha ou Caverna — cada visita pode trazer um combate e uma missão
3. **Lute por turnos**: atacar, defender, beber poção ou fugir
4. **Volte à cidade** para comprar equipamento, estocar poções e dormir na estalagem
5. **Sobreviva ao chefe**, que aparece a cada 5 missões concluídas

> **Dica:** nunca encare o chefe de mãos vazias. Sem poção suas chances de vitória são muito reduzidas

---

## Arquitetura

O projeto é organizado em camadas com uma regra simples: **cada camada só
conhece as de baixo**.

```
rpg_projeto/
│
├── main.py                    ← ponto de entrada
│
├── ferramentas/
│   └── balanceamento.py       ← simulador de partidas
│
└── rpg/
    ├── config.py              ← TODAS as constantes de ajuste
    ├── jogo.py                ← menu principal e tratamento de derrota
    │
    ├── models/                ← DOMÍNIO — estado e comportamento próprio
    │   ├── personagem.py         HP, XP, nível, vidas, inventário
    │   ├── monstro.py
    │   ├── item.py
    │   └── terreno.py
    │
    ├── data/                  ← CONTEÚDO — catálogos editáveis
    │   ├── bestiario.py          arquétipos e escalonamento
    │   ├── itens.py
    │   └── missoes.py
    │
    ├── core/                  ← REGRAS — o que acontece e quando
    │   ├── criacao.py
    │   ├── combate.py
    │   ├── loja.py               loja + estalagem
    │   └── exploracao.py
    │
    └── ui/
        └── console.py         ← ÚNICO lugar com print(), input() e pausas
```

### As fronteiras

| Camada | Conhece | Não conhece |
|---|---|---|
| `models` | apenas `config` | interface, fluxo do jogo |
| `data` | `models` | regras, interface |
| `core` | `models`, `data`, `ui` | — |
| `ui` | nada | todo o resto |

**O que isso compra na prática:**

- Trocar o terminal por Tkinter, Flask ou Pygame → reescreve só `rpg/ui/`
- Criar um monstro, item ou missão → mexe só em `rpg/data/`
- Mudar a dificuldade → mexe só em `rpg/config.py`
- Testar as regras sem interface → o simulador faz exatamente isso

---

## Balanceamento (medido, não chutado)

Os inimigos **não têm atributos fixos**. Cada um é construído a partir dos
atributos atuais do herói, em função de quantos turnos a luta deve durar:

```python
TURNOS_PARA_VENCER = 6   # o herói derruba o inimigo médio em ~6 golpes
TURNOS_PARA_PERDER = 5   # o inimigo derruba o herói em ~5 golpes
```

O inimigo é deliberadamente **mais forte no ataque**. A vantagem do herói vem
de quatro mecânicas somadas:

```
  Herói ataca primeiro            ·  Crítico em 22% dos golpes
  Inimigo perde 28% dos turnos    ·  Poções e fuga
  se defendendo
```

### Taxa de vitória por build e nível

3.000 combates simulados por célula:

| Build inicial | Nv 1 | Nv 3 | Nv 6 | Nv 10 | Nv 15 |
|---|:---:|:---:|:---:|:---:|:---:|
| Equilibrado (12/8) | 78,7% | 81,0% | 81,5% | 80,4% | 80,2% |
| Ofensivo (18/2) | 80,9% | 78,7% | 81,7% | 81,1% | 79,2% |
| Defensivo (4/16) | 79,3% | 78,6% | 79,2% | 82,3% | 82,5% |
| Espalhado (10/10) | 78,3% | 82,1% | 79,6% | 81,1% | 81,3% |

Estável em ~80% para **qualquer distribuição de pontos** e **qualquer nível**.
Nenhuma build vira armadilha, nenhuma vira atalho.

### O chefe

| Poções | Vitória |
|:---:|:---:|
| 0 | 38,8% |
| 1 | 76,1% |
| 2 | 96,3% |
| 3 | 99,8% |

É a decisão mais importante do jogo: preparar-se ou arriscar.

### A jornada

| Métrica | Valor |
|---|---|
| Combates vencidos por partida | 23,7 |
| Nível médio alcançado | 4,3 |
| Duração média de um combate | 5,2 turnos |

Reproduza qualquer número acima com:

```bash
python ferramentas/balanceamento.py
```

<details>
<summary><b>Dois problemas que só a simulação revelou</b></summary>

**Builds defensivas eram invencíveis.** O ataque do inimigo escalava a partir
do *ataque* do herói. Quem investia tudo em Defesa recebia sempre o dano mínimo
e vencia 100% das lutas. A correção foi calcular o ataque inimigo a partir da
defesa e do HP do herói.

**Sem cura entre combates, o XP seria decorativo.** Com morte permanente e ~20%
de derrota por luta, uma jornada durava ~5 combates por pura aritmética —
ninguém sairia do nível 1. Duas mudanças resolveram: a **estalagem** (troca
ouro por HP) e o sistema de **vidas** (3 derrotas, com resgate custando metade
do ouro). O resultado saltou de 3 combates e nível 1,3 para 23,7 combates e
nível 4,3.

</details>

---

## Ajustando a dificuldade

Tudo mora em `rpg/config.py`. Depois de mexer, rode o simulador para ver o
efeito **antes** de jogar.

| Quero... | Mexa em |
|---|---|
| Lutas mais longas | `TURNOS_PARA_VENCER` |
| Inimigos mais letais | `TURNOS_PARA_PERDER` *(menor = mais letal)* |
| Jogo mais fácil | `CHANCE_CRITICO`, `REDUCAO_AO_DEFENDER`, `VIDAS_INICIAIS` |
| Jornadas mais longas | `CUSTO_DESCANSO_POR_NIVEL` *(menor = mais longa)* |
| Progressão mais rápida | `XP_PARA_SUBIR` *(menor = mais rápida)* |
| Narração mais rápida | `RITMO`, ou `PAUSAS_ATIVAS = False` |

> **Quer a tensão do roguelike?** `VIDAS_INICIAIS = 1` devolve a morte
> permanente — mas saiba que a progressão de nível volta a ser quase
> inatingível. O trade-off está medido acima.

---

## Estendendo o jogo

<details>
<summary><b>Adicionar um monstro</b></summary>

Em `rpg/data/bestiario.py`, acrescente um arquétipo. Os multiplicadores são
aplicados sobre os atributos do herói, então o inimigo escala sozinho:

```python
Arquetipo("Basilisco", mult_hp=1.20, mult_ataque=1.10,
          mult_defesa=0.90, mult_recompensa=1.30, peso=7),
```

`peso` controla a frequência no sorteio.

</details>

<details>
<summary><b>Adicionar um item</b></summary>

Em `rpg/data/itens.py`:

```python
Item("Elixir", custo=60, atributo="hp", valor=70,
     consumivel=True, percentual=True),
```

`percentual=True` faz `valor` ser uma porcentagem do HP máximo — assim o item
continua útil em qualquer nível.

</details>

<details>
<summary><b>Adicionar um terreno ou missão</b></summary>

Terreno: acrescente em `montar_mapa()` no `rpg/jogo.py`.
Missão: acrescente uma string na tupla `MISSOES` em `rpg/data/missoes.py`.

</details>

<details>
<summary><b>Trocar o terminal por outra interface</b></summary>

Todo `print()` e `input()` do projeto está em `rpg/ui/console.py`. Reimplemente
as funções públicas desse módulo (`exibir`, `narrar`, `menu`, `ler_inteiro`,
`pausa`, ...) e o resto do jogo funciona sem alteração.

</details>

---

## Licença

MIT — use, modifique e distribua livremente.

<div align="center">
<sub>Feito com Python puro e muitas simulações.</sub>
</div>
