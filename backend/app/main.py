from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import products, frete, pagamento

app = FastAPI(title="API Luyka", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://luyka.onrender.com/"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(products.router)
app.include_router(frete.router)
app.include_router(pagamento.router)