#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test unificado: validación de los 3 métodos de Programación Lineal.

Ejecuta todos los ejercicios de:
- docs/EJERCICIOS_COMPLETOS.md (test completo: 24 ejercicios)
- docs/EJERCICIOS_VALIDACION.md (validación: 17 ejercicios)
- docs/06_EJERCICIOS_2FASES.md (dos fases con resultado esperado: 3 ejercicios)

Usa los solvers en proceso (no requiere servidor).

Uso:
    python test.py              # Todos los métodos
    python test.py grafico      # Solo método gráfico
    python test.py simplex      # Solo método simplex
    python test.py dosfases     # Solo método dos fases
    python test.py rapido       # Una prueba por método
"""

import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Encoding UTF-8 en Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = RED = YELLOW = ""
    class Style:
        RESET_ALL = ""

sys.path.insert(0, ".")
from metodo_grafico import MetodoGrafico
from metodo_simplex import MetodoSimplex
from metodo_dos_fases import MetodoDosFases

TOL_Z = 0.01
TOL_X = 0.1


@dataclass
class Ejercicio:
    """Un ejercicio de prueba para cualquier método."""
    id: str
    nombre: str
    metodo: str  # 'grafico', 'simplex', 'dos_fases'
    objetivo: str
    c: List[float]
    A: List[List[float]]
    b: List[float]
    operadores: List[str]
    tipos_validos: List[str]  # Tipos de solución aceptables
    z_esperado: Optional[float] = None
    x_esperado: Optional[List[float]] = None


# =============================================================================
# EJERCICIOS MÉTODO GRÁFICO (G1-G8 + V1-V5 validación)
# =============================================================================

EJERCICIOS_GRAFICO = [
    # Test completo G1-G8
    Ejercicio("G1", "Maximización - Solución Única Clásica", "grafico", "max",
              [3, 2], [[2, 1], [1, 2], [1, 0]], [18, 16, 7], ['<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("G2", "Minimización - Solución Única", "grafico", "min",
              [4, 5], [[1, 1], [2, 1], [1, 0], [0, 1]], [8, 10, 12, 12], ['>=', '>=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("G3", "Soluciones Múltiples", "grafico", "max",
              [2, 4], [[1, 2], [1, 0], [0, 1]], [10, 6, 4], ['<=', '<=', '<='],
              ["multiple", "infinita"], None, None),
    Ejercicio("G4", "Problema No Factible", "grafico", "max",
              [5, 3], [[1, 1], [1, 1], [1, 0], [0, 1]], [5, 10, 8, 8], ['<=', '>=', '<=', '<='],
              ["no factible", "infeasible"], None, None),
    Ejercicio("G5", "Solución en el Origen", "grafico", "min",
              [7, 9], [[1, 1], [1, 0], [0, 1]], [0, 10, 10], ['>=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("G6", "Solución en un Solo Eje", "grafico", "max",
              [5, 1], [[1, 1], [2, 1], [0, 1]], [10, 16, 6], ['<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("G7", "Restricciones con >=", "grafico", "max",
              [3, 4], [[1, 1], [1, 1], [1, 0], [0, 1]], [4, 10, 6, 6], ['>=', '<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("G8", "Restricciones Mixtas", "grafico", "min",
              [2, 3], [[1, 1], [2, 1], [1, 0], [0, 1], [1, 0], [0, 1]], [5, 12, 1, 1, 8, 8],
              ['>=', '<=', '>=', '>=', '<=', '<='], ["unica"], None, None),
    # Validación V1-V5
    Ejercicio("V1", "Gráfico - Solución Única Básica", "grafico", "max",
              [4, 3], [[2, 1], [1, 2], [1, 0]], [20, 18, 8], ['<=', '<=', '<='],
              ["unica"], 45.33, [7.33, 5.33]),
    Ejercicio("V2", "Gráfico - Soluciones Múltiples", "grafico", "max",
              [2, 2], [[1, 1], [1, 0], [0, 1]], [10, 6, 6], ['<=', '<=', '<='],
              ["multiple", "infinita"], 20, None),
    Ejercicio("V3", "Gráfico - Solución en Origen", "grafico", "min",
              [3, 5], [[1, 1], [1, 0], [0, 1]], [0, 10, 10], ['>=', '<=', '<='],
              ["unica"], 0, [0, 0]),
    Ejercicio("V4", "Gráfico - No Factible", "grafico", "max",
              [1, 1], [[1, 1], [1, 1], [1, 0], [0, 1]], [4, 8, 10, 10], ['<=', '>=', '<=', '<='],
              ["no factible", "infeasible"], None, None),
    Ejercicio("V5", "Gráfico - Minimización Simple", "grafico", "min",
              [5, 8], [[1, 1], [2, 1], [1, 0], [0, 1]], [6, 16, 7, 8], ['>=', '<=', '<=', '<='],
              ["unica"], 30, [6, 0]),
]

# =============================================================================
# EJERCICIOS MÉTODO SIMPLEX (S1-S8 + V6-V10 validación)
# =============================================================================

EJERCICIOS_SIMPLEX = [
    Ejercicio("S1", "Simplex Básico 2 Variables", "simplex", "max",
              [4, 3], [[2, 1], [1, 2], [1, 1]], [10, 8, 6], ['<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("S2", "Simplex 3 Variables", "simplex", "max",
              [5, 4, 3], [[2, 1, 1], [1, 2, 1], [1, 1, 2]], [20, 18, 16], ['<=', '<=', '<='],
              ["unica", "multiple"], None, None),
    Ejercicio("S3", "Simplex 4 Variables", "simplex", "max",
              [6, 5, 4, 3], [[1, 1, 1, 1], [2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1]], [50, 60, 55, 45], ['<=', '<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("S4", "Simplex - Degenerada", "simplex", "max",
              [3, 2], [[1, 1], [2, 1], [1, 0], [0, 1]], [4, 6, 3, 3], ['<=', '<=', '<=', '<='],
              ["unica", "degenerada"], None, None),
    Ejercicio("S5", "Simplex - Múltiples Soluciones", "simplex", "max",
              [2, 2], [[1, 1], [1, 0], [0, 1]], [8, 5, 5], ['<=', '<=', '<='],
              ["multiple", "infinita"], None, None),
    Ejercicio("S6", "Simplex - No Acotado", "simplex", "max",
              [2, 3], [[-1, 1], [1, -2]], [5, 3], ['<=', '<='],
              ["no acotado", "unbounded"], None, None),
    Ejercicio("S7", "Simplex - Minimización", "simplex", "min",
              [8, 6, 4], [[1, 1, 1], [2, 1, 1], [1, 1, 2]], [30, 40, 35], ['<=', '<=', '<='],
              ["unica"], None, None),
    Ejercicio("S8", "Simplex - Coef. Negativos", "simplex", "max",
              [3, 5], [[1, -1], [-1, 2], [1, 1]], [4, 6, 8], ['<=', '<=', '<='],
              ["unica"], None, None),
    # Validación
    Ejercicio("V6", "Simplex Clásico 3 Variables", "simplex", "max",
              [5, 4, 3], [[2, 3, 1], [4, 2, 3], [1, 1, 2]], [60, 80, 40], ['<=', '<=', '<='],
              ["unica"], 115, [15, 10, 0]),
    Ejercicio("V7", "Simplex con Degeneración", "simplex", "max",
              [2, 3], [[1, 1], [1, 0], [0, 1], [1, 2]], [4, 2, 3, 6], ['<=', '<=', '<=', '<='],
              ["unica"], 10, [2, 2]),
    Ejercicio("V8", "Simplex 4 Variables", "simplex", "max",
              [3, 2, 4, 1], [[1, 1, 1, 1], [2, 1, 3, 1], [1, 2, 1, 2]], [100, 150, 120], ['<=', '<=', '<='],
              ["unica"], 240, [60, 30, 0, 0]),
    Ejercicio("V9", "Simplex - No Acotado", "simplex", "max",
              [3, 2], [[-1, 1], [1, -2]], [4, 2], ['<=', '<='],
              ["no acotado", "unbounded"], None, None),
    Ejercicio("V10", "Simplex Minimización", "simplex", "min",
              [6, 8, 5], [[2, 1, 1], [1, 2, 1], [1, 1, 2]], [8, 10, 12], ['>=', '>=', '>='],
              ["multiple", "unica"], None, None),
]

# =============================================================================
# EJERCICIOS MÉTODO DOS FASES (D1-D8 + V11-V17 + 2F1-2F3)
# =============================================================================

EJERCICIOS_DOS_FASES = [
    Ejercicio("D1", "Dos Fases - Solo >=", "dos_fases", "max",
              [4, 5], [[1, 1], [2, 1], [1, 2], [1, 0], [0, 1]], [6, 8, 7, 10, 10], ['>=', '>=', '>=', '<=', '<='],
              ["unica", "multiple"], None, None),
    Ejercicio("D2", "Dos Fases - Solo =", "dos_fases", "max",
              [3, 2], [[1, 1], [2, 1]], [6, 10], ['=', '='], ["unica"], None, None),
    Ejercicio("D3", "Dos Fases - Mezcla <=, >=, =", "dos_fases", "max",
              [5, 4], [[1, 1], [2, 1], [1, 0], [0, 1]], [8, 14, 2, 1], ['=', '<=', '>=', '>='],
              ["unica"], None, None),
    Ejercicio("D4", "Dos Fases - No Factible", "dos_fases", "max",
              [3, 4], [[1, 1], [1, 1], [1, 0], [0, 1]], [15, 8, 10, 10], ['>=', '<=', '<=', '<='],
              ["no factible", "infeasible"], None, None),
    Ejercicio("D5", "Dos Fases - Minimización", "dos_fases", "min",
              [6, 4], [[1, 1], [2, 1], [1, 3]], [8, 10, 12], ['>=', '>=', '>='],
              ["unica", "multiple"], None, None),
    Ejercicio("D6", "Dos Fases - 3 Variables", "dos_fases", "max",
              [3, 2, 5], [[1, 1, 1], [2, 1, 1], [1, 2, 1], [0, 0, 1]], [10, 8, 15, 2], ['=', '>=', '<=', '>='],
              ["unica", "multiple"], None, None),
    Ejercicio("D7", "Dos Fases - Múltiples Soluciones", "dos_fases", "max",
              [2, 2], [[1, 1], [1, 1], [1, 0], [0, 1]], [4, 8, 5, 5], ['>=', '<=', '<=', '<='],
              ["multiple", "infinita"], None, None),
    Ejercicio("D8", "Dos Fases - 4 Variables", "dos_fases", "max",
              [2, 3, 4, 1], [[1, 1, 1, 1], [2, 1, 1, 1], [1, 1, 2, 1], [1, 2, 1, 2]], [20, 15, 25, 18], ['=', '>=', '<=', '>='],
              ["unica", "multiple"], None, None),
    # Validación
    Ejercicio("V11", "Dos Fases Básico", "dos_fases", "max",
              [3, 5], [[1, 1], [2, 1], [1, 0]], [4, 6, 1], ['=', '<=', '>='],
              ["unica"], None, None),
    Ejercicio("V12", "Dos Fases Restricciones Mixtas", "dos_fases", "max",
              [4, 3], [[1, 1], [2, 1], [1, 0], [0, 1]], [5, 12, 4, 6], ['>=', '<=', '<=', '<='],
              ["multiple", "unica"], None, None),
    Ejercicio("V13", "Dos Fases No Factible", "dos_fases", "max",
              [2, 3], [[1, 1], [1, 1]], [10, 5], ['>=', '<='], ["no factible", "infeasible"], None, None),
    Ejercicio("V14", "Dos Fases Tres Variables", "dos_fases", "max",
              [2, 3, 4], [[1, 1, 1], [2, 1, 1], [1, 2, 1]], [10, 8, 15], ['=', '>=', '<='],
              ["unica"], None, None),
    Ejercicio("V15", "Dos Fases Minimización", "dos_fases", "min",
              [4, 2], [[1, 1], [2, 1], [1, 3]], [6, 8, 9], ['>=', '>=', '>='],
              ["multiple", "unica"], None, None),
    Ejercicio("V16", "Dos Fases Solo Igualdades", "dos_fases", "max",
              [5, 4], [[1, 1], [2, 1]], [8, 12], ['=', '='], ["unica"], 36, [4, 4]),
    Ejercicio("V17", "Dos Fases Múltiples Soluciones", "dos_fases", "max",
              [2, 4], [[1, 2], [1, 1], [1, 0], [0, 1]], [8, 2, 4, 3], ['<=', '>=', '<=', '<='],
              ["multiple"], None, None),
    # 06_EJERCICIOS_2FASES.md
    Ejercicio("2F1", "2Fases - Max 3x1+5x2, x1+x2=10, 2x1+3x2>=12", "dos_fases", "max",
              [3, 5], [[1, 1], [2, 3]], [10, 12], ['=', '>='], ["unica"], 50, [0, 10]),
    Ejercicio("2F2", "2Fases - Min 2x1+3x2, restricciones mixtas", "dos_fases", "min",
              [2, 3], [[0.5, 0.25], [1, 3], [1, 1]], [4, 20, 10], ['<=', '>=', '='], ["unica"], 25, [5, 5]),
    Ejercicio("2F3", "2Fases - Max 4x1+x2, 3x1+x2=3, ...", "dos_fases", "max",
              [4, 1], [[3, 1], [4, 3], [1, 2]], [3, 6, 4], ['=', '>=', '<='], ["unica"], 3.6, [0.6, 1.2]),
]


def _normalizar(s: str) -> str:
    s = s.lower()
    for a, b in [('ú', 'u'), ('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o')]:
        s = s.replace(a, b)
    return s


def _verificar_tipo(tipo_obtenido: str, tipos_validos: List[str]) -> bool:
    if not tipo_obtenido:
        return False
    t = _normalizar(str(tipo_obtenido))
    for v in tipos_validos:
        if _normalizar(v) in t:
            return True
    return False


def _verificar_z(z_obt: Optional[float], z_esp: float) -> bool:
    if z_obt is None:
        return False
    return abs(z_obt - z_esp) <= TOL_Z


def _verificar_x(x_obt: Optional[List], x_esp: List[float], n: int) -> bool:
    if x_obt is None or len(x_esp) != n:
        return False
    x = (x_obt[:n] if len(x_obt) >= n else x_obt + [0] * (n - len(x_obt)))
    return all(abs(x[i] - x_esp[i]) <= TOL_X for i in range(len(x_esp)))


def _ejecutar_grafico(ej: Ejercicio) -> Dict[str, Any]:
    p = MetodoGrafico(ej.c, ej.A, ej.b, ej.operadores, objetivo=ej.objetivo)
    return p.resolver()


def _ejecutar_simplex(ej: Ejercicio) -> Dict[str, Any]:
    p = MetodoSimplex(ej.c, ej.A, ej.b, ej.operadores, objetivo=ej.objetivo)
    return p.resolver()


def _ejecutar_dos_fases(ej: Ejercicio) -> Dict[str, Any]:
    p = MetodoDosFases(ej.c, ej.A, ej.b, ej.operadores, objetivo=ej.objetivo)
    return p.resolver()


def ejecutar_ejercicio(ej: Ejercicio) -> Dict[str, Any]:
    """Ejecuta un ejercicio con el solver correspondiente y verifica resultado."""
    resultado = {
        "id": ej.id,
        "nombre": ej.nombre,
        "metodo": ej.metodo,
        "exito": False,
        "tipo_obtenido": "",
        "z_obtenido": None,
        "error": None,
    }
    try:
        if ej.metodo == "grafico":
            resp = _ejecutar_grafico(ej)
        elif ej.metodo == "simplex":
            resp = _ejecutar_simplex(ej)
        else:
            resp = _ejecutar_dos_fases(ej)

        tipo = resp.get("tipo_solucion", resp.get("status", ""))
        resultado["tipo_obtenido"] = tipo
        resultado["z_obtenido"] = resp.get("z_optimo")

        if not _verificar_tipo(tipo, ej.tipos_validos):
            resultado["error"] = f"Tipo incorrecto: esperado alguno de {ej.tipos_validos}"
            return resultado

        if ej.z_esperado is not None:
            if not _verificar_z(resultado["z_obtenido"], ej.z_esperado):
                resultado["error"] = f"Z incorrecto: esperado {ej.z_esperado}, obtenido {resultado['z_obtenido']}"
                return resultado

        if ej.x_esperado is not None:
            x_obt = resp.get("punto_optimo") if ej.metodo == "grafico" else resp.get("solucion")
            if not _verificar_x(x_obt, ej.x_esperado, len(ej.c)):
                resultado["error"] = f"X incorrecto: esperado {ej.x_esperado}, obtenido {x_obt}"
                return resultado

        resultado["exito"] = True
    except Exception as e:
        resultado["error"] = str(e)
    return resultado


def imprimir_resultado(res: Dict[str, Any], detallado: bool = True):
    icono = f"{Fore.GREEN}[OK]{Style.RESET_ALL}" if res["exito"] else f"{Fore.RED}[X]{Style.RESET_ALL}"
    print(f"  {icono} {res['id']}: {res['nombre']}")
    if detallado:
        if res["tipo_obtenido"]:
            print(f"       Tipo: {res['tipo_obtenido']}")
        if res["z_obtenido"] is not None:
            print(f"       Z = {res['z_obtenido']:.4f}")
        if res["error"]:
            print(f"       {Fore.RED}Error: {res['error']}{Style.RESET_ALL}")


def ejecutar_seccion(ejercicios: List[Ejercicio], nombre_seccion: str, detallado: bool = True) -> List[Dict]:
    print(f"\n{'=' * 28} {nombre_seccion} {'=' * 28}")
    resultados = []
    for ej in ejercicios:
        res = ejecutar_ejercicio(ej)
        resultados.append(res)
        imprimir_resultado(res, detallado)
    return resultados


def main(filtro: Optional[str] = None) -> bool:
    print("\n" + "=" * 70)
    print("  TEST UNIFICADO - PROGRAMACIÓN LINEAL")
    print("  Gráfico | Simplex | Dos Fases (sin servidor)")
    print("=" * 70)

    tiempo_inicio = time.time()
    todos_resultados = []

    if filtro == "grafico":
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_GRAFICO, "MÉTODO GRÁFICO"))
    elif filtro == "simplex":
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_SIMPLEX, "MÉTODO SIMPLEX"))
    elif filtro == "dosfases":
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_DOS_FASES, "MÉTODO DOS FASES"))
    elif filtro == "rapido":
        print("\n  Modo rápido: 1 ejercicio por método")
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_GRAFICO[0]))
        imprimir_resultado(todos_resultados[-1])
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_SIMPLEX[0]))
        imprimir_resultado(todos_resultados[-1])
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_DOS_FASES[0]))
        imprimir_resultado(todos_resultados[-1])
    else:
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_GRAFICO, "MÉTODO GRÁFICO"))
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_SIMPLEX, "MÉTODO SIMPLEX"))
        todos_resultados.extend(ejecutar_seccion(EJERCICIOS_DOS_FASES, "MÉTODO DOS FASES"))

    tiempo_total = time.time() - tiempo_inicio

    total = len(todos_resultados)
    exitosos = sum(1 for r in todos_resultados if r["exito"])
    fallidos = total - exitosos
    porcentaje = (exitosos / total * 100) if total > 0 else 0

    print("\n" + "=" * 70)
    print("  RESUMEN")
    print("=" * 70)
    for metodo, nombre in [("grafico", "Gráfico"), ("simplex", "Simplex"), ("dos_fases", "Dos Fases")]:
        res_metodo = [r for r in todos_resultados if r["metodo"] == metodo]
        if res_metodo:
            ok = sum(1 for r in res_metodo if r["exito"])
            print(f"  {nombre:12} {ok}/{len(res_metodo)}")
    print(f"\n  {'Total':12} {exitosos}/{total}")
    print(f"  {'Tiempo':12} {tiempo_total:.2f}s")
    if porcentaje == 100:
        color = Fore.GREEN
    elif porcentaje >= 75:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    print(f"\n  {color}Tasa de éxito: {porcentaje:.1f}%{Style.RESET_ALL}")
    fallidos_lista = [r for r in todos_resultados if not r["exito"]]
    if fallidos_lista:
        print(f"\n  {Fore.RED}Fallidos:{Style.RESET_ALL}")
        for r in fallidos_lista:
            print(f"    - {r['id']}: {r['error'] or 'Error desconocido'}")
    print("\n" + "=" * 70 + "\n")
    return exitosos == total


if __name__ == "__main__":
    filtro = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["grafico", "g"]:
            filtro = "grafico"
        elif arg in ["simplex", "s"]:
            filtro = "simplex"
        elif arg in ["dosfases", "dos_fases", "2f", "df", "d"]:
            filtro = "dosfases"
        elif arg in ["rapido", "r", "quick", "q"]:
            filtro = "rapido"
        elif arg in ["help", "-h", "--help"]:
            print(__doc__)
            sys.exit(0)
    exito = main(filtro)
    sys.exit(0 if exito else 1)
