# Calculadora de Materiais de Construção Civil

App para mensurar quantidade de materiais usados na construção civil.

## Objetivo

Calcular a quantidade de materiais necessários para obras, considerando:
- Dimensões (largura x altura)
- Modelos de materiais disponíveis
- Preços por unidade

## Estrutura do Projeto

```
src/
├── api/                    # Endpoints da API (rotas)
├── config/                 # Configurações (banco, ambiente, etc)
├── shared/                 # Código compartilhado entre módulos
│   ├── database/           # Conexão e configuração do banco de dados
│   ├── models/             # Models base compartilhados
│   └── utils/              # Funções utilitárias (formatação, cálculos comuns)
└── modulos/
    ├── tijolos/            # Módulo de cálculo de tijolos
    └── blocos/             # Módulo de cálculo de blocos
```

## Arquitetura

### shared/
Contém código reutilizável por todos os módulos:
- **database/**: Configuração de conexão, migrations, seeds
- **models/**: Classes base, interfaces compartilhadas
- **utils/**: Funções auxiliares (formatação de moeda, cálculo de área, etc)

### modulos/
Cada módulo é independente mas pode importar do `shared/`:
- Tem seus próprios models, services e controllers
- Segue a mesma estrutura interna

### api/
Centraliza as rotas e endpoints para exposição web.

### config/
Configurações de ambiente, variáveis, conexões.

## Módulos Planejados

### Tijolos
- Cadastro de modelos de tijolos com dimensões e preços
- Cálculo de quantidade para paredes (largura x altura)
- Estimativa de custo total

### Blocos
- Cadastro de modelos de blocos com dimensões e preços
- Cálculo de quantidade para paredes/muros
- Estimativa de custo total

## Deploy

O app será hospedado em VPS para acesso público via web.

## Tecnologias

A definir conforme desenvolvimento.
