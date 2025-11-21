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
        self.registrar_paso(f"1. Iniciando análisis para {self.objetivo.upper()} Z = {self.c[0]}x + {self.c[1]}y")
        
        # 1. Intersecciones
        puntos_corte = []
        matriz_total = np.vstack([self.A, [[1, 0], [0, 1]]])
        vector_total = np.concatenate([self.b, [0, 0]])
        
        self.registrar_paso("2. Calculando intersecciones de rectas y ejes...")
        
        num_lineas = len(vector_total)
        for i in range(num_lineas):
            for j in range(i + 1, num_lineas):
                try:
                    A_temp = np.array([matriz_total[i], matriz_total[j]])
                    b_temp = np.array([vector_total[i], vector_total[j]])
                    punto = np.linalg.solve(A_temp, b_temp)
                    puntos_corte.append(punto)
                except np.linalg.LinAlgError:
                    continue

        # 2. Filtrar
        self.registrar_paso(f"3. Se encontraron {len(puntos_corte)} intersecciones brutas. Filtrando factibles...")
        validos = []
        for p in puntos_corte:
            if self.es_factible(p):
                validos.append(p)
                self.registrar_paso(f"   -> Punto válido encontrado: ({p[0]:.2f}, {p[1]:.2f})")
        
        self.vertices = np.unique(np.array(validos), axis=0)
        
        if len(self.vertices) == 0:
            self.registrar_paso("Error: No hay región factible.")
            return {"status": "infeasible", "pasos": self.pasos}

        # 3. Optimizar
        self.registrar_paso("4. Evaluando vértices en la Función Objetivo:")
        mejor_z = -np.inf if self.objetivo == 'max' else np.inf
        mejor_punto = None
        
        vertices_para_json = [] # Necesitamos convertir numpy a lista normal para JSON

        for v in self.vertices:
            z = np.dot(self.c, v)
            self.registrar_paso(f"   -> En ({v[0]:.2f}, {v[1]:.2f}) Z vale: {z:.2f}")
            vertices_para_json.append([float(v[0]), float(v[1])]) # Convertir a float nativo

            if self.objetivo == 'max':
                if z > mejor_z:
                    mejor_z = z
                    mejor_punto = v
            else:
                if z < mejor_z:
                    mejor_z = z
                    mejor_punto = v
        
        self.registrar_paso(f"5. SOLUCIÓN ÓPTIMA: Punto ({mejor_punto[0]:.2f}, {mejor_punto[1]:.2f}) con Z = {mejor_z:.2f}")

        # Retornamos un diccionario listo para enviar a la web
        return {
            "status": "optimal",
            "z_optimo": float(mejor_z),
            "punto_optimo": [float(mejor_punto[0]), float(mejor_punto[1])],
            "vertices": vertices_para_json,
            "pasos": self.pasos # Aquí va la historia completa
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




