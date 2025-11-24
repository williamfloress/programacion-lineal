# Guía de Despliegue en Producción - Calculadora de Programación Lineal

Este documento describe las diferentes opciones para desplegar la aplicación web Flask en producción, desde soluciones simples hasta configuraciones más robustas y escalables.

---

## ⚠️ IMPORTANTE: Gunicorn y Windows

> **🔴 Gunicorn NO funciona en Windows** - Esto es completamente normal y esperado. Gunicorn requiere módulos Unix (`fcntl`) que no existen en Windows.

**¿Por qué entonces todas las instrucciones mencionan Gunicorn?**

✅ **Porque Gunicorn se ejecuta en los servidores remotos (Linux), NO en tu Windows local**

- 🖥️ **En tu Windows:** Usas el servidor de desarrollo de Flask (`python app.py`) para probar
- 🚀 **En producción (servidores Linux):** Las plataformas de hosting ejecutan Gunicorn automáticamente

**Esto significa:**
- ✅ Incluye `gunicorn` en `requirements.txt` - Se instalará en el servidor Linux
- ✅ Configura el `Procfile` con Gunicorn - Se usará en el servidor Linux  
- ✅ NO intentes ejecutar Gunicorn en Windows - No funcionará
- ✅ Prueba localmente con `python app.py` - Funciona perfecto en Windows

**Ejemplo del flujo:**
1. Desarrollas en Windows → `python app.py` (servidor Flask dev)
2. Haces `git push` → Subes código a GitHub
3. Plataforma hosting detecta cambios → Descarga código
4. Servidor Linux ejecuta → `gunicorn app:app` (en servidor remoto)
5. Tu app está en línea → Funcionando con Gunicorn en Linux

> **✅ Compatibilidad con Windows:** Todas las opciones de hosting funcionan perfectamente desde Windows. El despliegue es remoto y Gunicorn se ejecuta automáticamente en sus servidores Linux.

---

## 📋 Índice

1. [Preparación del Proyecto](#preparación-del-proyecto)
2. [Opciones de Hosting](#opciones-de-hosting)
   - [Solución 1: Render (Recomendado para inicio rápido)](#solución-1-render-recomendado-para-inicio-rápido)
   - [Solución 2: Railway](#solución-2-railway)
   - [Solución 3: Heroku](#solución-3-heroku)
   - [Solución 4: DigitalOcean App Platform](#solución-4-digitalocean-app-platform)
   - [Solución 5: VPS (DigitalOcean Droplet, AWS EC2, Linode)](#solución-5-vps-digitalocean-droplet-aws-ec2-linode)
   - [Solución 6: AWS Elastic Beanstalk](#solución-6-aws-elastic-beanstalk)
   - [Solución 7: Google Cloud Run](#solución-7-google-cloud-run)
   - [Solución 8: Microsoft Azure App Service](#solución-8-microsoft-azure-app-service)
3. [Configuración Avanzada](#configuración-avanzada)
4. [Monitoreo y Logging](#monitoreo-y-logging)
5. [Consideraciones de Seguridad](#consideraciones-de-seguridad)

---

## 🔧 Preparación del Proyecto

Antes de desplegar, necesitamos preparar el proyecto para producción:

> **💡 Para Windows:** Los archivos de configuración (`requirements.txt`, `Procfile`) se usarán en el servidor Linux remoto. NO necesitas ejecutar Gunicorn en Windows. Prueba localmente con `python app.py`.

### 1. Crear archivo `requirements.txt`

Crea un archivo `requirements.txt` con las dependencias:

```txt
Flask>=2.0.0
numpy>=1.21.0
gunicorn>=20.1.0
```

> **📝 Nota Windows:** Incluye `gunicorn` aquí porque se instalará en el servidor Linux remoto. En Windows, no intentes instalar ni ejecutar Gunicorn - no funcionará. Para pruebas locales en Windows, usa solo Flask: `pip install Flask numpy` (sin gunicorn).

### 2. Modificar `app.py` para producción

Actualiza el final del archivo `app.py`:

```python
if __name__ == '__main__':
    # Desarrollo
    app.run(debug=True)
else:
    # Producción - configuración para servidor WSGI
    pass
```

### 3. Crear archivo `.env.example` (opcional)

Para variables de entorno:

```env
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-aqui
PORT=5000
```

### 4. Crear `Procfile` (para Heroku/Railway/Render)

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

> **📝 Nota Windows:** Este `Procfile` se ejecutará automáticamente en el servidor Linux de la plataforma de hosting. NO lo ejecutes en Windows (no funcionará). En Windows, prueba con `python app.py`.

### 5. Crear `runtime.txt` (opcional, para especificar versión de Python)

```
python-3.10.0
```

### 6. Probar la aplicación localmente (Windows)

**Para Windows - NO uses Gunicorn, usa el servidor de desarrollo de Flask:**

```powershell
# Windows PowerShell
python app.py
```

O si prefieres usar Flask CLI:

```powershell
# Windows PowerShell
flask run
```

Esto iniciará el servidor en `http://localhost:5000` donde podrás probar tu aplicación.

> **⚠️ Importante:** Esta es solo para desarrollo local. En producción, las plataformas de hosting usarán Gunicorn automáticamente en sus servidores Linux.

---

## 🌐 Opciones de Hosting

### Solución 1: Render (Recomendado para inicio rápido)

> **✅ Funciona perfectamente desde Windows:** Solo necesitas Git y un navegador web.

**Ventajas:**
- ✅ Gratis con plan básico
- ✅ HTTPS automático
- ✅ Despliegue automático desde Git
- ✅ Muy fácil de configurar
- ✅ Logs integrados
- ✅ 100% compatible con Windows (no requiere comandos locales)

**Desventajas:**
- ⚠️ El servicio gratuito se "duerme" después de inactividad
- ⚠️ Límites de recursos en plan gratuito

**Pasos para desplegar:**

1. **Preparar el proyecto:**
   - Asegúrate de tener un repositorio Git
   - Crea `requirements.txt` (ver arriba)
   - Crea `Procfile`:
     ```
     web: gunicorn app:app --bind 0.0.0.0:$PORT
     ```
     > **📝 Windows:** Este comando se ejecutará en el servidor Linux de Render, NO en tu Windows.

2. **En Render:**
   - Ve a https://render.com
   - Conecta tu repositorio GitHub/GitLab
   - Selecciona "New Web Service"
   - Configuración:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
       > **📝 Windows:** Este comando se ejecuta automáticamente en el servidor Linux de Render.
     - **Environment:** Python 3
     - **Port:** $PORT (variable automática)
   - Click "Create Web Service"
   
   > **💡 Para Windows:** No necesitas ejecutar estos comandos localmente. Render los ejecutará automáticamente en su servidor Linux cuando despliegues.

3. **Configurar variables de entorno (opcional):**
   - `FLASK_ENV=production`
   - `PYTHON_VERSION=3.10.0`

**Costo:** Gratis (con limitaciones) | Desde $7/mes para plan pago

---

### Solución 2: Railway

> **✅ Funciona perfectamente desde Windows:** Solo necesitas Git y un navegador web.

**Ventajas:**
- ✅ Muy fácil de usar
- ✅ Despliegue automático desde Git
- ✅ HTTPS automático
- ✅ $5 de crédito gratuito mensual
- ✅ 100% compatible con Windows (no requiere comandos locales)

**Desventajas:**
- ⚠️ Menos documentación que otras opciones
- ⚠️ Precios pueden aumentar con uso

**Pasos para desplegar:**

1. **Preparar el proyecto:**
   - Crea `requirements.txt`
   - Crea `Procfile`:
     ```
     web: gunicorn app:app --bind 0.0.0.0:$PORT
     ```
     > **📝 Windows:** Este comando se ejecutará en el servidor Linux de Railway, NO en tu Windows.

2. **En Railway:**
   - Ve a https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio
   - Railway detectará automáticamente que es una app Python
   - Railway ejecutará Gunicorn automáticamente en su servidor Linux
   - Configura variables de entorno si es necesario
   - Railway asignará automáticamente un dominio
   
   > **💡 Para Windows:** No necesitas ejecutar Gunicorn localmente. Railway lo ejecutará automáticamente en su servidor Linux.

**Costo:** $5 crédito gratuito/mes | Pagas por uso después

---

### Solución 3: Heroku

> **✅ Funciona perfectamente desde Windows:** Puedes usar Heroku CLI desde Windows PowerShell o hacerlo todo desde Git.

**Ventajas:**
- ✅ Muy popular y documentado
- ✅ Ecosistema grande de add-ons
- ✅ Despliegue desde Git
- ✅ Heroku CLI disponible para Windows

**Desventajas:**
- ⚠️ Eliminaron el plan gratuito (ahora es de pago)
- ⚠️ Más costoso que alternativas

**Pasos para desplegar:**

1. **Instalar Heroku CLI (opcional, también puedes usar Git directo):**
   ```powershell
   # Windows - PowerShell
   # Opción 1: Descargar instalador desde https://devcenter.heroku.com/articles/heroku-cli
   # Opción 2: Instalar con winget (Windows 10/11)
   winget install Heroku.CLI
   # Opción 3: Instalar con Chocolatey (si lo tienes)
   choco install heroku-cli
   ```

2. **Preparar el proyecto:**
   - Crea `requirements.txt`
   - Crea `Procfile`:
     ```
     web: gunicorn app:app --bind 0.0.0.0:$PORT
     ```
     > **📝 Windows:** Este comando se ejecutará en el servidor Linux de Heroku, NO en tu Windows.

3. **Desplegar (Windows PowerShell o Git Bash):**
   ```powershell
   # Windows PowerShell o Git Bash
   heroku login
   heroku create nombre-de-tu-app
   git push heroku main
   heroku open
   ```
   
   **Alternativa sin CLI (solo Git):**
   - Conecta tu repositorio GitHub a Heroku desde el dashboard web
   - Los comandos funcionan igual en PowerShell, CMD o Git Bash

**Costo:** Desde $5/mes (Eco Dyno)

---

### Solución 4: DigitalOcean App Platform

> **✅ Funciona perfectamente desde Windows:** Solo necesitas Git y un navegador web.

**Ventajas:**
- ✅ Despliegue automático desde Git
- ✅ HTTPS automático
- ✅ Buena relación precio/rendimiento
- ✅ Escalable
- ✅ 100% compatible con Windows (interfaz web completa)

**Desventajas:**
- ⚠️ Requiere tarjeta de crédito

**Pasos para desplegar:**

1. **Preparar el proyecto:**
   - Crea `requirements.txt`
   - Opcional: crea `app.yaml`:
     ```yaml
     name: programacion-lineal
     services:
     - name: web
       source_dir: /
       github:
         repo: tu-usuario/programacion-lineal
         branch: main
       run_command: gunicorn app:app --bind 0.0.0.0:$PORT
       environment_slug: python
       instance_count: 1
       instance_size_slug: basic-xxs
       http_port: 8080
     ```
     > **📝 Windows:** Este comando se ejecutará en el servidor Linux de DigitalOcean, NO en tu Windows.

2. **En DigitalOcean:**
   - Ve a https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Conecta tu repositorio
   - DigitalOcean detectará la configuración automáticamente
   - Revisa y ajusta la configuración
   - Click "Create Resources"

**Costo:** Desde $5/mes (Basic plan)

---

### Solución 5: VPS (DigitalOcean Droplet, AWS EC2, Linode)

> **⚠️ Requiere SSH desde Windows:** Esta opción requiere acceder a un servidor Linux vía SSH desde Windows. Puedes usar PowerShell (con OpenSSH), PuTTY, o WSL2.

**Ventajas:**
- ✅ Control total del servidor
- ✅ Más económico a largo plazo
- ✅ Flexible para configuraciones personalizadas

**Desventajas:**
- ⚠️ Requiere conocimiento de administración de servidores
- ⚠️ Debes configurar todo manualmente
- ⚠️ Necesitas acceder a un servidor Linux (no ejecuta en Windows directamente)

**Nota para Windows:** Los comandos siguientes se ejecutan en el servidor Linux remoto, no en tu máquina Windows. Puedes acceder usando:
- **PowerShell con OpenSSH** (incluido en Windows 10/11): `ssh usuario@servidor`
- **PuTTY** (Windows tradicional): https://www.putty.org/
- **WSL2** (Windows Subsystem for Linux): Para un entorno más similar a Linux

**Pasos para desplegar:**

#### 5.1 Configurar servidor (Ubuntu/Debian)

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python y pip
sudo apt install python3 python3-pip python3-venv nginx git -y

# 3. Crear usuario para la aplicación
sudo adduser appuser
sudo usermod -aG sudo appuser
su - appuser

# 4. Clonar repositorio
git clone https://github.com/tu-usuario/programacion-lineal.git
cd programacion-lineal

# 5. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 6. Probar la aplicación (esto se ejecuta en el servidor Linux, no en Windows)
gunicorn app:app --bind 0.0.0.0:5000
```

> **⚠️ Windows:** Estos comandos se ejecutan vía SSH en el servidor Linux remoto. NO intentes ejecutarlos directamente en Windows. Desde Windows, conéctate al servidor usando SSH y luego ejecuta estos comandos.

#### 5.2 Configurar Gunicorn como servicio

Crear archivo `/etc/systemd/system/programacion-lineal.service`:

```ini
[Unit]
Description=Gunicorn instance to serve Programacion Lineal
After=network.target

[Service]
User=appuser
Group=www-data
WorkingDirectory=/home/appuser/programacion-lineal
Environment="PATH=/home/appuser/programacion-lineal/venv/bin"
ExecStart=/home/appuser/programacion-lineal/venv/bin/gunicorn --workers 3 --bind unix:programacion-lineal.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Activar servicio
sudo systemctl start programacion-lineal
sudo systemctl enable programacion-lineal
```

#### 5.3 Configurar Nginx como proxy reverso

Crear archivo `/etc/nginx/sites-available/programacion-lineal`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/appuser/programacion-lineal/programacion-lineal.sock;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/programacion-lineal /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 5.4 Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

**Costo:** Desde $4/mes (DigitalOcean Droplet básico)

---

### Solución 6: AWS Elastic Beanstalk

> **✅ Funciona perfectamente desde Windows:** EB CLI funciona en Windows PowerShell, CMD o Git Bash.

**Ventajas:**
- ✅ Integración con servicios AWS
- ✅ Escalado automático
- ✅ Monitoreo integrado
- ✅ Muy escalable
- ✅ EB CLI compatible con Windows

**Desventajas:**
- ⚠️ Curva de aprendizaje de AWS
- ⚠️ Puede ser costoso

**Pasos para desplegar:**

1. **Instalar EB CLI (Windows PowerShell/CMD):**
   ```powershell
   # Windows PowerShell o CMD
   pip install awsebcli
   ```

2. **Inicializar aplicación (Windows PowerShell/CMD/Git Bash):**
   ```powershell
   # Windows PowerShell, CMD o Git Bash - todos funcionan igual
   eb init -p python-3.10 programacion-lineal
   eb create programacion-lineal-env
   eb deploy
   eb open
   ```

3. **Crear archivo `.ebextensions/python.config`:**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: application:app
   ```

**Costo:** Pagas por recursos EC2 utilizados (desde ~$10/mes)

---

### Solución 7: Google Cloud Run

> **✅ Funciona perfectamente desde Windows:** Google Cloud SDK está disponible para Windows.

**Ventajas:**
- ✅ Pago por uso (muy económico para tráfico bajo)
- ✅ Escalado automático a cero
- ✅ HTTPS automático
- ✅ Despliegue con Docker
- ✅ Google Cloud SDK compatible con Windows

**Desventajas:**
- ⚠️ Requiere crear Dockerfile
- ⚠️ Curva de aprendizaje

**Pasos para desplegar:**

1. **Crear `Dockerfile`:**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
   ```
   > **📝 Windows:** Este `CMD` se ejecutará dentro del contenedor Docker en el servidor Linux de Google Cloud. NO se ejecuta en tu Windows. Solo necesitas crear el archivo Dockerfile y subirlo.

2. **Instalar Google Cloud SDK (Windows):**
   - Descargar instalador: https://cloud.google.com/sdk/docs/install
   - O usar PowerShell:
     ```powershell
     (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
     & $env:Temp\GoogleCloudSDKInstaller.exe
     ```

3. **Desplegar (Windows PowerShell/CMD):**
   ```powershell
   # Windows PowerShell o CMD
   gcloud builds submit --tag gcr.io/tu-proyecto/programacion-lineal
   gcloud run deploy --image gcr.io/tu-proyecto/programacion-lineal --platform managed
   ```

**Costo:** $0.10 por millón de requests | Muy económico para tráfico bajo

---

### Solución 8: Microsoft Azure App Service

> **✅ Funciona perfectamente desde Windows:** Azure CLI está optimizado para Windows.

**Ventajas:**
- ✅ Integración con servicios Azure
- ✅ Escalado automático
- ✅ HTTPS automático
- ✅ Azure CLI nativo para Windows (MSI installer)

**Desventajas:**
- ⚠️ Curva de aprendizaje
- ⚠️ Puede ser costoso

**Pasos para desplegar:**

1. **Instalar Azure CLI (Windows):**
   ```powershell
   # Opción 1: Descargar MSI desde https://aka.ms/installazurecliwindows
   # Opción 2: Usar winget (Windows 10/11)
   winget install -e --id Microsoft.AzureCLI
   # Opción 3: Usar PowerShell (ejecutar como administrador)
   $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi
   ```

2. **Crear app service (Windows PowerShell/CMD):**
   ```powershell
   # Windows PowerShell o CMD
   az login
   az webapp up --name programacion-lineal --runtime "PYTHON:3.10" --sku F1
   ```

**Costo:** Plan gratuito disponible | Desde ~$10/mes para plan básico

---

## ⚙️ Configuración Avanzada

### Mejorar `app.py` para producción

```python
from flask import Flask, render_template, request, jsonify
from solver import MetodoGrafico, MetodoSimplex, convertir_restricciones_relacionales
import os

app = Flask(__name__)

# Configuración de producción
app.config['DEBUG'] = os.environ.get('FLASK_ENV') != 'production'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configurar CORS si es necesario
from flask_cors import CORS
CORS(app)  # Permitir peticiones desde otros dominios si es necesario

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de salud para monitoreo"""
    return jsonify({'status': 'healthy'}), 200

# ... resto de rutas ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Configurar Gunicorn para mejor rendimiento

> **⚠️ Windows:** Esta configuración es para el servidor Linux de producción. NO intentes ejecutar esto en Windows localmente.

Crear archivo `gunicorn_config.py`:

```python
# Número de workers = (2 x CPU cores) + 1
workers = 4
bind = "0.0.0.0:8000"
timeout = 120
keepalive = 5
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

Ejecutar en el servidor Linux (NO en Windows):
```bash
# Este comando se ejecuta en el servidor Linux de producción
gunicorn -c gunicorn_config.py app:app
```

> **📝 Windows:** Este archivo de configuración se usará en el servidor Linux remoto. En Windows, no necesitas ejecutar este comando.

---

## 📊 Monitoreo y Logging

### Opción 1: Logging básico con Python

Agregar a `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Programacion Lineal startup')
```

### Opción 2: Sentry para monitoreo de errores

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="tu-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Opción 3: Uptime monitoring

Servicios gratuitos:
- **UptimeRobot** (50 monitores gratis)
- **Pingdom** (1 monitor gratis)
- **StatusCake** (10 monitores gratis)

---

## 🔒 Consideraciones de Seguridad

### 1. Variables de entorno

Nunca hardcodees valores sensibles. Usa variables de entorno:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### 2. Rate limiting

Instalar Flask-Limiter:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/calcular', methods=['POST'])
@limiter.limit("10 per minute")
def calcular():
    # ...
```

### 3. HTTPS

Asegúrate de usar HTTPS en producción. La mayoría de plataformas lo configuran automáticamente.

### 4. Headers de seguridad

```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

---

## 📝 Comparación Rápida

| Plataforma | Facilidad | Costo | Escalabilidad | Recomendado para |
|------------|-----------|-------|---------------|------------------|
| **Render** | ⭐⭐⭐⭐⭐ | Gratis/$7+ | ⭐⭐⭐ | Inicio rápido |
| **Railway** | ⭐⭐⭐⭐⭐ | $5 crédito/mes | ⭐⭐⭐⭐ | Proyectos pequeños |
| **Heroku** | ⭐⭐⭐⭐ | $5+ | ⭐⭐⭐⭐ | Proyectos establecidos |
| **DigitalOcean App** | ⭐⭐⭐⭐ | $5+ | ⭐⭐⭐⭐ | Aplicaciones medianas |
| **VPS** | ⭐⭐ | $4+ | ⭐⭐⭐⭐⭐ | Control total |
| **AWS Beanstalk** | ⭐⭐⭐ | $10+ | ⭐⭐⭐⭐⭐ | Empresas |
| **Google Cloud Run** | ⭐⭐⭐ | $0.10/1M req | ⭐⭐⭐⭐⭐ | Tráfico variable |
| **Azure App Service** | ⭐⭐⭐ | $0/$10+ | ⭐⭐⭐⭐ | Ecosistema Azure |

---

## 🚀 Recomendación Inicial

### Para usuarios de Windows:

**Para comenzar rápido (recomendado):**
- ✅ **Render** - Solo navegador + Git (más fácil)
- ✅ **Railway** - Solo navegador + Git (muy simple)

**Si necesitas más control:**
- ✅ **Azure App Service** - Excelente integración con Windows
- ✅ **DigitalOcean App Platform** - Interfaz web completa

**Para proyectos avanzados:**
- ⚠️ **VPS** - Requiere SSH desde Windows (PowerShell/PuTTY/WSL2)
- ✅ **Google Cloud Run** - Requiere Google Cloud SDK (disponible para Windows)
- ✅ **AWS Elastic Beanstalk** - Requiere EB CLI (funciona en Windows)

> **💡 Consejo:** Si estás empezando desde Windows, comienza con **Render** o **Railway**. Son las opciones más simples y no requieren instalar nada más que Git.

---

## 📚 Recursos Adicionales

- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [12-Factor App](https://12factor.net/)

---

## ⚠️ Checklist Pre-Despliegue

- [ ] ✅ Crear `requirements.txt`
- [ ] ✅ Crear `Procfile` (si es necesario)
- [ ] ✅ Configurar variables de entorno
- [ ] ✅ Desactivar modo debug en producción
- [ ] ✅ Configurar logging
- [ ] ✅ Probar aplicación localmente:
  - **Windows:** Usar `python app.py` (servidor Flask dev) - Gunicorn NO funciona en Windows
  - **Linux/macOS:** Puedes usar `python app.py` o `gunicorn app:app` para pruebas locales
- [ ] ✅ Configurar dominio personalizado (opcional)
- [ ] ✅ Configurar SSL/HTTPS
- [ ] ✅ Configurar monitoreo
- [ ] ✅ Configurar backups (si aplica)

---

**Última actualización:** 2024

---

## 🔄 Resumen: Gunicorn y Windows - Lo que necesitas saber

### ✅ Lo que SÍ debes hacer (Windows):

1. **Incluir Gunicorn en `requirements.txt`** 
   - Se instalará automáticamente en el servidor Linux remoto
   - NO intentes instalarlo localmente en Windows

2. **Crear `Procfile` con comando Gunicorn**
   - Se ejecutará automáticamente en el servidor Linux remoto
   - NO intentes ejecutarlo localmente en Windows

3. **Probar localmente con Flask dev server**
   ```powershell
   python app.py
   ```

### ❌ Lo que NO debes hacer (Windows):

1. **NO intentes instalar Gunicorn en Windows** - No funcionará
2. **NO intentes ejecutar `gunicorn` desde Windows** - Dará error
3. **NO te preocupes** - Las plataformas de hosting ejecutan Gunicorn automáticamente en sus servidores Linux

### 🎯 Flujo típico desde Windows:

```
1. Desarrollo local (Windows)
   └─> python app.py (servidor Flask dev)
   
2. Git push a GitHub
   └─> git add . && git commit && git push
   
3. Plataforma hosting detecta cambios
   └─> Render/Railway/Heroku/etc. descarga código
   
4. Servidor Linux ejecuta automáticamente
   └─> pip install -r requirements.txt (incluye gunicorn)
   └─> gunicorn app:app (en servidor Linux)
   
5. Tu app está en línea ✅
```

**Todo funciona perfectamente desde Windows. Solo recuerda: Gunicorn corre en el servidor remoto, no en tu máquina.**

