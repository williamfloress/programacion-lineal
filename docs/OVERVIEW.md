# Resumen del Proyecto - Calculadora de Programación Lineal

Guía breve para entender cómo funciona este proyecto al descargar el repositorio.

---

## ¿Qué es?

Una **aplicación web** que resuelve problemas de Programación Lineal (optimización) usando tres métodos diferentes. Permite definir una función objetivo (maximizar o minimizar) y restricciones, y obtiene la solución óptima con el proceso detallado.

---

## ¿Cómo funciona?

1. **Entrada**: El usuario define la función objetivo (Z) y las restricciones desde la interfaz web.
2. **Backend (Python/Flask)**: Recibe los datos, los pasa al método correspondiente y devuelve la solución.
3. **Salida**: Muestra la solución óptima, tablas iterativas (Simplex/Dos Fases) o gráfica interactiva (Gráfico).

---

## Métodos de resolución

| Método | Cuándo usarlo | Salida principal |
|--------|---------------|------------------|
| **Método Gráfico** | Problemas con 2 variables (X, Y) | Gráfica de la región factible, tabla de vértices |
| **Método Simplex** | n variables, restricciones ≤ | Tablas Simplex iteración a iteración |
| **Método de Dos Fases** | Restricciones ≥ o = | Tablas Fase 1 y Fase 2 |

---

## Detalles destacados por método

### Método Gráfico
- Calcula intersecciones entre rectas y filtra los vértices factibles.
- Evalúa Z en cada vértice y encuentra el óptimo.
- Visualiza la región factible con Plotly.js.
- Detecta: solución única, múltiple, no factible, degenerada.

### Método Simplex
- Convierte restricciones ≤ a igualdades con variables de holgura.
- Usa Big M cuando hay restricciones ≥ o = (variables artificiales).
- Muestra variable entrante, saliente, elemento pivote y ratios.
- Soporta maximización y minimización.

### Método de Dos Fases
- **Fase 1**: Minimiza la suma de variables artificiales hasta W = 0 (punto factible).
- **Fase 2**: Optimiza Z a partir de la base factible obtenida.
- Alternativa a Big M, más estable numéricamente.
- Si W > 0 al final de Fase 1 → problema no factible.

---

## Funcionalidades adicionales

- **Toggle decimales/fracciones** en tablas Simplex y Dos Fases (solo visual).
- **Modo forma natural**: escribir restricciones como `x1 + x2 <= 10`.
- **Tema claro/oscuro** configurable.
- **Placeholders** con ejemplos válidos en cada método.

---

## Inicio rápido

```bash
pip install -r requirements.txt
python app.py
# Abrir http://localhost:5000
```

---

## Estructura principal

```
app.py              → Servidor Flask y rutas API
solver.py           → Orquestador, importa los métodos
metodo_grafico.py   → Implementación método gráfico
metodo_simplex.py   → Implementación Simplex (Big M)
metodo_dos_fases.py → Implementación Dos Fases
templates/          → HTML
static/js/main.js   → Lógica frontend
```

---

## Más información

- `README.md` — Instalación, uso y despliegue
- `docs/02_ARQUITECTURA.md` — Detalle técnico de los métodos
- `docs/03_DESPLIEGUE.md` — Despliegue en Render, Heroku, Docker
