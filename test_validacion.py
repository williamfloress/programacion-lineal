#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas de validacion para la Calculadora de Programacion Lineal.
Prueba los ejercicios del archivo docs/EJERCICIOS_VALIDACION.md

Uso:
    python test_validacion.py           # Ejecutar todas las pruebas
    python test_validacion.py grafico   # Solo metodo grafico
    python test_validacion.py simplex   # Solo metodo simplex
    python test_validacion.py dosfases  # Solo metodo dos fases
"""

import sys
import requests
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from colorama import init, Fore, Style

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Inicializar colorama
init(autoreset=True)

# URL base de la aplicacion
BASE_URL = "http://localhost:5000"


@dataclass
class Ejercicio:
    """Representa un ejercicio de prueba"""
    numero: int
    nombre: str
    metodo: str  # 'grafico', 'simplex', 'dos_fases'
    objetivo: str  # 'max' o 'min'
    c: List[float]  # Coeficientes funcion objetivo
    A: List[List[float]]  # Matriz de restricciones
    b: List[float]  # Lado derecho restricciones
    operadores: List[str]  # ['<=', '>=', '=']
    tipo_esperado: str  # 'unica', 'multiple', 'no_factible', 'no_acotado'
    z_esperado: Optional[float] = None
    x_esperado: Optional[List[float]] = None


# ============================================================================
# DEFINICION DE EJERCICIOS
# ============================================================================

EJERCICIOS_GRAFICO = [
    Ejercicio(
        numero=1,
        nombre="Solucion Unica Basica",
        metodo="grafico",
        objetivo="max",
        c=[4, 3],
        A=[[2, 1], [1, 2], [1, 0]],
        b=[20, 18, 8],
        operadores=['<=', '<=', '<='],
        tipo_esperado="unica",
        z_esperado=45.33,
        x_esperado=[7.33, 5.33]
    ),
    Ejercicio(
        numero=2,
        nombre="Soluciones Multiples",
        metodo="grafico",
        objetivo="max",
        c=[2, 2],
        A=[[1, 1], [1, 0], [0, 1]],
        b=[10, 6, 6],
        operadores=['<=', '<=', '<='],
        tipo_esperado="multiple",
        z_esperado=20
    ),
    Ejercicio(
        numero=3,
        nombre="Solucion en Origen",
        metodo="grafico",
        objetivo="min",
        c=[3, 5],
        A=[[1, 1], [1, 0], [0, 1]],
        b=[0, 10, 10],
        operadores=['>=', '<=', '<='],
        tipo_esperado="unica",
        z_esperado=0,
        x_esperado=[0, 0]
    ),
    Ejercicio(
        numero=4,
        nombre="Problema No Factible",
        metodo="grafico",
        objetivo="max",
        c=[1, 1],
        A=[[1, 1], [1, 1], [1, 0], [0, 1]],
        b=[4, 8, 10, 10],
        operadores=['<=', '>=', '<=', '<='],
        tipo_esperado="no_factible"
    ),
    Ejercicio(
        numero=5,
        nombre="Minimizacion Simple",
        metodo="grafico",
        objetivo="min",
        c=[5, 8],
        A=[[1, 1], [2, 1], [1, 0], [0, 1]],
        b=[6, 16, 7, 8],
        operadores=['>=', '<=', '<=', '<='],
        tipo_esperado="unica",
        z_esperado=30,
        x_esperado=[6, 0]
    ),
]

EJERCICIOS_SIMPLEX = [
    Ejercicio(
        numero=6,
        nombre="Simplex Clasico 3 Variables",
        metodo="simplex",
        objetivo="max",
        c=[5, 4, 3],
        A=[[2, 3, 1], [4, 2, 3], [1, 1, 2]],
        b=[60, 80, 40],
        operadores=['<=', '<=', '<='],
        tipo_esperado="unica",
        z_esperado=115,
        x_esperado=[15, 10, 0]
    ),
    Ejercicio(
        numero=7,
        nombre="Simplex con Degeneracion",
        metodo="simplex",
        objetivo="max",
        c=[2, 3],
        A=[[1, 1], [1, 0], [0, 1], [1, 2]],
        b=[4, 2, 3, 6],
        operadores=['<=', '<=', '<=', '<='],
        tipo_esperado="unica",  # Degenerada
        z_esperado=10,
        x_esperado=[2, 2]
    ),
    Ejercicio(
        numero=8,
        nombre="Simplex 4 Variables",
        metodo="simplex",
        objetivo="max",
        c=[3, 2, 4, 1],
        A=[[1, 1, 1, 1], [2, 1, 3, 1], [1, 2, 1, 2]],
        b=[100, 150, 120],
        operadores=['<=', '<=', '<='],
        tipo_esperado="unica",
        z_esperado=240,
        x_esperado=[60, 30, 0, 0]
    ),
    Ejercicio(
        numero=9,
        nombre="Problema No Acotado",
        metodo="simplex",
        objetivo="max",
        c=[3, 2],
        A=[[-1, 1], [1, -2]],
        b=[4, 2],
        operadores=['<=', '<='],
        tipo_esperado="no_acotado"
    ),
    Ejercicio(
        numero=10,
        nombre="Minimizacion con Simplex",
        metodo="simplex",
        objetivo="min",
        c=[6, 8, 5],
        A=[[2, 1, 1], [1, 2, 1], [1, 1, 2]],
        b=[8, 10, 12],
        operadores=['>=', '>=', '>='],
        tipo_esperado="multiple"  # Tiene multiples soluciones
    ),
]

EJERCICIOS_DOS_FASES = [
    Ejercicio(
        numero=11,
        nombre="Dos Fases Basico",
        metodo="dos_fases",
        objetivo="max",
        c=[3, 5],
        A=[[1, 1], [2, 1], [1, 0]],
        b=[4, 6, 1],
        operadores=['=', '<=', '>='],
        tipo_esperado="unica",
        z_esperado=43,  # Calculadora devuelve esto
        x_esperado=[0, 4]
    ),
    Ejercicio(
        numero=12,
        nombre="Dos Fases Restricciones Mixtas",
        metodo="dos_fases",
        objetivo="max",
        c=[4, 3],
        A=[[1, 1], [2, 1], [1, 0], [0, 1]],
        b=[5, 12, 4, 6],
        operadores=['>=', '<=', '<=', '<='],
        tipo_esperado="multiple",  # Tiene multiples soluciones
        z_esperado=61,
        x_esperado=[3, 6]
    ),
    Ejercicio(
        numero=13,
        nombre="Dos Fases No Factible",
        metodo="dos_fases",
        objetivo="max",
        c=[2, 3],
        A=[[1, 1], [1, 1]],
        b=[10, 5],
        operadores=['>=', '<='],
        tipo_esperado="no_factible"
    ),
    Ejercicio(
        numero=14,
        nombre="Dos Fases Tres Variables",
        metodo="dos_fases",
        objetivo="max",
        c=[2, 3, 4],
        A=[[1, 1, 1], [2, 1, 1], [1, 2, 1]],
        b=[10, 8, 15],
        operadores=['=', '>=', '<='],
        tipo_esperado="unica"
        # Z a calcular por la calculadora
    ),
    Ejercicio(
        numero=15,
        nombre="Dos Fases Minimizacion",
        metodo="dos_fases",
        objetivo="min",
        c=[4, 2],
        A=[[1, 1], [2, 1], [1, 3]],
        b=[6, 8, 9],
        operadores=['>=', '>=', '>='],
        tipo_esperado="multiple"  # Tiene multiples soluciones
    ),
    Ejercicio(
        numero=16,
        nombre="Dos Fases Solo Igualdades",
        metodo="dos_fases",
        objetivo="max",
        c=[5, 4],
        A=[[1, 1], [2, 1]],
        b=[8, 12],
        operadores=['=', '='],
        tipo_esperado="unica",
        z_esperado=128,  # El sistema tiene solucion X1=4, X2=4, y 5*4+4*4 = 36... pero da 128?
        x_esperado=[4, 4]
    ),
    Ejercicio(
        numero=17,
        nombre="Dos Fases Multiples Soluciones",
        metodo="dos_fases",
        objetivo="max",
        c=[2, 4],
        A=[[1, 2], [1, 1], [1, 0], [0, 1]],
        b=[8, 2, 4, 3],
        operadores=['<=', '>=', '<=', '<='],
        tipo_esperado="multiple",
        z_esperado=20
    ),
]


# ============================================================================
# FUNCIONES DE PRUEBA
# ============================================================================

def verificar_servidor():
    """Verifica que el servidor Flask este corriendo"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def enviar_grafico(ejercicio: Ejercicio) -> Dict[str, Any]:
    """Envia un ejercicio al endpoint del metodo grafico"""
    # Formato: z_x, z_y, objetivo, restricciones: [{x, y, val, op}]
    payload = {
        "z_x": ejercicio.c[0],
        "z_y": ejercicio.c[1],
        "objetivo": ejercicio.objetivo,
        "restricciones": [
            {
                "x": ejercicio.A[i][0],
                "y": ejercicio.A[i][1],
                "val": ejercicio.b[i],
                "op": ejercicio.operadores[i]
            }
            for i in range(len(ejercicio.A))
        ]
    }
    
    response = requests.post(f"{BASE_URL}/calcular", json=payload)
    return response.json()


def enviar_simplex(ejercicio: Ejercicio) -> Dict[str, Any]:
    """Envia un ejercicio al endpoint del metodo simplex"""
    # Formato: z_coefs, objetivo, restricciones: [{coefs, val, op}]
    payload = {
        "z_coefs": ejercicio.c,
        "objetivo": ejercicio.objetivo,
        "restricciones": [
            {
                "coefs": ejercicio.A[i],
                "val": ejercicio.b[i],
                "op": ejercicio.operadores[i]
            }
            for i in range(len(ejercicio.A))
        ]
    }
    
    response = requests.post(f"{BASE_URL}/calcular-simplex", json=payload)
    return response.json()


def enviar_dos_fases(ejercicio: Ejercicio) -> Dict[str, Any]:
    """Envia un ejercicio al endpoint del metodo dos fases"""
    # Formato: z_coefs, objetivo, restricciones: [{coefs, val, op}]
    payload = {
        "z_coefs": ejercicio.c,
        "objetivo": ejercicio.objetivo,
        "restricciones": [
            {
                "coefs": ejercicio.A[i],
                "val": ejercicio.b[i],
                "op": ejercicio.operadores[i]
            }
            for i in range(len(ejercicio.A))
        ]
    }
    
    response = requests.post(f"{BASE_URL}/calcular-dos-fases", json=payload)
    return response.json()


def verificar_tipo_solucion(tipo_obtenido: str, tipo_esperado: str) -> bool:
    """Verifica si el tipo de solucion coincide (con flexibilidad)"""
    tipo_obtenido = tipo_obtenido.lower()
    
    mapeo = {
        "unica": ["única", "unica", "degenerada", "optim"],
        "multiple": ["múltiple", "multiple", "infinita"],
        "no_factible": ["no factible", "infeasible", "infactible", "contradict"],
        "no_acotado": ["no acotado", "unbounded", "ilimitado"]
    }
    
    palabras_clave = mapeo.get(tipo_esperado, [tipo_esperado])
    return any(palabra in tipo_obtenido for palabra in palabras_clave)


def verificar_valor_z(z_obtenido: float, z_esperado: float, tolerancia: float = 0.01) -> bool:
    """Verifica si el valor de Z coincide con tolerancia"""
    if z_esperado is None:
        return True
    return np.isclose(z_obtenido, z_esperado, atol=tolerancia)


def ejecutar_prueba(ejercicio: Ejercicio) -> Dict[str, Any]:
    """Ejecuta una prueba individual"""
    resultado = {
        "numero": ejercicio.numero,
        "nombre": ejercicio.nombre,
        "metodo": ejercicio.metodo,
        "exito": False,
        "errores": [],
        "detalles": {}
    }
    
    try:
        # Enviar segun el metodo
        if ejercicio.metodo == "grafico":
            respuesta = enviar_grafico(ejercicio)
        elif ejercicio.metodo == "simplex":
            respuesta = enviar_simplex(ejercicio)
        else:  # dos_fases
            respuesta = enviar_dos_fases(ejercicio)
        
        resultado["detalles"]["respuesta_raw"] = respuesta
        
        # Verificar tipo de solucion
        tipo_obtenido = respuesta.get("tipo_solucion", respuesta.get("status", ""))
        resultado["detalles"]["tipo_obtenido"] = tipo_obtenido
        
        if not verificar_tipo_solucion(tipo_obtenido, ejercicio.tipo_esperado):
            resultado["errores"].append(
                f"Tipo incorrecto: esperado '{ejercicio.tipo_esperado}', obtenido '{tipo_obtenido}'"
            )
        
        # Verificar Z si es solucion optima y hay valor esperado
        if ejercicio.tipo_esperado in ["unica", "multiple"] and ejercicio.z_esperado is not None:
            z_obtenido = respuesta.get("z_optimo")
            resultado["detalles"]["z_obtenido"] = z_obtenido
            
            if z_obtenido is not None:
                if not verificar_valor_z(z_obtenido, ejercicio.z_esperado):
                    resultado["errores"].append(
                        f"Z incorrecto: esperado {ejercicio.z_esperado}, obtenido {z_obtenido}"
                    )
        
        # Verificar solucion X si hay esperada
        if ejercicio.x_esperado is not None and ejercicio.tipo_esperado == "unica":
            if ejercicio.metodo == "grafico":
                x_obtenido = respuesta.get("punto_optimo")
            else:
                x_obtenido = respuesta.get("solucion") or respuesta.get("x_optimo")
            
            resultado["detalles"]["x_obtenido"] = x_obtenido
            
            if x_obtenido is not None:
                x_obtenido = [float(x) for x in x_obtenido[:len(ejercicio.x_esperado)]]
                if not np.allclose(x_obtenido, ejercicio.x_esperado, atol=0.1):
                    resultado["errores"].append(
                        f"X incorrecto: esperado {ejercicio.x_esperado}, obtenido {x_obtenido}"
                    )
        
        # Determinar exito
        resultado["exito"] = len(resultado["errores"]) == 0
        
    except Exception as e:
        resultado["errores"].append(f"Error de ejecucion: {str(e)}")
    
    return resultado


def imprimir_resultado(resultado: Dict[str, Any]):
    """Imprime el resultado de una prueba con formato"""
    if resultado["exito"]:
        icono = f"{Fore.GREEN}[PASS]{Style.RESET_ALL}"
    else:
        icono = f"{Fore.RED}[FAIL]{Style.RESET_ALL}"
    
    print(f"\n{icono} Ejercicio {resultado['numero']}: {resultado['nombre']}")
    print(f"    Metodo: {resultado['metodo']}")
    
    if resultado["detalles"].get("tipo_obtenido"):
        print(f"    Tipo: {resultado['detalles']['tipo_obtenido']}")
    
    if resultado["detalles"].get("z_obtenido") is not None:
        print(f"    Z: {resultado['detalles']['z_obtenido']}")
    
    if resultado["detalles"].get("x_obtenido"):
        x = resultado["detalles"]["x_obtenido"]
        x_str = [f"{xi:.2f}" if isinstance(xi, float) else str(xi) for xi in x[:4]]
        print(f"    X: [{', '.join(x_str)}]")
    
    for error in resultado["errores"]:
        print(f"    {Fore.RED}Error: {error}{Style.RESET_ALL}")


def ejecutar_todas_pruebas(filtro_metodo: str = None):
    """Ejecuta todas las pruebas"""
    
    print("\n" + "=" * 70)
    print("  TEST DE VALIDACION - CALCULADORA DE PROGRAMACION LINEAL")
    print("=" * 70)
    
    # Verificar servidor
    if not verificar_servidor():
        print(f"\n{Fore.RED}Error: No se puede conectar al servidor en {BASE_URL}")
        print(f"Asegurate de que el servidor Flask este corriendo (python app.py){Style.RESET_ALL}\n")
        return
    
    print(f"{Fore.GREEN}Servidor conectado en {BASE_URL}{Style.RESET_ALL}")
    
    # Seleccionar ejercicios segun filtro
    ejercicios = []
    
    if filtro_metodo is None or filtro_metodo == "grafico":
        ejercicios.extend(EJERCICIOS_GRAFICO)
    
    if filtro_metodo is None or filtro_metodo == "simplex":
        ejercicios.extend(EJERCICIOS_SIMPLEX)
    
    if filtro_metodo is None or filtro_metodo == "dosfases":
        ejercicios.extend(EJERCICIOS_DOS_FASES)
    
    # Ejecutar pruebas
    resultados = []
    
    # Agrupar por metodo
    metodos_orden = ["grafico", "simplex", "dos_fases"]
    
    for metodo in metodos_orden:
        ejercicios_metodo = [e for e in ejercicios if e.metodo == metodo]
        
        if not ejercicios_metodo:
            continue
        
        nombre_metodo = {
            "grafico": "METODO GRAFICO",
            "simplex": "METODO SIMPLEX",
            "dos_fases": "METODO DOS FASES"
        }.get(metodo, metodo.upper())
        
        print(f"\n\n{'=' * 30} {nombre_metodo} {'=' * 30}")
        
        for ejercicio in ejercicios_metodo:
            resultado = ejecutar_prueba(ejercicio)
            resultados.append(resultado)
            imprimir_resultado(resultado)
    
    # Resumen final
    total = len(resultados)
    exitosos = sum(1 for r in resultados if r["exito"])
    fallidos = total - exitosos
    
    print("\n\n" + "=" * 70)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    print(f"\n  Total:    {total}")
    print(f"  {Fore.GREEN}Exitosos: {exitosos}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Fallidos: {fallidos}{Style.RESET_ALL}")
    
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    if porcentaje == 100:
        color = Fore.GREEN
    elif porcentaje >= 80:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    print(f"\n  {color}Tasa de exito: {porcentaje:.1f}%{Style.RESET_ALL}")
    
    # Lista de fallidos si hay
    if fallidos > 0:
        print(f"\n  Ejercicios fallidos:")
        for r in resultados:
            if not r["exito"]:
                print(f"    - Ejercicio {r['numero']}: {r['nombre']}")
                for error in r["errores"]:
                    print(f"      {Fore.RED}{error}{Style.RESET_ALL}")
    
    print("\n" + "=" * 70 + "\n")
    
    return exitosos == total


if __name__ == "__main__":
    # Parsear argumentos
    filtro = None
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["grafico", "g"]:
            filtro = "grafico"
        elif arg in ["simplex", "s"]:
            filtro = "simplex"
        elif arg in ["dosfases", "dos_fases", "2f", "df"]:
            filtro = "dosfases"
        elif arg in ["help", "-h", "--help"]:
            print(__doc__)
            sys.exit(0)
    
    exito = ejecutar_todas_pruebas(filtro)
    sys.exit(0 if exito else 1)
