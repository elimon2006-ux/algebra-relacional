FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements desde la misma carpeta donde está el Dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código (main.py)
COPY . .

CMD ["python", "main.py"]