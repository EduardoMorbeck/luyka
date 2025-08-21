from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import products

app = FastAPI(title="API Luyka", version="1.0.0")

# CORS — ajuste se necessário
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(products.router)
