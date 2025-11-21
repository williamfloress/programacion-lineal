# Guía de Desarrollo: Calculadora de Programación Lineal (Método Gráfico)

## 1. Descripción del Proyecto
Desarrollo de una aplicación web escalable para resolver problemas de Programación Lineal (2 variables) mediante el método gráfico. El sistema debe calcular vértices, definir la región factible, evaluar la función objetivo y clasificar el tipo de solución (Única, Infinita, No acotada, No factible), mostrando los resultados analíticos y visuales.

---

## 2. Stack Tecnológico Recomendado
Para garantizar escalabilidad y facilidad de cálculo matemático:

* **Backend:** Python (FastAPI o Flask).
    * *Razón:* Manejo nativo de matrices (`NumPy`) y fácil implementación futura del Simplex (`SciPy`).
* **Frontend:** React.js (o Vue.js).
* **Gráficos:** Plotly.js (Librería robusta para gráficos científicos interactivos).
* **Intercambio de datos:** JSON (REST API).

---

## 3. Fase 1: Lógica Matemática (Backend)

El núcleo del sistema. Se debe crear una clase `LinearSolver` que maneje la lógica.

### Paso 3.1: Estandarización de Datos
Convertir las entradas del usuario en una estructura matricial estándar.
* Formato de restricción: $ax + by \leq c$
* Almacenamiento: Lista de diccionarios o Tuplas `[(a, b, c, operador), ...]`.

### Paso 3.2: Cálculo de Intersecciones
1.  Identificar todas las líneas frontera (incluyendo ejes $x=0, y=0$).
2.  Resolver sistemas de ecuaciones 2x2 para cada par de líneas combinables.
3.  **Fórmula:** Para líneas $a_1x + b_1y = c_1$ y $a_2x + b_2y = c_2$.
    $$x = \frac{c_1b_2 - c_2b_1}{a_1b_2 - a_2b_1}, \quad y = \frac{a_1c_2 - a_2c_1}{a_1b_2 - a_2b_1}$$
4.  Manejar excepciones (líneas paralelas = división por cero).

### Paso 3.3: Filtrado de Región Factible
1.  Tomar cada punto de intersección calculado $(x, y)$.
2.  Verificar si $(x, y)$ cumple con **TODAS** las restricciones originales.
3.  Si cumple, agregarlo a la lista de `vertices_factibles`.

### Paso 3.4: Evaluación y Clasificación
Evaluar la Función Objetivo $Z = c_1x + c_2y$ en cada vértice factible.

| Tipo de Solución | Condición Lógica |
| :--- | :--- |
| **Única** | Un solo vértice tiene el valor máximo (o mínimo) estricto. |
| **Infinita** | Dos vértices adyacentes tienen el mismo valor óptimo (Z). |
| **No Factible** | La lista de `vertices_factibles` está vacía. |
| **No Acotada** | La región factible no está cerrada en la dirección de mejora de Z (requiere verificar si el polígono es cerrado). |

---

## 4. Fase 2: Diseño de la API (Interacción)

Definir los endpoints para separar la lógica de la vista.

### Endpoint: `POST /solve/graphical`
**Request body (JSON):**
```json
{
  "objective": { "c1": 3, "c2": 2, "goal": "maximize" },
  "constraints": [
    { "a": 2, "b": 1, "op": "<=", "c": 10 },
    { "a": 1, "b": 1, "op": "<=", "c": 8 }
  ]
}