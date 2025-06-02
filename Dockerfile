FROM python:3.11-slim

# Evita problemas con buffering
ENV PYTHONUNBUFFERED=1

# Cloud Run asigna dinámicamente el puerto en la variable de entorno $PORT
ENV PORT=8080

WORKDIR /app

# Instala dependencias del sistema necesarias si usas PostgreSQL, Pillow, etc.
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código de tu proyecto
COPY . .

# Recolecta archivos estáticos (para Django)
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]


