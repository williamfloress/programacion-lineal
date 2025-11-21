import numpy as np

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
        self.registrar_paso(f"FUNCIÓN OBJETIVO: {self.objetivo.upper()} Z = {self.c[0]}x + {self.c[1]}y")
        
        # Mostrar restricciones
        self.registrar_paso("RESTRICCIONES:")
        for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
            self.registrar_paso(f"  R{idx}: {a_row[0]}x + {a_row[1]}y {op} {b_val}")
        
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
                    
                    # Mostrar el cálculo de la intersección
                    eq1 = f"{matriz_total[i][0]}x + {matriz_total[i][1]}y = {vector_total[i]}"
                    eq2 = f"{matriz_total[j][0]}x + {matriz_total[j][1]}y = {vector_total[j]}"
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
                self.registrar_paso(f"    {simbolo} R{idx}: {a_row[0]}·{p[0]:.2f} + {a_row[1]}·{p[1]:.2f} = {valor:.2f} {op} {b_val}")
                
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
        self.registrar_paso(f"  Z = {self.c[0]}x + {self.c[1]}y")
        
        resultados_vertices = []
        
        # Calculamos Z para todos primero
        for v in self.vertices:
            z = np.dot(self.c, v)
            calculo = f"{self.c[0]}·{v[0]:.2f} + {self.c[1]}·{v[1]:.2f} = {self.c[0]*v[0]:.2f} + {self.c[1]*v[1]:.2f} = {z:.2f}"
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
#------ ZONA DE PRUEBA -------

if __name__ == "__main__":

    #1. Configurar datos:
    c = [3, 2] #Z = 3x + 2y

    #Restricciones: (Lado izquierdo de la desigualdad)
    A = [
        [2, 1], #2x + 1y
        [1, 1], #1x + 1y
        [0, 1], #0x + 1y
    ]

    b = [10, 8, 8] #10, 8, 8

    #2. Crear el Objetivo:
    problema = MetodoGrafico(c, A, b, objetivo= 'max')
    problema.mostrar_datos()

    #3. Resolver: 

    resultado = problema.resolver()

    print ("\n" + "="*30)
    print (f"SOLUCION ÓPTIMA:")
    print (f"Punto x,y: {resultado[0]}")
    print (f"Valor Optimo de Z: {resultado[1]}")




