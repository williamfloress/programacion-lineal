import numpy as np

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
        
        # Detectar operador
        if ">=" in restriccion:
            partes = restriccion.split(">=")
            op = ">="
        elif "<=" in restriccion:
            partes = restriccion.split("<=")
            op = "<="
        elif "=" in restriccion:
            partes = restriccion.split("=")
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


class MetodoGrafico:
    def __init__(self, c, A, b,operadores, objetivo='max'):
        """
        c: Coeficientes de la función objetivo[c1, c2]
        A: Matriz de coeficientes de las restricciones (lado izquierdo)
        b: Vector de limites de restricciones(lado derecho)
        objetivo: 'max' o 'min'
        """
        self.c = np.array(c)
        self.A = np.array(A)
        self.b = np.array(b)
        self.objetivo = objetivo
        self.operadores = operadores
        self.vertice = [] #Guardaremos aqui los puntos clave.
        #Guardaremos los datos del LOG en una lista
        self.pasos = []
    
    def registrar_paso(self, mensaje):
        """Guarda un mensaje en la lista de pasos."""
        self.pasos.append(mensaje)


    def mostrar_datos(self):
        print(f"Objetivo: {self.objetivo} Z= {self.c[0]}x + {self.c[1]}y")
        print("Restricciones:")
        for i in range(len(self.b)):
            print(f"{self.A[i][0]}x + {self.A[i][1]}y <= {self.b[i]}")

    def encontrar_intersecciones(self):
        posibles_puntos = []

        ## 1. Añadimos las restricciones de no negatividad (ejes X e Y) a la matriz
        # x >= 0 es como -1x + 0y <= 0 (truco matemático para estandarizar)
        # Pero para simplificar, asumiremos que buscamos cruces entre restricciones dadas + ejes.
        
        #Combinamos las restricciones dadas con los ejes x= 0, y= 0.
        # Eje Y (x= 0) -> [1, 0] = 0
        # Eje X (y= 0) -> [0, 1] = 0
        matriz_total_A = np.vstack([self.A, [[1, 0], [0, 1]]])
        vector_total_b = np.concatenate([self.b, [0,0]])

        num_lineas = len(vector_total_b)

        #2. Doble Bucle: Cruzar la linea 'i' con la linea 'j' 
        for i in range(num_lineas):
            for j in range (i + 1, num_lineas):
                #formamos un sistema de ecuaciones 2x2 para resolver.
                a_sistema =np.array([matriz_total_A[i], matriz_total_A[j]])
                b_sistema = np.array([vector_total_b[i], vector_total_b[j]])

                try:
                    #Esta es la MAGIA: Resuelve el sistema ax + by = c
                    punto = np.linalg.solve(a_sistema, b_sistema)
                    posibles_puntos.append(punto)
                except np.linalg.LinAlgError:
                    #Si las lineas son paralelas, linalg.solve lanza un error, lo ignoramos.
                    continue

        return posibles_puntos

    #3Paso: Filtrar los puntos de la region factible.

    def es_factible(self, punto):
        x, y = punto
        if x < -1e-9 or y < -1e-9: return False
        
        for i in range(len(self.b)):
            valor = np.dot(self.A[i], punto)
            limite = self.b[i]
            op = self.operadores[i]
            
            if op == '<=' and valor > limite + 1e-9: return False
            if op == '>=' and valor < limite - 1e-9: return False
            if op == '=' and not np.isclose(valor, limite): return False
        return True

    def obtener_vertices_validos(self):
        todos_puntos = self.encontrar_intersecciones()
        validos = []
        for p in todos_puntos:
            if self.es_factible(p):
                validos.append(p)
        
        #Eliminamos duplicados (A veces intersecciones se repiten)
        self.vertice = np.unique(np.array(validos), axis =0)
        return self.vertice

    #4 Paso: Encontrar el Valor Optimo de la funcion objetivo.
    def resolver(self):
        # Formatear función objetivo con operadores correctos
        signo_y = '-' if self.c[1] < 0 else '+'
        abs_y = abs(self.c[1])
        self.registrar_paso(f"FUNCIÓN OBJETIVO: {self.objetivo.upper()} Z = {self.c[0]}x {signo_y} {abs_y}y")
        
        # Mostrar restricciones
        self.registrar_paso("RESTRICCIONES:")
        for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
            signo_y = '-' if a_row[1] < 0 else '+'
            abs_y = abs(a_row[1])
            self.registrar_paso(f"  R{idx}: {a_row[0]}x {signo_y} {abs_y}y {op} {b_val}")
        
        # 1. Intersecciones
        puntos_corte = []
        # Agregamos límites "virtuales" muy grandes para evitar errores numéricos en problemas abiertos
        # pero matemáticamente el método gráfico busca cruces.
        matriz_total = np.vstack([self.A, [[1, 0], [0, 1]]])
        vector_total = np.concatenate([self.b, [0, 0]])
        
        # Etiquetas para las líneas (restricciones + ejes)
        etiquetas = [f"R{i+1}" for i in range(len(self.A))] + ["Eje Y (x=0)", "Eje X (y=0)"]
        
        self.registrar_paso("CÁLCULO DE INTERSECCIONES:")
        num_lineas = len(vector_total)
        intersecciones_info = []
        
        for i in range(num_lineas):
            for j in range(i + 1, num_lineas):
                try:
                    A_temp = np.array([matriz_total[i], matriz_total[j]])
                    b_temp = np.array([vector_total[i], vector_total[j]])
                    punto = np.linalg.solve(A_temp, b_temp)
                    puntos_corte.append(punto)
                    
                    # Mostrar el cálculo de la intersección con formato correcto
                    signo1_y = '-' if matriz_total[i][1] < 0 else '+'
                    abs1_y = abs(matriz_total[i][1])
                    signo2_y = '-' if matriz_total[j][1] < 0 else '+'
                    abs2_y = abs(matriz_total[j][1])
                    eq1 = f"{matriz_total[i][0]}x {signo1_y} {abs1_y}y = {vector_total[i]}"
                    eq2 = f"{matriz_total[j][0]}x {signo2_y} {abs2_y}y = {vector_total[j]}"
                    self.registrar_paso(f"  {etiquetas[i]} ∩ {etiquetas[j]}:")
                    self.registrar_paso(f"    Sistema: {eq1} y {eq2}")
                    self.registrar_paso(f"    Solución: P({punto[0]:.2f}, {punto[1]:.2f})")
                    
                    intersecciones_info.append({
                        "punto": [float(punto[0]), float(punto[1])],
                        "lineas": [etiquetas[i], etiquetas[j]]
                    })
                except np.linalg.LinAlgError:
                    continue

        # 2. Filtrar y verificar factibilidad
        self.registrar_paso("VERIFICACIÓN DE FACTIBILIDAD:")
        validos = []
        validos_info = []
        
        for info in intersecciones_info:
            p = np.array(info["punto"])
            es_valido = self.es_factible(p)
            
            # Mostrar verificación de cada restricción
            self.registrar_paso(f"  Punto P({p[0]:.2f}, {p[1]:.2f}):")
            factible = True
            
            # Verificar no negatividad
            if p[0] < -1e-9 or p[1] < -1e-9:
                self.registrar_paso(f"    ✗ No cumple: x ≥ 0, y ≥ 0")
                factible = False
            else:
                self.registrar_paso(f"    ✓ Cumple: x ≥ 0, y ≥ 0")
            
            # Verificar cada restricción
            for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
                valor = np.dot(a_row, p)
                cumple = False
                
                if op == '<=' and valor <= b_val + 1e-9:
                    cumple = True
                elif op == '>=' and valor >= b_val - 1e-9:
                    cumple = True
                elif op == '=' and np.isclose(valor, b_val):
                    cumple = True
                
                simbolo = "✓" if cumple else "✗"
                signo_y = '-' if a_row[1] < 0 else '+'
                abs_a1 = abs(a_row[1])
                signo_calc = '-' if a_row[1]*p[1] < 0 else '+'
                abs_calc = abs(a_row[1]*p[1])
                self.registrar_paso(f"    {simbolo} R{idx}: {a_row[0]}·{p[0]:.2f} {signo_y} {abs_a1}·{p[1]:.2f} = {a_row[0]*p[0]:.2f} {signo_calc} {abs_calc} = {valor:.2f} {op} {b_val}")
                
                if not cumple:
                    factible = False
            
            if factible:
                self.registrar_paso(f"    → P({p[0]:.2f}, {p[1]:.2f}) es FACTIBLE")
                validos.append(p)
                validos_info.append(info)
            else:
                self.registrar_paso(f"    → P({p[0]:.2f}, {p[1]:.2f}) NO es factible")
        
        if not validos:
            self.registrar_paso("RESULTADO: No existe ningún punto que cumpla todas las restricciones.")
            return {
                "status": "infeasible",
                "tipo_solucion": "No Factible",
                "explicacion": "Las restricciones son contradictorias. No existe una región común entre ellas.",
                "pasos": self.pasos
            }

        # Eliminamos duplicados
        self.vertices = np.unique(np.array(validos), axis=0)
        
        # 3. Optimizar y Analizar Tipo de Solución
        self.registrar_paso("EVALUACIÓN DE VÉRTICES EN LA FUNCIÓN OBJETIVO:")
        signo_y = '-' if self.c[1] < 0 else '+'
        abs_y = abs(self.c[1])
        self.registrar_paso(f"  Z = {self.c[0]}x {signo_y} {abs_y}y")
        
        resultados_vertices = []
        
        # Calculamos Z para todos primero
        for v in self.vertices:
            z = np.dot(self.c, v)
            signo_y = '-' if self.c[1] < 0 else '+'
            abs_c1 = abs(self.c[1])
            signo_calc = '-' if self.c[1]*v[1] < 0 else '+'
            abs_calc = abs(self.c[1]*v[1])
            calculo = f"{self.c[0]}·{v[0]:.2f} {signo_y} {abs_c1}·{v[1]:.2f} = {self.c[0]*v[0]:.2f} {signo_calc} {abs_calc} = {z:.2f}"
            self.registrar_paso(f"  Vértice ({v[0]:.2f}, {v[1]:.2f}):")
            self.registrar_paso(f"    Z = {calculo}")
            
            resultados_vertices.append({
                "punto": [float(v[0]), float(v[1])],
                "z": float(z)
            })

        # Encontrar el mejor Z
        valores_z = [r['z'] for r in resultados_vertices]
        mejor_z = max(valores_z) if self.objetivo == 'max' else min(valores_z)
        
        self.registrar_paso(f"  Valores de Z obtenidos: {[f'{z:.2f}' for z in valores_z]}")
        self.registrar_paso(f"  Objetivo: {self.objetivo.upper()}")
        self.registrar_paso(f"  Mejor Z: {mejor_z:.2f}")
        
        # Buscar cuántos puntos tienen ese mejor Z
        # Usamos np.isclose para comparar floats por si hay decimales (ej: 19.99999 vs 20)
        ganadores = [r for r in resultados_vertices if np.isclose(r['z'], mejor_z)]
        
        self.registrar_paso(f"  Vértices óptimos: {len(ganadores)}")
        for g in ganadores:
            self.registrar_paso(f"    → ({g['punto'][0]:.2f}, {g['punto'][1]:.2f}) con Z = {g['z']:.2f}")
        
        # --- DETERMINACIÓN DEL TIPO DE SOLUCIÓN ---
        tipo_solucion = ""
        explicacion = ""
        
        if len(ganadores) == 1:
            tipo_solucion = "Solución Única"
            explicacion = (f"Existe un único vértice ({ganadores[0]['punto'][0]}, {ganadores[0]['punto'][1]}) "
                           f"que maximiza/minimiza la función. Esto ocurre porque la pendiente de la función objetivo "
                           f"no es paralela a ninguna restricción activa.")
            punto_final = ganadores[0]['punto']
            
        elif len(ganadores) > 1:
            tipo_solucion = "Solución Múltiple (Infinitas Soluciones)"
            explicacion = (f"Se encontraron {len(ganadores)} vértices con el mismo valor óptimo Z={mejor_z:.2f}. "
                           f"Esto significa que la función objetivo es PARALELA a una de las restricciones. "
                           f"Cualquier punto en el segmento de recta que une estos vértices es una solución válida.")
            punto_final = ganadores[0]['punto'] # Devolvemos uno de referencia para graficar

        return {
            "status": "optimal",
            "tipo_solucion": tipo_solucion,
            "explicacion": explicacion,
            "z_optimo": float(mejor_z),
            "punto_optimo": punto_final, # Uno de los puntos para centrar la gráfica
            "vertices": [r['punto'] for r in resultados_vertices],
            "puntos_ganadores": [g['punto'] for g in ganadores], # Enviamos todos los ganadores
            "pasos": self.pasos
        }


class MetodoSimplex:
    def __init__(self, c, A, b, operadores, objetivo='max'):
        """
        c: Coeficientes de la función objetivo [c1, c2, ...]
        A: Matriz de coeficientes de las restricciones
        b: Vector de límites de restricciones
        operadores: Lista de operadores ['<=', '>=', '=']
        objetivo: 'max' o 'min'
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.operadores = operadores
        self.objetivo = objetivo
        self.pasos = []
        self.tablas = []  # Guardaremos cada tabla del Simplex
        
    def registrar_paso(self, mensaje):
        """Guarda un mensaje en la lista de pasos."""
        self.pasos.append(mensaje)
    
    def _convertir_a_nativo(self, valor):
        """Convierte valores de NumPy a tipos nativos de Python para serialización JSON."""
        if isinstance(valor, (np.integer, np.int64, np.int32)):
            return int(valor)
        elif isinstance(valor, (np.floating, np.float64, np.float32)):
            return float(valor)
        elif isinstance(valor, np.ndarray):
            return valor.tolist()
        elif isinstance(valor, list):
            return [self._convertir_a_nativo(v) for v in valor]
        elif isinstance(valor, dict):
            return {k: self._convertir_a_nativo(v) for k, v in valor.items()}
        elif valor == np.inf or valor == float('inf'):
            return float('inf')
        elif valor == -np.inf or valor == float('-inf'):
            return float('-inf')
        else:
            return valor
    
    def registrar_tabla(self, tabla, iteracion, variables_basicas=None, explicacion="", 
                       nombres_columnas=None, col_entrante=None, fila_saliente=None, 
                       elemento_pivote=None, ratios=None):
        """Guarda una tabla del Simplex para visualización."""
        # Convertir tabla a lista y luego a tipos nativos
        tabla_lista = tabla.tolist()
        tabla_nativa = self._convertir_a_nativo(tabla_lista)
        
        # Convertir ratios si existen
        ratios_nativo = None
        if ratios is not None:
            ratios_nativo = []
            for r in ratios:
                if r == np.inf or r == float('inf'):
                    ratios_nativo.append(float('inf'))
                elif r == -np.inf or r == float('-inf'):
                    ratios_nativo.append(float('-inf'))
                else:
                    ratios_nativo.append(self._convertir_a_nativo(r))
        
        self.tablas.append({
            "iteracion": int(iteracion),
            "tabla": tabla_nativa,
            "variables_basicas": variables_basicas if variables_basicas else [],
            "explicacion": explicacion,
            "nombres_columnas": nombres_columnas if nombres_columnas else [],
            "col_entrante": int(col_entrante) if col_entrante is not None else None,
            "fila_saliente": int(fila_saliente) if fila_saliente is not None else None,
            "elemento_pivote": self._convertir_a_nativo(elemento_pivote) if elemento_pivote is not None else None,
            "ratios": ratios_nativo if ratios_nativo is not None else []
        })
    
    def convertir_forma_estandar(self):
        """Convierte el problema a forma estándar."""
        self.registrar_paso("CONVERSIÓN A FORMA ESTÁNDAR:")
        self.registrar_paso(f"Problema original: {self.objetivo.upper()} Z = {' + '.join([f'{self.c[i]}x{i+1}' for i in range(len(self.c))])}")
        
        num_vars = len(self.c)
        num_rest = len(self.b)
        
        # Contar variables de holgura, exceso y artificiales necesarias
        num_holgura = sum(1 for op in self.operadores if op == '<=')
        num_exceso = sum(1 for op in self.operadores if op == '>=')
        num_artificiales = sum(1 for op in self.operadores if op in ['>=', '='])
        
        self.registrar_paso(f"Variables de holgura necesarias: {num_holgura}")
        self.registrar_paso(f"Variables de exceso necesarias: {num_exceso}")
        self.registrar_paso(f"Variables artificiales necesarias: {num_artificiales}")
        
        # Construir matriz extendida
        A_estandar = np.zeros((num_rest, num_vars + num_holgura + num_exceso + num_artificiales))
        col_actual = num_vars
        
        # Variables de holgura y exceso
        idx_holgura = 0
        idx_exceso = 0
        idx_artificial = 0
        
        for i in range(num_rest):
            # Copiar coeficientes originales
            # Validar que cada restricción tenga el número correcto de variables
            if len(self.A[i]) != num_vars:
                raise ValueError(
                    f"La restricción {i+1} tiene {len(self.A[i])} variables, "
                    f"pero la función objetivo tiene {num_vars} variables. "
                    f"Todas las restricciones deben tener el mismo número de variables que el objetivo."
                )
            A_estandar[i, :num_vars] = self.A[i]
            
            if self.operadores[i] == '<=':
                A_estandar[i, col_actual] = 1  # Variable de holgura
                self.registrar_paso(f"R{i+1}: Agregada variable de holgura s{idx_holgura+1}")
                col_actual += 1
                idx_holgura += 1
            elif self.operadores[i] == '>=':
                A_estandar[i, col_actual] = -1  # Variable de exceso
                self.registrar_paso(f"R{i+1}: Agregada variable de exceso e{idx_exceso+1}")
                col_actual += 1
                idx_exceso += 1
                # También agregar variable artificial
                A_estandar[i, col_actual] = 1
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                col_actual += 1
                idx_artificial += 1
            elif self.operadores[i] == '=':
                A_estandar[i, col_actual] = 1  # Variable artificial
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                col_actual += 1
                idx_artificial += 1
        
        # Función objetivo extendida
        # Trabajamos directamente con la función objetivo (sin negar)
        # La lógica de optimalidad se ajusta según max/min
        c_estandar = np.zeros(num_vars + num_holgura + num_exceso + num_artificiales)
        c_estandar[:num_vars] = np.array(self.c)
        
        # Si hay variables artificiales, usar método de dos fases o Big M
        # Por simplicidad, usaremos Big M con M grande
        M = 10000
        if num_artificiales > 0:
            # Coeficientes para variables artificiales en la función objetivo
            idx_art = num_vars + num_holgura + num_exceso
            for i in range(num_artificiales):
                c_estandar[idx_art + i] = M
        
        return A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales
    
    def resolver(self):
        """Resuelve el problema usando el método Simplex."""
        self.registrar_paso(f"=== MÉTODO SIMPLEX ===")
        # Formatear función objetivo con operadores correctos
        objetivo_str = f"{self.c[0]}x₁"
        for i in range(1, len(self.c)):
            signo = '-' if self.c[i] < 0 else '+'
            abs_val = abs(self.c[i])
            objetivo_str += f" {signo} {abs_val}x{i+1}"
        self.registrar_paso(f"FUNCIÓN OBJETIVO: {self.objetivo.upper()} Z = {objetivo_str}")
        
        self.registrar_paso("RESTRICCIONES:")
        for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
            # Formatear restricción con operadores correctos
            restriccion_str = f"{a_row[0]}x₁"
            for i in range(1, len(a_row)):
                signo = '-' if a_row[i] < 0 else '+'
                abs_val = abs(a_row[i])
                restriccion_str += f" {signo} {abs_val}x{i+1}"
            self.registrar_paso(f"  R{idx}: {restriccion_str} {op} {b_val}")
        
        # Convertir a forma estándar
        A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales = self.convertir_forma_estandar()
        
        num_rest = len(self.b)
        num_cols_totales = A_estandar.shape[1]
        
        # Identificar variables básicas iniciales
        variables_basicas = []
        indices_basicas = []
        
        # Variables básicas iniciales: holguras y artificiales
        col_actual = num_vars
        for i in range(num_rest):
            if self.operadores[i] == '<=':
                variables_basicas.append(f"s{len([v for v in variables_basicas if v.startswith('s')]) + 1}")
                indices_basicas.append(col_actual)
                col_actual += 1
            elif self.operadores[i] == '>=':
                variables_basicas.append(f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}")
                indices_basicas.append(col_actual + 1)  # La artificial está después del exceso
                col_actual += 2
            elif self.operadores[i] == '=':
                variables_basicas.append(f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}")
                indices_basicas.append(col_actual)
                col_actual += 1
        
        # Crear tabla inicial
        # Reordenamos para que Z esté primero: [Z, R1, R2, ...]
        tabla = np.zeros((num_rest + 1, num_cols_totales + 1))
        
        # Primero ponemos las restricciones (filas 1 a num_rest)
        tabla[1:, :num_cols_totales] = A_estandar
        tabla[1:, -1] = self.b
        
        # Luego la fila Z (fila 0)
        # En el Simplex estándar, trabajamos con Z - c₁x₁ - c₂x₂ - ... = 0
        # Por lo tanto, la fila Z muestra los coeficientes negativos: -c_j
        # Para maximización: cuando todos los coeficientes son ≤ 0, es óptimo
        # Para minimización: cuando todos los coeficientes son ≥ 0, es óptimo
        tabla[0, :num_cols_totales] = -c_estandar
        
        # Calcular Z inicial: Z = sum(c_basica * b)
        # Para variables básicas iniciales (holguras), c_basica = 0
        # Para artificiales, c_basica = M (grande)
        z_val = 0
        for i, idx_basica in enumerate(indices_basicas):
            z_val += c_estandar[idx_basica] * self.b[i]
        tabla[0, -1] = z_val
        
        # Actualizar fila Z para que los coeficientes de variables básicas sean 0
        # Esto convierte la fila Z a coeficientes reducidos
        # Nota: las restricciones están en las filas 1 a num_rest, no en 0 a num_rest-1
        for i, idx_basica in enumerate(indices_basicas):
            if abs(tabla[0, idx_basica]) > 1e-9:
                factor = tabla[0, idx_basica]
                tabla[0, :] -= factor * tabla[i + 1, :]  # i+1 porque las restricciones empiezan en fila 1
        
        # Generar nombres de columnas
        nombres_columnas = []
        for i in range(num_vars):
            nombres_columnas.append(f"x{i+1}")
        for i in range(num_holgura):
            nombres_columnas.append(f"s{i+1}")
        for i in range(num_exceso):
            nombres_columnas.append(f"e{i+1}")
        for i in range(num_artificiales):
            nombres_columnas.append(f"a{i+1}")
        
        self.registrar_paso("\nTABLA INICIAL:")
        self.registrar_tabla(tabla, 0, variables_basicas, "Tabla inicial del Simplex", 
                           nombres_columnas=nombres_columnas)
        
        iteracion = 0
        max_iteraciones = 100
        
        while iteracion < max_iteraciones:
            iteracion += 1
            self.registrar_paso(f"\n--- ITERACIÓN {iteracion} ---")
            
            # Verificar optimalidad
            # La fila Z está en el índice 0 (primera fila)
            fila_z = tabla[0, :num_cols_totales]
            
            # En el Simplex estándar con Z - c₁x₁ - c₂x₂ = 0:
            # Para maximización: buscamos valores negativos (los más negativos mejoran más)
            # Cuando todos son ≥ 0, es óptimo (todos los coeficientes de Z son ≤ 0)
            # Para minimización: buscamos valores positivos (los más positivos reducen más)
            # Cuando todos son ≤ 0, es óptimo (todos los coeficientes de Z son ≥ 0)
            if self.objetivo == 'max':
                # Buscamos el más negativo (el que más mejora Z)
                indices_negativos = np.where(fila_z < -1e-9)[0]
                if len(indices_negativos) == 0:
                    self.registrar_paso("✓ Condición de optimalidad alcanzada (todos los coeficientes ≥ 0)")
                    break
                col_entrante = int(indices_negativos[np.argmin(fila_z[indices_negativos])])
            else:  # min
                # Buscamos el más positivo (el que más reduce Z)
                indices_positivos = np.where(fila_z > 1e-9)[0]
                if len(indices_positivos) == 0:
                    self.registrar_paso("✓ Condición de optimalidad alcanzada (todos los coeficientes ≤ 0)")
                    break
                col_entrante = int(indices_positivos[np.argmax(fila_z[indices_positivos])])
            
            # Identificar nombre de variable entrante
            if col_entrante < num_vars:
                var_entrante_nombre = f"x{col_entrante + 1}"
            elif col_entrante < num_vars + num_holgura:
                var_entrante_nombre = f"s{col_entrante - num_vars + 1}"
            elif col_entrante < num_vars + num_holgura + num_exceso:
                var_entrante_nombre = f"e{col_entrante - num_vars - num_holgura + 1}"
            else:
                var_entrante_nombre = f"a{col_entrante - num_vars - num_holgura - num_exceso + 1}"
            
            self.registrar_paso(f"\n📌 VARIABLE ENTRANTE: {var_entrante_nombre}")
            self.registrar_paso(f"   Razón: El coeficiente en la fila Z es {fila_z[col_entrante]:.4f}, que es {'negativo' if fila_z[col_entrante] < 0 else 'positivo'}.")
            if self.objetivo == 'max':
                self.registrar_paso(f"   En maximización, valores negativos en la fila Z indican que aumentar {var_entrante_nombre} mejorará el valor de Z.")
            else:
                self.registrar_paso(f"   En minimización, valores positivos en la fila Z indican que aumentar {var_entrante_nombre} reducirá el valor de Z.")
            
            # Calcular ratios para determinar variable saliente
            # Las restricciones están en las filas 1 a num_rest (no 0, que es Z)
            self.registrar_paso(f"\n📊 CÁLCULO DE RATIOS (para determinar variable saliente):")
            self.registrar_paso(f"   Ratio = Valor en columna 'Solución' ÷ Valor en columna '{var_entrante_nombre}'")
            self.registrar_paso(f"   Solo se calculan ratios para filas donde el coeficiente de {var_entrante_nombre} es positivo.")
            
            ratios = []
            for i in range(num_rest):
                fila_rest = i + 1  # Las restricciones empiezan en fila 1
                var_basica_actual = variables_basicas[i] if i < len(variables_basicas) else f"Fila {i+1}"
                if tabla[fila_rest, col_entrante] > 1e-9:
                    ratio = float(tabla[fila_rest, -1] / tabla[fila_rest, col_entrante])
                    ratios.append(ratio)
                    self.registrar_paso(f"   {var_basica_actual}: {tabla[fila_rest, -1]:.4f} ÷ {tabla[fila_rest, col_entrante]:.4f} = {ratio:.4f}")
                else:
                    ratios.append(float('inf'))
                    self.registrar_paso(f"   {var_basica_actual}: No se calcula (coeficiente ≤ 0 o muy pequeño)")
            
            if all(r == float('inf') for r in ratios):
                self.registrar_paso("\n⚠ Problema no acotado: No se puede encontrar variable saliente")
                self.registrar_paso("   Razón: Todas las filas tienen coeficientes no positivos en la columna entrante.")
                self.registrar_paso("   Esto significa que {var_entrante_nombre} puede crecer indefinidamente sin violar restricciones.")
                # Serializar tablas antes de retornar
                tablas_serializadas = []
                for tabla_info in self.tablas:
                    tablas_serializadas.append({
                        "iteracion": int(tabla_info["iteracion"]),
                        "tabla": self._convertir_a_nativo(tabla_info["tabla"]),
                        "variables_basicas": tabla_info["variables_basicas"],
                        "explicacion": tabla_info["explicacion"],
                        "nombres_columnas": tabla_info.get("nombres_columnas", []),
                        "col_entrante": tabla_info.get("col_entrante"),
                        "fila_saliente": tabla_info.get("fila_saliente"),
                        "elemento_pivote": self._convertir_a_nativo(tabla_info.get("elemento_pivote")) if tabla_info.get("elemento_pivote") is not None else None,
                        "ratios": self._convertir_a_nativo(tabla_info.get("ratios", []))
                    })
                return {
                    "status": "unbounded",
                    "tipo_solucion": "Problema No Acotado",
                    "explicacion": "El problema no tiene solución óptima finita. La región factible es no acotada en la dirección de mejora de la función objetivo, lo que significa que Z puede crecer (maximización) o decrecer (minimización) indefinidamente.",
                    "pasos": self.pasos,
                    "tablas": tablas_serializadas
                }
            
            fila_saliente = int(np.argmin(ratios))
            ratio_minimo = ratios[fila_saliente]
            ratio_minimo_float = float(ratio_minimo) if ratio_minimo != np.inf else float('inf')
            var_saliente_actual = variables_basicas[fila_saliente] if fila_saliente < len(variables_basicas) else f"Fila {fila_saliente + 1}"
            
            self.registrar_paso(f"\n📌 VARIABLE SALIENTE: {var_saliente_actual}")
            self.registrar_paso(f"   Razón: Tiene el ratio mínimo ({ratio_minimo_float:.4f}).")
            self.registrar_paso(f"   El ratio mínimo asegura que al hacer {var_entrante_nombre} = {ratio_minimo_float:.4f}, la variable {var_saliente_actual} se vuelve cero (sale de la base).")
            
            # Guardar valor anterior de Z antes del pivoteo
            z_val_anterior = float(tabla[0, -1])
            
            # Actualizar variable básica (usar var_entrante_nombre que ya está definido)
            variables_basicas[fila_saliente] = var_entrante_nombre
            indices_basicas[fila_saliente] = col_entrante
            
            # Pivoteo
            # La fila saliente está en índice fila_saliente + 1 (porque Z está en 0)
            fila_pivote = fila_saliente + 1
            elemento_pivote = float(tabla[fila_pivote, col_entrante])
            
            self.registrar_paso(f"\n🔄 OPERACIONES DE PIVOTEO:")
            self.registrar_paso(f"   Elemento Pivote: {elemento_pivote:.4f} (intersección de fila {var_saliente_actual} y columna {var_entrante_nombre})")
            self.registrar_paso(f"   Paso 1: Normalizar la fila pivote (dividir toda la fila por {elemento_pivote:.4f})")
            self.registrar_paso(f"           Esto hace que el elemento pivote sea 1 y {var_entrante_nombre} entre a la base con coeficiente 1.")
            
            # Normalizar fila pivote
            tabla[fila_pivote, :] /= elemento_pivote
            
            self.registrar_paso(f"   Paso 2: Eliminación gaussiana (hacer cero la columna {var_entrante_nombre} en todas las demás filas)")
            self.registrar_paso(f"           Para cada fila i ≠ fila pivote: Fila[i] = Fila[i] - (coeficiente en columna {var_entrante_nombre}) × Fila[pivote]")
            
            # Eliminación gaussiana
            # Actualizar todas las filas (Z en 0, restricciones en 1 a num_rest)
            for i in range(num_rest + 1):
                if i != fila_pivote:
                    factor = tabla[i, col_entrante]
                    if abs(factor) > 1e-9:
                        nombre_fila = 'Z' if i == 0 else (variables_basicas[i-1] if i-1 < len(variables_basicas) else f"Fila {i}")
                        self.registrar_paso(f"           - Fila {nombre_fila}: Restamos {factor:.4f} × Fila[{var_saliente_actual}]")
                    tabla[i, :] -= factor * tabla[fila_pivote, :]
            
            # Actualizar Z
            z_val = tabla[0, -1]  # Z está en la fila 0
            self.registrar_paso(f"\n✅ RESULTADO DE LA ITERACIÓN:")
            self.registrar_paso(f"   Valor anterior de Z: {z_val_anterior:.4f}")
            self.registrar_paso(f"   Nuevo valor de Z: {z_val:.4f}")
            if ratio_minimo != float('inf'):
                mejora = z_val - z_val_anterior
                self.registrar_paso(f"   Mejora en Z: {mejora:+.4f} ({'aumento' if mejora > 0 else 'disminución' if mejora < 0 else 'sin cambio'})")
            self.registrar_paso(f"   Nueva base: {', '.join(variables_basicas)}")
            self.registrar_paso(f"   {var_entrante_nombre} ahora es básica (valor = {ratio_minimo_float:.4f}), {var_saliente_actual} sale de la base (valor = 0)")
            
            # Generar nombres de columnas (mismo que antes)
            nombres_columnas = []
            for i in range(num_vars):
                nombres_columnas.append(f"x{i+1}")
            for i in range(num_holgura):
                nombres_columnas.append(f"s{i+1}")
            for i in range(num_exceso):
                nombres_columnas.append(f"e{i+1}")
            for i in range(num_artificiales):
                nombres_columnas.append(f"a{i+1}")
            
            var_saliente_anterior = var_saliente_actual
            
            self.registrar_tabla(tabla.copy(), iteracion, variables_basicas.copy(), 
                               f"Iteración {iteracion}: {var_entrante_nombre} entra, {var_saliente_anterior} sale",
                               nombres_columnas=nombres_columnas,
                               col_entrante=col_entrante,
                               fila_saliente=fila_saliente,
                               elemento_pivote=elemento_pivote,
                               ratios=ratios)
        
        # Extraer solución
        # Las restricciones están en las filas 1 a num_rest (Z está en fila 0)
        solucion = np.zeros(num_vars)
        for i, idx_basica in enumerate(indices_basicas):
            if idx_basica < num_vars:
                fila_rest = i + 1  # Las restricciones empiezan en fila 1
                solucion[idx_basica] = tabla[fila_rest, -1]
        
        # Calcular z_optimo
        # Z está en la fila 0 (primera fila)
        z_optimo = float(tabla[0, -1])
        
        self.registrar_paso(f"\n=== SOLUCIÓN ÓPTIMA ===")
        self.registrar_paso(f"Valor óptimo de Z: {z_optimo:.4f}")
        for i in range(num_vars):
            self.registrar_paso(f"x{i+1} = {solucion[i]:.4f}")
        
        # Verificar si hay variables artificiales en la base (problema no factible)
        if num_artificiales > 0:
            idx_art_inicio = num_vars + num_holgura + num_exceso
            for i, idx_basica in enumerate(indices_basicas):
                if idx_basica >= idx_art_inicio:
                    fila_rest = i + 1  # Las restricciones empiezan en fila 1
                    if abs(tabla[fila_rest, -1]) > 1e-6:
                        # Serializar tablas antes de retornar
                        tablas_serializadas = []
                        for tabla_info in self.tablas:
                            tablas_serializadas.append({
                                "iteracion": int(tabla_info["iteracion"]),
                                "tabla": self._convertir_a_nativo(tabla_info["tabla"]),
                                "variables_basicas": tabla_info["variables_basicas"],
                                "explicacion": tabla_info["explicacion"],
                                "nombres_columnas": tabla_info.get("nombres_columnas", []),
                                "col_entrante": tabla_info.get("col_entrante"),
                                "fila_saliente": tabla_info.get("fila_saliente"),
                                "elemento_pivote": self._convertir_a_nativo(tabla_info.get("elemento_pivote")) if tabla_info.get("elemento_pivote") is not None else None,
                                "ratios": self._convertir_a_nativo(tabla_info.get("ratios", []))
                            })
                        return {
                            "status": "infeasible",
                            "tipo_solucion": "Problema No Factible",
                            "explicacion": "Una variable artificial permanece en la base con valor distinto de cero. Esto indica que las restricciones son contradictorias y no existe una solución factible que satisfaga todas las restricciones simultáneamente.",
                            "pasos": self.pasos,
                            "tablas": tablas_serializadas
                        }
        
        # Analizar tipo de solución
        fila_z_final = tabla[0, :num_cols_totales]
        
        # Contar variables no básicas con coeficiente cero en la fila Z
        # Si hay variables no básicas con coeficiente cero, pueden entrar sin cambiar Z (solución múltiple)
        vars_no_basicas_cero = 0
        for j in range(num_cols_totales):
            if j not in indices_basicas:  # Variable no básica
                if abs(fila_z_final[j]) < 1e-9:  # Coeficiente aproximadamente cero
                    vars_no_basicas_cero += 1
        
        # Determinar tipo de solución y explicación
        if vars_no_basicas_cero > 0:
            tipo_solucion = "Solución Múltiple (Infinitas Soluciones)"
            explicacion = (f"Se encontró una solución óptima, pero existen {vars_no_basicas_cero} variable(s) no básica(s) "
                         f"con coeficiente cero en la fila Z. Esto significa que estas variables pueden entrar a la base "
                         f"sin cambiar el valor de Z, generando infinitas soluciones óptimas a lo largo de un borde de la "
                         f"región factible.")
        else:
            tipo_solucion = "Solución Única"
            explicacion = (f"Se encontró una solución óptima única. Todos los coeficientes en la fila Z son del signo "
                         f"correcto (≥ 0 para maximización, ≤ 0 para minimización) y no hay variables no básicas con "
                         f"coeficiente cero. Esto significa que cualquier cambio en las variables no básicas empeoraría "
                         f"el valor de Z, confirmando que esta es la única solución óptima.")
        
        # Convertir solución a lista de floats nativos
        solucion_lista = [float(solucion[i]) for i in range(num_vars)]
        
        # Asegurar que las tablas estén completamente convertidas a tipos nativos
        tablas_serializadas = []
        for tabla_info in self.tablas:
            tablas_serializadas.append({
                "iteracion": int(tabla_info["iteracion"]),
                "tabla": self._convertir_a_nativo(tabla_info["tabla"]),
                "variables_basicas": tabla_info["variables_basicas"],
                "explicacion": tabla_info["explicacion"],
                "nombres_columnas": tabla_info.get("nombres_columnas", []),
                "col_entrante": tabla_info.get("col_entrante"),
                "fila_saliente": tabla_info.get("fila_saliente"),
                "elemento_pivote": self._convertir_a_nativo(tabla_info.get("elemento_pivote")) if tabla_info.get("elemento_pivote") is not None else None,
                "ratios": self._convertir_a_nativo(tabla_info.get("ratios", []))
            })
        
        return {
            "status": "optimal",
            "tipo_solucion": tipo_solucion,
            "explicacion": explicacion,
            "z_optimo": float(z_optimo),
            "solucion": solucion_lista,
            "iteraciones": int(iteracion),
            "pasos": self.pasos,
            "tablas": tablas_serializadas,
            "variables_basicas": variables_basicas
        }

#------ ZONA DE PRUEBA -------
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
    
    # Test case 1: Problema original
    if len(sys.argv) == 1 or sys.argv[1] == "1":
        print("="*50)
        print("TEST CASE 1: Problema Original")
        print("="*50)
        
        #1. Configurar datos:
        c = [3, 2] #Z = 3x + 2y

        #Restricciones: (Lado izquierdo de la desigualdad)
        A = [
            [2, 1], #2x + 1y
            [1, 1], #1x + 1y
            [0, 1], #0x + 1y
        ]

        b = [10, 8, 8] #10, 8, 8
        operadores = ['<=', '<=', '<=']

        #2. Crear el Objetivo:
        problema = MetodoGrafico(c, A, b, operadores, objetivo= 'max')
        problema.mostrar_datos()

        #3. Resolver: 
        resultado = problema.resolver()

        print ("\n" + "="*30)
        print (f"SOLUCION ÓPTIMA:")
        if resultado.get('status') == 'optimal':
            print (f"Punto óptimo: {resultado.get('punto_optimo')}")
            print (f"Valor Optimo de Z: {resultado.get('z_optimo')}")
            print (f"Tipo de solución: {resultado.get('tipo_solucion')}")
    
    # Test case 2: Restricciones con relaciones entre variables (y >= x, y <= 2x, etc.)
    elif sys.argv[1] == "2":
        print("="*50)
        print("TEST CASE 2: Restricciones con relaciones entre variables")
        print("Restricciones: y >= x, y <= 2x, x <= 30, y <= 20")
        print("="*50)
        
        # Función objetivo: Maximizar o minimizar (ejemplo)
        c = [1, 1]  # Z = x + y (puedes cambiarlo)
        
        # Restricciones convertidas a forma estándar:
        # y >= x  →  -x + y >= 0  →  A = [-1, 1], b = 0, op = '>='
        # y <= 2x →  -2x + y <= 0  →  A = [-2, 1], b = 0, op = '<='
        # x <= 30 →  A = [1, 0], b = 30, op = '<='
        # y <= 20 →  A = [0, 1], b = 20, op = '<='
        
        A = [
            [-1, 1],   # -x + y >= 0  (equivalente a y >= x)
            [-2, 1],   # -2x + y <= 0  (equivalente a y <= 2x)
            [1, 0],    # x <= 30
            [0, 1],    # y <= 20
        ]
        
        b = [0, 0, 30, 20]
        operadores = ['>=', '<=', '<=', '<=']
        
        # Crear y resolver el problema
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
            print(f"\nVértices factibles: {len(resultado.get('vertices', []))}")
            for v in resultado.get('vertices', []):
                print(f"  - ({v[0]:.2f}, {v[1]:.2f})")
        elif resultado.get('status') == 'infeasible':
            print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
            print(f"Explicación: {resultado.get('explicacion')}")
        
        # Mostrar pasos detallados
        print("\n" + "="*50)
        print("PASOS DETALLADOS:")
        print("="*50)
        for paso in resultado.get('pasos', []):
            print(paso)
    
    # Test case 3: Usando la función helper para convertir restricciones relacionales
    elif sys.argv[1] == "3":
        print("="*50)
        print("TEST CASE 3: Usando función helper convertir_restricciones_relacionales()")
        print("Restricciones en forma natural: y >= x, y <= 2x, x <= 30, y <= 20")
        print("="*50)
        
        # Función objetivo
        c = [1, 1]  # Z = x + y
        
        # Restricciones en forma natural (como las escribes)
        restricciones_str = [
            "y >= x",
            "y <= 2x",
            "x <= 30",
            "y <= 20"
        ]
        
        print("\nRestricciones originales (forma natural):")
        for r in restricciones_str:
            print(f"  - {r}")
        
        # Convertir a forma estándar usando la función helper
        print("\nConvirtiendo a forma estándar...")
        A, b, operadores = convertir_restricciones_relacionales(restricciones_str)
        
        print("\nRestricciones convertidas (forma estándar):")
        for i, (a_row, b_val, op) in enumerate(zip(A, b, operadores), 1):
            signo_y = '-' if a_row[1] < 0 else '+'
            abs_y = abs(a_row[1])
            print(f"  R{i}: {a_row[0]}x {signo_y} {abs_y}y {op} {b_val}")
        
        # Crear y resolver el problema
        problema = MetodoGrafico(c, A, b, operadores, objetivo='max')
        resultado = problema.resolver()
        
        print("\n" + "="*30)
        print("RESULTADO:")
        if resultado.get('status') == 'optimal':
            print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
            print(f"Punto óptimo: {resultado.get('punto_optimo')}")
            print(f"Valor óptimo de Z: {resultado.get('z_optimo')}")
            print(f"\nVértices factibles: {len(resultado.get('vertices', []))}")
            for v in resultado.get('vertices', []):
                print(f"  - ({v[0]:.2f}, {v[1]:.2f})")
        elif resultado.get('status') == 'infeasible':
            print(f"Tipo de solución: {resultado.get('tipo_solucion')}")
            print(f"Explicación: {resultado.get('explicacion')}")




