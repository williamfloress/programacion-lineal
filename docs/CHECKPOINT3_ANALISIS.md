# Análisis y pasos para Checkpoint 3: Persistencia de Datos entre Métodos

Este documento recoge el análisis del flujo actual de datos, las decisiones de diseño y los pasos recomendados **antes** de implementar la persistencia. No incluye cambios de código; es la fase de planificación.

---

## 1. Flujo actual de datos

### 1.1 Dónde viven los datos

| Método | Función objetivo | Restricciones (coef.) | Restricciones (natural) |
|--------|------------------|------------------------|--------------------------|
| **Gráfico** | `#objetivo`, `#z-coefs-container-grafico` (`.z-coef-grafico`, `.z-op-grafico`) | `#lista-restricciones` (`.fila-restriccion`: `.res-x`, `.res-y`, `.res-op-var`, `.res-op`, `.res-val`) | `#restricciones-natural` |
| **Simplex** | `#objetivo-simplex`, `#z-coefs-container` (`.z-coef`, `.z-op`) | `#lista-restricciones-simplex` (`.fila-restriccion-simplex`: `.res-coef`, `.res-op-var-simplex`, `.res-op-simplex`, `.res-val-simplex`) | `#restricciones-natural-simplex` |

- Los formularios de Gráfico y Simplex son **independientes**: IDs, clases y contenedores distintos.
- No hay estado compartido en JS: todo se lee y escribe en el DOM.

### 1.2 Qué hace `cambiarMetodo(metodo)`

- Activa/desactiva tabs y muestra/oculta `#metodo-grafico` y `#metodo-simplex`.
- Oculta ambos paneles de resultados.
- **Solo al pasar a Simplex:** si hay variables en la función objetivo y **no** hay filas en `#lista-restricciones-simplex`, llama a `agregarRestriccionSimplex()` para crear una restricción por defecto.
- **No** copia datos de un método al otro ni lee/escribe `localStorage`.

### 1.3 Dónde se “pierden” los datos

- No se borran al cambiar de método: cada formulario conserva su propio estado en el DOM.
- El “problema” es que **no se comparten**:
  - Usuario rellena Gráfico → cambia a Simplex → ve el estado por defecto (o el de Simplex), no el de Gráfico.
  - Y al revés: lo editado en Simplex no se refleja en Gráfico.
- Al **recargar la página**, todo vuelve a los valores por defecto del HTML (p. ej. Z = 3x + 2y, dos restricciones iniciales en Gráfico, Simplex sin restricciones).

### 1.4 Cómo se envían los datos al backend

- **Gráfico** (`/calcular`):  
  `{ objetivo, z_x, z_y, restricciones: [ { x, y, op, val } ] }`  
  Solo 2 variables. El signo entre x e y se aplica en frontend (`.res-op-var` → `y` puede ser negativo).

- **Simplex** (`/calcular-simplex`):  
  `{ objetivo, z_coefs, restricciones: [ { coefs, op, val } ] }`  
  N variables. Los signos entre variables se aplican en los `coefs` antes de enviar.

### 1.5 Modos de entrada de restricciones

- Ambos métodos tienen **Coeficientes** y **Forma natural**.
- En “natural” se usa el textarea y luego “Convertir a coeficientes”, que **sobrescribe** la lista de restricciones en modo coeficientes.
- Es decir: el estado “verdadero” que se usa para calcular es el de coeficientes; natural es solo otra forma de editarlo.

---

## 2. Requisitos del Checkpoint 3 (resumidos)

- Analizar flujo de datos e identificar pérdida al cambiar de método.
- Decidir estrategia de almacenamiento y estructura de datos.
- Guardar automáticamente: función objetivo al ingresarla, cada restricción al agregar/modificar, método seleccionado.
- Restaurar: al cambiar de método, al recargar, y mantener datos durante la sesión.
- Sincronizar: mismo modelo para ambos métodos, ambos formularios actualizados cuando cambia un dato.

---

## 3. Decisiones de diseño

### 3.1 Estrategia de almacenamiento

| Opción | Pros | Contras |
|--------|------|--------|
| **Solo memoria** | Simple, sin I/O | Se pierde al recargar. No cumple “recargar y mantener datos”. |
| **`sessionStorage`** | Persiste al recargar en la misma pestaña | Se pierde al cerrar pestaña. Menos predecible que `localStorage` para “mis últimos datos”. |
| **`localStorage`** | Persiste recargas y cierre del navegador, ya se usa para tema | Hay que definir clave y formato. Datos pueden quedar obsoletos si cambiamos estructura (versión). |

**Recomendación:** **`localStorage`** como almacén persistente, y **objeto en memoria** como fuente de verdad durante la sesión. Al cargar la página, se intenta restaurar desde `localStorage` al modelo en memoria; luego, ese modelo es el que se usa y se persiste.

- Checkpoint y `CHECKPOINTS.md` ya apuntan a `localStorage`.
- Consistente con el uso actual de `localStorage` para el tema.

### 3.2 Estructura de datos canónica

Representación única que sirve para ambos métodos y para persistir:

```json
{
  "version": 1,
  "objetivo": "max",
  "z_coefs": [3, 2],
  "restricciones": [
    { "coefs": [2, 1], "op": "<=", "val": 100 },
    { "coefs": [1, 1], "op": "<=", "val": 80 }
  ],
  "ultimoMetodo": "grafico"
}
```

- **`version`:** por si en el futuro cambiamos el formato; permite migración o descarte de datos antiguos.
- **`objetivo`:** `"max"` | `"min"`.
- **`z_coefs`:** array de coeficientes **efectivos** (con signo ya aplicado). Compatible con Simplex. Para Gráfico se usan `z_coefs[0]` y `z_coefs[1]`.
- **`restricciones`:** cada una con `coefs`, `op`, `val`. Misma forma que Simplex. Para Gráfico (2 vars) se usan `coefs[0]` y `coefs[1]`.
- **`ultimoMetodo`:** `"grafico"` | `"simplex"`. Útil para restaurar tab activo y para “recordar” preferencia.

**Por qué esta estructura:**

- Simplex ya trabaja con `z_coefs` y `restricciones[].coefs`. Gráfico puede mapearse a esto sin problema.
- Un solo modelo evita duplicar lógica y fuentes de verdad.
- Facilita guardar/restaurar en un solo objeto JSON.

### 3.3 Mapeo Gráfico ↔ modelo canónico

- **Gráfico → modelo:**  
  - `objetivo` ← `#objetivo`.  
  - `z_coefs` ← `[z_x, z_y]` aplicando `z_op_y` (+/−) a `z_y`.  
  - Por cada `.fila-restriccion`: `coefs = [x, y]` (aplicando `res-op-var` a `y`), `op` ← `res-op`, `val` ← `res-val`.

- **Modelo → Gráfico:**  
  - Solo si `z_coefs.length >= 2`. Usar `z_coefs[0]`, `z_coefs[1]`.  
  - Signo de `z_coefs[1]`: si `< 0`, `res-op-var = '-'` y guardar `|z_coefs[1]|` en el input.  
  - Restricciones: solo las que tengan `coefs.length >= 2`; se rellenan `res-x`, `res-y`, `res-op-var`, `res-op`, `res-val` y se reconstruyen filas en `#lista-restricciones` (limpiando las actuales).

### 3.4 Mapeo Simplex ↔ modelo canónico

- **Simplex → modelo:**  
  - `objetivo` ← `#objetivo-simplex`.  
  - `z_coefs` ← lo que ya se calcula para el payload (coefs con signo de `.z-op`).  
  - Por cada `.fila-restriccion-simplex`: `coefs` con signos de `.res-op-var-simplex`, `op` y `val` de los correspondientes selects/inputs.

- **Modelo → Simplex:**  
  - Rellenar `#objetivo-simplex`.  
  - Reconstruir `#z-coefs-container` (inputs y operadores) según `z_coefs.length`.  
  - Vaciar `#lista-restricciones-simplex` y volver a crear filas para cada restricción con `agregarRestriccionSimplexDesdeDatos` o equivalente, usando `coefs`, `op`, `val`.

### 3.5 Restricción a 2 variables en Gráfico

- Gráfico solo puede **mostrar** 2 variables. El modelo puede tener N.
- Si `z_coefs.length > 2`:
  - **Gráfico:** usar solo `z_coefs[0]` y `z_coefs[1]` (o mostrar mensaje tipo “Solo se representan x₁, x₂”).
  - Al editar en Gráfico, seguimos modificando solo esas dos dimensiones; el resto de `z_coefs` y de `restricciones[].coefs` se mantiene (o se define regla explícita, p. ej. “solo permitir edición Gráfico cuando hay 2 vars”).
- Decisión recomendada para una primera versión: **solo sincronizar Gráfico cuando hay exactamente 2 variables**. Si en Simplex se agrega una 3.ª variable, se puede ocultar/deshabilitar Gráfico o mostrar advertencia hasta volver a 2 variables.

### 3.6 Modo “forma natural”

- **No** persistir el texto de los textareas de forma natural.
- Persistir solo el modelo en coeficientes. Al restaurar, se rellenan los modos **Coeficientes** de ambos métodos.
- Si el usuario tenía “natural” abierto, al cambiar de método o recargar volverá a coeficientes con los datos restaurados. Opcional: restaurar también el “modo” activo (coef/natural) por método; si se hace, habría que generar natural desde coefs o dejarlo vacío.

### 3.7 Dónde persistir “método seleccionado”

- Incluirlo en el modelo canónico como `ultimoMetodo` y guardarlo en `localStorage` junto con el resto.
- Al cargar la página, restaurar modelo y luego activar el tab correspondiente (`cambiarMetodo(ultimoMetodo)`).

### 3.8 Cuándo guardar

- **Al editar:**
  - Cambio en objetivo (select).
  - Cambio en coeficientes de Z (inputs/operadores).
  - Añadir / eliminar / editar restricción (en coeficientes).
- **Al cambiar de método:**  
  Antes de cambiar de tab: leer el formulario **actual**, actualizar el modelo, persistir, luego cambiar de tab y **rellenar el formulario de destino** desde el modelo (o tener siempre ambos formularios sincronizados con el modelo y solo cambiar vista).

Para evitar guardar en cada tecla:
- **Debounce** (p. ej. 300–500 ms) en inputs de Z y en inputs de restricciones.
- **Inmediato** en: cambio de select, agregar/eliminar restricción, cambiar de método.

### 3.9 Cuándo restaurar

- **Al cargar la página:** leer de `localStorage` → modelo en memoria → rellenar el formulario del método activo (y opcionalmente el otro). Aplicar `cambiarMetodo(ultimoMetodo)` si se guardó.
- **Al cambiar de método:** asegurar que el formulario que se va a **mostrar** refleja el modelo (sync “modelo → formulario” del método destino). Si siempre se mantienen ambos forms sincronizados con el modelo, al cambiar de tab ya estaría actualizado.

### 3.10 Sincronización “ambos formularios comparten los mismos datos”

- **Fuente de verdad:** el modelo canónico en memoria.
- **Regla:** cada edición en Gráfico o Simplex actualiza el modelo; luego se actualiza el **otro** formulario desde el modelo (o ambos se derivan del modelo en cada cambio).
- Con eso se cumple “actualizar ambos formularios cuando se cambia un dato”.

---

## 4. Clave y formato en `localStorage`

- **Clave propuesta:** `programacion-lineal-datos` (o similar, distinta de `theme`).
- **Valor:** `JSON.stringify` del objeto canónico.
- Si `localStorage` falla o hay `JSON.parse` inválido, usar modelo por defecto y no romper la app.

---

## 5. Casos borde a considerar

- **Primera visita / sin datos guardados:** modelo por defecto (p. ej. el que refleja el HTML actual: Z = 3x + 2y, dos restricciones en Gráfico). No escribir en `localStorage` hasta que haya al menos un cambio.
- **Datos corruptos o `version` antigua:** ignorar y usar valores por defecto; opcionalmente limpiar la clave.
- **Simplex con 0 restricciones:** el backend puede fallar. Hoy `cambiarMetodo('simplex')` añade una si hay variables. Mantener una política similar al restaurar (p. ej. asegurar al menos una restricción por defecto cuando se carga modelo vacío para Simplex).
- **Usuario borra todos los coeficientes o todas las restricciones:** el modelo puede quedar “vacío”. Definir si se permite y qué mostrar (mensaje, valores por defecto, etc.).

---

## 6. Pasos sugeridos (orden de implementación)

Estos pasos son **anteriores** a escribir código; sirven como plan. Al implementar, se traducirán en cambios concretos en `main.js` (y si acaso en `index.html` mínimos).

1. **Definir el modelo canónico en JS**  
   - Objeto con `version`, `objetivo`, `z_coefs`, `restricciones`, `ultimoMetodo`.  
   - Funciones: `modeloDefault()`, `modeloDesdeLocalStorage()`, `guardarModeloEnLocalStorage(modelo)`.

2. **Implementar lectura “formulario → modelo”**  
   - `leerModeloDesdeGrafico()` → devuelve objeto canónico (solo si 2 vars).  
   - `leerModeloDesdeSimplex()` → devuelve objeto canónico.

3. **Implementar escritura “modelo → formulario”**  
   - `aplicarModeloAGrafico(modelo)` (solo si `z_coefs.length === 2`): actualizar objetivo, Z, lista de restricciones.  
   - `aplicarModeloASimplex(modelo)`: actualizar objetivo, Z, restricciones (recrear filas).

4. **Integrar en `cambiarMetodo`**  
   - Al salir del método actual: leer su formulario → actualizar modelo → `guardarModeloEnLocalStorage`.  
   - Antes de mostrar el otro método: `aplicarModeloA...` al formulario que se va a mostrar.  
   - Actualizar tab activo según `ultimoMetodo` y guardar `ultimoMetodo` en el modelo.

5. **Guardado automático al editar**  
   - Listeners (change/input) en objetivo, Z y restricciones (coef.).  
   - Debounce en inputs numéricos; sin debounce en selects y en agregar/eliminar restricción.  
   - En cada cambio: leer formulario activo → actualizar modelo → persistir → aplicar modelo al **otro** formulario para mantener sync.

6. **Restauración al cargar**  
   - En `DOMContentLoaded`: obtener modelo desde `localStorage` o default.  
   - `aplicarModeloAGrafico` y `aplicarModeloASimplex` (o solo al correspondiente a `ultimoMetodo` si se decide cargar bajo demanda).  
   - Llamar a `cambiarMetodo(ultimoMetodo)` para mostrar el tab guardado.

7. **Persistir método seleccionado**  
   - Al cambiar de tab, actualizar `ultimoMetodo` en el modelo y guardar.  
   - Incluido ya en los pasos 4 y 6.

8. **Manejo de modo “forma natural”**  
   - No persistir texto natural. Al restaurar, dejar natural vacío y modo coeficientes con datos.  
   - Opcional: al convertir natural → coeficientes, además de actualizar DOM, actualizar modelo y persistir (ya cubierto si “convertir” acaba modificando el formulario de coef. y tenemos listeners ahí).

9. **Casos borde y robustez**  
   - Validar estructura al leer de `localStorage`; fallback a modelo por defecto.  
   - Evitar errores si `z_coefs` o `restricciones` vienen vacíos o mal formados.

10. **Pruebas manuales (checklist)**  
    - Llenar Gráfico → cambiar a Simplex → comprobar que objetivo y restricciones coinciden.  
    - Cambiar a Gráfico de nuevo → comprobar que se mantienen.  
    - Editar en Simplex → volver a Gráfico → comprobar que los cambios se ven.  
    - Recargar → comprobar que todo se restaura (incluido tab activo).  
    - Cerrar y reabrir navegador → comprobar que `localStorage` sigue persistiendo.

---

## 7. Resumen de decisiones

| Tema | Decisión |
|------|----------|
| Almacenamiento | `localStorage` + modelo en memoria como fuente de verdad |
| Estructura | Objeto canónico con `version`, `objetivo`, `z_coefs`, `restricciones`, `ultimoMetodo` |
| Sync entre métodos | Modelo único; ambos formularios se actualizan desde el modelo |
| Gráfico con N > 2 vars | Solo sincronizar Gráfico cuando hay 2 variables; definir política para N > 2 |
| Forma natural | No persistir; solo coeficientes. Restaurar en modo coeficientes |
| Cuándo guardar | Debounce en inputs; inmediato en selects, agregar/eliminar restricción y al cambiar de método |
| Clave `localStorage` | `programacion-lineal-datos` (o similar) |

---

## 8. Próximos pasos

1. Revisar este análisis y ajustar decisiones si hace falta (p. ej. política para N > 2 variables, o persistir modo natural).  
2. Implementar según los pasos de la sección 6, en el orden indicado.  
3. Ejecutar el checklist de pruebas del Checkpoint 3 y complementar con los casos borde de la sección 5.

Cuando este plan esté validado, se puede pasar a los cambios concretos en el proyecto.
