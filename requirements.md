# Requisitos MVP: Calculadora de Programación Lineal (Método Gráfico)

## Objetivo del MVP
Desarrollar una aplicación web funcional que resuelva problemas de Programación Lineal con 2 variables usando el método gráfico, mostrando resultados analíticos y visuales.

---

## 1. Alcance del MVP

### Incluido en MVP
- ✅ Resolución de problemas con 2 variables (x, y)
- ✅ Soporte para restricciones: ≤, ≥, =
- ✅ Cálculo de vértices de la región factible
- ✅ Evaluación de función objetivo (maximizar/minimizar)
- ✅ Clasificación de tipo de solución (Única, Infinita, No factible, No acotada)
- ✅ Visualización gráfica de la región factible
- ✅ Interfaz web básica funcional

### Excluido del MVP (Futuras versiones)
- ❌ Más de 2 variables
- ❌ Método Simplex
- ❌ Guardado de problemas
- ❌ Historial de soluciones
- ❌ Autenticación de usuarios

---

## 2. Requisitos Funcionales

### RF-1: Entrada de Datos
**Prioridad: ALTA**

El sistema debe permitir al usuario ingresar:
- **Función Objetivo:**
  - Coeficiente de x (c1)
  - Coeficiente de y (c2)
  - Objetivo: maximizar o minimizar

- **Restricciones:**
  - Coeficiente a (de x)
  - Coeficiente b (de y)
  - Operador: ≤, ≥, o =
  - Valor c (lado derecho)
  - Mínimo 1 restricción, máximo 10 restricciones

**Validaciones:**
- Todos los campos numéricos deben ser válidos (números reales)
- Al menos 1 restricción es obligatoria
- Los coeficientes a y b no pueden ser ambos cero en una restricción

### RF-2: Procesamiento Matemático
**Prioridad: ALTA**

El backend debe:

1. **Estandarizar restricciones:**
   - Convertir todas las restricciones a formato estándar: ax + by ≤ c
   - Manejar restricciones ≥ (multiplicar por -1)
   - Manejar restricciones = (convertir a dos restricciones: ≤ y ≥)

2. **Calcular intersecciones:**
   - Identificar todas las líneas frontera (restricciones + ejes x=0, y=0)
   - Resolver sistemas de ecuaciones 2x2 para cada par de líneas
   - Manejar casos especiales:
     - Líneas paralelas (sin intersección)
     - División por cero
     - Líneas idénticas

3. **Filtrar región factible:**
   - Verificar cada punto de intersección contra TODAS las restricciones
   - Incluir solo puntos que satisfacen todas las restricciones
   - Considerar restricciones de no negatividad (x ≥ 0, y ≥ 0) si aplican

4. **Evaluar función objetivo:**
   - Calcular Z = c1*x + c2*y para cada vértice factible
   - Identificar vértice(s) óptimo(s) según objetivo (max/min)

5. **Clasificar solución:**
   - **Única:** Un solo vértice tiene el valor óptimo estricto
   - **Infinita:** Dos o más vértices adyacentes tienen el mismo valor óptimo
   - **No Factible:** No hay vértices factibles
   - **No Acotada:** La región factible no está cerrada en dirección de mejora

### RF-3: Visualización Gráfica
**Prioridad: ALTA**

El frontend debe mostrar:

1. **Gráfico 2D interactivo:**
   - Ejes X e Y con etiquetas
   - Líneas de restricción con colores distintos
   - Región factible sombreada
   - Vértices factibles marcados
   - Vértice(s) óptimo(s) destacado(s) con color diferente

2. **Información del gráfico:**
   - Leyenda identificando cada restricción
   - Coordenadas de vértices al hacer hover
   - Zoom y pan para mejor visualización

### RF-4: Resultados Analíticos
**Prioridad: ALTA**

El sistema debe mostrar:

1. **Resumen de solución:**
   - Tipo de solución (Única, Infinita, No factible, No acotada)
   - Valor óptimo de Z (si existe)
   - Coordenadas del(los) punto(s) óptimo(s)

2. **Detalles:**
   - Lista de todos los vértices factibles con sus coordenadas
   - Valor de Z en cada vértice
   - Tabla de restricciones activas en el óptimo

### RF-5: Manejo de Errores
**Prioridad: MEDIA**

El sistema debe manejar y mostrar mensajes claros para:
- Entradas inválidas
- Problemas sin solución factible
- Problemas no acotados
- Errores de cálculo (divisiones por cero, etc.)
- Errores de conexión entre frontend y backend

---

## 3. Requisitos Técnicos

### RT-1: Arquitectura
- **Backend:** Python con FastAPI o Flask
- **Frontend:** React.js o Vue.js
- **Bibliotecas matemáticas:** NumPy para cálculos
- **Gráficos:** Plotly.js para visualización
- **Comunicación:** REST API con JSON

### RT-2: Estructura del Proyecto
```
programacion-lineal/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI/Flask app
│   │   ├── models.py        # Pydantic models
│   │   ├── solver.py        # LinearSolver class
│   │   └── utils.py         # Funciones auxiliares
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputForm.jsx
│   │   │   ├── Results.jsx
│   │   │   └── Graph.jsx
│   │   ├── App.jsx
│   │   └── api.js           # Cliente API
│   ├── package.json
│   └── README.md
└── README.md
```

### RT-3: API Endpoints

#### POST /solve/graphical
**Descripción:** Resuelve un problema de programación lineal

**Request Body:**
```json
{
  "objective": {
    "c1": 3,
    "c2": 2,
    "goal": "maximize"
  },
  "constraints": [
    { "a": 2, "b": 1, "op": "<=", "c": 10 },
    { "a": 1, "b": 1, "op": "<=", "c": 8 },
    { "a": 1, "b": 0, "op": ">=", "c": 0 },
    { "a": 0, "b": 1, "op": ">=", "c": 0 }
  ]
}
```

**Response (Éxito):**
```json
{
  "status": "success",
  "solution_type": "unique",
  "optimal_value": 26.0,
  "optimal_points": [
    { "x": 2.0, "y": 6.0 }
  ],
  "feasible_vertices": [
    { "x": 0.0, "y": 0.0, "z": 0.0 },
    { "x": 5.0, "y": 0.0, "z": 15.0 },
    { "x": 2.0, "y": 6.0, "z": 26.0 },
    { "x": 0.0, "y": 8.0, "z": 16.0 }
  ],
  "constraints": [
    { "a": 2, "b": 1, "op": "<=", "c": 10, "active": true },
    { "a": 1, "b": 1, "op": "<=", "c": 8, "active": true }
  ],
  "plot_data": {
    "constraint_lines": [...],
    "feasible_region": [...],
    "optimal_points": [...]
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "No feasible solution exists",
  "error_type": "infeasible"
}
```

#### GET /health
**Descripción:** Verifica que el servidor esté funcionando

**Response:**
```json
{
  "status": "ok"
}
```

### RT-4: Clase LinearSolver

La clase debe tener los siguientes métodos:

```python
class LinearSolver:
    def __init__(self, objective, constraints):
        """Inicializa el solver con función objetivo y restricciones"""
        
    def standardize_constraints(self):
        """Convierte todas las restricciones a formato estándar"""
        
    def calculate_intersections(self):
        """Calcula todas las intersecciones entre líneas"""
        
    def filter_feasible_vertices(self):
        """Filtra vértices que satisfacen todas las restricciones"""
        
    def evaluate_objective(self):
        """Evalúa la función objetivo en cada vértice"""
        
    def classify_solution(self):
        """Clasifica el tipo de solución"""
        
    def solve(self):
        """Método principal que ejecuta todo el proceso"""
```

---

## 4. Requisitos de Interfaz de Usuario

### UI-1: Formulario de Entrada
- Campos claramente etiquetados
- Botón para agregar/eliminar restricciones dinámicamente
- Validación en tiempo real de campos
- Botón "Resolver" prominente
- Botón "Limpiar" para resetear el formulario

### UI-2: Área de Resultados
- Sección visible para mostrar resultados
- Formato claro y legible
- Tabla de vértices factibles
- Destacar solución óptima

### UI-3: Área de Gráfico
- Gráfico responsivo que se adapte al tamaño de pantalla
- Controles de zoom y pan
- Tooltips informativos al pasar el mouse
- Leyenda clara

### UI-4: Estados de la Aplicación
- Estado de carga mientras se procesa
- Mensajes de error claros y accionables
- Estado vacío cuando no hay datos

---

## 5. Requisitos de Calidad

### Q-1: Precisión Numérica
- Usar tolerancia numérica adecuada (1e-9) para comparaciones
- Manejar errores de punto flotante
- Redondear resultados a 2-4 decimales para presentación

### Q-2: Rendimiento
- Resolver problemas con hasta 10 restricciones en < 1 segundo
- Gráfico debe renderizarse en < 500ms

### Q-3: Usabilidad
- Interfaz intuitiva sin necesidad de documentación
- Mensajes de error claros y útiles
- Feedback visual inmediato

---

## 6. Criterios de Aceptación del MVP

El MVP se considerará completo cuando:

1. ✅ El usuario puede ingresar un problema de PL con 2 variables
2. ✅ El sistema calcula correctamente los vértices factibles
3. ✅ El sistema identifica correctamente el tipo de solución
4. ✅ El sistema muestra un gráfico con la región factible
5. ✅ El sistema muestra los resultados analíticos correctos
6. ✅ El sistema maneja casos especiales (no factible, no acotado)
7. ✅ La interfaz es funcional y usable
8. ✅ El sistema funciona end-to-end sin errores críticos

---

## 7. Casos de Prueba Esenciales

### CP-1: Solución Única
**Entrada:**
- Objetivo: Maximizar Z = 3x + 2y
- Restricciones:
  - 2x + y ≤ 10
  - x + y ≤ 8
  - x ≥ 0, y ≥ 0

**Resultado Esperado:** Solución única en (2, 6) con Z = 18

### CP-2: Solución Infinita
**Entrada:**
- Objetivo: Maximizar Z = x + y
- Restricciones:
  - x + y ≤ 10
  - x ≥ 0, y ≥ 0

**Resultado Esperado:** Solución infinita (múltiples puntos óptimos)

### CP-3: No Factible
**Entrada:**
- Objetivo: Maximizar Z = x + y
- Restricciones:
  - x + y ≤ 5
  - x + y ≥ 10
  - x ≥ 0, y ≥ 0

**Resultado Esperado:** "No Factible"

### CP-4: No Acotado
**Entrada:**
- Objetivo: Maximizar Z = x + y
- Restricciones:
  - x - y ≤ 5
  - x ≥ 0, y ≥ 0

**Resultado Esperado:** "No Acotado"

---

## 8. Plan de Implementación Sugerido

### Sprint 1: Backend Core
- Implementar clase LinearSolver
- Implementar cálculo de intersecciones
- Implementar filtrado de región factible
- Implementar evaluación y clasificación

### Sprint 2: API y Frontend Base
- Crear endpoints de API
- Crear formulario de entrada
- Integrar frontend con backend

### Sprint 3: Visualización y Pulido
- Implementar gráfico con Plotly.js
- Mejorar UI/UX
- Manejo de errores
- Testing y corrección de bugs

---

## 9. Dependencias Técnicas

### Backend
```
fastapi>=0.104.0
uvicorn>=0.24.0
numpy>=1.24.0
pydantic>=2.0.0
```

### Frontend
```
react>=18.0.0
react-dom>=18.0.0
plotly.js>=2.26.0
axios>=1.5.0
```

---

## 10. Notas de Implementación

### Consideraciones Importantes:
1. **Restricciones de no negatividad:** Por defecto, asumir x ≥ 0, y ≥ 0 a menos que se especifique lo contrario
2. **Precisión numérica:** Usar `numpy.isclose()` para comparaciones de punto flotante
3. **Detección de no acotado:** Verificar si la región factible está cerrada y si el vector gradiente puede extenderse infinitamente
4. **Orden de vértices:** Para visualización, ordenar vértices en sentido horario/antihorario para dibujar el polígono correctamente

---

**Versión:** 1.0  
**Fecha:** 2024  
**Estado:** MVP Requirements

