# Stage 1 — Front build
FROM node:20 AS front
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build   # gera /dist na raiz do projeto

# Stage 2 — Backend Python
FROM python:3.11-slim
WORKDIR /app

# deps de sistema (se precisar compilar libs)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código backend + dist do front
COPY backend ./backend
COPY --from=front /app/dist ./dist

ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
