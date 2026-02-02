# Ejercicios de Validacion - Calculadora de Programacion Lineal

Este archivo contiene una nueva tanda de ejercicios para validar el correcto funcionamiento
de la calculadora despues de la reorganizacion del codigo.

---

## METODO GRAFICO (2 Variables)

### Ejercicio 1: Solucion Unica Basica
**Problema de Produccion de Muebles**

Una fabrica produce mesas (X) y sillas (Y). Maximizar ganancias.

**Funcion Objetivo:**
```
MAX Z = 4X + 3Y
```

**Restricciones:**
```
2X + Y <= 20    (Madera disponible)
X + 2Y <= 18    (Horas de trabajo)
X <= 8          (Demanda maxima de mesas)
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 45.33
- X = 7.33
- Y = 5.33

---

### Ejercicio 2: Soluciones Multiples
**Problema de Mezcla**

Mezclar dos productos A (X) e B (Y) para maximizar beneficio.

**Funcion Objetivo:**
```
MAX Z = 2X + 2Y
```

**Restricciones:**
```
X + Y <= 10
X <= 6
Y <= 6
```

**Resultado Esperado:**
- Tipo: Solucion Multiple (Infinitas Soluciones)
- Z = 20
- Multiples puntos optimos entre (4, 6) y (6, 4)

---

### Ejercicio 3: Solucion en Vertice del Origen
**Problema con Restricciones Estrictas**

**Funcion Objetivo:**
```
MIN Z = 3X + 5Y
```

**Restricciones:**
```
X + Y >= 0
X <= 10
Y <= 10
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 0
- X = 0
- Y = 0

---

### Ejercicio 4: Problema No Factible (Grafico)
**Restricciones Contradictorias**

**Funcion Objetivo:**
```
MAX Z = X + Y
```

**Restricciones:**
```
X + Y <= 4
X + Y >= 8
X <= 10
Y <= 10
```

**Resultado Esperado:**
- Tipo: No Factible
- Las restricciones son contradictorias (no puede ser <= 4 y >= 8 simultaneamente)

---

### Ejercicio 5: Minimizacion Simple
**Problema de Costos**

Minimizar costos de transporte usando dos rutas X e Y.

**Funcion Objetivo:**
```
MIN Z = 5X + 8Y
```

**Restricciones:**
```
X + Y >= 6      (Demanda minima)
2X + Y <= 16    (Capacidad)
X <= 7
Y <= 8
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 30
- X = 6
- Y = 0

---

## METODO SIMPLEX (Multiples Variables)

### Ejercicio 6: Simplex Clasico 3 Variables
**Problema de Produccion Industrial**

Una empresa fabrica 3 productos: A (X1), B (X2), C (X3).

**Funcion Objetivo:**
```
MAX Z = 5X1 + 4X2 + 3X3
```

**Restricciones:**
```
2X1 + 3X2 + X3 <= 60
4X1 + 2X2 + 3X3 <= 80
X1 + X2 + 2X3 <= 40
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 115
- X1 = 15
- X2 = 10
- X3 = 0

---

### Ejercicio 7: Simplex con Solucion Degenerada
**Problema de Asignacion de Recursos**

**Funcion Objetivo:**
```
MAX Z = 2X1 + 3X2
```

**Restricciones:**
```
X1 + X2 <= 4
X1 <= 2
X2 <= 3
X1 + 2X2 <= 6
```

**Resultado Esperado:**
- Tipo: Solucion Unica (Degenerada)
- Z = 10
- X1 = 2
- X2 = 2

---

### Ejercicio 8: Simplex 4 Variables
**Problema de Dieta Extendido**

Mezclar 4 alimentos para maximizar nutricion.

**Funcion Objetivo:**
```
MAX Z = 3X1 + 2X2 + 4X3 + X4
```

**Restricciones:**
```
X1 + X2 + X3 + X4 <= 100
2X1 + X2 + 3X3 + X4 <= 150
X1 + 2X2 + X3 + 2X4 <= 120
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 240
- X1 = 60, X2 = 30, X3 = 0, X4 = 0

---

### Ejercicio 9: Simplex Problema No Acotado
**Produccion Sin Limites Superiores**

**Funcion Objetivo:**
```
MAX Z = 3X1 + 2X2
```

**Restricciones:**
```
-X1 + X2 <= 4
X1 - 2X2 <= 2
```

**Resultado Esperado:**
- Tipo: Problema No Acotado
- Z puede crecer indefinidamente

---

### Ejercicio 10: Minimizacion con Simplex
**Problema de Costos de Produccion**

**Funcion Objetivo:**
```
MIN Z = 6X1 + 8X2 + 5X3
```

**Restricciones:**
```
2X1 + X2 + X3 >= 8
X1 + 2X2 + X3 >= 10
X1 + X2 + 2X3 >= 12
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z minimo encontrado

---

## METODO DOS FASES (Restricciones >= y =)

### Ejercicio 11: Dos Fases Basico
**Problema con Restricciones de Igualdad**

**Funcion Objetivo:**
```
MAX Z = 3X1 + 5X2
```

**Restricciones:**
```
X1 + X2 = 4
2X1 + X2 <= 6
X1 >= 1
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 43
- X1 = 0
- X2 = 4

---

### Ejercicio 12: Dos Fases con Restricciones Mixtas
**Problema de Produccion con Minimos**

**Funcion Objetivo:**
```
MAX Z = 4X1 + 3X2
```

**Restricciones:**
```
X1 + X2 >= 5
2X1 + X2 <= 12
X1 <= 4
X2 <= 6
```

**Resultado Esperado:**
- Tipo: Solucion Multiple (Infinitas Soluciones)
- Z = 61
- X1 = 3
- X2 = 6

---

### Ejercicio 13: Dos Fases - Problema No Factible
**Restricciones Imposibles**

**Funcion Objetivo:**
```
MAX Z = 2X1 + 3X2
```

**Restricciones:**
```
X1 + X2 >= 10
X1 + X2 <= 5
X1 >= 0
X2 >= 0
```

**Resultado Esperado:**
- Tipo: Problema No Factible
- Las restricciones son contradictorias

---

### Ejercicio 14: Dos Fases - Tres Variables
**Problema de Mezcla con Requisitos Minimos**

**Funcion Objetivo:**
```
MAX Z = 2X1 + 3X2 + 4X3
```

**Restricciones:**
```
X1 + X2 + X3 = 10
2X1 + X2 + X3 >= 8
X1 + 2X2 + X3 <= 15
```

**Resultado Esperado:**
- Tipo: Solucion Unica o Multiple
- Z optimo calculado

---

### Ejercicio 15: Dos Fases - Minimizacion
**Problema de Costos con Requisitos**

**Funcion Objetivo:**
```
MIN Z = 4X1 + 2X2
```

**Restricciones:**
```
X1 + X2 >= 6
2X1 + X2 >= 8
X1 + 3X2 >= 9
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z minimo (optimizacion de costos)

---

### Ejercicio 16: Dos Fases - Solo Igualdades
**Sistema de Ecuaciones como PL**

**Funcion Objetivo:**
```
MAX Z = 5X1 + 4X2
```

**Restricciones:**
```
X1 + X2 = 8
2X1 + X2 = 12
```

**Resultado Esperado:**
- Tipo: Solucion Unica
- Z = 128
- X1 = 4
- X2 = 4

---

### Ejercicio 17: Dos Fases - Multiples Soluciones
**Funcion Objetivo Paralela**

**Funcion Objetivo:**
```
MAX Z = 2X1 + 4X2
```

**Restricciones:**
```
X1 + 2X2 <= 8
X1 + X2 >= 2
X1 <= 4
X2 <= 3
```

**Resultado Esperado:**
- Tipo: Solucion Multiple (Infinitas Soluciones)
- Z = 20

---

## RESUMEN DE CASOS DE PRUEBA

| Ejercicio | Metodo | Tipo Esperado | Z Esperado |
|-----------|--------|---------------|------------|
| 1 | Grafico | Unica | 45.33 |
| 2 | Grafico | Multiple | 20 |
| 3 | Grafico | Unica (Origen) | 0 |
| 4 | Grafico | No Factible | - |
| 5 | Grafico | Unica (MIN) | 30 |
| 6 | Simplex | Unica | 115 |
| 7 | Simplex | Degenerada | 10 |
| 8 | Simplex | Unica | 240 |
| 9 | Simplex | No Acotado | - |
| 10 | Simplex | Multiple (MIN) | - |
| 11 | Dos Fases | Unica | 43 |
| 12 | Dos Fases | Multiple | 61 |
| 13 | Dos Fases | No Factible | - |
| 14 | Dos Fases | Unica | - |
| 15 | Dos Fases | Multiple (MIN) | - |
| 16 | Dos Fases | Unica | 128 |
| 17 | Dos Fases | Multiple | 20 |

---

## Notas de Validacion

1. **Metodo Grafico**: Solo acepta 2 variables (X, Y)
2. **Metodo Simplex**: Acepta n variables, ideal para restricciones <=
3. **Metodo Dos Fases**: Necesario cuando hay restricciones >= o =
4. **Restricciones de no negatividad**: Estan implicitas en todos los metodos

---

*Archivo generado para validacion post-refactorizacion del proyecto.*
*Fecha de generacion: Enero 2026*
