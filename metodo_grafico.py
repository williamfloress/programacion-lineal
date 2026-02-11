"""
Método Gráfico para Programación Lineal.

Solo sirve cuando tenemos exactamente 2 variables (x e y). La idea es dibujar
las restricciones en el plano, ver dónde se cortan, quedarnos con los puntos
que cumplen todo y en esos vértices evaluar Z para ver cuál da el mejor valor.

PASOS DEL ALGORITMO (resumen):
  1. Calcular todos los puntos donde se cortan las rectas (restricciones + ejes).
  2. De esos puntos, quedarse solo con los que cumplen todas las restricciones (factibles).
  3. En cada vértice factible evaluar Z; el que da mejor Z (max o min) es la solución.
"""

import numpy as np


class MetodoGrafico:
    def __init__(self, c, A, b, operadores, objetivo='max'):
        """Guarda el problema: coeficientes de Z (c), restricciones (A, b, operadores), y si es max o min."""
        self.c = np.array(c)
        self.A = np.array(A)
        self.b = np.array(b)
        self.objetivo = objetivo
        self.operadores = operadores
        # Aquí irán los vértices de la región factible que encontremos
        self.vertice = []
        # Lista donde voy guardando cada paso del proceso para mostrarlo después (log)
        self.pasos = []
    
    def registrar_paso(self, mensaje):
        """Simplemente añado un mensaje al log de pasos para que el usuario vea qué hice."""
        self.pasos.append(mensaje)


    def mostrar_datos(self):
        """Imprimo en consola el problema (objetivo y restricciones); útil para depurar."""
        print(f"Objetivo: {self.objetivo} Z= {self.c[0]}x + {self.c[1]}y")
        print("Restricciones:")
        for i in range(len(self.b)):
            print(f"{self.A[i][0]}x + {self.A[i][1]}y <= {self.b[i]}")

    def encontrar_intersecciones(self):
        """Calcula todos los puntos donde se cortan las rectas (restricciones + ejes x=0, y=0)."""
        posibles_puntos = []

        # Incluir ejes x=0 e y=0 como “rectas” más para obtener cortes con los ejes
        matriz_total_A = np.vstack([self.A, [[1, 0], [0, 1]]])
        vector_total_b = np.concatenate([self.b, [0, 0]])
        num_lineas = len(vector_total_b)

        # Por cada par de rectas: resolver sistema 2x2 → (x,y) del corte
        for i in range(num_lineas):
            for j in range(i + 1, num_lineas):
                a_sistema = np.array([matriz_total_A[i], matriz_total_A[j]])
                b_sistema = np.array([vector_total_b[i], vector_total_b[j]])
                try:
                    punto = np.linalg.solve(a_sistema, b_sistema)
                    posibles_puntos.append(punto)
                except np.linalg.LinAlgError:
                    continue  # rectas paralelas, no hay corte único

        return posibles_puntos

    def es_factible(self, punto):
        """Indica si el punto cumple x≥0, y≥0 y todas las restricciones (<=, >=, =)."""
        x, y = punto
        if x < -1e-9 or y < -1e-9:
            return False
        for i in range(len(self.b)):
            valor = np.dot(self.A[i], punto)
            limite = self.b[i]
            op = self.operadores[i]
            if op == '<=' and valor > limite + 1e-9:
                return False
            if op == '>=' and valor < limite - 1e-9:
                return False
            if op == '=' and not np.isclose(valor, limite):
                return False
        return True

    def obtener_vertices_validos(self):
        """De todos los cortes entre rectas, deja solo los que son factibles y quita duplicados."""
        todos_puntos = self.encontrar_intersecciones()
        validos = [p for p in todos_puntos if self.es_factible(p)]
        self.vertice = np.unique(np.array(validos), axis=0)
        return self.vertice

    def resolver(self):
        """
        Ejecuta el método gráfico completo:
        1. Registra objetivo y restricciones en el log.
        2. Calcula intersecciones entre todas las rectas (restricciones + ejes).
        3. Filtra los puntos factibles (cumplen todo).
        4. Evalúa Z en cada vértice; el mejor (max o min) es la solución.
        """
        # Log: función objetivo
        signo_y = '-' if self.c[1] < 0 else '+'
        abs_y = abs(self.c[1])
        self.registrar_paso(f"FUNCIÓN OBJETIVO: {self.objetivo.upper()} Z = {self.c[0]}x {signo_y} {abs_y}y")

        self.registrar_paso("RESTRICCIONES:")
        for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
            signo_y = '-' if a_row[1] < 0 else '+'
            abs_y = abs(a_row[1])
            self.registrar_paso(f"  R{idx}: {a_row[0]}x {signo_y} {abs_y}y {op} {b_val}")
        
        # Paso 1: intersecciones entre rectas (restricciones + ejes)
        puntos_corte = []
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

        # Paso 2: de esos puntos, cuáles cumplen todas las restricciones (factibles)
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
            # Si ningún punto de corte es factible, las restricciones no tienen región común
            self.registrar_paso("RESULTADO: No existe ningún punto que cumpla todas las restricciones.")
            return {
                "status": "infeasible",
                "tipo_solucion": "No Factible",
                "explicacion": "Las restricciones son contradictorias. No existe una región común entre ellas.",
                "pasos": self.pasos
            }

        # Quito vértices repetidos (a veces dos intersecciones dan casi el mismo punto por float)
        vertices_array = np.array(validos)
        vertices_unicos = []
        tolerancia = 1e-9

        for vertice in vertices_array:
            es_duplicado = False
            for v_unico in vertices_unicos:
                if np.allclose(vertice, v_unico, atol=tolerancia):
                    es_duplicado = True
                    break
            if not es_duplicado:
                vertices_unicos.append(vertice)
        
        self.vertices = np.array(vertices_unicos)

        # Paso 3: evaluar Z en cada vértice; el mejor (max o min) es el óptimo
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

        # El óptimo es el mayor Z si maximizamos, o el menor si minimizamos
        valores_z = [r['z'] for r in resultados_vertices]
        mejor_z = max(valores_z) if self.objetivo == 'max' else min(valores_z)

        self.registrar_paso(f"  Valores de Z obtenidos: {[f'{z:.2f}' for z in valores_z]}")
        self.registrar_paso(f"  Objetivo: {self.objetivo.upper()}")
        self.registrar_paso(f"  Mejor Z: {mejor_z:.2f}")

        # Puede haber varios vértices con el mismo Z óptimo (solución múltiple); los identifico con tolerancia
        ganadores = [r for r in resultados_vertices if np.isclose(r['z'], mejor_z)]

        self.registrar_paso(f"  Vértices óptimos: {len(ganadores)}")
        for g in ganadores:
            self.registrar_paso(f"    → ({g['punto'][0]:.2f}, {g['punto'][1]:.2f}) con Z = {g['z']:.2f}")

        # Decido si es solución única, múltiple, etc. para el mensaje final
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
