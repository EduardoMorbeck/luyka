# backend/app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.routers import products  # ajuste conforme seus routers

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# sua API…
@app.get("/api/ping")
def ping():
    return {"ok": True}

# servir o front
app.mount("/", StaticFiles(directory="dist", html=True), name="static")

# Rotas da API sob /api
app.include_router(products.router, prefix="/api")

