# Método de 2 Fases: Análisis e Implementación

Este documento describe el análisis y el plan de implementación para añadir el **Método de las Dos Fases** a la calculadora de Programación Lineal, manteniendo el mismo flujo que los métodos Gráfico y Simplex.

---

## 1. Qué es el método de 2 fases

### 1.1 Concepto

Es una variante del Simplex usada cuando el problema tiene restricciones **≥** o **=**. En esos casos se añaden **variables artificiales** para obtener una base inicial. En lugar de usar un coeficiente “M” muy grande (Big M), el método divide el proceso en dos fases:

- **Fase 1:** Se minimiza la función auxiliar **W = suma de variables artificiales**. Se aplica Simplex hasta que W = 0. Si se logra, tenemos una solución básica factible para el problema original (con todas las artificiales fuera de la base o en cero). Si el óptimo de W > 0, el problema es **no factible**.
- **Fase 2:** Se elimina W y las columnas de variables artificiales (o se dejan en 0). Se restaura la **función objetivo original Z** y se continúa Simplex desde la base obtenida en Fase 1 hasta alcanzar el óptimo.

### 1.2 Cuándo se usa

- Hay al menos una restricción **≥** o **=** (y por tanto variables artificiales).
- Se quiere evitar el uso de **Big M** (mejor estabilidad numérica y claridad didáctica).

Si **todas** las restricciones son **≤**, no hay artificiales y basta el Simplex estándar (una sola fase). Aún así, la calculadora puede ofrecer siempre la pestaña “2 Fases” y, en ese caso, usarlo solo cuando haya ≥ o =, o aplicar directamente Simplex en un solo bloque cuando no haya artificiales (equivalente a “Fase 2 solamente”).

### 1.3 Relación con el Simplex actual del proyecto

- El **Simplex actual** (`MetodoSimplex` en `solver.py`) ya contempla **≤**, **≥** y **=**, con holgura, exceso y variables artificiales, y usa **Big M** para las artificiales.
- El **Método de 2 Fases** sustituye Big M por las dos fases anteriores. El formato de entrada (función objetivo, restricciones) es el **mismo** que en Simplex.

---

## 2. Flujo actual de Gráfico y Simplex (resumen)

Para replicar el mismo flujo:

| Aspecto | Gráfico | Simplex |
|--------|---------|---------|
| **Tab** | "Método Gráfico" | "Método Simplex" |
| **Sección** | `#metodo-grafico` | `#metodo-simplex` |
| **Entrada** | Objetivo (max/min), Z con 2 vars, restricciones (coef. o natural) | Objetivo, Z con N vars, restricciones (coef. o natural) |
| **Acción** | "CALCULAR SOLUCIÓN" → `resolverProblema()` | "CALCULAR SOLUCIÓN (SIMPLEX)" → `resolverSimplex()` |
| **API** | `POST /calcular` | `POST /calcular-simplex` |
| **Resultados** | `#resultados`: resumen, detalles (toggle), gráfica, tabla vértices, análisis final | `#resultados-simplex`: resumen, detalles (toggle), tablas Simplex, análisis final |
| **Cambio de método** | `cambiarMetodo('grafico' \| 'simplex')` muestra/oculta secciones y resultados |

El método de 2 Fases debe seguir este mismo patrón: tab propio, sección propia, formulario, botón de calcular, endpoint propio y panel de resultados análogo al de Simplex.

---

## 3. Decisiones de diseño

### 3.1 Entrada de datos

- **Misma estructura que Simplex:** objetivo (max/min), coeficientes de Z, restricciones (coeficientes + operador + término derecho). Mismo soporte para **Coeficientes** y **Forma natural**.
- **Mismas restricciones:** N variables, operadores **≤**, **≥**, **=**.

Por tanto, el **formulario** del método de 2 Fases será estructuralmente idéntico al de Simplex (objetivo, Z, lista de restricciones, modo coeficientes/natural, botón calcular).

### 3.2 Reutilización de conversión “forma natural”

- Reutilizar el endpoint **`POST /convertir-restricciones-simplex`** y la lógica existente. El método de 2 Fases solo consume restricciones ya en formato coeficientes.

### 3.3 Backend

- **Nueva ruta:** `POST /calcular-dos-fases`.
- **Payload:** mismo que `/calcular-simplex`:
  ```json
  { "objetivo": "max"|"min", "z_coefs": [...], "restricciones": [ { "coefs": [...], "op": "<="|">="|"=", "val": number } ] }
  ```
- **Nueva clase en `solver.py`:** `MetodoDosFases`. Misma entrada que `MetodoSimplex` (`c`, `A`, `b`, `operadores`, `objetivo`). Implementa las dos fases y devuelve un resultado con estructura compatible con el frontend (ver más abajo).

### 3.4 Estructura de la respuesta del backend

Misma estructura que Simplex para facilitar la UI:

- `status`: `"optimal"` | `"infeasible"` | `"unbounded"`.
- `tipo_solucion`: texto breve (ej. "Solución Única", "Problema No Factible", "Problema No Acotado").
- `explicacion`: párrafo explicativo.
- `z_optimo`: número (cuando `status === 'optimal'`).
- `solucion`: array de valores de las variables de decisión.
- `pasos`: array de strings (log de pasos).
- `tablas`: array de tablas para la UI.

Para 2 Fases, `tablas` incluirá tablas de **Fase 1** y **Fase 2**. Cada elemento puede llevar un campo `fase: 1 | 2` para que el frontend las agrupe y muestre en bloques “Fase 1” y “Fase 2”. Si se prefiere, se pueden devolver `tablas_fase1` y `tablas_fase2` por separado; la implementación puede elegir una u otra y documentarla.

### 3.5 Frontend

- **Nuevo tab:** "Método 2 Fases" en la misma barra de tabs que Gráfico y Simplex.
- **Nueva sección:** `#metodo-dos-fases`, con el mismo layout que `#metodo-simplex`:
  - Objetivo (select).
  - Z (contenedor de coeficientes y operadores, botones +/- variable).
  - Restricciones (modo Coeficientes / Forma natural, lista, +/- restricción).
  - Botón **"CALCULAR SOLUCIÓN (2 FASES)"** que dispara `resolverDosFases()`.
- **Nuevo panel de resultados:** `#resultados-dos-fases`, análogo a `#resultados-simplex`:
  - Cabecera “Pasos del Método de 2 Fases” y botón “Ver Detalles” (toggle).
  - Resumen (`#calculations-summary-dos-fases`), log expandible (`#log-container-dos-fases`).
  - Bloque “Tablas” (Fase 1 y Fase 2) y caja de análisis final con `#titulo-tipo-solucion-dos-fases`, `#texto-explicacion-dos-fases`, `#caja-resultado-final-dos-fases`.
- **`cambiarMetodo('dos-fases')`:** Mostrar/ocultar `#metodo-dos-fases` y `#resultados-dos-fases` igual que con Simplex; ocultar resultados de Gráfico y Simplex. Inicializar restricciones si al entrar no hay ninguna (como en Simplex). Actualmente `cambiarMetodo` activa el tab según si el botón contiene "Gráfico" o "Simplex"; habrá que extender la lógica para un tercer tab (p. ej. `metodo === 'dos-fases'` → botón cuyo texto contenga "2 Fases").
- **`resolverDosFases()`:** Obtener datos del formulario de 2 Fases (misma lógica que `resolverSimplex`), `POST /calcular-dos-fases`, y rellenar `#resultados-dos-fases` (resumen, log, tablas, análisis).

### 3.6 Persistencia y compartir datos (Checkpoint 3)

Si más adelante se implementa persistencia entre métodos (Checkpoint 3), el modelo canónico puede incluir “método activo” (gráfico | simplex | dos-fases). El método de 2 Fases usará el mismo formato de datos que Simplex, por lo que no requiere cambios adicionales en la estructura de persistencia más allá de poder guardar/restaurar ese tab.

---

## 4. Implementación en backend (`solver.py`)

### 4.1 Clase `MetodoDosFases`

- **`__init__(self, c, A, b, operadores, objetivo='max')`**  
  Igual que `MetodoSimplex`: mismos parámetros y significando.

- **Forma estándar y variables auxiliares:**  
  Reutilizar la lógica de `MetodoSimplex.convertir_forma_estandar()` (holgura, exceso, artificiales) o factorizarla en una función común. No usar Big M para las artificiales.

- **Fase 1:**
  - Función objetivo auxiliar: **min W = suma de variables artificiales** (coeficientes 1 para artificiales, 0 para el resto).
  - Construir tabla inicial con fila W en lugar de Z.
  - Aplicar Simplex (minimización) hasta que W = 0 o se detecte no factible / no acotado.
  - Registrar cada iteración en `self.pasos` y guardar tablas con `fase: 1`.

- **Criterios de parada Fase 1:**
  - **W = 0** y todas las artificiales fuera de la base (o con valor 0): éxito → pasar a Fase 2.
  - **Óptimo de W > 0:** problema **no factible**. Devolver `status: "infeasible"`, `tipo_solucion`, `explicacion`, `pasos`, `tablas` (solo Fase 1).
  - **No acotado en Fase 1:** en la práctica, si se minimiza W, suele indicar error en el modelo o en la implementación; definir manejo explícito (ej. `infeasible` o `unbounded` según convenga).

- **Fase 2:**
  - Partir de la última tabla de Fase 1.
  - Eliminar columnas de variables artificiales (o fijarlas en 0). Eliminar la fila W.
  - Restaurar la fila Z con la función objetivo original y actualizar los costos reducidos (fila Z expresada en términos de variables no básicas) usando la base actual.
  - Aplicar Simplex estándar (max o min según `objetivo`) hasta optimalidad o no acotado.
  - Registrar pasos y tablas con `fase: 2`.

- **Salida:**  
  Misma estructura que `MetodoSimplex.resolver()`: `status`, `tipo_solucion`, `explicacion`, `z_optimo`, `solucion`, `pasos`, `tablas` (y opcionalmente `iteraciones`). Incluir en `tablas` tanto las de Fase 1 como las de Fase 2, con `fase` en cada una.

### 4.2 Casos sin variables artificiales

- Si **todas** las restricciones son **≤**: no hay artificiales. Opciones:
  - **A)** Considerar que “2 Fases” no aplica y devolver mensaje o redirigir a Simplex.
  - **B)** Ejecutar solo Fase 2 (Simplex estándar) sin Fase 1, y devolver el resultado con `tablas` solo de Fase 2.

La opción **B** simplifica la UX: el usuario siempre puede elegir “2 Fases” y obtener una solución coherente.

---

## 5. Implementación en backend (`app.py`)

- Añadir ruta:

```python
@app.route('/calcular-dos-fases', methods=['POST'])
def calcular_dos_fases():
    data = request.json
    c = [float(x) for x in data['z_coefs']]
    objetivo = data['objetivo']
    restricciones = data['restricciones']
    A = [[float(x) for x in r['coefs']] for r in restricciones]
    b = [float(r['val']) for r in restricciones]
    operadores = [r['op'] for r in restricciones]
    solver = MetodoDosFases(c, A, b, operadores, objetivo)
    return jsonify(solver.resolver())
```

- Importar `MetodoDosFases` desde `solver`.

---

## 6. Implementación en frontend

### 6.1 `index.html`

- **Tabs:** Añadir botón "Método 2 Fases" y `onclick="cambiarMetodo('dos-fases')"`.
- **Sección `#metodo-dos-fases`:**  
  Copiar la estructura de `#metodo-simplex` y adaptar IDs y llamadas:
  - `#objetivo-dos-fases`, `#z-coefs-container-dos-fases`, `#lista-restricciones-dos-fases`, etc.
  - Modo Coeficientes / Forma natural: `#modo-coeficientes-dos-fases`, `#modo-natural-dos-fases`, `#restricciones-natural-dos-fases`.
  - Botones de modo, agregar/eliminar restricción, agregar/eliminar variable.
  - Botón "CALCULAR SOLUCIÓN (2 FASES)" → `onclick="resolverDosFases()"`.
- **Resultados `#resultados-dos-fases`:**  
  Misma estructura que `#resultados-simplex`: cabecera, toggle “Ver Detalles”, `#calculations-summary-dos-fases`, `#log-container-dos-fases`, bloque de tablas, `#analisis-box-dos-fases` con título, explicación y caja de resultado final.

### 6.2 `main.js`

- **`cambiarMetodo(metodo)`:**  
  Incluir `'dos-fases'`. Mostrar/ocultar `#metodo-dos-fases` y `#resultados-dos-fases`; ocultar resultados de Gráfico y Simplex. Al activar 2 Fases, si hay variables y no hay restricciones, añadir una restricción por defecto (igual que en Simplex).

- **Formulario 2 Fases:**  
  Replicar la lógica de Simplex para:
  - Objetivo, Z (coefs y operadores), agregar/eliminar variable.
  - Restricciones: agregar/eliminar, modo coeficientes/natural.
  - Conversión desde forma natural: reutilizar `convertir-restricciones-simplex` (mismo payload; se puede extraer una función común que prepare el body y llame al endpoint, luego actualice el formulario correspondiente).

- **`resolverDosFases()`:**  
  - Leer objetivo, `z_coefs` y restricciones del formulario de 2 Fases (igual que en `resolverSimplex`).
  - `POST /calcular-dos-fases` con ese payload.
  - Mostrar `#resultados-dos-fases`.
  - Rellenar resumen, log (toggle) y análisis final (`#titulo-tipo-solucion-dos-fases`, `#texto-explicacion-dos-fases`, `#caja-resultado-final-dos-fases`).
  - Llamar a una función de renderizado de tablas para 2 Fases (ver abajo).

- **Tablas 2 Fases:**  
  - Opción **A:** Nueva función `mostrarTablasDosFases(datos)` que recorre `datos.tablas`, agrupa por `fase` y muestra dos bloques “Fase 1” y “Fase 2”, cada uno con sus tablas usando la misma estructura de tabla que `mostrarTablasSimplex` (reutilizar estilos y estructura de `<table>`).
  - Opción **B:** Reutilizar `mostrarTablasSimplex` (o una versión genérica `mostrarTablasSimplex(datos, containerId, options)`) y pasar `datos` del método de 2 Fases, diferenciando solo el contenedor y, si hace falta, títulos por `fase`.  
  Cualquiera de las dos es válida; la **A** suele dar más control para textos específicos de “Fase 1” / “Fase 2”.

- **Toggles y logs:**  
  Implementar `toggleCalculationsDosFases()` análogo a `toggleCalculationsSimplex()`, y rellenar `#log-container-dos-fases` con `datos.pasos` cuando se usen los detalles.

### 6.3 CSS

- Reutilizar estilos de Simplex (`.simplex-table-container`, `.simplex-table`, etc.) para las tablas de 2 Fases.
- Si se añaden bloques “Fase 1” / “Fase 2”, usar títulos o badges (ej. `.fase-badge`) para distinguirlos visualmente; mantener coherencia con el resto de la app.

---

## 7. Orden sugerido de implementación

1. **Backend – `MetodoDosFases` en `solver.py`**
   - Implementar Fase 1 (min W, tablas, parada).
   - Implementar Fase 2 (quitar artificiales, restaurar Z, Simplex hasta óptimo).
   - Caso sin artificiales: solo Fase 2.
   - Devolver siempre `status`, `tipo_solucion`, `explicacion`, `z_optimo`, `solucion`, `pasos`, `tablas` con `fase` en cada tabla.

2. **Backend – `app.py`**
   - Ruta `POST /calcular-dos-fases` y uso de `MetodoDosFases`.

3. **Frontend – HTML**
   - Nuevo tab “Método 2 Fases”.
   - Sección `#metodo-dos-fases` y panel `#resultados-dos-fases` según sección 6.1.

4. **Frontend – JS**
   - `cambiarMetodo('dos-fases')` y lógica de visibilidad e inicialización.
   - Funciones de formulario 2 Fases (objetivo, Z, restricciones, natural).
   - `resolverDosFases()` y llamada a `mostrarTablasDosFases` (o equivalente).
   - Toggle de detalles y relleno de resumen/log.

5. **Frontend – Tablas y estilos**
   - `mostrarTablasDosFases` (o ampliación de `mostrarTablasSimplex`) y estilos necesarios.

6. **Pruebas**
   - Problema solo con **≤**: sin artificiales, solo Fase 2; solución igual que Simplex.
   - Problema con **≥** o **=**: Fase 1 + Fase 2; comprobar que no quedan artificiales en la base y que Z coincide con Simplex (si ambos son aplicables).
   - Problema no factible (restricciones contradictorias): Fase 1 con W > 0, `status: "infeasible"`.
   - Verificar que el flujo (tabs, formulario, calcular, resultados) es igual al de Gráfico y Simplex.

---

## 8. Resumen

| Componente | Acción |
|------------|--------|
| **Entrada** | Igual que Simplex (objetivo, Z, restricciones; coef. o natural). |
| **Backend** | `MetodoDosFases` en `solver.py`, ruta `POST /calcular-dos-fases` en `app.py`. |
| **Frontend** | Tab “Método 2 Fases”, sección `#metodo-dos-fases`, resultados `#resultados-dos-fases`, `resolverDosFases()`, tablas con Fase 1 y Fase 2. |
| **Flujo** | Mismo que Gráfico y Simplex: tab → formulario → Calcular → resultados (resumen, detalles, tablas, análisis). |

Con esto se incorpora el Método de 2 Fases a la calculadora manteniendo un flujo uniforme con los métodos ya existentes y reutilizando tanto la conversión de restricciones como los estilos y la estructura de resultados del Simplex.

---

## 9. Notas adicionales

- **Convertir restricciones (forma natural):** El método de 2 Fases usa el mismo formato de restricciones que Simplex. Se reutiliza `POST /convertir-restricciones-simplex` y el mismo flujo de “Convertir a Coeficientes” en el formulario de 2 Fases.
- **Duplicación de formulario:** El formulario de 2 Fases es una réplica del de Simplex (mismos campos y modos). Si en el futuro se unifican Simplex y 2 Fases en una sola sección con selector interno “Simplex” vs “2 Fases”, se podría tener un único formulario y solo cambiar el endpoint al calcular. Por ahora, mantener secciones separadas conserva el flujo idéntico a Gráfico y Simplex.
- **Estabilidad numérica:** El método de 2 Fases evita el uso de M grande, lo que puede dar mejores resultados en algunos problemas que con Big M en el Simplex actual.
