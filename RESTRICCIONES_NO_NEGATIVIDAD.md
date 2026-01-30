# Restricciones de No Negatividad Explícitas

## ¿Qué son las restricciones de no negatividad?

En Programación Lineal, las **restricciones de no negatividad** establecen que todas las variables deben ser mayores o iguales a cero:

```
x₁ ≥ 0
x₂ ≥ 0
x₃ ≥ 0
...
```

## Implementación en la Calculadora

### Modo Implícito (Por defecto)

Por defecto, el solver **asume automáticamente** que todas las variables son no negativas. Esto significa que:

- No necesitas escribir explícitamente `x ≥ 0`, `y ≥ 0`, etc.
- El algoritmo internamente maneja estas restricciones
- Los pasos del cálculo no mostrarán estas restricciones

**Ventajas:**
- Menos escritura
- Interfaz más limpia
- Rápido para problemas estándar

### Modo Explícito (Checkbox activado)

Cuando activas el checkbox **"Incluir restricciones de no negatividad explícitas"**:

1. Se añaden automáticamente las restricciones `xᵢ ≥ 0` para cada variable
2. Estas restricciones aparecen en los cálculos y pasos del algoritmo
3. Se muestran en las tablas del Simplex como restricciones normales

**Ventajas:**
- Útil para **problemas académicos** donde se requiere mostrar todas las restricciones
- Claridad pedagógica: se ve explícitamente cómo las restricciones de no negatividad afectan la región factible
- Cumple con formatos de exámenes y tareas que requieren mostrar todas las restricciones

## ¿Cuándo usar cada modo?

### Usa el modo IMPLÍCITO (checkbox desactivado) cuando:
- Estés resolviendo problemas reales donde solo te interesa el resultado
- Quieras una presentación más limpia y concisa
- Estés trabajando con muchas variables (evitas restricciones redundantes en pantalla)

### Usa el modo EXPLÍCITO (checkbox activado) cuando:
- Estés haciendo una tarea o examen que requiere mostrar todas las restricciones
- Quieras explicar didácticamente cómo funcionan las restricciones de no negatividad
- Necesites documentar completamente el problema matemático
- El profesor/instructor solicita explícitamente ver todas las restricciones

## Ejemplo Comparativo

### Problema Original
```
Maximizar Z = X₁ + 5X₂

Sujeto a:
5X₁ + 6X₂ ≤ 30  (Papel)
3X₁ + 2X₂ ≤ 15  (Tintas)
-X₁ + 2X₂ ≤ 10  (Plantillas)
```

### Modo Implícito (checkbox desactivado)
El solver procesa internamente:
```
X₁ ≥ 0, X₂ ≥ 0  (implícitas, no mostradas)
```

**Salida en pasos:**
```
RESTRICCIONES:
  R1: 5X₁ + 6X₂ ≤ 30
  R2: 3X₁ + 2X₂ ≤ 15
  R3: -X₁ + 2X₂ ≤ 10
```

### Modo Explícito (checkbox activado)
El solver añade automáticamente:
```
X₁ ≥ 0  (añadida explícitamente)
X₂ ≥ 0  (añadida explícitamente)
```

**Salida en pasos:**
```
RESTRICCIONES:
  R1: 5X₁ + 6X₂ ≤ 30
  R2: 3X₁ + 2X₂ ≤ 15
  R3: -X₁ + 2X₂ ≤ 10
  R4: 1X₁ + 0X₂ ≥ 0  (No negatividad de X₁)
  R5: 0X₁ + 1X₂ ≥ 0  (No negatividad de X₂)
```

## Disponibilidad

Esta funcionalidad está disponible en:
- ✅ **Método Gráfico**: Añade X ≥ 0, Y ≥ 0
- ✅ **Método Simplex**: Añade xᵢ ≥ 0 para todas las variables
- ✅ **Método de Dos Fases**: Añade xᵢ ≥ 0 para todas las variables

## Ubicación del Checkbox

El checkbox se encuentra justo antes del botón "CALCULAR SOLUCIÓN" en cada método:

```
┌──────────────────────────────────────────────────┐
│ ☐ Incluir restricciones de no negatividad       │
│   explícitas (x₁ ≥ 0, x₂ ≥ 0, ...)              │
│                                                  │
│   Al activar esta opción, las restricciones     │
│   xᵢ ≥ 0 se añadirán automáticamente...         │
└──────────────────────────────────────────────────┘

[CALCULAR SOLUCIÓN]
```

## Nota Técnica

**Importante:** La solución matemática es **idéntica** en ambos modos. La única diferencia es cómo se **presenta** la información:

- **Modo implícito**: Las restricciones de no negatividad se procesan internamente pero no se muestran
- **Modo explícito**: Las restricciones de no negatividad se añaden al problema y aparecen en todos los pasos

Ambos modos producen el **mismo resultado numérico** (mismo Z óptimo, mismos valores de variables).

## Implementación Técnica

### Frontend (JavaScript)
```javascript
// Al resolver, si el checkbox está activado:
if (incluirNoNegatividad) {
    // Para método gráfico (2 variables):
    restricciones.push({ x: 1, y: 0, op: '>=', val: 0 });  // X ≥ 0
    restricciones.push({ x: 0, y: 1, op: '>=', val: 0 });  // Y ≥ 0
    
    // Para Simplex/Dos Fases (n variables):
    for (let i = 0; i < numVariables; i++) {
        const coefs = new Array(numVariables).fill(0);
        coefs[i] = 1;  // 1*xᵢ ≥ 0
        restricciones.push({ coefs, op: '>=', val: 0 });
    }
}
```

### Backend (Python)
El backend recibe las restricciones adicionales y las procesa como cualquier otra restricción usando el método Simplex o el método gráfico estándar.

---

**Fecha de implementación:** 2026-01-30
**Versión:** 1.0
**Autor:** Sistema de Programación Lineal
