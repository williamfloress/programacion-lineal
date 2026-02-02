"""
Módulo principal de solvers para Programación Lineal.

Este módulo importa y re-exporta las clases de los tres métodos de resolución:
- MetodoGrafico: Para problemas con 2 variables
- MetodoSimplex: Para problemas con múltiples variables
- MetodoDosFases: Para problemas con restricciones >= o =

También incluye la función helper convertir_restricciones_relacionales
para facilitar la entrada de restricciones en lenguaje natural.
"""

import numpy as np

# Importar las clases desde sus módulos individuales
from metodo_grafico import MetodoGrafico
from metodo_simplex import MetodoSimplex
from metodo_dos_fases import MetodoDosFases

# Exportar para que app.py pueda importar desde solver
__all__ = [
    'MetodoGrafico',
    'MetodoSimplex', 
    'MetodoDosFases',
    'convertir_restricciones_relacionales'
]


def convertir_restricciones_relacionales(restricciones_str):
    """
    Convierte restricciones escritas en forma relacional a formato estándar.
    
    Esta función ayuda a convertir restricciones como "y >= x" o "y <= 2x" 
    al formato estándar Ax + By op C que requiere el solver.
    
    CONVERSIÓN MANUAL (RECOMENDADO):
    Para mejor control, convierte manualmente usando estas reglas:
    
    1. Restricciones con relaciones entre variables:
       - "y >= x" → Mover todo al lado izquierdo: "-x + y >= 0"
         → A = [-1, 1], b = 0, op = '>='
       
       - "y <= 2x" → Mover todo al lado izquierdo: "-2x + y <= 0"
         → A = [-2, 1], b = 0, op = '<='
       
       - "y >= 2x + 5" → "-2x + y >= 5"
         → A = [-2, 1], b = 5, op = '>='
    
    2. Restricciones simples:
       - "x <= 30" → A = [1, 0], b = 30, op = '<='
       - "y <= 20" → A = [0, 1], b = 20, op = '<='
       - "x + y <= 10" → A = [1, 1], b = 10, op = '<='
    
    EJEMPLO DE USO:
    restricciones = ["y >= x", "y <= 2x", "x <= 30", "y <= 20"]
    A, b, operadores = convertir_restricciones_relacionales(restricciones)
    
    Parámetros:
        restricciones_str: Lista de strings con restricciones en forma natural
    
    Retorna:
        (A, b, operadores): Matriz A, vector b, y lista de operadores
    """
    A = []
    b = []
    operadores = []
    
    for restriccion in restricciones_str:
        restriccion = restriccion.strip().replace(" ", "")
        
        # Convertir a minúsculas para aceptar X/Y y x/y
        restriccion_lower = restriccion.lower()
        
        # Detectar operador
        if ">=" in restriccion_lower:
            partes = restriccion_lower.split(">=")
            op = ">="
        elif "<=" in restriccion_lower:
            partes = restriccion_lower.split("<=")
            op = "<="
        elif "=" in restriccion_lower:
            partes = restriccion_lower.split("=")
            op = "="
        else:
            raise ValueError(f"No se pudo detectar el operador en: {restriccion}")
        
        lado_izq = partes[0]
        lado_der = partes[1]
        
        coef_x = 0
        coef_y = 0
        b_val = 0
        
        # Parsear lado izquierdo (puede contener x, y, o ambos)
        if "x" in lado_izq:
            idx_x = lado_izq.index("x")
            if idx_x == 0:
                coef_x = 1
            else:
                coef_x_str = lado_izq[:idx_x]
                if coef_x_str in ["+", ""]:
                    coef_x = 1
                elif coef_x_str == "-":
                    coef_x = -1
                else:
                    coef_x = float(coef_x_str)
        
        if "y" in lado_izq:
            idx_y = lado_izq.index("y")
            if idx_y == 0:
                coef_y = 1
            else:
                # Buscar coeficiente antes de y
                inicio = 0
                if "x" in lado_izq and idx_y > lado_izq.index("x"):
                    inicio = lado_izq.index("x") + 1
                
                coef_y_str = lado_izq[inicio:idx_y]
                if coef_y_str in ["+", ""]:
                    coef_y = 1
                elif coef_y_str == "-":
                    coef_y = -1
                else:
                    coef_y = float(coef_y_str) if coef_y_str else 1
        
        # Parsear lado derecho
        # Si tiene variables, moverlas al lado izquierdo
        if "x" in lado_der:
            idx_x = lado_der.index("x")
            coef_der_x = 1
            if idx_x > 0:
                coef_der_x_str = lado_der[:idx_x]
                if coef_der_x_str in ["+", ""]:
                    coef_der_x = 1
                elif coef_der_x_str == "-":
                    coef_der_x = -1
                else:
                    coef_der_x = float(coef_der_x_str)
            coef_x -= coef_der_x  # Restar del lado izquierdo
            lado_der = lado_der[idx_x+1:].lstrip("+-")
        
        if "y" in lado_der:
            idx_y = lado_der.index("y")
            coef_der_y = 1
            if idx_y > 0:
                coef_der_y_str = lado_der[:idx_y]
                if coef_der_y_str in ["+", ""]:
                    coef_der_y = 1
                elif coef_der_y_str == "-":
                    coef_der_y = -1
                else:
                    coef_der_y = float(coef_der_y_str)
            coef_y -= coef_der_y  # Restar del lado izquierdo
            lado_der = lado_der[idx_y+1:].lstrip("+-")
        
        # El resto del lado derecho debe ser un número
        if lado_der and lado_der not in ["x", "y"]:
            try:
                b_val = float(lado_der)
            except ValueError:
                # Si queda algo que no es número puro, intentar extraer número
                import re
                numeros = re.findall(r'-?\d+\.?\d*', lado_der)
                if numeros:
                    b_val = float(numeros[0])
                else:
                    b_val = 0
        
        A.append([coef_x, coef_y])
        b.append(b_val)
        operadores.append(op)
    
    return A, b, operadores


# ------ ZONA DE PRUEBA -------
# 
# EJEMPLOS DE USO PARA RESTRICCIONES CON RELACIONES ENTRE VARIABLES:
#
# El solver puede manejar restricciones que relacionan variables entre sí,
# como "y >= x" o "y <= 2x". Estas deben convertirse a forma estándar:
#
# FORMA 1: Conversión Manual (Recomendado para mayor control)
# ============================================================
# Restricción: "y >= x"
# Paso 1: Mover todo al lado izquierdo → "-x + y >= 0"
# Paso 2: Identificar coeficientes:
#         - Coeficiente de x: -1
#         - Coeficiente de y: 1
#         - Valor derecho: 0
#         - Operador: >=
# Resultado: A = [-1, 1], b = 0, operador = '>='
#
# Restricción: "y <= 2x"
# Paso 1: Mover todo al lado izquierdo → "-2x + y <= 0"
# Paso 2: Identificar coeficientes:
#         - Coeficiente de x: -2
#         - Coeficiente de y: 1
#         - Valor derecho: 0
#         - Operador: <=
# Resultado: A = [-2, 1], b = 0, operador = '<='
#
# FORMA 2: Usando la función helper (más cómodo)
# ===============================================
# from solver import convertir_restricciones_relacionales
#
# restricciones = ["y >= x", "y <= 2x", "x <= 30", "y <= 20"]
# A, b, operadores = convertir_restricciones_relacionales(restricciones)
#
# EJEMPLO COMPLETO:
# =================
# c = [1, 1]  # Función objetivo: Z = x + y
# 
# A = [
#     [-1, 1],   # y >= x  →  -x + y >= 0
#     [-2, 1],   # y <= 2x →  -2x + y <= 0
#     [1, 0],    # x <= 30
#     [0, 1],    # y <= 20
# ]
# b = [0, 0, 30, 20]
# operadores = ['>=', '<=', '<=', '<=']
#
# problema = MetodoGrafico(c, A, b, operadores, objetivo='max')
# resultado = problema.resolver()

if __name__ == "__main__":
    import sys
    
    # Test case 1: Problema original con Método Gráfico
    if len(sys.argv) == 1 or sys.argv[1] == "1":
        print("="*50)
        print("TEST CASE 1: Problema Original (Método Gráfico)")
        print("="*50)
        
        # Configurar datos:
        c = [3, 2]  # Z = 3x + 2y

        # Restricciones: (Lado izquierdo de la desigualdad)
        A = [
            [2, 1],  # 2x + 1y
            [1, 1],  # 1x + 1y
            [0, 1],  # 0x + 1y
        ]

        b = [10, 8, 8]
        operadores = ['<=', '<=', '<=']

        # Crear el Objetivo:
        problema = MetodoGrafico(c, A, b, operadores, objetivo='max')
        problema.mostrar_datos()

        # Resolver: 
        resultado = problema.resolver()

        print("\n" + "="*30)
        print("SOLUCIÓN ÓPTIMA:")
        if resultado.get('status') == 'optimal':
            print(f"Punto óptimo: {resultado.get('punto_optimo')}")
            print(f"Valor Óptimo de Z: {resultado.get('z_optimo')}")
            print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
    
    # Test case 2: Restricciones con relaciones entre variables
    elif sys.argv[1] == "2":
        print("="*50)
        print("TEST CASE 2: Restricciones con relaciones entre variables")
        print("Restricciones: y >= x, y <= 2x, x <= 30, y <= 20")
        print("="*50)
        
        c = [1, 1]  # Z = x + y
        
        A = [
            [-1, 1],   # -x + y >= 0  (equivalente a y >= x)
            [-2, 1],   # -2x + y <= 0  (equivalente a y <= 2x)
            [1, 0],    # x <= 30
            [0, 1],    # y <= 20
        ]
        
        b = [0, 0, 30, 20]
        operadores = ['>=', '<=', '<=', '<=']
        
        problema = MetodoGrafico(c, A, b, operadores, objetivo='max')
        
        print("\nRestricciones en forma estándar:")
        print("R1: -x + y >= 0   (y >= x)")
        print("R2: -2x + y <= 0  (y <= 2x)")
        print("R3: x <= 30")
        print("R4: y <= 20")
        print()
        
        resultado = problema.resolver()
        
        print("\n" + "="*30)
        print("RESULTADO:")
        if resultado.get('status') == 'optimal':
            print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
            print(f"Punto óptimo: {resultado.get('punto_optimo')}")
            print(f"Valor óptimo de Z: {resultado.get('z_optimo')}")
    
    # Test case 3: Método Simplex
    elif sys.argv[1] == "3":
        print("="*50)
        print("TEST CASE 3: Método Simplex (3 variables)")
        print("="*50)
        
        c = [3, 2, 5]  # Z = 3x₁ + 2x₂ + 5x₃
        
        A = [
            [1, 2, 1],   # x₁ + 2x₂ + x₃ <= 430
            [3, 0, 2],   # 3x₁ + 2x₃ <= 460
            [1, 4, 0],   # x₁ + 4x₂ <= 420
        ]
        
        b = [430, 460, 420]
        operadores = ['<=', '<=', '<=']
        
        problema = MetodoSimplex(c, A, b, operadores, objetivo='max')
        resultado = problema.resolver()
        
        print("\n" + "="*30)
        print("RESULTADO:")
        print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
        print(f"Valor óptimo de Z: {resultado.get('z_optimo')}")
        print(f"Solución: {resultado.get('solucion')}")
    
    # Test case 4: Método de Dos Fases
    elif sys.argv[1] == "4":
        print("="*50)
        print("TEST CASE 4: Método de Dos Fases")
        print("="*50)
        
        c = [3, 2]  # Z = 3x₁ + 2x₂
        
        A = [
            [1, 1],   # x₁ + x₂ >= 4
            [1, 0],   # x₁ <= 6
            [0, 1],   # x₂ <= 6
        ]
        
        b = [4, 6, 6]
        operadores = ['>=', '<=', '<=']
        
        problema = MetodoDosFases(c, A, b, operadores, objetivo='max')
        resultado = problema.resolver()
        
        print("\n" + "="*30)
        print("RESULTADO:")
        print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
        print(f"Valor óptimo de Z: {resultado.get('z_optimo')}")
        if resultado.get('x_optimo'):
            print(f"Solución: {resultado.get('x_optimo')}")
    
    else:
        print("Uso: python solver.py [1|2|3|4]")
        print("  1: Test Método Gráfico básico")
        print("  2: Test Método Gráfico con restricciones relacionales")
        print("  3: Test Método Simplex")
        print("  4: Test Método de Dos Fases")
