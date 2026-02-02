# Script de Pruebas Automáticas

Este script prueba automáticamente todos los ejercicios del archivo `docs/EJERCICIOS_PRUEBA.md` contra la calculadora de programación lineal.

## Requisitos Previos

1. **Python 3.7+** instalado
2. **Servidor Flask corriendo** (la calculadora debe estar activa)
3. Dependencias instaladas

## Instalación

### 1. Instalar dependencias:

```bash
pip install -r requirements_test.txt
```

O manualmente:
```bash
pip install requests colorama
```

### 2. Iniciar el servidor de la calculadora:

En una terminal separada:
```bash
python app.py
```

Esto debería iniciar el servidor en `http://localhost:5000`

## Uso

### Ejecutar todas las pruebas:

```bash
python test_ejercicios.py
```

### Salida esperada:

```
╔════════════════════════════════════════════════════════════════╗
║  TEST AUTOMÁTICO - CALCULADORA DE PROGRAMACIÓN LINEAL         ║
╚════════════════════════════════════════════════════════════════╝

✓ Servidor detectado en http://localhost:5000

Parseando ejercicios de docs/EJERCICIOS_PRUEBA.md...
✓ 24 ejercicios encontrados

Ejecutando pruebas...

[1/8] Probando Ejercicio 1... ✓ PASÓ
[2/8] Probando Ejercicio 2... ✓ PASÓ
[3/8] Probando Ejercicio 3... ✓ PASÓ
...

================================================================================
REPORTE DE PRUEBAS - CALCULADORA DE PROGRAMACIÓN LINEAL
================================================================================

RESUMEN GENERAL:
  Total de ejercicios probados: 8
  ✓ Exitosos: 7
  ✗ Fallidos: 1
  Tasa de éxito: 87.5%

POR MÉTODO:
  Gráfico: 7/8 (87.5%)

--------------------------------------------------------------------------------

DETALLES DE EJERCICIOS:

✓ Ejercicio 1 (Gráfico)
✓ Ejercicio 2 (Gráfico)
✓ Ejercicio 3 (Gráfico)
✗ Ejercicio 4 (Gráfico)
    ERROR: Tipo de solución incorrecto. Esperado: 'Múltiple', Obtenido: 'Única'
...
```

## Qué prueba el script

### Método Gráfico (Ejercicios 1-8):
- Función objetivo (maximización/minimización)
- Restricciones (≤, ≥, =)
- Tipo de solución (Única, Degenerada, Múltiple, No Factible)
- Valor óptimo de Z
- Punto óptimo (X, Y)

### Método Simplex (Ejercicios 9-13B):
- Múltiples variables (X₁, X₂, X₃, ...)
- Tabla final
- Variables básicas
- Detección de problemas no acotados

### Método Dos Fases (Ejercicios 14-19):
- Fase 1 (minimización de W)
- Fase 2 (optimización de Z)
- Detección de no factibilidad (W > 0)
- Variables artificiales

## Configuración

### Cambiar URL del servidor:

Si tu servidor corre en otro puerto, edita `test_ejercicios.py`:

```python
BASE_URL = "http://localhost:8080"  # Cambia el puerto
```

### Probar solo ciertos ejercicios:

Edita la función `main()` en `test_ejercicios.py`:

```python
# Probar solo ejercicios 1-5
for i, ej in enumerate(ejercicios[:5], 1):
    ...

# O probar ejercicios específicos
ejercicios_a_probar = [1, 3, 5, 7]
for ej in ejercicios:
    if int(ej['numero']) in ejercicios_a_probar:
        ...
```

## Solución de Problemas

### Error: "No se puede conectar al servidor"

```
✗ Error: No se puede conectar al servidor en http://localhost:5000
```

**Solución:** Asegúrate de que el servidor Flask esté corriendo:
```bash
python app.py
```

### Error: "ModuleNotFoundError: No module named 'colorama'"

**Solución:** Instala las dependencias:
```bash
pip install -r requirements_test.txt
```

### Error al parsear ejercicios

**Solución:** Verifica que el archivo `docs/EJERCICIOS_PRUEBA.md` exista en la carpeta docs.

## Estructura de Archivos

```
programacion-lineal/
│
├── app.py                      # Servidor Flask
├── solver.py                   # Lógica de solvers
├── metodo_dos_fases.py         # Método de dos fases
│
├── docs/                       # Documentación
│   ├── EJERCICIOS_PRUEBA.md    # Ejercicios de prueba
│   └── TEST_README.md          # Esta documentación
│
├── test_ejercicios.py          # Script de pruebas ← ESTE
└── requirements_test.txt       # Dependencias
```

## Personalización

### Agregar nuevos ejercicios:

1. Edita `docs/EJERCICIOS_PRUEBA.md`
2. Sigue el formato:

```markdown
### Ejercicio XX: Nombre
**Función Objetivo:**
- Maximizar Z = 3X + 2Y

**Restricciones:**
\```
X + Y ≤ 10
2X + Y ≤ 15
\```

**Solución Esperada:**
- X = 5
- Y = 5
- Z = 25
- **Tipo:** Solución Única
```

3. Ejecuta el script nuevamente

### Modificar tolerancias:

En `test_ejercicios.py`, busca:

```python
if abs(z_obtenido - esperado['z_optimo']) > 0.1:  # ← Cambiar tolerancia
```

## Notas

- El script actualmente solo prueba completamente los **ejercicios del método gráfico** (1-8)
- Los ejercicios de Simplex y Dos Fases requieren parsing adicional de subíndices Unicode
- Las pruebas usan una tolerancia de 0.1 para comparaciones numéricas
- Los colores en terminal pueden no funcionar correctamente en algunos entornos (Windows CMD antiguo)

## Próximas Mejoras

- [ ] Soporte completo para ejercicios de Simplex
- [ ] Soporte completo para ejercicios de Dos Fases
- [ ] Exportar reporte a HTML/PDF
- [ ] Modo verbose con detalles de requests
- [ ] Tiempo de ejecución por ejercicio
- [ ] Comparación de gráficas generadas

## Soporte

Si encuentras bugs o tienes sugerencias, revisa el código en `test_ejercicios.py` y ajusta según tus necesidades.

---

**Última actualización:** Enero 2026
**Autor:** William Flores
