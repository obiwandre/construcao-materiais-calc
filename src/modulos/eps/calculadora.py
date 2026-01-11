# Calculadora de EPS - Isolamento Térmico
# Módulo para cálculo de placas de EPS

import json
import math
import os

# Caminho do arquivo de dados
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'dados', 'eps.json')


def carregar_eps():
    """Carrega os dados dos produtos EPS do JSON"""
    with open(DADOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def listar_eps():
    """Lista todos os produtos EPS disponíveis"""
    dados = carregar_eps()
    print("\n=== EPS DISPONÍVEIS ===\n")
    print(f"Fabricante: {dados['fabricante']['nome']}")
    print(f"Contato: {dados['fabricante']['contato']}")
    print(f"Material: {dados['material']['nome']} - Densidade {dados['material']['densidade_kg_m3']} kg/m³")
    print(f"Antichama: {'Sim' if dados['material']['antichama'] else 'Não'}")
    print("-" * 50)

    for produto in dados['produtos']:
        print(f"\n[{produto['id']}] {produto['nome']}")
        print(f"    Medida: {produto['largura_mm']}x{produto['altura_mm']}mm ({produto['area_m2']}m² por placa)")
        print(f"    Espessura: {produto['espessura_mm']}mm")
        print(f"    Preço: R$ {produto['preco_unitario']:.2f}/placa | R$ {produto['preco_m2']:.2f}/m²")
        print(f"    Isolamento: {produto['isolamento']}")
        print(f"    Uso: {produto['aplicacao']}")


def calcular_frete(valor_total: float) -> dict:
    """
    Calcula o frete baseado no valor total do pedido.

    Args:
        valor_total: valor total das placas em reais

    Returns:
        Dicionário com valor do frete e observação
    """
    dados = carregar_eps()
    tabela_frete = dados['frete']['tabela']

    for faixa in tabela_frete:
        valor_min = faixa['valor_min']
        valor_max = faixa['valor_max']

        if valor_max is None:
            if valor_total >= valor_min:
                return {
                    'valor': faixa['frete'],
                    'obs': faixa.get('obs', 'Frete grátis')
                }
        elif valor_min <= valor_total < valor_max:
            if faixa['frete'] is None:
                return {
                    'valor': None,
                    'obs': faixa.get('obs', 'Consultar')
                }
            return {
                'valor': faixa['frete'],
                'obs': f"Frete para {dados['frete']['destino_referencia']}"
            }

    return {'valor': None, 'obs': 'Consultar'}


def calcular_eps(area_m2: float, produto_id: int = 1) -> dict:
    """
    Calcula quantas placas de EPS são necessárias para uma área.

    Args:
        area_m2: área a ser coberta em metros quadrados
        produto_id: ID do tipo de EPS (1=30mm, 2=40mm, 3=100mm)

    Returns:
        Dicionário com quantidade, custo e detalhes
    """
    dados = carregar_eps()

    # Encontra o produto pelo ID
    produto = None
    for p in dados['produtos']:
        if p['id'] == produto_id:
            produto = p
            break

    if not produto:
        raise ValueError(f"EPS com ID {produto_id} não encontrado")

    # Área de cada placa
    area_placa = produto['area_m2']

    # Quantidade de placas (arredonda pra cima)
    quantidade = math.ceil(area_m2 / area_placa)

    # Custo total das placas
    custo_placas = quantidade * produto['preco_unitario']

    # Calcula frete
    frete_info = calcular_frete(custo_placas)

    # Custo total com frete
    custo_total = custo_placas
    if frete_info['valor'] is not None:
        custo_total += frete_info['valor']

    # Desconto à vista
    desconto_percent = dados['fabricante']['desconto_avista_percent']
    custo_avista = custo_placas * (1 - desconto_percent / 100)

    return {
        'produto': produto['nome'],
        'espessura_mm': produto['espessura_mm'],
        'area_solicitada_m2': area_m2,
        'area_placa_m2': area_placa,
        'quantidade_placas': quantidade,
        'area_total_m2': quantidade * area_placa,
        'preco_unitario': produto['preco_unitario'],
        'preco_m2': produto['preco_m2'],
        'custo_placas': custo_placas,
        'custo_avista': custo_avista,
        'desconto_avista_percent': desconto_percent,
        'frete': frete_info['valor'],
        'frete_obs': frete_info['obs'],
        'custo_total': custo_total,
        'isolamento': produto['isolamento'],
        'aplicacao': produto['aplicacao']
    }


# Teste rápido
if __name__ == "__main__":
    # Lista produtos disponíveis
    listar_eps()

    print("\n" + "=" * 50)
    print("CÁLCULO PARA 120m²")
    print("=" * 50)

    area = 120.0  # metros quadrados

    # Calcula para cada tipo de EPS
    for produto_id in [1, 2, 3]:
        resultado = calcular_eps(area, produto_id)

        print(f"\n--- {resultado['produto']} ({resultado['espessura_mm']}mm) ---")
        print(f"Quantidade: {resultado['quantidade_placas']} placas")
        print(f"Custo placas: R$ {resultado['custo_placas']:.2f}")
        print(f"Custo à vista (3% desc): R$ {resultado['custo_avista']:.2f}")
        if resultado['frete'] is not None:
            print(f"Frete: R$ {resultado['frete']:.2f} ({resultado['frete_obs']})")
        else:
            print(f"Frete: {resultado['frete_obs']}")
        print(f"TOTAL: R$ {resultado['custo_total']:.2f}")
