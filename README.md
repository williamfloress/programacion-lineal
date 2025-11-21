# Calculadora de Programación Lineal - Método Gráfico

Una aplicación web interactiva para resolver problemas de Programación Lineal con 2 variables utilizando el método gráfico. La aplicación calcula automáticamente los vértices de la región factible, evalúa la función objetivo y proporciona una visualización gráfica interactiva de la solución.

## 🚀 Características

- ✅ Resolución de problemas de Programación Lineal con 2 variables (x, y)
- ✅ Soporte para maximización y minimización
- ✅ Restricciones con operadores: ≤, ≥, =
- ✅ Cálculo automático de intersecciones y vértices factibles
- ✅ Visualización gráfica interactiva de la región factible
- ✅ Registro paso a paso del proceso de solución
- ✅ Interfaz web intuitiva y fácil de usar

## 📋 Requisitos

- Python 3.7 o superior
- Flask
- NumPy
- Navegador web moderno

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/programacion-lineal.git
cd programacion-lineal
```

2. Instala las dependencias:
```bash
pip install flask numpy
```

O crea un archivo `requirements.txt` con:
```
Flask>=2.0.0
numpy>=1.21.0
```

Y luego ejecuta:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

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

## 📁 Estructura del Proyecto

```
programacion-lineal/
├── app.py                 # Aplicación Flask (backend)
├── solver.py             # Clase MetodoGrafico (lógica matemática)
├── templates/
│   └── index.html        # Interfaz web (frontend)
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Flask
- **Cálculos Matemáticos**: NumPy
- **Frontend**: HTML, CSS, JavaScript
- **Visualización**: Plotly.js

## 📖 Ejemplo de Uso

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

## 🔍 Cómo Funciona

1. **Cálculo de Intersecciones**: El sistema resuelve sistemas de ecuaciones 2x2 para encontrar todos los puntos de intersección entre las restricciones y los ejes coordenados.

2. **Filtrado de Región Factible**: Se verifica cada punto de intersección contra todas las restricciones para determinar si pertenece a la región factible.

3. **Evaluación de Vértices**: Se calcula el valor de la función objetivo (Z) en cada vértice factible.

4. **Optimización**: Se identifica el vértice que maximiza o minimiza Z según el objetivo seleccionado.

5. **Visualización**: Se genera un gráfico interactivo mostrando las restricciones, la región factible y el punto óptimo.

## 📝 Notas

- La aplicación está diseñada para problemas con exactamente 2 variables.
- Se asume que las variables son no negativas (x ≥ 0, y ≥ 0).
- Los cálculos utilizan tolerancias numéricas para manejar errores de punto flotante.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 👤 Autor

Tu nombre - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- NumPy por las herramientas de cálculo matemático
- Plotly.js por la visualización interactiva
- Flask por el framework web ligero y flexible

