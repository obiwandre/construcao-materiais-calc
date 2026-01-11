# Calculadora de Blocos - Blocok
# Versão 2 - Lê dados do JSON

import json
import math
import os

# Caminho do arquivo de dados
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'dados', 'blocos.json')


def carregar_blocos():
    """Carrega os dados dos blocos do JSON"""
    with open(DADOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def listar_blocos():
    """Lista todos os blocos disponíveis"""
    dados = carregar_blocos()
    print("\n=== BLOCOS DISPONÍVEIS ===\n")
    print(f"Fabricante: {dados['fabricante']['nome']}")
    print(f"Material: {dados['material']['nome']} - {dados['material']['composicao']}")
    print("-" * 50)

    for bloco in dados['blocos']:
        print(f"\n[{bloco['id']}] {bloco['nome']}")
        print(f"    Tamanho: {bloco['largura_cm']}x{bloco['altura_cm']}x{bloco['espessura_total_cm']} cm")
        print(f"    Preço: R$ {bloco['preco_avista']:.2f} à vista")
        print(f"    Uso: {bloco['aplicacao']}")


def calcular_blocos(largura_parede: float, altura_parede: float, bloco_id: int = 1) -> dict:
    """
    Calcula quantos blocos são necessários para uma parede.

    Args:
        largura_parede: largura da parede em metros
        altura_parede: altura da parede em metros
        bloco_id: ID do tipo de bloco (1=10cm, 2=13cm, 3=15cm, 4=20cm)

    Returns:
        Dicionário com quantidade, custo e detalhes
    """
    dados = carregar_blocos()

    # Encontra o bloco pelo ID
    bloco = None
    for b in dados['blocos']:
        if b['id'] == bloco_id:
            bloco = b
            break

    if not bloco:
        raise ValueError(f"Bloco com ID {bloco_id} não encontrado")

    # Área da parede
    area_parede = largura_parede * altura_parede

    # Área que um bloco ocupa (90x90cm = 0.81m²)
    # Blocok não usa junta tradicional, encaixa direto
    area_bloco = (bloco['largura_cm'] / 100) * (bloco['altura_cm'] / 100)

    # Quantidade de blocos
    quantidade = math.ceil(area_parede / area_bloco)

    # Custo total
    custo_total = quantidade * bloco['preco_avista']

    return {
        'bloco': bloco['nome'],
        'area_parede_m2': area_parede,
        'area_bloco_m2': area_bloco,
        'quantidade': quantidade,
        'preco_unitario': bloco['preco_avista'],
        'custo_total': custo_total,
        'peso_total_kg': quantidade * bloco['peso_kg'],
        'aplicacao': bloco['aplicacao']
    }


# Teste rápido
if __name__ == "__main__":
    # Lista blocos disponíveis
    listar_blocos()

    print("\n" + "=" * 50)
    print("CÁLCULO PARA PAREDE 3x3m")
    print("=" * 50)

    largura = 3.0  # metros
    altura = 3.0   # metros

    # Calcula para cada tipo de bloco
    for bloco_id in [1, 2, 3, 4]:
        resultado = calcular_blocos(largura, altura, bloco_id)

        print(f"\n--- {resultado['bloco']} ---")
        print(f"Quantidade: {resultado['quantidade']} unidades")
        print(f"Custo total: R$ {resultado['custo_total']:.2f}")
        print(f"Peso total: {resultado['peso_total_kg']} kg")
