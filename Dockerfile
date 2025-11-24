# Dockerfile para Google Cloud Run u otros servicios que usen Docker
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer puerto (Cloud Run usa la variable PORT)
EXPOSE 8080

# Comando para ejecutar la aplicación
# Cloud Run pasa PORT como variable de entorno
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

