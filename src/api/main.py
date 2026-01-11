# API Principal - FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Adiciona o src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modulos.blocos.calculadora import calcular_blocos, carregar_blocos
from modulos.eps.calculadora import calcular_eps, carregar_eps
from shared.fornecedores.gerenciador import (
    listar_fornecedores, buscar_fornecedor, adicionar_fornecedor, atualizar_fornecedor,
    buscar_precos_atuais, adicionar_registro_precos, historico_por_produto, listar_historico_completo
)
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="Calculadora de Materiais - Construcao Civil",
    description="API para calcular quantidade de materiais para obras",
    version="1.1.0"
)

# Servir arquivos estaticos (frontend)
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')
if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")


@app.get("/")
async def home():
    """Pagina inicial - serve o frontend"""
    index_path = os.path.join(FRONTEND_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Calculadora de Materiais API", "docs": "/docs"}


# ============ BLOCOS ============

@app.get("/api/blocos")
async def listar_blocos():
    """Lista todos os blocos disponiveis"""
    dados = carregar_blocos()
    return dados


@app.get("/api/blocos/calcular")
async def calcular_bloco(largura: float, altura: float, bloco_id: int = 1):
    """
    Calcula quantidade de blocos para uma parede

    - **largura**: largura da parede em metros
    - **altura**: altura da parede em metros
    - **bloco_id**: tipo do bloco (1=10cm, 2=13cm, 3=15cm, 4=20cm)
    """
    resultado = calcular_blocos(largura, altura, bloco_id)
    return resultado


@app.get("/api/blocos/calcular-todos")
async def calcular_todos_blocos(largura: float, altura: float):
    """
    Calcula quantidade de blocos para todos os tipos

    - **largura**: largura da parede em metros
    - **altura**: altura da parede em metros
    """
    resultados = []
    for bloco_id in [1, 2, 3, 4]:
        resultado = calcular_blocos(largura, altura, bloco_id)
        resultados.append(resultado)
    return resultados


# ============ EPS ============

@app.get("/api/eps")
async def listar_eps():
    """Lista todos os produtos EPS disponiveis"""
    dados = carregar_eps()
    return dados


@app.get("/api/eps/calcular")
async def calcular_placa_eps(area: float, produto_id: int = 1):
    """
    Calcula quantidade de placas EPS para uma area

    - **area**: area em metros quadrados
    - **produto_id**: tipo do EPS (1=30mm, 2=40mm, 3=100mm)
    """
    resultado = calcular_eps(area, produto_id)
    return resultado


@app.get("/api/eps/calcular-todos")
async def calcular_todos_eps(area: float):
    """
    Calcula quantidade de EPS para todos os tipos

    - **area**: area em metros quadrados
    """
    resultados = []
    for produto_id in [1, 2, 3]:
        resultado = calcular_eps(area, produto_id)
        resultados.append(resultado)
    return resultados


# ============ FORNECEDORES ============

class FornecedorCreate(BaseModel):
    nome: str
    contato: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None
    endereco: Optional[str] = None
    categorias: List[str] = []


class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    contato: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None
    endereco: Optional[str] = None
    categorias: Optional[List[str]] = None
    ativo: Optional[bool] = None


class ProdutoPreco(BaseModel):
    produto_id: int
    nome: str
    preco: float
    preco_m2: Optional[float] = None


class FreteItem(BaseModel):
    min: float
    max: Optional[float] = None
    valor: Optional[float] = None
    obs: Optional[str] = None


class RegistroPrecos(BaseModel):
    fornecedor_id: int
    categoria: str
    produtos: List[ProdutoPreco]
    data: Optional[str] = None
    observacao: Optional[str] = None
    frete: Optional[List[FreteItem]] = None
    desconto_avista_percent: Optional[float] = None


@app.get("/api/fornecedores")
async def api_listar_fornecedores(apenas_ativos: bool = True):
    """Lista todos os fornecedores cadastrados"""
    return listar_fornecedores(apenas_ativos)


@app.get("/api/fornecedores/{fornecedor_id}")
async def api_buscar_fornecedor(fornecedor_id: int):
    """Busca um fornecedor pelo ID"""
    fornecedor = buscar_fornecedor(fornecedor_id)
    if not fornecedor:
        return {"error": "Fornecedor nao encontrado"}
    return fornecedor


@app.post("/api/fornecedores")
async def api_adicionar_fornecedor(fornecedor: FornecedorCreate):
    """Cadastra um novo fornecedor"""
    return adicionar_fornecedor(fornecedor.dict())


@app.put("/api/fornecedores/{fornecedor_id}")
async def api_atualizar_fornecedor(fornecedor_id: int, dados: FornecedorUpdate):
    """Atualiza dados de um fornecedor"""
    # Remove campos None
    dados_filtrados = {k: v for k, v in dados.dict().items() if v is not None}
    resultado = atualizar_fornecedor(fornecedor_id, dados_filtrados)
    if not resultado:
        return {"error": "Fornecedor nao encontrado"}
    return resultado


# ============ PRECOS ============

@app.get("/api/precos")
async def api_listar_historico():
    """Lista todo o historico de precos"""
    return listar_historico_completo()


@app.get("/api/precos/atuais")
async def api_precos_atuais(fornecedor_id: int = None, categoria: str = None):
    """Busca os precos mais recentes"""
    return buscar_precos_atuais(fornecedor_id, categoria)


@app.post("/api/precos")
async def api_adicionar_precos(registro: RegistroPrecos):
    """Registra novos precos no historico"""
    produtos = [p.dict() for p in registro.produtos]
    frete = [f.dict() for f in registro.frete] if registro.frete else None

    return adicionar_registro_precos(
        fornecedor_id=registro.fornecedor_id,
        categoria=registro.categoria,
        produtos=produtos,
        data=registro.data,
        observacao=registro.observacao,
        frete=frete,
        desconto_avista_percent=registro.desconto_avista_percent
    )


@app.get("/api/precos/historico/{categoria}/{produto_id}")
async def api_historico_produto(categoria: str, produto_id: int):
    """Retorna a evolucao de preco de um produto"""
    return historico_por_produto(categoria, produto_id)


# Para rodar: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
