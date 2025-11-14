from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.api.cnj_router import router as cnj_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting CNJ Consulta API...")
    yield
    # Shutdown
    print("Shutting down CNJ Consulta API...")

app = FastAPI(
    title="CNJ Consulta API",
    version="1.0.0",
    description="API para consultar informações do CNJ (processos e advogados).",
    lifespan=lifespan
)

app.include_router(cnj_router, prefix="/cnj", tags=["CNJ"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API CNJ is working!",
        "version": "1.0.0",
        "endpoints": {
            "case_by_number": "/cnj/case-number?case_number=...",
            "case_by_lawyer": "/cnj/lawyer-name?lawyer_name=..."
        }
    }