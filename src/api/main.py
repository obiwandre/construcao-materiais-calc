# API Principal - FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Adiciona o src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modulos.blocos.calculadora import calcular_blocos, carregar_blocos

app = FastAPI(
    title="Calculadora de Materiais - Construção Civil",
    description="API para calcular quantidade de materiais para obras",
    version="1.0.0"
)

# Servir arquivos estáticos (frontend)
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')
if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")


@app.get("/")
async def home():
    """Página inicial - serve o frontend"""
    index_path = os.path.join(FRONTEND_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Calculadora de Materiais API", "docs": "/docs"}


@app.get("/api/blocos")
async def listar_blocos():
    """Lista todos os blocos disponíveis"""
    dados = carregar_blocos()
    return dados


@app.get("/api/blocos/calcular")
async def calcular(largura: float, altura: float, bloco_id: int = 1):
    """
    Calcula quantidade de blocos para uma parede

    - **largura**: largura da parede em metros
    - **altura**: altura da parede em metros
    - **bloco_id**: tipo do bloco (1=10cm, 2=13cm, 3=15cm, 4=20cm)
    """
    resultado = calcular_blocos(largura, altura, bloco_id)
    return resultado


@app.get("/api/blocos/calcular-todos")
async def calcular_todos(largura: float, altura: float):
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


# Para rodar: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
