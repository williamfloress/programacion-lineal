# Ejercicios Completos de Programacion Lineal

Bateria completa de ejercicios para validar todos los escenarios posibles
de la calculadora de Programacion Lineal.

---

## METODO GRAFICO

El metodo grafico resuelve problemas con **2 variables** (X, Y).
Puede detectar: Solucion Unica, Multiples Soluciones, No Factible.

---

### G1: Maximizacion - Solucion Unica Clasica

**Contexto:** Produccion de dos productos con recursos limitados.

```
MAX Z = 3X + 2Y

Sujeto a:
2X + Y <= 18
X + 2Y <= 16
X <= 7
```

**Tipo:** Solucion Unica
**Z =** 29.33

---

### G2: Minimizacion - Solucion Unica

**Contexto:** Minimizar costos de produccion.

```
MIN Z = 4X + 5Y

Sujeto a:
X + Y >= 8
2X + Y >= 10
X <= 12
Y <= 12
```

**Tipo:** Solucion Unica

---

### G3: Soluciones Multiples (Infinitas)

**Contexto:** Funcion objetivo paralela a una restriccion activa.

```
MAX Z = 2X + 4Y

Sujeto a:
X + 2Y <= 10
X <= 6
Y <= 4
```

**Tipo:** Solucion Multiple (Infinitas Soluciones)
**Nota:** Z = 2X + 4Y es paralela a X + 2Y <= 10

---

### G4: Problema No Factible

**Contexto:** Restricciones contradictorias.

```
MAX Z = 5X + 3Y

Sujeto a:
X + Y <= 5
X + Y >= 10
X <= 8
Y <= 8
```

**Tipo:** No Factible

---

### G5: Solucion en el Origen

**Contexto:** Minimizacion donde el optimo esta en (0,0).

```
MIN Z = 7X + 9Y

Sujeto a:
X + Y >= 0
X <= 10
Y <= 10
```

**Tipo:** Solucion Unica
**Solucion:** X=0, Y=0, Z=0

---

### G6: Solucion en un Solo Eje

**Contexto:** Optimo sobre el eje X.

```
MAX Z = 5X + Y

Sujeto a:
X + Y <= 10
2X + Y <= 16
Y <= 6
```

**Tipo:** Solucion Unica
**Nota:** El optimo esta sobre el eje X (Y=0)

---

### G7: Restricciones con >= (Region Factible Acotada)

**Contexto:** Demandas minimas y capacidades maximas.

```
MAX Z = 3X + 4Y

Sujeto a:
X + Y >= 4
X + Y <= 10
X <= 6
Y <= 6
```

**Tipo:** Solucion Unica

---

### G8: Restricciones Mixtas Complejas

**Contexto:** Problema con multiples tipos de restricciones.

```
MIN Z = 2X + 3Y

Sujeto a:
X + Y >= 5
2X + Y <= 12
X >= 1
Y >= 1
X <= 8
Y <= 8
```

**Tipo:** Solucion Unica

---

## METODO SIMPLEX

El metodo Simplex resuelve problemas con **n variables**.
Ideal para restricciones <=. Detecta: Unica, Degenerada, Multiple, No Acotado, No Factible.

---

### S1: Simplex Basico - 2 Variables

**Contexto:** Problema clasico de maximizacion.

```
MAX Z = 4X1 + 3X2

Sujeto a:
2X1 + X2 <= 10
X1 + 2X2 <= 8
X1 + X2 <= 6
```

**Tipo:** Solucion Unica

---

### S2: Simplex - 3 Variables

**Contexto:** Produccion industrial con tres productos.

```
MAX Z = 5X1 + 4X2 + 3X3

Sujeto a:
2X1 + X2 + X3 <= 20
X1 + 2X2 + X3 <= 18
X1 + X2 + 2X3 <= 16
```

**Tipo:** Solucion Unica

---

### S3: Simplex - 4 Variables

**Contexto:** Mezcla de cuatro ingredientes.

```
MAX Z = 6X1 + 5X2 + 4X3 + 3X4

Sujeto a:
X1 + X2 + X3 + X4 <= 50
2X1 + X2 + X3 + X4 <= 60
X1 + 2X2 + X3 + X4 <= 55
X1 + X2 + 2X3 + X4 <= 45
```

**Tipo:** Solucion Unica

---

### S4: Simplex - Solucion Degenerada

**Contexto:** Multiples restricciones activas en el optimo.

```
MAX Z = 3X1 + 2X2

Sujeto a:
X1 + X2 <= 4
2X1 + X2 <= 6
X1 <= 3
X2 <= 3
```

**Tipo:** Solucion Unica (Degenerada)

---

### S5: Simplex - Soluciones Multiples

**Contexto:** Funcion objetivo paralela a restriccion activa.

```
MAX Z = 2X1 + 2X2

Sujeto a:
X1 + X2 <= 8
X1 <= 5
X2 <= 5
```

**Tipo:** Solucion Multiple (Infinitas Soluciones)

---

### S6: Simplex - Problema No Acotado

**Contexto:** Region factible no acotada en direccion de mejora.

```
MAX Z = 2X1 + 3X2

Sujeto a:
-X1 + X2 <= 5
X1 - X2 <= 3
```

**Tipo:** Problema No Acotado

---

### S7: Simplex - Minimizacion

**Contexto:** Minimizar costos de transporte.

```
MIN Z = 8X1 + 6X2 + 4X3

Sujeto a:
X1 + X2 + X3 <= 30
2X1 + X2 + X3 <= 40
X1 + X2 + 2X3 <= 35
```

**Tipo:** Solucion Unica

---

### S8: Simplex - Coeficientes Negativos

**Contexto:** Problema con coeficientes negativos en restricciones.

```
MAX Z = 3X1 + 5X2

Sujeto a:
X1 - X2 <= 4
-X1 + 2X2 <= 6
X1 + X2 <= 8
```

**Tipo:** Solucion Unica

---

## METODO DOS FASES

El metodo de Dos Fases maneja restricciones **>=** y **=**.
Fase 1: Encontrar solucion factible. Fase 2: Optimizar.

---

### D1: Solo Restricciones >=

**Contexto:** Demandas minimas de produccion.

```
MAX Z = 4X1 + 5X2

Sujeto a:
X1 + X2 >= 6
2X1 + X2 >= 8
X1 + 2X2 >= 7
X1 <= 10
X2 <= 10
```

**Tipo:** Solucion Unica o Multiple

---

### D2: Solo Restricciones =

**Contexto:** Sistema de ecuaciones como PL.

```
MAX Z = 3X1 + 2X2

Sujeto a:
X1 + X2 = 6
2X1 + X2 = 10
```

**Tipo:** Solucion Unica
**Solucion:** X1=4, X2=2, Z=16

---

### D3: Mezcla de <=, >= y =

**Contexto:** Problema con todos los tipos de restricciones.

```
MAX Z = 5X1 + 4X2

Sujeto a:
X1 + X2 = 8
2X1 + X2 <= 14
X1 >= 2
X2 >= 1
```

**Tipo:** Solucion Unica

---

### D4: Dos Fases - No Factible (Fase 1 Falla)

**Contexto:** Restricciones imposibles de satisfacer.

```
MAX Z = 3X1 + 4X2

Sujeto a:
X1 + X2 >= 15
X1 + X2 <= 8
X1 <= 10
X2 <= 10
```

**Tipo:** Problema No Factible

---

### D5: Dos Fases - Minimizacion

**Contexto:** Minimizar costos con requisitos minimos.

```
MIN Z = 6X1 + 4X2

Sujeto a:
X1 + X2 >= 8
2X1 + X2 >= 10
X1 + 3X2 >= 12
```

**Tipo:** Solucion Unica

---

### D6: Dos Fases - 3 Variables

**Contexto:** Problema de mezcla con tres componentes.

```
MAX Z = 3X1 + 2X2 + 5X3

Sujeto a:
X1 + X2 + X3 = 10
2X1 + X2 + X3 >= 8
X1 + 2X2 + X3 <= 15
X3 >= 2
```

**Tipo:** Solucion Unica

---

### D7: Dos Fases - Soluciones Multiples

**Contexto:** FO paralela a restriccion activa.

```
MAX Z = 2X1 + 2X2

Sujeto a:
X1 + X2 >= 4
X1 + X2 <= 8
X1 <= 5
X2 <= 5
```

**Tipo:** Solucion Multiple (Infinitas Soluciones)

---

### D8: Dos Fases - 4 Variables con Igualdades

**Contexto:** Sistema complejo con restricciones de igualdad.

```
MAX Z = 2X1 + 3X2 + 4X3 + X4

Sujeto a:
X1 + X2 + X3 + X4 = 20
2X1 + X2 + X3 + X4 >= 15
X1 + X2 + 2X3 + X4 <= 25
X1 + 2X2 + X3 + 2X4 >= 18
```

**Tipo:** Solucion Unica

---

## RESUMEN DE ESCENARIOS CUBIERTOS

### Metodo Grafico (8 ejercicios)
| ID | Escenario | Objetivo |
|----|-----------|----------|
| G1 | Maximizacion clasica | MAX |
| G2 | Minimizacion clasica | MIN |
| G3 | Soluciones multiples | MAX |
| G4 | No factible | MAX |
| G5 | Solucion en origen | MIN |
| G6 | Solucion en eje | MAX |
| G7 | Restricciones >= | MAX |
| G8 | Restricciones mixtas | MIN |

### Metodo Simplex (8 ejercicios)
| ID | Escenario | Variables |
|----|-----------|-----------|
| S1 | Basico | 2 |
| S2 | Tres variables | 3 |
| S3 | Cuatro variables | 4 |
| S4 | Degenerada | 2 |
| S5 | Multiples soluciones | 2 |
| S6 | No acotado | 2 |
| S7 | Minimizacion | 3 |
| S8 | Coeficientes negativos | 2 |

### Metodo Dos Fases (8 ejercicios)
| ID | Escenario | Restricciones |
|----|-----------|---------------|
| D1 | Solo >= | >= |
| D2 | Solo = | = |
| D3 | Mezcla completa | <=, >=, = |
| D4 | No factible | >=, <= |
| D5 | Minimizacion | >= |
| D6 | Tres variables | =, >=, <= |
| D7 | Multiples soluciones | >=, <= |
| D8 | Cuatro variables | =, >=, <= |

---

## TOTAL: 24 EJERCICIOS

Cubren todas las situaciones posibles:
- Maximizacion y Minimizacion
- Solucion Unica, Degenerada, Multiple
- Problema No Factible y No Acotado
- 2, 3 y 4 variables
- Restricciones <=, >=, =
- Coeficientes positivos y negativos

---

## COMO EJECUTAR LAS PRUEBAS

```bash
# Todas las pruebas (24 ejercicios)
python test_completo.py

# Solo metodo grafico (8 ejercicios)
python test_completo.py grafico

# Solo metodo simplex (8 ejercicios)
python test_completo.py simplex

# Solo metodo dos fases (8 ejercicios)
python test_completo.py dosfases

# Prueba rapida (1 de cada metodo)
python test_completo.py rapido
```

---

*Archivo generado para pruebas exhaustivas de la calculadora.*
*Ultima validacion: 24/24 ejercicios pasados (100%)*
