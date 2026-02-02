# Historial de Desarrollo

Registro del progreso, mejoras implementadas y trabajo pendiente.

---

## Estado Actual

### Completado [X]

| Checkpoint | Descripción | Estado |
|------------|-------------|--------|
| Core | Método Gráfico, Simplex, Dos Fases | [X] |
| CP1 | Dark Mode | [X] |
| CP2 | Responsividad Mobile-First | [X] |
| Tests | 24/24 ejercicios (100%) | [X] |
| Deploy | Configuración Render/Docker | [X] |

### Pendiente

| Checkpoint | Descripción | Estado |
|------------|-------------|--------|
| CP3 | Persistencia de datos entre métodos | [ ] |
| CP4 | Reorganizar flujo (input primero, método después) | [ ] |
| CP5 | Log temporal de operaciones | [ ] |
| CP6 | Mejoras de validaciones | [ ] |

---

## Checkpoint 1: Dark Mode [X]

**Implementado:**
- Toggle de tema claro/oscuro
- Persistencia en `localStorage`
- Detección de preferencia del sistema (`prefers-color-scheme`)
- Transiciones suaves
- Contraste WCAG AA

---

## Checkpoint 2: Responsividad [X]

**Implementado:**
- Breakpoints: 360px, 480px, 768px, 896px
- Touch targets ≥ 44×44px
- `inputmode="decimal"` en inputs numéricos
- Plotly responsive con resize automático
- Tablas con scroll horizontal en móvil

---

## Checkpoint 3: Persistencia (Pendiente)

**Objetivo:** Compartir datos entre métodos Gráfico y Simplex.

**Diseño propuesto:**
```json
{
  "version": 1,
  "objetivo": "max",
  "z_coefs": [3, 2],
  "restricciones": [
    { "coefs": [2, 1], "op": "<=", "val": 100 }
  ],
  "ultimoMetodo": "grafico"
}
```

**Pasos:**
1. Modelo canónico en memoria
2. Lectura formulario → modelo
3. Escritura modelo → formulario
4. Sincronización al cambiar método
5. Guardado en `localStorage`

---

## Bugs Solucionados

### Método Dos Fases
| Bug | Problema | Solución |
|-----|----------|----------|
| 1.1 | Orden de columnas incorrecto | Generar nombres en orden de construcción |
| 1.2 | Variable entrante mal identificada | Usar `nombres_columnas[col]` |
| 1.3 | Valor W duplicado | Eliminar asignación manual |
| 1.4 | Referencias sin `.copy()` | Usar `.copy()` al registrar tablas |

### Método Gráfico
| Bug | Problema | Solución |
|-----|----------|----------|
| 4.1 | Precisión en vértices duplicados | Usar `np.allclose()` con tolerancia |
| 4.2 | Parser case-sensitive | Convertir a minúsculas |

### Script de Pruebas
| Bug | Problema | Solución |
|-----|----------|----------|
| 2.1 | Filtrado incorrecto de restricciones | Regex específico para no-negatividad |
| 2.7 | UTF-8 en Windows | `sys.stdout.reconfigure(encoding='utf-8')` |

---

## Progreso de Correcciones

```
Inicio:              0/19 tests (0%)
Bugs 1.1-1.4:       14/19 tests (73.7%)
Bugs 2.1-2.4:       16/19 tests (84.2%)
Bugs 3.1-3.5:       19/19 tests (100%) [X]
Actualización:      24/24 tests (100%) [X]
```

---

## Lecciones Aprendidas

1. **Testing revela bugs ocultos** - Automatizar pruebas temprano
2. **Referencias en Python** - Siempre usar `.copy()` con listas mutables
3. **Tolerancia numérica** - Floats nunca son exactos, usar `np.isclose()`
4. **Validar datos de prueba** - Los "valores esperados" pueden estar mal
5. **Encoding en Windows** - UTF-8 no es el default

---

## Arquitectura de Archivos

```
programacion-lineal/
|-- app.py                    # Flask backend
|-- solver.py                 # Orquestador
|-- metodo_grafico.py         # Gráfico
|-- metodo_simplex.py         # Simplex
|-- metodo_dos_fases.py       # Dos Fases
|-- static/css/style.css      # Estilos + Dark Mode
|-- static/js/main.js         # Lógica frontend
|-- templates/index.html      # UI
|-- tests/                    # Pruebas automatizadas
|-- docs/                     # Documentación
```

---

**Última actualización:** Febrero 2026
