# Calculadora de Programación Lineal

Una aplicación web interactiva para resolver problemas de Programación Lineal utilizando múltiples métodos: **Método Gráfico** (2 variables con visualización), **Método Simplex** y **Método de Dos Fases** (n variables). La aplicación calcula automáticamente la solución óptima, muestra el proceso paso a paso y proporciona visualizaciones interactivas.

## Características

- **Múltiples métodos de solución**:
  - **Método Gráfico**: Para problemas con 2 variables (visualización interactiva)
  - **Método Simplex**: Para problemas de n variables con restricciones ≤
  - **Método de Dos Fases**: Para problemas con restricciones ≥ o = (variables artificiales)
- Soporte para maximización y minimización
- Restricciones con operadores: ≤, ≥, =
- Cálculo automático de intersecciones y vértices factibles
- Visualización gráfica interactiva de la región factible (método gráfico)
- Tablas Simplex paso a paso (método Simplex y Dos Fases)
- Registro detallado del proceso de solución
- Interfaz web intuitiva y fácil de usar
- Desplegable en la nube (Render, Heroku, Docker)

## Requisitos

- Python 3.7 o superior
- Flask
- NumPy
- Gunicorn (para despliegue en producción)
- Navegador web moderno

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/programacion-lineal.git
cd programacion-lineal
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:
```
Flask>=2.0.0
numpy>=1.21.0
gunicorn>=20.1.0
```

## Uso

1. Inicia el servidor Flask:
```bash
python app.py
```

2. Abre tu navegador y navega a:
```
http://localhost:5000
```

3. Ingresa los datos del problema:
   - **Función Objetivo**: Selecciona si deseas maximizar o minimizar, e ingresa los coeficientes de x e y
   - **Restricciones**: Agrega las restricciones del problema (puedes agregar o eliminar restricciones)

4. Haz clic en **"CALCULAR SOLUCIÓN"** para obtener:
   - La solución óptima (punto y valor de Z)
   - Visualización gráfica de la región factible
   - Registro paso a paso del proceso

## Estructura del Proyecto

```
programacion-lineal/
├── app.py                    # Aplicación Flask (backend)
├── solver.py                 # Clase Solver principal (orquestador)
├── metodo_grafico.py         # Implementación del Método Gráfico
├── metodo_simplex.py         # Implementación del Método Simplex
├── metodo_dos_fases.py       # Implementación del Método de Dos Fases
│
├── templates/
│   └── index.html            # Interfaz web (frontend)
│
├── static/
│   ├── css/
│   │   └── style.css         # Estilos de la aplicación
│   └── js/
│       └── main.js           # Lógica JavaScript del frontend
│
├── docs/                     # Documentación del proyecto
│   ├── 01_REQUISITOS.md      # Requisitos del MVP
│   ├── 02_ARQUITECTURA.md    # Funcionamiento de los métodos
│   ├── 03_DESPLIEGUE.md      # Guía de despliegue
│   ├── 04_EJERCICIOS.md      # Ejercicios de prueba
│   └── 05_DESARROLLO.md      # Historial y mejoras pendientes
│
├── tests/                    # Pruebas del proyecto
│   ├── test_completo.py      # Suite completa de pruebas
│   ├── test_validacion.py    # Pruebas de validación
│   ├── test_ejercicios.py    # Pruebas de ejercicios específicos
│   └── README.md             # Documentación de pruebas
│
├── Dockerfile                # Configuración de Docker
├── Procfile                  # Configuración para Render/Heroku
├── runtime.txt               # Versión de Python para despliegue
├── requirements.txt          # Dependencias de producción
├── requirements_test.txt     # Dependencias de pruebas
├── .gitignore                # Archivos ignorados por Git
└── README.md                 # Este archivo
```

## Tecnologías Utilizadas

- **Backend**: Python, Flask, Gunicorn
- **Cálculos Matemáticos**: NumPy
- **Frontend**: HTML, CSS, JavaScript
- **Visualización**: Plotly.js
- **Despliegue**: Docker, Render/Heroku

## Ejemplo de Uso

### Problema de Ejemplo:

**Maximizar**: Z = 3x + 2y

**Sujeto a**:
- 2x + y ≤ 10
- x + y ≤ 8
- y ≤ 8
- x ≥ 0, y ≥ 0

### Solución:

La aplicación calculará automáticamente:
- Los puntos de intersección de las restricciones
- Los vértices de la región factible
- El valor óptimo de Z en cada vértice
- El punto óptimo y su valor correspondiente

## Cómo Funciona

### Método Gráfico (2 variables)
1. **Cálculo de Intersecciones**: Resuelve sistemas de ecuaciones 2x2 para encontrar puntos de intersección.
2. **Filtrado de Región Factible**: Verifica cada punto contra todas las restricciones.
3. **Evaluación de Vértices**: Calcula Z en cada vértice factible.
4. **Optimización**: Identifica el vértice óptimo.
5. **Visualización**: Genera gráfico interactivo con Plotly.js.

### Método Simplex (n variables, restricciones ≤)
1. **Forma Estándar**: Convierte el problema a forma estándar con variables de holgura.
2. **Tabla Simplex**: Construye la tabla inicial.
3. **Iteraciones**: Aplica el algoritmo Simplex hasta encontrar la solución óptima.
4. **Registro de Pasos**: Muestra cada tabla intermedia.

### Método de Dos Fases (restricciones ≥ o =)
1. **Fase I**: Minimiza la suma de variables artificiales para encontrar una solución básica factible.
2. **Fase II**: Optimiza la función objetivo original desde la solución de Fase I.
3. **Detección de Casos Especiales**: Identifica soluciones no acotadas o regiones infactibles.

## Notas

- El **Método Gráfico** está diseñado para problemas con exactamente 2 variables.
- El **Método Simplex** y **Dos Fases** soportan n variables.
- Se asume que las variables son no negativas (x ≥ 0, y ≥ 0, ...).
- Los cálculos utilizan tolerancias numéricas para manejar errores de punto flotante.
- La aplicación detecta automáticamente casos especiales (solución no acotada, región infactible).

## Despliegue

La aplicación está preparada para desplegarse en servicios de hosting como Render o Heroku:

```bash
# Con Docker
docker build -t programacion-lineal .
docker run -p 5000:5000 programacion-lineal

# Con Gunicorn (producción)
gunicorn app:app --bind 0.0.0.0:5000
```

Consulta `docs/03_DESPLIEGUE.md` para instrucciones detalladas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Autor

William Flores - [@williamfloress](https://github.com/williamfloress)

## Agradecimientos

- NumPy por las herramientas de cálculo matemático
- Plotly.js por la visualización interactiva
- Flask por el framework web ligero y flexible

