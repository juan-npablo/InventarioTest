from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import auth, categories, movements, products
from core.security import get_current_user


app1 = FastAPI(
    title="Sistema de Gestión de Inventario",
    version="1.0.0",
    docs_url="/docs",  # público
    redoc_url="/redoc",  # público
    openapi_url="/openapi.json"  # necesario para Swagger
)

app1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app1.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app1.include_router(categories.router, prefix="/api/v1/categories")
app1.include_router(movements.router, prefix="/api/v1/movements", dependencies=[Depends(get_current_user)])
app1.include_router(products.router, prefix="/api/v1/products", dependencies=[Depends(get_current_user)])

@app1.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the API!"}