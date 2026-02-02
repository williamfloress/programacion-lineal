# Ejercicios de Prueba - Programación Lineal

Batería de ejercicios para validar la calculadora. Total: **24 ejercicios**.

---

## Método Gráfico (8 ejercicios)

### G1: Maximización Clásica
```
MAX Z = 3X + 2Y
Sujeto a:
  2X + Y <= 18
  X + 2Y <= 16
  X <= 7
```
**Tipo:** Solución Única | **Z ≈** 29.33

### G2: Minimización
```
MIN Z = 4X + 5Y
Sujeto a:
  X + Y >= 8
  2X + Y >= 10
  X <= 12
  Y <= 12
```
**Tipo:** Solución Única

### G3: Soluciones Múltiples
```
MAX Z = 2X + 4Y
Sujeto a:
  X + 2Y <= 10
  X <= 6
  Y <= 4
```
**Tipo:** Múltiple (Z paralela a restricción activa)

### G4: No Factible
```
MAX Z = 5X + 3Y
Sujeto a:
  X + Y <= 5
  X + Y >= 10
```
**Tipo:** No Factible (restricciones contradictorias)

### G5: Solución en el Origen
```
MIN Z = 7X + 9Y
Sujeto a:
  X + Y >= 0
  X <= 10
  Y <= 10
```
**Tipo:** Única | **Solución:** (0, 0), Z = 0

### G6: Solución en Eje
```
MAX Z = 5X + Y
Sujeto a:
  X + Y <= 10
  2X + Y <= 16
  Y <= 6
```
**Tipo:** Única (óptimo en eje X)

### G7: Restricciones >=
```
MAX Z = 3X + 4Y
Sujeto a:
  X + Y >= 4
  X + Y <= 10
  X <= 6
  Y <= 6
```
**Tipo:** Solución Única

### G8: Restricciones Mixtas
```
MIN Z = 2X + 3Y
Sujeto a:
  X + Y >= 5
  2X + Y <= 12
  X >= 1
  Y >= 1
```
**Tipo:** Solución Única

---

## Método Simplex (8 ejercicios)

### S1: Básico 2 Variables
```
MAX Z = 4X₁ + 3X₂
Sujeto a:
  2X₁ + X₂ <= 10
  X₁ + 2X₂ <= 8
  X₁ + X₂ <= 6
```
**Tipo:** Solución Única

### S2: 3 Variables
```
MAX Z = 5X₁ + 4X₂ + 3X₃
Sujeto a:
  2X₁ + X₂ + X₃ <= 20
  X₁ + 2X₂ + X₃ <= 18
  X₁ + X₂ + 2X₃ <= 16
```
**Tipo:** Solución Única

### S3: 4 Variables
```
MAX Z = 6X₁ + 5X₂ + 4X₃ + 3X₄
Sujeto a:
  X₁ + X₂ + X₃ + X₄ <= 50
  2X₁ + X₂ + X₃ + X₄ <= 60
  X₁ + 2X₂ + X₃ + X₄ <= 55
  X₁ + X₂ + 2X₃ + X₄ <= 45
```
**Tipo:** Solución Única

### S4: Degenerada
```
MAX Z = 3X₁ + 2X₂
Sujeto a:
  X₁ + X₂ <= 4
  2X₁ + X₂ <= 6
  X₁ <= 3
  X₂ <= 3
```
**Tipo:** Única (Degenerada)

### S5: Múltiples Soluciones
```
MAX Z = 2X₁ + 2X₂
Sujeto a:
  X₁ + X₂ <= 8
  X₁ <= 5
  X₂ <= 5
```
**Tipo:** Solución Múltiple

### S6: No Acotado
```
MAX Z = 2X₁ + 3X₂
Sujeto a:
  -X₁ + X₂ <= 5
  X₁ - X₂ <= 3
```
**Tipo:** No Acotado

### S7: Minimización
```
MIN Z = 8X₁ + 6X₂ + 4X₃
Sujeto a:
  X₁ + X₂ + X₃ <= 30
  2X₁ + X₂ + X₃ <= 40
  X₁ + X₂ + 2X₃ <= 35
```
**Tipo:** Solución Única

### S8: Coeficientes Negativos
```
MAX Z = 3X₁ + 5X₂
Sujeto a:
  X₁ - X₂ <= 4
  -X₁ + 2X₂ <= 6
  X₁ + X₂ <= 8
```
**Tipo:** Solución Única

---

## Método Dos Fases (8 ejercicios)

### D1: Solo Restricciones >=
```
MAX Z = 4X₁ + 5X₂
Sujeto a:
  X₁ + X₂ >= 6
  2X₁ + X₂ >= 8
  X₁ + 2X₂ >= 7
  X₁ <= 10
  X₂ <= 10
```
**Tipo:** Solución Única

### D2: Solo Restricciones =
```
MAX Z = 3X₁ + 2X₂
Sujeto a:
  X₁ + X₂ = 6
  2X₁ + X₂ = 10
```
**Tipo:** Única | **Solución:** X₁=4, X₂=2, Z=16

### D3: Mezcla <=, >=, =
```
MAX Z = 5X₁ + 4X₂
Sujeto a:
  X₁ + X₂ = 8
  2X₁ + X₂ <= 14
  X₁ >= 2
  X₂ >= 1
```
**Tipo:** Solución Única

### D4: No Factible (Fase 1 Falla)
```
MAX Z = 3X₁ + 4X₂
Sujeto a:
  X₁ + X₂ >= 15
  X₁ + X₂ <= 8
```
**Tipo:** No Factible

### D5: Minimización
```
MIN Z = 6X₁ + 4X₂
Sujeto a:
  X₁ + X₂ >= 8
  2X₁ + X₂ >= 10
  X₁ + 3X₂ >= 12
```
**Tipo:** Solución Única

### D6: 3 Variables
```
MAX Z = 3X₁ + 2X₂ + 5X₃
Sujeto a:
  X₁ + X₂ + X₃ = 10
  2X₁ + X₂ + X₃ >= 8
  X₁ + 2X₂ + X₃ <= 15
  X₃ >= 2
```
**Tipo:** Solución Única

### D7: Múltiples Soluciones
```
MAX Z = 2X₁ + 2X₂
Sujeto a:
  X₁ + X₂ >= 4
  X₁ + X₂ <= 8
  X₁ <= 5
  X₂ <= 5
```
**Tipo:** Solución Múltiple

### D8: 4 Variables con Igualdades
```
MAX Z = 2X₁ + 3X₂ + 4X₃ + X₄
Sujeto a:
  X₁ + X₂ + X₃ + X₄ = 20
  2X₁ + X₂ + X₃ + X₄ >= 15
  X₁ + X₂ + 2X₃ + X₄ <= 25
  X₁ + 2X₂ + X₃ + 2X₄ >= 18
```
**Tipo:** Solución Única

---

## Resumen

| Método | Ejercicios | Escenarios |
|--------|------------|------------|
| Gráfico | G1-G8 | Max, Min, Múltiple, No Factible, Origen, Eje |
| Simplex | S1-S8 | 2-4 vars, Degenerada, Múltiple, No Acotado |
| Dos Fases | D1-D8 | >=, =, Mezcla, No Factible, 3-4 vars |

---

## Ejecución de Pruebas

```bash
# Todas las pruebas
python tests/test_completo.py

# Por método
python tests/test_completo.py grafico
python tests/test_completo.py simplex
python tests/test_completo.py dosfases
```

**Resultado esperado:** 24/24 ejercicios (100%)
