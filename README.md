# RPG Simples — versão modularizada

Refatoração do script único `rpg.py` em pacotes com responsabilidades separadas.

## Como executar

```bash
cd rpg_projeto
python main.py
```

## Estrutura

```
rpg_projeto/
├── main.py                  # ponto de entrada (só chama iniciar_jogo)
└── rpg/
    ├── config.py            # constantes de balanceamento
    ├── jogo.py              # orquestra o fluxo principal / menu
    ├── models/              # DOMÍNIO: estado + comportamento próprio
    │   ├── personagem.py
    │   ├── monstro.py
    │   ├── item.py
    │   └── terreno.py
    ├── data/                # CONTEÚDO: catálogos editáveis
    │   ├── bestiario.py
    │   ├── itens.py
    │   └── missoes.py
    ├── core/                # REGRAS: o que acontece e quando
    │   ├── criacao.py
    │   ├── combate.py
    │   ├── loja.py
    │   └── exploracao.py
    └── ui/
        └── console.py       # ÚNICO lugar com print() e input()
```

## Princípios aplicados

| Camada | Conhece | Não conhece |
|---|---|---|
| `models` | nada do projeto (só `config`) | interface, regras de fluxo |
| `data` | `models` | regras, interface |
| `core` | `models`, `data`, `ui` | — |
| `ui` | nada | todo o resto |
| `jogo` | `core`, `models`, `ui` | detalhes de combate/loja |

O ganho prático: trocar o console por Tkinter, Flask ou Pygame exige
reescrever apenas `rpg/ui/`. Adicionar um monstro ou item novo mexe só
em `rpg/data/`. Ajustar dificuldade mexe só em `rpg/config.py`.

## Correções feitas durante a refatoração

1. **`if Terreno('Sair') == 'sair'` nunca era verdadeiro** — comparava um objeto
   com uma string, então o item "Sair" do menu não funcionava. Agora "Sair" é uma
   opção do menu, não um `Terreno` de mentira.
2. **`int(input())` sem tratamento** — qualquer letra derrubava o jogo com
   `ValueError`. Centralizado em `console.ler_inteiro()` com validação de faixa.
3. **`terrenos` era uma lista heterogênea** (`Terreno` misturado com a string
   `"Cidade"`), exigindo `isinstance()` no loop. Agora a lista é homogênea.
4. **Mensagem duplicada** — "Um X apareceu!" era impressa em `iniciar_jogo` e de
   novo em `batalhar`.
5. **Dano em ponto flutuante** — o crítico gerava `12.5 de dano`. Agora é inteiro.
6. **"Defender" não defendia** — apenas fazia o jogador perder o turno. Agora
   reduz o dano recebido em 50% (`REDUCAO_AO_DEFENDER`).
7. **Poção de cura ultrapassava o HP máximo** infinitamente. Agora existe
   `hp_maximo` e a cura respeita o teto.
8. **`if self.missoes_completas == random.randint(4,15)`** — o chefe aparecia por
   coincidência aleatória. Agora é determinístico: a cada `MISSOES_PARA_CHEFE`
   missões concluídas.
9. **Métodos mortos removidos** — `Monstro.atacado()` e o campo `recompensa`
   (duplicava `ouro`) nunca eram usados.
10. **`inventario` era decorativo** — agora recebe os itens permanentes comprados.
11. **Fuga bem-sucedida não interrompia o fluxo corretamente** — `batalhar()` agora
    devolve um `Resultado` (`VITORIA` / `DERROTA` / `FUGA`), permitindo ao chamador
    decidir o que fazer.

## Observação de balanceamento

O chefe "Dragão brilhante" tem defesa 50, acima do ataque máximo alcançável pelo
jogador no início — o dano fica em 0 e a luta é invencível. Isso vem do código
original; para corrigir, reduza `CHEFE["defesa"]` em `rpg/data/bestiario.py` ou
adicione dano mínimo garantido em `calcular_dano()`.
