# Tests - Calculadora de Programacion Lineal

Esta carpeta contiene los scripts de prueba y ejercicios para validar
el correcto funcionamiento de la calculadora.

---

## Estructura

```
tests/
├── README.md                    # Este archivo
├── test_completo.py             # Test principal (24 ejercicios)
├── test_validacion.py           # Test de validacion (17 ejercicios)
├── test_ejercicios.py           # Test original (parsea .md)
├── EJERCICIOS_COMPLETOS.md      # 24 ejercicios exhaustivos
├── EJERCICIOS_VALIDACION.md     # 17 ejercicios de validacion
└── EJERCICIOS_PRUEBA.md         # Ejercicios originales
```

---

## Scripts de Prueba

### test_completo.py (Recomendado)

El test mas completo con **24 ejercicios** que cubren todos los escenarios.

```bash
# Desde la raiz del proyecto
cd tests
python test_completo.py              # Todas las pruebas (24)
python test_completo.py grafico      # Solo grafico (8)
python test_completo.py simplex      # Solo simplex (8)
python test_completo.py dosfases     # Solo dos fases (8)
python test_completo.py rapido       # Prueba rapida (3)
```

### test_validacion.py

Test con **17 ejercicios** de validacion.

```bash
python test_validacion.py            # Todas las pruebas
python test_validacion.py grafico    # Solo grafico
python test_validacion.py simplex    # Solo simplex
python test_validacion.py dosfases   # Solo dos fases
```

### test_ejercicios.py

Test original que parsea el archivo EJERCICIOS_PRUEBA.md.

```bash
python test_ejercicios.py
```

---

## Escenarios Cubiertos

### Metodo Grafico (2 variables)
- Maximizacion y Minimizacion
- Solucion Unica
- Soluciones Multiples (Infinitas)
- Problema No Factible
- Solucion en origen
- Solucion en ejes
- Restricciones >=

### Metodo Simplex (n variables)
- 2, 3 y 4 variables
- Solucion Degenerada
- Soluciones Multiples
- Problema No Acotado
- Minimizacion
- Coeficientes negativos

### Metodo Dos Fases
- Solo restricciones >=
- Solo restricciones =
- Mezcla de <=, >=, =
- Problema No Factible (Fase 1 falla)
- Minimizacion
- 3 y 4 variables

---

## Requisitos

```bash
pip install requests colorama numpy
```

---

## Ejecucion

1. Asegurate de que el servidor Flask este corriendo:
   ```bash
   # Desde la raiz del proyecto
   python app.py
   ```

2. En otra terminal, ejecuta los tests:
   ```bash
   cd tests
   python test_completo.py
   ```

---

## Resultados Esperados

```
======================================================================
  RESUMEN
======================================================================
  Grafico      8/8
  Simplex      8/8
  Dos Fases    8/8

  Total        24/24
  Tiempo       ~50s

  Tasa de Exito: 100.0%
======================================================================
```
