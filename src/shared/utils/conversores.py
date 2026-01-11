# Conversores de unidades

def mm_para_m(valor: float) -> float:
    """Converte milímetros para metros"""
    return valor / 1000

def cm_para_m(valor: float) -> float:
    """Converte centímetros para metros"""
    return valor / 100

def m_para_cm(valor: float) -> float:
    """Converte metros para centímetros"""
    return valor * 100

def m_para_mm(valor: float) -> float:
    """Converte metros para milímetros"""
    return valor * 1000


def converter_para_metros(valor: float, unidade: str) -> float:
    """
    Converte qualquer unidade para metros.

    Args:
        valor: valor numérico
        unidade: 'mm', 'cm' ou 'm'

    Returns:
        Valor em metros
    """
    unidade = unidade.lower().strip()

    if unidade == 'mm':
        return mm_para_m(valor)
    elif unidade == 'cm':
        return cm_para_m(valor)
    elif unidade == 'm':
        return valor
    else:
        raise ValueError(f"Unidade '{unidade}' não reconhecida. Use: mm, cm ou m")


# Teste rápido
if __name__ == "__main__":
    print(f"900mm = {converter_para_metros(900, 'mm')}m")
    print(f"90cm = {converter_para_metros(90, 'cm')}m")
    print(f"0.9m = {converter_para_metros(0.9, 'm')}m")
