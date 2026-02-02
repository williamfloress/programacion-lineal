# Cómo funciona cada método de Programación Lineal

Este documento explica, paso a paso, el proceso que sigue cada uno de los métodos implementados en el proyecto. Lo escribí para tener claro qué hace cada algoritmo y en qué orden ocurren las cosas.

---

## 1. Método Gráfico

**Cuándo se usa:** Solo cuando el problema tiene **exactamente 2 variables** (por ejemplo x e y). Con más variables no se puede “dibujar” en el plano.

**Idea general:** Las restricciones son rectas en el plano. Esas rectas delimitan una región (polígono o no acotada). El óptimo de una función lineal en esa región siempre está en un **vértice** (o en todo un lado si hay infinitas soluciones). Entonces: calculo todos los vértices, me quedo con los que cumplen todas las restricciones y en esos evalúo Z; el que da el mejor Z es la solución.

### Proceso paso a paso

1. **Definir el problema**  
   Tengo la función objetivo Z (por ejemplo Z = 3x + 2y) y las restricciones (desigualdades o igualdades). También los ejes x ≥ 0 e y ≥ 0.

2. **Calcular intersecciones**  
   Cada restricción es una recta. Además trato x = 0 e y = 0 como rectas.  
   - Cruzo cada par de rectas (restricción i con restricción j, restricción con eje, etc.).  
   - Resuelvo el sistema 2×2 y obtengo un punto (x, y).  
   - Si las rectas son paralelas, no hay un único corte y ese par lo ignoro.

3. **Filtrar puntos factibles**  
   De todos los puntos de corte, me quedo solo con los que:  
   - Cumplen x ≥ 0 e y ≥ 0.  
   - Cumplen **todas** las restricciones (≤, ≥ o = según corresponda).  
   Esos son los vértices de la región factible. Elimino duplicados (a veces dos pares de rectas dan casi el mismo punto por redondeo).

4. **Evaluar Z en cada vértice**  
   En cada vértice factible calculo Z = c₁x + c₂y.  
   - Si el objetivo es **maximizar**: el óptimo es el vértice con Z más grande.  
   - Si es **minimizar**: el óptimo es el vértice con Z más pequeño.

5. **Resultado**  
   - Si no hay ningún punto factible → problema **no factible**.  
   - Si hay un solo vértice con el mejor Z → **solución única**.  
   - Si hay varios vértices con el mismo Z óptimo → **solución múltiple** (cualquier punto del segmento que los une también es óptimo).

---

## 2. Método Simplex

**Cuándo se usa:** Para problemas con **cualquier número de variables**. Es el algoritmo clásico de programación lineal.

**Idea general:** Convierto el problema a “forma estándar” (todas las restricciones en igualdad usando variables de holgura, exceso o artificiales). Armo una tabla donde cada fila es una ecuación (Z y las restricciones). En cada iteración “entra” una variable que mejora Z y “sale” otra para mantener factibilidad; hago un pivoteo y repito hasta que ya no se pueda mejorar (óptimo) o detecte no acotado o no factible.

### Proceso paso a paso

1. **Conversión a forma estándar**  
   - Restricción **≤**: añado una variable de **holgura** (slack) con coeficiente +1. Ejemplo: 2x + y ≤ 10 → 2x + y + s = 10.  
   - Restricción **≥**: añado variable de **exceso** con -1 y una variable **artificial** con +1 (para tener una base factible inicial).  
   - Restricción **=**: solo añado variable **artificial** con +1.  
   La función objetivo se extiende: coeficiente 0 para holgura y exceso, y un valor **M muy grande** (Big M) para las artificiales, para que el algoritmo las expulse lo antes posible.

2. **Tabla inicial**  
   - Fila 0: ecuación de Z en forma Z − c₁x₁ − … = 0 (en la tabla pongo los coeficientes −c_j).  
   - Filas 1 a n: las restricciones (matriz A ampliada y lado derecho b).  
   - Última columna: solución actual (RHS).  
   Las variables básicas iniciales son las de holgura y las artificiales (una por fila de restricción). Actualizo la fila Z para que los coeficientes de las variables básicas sean 0 (queda expresada solo con no básicas).

3. **Iteración (repetir hasta parar)**  
   - **Optimalidad:**  
     - Maximización: si todos los coeficientes en la fila Z son ≥ 0 → **óptimo**, termino.  
     - Minimización: si todos son ≤ 0 → **óptimo**, termino.  
   - **Variable entrante:**  
     - Maximización: elijo la columna con coeficiente **más negativo** en la fila Z (es la que más mejora Z).  
     - Minimización: la columna con coeficiente **más positivo**.  
   - **Variable saliente:**  
     - Calculo el “ratio” para cada fila: (valor en columna solución) ÷ (valor en columna entrante), solo cuando el denominador es positivo.  
     - La variable saliente es la de la fila con **ratio mínimo** (así me mantengo factible).  
   - Si todos los ratios son infinito (denominador ≤ 0 en todas las filas) → problema **no acotado**.  
   - **Pivoteo:**  
     - El “elemento pivote” es el que está en la intersección de la fila saliente y la columna entrante.  
     - Divido toda la fila pivote por ese número (para que el pivote quede 1).  
     - En las demás filas (incluida Z) resto un múltiplo de la fila pivote para dejar 0 en la columna entrante.  
   - Actualizo qué variable es básica en esa fila (entra la entrante, sale la saliente) y repito.

4. **Lectura de la solución**  
   Cuando paro por optimalidad: las variables que están en la base toman el valor del lado derecho (última columna) de su fila; las que no están en la base valen 0. El valor de Z está en la fila 0, columna solución.

5. **Casos especiales**  
   - Si alguna **variable artificial** sigue en la base con valor > 0 → problema **no factible**.  
   - Si hay variables no básicas con coeficiente 0 en la fila Z → **solución múltiple** (infinitas soluciones óptimas).  
   - Si alguna variable básica tiene valor 0 → **degeneración** (solución única pero con un vértice “redundante”).

---

## 3. Método de las Dos Fases

**Cuándo se usa:** Cuando hay restricciones **≥** o **=** y por tanto necesitamos variables artificiales. En lugar de usar Big M en la función objetivo, hacemos dos etapas: primero minimizar la suma de artificiales (Fase 1) y luego, con esa base factible, optimizar la Z original (Fase 2).

**Idea general:** En Fase 1 solo me preocupo de hacer que las artificiales salgan de la base y lleguen a 0 (minimizar W = suma de artificiales). Si logro W = 0, tengo una solución básica factible “real”. En Fase 2 uso esa tabla como punto de partida, cambio la fila W por la fila Z con la función objetivo original y aplico Simplex normal hasta el óptimo.

### Proceso paso a paso

1. **Conversión a forma estándar**  
   Igual que en Simplex: holgura para ≤, exceso + artificial para ≥, solo artificial para =.  
   La diferencia: en la función objetivo **no** pongo Big M. Los coeficientes de las artificiales en Z son 0. Guardo los índices de las columnas de artificiales para la Fase 1.

2. **Fase 1: Minimizar W = suma de variables artificiales**  
   - Defino una nueva función W = suma de todas las variables artificiales. En forma “W − … = 0” pongo coeficiente −1 en cada columna artificial.  
   - Armo la tabla igual que antes (filas de restricciones), pero la fila 0 es la de W, no la de Z.  
   - Aplico Simplex para **minimizar** W:  
     - Variable entrante: la de mayor coeficiente **positivo** en la fila W.  
     - Variable saliente: ratio mínimo como siempre.  
     - Pivoteo y repito hasta que en la fila W no queden coeficientes positivos.  
   - **Si al terminar W > 0:** alguna artificial sigue en la base con valor > 0 → problema **no factible**, termino.  
   - **Si W = 0:** todas las artificiales salieron de la base (o están a 0). La tabla actual es una solución básica factible para el problema original.

3. **Fase 2: Optimizar la función objetivo original Z**  
   - Parto de la tabla final de Fase 1.  
   - Reemplazo la fila 0: en vez de W pongo la fila Z con la función objetivo original (coeficientes −c_j para las x’s y 0 para holgura, exceso y artificiales).  
   - Recalculo el valor actual de Z y expreso la fila Z en términos de variables no básicas (coef. de básicas = 0), usando las filas de restricción.  
   - A partir de ahí aplico **Simplex normal** (igual que en el método Simplex): variable entrante según signo en fila Z, variable saliente por ratio mínimo, pivoteo, hasta optimalidad o no acotado.

4. **Resultado**  
   - Si Fase 1 termina con W > 0 → devuelvo **no factible**.  
   - Si Fase 2 termina con optimalidad → devuelvo la solución óptima (valores de x’s, Z, y si es única, múltiple o degenerada, igual que en Simplex).

---

## Resumen rápido

| Método        | Variables | Idea principal |
|---------------|-----------|------------------|
| **Gráfico**   | Solo 2    | Rectas → vértices → evaluar Z en cada uno y elegir el mejor. |
| **Simplex**   | Cualquiera| Forma estándar + tabla + entrar/salir variable + pivoteo hasta optimalidad (usa Big M si hay ≥ o =). |
| **Dos Fases** | Cualquiera| Igual que Simplex cuando hay ≥ o =, pero en dos etapas: Fase 1 min W (artificiales), Fase 2 opt Z (sin Big M). |

Si algo no cuadra con lo que ves en el código, los comentarios dentro de cada archivo (`metodo_grafico.py`, `metodo_simplex.py`, `metodo_dos_fases.py`) explican línea a línea qué hace cada parte.
