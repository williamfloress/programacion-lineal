# Ejercicios de Prueba - Calculadora de Programación Lineal

Este documento contiene ejercicios resueltos para probar todas las funcionalidades de la calculadora.

---

## MÉTODO GRÁFICO (2 Variables)

**Nota:** El método gráfico actual solo maneja regiones factibles acotadas. Para problemas no acotados, usar el Método Simplex o Dos Fases.

### Ejercicio 1: Solución Única - Problema de Producción
**Contexto:** Una empresa fabrica dos productos A y B.

**Función Objetivo:**
- Maximizar Z = 3X + 2Y

**Restricciones:**
```
2X + Y ≤ 100
X + Y ≤ 80
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 20
- Y = 60
- Z = 180
- **Tipo:** Solución Única

---

### Ejercicio 2: Solución Única - Problema Básico
**Función Objetivo:**
- Maximizar Z = 5X + 4Y

**Restricciones:**
```
X + 2Y ≤ 40
3X + 2Y ≤ 60
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 10
- Y = 15
- Z = 110
- **Tipo:** Solución Única

---

### Ejercicio 3: Solución Única Degenerada
**Contexto:** El ejercicio que reportaste originalmente.

**Función Objetivo:**
- Maximizar Z = X + 5Y

**Restricciones:**
```
5X + 6Y ≤ 30
-X + 2Y ≤ 10
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 0
- Y = 5
- Z = 25
- **Tipo:** Solución Única (Degenerada)
- **Nota:** Tres restricciones se cruzan en el punto óptimo

---

### Ejercicio 4: Soluciones Múltiples (Infinitas)
**Función Objetivo:**
- Maximizar Z = 2X + 4Y

**Restricciones:**
```
X + 2Y ≤ 20
2X + Y ≤ 30
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- Múltiples soluciones en el segmento entre dos vértices
- Z = 40 (constante en el segmento óptimo)
- **Tipo:** Solución Múltiple (Infinitas Soluciones)
- **Nota:** La función objetivo es paralela a una restricción activa

---

### Ejercicio 5: Solución en el Origen
**Función Objetivo:**
- Maximizar Z = -X - Y

**Restricciones:**
```
X + Y ≤ 10
2X + Y ≤ 15
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 0
- Y = 0
- Z = 0
- **Tipo:** Solución Única
- **Nota:** Cuando la función objetivo tiene coeficientes negativos en maximización, el óptimo está en el origen

---

### Ejercicio 6: Problema No Factible
**Función Objetivo:**
- Maximizar Z = X + Y

**Restricciones:**
```
X + Y ≤ 5
X + Y ≥ 10
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- **Tipo:** Problema No Factible
- **Nota:** Las restricciones son contradictorias (no existe región factible)

---

### Ejercicio 7: Minimización Simple
**Función Objetivo:**
- Minimizar Z = 2X + 3Y

**Restricciones:**
```
X + Y ≥ 10
2X + Y ≥ 16
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 10
- Y = 0
- Z = 20
- **Tipo:** Solución Única

---

### Ejercicio 8: Región Triangular
**Función Objetivo:**
- Maximizar Z = 4X + 3Y

**Restricciones:**
```
X + Y ≤ 10
X ≤ 6
Y ≤ 8
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 6
- Y = 4
- Z = 36
- **Tipo:** Solución Única

---

## MÉTODO SIMPLEX (3+ Variables)

### Ejercicio 9: Simplex Básico - 3 Variables
**Contexto:** Problema de producción con tres productos.

**Función Objetivo:**
- Maximizar Z = 3X₁ + 2X₂ + 5X₃

**Restricciones:**
```
X₁ + 2X₂ + X₃ ≤ 430
3X₁ + 2X₃ ≤ 460
X₁ + 4X₂ ≤ 420
X₁, X₂, X₃ ≥ 0
```

**Solución Esperada:**
- Verificar tabla final del Simplex
- Z óptimo = 1350
- **Iteraciones:** 3
- **Tipo:** Solución Única
- **Nota:** La solución óptima aprovecha múltiples restricciones

---

### Ejercicio 10: Simplex Standard - 4 Variables
**Función Objetivo:**
- Maximizar Z = 5X₁ + 4X₂ + 3X₃ + 6X₄

**Restricciones:**
```
X₁ + X₂ + X₃ + X₄ ≤ 20
2X₁ + X₂ + 3X₃ + X₄ ≤ 30
X₁, X₂, X₃, X₄ ≥ 0
```

**Solución Esperada:**
- Variables básicas: verificar en la tabla final
- Z óptimo > 0
- **Iteraciones:** 2-4
- **Tipo:** Solución Única

---

### Ejercicio 11: Simplex - Problema de Mezcla
**Función Objetivo:**
- Maximizar Z = 2X₁ + 3X₂ + 4X₃

**Restricciones:**
```
X₁ + X₂ + 2X₃ ≤ 40
2X₁ + X₂ + X₃ ≤ 60
X₁ + 2X₂ + X₃ ≤ 50
X₁, X₂, X₃ ≥ 0
```

**Solución Esperada:**
- Verificar tabla final del Simplex
- Z óptimo calculado por el método
- **Iteraciones:** 2-3
- **Tipo:** Solución Única

---

### Ejercicio 12: Simplex - Minimización
**Función Objetivo:**
- Minimizar Z = 2X₁ + 3X₂ + X₃

**Restricciones:**
```
X₁ + X₂ + X₃ ≤ 40
2X₁ + X₂ - X₃ ≤ 10
-X₁ + 2X₂ + X₃ ≤ 20
X₁, X₂, X₃ ≥ 0
```

**Solución Esperada:**
- Verificar conversión a maximización (-Z)
- Solución en vértice de la región factible
- **Tipo:** Solución Única

---

### Ejercicio 13: Simplex - Caso Degenerado
**Función Objetivo:**
- Maximizar Z = 2X₁ + X₂ + X₃

**Restricciones:**
```
X₁ + X₂ ≤ 8
X₂ + X₃ ≤ 8
X₁ + X₃ ≤ 8
X₁, X₂, X₃ ≥ 0
```

**Solución Esperada:**
- Z óptimo = 16
- **Tipo:** Solución Múltiple (Infinitas Soluciones)
- **Nota:** Existe una variable no básica con coeficiente cero en Z, generando infinitas soluciones óptimas

---

### Ejercicio 13B: Simplex - Problema No Acotado
**Función Objetivo:**
- Maximizar Z = X₁ + 2X₂

**Restricciones:**
```
-X₁ + X₂ ≤ 5
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- **Tipo:** Problema No Acotado
- **Explicación:** La región factible permite que Z crezca indefinidamente. La restricción -X₁ + X₂ ≤ 5 (o sea X₂ ≤ X₁ + 5) no limita el crecimiento en la dirección del gradiente (1, 2).
- **Detección:** El Simplex detecta que la variable entrante no puede salir (todos los coeficientes son ≤ 0)

---

## MÉTODO DE DOS FASES (Restricciones ≥ o =)

### Ejercicio 14: Dos Fases Básico
**Función Objetivo:**
- Maximizar Z = 3X₁ + 2X₂

**Restricciones:**
```
X₁ + X₂ = 5
2X₁ + X₂ ≥ 8
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Fase 1: Minimizar W (variables artificiales)
- Fase 2: Optimizar Z
- Z = 49
- **Tipo:** Solución Única

---

### Ejercicio 15: Dos Fases Simple
**Función Objetivo:**
- Maximizar Z = 3X₁ + 5X₂

**Restricciones:**
```
X₁ + 2X₂ ≥ 4
X₁ + X₂ ≥ 3
X₁ ≤ 10
X₂ ≤ 8
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Variables artificiales en Fase 1 para las restricciones ≥
- W = 0 al final de Fase 1 (factible)
- Z = 99
- **Tipo:** Solución Múltiple (Infinitas Soluciones)
- **Nota:** La función objetivo es paralela a una restricción activa

---

### Ejercicio 16: Dos Fases con Igualdad
**Función Objetivo:**
- Maximizar Z = X₁ + 2X₂

**Restricciones:**
```
X₁ + X₂ = 5
X₁ ≤ 4
X₂ ≤ 4
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Variable artificial para la restricción de igualdad
- W = 0 al final de Fase 1 (factible)
- Solución óptima en Fase 2
- **Tipo:** Solución Única

---

### Ejercicio 17: Dos Fases - Restricción Mayor o Igual
**Función Objetivo:**
- Minimizar Z = 2X₁ + 3X₂

**Restricciones:**
```
X₁ + X₂ ≥ 6
2X₁ + X₂ ≥ 8
X₁ ≤ 10
X₂ ≤ 10
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Variables artificiales para restricciones ≥
- Conversión de minimización a maximización internamente
- Fase 1: W = 0 (factible)
- Z = 34
- **Tipo:** Solución Múltiple (Infinitas Soluciones)
- **Nota:** La función objetivo es paralela a una restricción activa

---

### Ejercicio 18: Dos Fases - No Factible
**Función Objetivo:**
- Maximizar Z = X₁ + X₂

**Restricciones:**
```
X₁ + X₂ ≥ 10
X₁ ≤ 3
X₂ ≤ 4
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Fase 1: W > 0 (no se pueden eliminar artificiales)
- **Tipo:** Problema No Factible
- **Nota:** No existe solución que cumpla todas las restricciones

---

### Ejercicio 19: Dos Fases - Problema de Asignación
**Función Objetivo:**
- Maximizar Z = 5X₁ + 7X₂ + 6X₃

**Restricciones:**
```
X₁ + X₂ + X₃ = 100
X₁ ≥ 20
X₂ ≥ 30
X₃ ≥ 10
X₁, X₂, X₃ ≥ 0
```

**Solución Esperada:**
- Una restricción de igualdad
- Tres restricciones de desigualdad ≥
- Variables artificiales en Fase 1
- **Tipo:** Solución Única

---

## CASOS ESPECIALES PARA PRUEBAS

### Ejercicio 20: Coeficientes Decimales
**Función Objetivo:**
- Maximizar Z = 1.5X + 2.75Y

**Restricciones:**
```
0.5X + 1.25Y ≤ 10
1.75X + 0.5Y ≤ 15
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- Verificar manejo de decimales
- **Tipo:** Solución Única

---

### Ejercicio 21: Coeficientes Negativos en Objetivo
**Función Objetivo:**
- Maximizar Z = 5X - 2Y

**Restricciones:**
```
X + Y ≤ 10
X - Y ≤ 5
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- Y = 0 en solución óptima
- **Tipo:** Solución Única

---

### Ejercicio 22: Coeficientes Muy Grandes
**Función Objetivo:**
- Maximizar Z = 1000X₁ + 1500X₂

**Restricciones:**
```
50X₁ + 100X₂ ≤ 10000
200X₁ + 150X₂ ≤ 15000
X₁, X₂ ≥ 0
```

**Solución Esperada:**
- Verificar estabilidad numérica
- **Tipo:** Solución Única

---

### Ejercicio 23: Problema con Muchas Variables (Simplex)
**Función Objetivo:**
- Maximizar Z = X₁ + 2X₂ + 3X₃ + 4X₄ + 5X₅

**Restricciones:**
```
X₁ + X₂ + X₃ + X₄ + X₅ ≤ 20
2X₁ + X₂ + X₃ + X₄ + 2X₅ ≤ 30
X₁, X₂, X₃, X₄, X₅ ≥ 0
```

**Solución Esperada:**
- Verificar manejo de múltiples variables
- Tabla Simplex amplia
- **Tipo:** Solución Única

---

### Ejercicio 24: Región Factible Muy Pequeña
**Función Objetivo:**
- Maximizar Z = X + Y

**Restricciones:**
```
X ≤ 1
Y ≤ 1
X + Y ≥ 0.5
X ≥ 0
Y ≥ 0
```

**Solución Esperada:**
- X = 1, Y = 1
- Z = 2
- **Tipo:** Solución Única

---

## GUÍA DE USO

### Cómo Probar los Ejercicios:

1. **Método Gráfico (Ejercicios 1-8):**
   - Selecciona "Método Gráfico"
   - Ingresa la función objetivo
   - Agrega las restricciones (sin incluir X ≥ 0, Y ≥ 0, ya están implícitas)
   - Calcula y verifica resultados
   - **Nota:** El método gráfico solo maneja regiones acotadas

2. **Método Simplex (Ejercicios 9-13B):**
   - Selecciona "Método Simplex"
   - Agrega las variables necesarias
   - Ingresa coeficientes de función objetivo
   - Agrega restricciones
   - Verifica tabla final e iteraciones
   - **Ejercicio 13B:** Prueba detección de problema no acotado

3. **Método Dos Fases (Ejercicios 14-19):**
   - Selecciona "Método 2 Fases"
   - Usa este método cuando tengas restricciones ≥ o =
   - Verifica Fase 1 (W) y Fase 2 (Z)
   - Confirma que W = 0 al final de Fase 1

4. **Casos Especiales (Ejercicios 20-24):**
   - Prueba edge cases
   - Verifica estabilidad numérica
   - Confirma manejo de diferentes tipos de coeficientes

---

## CHECKLIST DE PRUEBAS

### Funcionalidades Básicas:
- [ ] Maximización (Ejercicios 1, 2, 3, 9, 14)
- [ ] Minimización (Ejercicios 7, 12, 16)
- [ ] Solución Única (Ejercicios 1, 2, 5, 8, 9-13, 14-17, 19)
- [ ] Solución Única Degenerada (Ejercicios 3, 13)
- [ ] Soluciones Múltiples (Ejercicio 4)
- [ ] Problema No Acotado (Ejercicio 13B - solo Simplex)
- [ ] Problema No Factible (Ejercicios 6, 18)

### Métodos:
- [ ] Método Gráfico - 2 variables (Ejercicios 1-8)
- [ ] Método Simplex - 3+ variables (Ejercicios 9-13B)
- [ ] Método Dos Fases - restricciones ≥ o = (Ejercicios 14-19)

### Tipos de Restricciones:
- [ ] Restricciones ≤
- [ ] Restricciones ≥
- [ ] Restricciones =
- [ ] Restricciones mixtas

### Casos Especiales:
- [ ] Coeficientes decimales
- [ ] Coeficientes negativos
- [ ] Coeficientes muy grandes
- [ ] Muchas variables (5+)
- [ ] Región factible pequeña

### UI/UX:
- [ ] Modo Coeficientes
- [ ] Modo Forma Natural
- [ ] Vista móvil (restricciones en línea)
- [ ] Tema claro/oscuro
- [ ] Gráficas interactivas (método gráfico)
- [ ] Tablas Simplex con resaltado

---

## REPORTE DE BUGS

Si encuentras algún error durante las pruebas, documenta:

1. **Ejercicio:** Número y nombre del ejercicio
2. **Método:** Gráfico / Simplex / Dos Fases
3. **Entrada:** Datos exactos ingresados
4. **Resultado Esperado:** Según este documento
5. **Resultado Obtenido:** Lo que mostró la calculadora
6. **Tipo de Error:** 
   - Resultado incorrecto
   - Error de cálculo
   - Clasificación incorrecta (tipo de solución)
   - Error visual/UI
   - Crash/Error de sistema

---

**Última actualización:** Enero 2026
**Autor:** William Flores
**Proyecto:** Calculadora de Programación Lineal
