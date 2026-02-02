# Documentacion - Calculadora de Programacion Lineal

Este directorio contiene la documentacion tecnica, analisis y guias del proyecto.

## Indice de Documentacion

### Documentacion Tecnica

- **[METODO_DOS_FASES_ANALISIS_IMPLEMENTACION.md](METODO_DOS_FASES_ANALISIS_IMPLEMENTACION.md)** - Analisis detallado del Metodo de Dos Fases
- **[RESTRICCIONES_NO_NEGATIVIDAD.md](RESTRICCIONES_NO_NEGATIVIDAD.md)** - Documentacion sobre restricciones de no-negatividad
- **[BUGS_SOLUCIONADOS_TEST.md](BUGS_SOLUCIONADOS_TEST.md)** - Bugs solucionados durante el desarrollo
- **[requirements.md](requirements.md)** - Requisitos y dependencias del sistema

### Despliegue y Configuracion

- **[DESPLIEGUE.md](DESPLIEGUE.md)** - Guia completa para desplegar la aplicacion
- **[CHECKLIST_RENDER.md](CHECKLIST_RENDER.md)** - Lista de verificacion para despliegue en Render

### Control de Calidad

- **[CHECKPOINTS.md](CHECKPOINTS.md)** - Puntos de control del desarrollo
- **[CHECKPOINT3_ANALISIS.md](CHECKPOINT3_ANALISIS.md)** - Analisis del checkpoint 3

---

## Tests y Ejercicios

Los archivos de prueba y ejercicios se encuentran en la carpeta **`tests/`**:

```
tests/
├── test_completo.py         # Test principal (24 ejercicios)
├── test_validacion.py       # Test de validacion (17 ejercicios)
├── test_ejercicios.py       # Test original
├── EJERCICIOS_COMPLETOS.md  # 24 ejercicios exhaustivos
├── EJERCICIOS_VALIDACION.md # 17 ejercicios de validacion
└── EJERCICIOS_PRUEBA.md     # Ejercicios originales
```

Ver **[../tests/README.md](../tests/README.md)** para instrucciones de ejecucion.

---

## Estructura Recomendada de Lectura

### Para Usuarios Nuevos:
1. Comienza con el `README.md` principal (en la raiz del proyecto)
2. Revisa los ejercicios en `tests/EJERCICIOS_COMPLETOS.md`
3. Ejecuta `tests/test_completo.py` para validar

### Para Desarrolladores:
1. `METODO_DOS_FASES_ANALISIS_IMPLEMENTACION.md` - Entender la logica del solver
2. `BUGS_SOLUCIONADOS_TEST.md` - Problemas resueltos
3. `CHECKPOINTS.md` - Historia del desarrollo

### Para Mantenimiento:
1. `tests/test_completo.py` - Ejecutar pruebas de regresion
2. `CHECKLIST_RENDER.md` - Validar despliegue
3. `requirements.md` - Verificar dependencias

---

**Ultima actualizacion:** Febrero 2026  
**Repositorio:** [GitHub - williamfloress](https://github.com/williamfloress)
