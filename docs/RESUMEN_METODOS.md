# Resumen: Qué hace cada parte del código (3 métodos)

Guía a nivel de código: qué hace cada clase, método y bloque en `metodo_grafico.py`, `metodo_simplex.py` y `metodo_dos_fases.py`.

---

## 1. `metodo_grafico.py`

### Clase `MetodoGrafico`

**`__init__(self, c, A, b, operadores, objetivo='max')`**
- Guarda en atributos: `c` (coef. de Z), `A`, `b`, `operadores` (por fila: `'<=', '>=', '='`), `objetivo` (`'max'`/`'min'`).
- Inicializa `self.vertice = []` (vértices factibles) y `self.pasos = []` (log para la UI).

**`registrar_paso(self, mensaje)`**
- Añade una línea a `self.pasos` para mostrar el proceso al usuario.

**`mostrar_datos(self)`**
- Imprime en consola el objetivo y las restricciones (solo para depuración).

**`encontrar_intersecciones(self)`**
- Construye una matriz con las filas de `A` más dos filas para los ejes `x=0` e `y=0` (`[[1,0],[0,1]]` y b = 0).
- Para cada par de filas (rectas), arma un sistema 2×2 y lo resuelve con `np.linalg.solve`; si hay error (rectas paralelas), hace `continue`.
- Devuelve la lista de puntos (x, y) donde se cortan las rectas.

**`es_factible(self, punto)`**
- Comprueba `x ≥ 0`, `y ≥ 0` (con tolerancia `1e-9`).
- Para cada restricción calcula `np.dot(A[i], punto)` y compara con `b[i]` según `operadores[i]` (`<=`, `>=`, `=`); usa `np.isclose` para `=`.
- Devuelve `True` solo si se cumplen todas.

**`obtener_vertices_validos(self)`**
- Llama a `encontrar_intersecciones()`, filtra con `es_factible()` y elimina duplicados con `np.unique(..., axis=0)`.
- Guarda el resultado en `self.vertice` y lo devuelve.

**`resolver(self)`**
- Escribe en `pasos` la función objetivo y las restricciones (con signos formateados).
- **Intersecciones:** Igual que `encontrar_intersecciones` pero guardando en `intersecciones_info` punto y etiquetas de las rectas, y registrando cada paso.
- **Factibilidad:** Para cada punto de intersección llama a `es_factible`, escribe en `pasos` la comprobación restricción a restricción; si no hay ningún factible → devuelve `status: "infeasible"`.
- **Vértices únicos:** Quita duplicados con un bucle y `np.allclose` (tolerancia `1e-9`), guarda en `self.vertices`.
- **Evaluar Z:** Para cada vértice calcula `np.dot(self.c, v)`, lo guarda en `resultados_vertices`; el óptimo es `max` o `min` de esos Z según `self.objetivo`.
- **Ganadores:** Lista de vértices con Z igual al óptimo (`np.isclose`); si hay más de uno → solución múltiple.
- Devuelve un dict con `status`, `tipo_solucion`, `explicacion`, `z_optimo`, `punto_optimo`, `vertices`, `puntos_ganadores`, `pasos`.

---

## 2. `metodo_simplex.py`

### Clase `MetodoSimplex`

**`__init__`**
- Guarda `c`, `A`, `b`, `operadores`, `objetivo` como arrays NumPy; `self.pasos = []` (log) y `self.tablas = []` (cada tabla para la UI).

**`registrar_paso(self, mensaje)`**
- Añade una línea a `self.pasos`.

**`_convertir_a_nativo(self, valor)`**
- Convierte tipos NumPy (`np.int64`, `np.float64`, arrays, etc.) a `int`/`float`/listas/dicts nativos para que el front pueda serializar a JSON; `inf`/`-inf` → `None`.

**`registrar_tabla(self, ...)`**
- Convierte la tabla a tipos nativos, trata los ratios con `inf` → `None`, y hace `self.tablas.append({ iteracion, tabla, variables_basicas, explicacion, nombres_columnas, col_entrante, fila_saliente, elemento_pivote, ratios })` para guardar cada “foto” de la tabla.

**`convertir_forma_estandar(self)`**
- Cuenta holguras (`<=`), excesos y artificiales (`>=`, `=`) según `operadores`.
- Crea `A_estandar`: misma cantidad de filas, columnas = x’s + holguras + excesos + artificiales. Por fila:
  - Copia `A[i]` en las primeras columnas.
  - `<=`: añade columna con 1 (holgura).
  - `>=`: añade -1 (exceso) y luego 1 (artificial).
  - `=`: añade solo 1 (artificial).
- Construye `c_estandar`: coef. originales para x’s, 0 para holgura/exceso, y `M = 10000` para cada artificial (Big M).
- Devuelve `(A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales)`.

**`resolver(self)`**
- Escribe en `pasos` el título, la función objetivo y las restricciones.
- Llama a `convertir_forma_estandar()` y obtiene tamaños (`num_rest`, `num_cols_totales`).
- **Base inicial:** Recorre `operadores` y llena `variables_basicas` (nombres `s1`, `a1`, …) e `indices_basicas` (índices de columna): holguras y artificiales según corresponda.
- **Tabla inicial:** Matriz `(num_rest+1) x (num_cols_totales+1)`. Filas 1..num_rest = `A_estandar` y última columna = `b`. Fila 0 = fila Z: `-c_estandar` en columnas de variables; RHS de Z = suma de (coef. en c de variable básica × b de esa fila). Luego hace combinaciones de filas para que en la fila Z los coeficientes de las variables básicas queden en 0 (reescribir Z en términos de no básicas).
- Genera `nombres_columnas` (x1, s1, e1, a1, …) y llama a `registrar_tabla` para la tabla inicial.
- **Bucle de iteraciones (máx 100):**
  - **Optimalidad:** Lee `fila_z = tabla[0, :num_cols_totales]`. Si max: si no hay negativos → `break` (óptimo). Si min: si no hay positivos → `break`. Si no, elige **variable entrante**: columna con el coeficiente más negativo (max) o más positivo (min) en la fila Z.
  - **Ratios:** Para cada fila de restricción, si el coef. en la columna entrante > 0, ratio = RHS / ese coef.; si no, ratio = `np.inf`. Si todos son `inf` → devuelve `status: "unbounded"` y serializa tablas.
  - **Variable saliente:** Índice de fila con ratio mínimo (`np.argmin(ratios)`).
  - **Pivoteo:** Actualiza `variables_basicas` e `indices_basicas` (la entrante sustituye a la saliente). Elemento pivote = intersección fila saliente × columna entrante. Divide la fila pivote por el elemento pivote; luego para cada otra fila (incluida Z) resta `(coef. en col. entrante) × fila_pivote` para dejar 0 en esa columna.
  - Escribe en `pasos` y llama a `registrar_tabla` con la nueva tabla, entrante, saliente, pivote y ratios.
- **Solución:** Construye `solucion` (array de ceros para las x’s): para cada variable básica que sea x (índice < num_vars), asigna el valor del RHS de su fila. `z_optimo = tabla[0, -1]`.
- **Infactibilidad:** Si hay artificiales y alguna sigue en la base con valor > 0 (RHS de su fila), devuelve `status: "infeasible"` y serializa tablas.
- **Tipo de solución:** Revisa si hay variables no básicas (no artificiales) con coef. 0 en la fila Z y si al pivotar en ellas el ratio mínimo sería > 0 → solución múltiple. Si hay variables básicas con valor 0 → degenerada. Si no → única.
- Serializa todas las tablas con `_convertir_a_nativo` y devuelve el dict con `status`, `tipo_solucion`, `explicacion`, `z_optimo`, `solucion`, `iteraciones`, `pasos`, `tablas`, `variables_basicas`.

---

## 3. `metodo_dos_fases.py`

### Clase `MetodoDosFases`

**`__init__`**
- Igual que Simplex: guarda `c`, `A`, `b`, `operadores`, `objetivo`; `pasos = []`, `tablas = []`.

**`registrar_paso`**, **`_convertir_a_nativo`**
- Misma idea que en Simplex: log y conversión a tipos serializables.

**`registrar_tabla(self, ..., fase=1)`**
- Igual que en Simplex pero cada entrada en `self.tablas` incluye `"fase": 1 o 2` para distinguir Fase 1 y Fase 2.

**`convertir_forma_estandar(self)`**
- Igual que en Simplex en cuanto a construir `A_estandar` (holgura, exceso, artificiales por fila) y `c_estandar` (solo coef. originales; 0 para holgura, exceso y artificiales; **no** usa Big M). Además guarda `indices_artificiales` (lista de índices de columna donde están las artificiales) para la Fase 1.
- Devuelve `(A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales)`.

**`fase1(self, A_estandar, num_vars, ...)`**
- Si `num_artificiales == 0` → devuelve `(True, None, None, None)` (no hay Fase 1).
- Construye base inicial igual que Simplex (holguras y artificiales) → `variables_basicas`, `indices_basicas`.
- Arma la tabla: filas de restricciones = `A_estandar` y RHS = `b`. Fila 0 = fila **W**: pone -1 en cada columna de `indices_artificiales` (minimizar W = suma de artificiales). Luego reexpresa la fila W con combinaciones de filas para que los coef. de las básicas sean 0.
- Genera `nombres_columnas` en el mismo orden que las columnas de `A_estandar` y registra la tabla inicial (fase=1).
- **Bucle Simplex para minimizar W:** Variable entrante = columna con mayor coef. positivo en la fila W. Ratios como en Simplex; saliente = ratio mínimo. Pivoteo (normalizar fila pivote, luego eliminar la columna entrante en el resto). Registra cada tabla con `fase=1`.
- Al salir del bucle: si `abs(tabla[0,-1]) > 1e-6` (W ≠ 0) → devuelve `(False, tabla, variables_basicas, indices_basicas)` (infactible). Si no → `(True, tabla, variables_basicas, indices_basicas)`.

**`fase2(self, tabla_fase1, variables_basicas, indices_basicas, c_estandar, ...)`**
- Si `tabla_fase1 is None` (no hubo artificiales): construye una tabla desde cero solo con holguras, fila Z = `-c_estandar`, base = holguras.
- Si no: copia la tabla de Fase 1, sustituye la fila 0 por la fila Z: `tabla[0, :num_cols] = -c_estandar`, `tabla[0, -1] = 0`, y con un bucle reexpresa la fila Z para que los coef. de las variables básicas actuales sean 0 (restar múltiplo de cada fila de restricción).
- Genera `nombres_columnas` y registra la tabla inicial de Fase 2 (fase=2).
- **Bucle Simplex para Z:** Misma lógica que en `MetodoSimplex.resolver`: entrante por fila Z (max/min), ratios, saliente, pivoteo. Si todos los ratios son `inf` → devuelve `status: "unbounded"` y serializa tablas.
- **Solución:** Igual que Simplex: variables x básicas = RHS de su fila; `z_optimo = tabla[0, -1]`.
- **Tipo de solución:** Misma lógica que en Simplex (vars. no básicas con coef. 0 en Z y ratio > 0 → múltiple; básicas con valor 0 → degenerada).
- Serializa `self.tablas` y devuelve el dict con `status`, `tipo_solucion`, `explicacion`, `z_optimo`, `solucion`, `iteraciones`, `pasos`, `tablas`.

**`resolver(self)`**
- Escribe en `pasos` el título, objetivo y restricciones.
- Llama a `convertir_forma_estandar()`.
- Llama a `fase1(...)`. Si devuelve `factible == False` → devuelve `status: "infeasible"` y tablas serializadas.
- Llama a `fase2(tabla_fase1, variables_basicas, indices_basicas, c_estandar, ...)` y devuelve su resultado.

---

## Flujo rápido por archivo

| Archivo              | Entrada      | Salida principal                                      |
|----------------------|-------------|--------------------------------------------------------|
| `metodo_grafico.py`  | `resolver()`| Dict con `z_optimo`, `punto_optimo`, `vertices`, `pasos` |
| `metodo_simplex.py`  | `resolver()`| Dict con `z_optimo`, `solucion`, `tablas`, `pasos`     |
| `metodo_dos_fases.py`| `resolver()`| Igual que Simplex; las tablas incluyen `fase` 1 o 2    |

En los tres, `pasos` es la lista de mensajes que consume la interfaz para mostrar el proceso paso a paso. Simplex y Dos Fases además rellenan `tablas` para mostrar cada tabla en la UI.
