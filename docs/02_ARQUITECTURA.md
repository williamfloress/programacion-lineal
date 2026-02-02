# Arquitectura y Funcionamiento de los Métodos

Este documento explica cómo funciona cada método de solución implementado.

---

## 1. Método Gráfico

**Uso:** Problemas con exactamente **2 variables** (X, Y).

### Proceso

1. **Definir problema:** Z (función objetivo) y restricciones como rectas en el plano
2. **Calcular intersecciones:** Resolver sistemas 2×2 para cada par de rectas
3. **Filtrar vértices factibles:** Solo puntos que cumplen TODAS las restricciones
4. **Evaluar Z:** Calcular Z en cada vértice factible
5. **Identificar óptimo:** Vértice con mejor Z (max o min)

### Clasificación de Soluciones

| Tipo | Condición |
|------|-----------|
| Única | Un solo vértice con Z óptimo |
| Múltiple | Varios vértices con mismo Z óptimo |
| No Factible | Ningún vértice satisface todas las restricciones |
| Degenerada | Múltiples restricciones activas en el óptimo |

---

## 2. Método Simplex

**Uso:** Problemas con **n variables**. Ideal para restricciones ≤.

### Proceso

1. **Forma estándar:** Agregar variables de holgura (s) para convertir ≤ en =
2. **Tabla inicial:** Fila Z + filas de restricciones + columna RHS
3. **Iteraciones:**
   - Elegir variable entrante (coeficiente más negativo en fila Z para max)
   - Elegir variable saliente (ratio mínimo positivo)
   - Pivotear para hacer 1 el pivote y 0 el resto de la columna
4. **Parar cuando:** Todos los coeficientes en fila Z son ≥ 0 (max) o ≤ 0 (min)

### Detección de Casos Especiales

| Caso | Detección |
|------|-----------|
| Óptimo | Coeficientes en fila Z tienen signo correcto |
| No Acotado | Todos los ratios son negativos/infinitos |
| Múltiple | Variables no básicas con costo reducido = 0 |
| Degenerada | Variable básica con valor 0 |

---

## 3. Método de Dos Fases

**Uso:** Problemas con restricciones **≥** o **=** (requieren variables artificiales).

### Fase 1: Encontrar Solución Factible

1. Agregar variables artificiales (a) para restricciones ≥ y =
2. Minimizar W = suma de variables artificiales
3. Aplicar Simplex hasta W = 0
4. Si W > 0 al terminar → **No Factible**

### Fase 2: Optimizar Función Objetivo

1. Eliminar variables artificiales de la tabla
2. Restaurar fila Z con coeficientes originales
3. Aplicar Simplex normal hasta óptimo

### Diferencia con Big M

| Aspecto | Big M | Dos Fases |
|---------|-------|-----------|
| Enfoque | Penaliza artificiales con M grande | Minimiza artificiales primero |
| Estabilidad | Puede tener errores numéricos | Más estable |
| Claridad | Una sola fase | Dos fases distintas |

---

## 4. Restricciones de No Negatividad

Por defecto, el solver asume **implícitamente** que X ≥ 0, Y ≥ 0, etc.

### Modo Explícito

Activando el checkbox "Incluir restricciones de no negatividad explícitas":
- Se añaden xᵢ ≥ 0 para cada variable
- Aparecen en los pasos del cálculo
- Útil para contextos académicos

**Nota:** La solución matemática es idéntica en ambos modos.

---

## Resumen de Métodos

| Método | Variables | Restricciones | Resultado |
|--------|-----------|---------------|-----------|
| Gráfico | Solo 2 | ≤, ≥, = | Gráfica + vértices |
| Simplex | n | ≤ (ideal) | Tablas iterativas |
| Dos Fases | n | ≤, ≥, = | Tablas Fase 1 y 2 |

---

## Archivos de Implementación

| Archivo | Clase/Función | Descripción |
|---------|---------------|-------------|
| `solver.py` | `Solver` | Orquestador principal |
| `metodo_grafico.py` | `MetodoGrafico` | Implementación gráfica |
| `metodo_simplex.py` | `MetodoSimplex` | Implementación Simplex |
| `metodo_dos_fases.py` | `MetodoDosFases` | Implementación Dos Fases |
