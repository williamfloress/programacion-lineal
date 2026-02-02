#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas automáticas para la Calculadora de Programación Lineal.
Prueba todos los ejercicios del archivo EJERCICIOS_PRUEBA.md
"""

import sys
import os
import requests
import json
import re
from typing import Dict, List, Any, Optional
from colorama import init, Fore, Style

# Obtener directorio del script para rutas relativas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Inicializar colorama para colores en terminal
init(autoreset=True)

# URL base de la aplicación (ajustar según tu configuración)
BASE_URL = "http://localhost:5000"

class TestResultado:
    def __init__(self, ejercicio: str, metodo: str):
        self.ejercicio = ejercicio
        self.metodo = metodo
        self.pasado = False
        self.errores = []
        self.warnings = []
        self.detalles = {}
    
    def agregar_error(self, mensaje: str):
        self.errores.append(mensaje)
    
    def agregar_warning(self, mensaje: str):
        self.warnings.append(mensaje)
    
    def marcar_exitoso(self):
        self.pasado = len(self.errores) == 0


class EjercicioParser:
    """Parsea el archivo EJERCICIOS_PRUEBA.md"""
    
    @staticmethod
    def extraer_ejercicios(ruta_archivo: str) -> List[Dict[str, Any]]:
        """Extrae todos los ejercicios del archivo markdown"""
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        ejercicios = []
        
        # Primero, dividir por secciones de métodos
        seccion_actual = "grafico"  # Default
        
        # Dividir por ejercicios (buscar ### Ejercicio)
        patron_ejercicio = r'### (Ejercicio \d+[AB]?:[^\n]+)'
        partes = re.split(patron_ejercicio, contenido)
        
        for i in range(1, len(partes), 2):
            titulo = partes[i]
            cuerpo = partes[i + 1] if i + 1 < len(partes) else ""
            
            # Detectar cambio de sección antes del ejercicio
            context_previo = partes[i-1] if i > 0 else ""
            if "MÉTODO GRÁFICO" in context_previo[-200:]:
                seccion_actual = "grafico"
            elif "MÉTODO SIMPLEX" in context_previo[-200:]:
                seccion_actual = "simplex"
            elif "MÉTODO DE DOS FASES" in context_previo[-200:] or "DOS FASES" in context_previo[-200:]:
                seccion_actual = "dos_fases"
            
            ejercicio = EjercicioParser._parsear_ejercicio(titulo, cuerpo, seccion_actual)
            if ejercicio:
                ejercicios.append(ejercicio)
        
        return ejercicios
    
    @staticmethod
    def _parsear_ejercicio(titulo: str, cuerpo: str, seccion: str = None) -> Optional[Dict[str, Any]]:
        """Parsea un ejercicio individual"""
        
        # Extraer número de ejercicio
        match_num = re.search(r'Ejercicio (\d+[AB]?)', titulo)
        if not match_num:
            return None
        
        num_ejercicio = match_num.group(1)
        
        # Determinar método basado en sección detectada o inferir
        metodo = seccion
        if not metodo:
            if "Simplex" in titulo or "SIMPLEX" in cuerpo:
                metodo = "simplex"
            elif "Dos Fases" in titulo or "DOS FASES" in cuerpo:
                metodo = "dos_fases"
            else:
                # Inferir por número de ejercicio
                num = int(re.search(r'\d+', num_ejercicio).group())
                if num <= 8:
                    metodo = "grafico"
                elif num <= 13:
                    metodo = "simplex"
                else:
                    metodo = "dos_fases"
        
        # Extraer función objetivo
        objetivo_match = re.search(r'- (Maximizar|Minimizar) Z = (.+)', cuerpo)
        if not objetivo_match:
            return None
        
        tipo_objetivo = objetivo_match.group(1).lower()
        funcion_z = objetivo_match.group(2).strip()
        
        # Extraer restricciones (dentro de triple backticks)
        restricciones_match = re.search(r'```\n(.*?)\n```', cuerpo, re.DOTALL)
        restricciones_raw = []
        if restricciones_match:
            # Filtrar solo las restricciones de no-negatividad (X ≥ 0, Y ≥ 0, etc.)
            restricciones_raw = [r.strip() for r in restricciones_match.group(1).split('\n') 
                                if r.strip() and not re.match(r'^[XY].*[≥>=]\s*0\s*$', r.strip()) 
                                and not re.match(r'^X[₀₁₂₃₄₅₆₇₈₉,\s]+[≥>=]\s*0\s*$', r.strip())]
        
        # Extraer solución esperada
        solucion_esperada = EjercicioParser._extraer_solucion_esperada(cuerpo)
        
        return {
            'numero': num_ejercicio,
            'titulo': titulo,
            'metodo': metodo,
            'objetivo': tipo_objetivo,
            'funcion_z': funcion_z,
            'restricciones': restricciones_raw,
            'solucion_esperada': solucion_esperada
        }
    
    @staticmethod
    def _extraer_solucion_esperada(cuerpo: str) -> Dict[str, Any]:
        """Extrae la solución esperada del ejercicio"""
        solucion = {
            'tipo': None,
            'valores': {},
            'z_optimo': None
        }
        
        # Buscar tipo de solución
        tipo_match = re.search(r'\*\*Tipo:\*\* (.+)', cuerpo)
        if tipo_match:
            solucion['tipo'] = tipo_match.group(1).strip()
        
        # Buscar valores de variables (X = valor, Y = valor, etc.)
        valores_matches = re.findall(r'- ([XY]|X[₀-₉]+) = ([\d.]+)', cuerpo)
        for var, val in valores_matches:
            solucion['valores'][var] = float(val)
        
        # Buscar Z óptimo
        z_match = re.search(r'- Z = ([\d.]+)', cuerpo)
        if z_match:
            solucion['z_optimo'] = float(z_match.group(1))
        
        return solucion


class CalculadoraTester:
    """Ejecuta pruebas contra la calculadora"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.resultados = []
    
    def probar_ejercicio_grafico(self, ejercicio: Dict[str, Any]) -> TestResultado:
        """Prueba un ejercicio del método gráfico"""
        resultado = TestResultado(ejercicio['numero'], 'Gráfico')
        
        try:
            # Parsear función Z
            z_data = self._parsear_funcion_z_grafico(ejercicio['funcion_z'])
            resultado.detalles['z_parseado'] = z_data
            
            # Parsear restricciones
            restricciones = self._parsear_restricciones_grafico(ejercicio['restricciones'])
            resultado.detalles['restricciones_raw'] = ejercicio['restricciones']
            resultado.detalles['restricciones_parseadas'] = restricciones
            
            # Hacer request
            payload = {
                'objetivo': 'max' if ejercicio['objetivo'] == 'maximizar' else 'min',
                'z_x': z_data['x'],
                'z_y': z_data['y'],
                'restricciones': restricciones
            }
            
            response = requests.post(f"{self.base_url}/calcular", json=payload, timeout=10)
            response.raise_for_status()
            datos = response.json()
            
            # Verificar resultados
            self._verificar_resultados_grafico(datos, ejercicio['solucion_esperada'], resultado)
            
        except Exception as e:
            resultado.agregar_error(f"Error al ejecutar: {str(e)}")
        
        resultado.marcar_exitoso()
        return resultado
    
    def probar_ejercicio_simplex(self, ejercicio: Dict[str, Any]) -> TestResultado:
        """Prueba un ejercicio del método Simplex"""
        resultado = TestResultado(ejercicio['numero'], 'Simplex')
        
        try:
            # Parsear función Z
            z_data = self._parsear_funcion_z_simplex(ejercicio['funcion_z'])
            
            # Parsear restricciones
            restricciones = self._parsear_restricciones_simplex(ejercicio['restricciones'], z_data['num_vars'])
            
            # Hacer request
            payload = {
                'objetivo': 'max' if ejercicio['objetivo'] == 'maximizar' else 'min',
                'num_variables': z_data['num_vars'],
                'z_coefs': z_data['coefs'],  # Corregido: z_coefs en lugar de coeficientes_z
                'restricciones': restricciones
            }
            
            response = requests.post(f"{self.base_url}/calcular-simplex", json=payload, timeout=10)
            response.raise_for_status()
            datos = response.json()
            
            # Verificar resultados
            self._verificar_resultados_simplex(datos, ejercicio['solucion_esperada'], resultado)
            
        except Exception as e:
            resultado.agregar_error(f"Error al ejecutar: {str(e)}")
        
        resultado.marcar_exitoso()
        return resultado
    
    def probar_ejercicio_dos_fases(self, ejercicio: Dict[str, Any]) -> TestResultado:
        """Prueba un ejercicio del método Dos Fases"""
        resultado = TestResultado(ejercicio['numero'], 'Dos Fases')
        
        try:
            # Parsear función Z
            z_data = self._parsear_funcion_z_simplex(ejercicio['funcion_z'])
            
            # Parsear restricciones
            restricciones = self._parsear_restricciones_dos_fases(ejercicio['restricciones'], z_data['num_vars'])
            
            # Hacer request
            payload = {
                'objetivo': 'max' if ejercicio['objetivo'] == 'maximizar' else 'min',
                'num_variables': z_data['num_vars'],
                'z_coefs': z_data['coefs'],  # Corregido: z_coefs en lugar de coeficientes_z
                'restricciones': restricciones
            }
            
            response = requests.post(f"{self.base_url}/calcular-dos-fases", json=payload, timeout=10)
            response.raise_for_status()
            datos = response.json()
            
            # Verificar resultados
            self._verificar_resultados_dos_fases(datos, ejercicio['solucion_esperada'], resultado)
            
        except Exception as e:
            resultado.agregar_error(f"Error al ejecutar: {str(e)}")
        
        resultado.marcar_exitoso()
        return resultado
    
    def _parsear_funcion_z_grafico(self, funcion_z: str) -> Dict[str, float]:
        """Parsea función Z para método gráfico (X, Y)"""
        # Ejemplo: "3X + 2Y" o "5X - 3Y"
        funcion_z = funcion_z.replace(' ', '').upper()
        
        # Buscar coeficiente de X
        x_match = re.search(r'([+-]?\d*\.?\d*)X', funcion_z)
        coef_x = 1.0
        if x_match:
            coef_str = x_match.group(1)
            if coef_str in ['', '+']:
                coef_x = 1.0
            elif coef_str == '-':
                coef_x = -1.0
            else:
                coef_x = float(coef_str)
        
        # Buscar coeficiente de Y
        y_match = re.search(r'([+-]?\d*\.?\d*)Y', funcion_z)
        coef_y = 1.0
        if y_match:
            coef_str = y_match.group(1)
            if coef_str in ['', '+']:
                coef_y = 1.0
            elif coef_str == '-':
                coef_y = -1.0
            else:
                coef_y = float(coef_str)
        
        return {'x': coef_x, 'y': coef_y}
    
    def _parsear_funcion_z_simplex(self, funcion_z: str) -> Dict[str, Any]:
        """Parsea función Z para Simplex/Dos Fases (X₁, X₂, ...)"""
        funcion_z = funcion_z.replace(' ', '').upper()
        
        # Detectar número de variables
        vars_encontradas = re.findall(r'X[₀₁₂₃₄₅₆₇₈₉]+', funcion_z)
        
        # Convertir subíndices a números
        subindices_map = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', 
                          '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}
        
        num_vars = 0
        for var in vars_encontradas:
            sub = var[1:]  # Quitar la X
            num_str = ''.join(subindices_map.get(c, c) for c in sub)
            num_vars = max(num_vars, int(num_str))
        
        # Extraer coeficientes
        coefs = [0.0] * num_vars
        
        for i in range(1, num_vars + 1):
            # Buscar X con subíndice i
            subscript = ''.join(k for k, v in subindices_map.items() if v == str(i))
            pattern = rf'([+-]?\d*\.?\d*)X{subscript}'
            match = re.search(pattern, funcion_z)
            
            if match:
                coef_str = match.group(1)
                if coef_str in ['', '+']:
                    coefs[i-1] = 1.0
                elif coef_str == '-':
                    coefs[i-1] = -1.0
                else:
                    coefs[i-1] = float(coef_str)
        
        return {'num_vars': num_vars, 'coefs': coefs}
    
    def _parsear_restricciones_grafico(self, restricciones: List[str]) -> List[Dict[str, Any]]:
        """Parsea restricciones para método gráfico"""
        result = []
        
        for rest in restricciones:
            rest = rest.replace(' ', '').upper()
            
            # Detectar operador
            if '<=' in rest or '≤' in rest:
                op = '<='
                partes = re.split(r'<=|≤', rest)
            elif '>=' in rest or '≥' in rest:
                op = '>='
                partes = re.split(r'>=|≥', rest)
            elif '=' in rest:
                op = '='
                partes = rest.split('=')
            else:
                continue
            
            lado_izq = partes[0]
            lado_der = partes[1] if len(partes) > 1 else '0'
            
            # Extraer coeficientes con regex más robusto
            # Para X
            coef_x = 0.0
            if 'X' in lado_izq:
                # Buscar patrón: número opcional + X
                x_pattern = r'([+-]?\d+\.?\d*)X'
                x_match = re.search(x_pattern, lado_izq)
                if x_match and x_match.group(1):
                    coef_str = x_match.group(1)
                    if coef_str in ['+', '']:
                        coef_x = 1.0
                    elif coef_str == '-':
                        coef_x = -1.0
                    else:
                        coef_x = float(coef_str)
                else:
                    coef_x = 1.0  # Solo "X" sin número
            
            # Para Y
            coef_y = 0.0
            if 'Y' in lado_izq:
                # Buscar patrón: número opcional + Y
                y_pattern = r'([+-]?\d+\.?\d*)Y'
                y_match = re.search(y_pattern, lado_izq)
                if y_match and y_match.group(1):
                    coef_str = y_match.group(1)
                    if coef_str in ['+', '']:
                        coef_y = 1.0
                    elif coef_str == '-':
                        coef_y = -1.0
                    else:
                        coef_y = float(coef_str)
                else:
                    coef_y = 1.0  # Solo "Y" sin número
            
            # Extraer valor del lado derecho
            val = float(lado_der) if lado_der.replace('.', '').replace('-', '').isdigit() else 0.0
            
            result.append({
                'x': coef_x,
                'y': coef_y,
                'op': op,
                'val': val
            })
        
        return result
    
    def _parsear_restricciones_simplex(self, restricciones: List[str], num_vars: int) -> List[Dict[str, Any]]:
        """Parsea restricciones para Simplex"""
        result = []
        
        for rest in restricciones:
            rest = rest.replace(' ', '').upper()
            
            # Detectar operador
            if '<=' in rest or '≤' in rest:
                op = '<='
                partes = re.split(r'<=|≤', rest)
            elif '>=' in rest or '≥' in rest:
                op = '>='
                partes = re.split(r'>=|≥', rest)
            elif '=' in rest and '<=' not in rest and '>=' not in rest:
                op = '='
                partes = rest.split('=')
            else:
                continue
            
            lado_izq = partes[0]
            lado_der = partes[1] if len(partes) > 1 else '0'
            
            # Inicializar coeficientes para todas las variables
            coefs = [0.0] * num_vars
            
            # Convertir subíndices Unicode a números
            subindices_map = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', 
                              '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}
            
            # Extraer todos los términos con X
            for i in range(1, num_vars + 1):
                # Crear patrón para Xi con subíndice Unicode
                sub_unicode = ''.join([k for k, v in subindices_map.items() if v == str(i)])
                
                # Buscar patrones mejorados para capturar coeficientes
                patterns = [
                    rf'([+-]?\d*\.?\d*)X{sub_unicode}',  # Con subíndice Unicode
                    rf'([+-]?\d*\.?\d*)X{i}',             # Con número normal
                ]
                
                coef_encontrado = False
                for pattern in patterns:
                    match = re.search(pattern, lado_izq)
                    if match:
                        coef_str = match.group(1)
                        if coef_str in ['+', '', ' ']:
                            coefs[i-1] = 1.0
                        elif coef_str == '-':
                            coefs[i-1] = -1.0
                        elif coef_str:
                            try:
                                coefs[i-1] = float(coef_str)
                            except:
                                coefs[i-1] = 1.0
                        else:
                            coefs[i-1] = 1.0
                        coef_encontrado = True
                        break
            
            # Extraer valor del lado derecho
            val = 0.0
            try:
                val = float(lado_der) if lado_der.replace('.', '').replace('-', '').isdigit() else 0.0
            except:
                val = 0.0
            
            result.append({
                'coefs': coefs,
                'op': op,
                'val': val
            })
        
        return result
    
    def _parsear_restricciones_dos_fases(self, restricciones: List[str], num_vars: int) -> List[Dict[str, Any]]:
        """Parsea restricciones para Dos Fases (mismo formato que Simplex)"""
        return self._parsear_restricciones_simplex(restricciones, num_vars)
    
    def _verificar_resultados_grafico(self, datos: Dict, esperado: Dict, resultado: TestResultado):
        """Verifica resultados del método gráfico"""
        # Verificar tipo de solución (más flexible)
        if esperado['tipo']:
            tipo_obtenido = datos.get('tipo_solucion', '')
            tipo_esperado = esperado['tipo']
            
            # Normalizar para comparación flexible
            tipo_obtenido_norm = tipo_obtenido.lower().replace(' ', '')
            tipo_esperado_norm = tipo_esperado.lower().replace(' ', '')
            
            # Verificar coincidencia flexible
            palabras_clave = ['única', 'unica', 'múltiple', 'multiple', 'infinita', 'degenerada', 
                             'factible', 'acotado', 'acotada']
            coincide = False
            
            for palabra in palabras_clave:
                if palabra in tipo_esperado_norm and palabra in tipo_obtenido_norm:
                    coincide = True
                    break
            
            if not coincide:
                resultado.agregar_error(f"Tipo de solución incorrecto. Esperado: '{esperado['tipo']}', Obtenido: '{tipo_obtenido}'")
        
        # Verificar Z óptimo (con tolerancia)
        if esperado['z_optimo'] is not None and datos.get('status') == 'optimal':
            z_obtenido = datos.get('z_optimo', 0)
            if abs(z_obtenido - esperado['z_optimo']) > 0.1:
                resultado.agregar_error(f"Z óptimo incorrecto. Esperado: {esperado['z_optimo']}, Obtenido: {z_obtenido}")
        
        # Verificar valores de variables
        if datos.get('status') == 'optimal' and esperado['valores']:
            punto = datos.get('punto_optimo', [])
            if 'X' in esperado['valores'] and len(punto) > 0:
                if abs(punto[0] - esperado['valores']['X']) > 0.1:
                    resultado.agregar_warning(f"Valor de X difiere. Esperado: {esperado['valores']['X']}, Obtenido: {punto[0]}")
            if 'Y' in esperado['valores'] and len(punto) > 1:
                if abs(punto[1] - esperado['valores']['Y']) > 0.1:
                    resultado.agregar_warning(f"Valor de Y difiere. Esperado: {esperado['valores']['Y']}, Obtenido: {punto[1]}")
    
    def _verificar_resultados_simplex(self, datos: Dict, esperado: Dict, resultado: TestResultado):
        """Verifica resultados del método Simplex"""
        # Similar a gráfico
        self._verificar_resultados_grafico(datos, esperado, resultado)
    
    def _verificar_resultados_dos_fases(self, datos: Dict, esperado: Dict, resultado: TestResultado):
        """Verifica resultados del método Dos Fases"""
        # Similar a gráfico
        self._verificar_resultados_grafico(datos, esperado, resultado)


def imprimir_reporte(resultados: List[TestResultado]):
    """Imprime un reporte colorido de los resultados"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}REPORTE DE PRUEBAS - CALCULADORA DE PROGRAMACIÓN LINEAL{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    total = len(resultados)
    exitosos = sum(1 for r in resultados if r.pasado)
    fallidos = total - exitosos
    
    # Resumen general
    print(f"{Fore.WHITE}{Style.BRIGHT}RESUMEN GENERAL:{Style.RESET_ALL}")
    print(f"  Total de ejercicios probados: {total}")
    print(f"  {Fore.GREEN}✓ Exitosos: {exitosos}{Style.RESET_ALL}")
    print(f"  {Fore.RED}✗ Fallidos: {fallidos}{Style.RESET_ALL}")
    print(f"  Tasa de éxito: {(exitosos/total*100):.1f}%\n")
    
    # Resultados por método
    metodos = {}
    for r in resultados:
        if r.metodo not in metodos:
            metodos[r.metodo] = {'total': 0, 'exitosos': 0}
        metodos[r.metodo]['total'] += 1
        if r.pasado:
            metodos[r.metodo]['exitosos'] += 1
    
    print(f"{Fore.WHITE}{Style.BRIGHT}POR MÉTODO:{Style.RESET_ALL}")
    for metodo, stats in metodos.items():
        tasa = (stats['exitosos'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {metodo}: {stats['exitosos']}/{stats['total']} ({tasa:.1f}%)")
    
    print("\n" + "-"*80 + "\n")
    
    # Detalles de cada ejercicio
    print(f"{Fore.WHITE}{Style.BRIGHT}DETALLES DE EJERCICIOS:{Style.RESET_ALL}\n")
    
    for r in resultados:
        if r.pasado:
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} Ejercicio {r.ejercicio} ({r.metodo})")
        else:
            print(f"{Fore.RED}✗{Style.RESET_ALL} Ejercicio {r.ejercicio} ({r.metodo})")
            for error in r.errores:
                print(f"    {Fore.RED}ERROR:{Style.RESET_ALL} {error}")
            for warning in r.warnings:
                print(f"    {Fore.YELLOW}WARN:{Style.RESET_ALL} {warning}")
    
    print("\n" + "="*80 + "\n")


def main():
    """Función principal"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*70)
    print("  TEST AUTOMATICO - CALCULADORA DE PROGRAMACION LINEAL")
    print("="*70)
    print(Style.RESET_ALL)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"{Fore.GREEN}✓ Servidor detectado en {BASE_URL}{Style.RESET_ALL}\n")
    except:
        print(f"{Fore.RED}✗ Error: No se puede conectar al servidor en {BASE_URL}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Asegúrate de que el servidor Flask esté corriendo (python app.py){Style.RESET_ALL}\n")
        return
    
    # Parsear ejercicios
    archivo_ejercicios = os.path.join(SCRIPT_DIR, 'EJERCICIOS_PRUEBA.md')
    print(f"{Fore.CYAN}Parseando ejercicios de {archivo_ejercicios}...{Style.RESET_ALL}")
    ejercicios = EjercicioParser.extraer_ejercicios(archivo_ejercicios)
    print(f"{Fore.GREEN}✓ {len(ejercicios)} ejercicios encontrados{Style.RESET_ALL}\n")
    
    # Ejecutar pruebas
    tester = CalculadoraTester(BASE_URL)
    resultados = []
    
    print(f"{Fore.CYAN}Ejecutando pruebas...{Style.RESET_ALL}\n")
    
    # Probar ejercicios: Gráfico (1-8), Simplex (9-13), Dos Fases (14-19)
    ejercicios_a_probar = ejercicios[:19]  # Probar hasta el ejercicio 19
    
    for i, ej in enumerate(ejercicios_a_probar, 1):
        print(f"[{i}/{len(ejercicios_a_probar)}] Probando Ejercicio {ej['numero']}...", end=" ")
        
        if ej['metodo'] == 'grafico':
            resultado = tester.probar_ejercicio_grafico(ej)
        elif ej['metodo'] == 'simplex':
            resultado = tester.probar_ejercicio_simplex(ej)
        elif ej['metodo'] == 'dos_fases':
            resultado = tester.probar_ejercicio_dos_fases(ej)
        else:
            continue
        
        resultados.append(resultado)
        
        if resultado.pasado:
            print(f"{Fore.GREEN}✓ PASÓ{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ FALLÓ{Style.RESET_ALL}")
    
    # Imprimir reporte
    imprimir_reporte(resultados)


if __name__ == "__main__":
    main()
