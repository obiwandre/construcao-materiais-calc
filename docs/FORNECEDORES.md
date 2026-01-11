# Sistema de Gerenciamento de Fornecedores

Sistema centralizado para cadastro de fornecedores e historico de precos por data.

## Funcionalidades

### Fornecedores
- Cadastro completo (nome, contato, telefone, WhatsApp, email, site, endereco)
- Categorias por tipo de material (blocos, eps, tijolos, cimento)
- Link direto para WhatsApp
- Ativacao/desativacao (soft delete)

### Historico de Precos
- Registro de precos por data
- Filtro por categoria
- Visualizacao de evolucao de precos
- Suporte a tabela de frete
- Desconto a vista

---

## Estrutura de Arquivos

```
src/shared/fornecedores/
├── __init__.py
├── gerenciador.py          # Funcoes CRUD
└── dados/
    ├── fornecedores.json   # Cadastro de fornecedores
    └── precos.json         # Historico de precos
```

---

## API Endpoints

### Fornecedores

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/api/fornecedores` | Lista todos os fornecedores |
| GET | `/api/fornecedores/{id}` | Busca fornecedor por ID |
| POST | `/api/fornecedores` | Cadastra novo fornecedor |
| PUT | `/api/fornecedores/{id}` | Atualiza fornecedor |

### Precos

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/api/precos` | Lista historico completo |
| GET | `/api/precos/atuais` | Precos mais recentes |
| POST | `/api/precos` | Registra novos precos |
| GET | `/api/precos/historico/{cat}/{id}` | Evolucao de preco |

---

## Estrutura de Dados

### Fornecedor
```json
{
  "id": 1,
  "nome": "Isoportal",
  "contato": "Victor",
  "telefone": "(11) 97572-0094",
  "whatsapp": "(11) 97572-0094",
  "email": null,
  "site": "https://isoportal.com.br",
  "endereco": null,
  "categorias": ["eps"],
  "ativo": true,
  "data_cadastro": "2025-01-10"
}
```

### Registro de Precos
```json
{
  "id": 1,
  "data": "2025-01-10",
  "fornecedor_id": 2,
  "categoria": "eps",
  "produtos": [
    {"produto_id": 1, "nome": "EPS 30mm", "preco": 7.95},
    {"produto_id": 2, "nome": "EPS 40mm", "preco": 10.60},
    {"produto_id": 3, "nome": "EPS 100mm", "preco": 26.50}
  ],
  "frete": [
    {"min": 1000, "max": 3000, "valor": 960},
    {"min": 8000, "max": null, "valor": 0, "obs": "Frete gratis"}
  ],
  "desconto_avista_percent": 3,
  "observacao": "Orcamento WhatsApp - Victor"
}
```

---

## Interface Web

Acesse: `http://localhost:8000/static/fornecedores.html`

### Abas

1. **Fornecedores** - Lista e cadastro de fornecedores
2. **Historico de Precos** - Visualizacao por data e categoria
3. **Atualizar Precos** - Formulario para registrar novos precos

---

## Fornecedores Cadastrados

| ID | Nome | Contato | Telefone | Categorias |
|----|------|---------|----------|------------|
| 1 | Blocok Sao Paulo | Comercial | (11) 93068-9990 | blocos |
| 2 | Isoportal | Victor | (11) 97572-0094 | eps |

---

## Como Usar

### Adicionar Fornecedor (via API)
```bash
curl -X POST http://localhost:8000/api/fornecedores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Novo Fornecedor", "telefone": "(11) 99999-9999", "categorias": ["tijolos"]}'
```

### Registrar Precos (via API)
```bash
curl -X POST http://localhost:8000/api/precos \
  -H "Content-Type: application/json" \
  -d '{
    "fornecedor_id": 1,
    "categoria": "blocos",
    "data": "2025-01-15",
    "produtos": [
      {"produto_id": 1, "nome": "Blocok 10", "preco": 100.00}
    ],
    "observacao": "Reajuste janeiro"
  }'
```

### Consultar Precos Atuais
```bash
curl http://localhost:8000/api/precos/atuais?categoria=eps
```

---

## Integracao com Modulos

O sistema de fornecedores e compartilhado entre todos os modulos:
- `src/modulos/blocos/` - Blocok
- `src/modulos/eps/` - EPS Isolamento
- Futuros: tijolos, cimento, etc.

Cada modulo pode consultar os precos mais recentes do fornecedor correspondente.
