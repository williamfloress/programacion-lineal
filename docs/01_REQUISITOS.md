# Requisitos del MVP - Calculadora de Programación Lineal

## Objetivo

Aplicación web para resolver problemas de Programación Lineal usando múltiples métodos: Gráfico (2 variables), Simplex y Dos Fases (n variables).

---

## Alcance del MVP

### Incluido
- Resolución con 2+ variables
- Restricciones: ≤, ≥, =
- Maximización y minimización
- Clasificación de soluciones (Única, Múltiple, No Factible, No Acotada, Degenerada)
- Visualización gráfica (método gráfico)
- Tablas Simplex paso a paso
- Interfaz web responsive con Dark Mode

### Excluido
- Guardado/historial de problemas
- Autenticación de usuarios
- Exportación a PDF

---

## Requisitos Funcionales

### RF-1: Entrada de Datos
- **Función Objetivo:** Coeficientes + objetivo (max/min)
- **Restricciones:** Coeficientes + operador + valor (mín. 1, máx. 10)
- **Validaciones:** Campos numéricos válidos, al menos 1 restricción

### RF-2: Procesamiento Matemático
1. Estandarizar restricciones
2. Calcular intersecciones/iteraciones
3. Filtrar región factible
4. Evaluar función objetivo
5. Clasificar tipo de solución

### RF-3: Visualización
- Gráfico 2D interactivo (Plotly.js)
- Tablas Simplex con variables básicas
- Resumen de solución

### RF-4: Manejo de Errores
- Entradas inválidas
- Problemas no factibles/no acotados
- Errores de cálculo

---

## Requisitos Técnicos

### Stack
- **Backend:** Python, Flask, NumPy
- **Frontend:** HTML, CSS, JavaScript
- **Gráficos:** Plotly.js
- **Despliegue:** Gunicorn, Docker, Render

### API Endpoints
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/calcular` | POST | Método Gráfico |
| `/calcular-simplex` | POST | Método Simplex |
| `/calcular-dos-fases` | POST | Método Dos Fases |

---

## Criterios de Calidad

- **Precisión:** Tolerancia 1e-9 para comparaciones
- **Rendimiento:** < 1 segundo para 10 restricciones
- **Usabilidad:** Interfaz intuitiva, responsive

---

## Casos de Prueba Esenciales

| Caso | Tipo | Resultado |
|------|------|-----------|
| CP-1 | Solución Única | Z óptimo en un vértice |
| CP-2 | Solución Múltiple | Varios vértices óptimos |
| CP-3 | No Factible | Restricciones contradictorias |
| CP-4 | No Acotado | Región no cerrada |

---

**Estado:** MVP Completado
