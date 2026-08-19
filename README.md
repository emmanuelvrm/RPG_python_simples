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


