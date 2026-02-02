#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Completo - Calculadora de Programacion Lineal

Prueba exhaustiva de los 24 ejercicios del archivo docs/EJERCICIOS_COMPLETOS.md
Cubre todos los escenarios posibles para los 3 metodos.

Uso:
    python test_completo.py              # Todas las pruebas
    python test_completo.py grafico      # Solo metodo grafico (G1-G8)
    python test_completo.py simplex      # Solo metodo simplex (S1-S8)
    python test_completo.py dosfases     # Solo metodo dos fases (D1-D8)
    python test_completo.py rapido       # Una prueba de cada metodo
"""

import sys
import requests
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from colorama import init, Fore, Style

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

init(autoreset=True)

BASE_URL = "http://localhost:5000"


@dataclass
class Ejercicio:
    """Representa un ejercicio de prueba"""
    id: str
    nombre: str
    metodo: str  # 'grafico', 'simplex', 'dos_fases'
    objetivo: str  # 'max' o 'min'
    c: List[float]
    A: List[List[float]]
    b: List[float]
    operadores: List[str]
    tipos_validos: List[str]  # Lista de tipos aceptables
    descripcion: str = ""


# ============================================================================
# EJERCICIOS METODO GRAFICO (G1-G8)
# ============================================================================

EJERCICIOS_GRAFICO = [
    Ejercicio(
        id="G1",
        nombre="Maximizacion - Solucion Unica Clasica",
        metodo="grafico",
        objetivo="max",
        c=[3, 2],
        A=[[2, 1], [1, 2], [1, 0]],
        b=[18, 16, 7],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Produccion con recursos limitados"
    ),
    Ejercicio(
        id="G2",
        nombre="Minimizacion - Solucion Unica",
        metodo="grafico",
        objetivo="min",
        c=[4, 5],
        A=[[1, 1], [2, 1], [1, 0], [0, 1]],
        b=[8, 10, 12, 12],
        operadores=['>=', '>=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Minimizar costos de produccion"
    ),
    Ejercicio(
        id="G3",
        nombre="Soluciones Multiples (Infinitas)",
        metodo="grafico",
        objetivo="max",
        c=[2, 4],
        A=[[1, 2], [1, 0], [0, 1]],
        b=[10, 6, 4],
        operadores=['<=', '<=', '<='],
        tipos_validos=["multiple", "infinita"],
        descripcion="FO paralela a restriccion activa"
    ),
    Ejercicio(
        id="G4",
        nombre="Problema No Factible",
        metodo="grafico",
        objetivo="max",
        c=[5, 3],
        A=[[1, 1], [1, 1], [1, 0], [0, 1]],
        b=[5, 10, 8, 8],
        operadores=['<=', '>=', '<=', '<='],
        tipos_validos=["no factible", "infeasible"],
        descripcion="Restricciones contradictorias"
    ),
    Ejercicio(
        id="G5",
        nombre="Solucion en el Origen",
        metodo="grafico",
        objetivo="min",
        c=[7, 9],
        A=[[1, 1], [1, 0], [0, 1]],
        b=[0, 10, 10],
        operadores=['>=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Optimo en (0,0)"
    ),
    Ejercicio(
        id="G6",
        nombre="Solucion en un Solo Eje",
        metodo="grafico",
        objetivo="max",
        c=[5, 1],
        A=[[1, 1], [2, 1], [0, 1]],
        b=[10, 16, 6],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Optimo sobre el eje X"
    ),
    Ejercicio(
        id="G7",
        nombre="Restricciones con >=",
        metodo="grafico",
        objetivo="max",
        c=[3, 4],
        A=[[1, 1], [1, 1], [1, 0], [0, 1]],
        b=[4, 10, 6, 6],
        operadores=['>=', '<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Demandas minimas y maximas"
    ),
    Ejercicio(
        id="G8",
        nombre="Restricciones Mixtas Complejas",
        metodo="grafico",
        objetivo="min",
        c=[2, 3],
        A=[[1, 1], [2, 1], [1, 0], [0, 1], [1, 0], [0, 1]],
        b=[5, 12, 1, 1, 8, 8],
        operadores=['>=', '<=', '>=', '>=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Multiples tipos de restricciones"
    ),
]

# ============================================================================
# EJERCICIOS METODO SIMPLEX (S1-S8)
# ============================================================================

EJERCICIOS_SIMPLEX = [
    Ejercicio(
        id="S1",
        nombre="Simplex Basico - 2 Variables",
        metodo="simplex",
        objetivo="max",
        c=[4, 3],
        A=[[2, 1], [1, 2], [1, 1]],
        b=[10, 8, 6],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Problema clasico 2 variables"
    ),
    Ejercicio(
        id="S2",
        nombre="Simplex - 3 Variables",
        metodo="simplex",
        objetivo="max",
        c=[5, 4, 3],
        A=[[2, 1, 1], [1, 2, 1], [1, 1, 2]],
        b=[20, 18, 16],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica", "multiple"],
        descripcion="Produccion industrial 3 productos"
    ),
    Ejercicio(
        id="S3",
        nombre="Simplex - 4 Variables",
        metodo="simplex",
        objetivo="max",
        c=[6, 5, 4, 3],
        A=[[1, 1, 1, 1], [2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1]],
        b=[50, 60, 55, 45],
        operadores=['<=', '<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Mezcla de 4 ingredientes"
    ),
    Ejercicio(
        id="S4",
        nombre="Simplex - Solucion Degenerada",
        metodo="simplex",
        objetivo="max",
        c=[3, 2],
        A=[[1, 1], [2, 1], [1, 0], [0, 1]],
        b=[4, 6, 3, 3],
        operadores=['<=', '<=', '<=', '<='],
        tipos_validos=["unica", "degenerada"],
        descripcion="Multiples restricciones activas"
    ),
    Ejercicio(
        id="S5",
        nombre="Simplex - Soluciones Multiples",
        metodo="simplex",
        objetivo="max",
        c=[2, 2],
        A=[[1, 1], [1, 0], [0, 1]],
        b=[8, 5, 5],
        operadores=['<=', '<=', '<='],
        tipos_validos=["multiple", "infinita"],
        descripcion="FO paralela a restriccion"
    ),
    Ejercicio(
        id="S6",
        nombre="Simplex - Problema No Acotado",
        metodo="simplex",
        objetivo="max",
        c=[2, 3],
        A=[[-1, 1], [1, -2]],
        b=[5, 3],
        operadores=['<=', '<='],
        tipos_validos=["no acotado", "unbounded"],
        descripcion="Region no acotada"
    ),
    Ejercicio(
        id="S7",
        nombre="Simplex - Minimizacion",
        metodo="simplex",
        objetivo="min",
        c=[8, 6, 4],
        A=[[1, 1, 1], [2, 1, 1], [1, 1, 2]],
        b=[30, 40, 35],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Minimizar costos"
    ),
    Ejercicio(
        id="S8",
        nombre="Simplex - Coeficientes Negativos",
        metodo="simplex",
        objetivo="max",
        c=[3, 5],
        A=[[1, -1], [-1, 2], [1, 1]],
        b=[4, 6, 8],
        operadores=['<=', '<=', '<='],
        tipos_validos=["unica"],
        descripcion="Coeficientes negativos en restricciones"
    ),
]

# ============================================================================
# EJERCICIOS METODO DOS FASES (D1-D8)
# ============================================================================

EJERCICIOS_DOS_FASES = [
    Ejercicio(
        id="D1",
        nombre="Solo Restricciones >=",
        metodo="dos_fases",
        objetivo="max",
        c=[4, 5],
        A=[[1, 1], [2, 1], [1, 2], [1, 0], [0, 1]],
        b=[6, 8, 7, 10, 10],
        operadores=['>=', '>=', '>=', '<=', '<='],
        tipos_validos=["unica", "multiple"],
        descripcion="Demandas minimas"
    ),
    Ejercicio(
        id="D2",
        nombre="Solo Restricciones =",
        metodo="dos_fases",
        objetivo="max",
        c=[3, 2],
        A=[[1, 1], [2, 1]],
        b=[6, 10],
        operadores=['=', '='],
        tipos_validos=["unica"],
        descripcion="Sistema de ecuaciones"
    ),
    Ejercicio(
        id="D3",
        nombre="Mezcla de <=, >= y =",
        metodo="dos_fases",
        objetivo="max",
        c=[5, 4],
        A=[[1, 1], [2, 1], [1, 0], [0, 1]],
        b=[8, 14, 2, 1],
        operadores=['=', '<=', '>=', '>='],
        tipos_validos=["unica"],
        descripcion="Todos los tipos de restricciones"
    ),
    Ejercicio(
        id="D4",
        nombre="Dos Fases - No Factible",
        metodo="dos_fases",
        objetivo="max",
        c=[3, 4],
        A=[[1, 1], [1, 1], [1, 0], [0, 1]],
        b=[15, 8, 10, 10],
        operadores=['>=', '<=', '<=', '<='],
        tipos_validos=["no factible", "infeasible"],
        descripcion="Fase 1 falla"
    ),
    Ejercicio(
        id="D5",
        nombre="Dos Fases - Minimizacion",
        metodo="dos_fases",
        objetivo="min",
        c=[6, 4],
        A=[[1, 1], [2, 1], [1, 3]],
        b=[8, 10, 12],
        operadores=['>=', '>=', '>='],
        tipos_validos=["unica", "multiple"],
        descripcion="Minimizar con requisitos minimos"
    ),
    Ejercicio(
        id="D6",
        nombre="Dos Fases - 3 Variables",
        metodo="dos_fases",
        objetivo="max",
        c=[3, 2, 5],
        A=[[1, 1, 1], [2, 1, 1], [1, 2, 1], [0, 0, 1]],
        b=[10, 8, 15, 2],
        operadores=['=', '>=', '<=', '>='],
        tipos_validos=["unica", "multiple"],
        descripcion="Mezcla con 3 componentes"
    ),
    Ejercicio(
        id="D7",
        nombre="Dos Fases - Soluciones Multiples",
        metodo="dos_fases",
        objetivo="max",
        c=[2, 2],
        A=[[1, 1], [1, 1], [1, 0], [0, 1]],
        b=[4, 8, 5, 5],
        operadores=['>=', '<=', '<=', '<='],
        tipos_validos=["multiple", "infinita"],
        descripcion="FO paralela"
    ),
    Ejercicio(
        id="D8",
        nombre="Dos Fases - 4 Variables",
        metodo="dos_fases",
        objetivo="max",
        c=[2, 3, 4, 1],
        A=[[1, 1, 1, 1], [2, 1, 1, 1], [1, 1, 2, 1], [1, 2, 1, 2]],
        b=[20, 15, 25, 18],
        operadores=['=', '>=', '<=', '>='],
        tipos_validos=["unica", "multiple"],
        descripcion="Sistema complejo 4 variables"
    ),
]


# ============================================================================
# FUNCIONES DE PRUEBA
# ============================================================================

def verificar_servidor() -> bool:
    """Verifica conexion con el servidor Flask"""
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        return r.status_code == 200
    except:
        return False


def enviar_ejercicio(ej: Ejercicio) -> Dict[str, Any]:
    """Envia un ejercicio al endpoint correspondiente"""
    
    if ej.metodo == "grafico":
        payload = {
            "z_x": ej.c[0],
            "z_y": ej.c[1],
            "objetivo": ej.objetivo,
            "restricciones": [
                {"x": ej.A[i][0], "y": ej.A[i][1], "val": ej.b[i], "op": ej.operadores[i]}
                for i in range(len(ej.A))
            ]
        }
        url = f"{BASE_URL}/calcular"
    else:
        payload = {
            "z_coefs": ej.c,
            "objetivo": ej.objetivo,
            "restricciones": [
                {"coefs": ej.A[i], "val": ej.b[i], "op": ej.operadores[i]}
                for i in range(len(ej.A))
            ]
        }
        url = f"{BASE_URL}/calcular-simplex" if ej.metodo == "simplex" else f"{BASE_URL}/calcular-dos-fases"
    
    response = requests.post(url, json=payload, timeout=30)
    return response.json()


def verificar_tipo(tipo_obtenido: str, tipos_validos: List[str]) -> bool:
    """Verifica si el tipo de solucion es valido"""
    # Normalizar: quitar tildes y convertir a minusculas
    def normalizar(s):
        s = s.lower()
        s = s.replace('ú', 'u').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o')
        return s
    
    tipo_norm = normalizar(tipo_obtenido)
    
    for tipo_valido in tipos_validos:
        if normalizar(tipo_valido) in tipo_norm:
            return True
    return False


def ejecutar_ejercicio(ej: Ejercicio) -> Dict[str, Any]:
    """Ejecuta un ejercicio y retorna el resultado"""
    resultado = {
        "id": ej.id,
        "nombre": ej.nombre,
        "metodo": ej.metodo,
        "exito": False,
        "tipo_obtenido": "",
        "z_obtenido": None,
        "error": None
    }
    
    try:
        respuesta = enviar_ejercicio(ej)
        
        tipo = respuesta.get("tipo_solucion", respuesta.get("status", "desconocido"))
        resultado["tipo_obtenido"] = tipo
        resultado["z_obtenido"] = respuesta.get("z_optimo")
        
        if verificar_tipo(tipo, ej.tipos_validos):
            resultado["exito"] = True
        else:
            resultado["error"] = f"Tipo incorrecto: esperado alguno de {ej.tipos_validos}"
            
    except Exception as e:
        resultado["error"] = str(e)
    
    return resultado


def imprimir_resultado(res: Dict[str, Any], detallado: bool = True):
    """Imprime el resultado de un ejercicio"""
    
    if res["exito"]:
        icono = f"{Fore.GREEN}[OK]{Style.RESET_ALL}"
    else:
        icono = f"{Fore.RED}[X]{Style.RESET_ALL}"
    
    print(f"  {icono} {res['id']}: {res['nombre']}")
    
    if detallado:
        if res["tipo_obtenido"]:
            print(f"       Tipo: {res['tipo_obtenido']}")
        if res["z_obtenido"] is not None:
            print(f"       Z = {res['z_obtenido']:.4f}")
        if res["error"]:
            print(f"       {Fore.RED}Error: {res['error']}{Style.RESET_ALL}")


def ejecutar_pruebas(ejercicios: List[Ejercicio], nombre_seccion: str, detallado: bool = True) -> List[Dict]:
    """Ejecuta una lista de ejercicios"""
    
    print(f"\n{'=' * 25} {nombre_seccion} {'=' * 25}")
    
    resultados = []
    for ej in ejercicios:
        res = ejecutar_ejercicio(ej)
        resultados.append(res)
        imprimir_resultado(res, detallado)
    
    return resultados


def main(filtro: str = None):
    """Funcion principal"""
    
    print("\n" + "=" * 70)
    print("  TEST COMPLETO - CALCULADORA DE PROGRAMACION LINEAL")
    print("  24 Ejercicios | 3 Metodos | Todos los Escenarios")
    print("=" * 70)
    
    # Verificar servidor
    print(f"\nConectando a {BASE_URL}...", end=" ")
    if not verificar_servidor():
        print(f"{Fore.RED}FALLO{Style.RESET_ALL}")
        print(f"\n{Fore.RED}Error: Servidor no disponible.")
        print(f"Ejecuta: python app.py{Style.RESET_ALL}\n")
        return False
    print(f"{Fore.GREEN}OK{Style.RESET_ALL}")
    
    todos_resultados = []
    tiempo_inicio = time.time()
    
    # Filtrar ejercicios
    if filtro == "grafico":
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_GRAFICO, "METODO GRAFICO"))
    elif filtro == "simplex":
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_SIMPLEX, "METODO SIMPLEX"))
    elif filtro == "dosfases":
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_DOS_FASES, "METODO DOS FASES"))
    elif filtro == "rapido":
        # Una prueba de cada metodo
        print("\n  Modo Rapido: 1 ejercicio por metodo")
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_GRAFICO[0]))
        imprimir_resultado(todos_resultados[-1])
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_SIMPLEX[0]))
        imprimir_resultado(todos_resultados[-1])
        todos_resultados.append(ejecutar_ejercicio(EJERCICIOS_DOS_FASES[0]))
        imprimir_resultado(todos_resultados[-1])
    else:
        # Todos los ejercicios
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_GRAFICO, "METODO GRAFICO"))
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_SIMPLEX, "METODO SIMPLEX"))
        todos_resultados.extend(ejecutar_pruebas(EJERCICIOS_DOS_FASES, "METODO DOS FASES"))
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Resumen
    total = len(todos_resultados)
    exitosos = sum(1 for r in todos_resultados if r["exito"])
    fallidos = total - exitosos
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print("\n" + "=" * 70)
    print("  RESUMEN")
    print("=" * 70)
    
    # Por metodo
    for metodo, nombre in [("grafico", "Grafico"), ("simplex", "Simplex"), ("dos_fases", "Dos Fases")]:
        res_metodo = [r for r in todos_resultados if r["metodo"] == metodo]
        if res_metodo:
            ok = sum(1 for r in res_metodo if r["exito"])
            print(f"  {nombre:12} {ok}/{len(res_metodo)}")
    
    print(f"\n  {'Total':12} {exitosos}/{total}")
    print(f"  {'Tiempo':12} {tiempo_total:.2f}s")
    
    # Porcentaje con color
    if porcentaje == 100:
        color = Fore.GREEN
    elif porcentaje >= 75:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    print(f"\n  {color}Tasa de Exito: {porcentaje:.1f}%{Style.RESET_ALL}")
    
    # Ejercicios fallidos
    fallidos_lista = [r for r in todos_resultados if not r["exito"]]
    if fallidos_lista:
        print(f"\n  {Fore.RED}Ejercicios Fallidos:{Style.RESET_ALL}")
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
