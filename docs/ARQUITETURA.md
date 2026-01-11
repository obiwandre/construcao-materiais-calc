# Arquitetura do Projeto

## Visão Geral

Este projeto segue uma arquitetura modular, onde cada tipo de material de construção é um módulo independente que compartilha recursos comuns através da pasta `shared/`.

```
src/
├── api/                    # Camada de exposição (rotas HTTP)
├── config/                 # Configurações do sistema
├── shared/                 # Recursos compartilhados
│   ├── database/           # Camada de persistência
│   ├── models/             # Models e interfaces base
│   └── utils/              # Funções utilitárias
└── modulos/                # Módulos de negócio
    ├── tijolos/
    └── blocos/
```

---

## Camadas

### 1. `src/api/`

Responsável por expor a aplicação via HTTP (REST API).

**Contém:**
- Definição de rotas
- Controllers que recebem requisições
- Middlewares (autenticação, validação, etc)
- Tratamento de erros HTTP

**Exemplo de uso:**
```
api/
├── routes/
│   ├── tijolos.routes.js
│   └── blocos.routes.js
├── middlewares/
│   └── errorHandler.js
└── index.js
```

---

### 2. `src/config/`

Centraliza todas as configurações do sistema.

**Contém:**
- Variáveis de ambiente
- Configurações de banco de dados
- Configurações de terceiros (APIs externas, etc)
- Constantes do sistema

**Exemplo de uso:**
```
config/
├── database.js         # Config de conexão com banco
├── environment.js      # Variáveis de ambiente
└── constants.js        # Constantes globais
```

---

### 3. `src/shared/`

Código reutilizável por todos os módulos. **Nenhum módulo deve duplicar código que pode estar aqui.**

#### 3.1 `shared/database/`

Gerencia toda a camada de persistência.

**Contém:**
- Configuração de conexão com banco
- Migrations (criação/alteração de tabelas)
- Seeds (dados iniciais)
- Query builders ou ORM config

**Exemplo de uso:**
```
database/
├── connection.js       # Instância de conexão
├── migrations/         # Alterações no schema
└── seeds/              # Dados iniciais
```

#### 3.2 `shared/models/`

Models e interfaces base que serão estendidos pelos módulos.

**Contém:**
- Classes base (BaseModel, BaseEntity)
- Interfaces compartilhadas
- Types comuns

**Exemplo de uso:**
```
models/
├── BaseModel.js        # Classe base com métodos CRUD
└── interfaces/
    └── IMaterial.js    # Interface comum para materiais
```

#### 3.3 `shared/utils/`

Funções auxiliares puras, sem dependência de estado.

**Contém:**
- Cálculos comuns (área, volume, conversões)
- Formatação (moeda, números, datas)
- Validações genéricas
- Helpers diversos

**Exemplo de uso:**
```
utils/
├── calculos.js         # calcularArea(), calcularVolume()
├── formatadores.js     # formatarMoeda(), formatarNumero()
└── validadores.js      # validarDimensoes(), validarPreco()
```

---

### 4. `src/modulos/`

Cada módulo representa um domínio de negócio (tipo de material).

#### Estrutura interna de um módulo:

```
modulos/tijolos/
├── models/             # Models específicos do módulo
│   └── Tijolo.js
├── services/           # Lógica de negócio
│   └── TijoloService.js
├── controllers/        # Handlers de requisição
│   └── TijoloController.js
├── repositories/       # Acesso a dados
│   └── TijoloRepository.js
└── index.js            # Exportações do módulo
```

#### Responsabilidades:

| Camada | Responsabilidade |
|--------|------------------|
| **models/** | Definição da entidade, validações, schema |
| **services/** | Regras de negócio, cálculos específicos |
| **controllers/** | Receber request, chamar service, retornar response |
| **repositories/** | Queries ao banco, CRUD da entidade |

---

## Fluxo de uma Requisição

```
[Cliente]
    ↓ HTTP Request
[api/routes]
    ↓ roteia para controller
[modulos/X/controllers]
    ↓ chama service
[modulos/X/services]
    ↓ usa utils se necessário
    ↓ chama repository
[modulos/X/repositories]
    ↓ usa shared/database
[shared/database]
    ↓ executa query
[Banco de Dados]
```

---

## Regras de Dependência

```
┌─────────────────────────────────────────┐
│                  api/                   │  ← Pode importar de modulos/ e shared/
├─────────────────────────────────────────┤
│               modulos/                  │  ← Pode importar de shared/
├─────────────────────────────────────────┤
│               shared/                   │  ← NÃO importa de api/ nem modulos/
├─────────────────────────────────────────┤
│               config/                   │  ← Usado por todos
└─────────────────────────────────────────┘
```

**Regras:**
1. `shared/` NUNCA importa de `modulos/` ou `api/`
2. `modulos/` podem importar de `shared/` e `config/`
3. `api/` pode importar de `modulos/`, `shared/` e `config/`
4. Módulos NÃO devem importar uns dos outros diretamente

---

## Como Adicionar um Novo Módulo

1. Criar pasta em `src/modulos/[nome-do-modulo]/`
2. Criar estrutura interna (models, services, controllers, repositories)
3. Criar rotas em `src/api/routes/[nome-do-modulo].routes.js`
4. Registrar rotas no `src/api/index.js`
5. Se precisar de utils comum, adicionar em `shared/utils/`

---

## Boas Práticas

1. **Não duplicar código** - Se algo é usado por 2+ módulos, mova para `shared/`
2. **Módulos independentes** - Cada módulo deve funcionar isoladamente
3. **Config centralizada** - Nada de hardcode, usar `config/`
4. **Separação de responsabilidades** - Controller não faz query, Repository não valida negócio
5. **Utils são funções puras** - Sem efeitos colaterais, fácil de testar

---

## Tecnologias Sugeridas

| Componente | Opções |
|------------|--------|
| Backend | Node.js + Express / Python + FastAPI |
| Banco de Dados | PostgreSQL / SQLite (dev) |
| ORM | Prisma / Sequelize / SQLAlchemy |
| Frontend | React / Vue.js |
| Deploy | Docker + VPS |

---

## Próximos Passos

1. Definir tecnologia (Node.js ou Python)
2. Implementar `shared/database/` com conexão
3. Implementar módulo `tijolos/` como referência
4. Replicar padrão para `blocos/`
5. Criar API e frontend
