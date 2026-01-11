# Gerenciador de Fornecedores e Histórico de Preços
# Sistema centralizado para todos os módulos

import json
import os
from datetime import datetime
from typing import Optional

# Caminhos dos arquivos de dados
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'dados')
FORNECEDORES_PATH = os.path.join(DADOS_PATH, 'fornecedores.json')
PRECOS_PATH = os.path.join(DADOS_PATH, 'precos.json')


# ============ FORNECEDORES ============

def carregar_fornecedores() -> dict:
    """Carrega todos os fornecedores do JSON"""
    with open(FORNECEDORES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_fornecedores(dados: dict) -> None:
    """Salva os fornecedores no JSON"""
    with open(FORNECEDORES_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def listar_fornecedores(apenas_ativos: bool = True) -> list:
    """Lista todos os fornecedores"""
    dados = carregar_fornecedores()
    fornecedores = dados['fornecedores']
    if apenas_ativos:
        fornecedores = [f for f in fornecedores if f.get('ativo', True)]
    return fornecedores


def buscar_fornecedor(fornecedor_id: int) -> Optional[dict]:
    """Busca um fornecedor pelo ID"""
    dados = carregar_fornecedores()
    for fornecedor in dados['fornecedores']:
        if fornecedor['id'] == fornecedor_id:
            return fornecedor
    return None


def buscar_fornecedor_por_categoria(categoria: str) -> list:
    """Busca fornecedores por categoria (blocos, eps, tijolos, etc)"""
    dados = carregar_fornecedores()
    return [
        f for f in dados['fornecedores']
        if categoria in f.get('categorias', []) and f.get('ativo', True)
    ]


def adicionar_fornecedor(dados_fornecedor: dict) -> dict:
    """
    Adiciona um novo fornecedor.

    Args:
        dados_fornecedor: dict com nome, contato, telefone, etc.

    Returns:
        Fornecedor criado com ID
    """
    dados = carregar_fornecedores()

    # Gera novo ID
    max_id = max([f['id'] for f in dados['fornecedores']], default=0)
    novo_id = max_id + 1

    # Monta o fornecedor
    novo_fornecedor = {
        'id': novo_id,
        'nome': dados_fornecedor.get('nome'),
        'contato': dados_fornecedor.get('contato'),
        'telefone': dados_fornecedor.get('telefone'),
        'whatsapp': dados_fornecedor.get('whatsapp', dados_fornecedor.get('telefone')),
        'email': dados_fornecedor.get('email'),
        'site': dados_fornecedor.get('site'),
        'endereco': dados_fornecedor.get('endereco'),
        'categorias': dados_fornecedor.get('categorias', []),
        'ativo': True,
        'data_cadastro': datetime.now().strftime('%Y-%m-%d')
    }

    dados['fornecedores'].append(novo_fornecedor)
    salvar_fornecedores(dados)

    return novo_fornecedor


def atualizar_fornecedor(fornecedor_id: int, dados_atualizados: dict) -> Optional[dict]:
    """
    Atualiza dados de um fornecedor existente.

    Args:
        fornecedor_id: ID do fornecedor
        dados_atualizados: campos a atualizar

    Returns:
        Fornecedor atualizado ou None se não encontrado
    """
    dados = carregar_fornecedores()

    for i, fornecedor in enumerate(dados['fornecedores']):
        if fornecedor['id'] == fornecedor_id:
            # Atualiza apenas os campos fornecidos
            for chave, valor in dados_atualizados.items():
                if chave != 'id':  # Não permite alterar ID
                    dados['fornecedores'][i][chave] = valor

            salvar_fornecedores(dados)
            return dados['fornecedores'][i]

    return None


def desativar_fornecedor(fornecedor_id: int) -> bool:
    """Desativa um fornecedor (soft delete)"""
    resultado = atualizar_fornecedor(fornecedor_id, {'ativo': False})
    return resultado is not None


# ============ HISTÓRICO DE PREÇOS ============

def carregar_historico_precos() -> dict:
    """Carrega todo o histórico de preços"""
    with open(PRECOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_historico_precos(dados: dict) -> None:
    """Salva o histórico de preços"""
    with open(PRECOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def buscar_precos_atuais(fornecedor_id: int = None, categoria: str = None) -> list:
    """
    Busca os preços mais recentes.

    Args:
        fornecedor_id: filtra por fornecedor (opcional)
        categoria: filtra por categoria (opcional)

    Returns:
        Lista com os registros de preços mais recentes
    """
    dados = carregar_historico_precos()
    historico = dados['historico']

    # Filtra
    if fornecedor_id:
        historico = [h for h in historico if h['fornecedor_id'] == fornecedor_id]
    if categoria:
        historico = [h for h in historico if h['categoria'] == categoria]

    # Agrupa por fornecedor+categoria e pega o mais recente
    mais_recentes = {}
    for registro in historico:
        chave = f"{registro['fornecedor_id']}_{registro['categoria']}"
        if chave not in mais_recentes or registro['data'] > mais_recentes[chave]['data']:
            mais_recentes[chave] = registro

    return list(mais_recentes.values())


def adicionar_registro_precos(
    fornecedor_id: int,
    categoria: str,
    produtos: list,
    data: str = None,
    observacao: str = None,
    frete: list = None,
    desconto_avista_percent: float = None
) -> dict:
    """
    Adiciona um novo registro de preços ao histórico.

    Args:
        fornecedor_id: ID do fornecedor
        categoria: categoria dos produtos (blocos, eps, etc)
        produtos: lista de produtos com preços
        data: data do registro (YYYY-MM-DD), default hoje
        observacao: observação opcional
        frete: tabela de frete opcional
        desconto_avista_percent: desconto à vista opcional

    Returns:
        Registro criado
    """
    dados = carregar_historico_precos()

    # Gera novo ID
    max_id = max([h['id'] for h in dados['historico']], default=0)
    novo_id = max_id + 1

    # Data default = hoje
    if not data:
        data = datetime.now().strftime('%Y-%m-%d')

    novo_registro = {
        'id': novo_id,
        'data': data,
        'fornecedor_id': fornecedor_id,
        'categoria': categoria,
        'produtos': produtos,
        'observacao': observacao
    }

    # Campos opcionais
    if frete:
        novo_registro['frete'] = frete
    if desconto_avista_percent is not None:
        novo_registro['desconto_avista_percent'] = desconto_avista_percent

    dados['historico'].append(novo_registro)
    salvar_historico_precos(dados)

    return novo_registro


def historico_por_produto(categoria: str, produto_id: int) -> list:
    """
    Retorna a evolução de preço de um produto ao longo do tempo.

    Args:
        categoria: categoria do produto
        produto_id: ID do produto

    Returns:
        Lista ordenada por data com {data, preco, fornecedor}
    """
    dados = carregar_historico_precos()
    evolucao = []

    for registro in dados['historico']:
        if registro['categoria'] != categoria:
            continue

        for produto in registro['produtos']:
            if produto['produto_id'] == produto_id:
                evolucao.append({
                    'data': registro['data'],
                    'preco': produto['preco'],
                    'fornecedor_id': registro['fornecedor_id'],
                    'observacao': registro.get('observacao')
                })

    # Ordena por data
    evolucao.sort(key=lambda x: x['data'])
    return evolucao


def listar_historico_completo() -> list:
    """Lista todo o histórico de preços ordenado por data"""
    dados = carregar_historico_precos()
    historico = dados['historico']
    historico.sort(key=lambda x: x['data'], reverse=True)
    return historico


# ============ TESTE ============

if __name__ == "__main__":
    print("=== FORNECEDORES ===")
    for f in listar_fornecedores():
        print(f"[{f['id']}] {f['nome']} - {f['contato']} ({f['telefone']})")
        print(f"    Categorias: {', '.join(f['categorias'])}")

    print("\n=== PREÇOS ATUAIS ===")
    for preco in buscar_precos_atuais():
        fornecedor = buscar_fornecedor(preco['fornecedor_id'])
        print(f"\n{fornecedor['nome']} - {preco['categoria'].upper()} ({preco['data']})")
        for p in preco['produtos']:
            print(f"  - {p['nome']}: R$ {p['preco']:.2f}")
