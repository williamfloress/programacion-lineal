# ✅ Checklist: Despliegue en Render - Paso a Paso

Este checklist te guiará paso a paso para desplegar tu aplicación de Programación Lineal en Render.

---

## 📋 Preparación Local

### Paso 1: Verificar archivos necesarios

- [ ] **Verificar que existe `requirements.txt`**
  ```bash
  # Debe contener:
  Flask>=2.0.0
  numpy>=1.21.0
  gunicorn>=20.1.0
  ```

- [ ] **Verificar que existe `Procfile`**
  ```bash
  # Debe contener:
  web: gunicorn app:app --bind 0.0.0.0:$PORT
  ```

- [ ] **Verificar que `app.py` está configurado para producción**
  ```python
  # El archivo debe tener al final algo como:
  if __name__ == '__main__':
      import os
      port = int(os.environ.get('PORT', 5000))
      debug = os.environ.get('FLASK_ENV') != 'production'
      app.run(host='0.0.0.0', port=port, debug=debug)
  ```

### Paso 2: Probar la aplicación localmente con Gunicorn

> **⚠️ Nota importante para Windows:**
> Gunicorn NO funciona en Windows (requiere módulos Unix como `fcntl`). Esto es **normal y esperado**.
> Puedes saltar este paso si estás en Windows, ya que Gunicorn funcionará correctamente en Render (que usa Linux).
> Para probar localmente en Windows, usa el servidor de desarrollo de Flask (ver alternativa abajo).

- [ ] **Instalar Gunicorn localmente (opcional, solo para Linux/macOS)**
  ```bash
  pip install gunicorn
  ```

- [ ] **Probar que funciona con Gunicorn (solo Linux/macOS)**
  ```bashimage.png
  # Desde el directorio del proyecto
  gunicorn app:app --bind 0.0.0.0:5000
  ```
  
- [ ] **Alternativa para Windows - Probar con Flask (servidor de desarrollo)**
  ```bash
  # Usar el servidor de desarrollo de Flask para pruebas locales
  python app.py
  # O simplemente: flask run
  ```
  
- [ ] **Abrir en navegador**: http://localhost:5000
  
- [ ] **Verificar que la aplicación carga correctamente**
  
- [ ] **Probar que el cálculo funciona** (ingresar datos y calcular)

**✅ Resumen Paso 2:**
- ✅ Si estás en **Windows**: Puedes usar `python app.py` para probar localmente. Gunicorn funcionará en Render.
- ✅ Si estás en **Linux/macOS**: Puedes probar con Gunicorn localmente para simular el entorno de producción.

---

## 📦 Preparar Repositorio Git

### Paso 3: Inicializar Git (si no está inicializado)

- [ ] **Verificar si ya hay un repositorio Git**
  ```bash
  git status
  ```
  
  Si dice "not a git repository", ejecutar:
  ```bash
  git init
  ```

### Paso 4: Crear archivo `.gitignore` (si no existe)

- [ ] **Verificar que `.gitignore` existe y contiene:**
  ```
  __pycache__/
  *.pyc
  venv/
  env/
  .env
  *.log
  ```

### Paso 5: Commit de los archivos

- [ ] **Agregar todos los archivos al staging**
  ```bash
  git add .
  ```

- [ ] **Hacer commit**
  ```bash
  git commit -m "Preparar aplicación para despliegue en Render"
  ```

---

## 🌐 Crear Cuenta y Repositorio en GitHub/GitLab

### Paso 6: Subir código a GitHub o GitLab

**Opción A: Si NO tienes repositorio remoto todavía**

- [ ] **Crear repositorio en GitHub**
  1. Ve a https://github.com/new
  2. Nombre: `programacion-lineal` (o el que prefieras)
  3. Descripción: "Calculadora de Programación Lineal"
  4. Selecciona **Public** o **Private**
  5. **NO marques** "Initialize with README" (ya tienes archivos)
  6. Click **"Create repository"**

- [ ] **Conectar repositorio local con GitHub**
  ```bash
  git remote add origin https://github.com/TU-USUARIO/programacion-lineal.git
  git branch -M main
  git push -u origin main
  ```

**Opción B: Si YA tienes repositorio remoto**

- [ ] **Verificar el remote**
  ```bash
  git remote -v
  ```

- [ ] **Push de los cambios**
  ```bash
  git push origin main
  # o
  git push origin master
  ```

---

## 🚀 Configurar Render

### Paso 7: Crear cuenta en Render

- [ ] **Ir a Render.com**
  - URL: https://render.com
  
- [ ] **Crear cuenta**
  - Opción 1: Click en "Get Started for Free"
  - Opción 2: "Sign Up" → Conectar con GitHub (recomendado)
  
- [ ] **Verificar email** (si es necesario)

### Paso 8: Conectar cuenta de GitHub/GitLab con Render

- [ ] **En Render Dashboard**
  - Click en tu nombre/avatar (arriba derecha)
  - Ve a "Account Settings"
  - En la sección "Connected Accounts", click "Connect" en GitHub/GitLab
  - Autorizar acceso a tus repositorios

### Paso 9: Crear nuevo Web Service

- [ ] **En el Dashboard de Render**
  - Click en el botón azul **"New +"** (arriba derecha)
  - Seleccionar **"Web Service"**

### Paso 10: Conectar repositorio

- [ ] **Seleccionar repositorio**
  - Deberías ver una lista de tus repositorios
  - Buscar y seleccionar `programacion-lineal` (o el nombre que usaste)
  
- [ ] **Click en "Connect"**

### Paso 11: Configurar el servicio

**Configuración básica:**

- [ ] **Name**: 
  - Escribir: `programacion-lineal` (o el nombre que prefieras)
  - Este será parte de la URL: `programacion-lineal.onrender.com`

- [ ] **Region**: 
  - Seleccionar la más cercana (ej: `Oregon (US West)` para Latinoamérica)

- [ ] **Branch**: 
  - Dejar en `main` (o `master` si tu branch principal es master)

- [ ] **Root Directory**: 
  - Dejar vacío (si todos los archivos están en la raíz)

- [ ] **Runtime**: 
  - Seleccionar `Python 3`

**Configuración de Build:**

- [ ] **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Start Command**:
  ```bash
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

**Configuración de Plan:**

- [ ] **Plan**: 
  - Seleccionar **Free** (para comenzar)
  - O seleccionar **Starter ($7/mes)** si quieres sin límites de inactividad

**Configuración Avanzada (opcional):**

- [ ] **Environment Variables** (click en "Advanced"):
  
  - [ ] Agregar variable:
    - **Key**: `FLASK_ENV`
    - **Value**: `production`
    
  - [ ] Agregar variable (opcional):
    - **Key**: `PYTHON_VERSION`
    - **Value**: `3.10.0`

### Paso 12: Crear el servicio

- [ ] **Revisar toda la configuración**
  
- [ ] **Click en "Create Web Service"**

---

## ⏳ Esperar el despliegue

### Paso 13: Monitorear el proceso de despliegue

- [ ] **Ver el log de build**
  - Render comenzará a construir tu aplicación
  - Verás mensajes como:
    ```
    ==> Cloning from https://github.com/...
    ==> Checking out commit abc123...
    ==> Running: pip install -r requirements.txt
    ==> Running: gunicorn app:app --bind 0.0.0.0:$PORT
    ```

- [ ] **Esperar a que termine el build**
  - Típicamente toma 2-5 minutos
  - Verás "Build successful" cuando termine

- [ ] **Esperar a que el servicio inicie**
  - Después del build, el servicio se inicia
  - Verás "Your service is live" cuando esté listo

---

## ✅ Verificar el despliegue

### Paso 14: Probar la aplicación

- [ ] **Abrir la URL de tu aplicación**
  - Render te dará una URL como: `https://programacion-lineal.onrender.com`
  - Click en la URL o copiarla y abrirla en navegador

- [ ] **Verificar que carga la página principal**
  - Deberías ver la interfaz de la calculadora

- [ ] **Probar funcionalidad básica:**
  - [ ] Ingresar datos en la función objetivo
  - [ ] Agregar una restricción
  - [ ] Click en "CALCULAR SOLUCIÓN"
  - [ ] Verificar que muestra resultados correctamente

- [ ] **Probar ambos métodos (Gráfico y Simplex)**
  - [ ] Cambiar entre tabs
  - [ ] Verificar que ambos funcionan

### Paso 15: Verificar logs (si hay problemas)

- [ ] **Si algo no funciona, revisar logs:**
  - En Render Dashboard → Tu servicio → Pestaña "Logs"
  - Buscar errores en rojo
  
- [ ] **Errores comunes y soluciones:**
  - ❌ "Module not found": Verificar que `requirements.txt` tiene todas las dependencias
  - ❌ "Port already in use": Verificar que usas `$PORT` en el comando
  - ❌ "Application failed to respond": Verificar que el Start Command es correcto

---

## 🔧 Configuración adicional (opcional)

### Paso 16: Configurar dominio personalizado (opcional)

- [ ] **Si tienes un dominio propio:**
  - En Render Dashboard → Tu servicio → Settings
  - Scroll hasta "Custom Domains"
  - Click "Add Custom Domain"
  - Seguir instrucciones para configurar DNS

### Paso 17: Configurar variables de entorno adicionales (si es necesario)

- [ ] **Si necesitas más configuración:**
  - Settings → Environment
  - Agregar variables necesarias
  - Hacer "Manual Deploy" para aplicar cambios

### Paso 18: Configurar auto-despliegue (ya viene habilitado por defecto)

- [ ] **Verificar que Auto-Deploy está activado:**
  - Settings → Build & Deploy
  - "Auto-Deploy" debe estar en "Yes"
  - Esto hará que cada push a GitHub actualice automáticamente la app

---

## 🎉 ¡Listo!

### Paso 19: Compartir tu aplicación

- [ ] **Tu aplicación está en línea:**
  - URL: `https://programacion-lineal.onrender.com` (o tu dominio personalizado)
  - Puedes compartirla con otros usuarios

- [ ] **Notas importantes:**
  - ⚠️ En el plan **Free**, la app se "duerme" después de 15 minutos de inactividad
  - ⚠️ El primer acceso después de dormirse puede tardar 30-60 segundos
  - 💡 Para evitar que se duerma, considera el plan Starter ($7/mes)

---

## 📝 Comandos útiles para el futuro

### Actualizar la aplicación

```bash
# 1. Hacer cambios en tu código local
# 2. Commit y push
git add .
git commit -m "Descripción de cambios"
git push origin main

# 3. Render detectará el cambio y desplegará automáticamente
```

### Ver logs en tiempo real

- En Render Dashboard → Tu servicio → Pestaña "Logs"
- Click en "Follow" para ver logs en tiempo real

### Reiniciar el servicio manualmente

- En Render Dashboard → Tu servicio → Botón "Manual Deploy" → "Clear build cache & deploy"

### Detener el servicio

- Settings → Danger Zone → "Suspend Service"

---

## 🆘 Solución de Problemas Comunes

### Problema: La aplicación no carga

**Solución:**
- [ ] Verificar logs en Render
- [ ] Verificar que `Procfile` tiene el comando correcto
- [ ] Verificar que `app.py` está en la raíz del proyecto

### Problema: Error "Module not found"

**Solución:**
- [ ] Verificar que todas las dependencias están en `requirements.txt`
- [ ] Agregar la dependencia faltante
- [ ] Hacer commit y push

### Problema: La app se duerme frecuentemente

**Solución:**
- [ ] Actualizar al plan Starter ($7/mes)
- [ ] O configurar un servicio de ping externo (UptimeRobot gratuito)

### Problema: Error en el cálculo

**Solución:**
- [ ] Verificar logs para ver errores específicos
- [ ] Probar localmente primero
- [ ] Verificar que NumPy se instaló correctamente

---

## ✅ Resumen Final

**Archivos necesarios:**
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `app.py` configurado para producción
- ✅ Código en GitHub/GitLab

**Pasos principales:**
1. ✅ Preparar archivos localmente
2. ✅ Subir a GitHub
3. ✅ Crear cuenta en Render
4. ✅ Conectar repositorio
5. ✅ Configurar servicio
6. ✅ ¡Desplegar!

**Tu aplicación estará disponible en:**
`https://programacion-lineal.onrender.com` (o el nombre que elegiste)

---

**¿Necesitas ayuda?** Revisa los logs en Render o consulta la documentación: https://render.com/docs

