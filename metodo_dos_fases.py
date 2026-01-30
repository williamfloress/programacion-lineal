import numpy as np


class MetodoDosFases:
    """
    Método de las Dos Fases para resolver problemas de Programación Lineal.
    
    Este método se usa cuando hay restricciones >= o =, que requieren variables artificiales.
    En lugar de usar Big M, divide el proceso en dos fases:
    - Fase 1: Minimiza W = suma de variables artificiales hasta alcanzar W = 0
    - Fase 2: Elimina artificiales y optimiza la función objetivo original
    """
    
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
        self.tablas = []
        
    def registrar_paso(self, mensaje):
        """Guarda un mensaje en la lista de pasos."""
        self.pasos.append(mensaje)
    
    def _convertir_a_nativo(self, valor):
        """Convierte valores de NumPy a tipos nativos de Python para serialización JSON."""
        if isinstance(valor, (np.integer, np.int64, np.int32)):
            return int(valor)
        elif isinstance(valor, (np.floating, np.float64, np.float32)):
            if np.isinf(valor) or valor == float('inf') or valor == float('-inf'):
                return None
            return float(valor)
        elif isinstance(valor, np.ndarray):
            return valor.tolist()
        elif isinstance(valor, list):
            return [self._convertir_a_nativo(v) for v in valor]
        elif isinstance(valor, dict):
            return {k: self._convertir_a_nativo(v) for k, v in valor.items()}
        elif valor == np.inf or valor == float('inf'):
            return None
        elif valor == -np.inf or valor == float('-inf'):
            return None
        else:
            return valor
    
    def registrar_tabla(self, tabla, iteracion, variables_basicas=None, explicacion="", 
                       nombres_columnas=None, col_entrante=None, fila_saliente=None, 
                       elemento_pivote=None, ratios=None, fase=1):
        """Guarda una tabla para visualización, incluyendo el número de fase."""
        tabla_lista = tabla.tolist()
        tabla_nativa = self._convertir_a_nativo(tabla_lista)
        
        ratios_nativo = None
        if ratios is not None:
            ratios_nativo = []
            for r in ratios:
                if r == np.inf or r == float('inf') or (isinstance(r, (float, np.floating)) and np.isinf(r) and r > 0):
                    ratios_nativo.append(None)
                elif r == -np.inf or r == float('-inf') or (isinstance(r, (float, np.floating)) and np.isinf(r) and r < 0):
                    ratios_nativo.append(None)
                else:
                    ratios_nativo.append(self._convertir_a_nativo(r))
        
        self.tablas.append({
            "fase": int(fase),
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
        """Convierte el problema a forma estándar con variables de holgura, exceso y artificiales."""
        self.registrar_paso("CONVERSIÓN A FORMA ESTÁNDAR:")
        objetivo_str = f"{self.c[0]}x₁"
        for i in range(1, len(self.c)):
            signo = '-' if self.c[i] < 0 else '+'
            abs_val = abs(self.c[i])
            objetivo_str += f" {signo} {abs_val}x₁₊₁".replace("₁₊₁", f"{i+1}")
        self.registrar_paso(f"Problema original: {self.objetivo.upper()} Z = {objetivo_str}")
        
        num_vars = len(self.c)
        num_rest = len(self.b)
        
        # Contar variables auxiliares
        num_holgura = sum(1 for op in self.operadores if op == '<=')
        num_exceso = sum(1 for op in self.operadores if op == '>=')
        num_artificiales = sum(1 for op in self.operadores if op in ['>=', '='])
        
        self.registrar_paso(f"Variables de holgura necesarias: {num_holgura}")
        self.registrar_paso(f"Variables de exceso necesarias: {num_exceso}")
        self.registrar_paso(f"Variables artificiales necesarias: {num_artificiales}")
        
        # Construir matriz extendida
        A_estandar = np.zeros((num_rest, num_vars + num_holgura + num_exceso + num_artificiales))
        col_actual = num_vars
        
        idx_holgura = 0
        idx_exceso = 0
        idx_artificial = 0
        
        indices_artificiales = []  # Guardar índices de columnas de artificiales
        
        for i in range(num_rest):
            if len(self.A[i]) != num_vars:
                raise ValueError(
                    f"La restricción {i+1} tiene {len(self.A[i])} variables, "
                    f"pero la función objetivo tiene {num_vars} variables."
                )
            A_estandar[i, :num_vars] = self.A[i]
            
            if self.operadores[i] == '<=':
                A_estandar[i, col_actual] = 1
                self.registrar_paso(f"R{i+1}: Agregada variable de holgura s{idx_holgura+1}")
                col_actual += 1
                idx_holgura += 1
            elif self.operadores[i] == '>=':
                A_estandar[i, col_actual] = -1
                self.registrar_paso(f"R{i+1}: Agregada variable de exceso e{idx_exceso+1}")
                col_actual += 1
                idx_exceso += 1
                A_estandar[i, col_actual] = 1
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                indices_artificiales.append(col_actual)
                col_actual += 1
                idx_artificial += 1
            elif self.operadores[i] == '=':
                A_estandar[i, col_actual] = 1
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                indices_artificiales.append(col_actual)
                col_actual += 1
                idx_artificial += 1
        
        # Función objetivo extendida (sin Big M)
        c_estandar = np.zeros(num_vars + num_holgura + num_exceso + num_artificiales)
        c_estandar[:num_vars] = np.array(self.c)
        
        return (A_estandar, c_estandar, num_vars, num_holgura, num_exceso, 
                num_artificiales, indices_artificiales)
    
    def fase1(self, A_estandar, num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales):
        """
        Fase 1: Minimizar W = suma de variables artificiales.
        Retorna True si se alcanzó W = 0 (factible), False si no (infactible).
        También retorna la tabla final, variables básicas e índices básicas.
        """
        self.registrar_paso("\n" + "="*60)
        self.registrar_paso("FASE 1: MINIMIZAR W = SUMA DE VARIABLES ARTIFICIALES")
        self.registrar_paso("="*60)
        
        if num_artificiales == 0:
            self.registrar_paso("No hay variables artificiales. Saltando Fase 1.")
            return True, None, None, None
        
        num_rest = len(self.b)
        num_cols_totales = A_estandar.shape[1]
        
        # Identificar variables básicas iniciales
        variables_basicas = []
        indices_basicas = []
        
        col_actual = num_vars
        for i in range(num_rest):
            if self.operadores[i] == '<=':
                variables_basicas.append(f"s{len([v for v in variables_basicas if v.startswith('s')]) + 1}")
                indices_basicas.append(col_actual)
                col_actual += 1
            elif self.operadores[i] == '>=':
                variables_basicas.append(f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}")
                indices_basicas.append(col_actual + 1)
                col_actual += 2
            elif self.operadores[i] == '=':
                variables_basicas.append(f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}")
                indices_basicas.append(col_actual)
                col_actual += 1
        
        # Crear tabla inicial para Fase 1
        tabla = np.zeros((num_rest + 1, num_cols_totales + 1))
        
        # Restricciones
        tabla[1:, :num_cols_totales] = A_estandar
        tabla[1:, -1] = self.b
        
        # Fila W: coeficientes -1 para variables artificiales (porque minimizamos)
        for idx_art in indices_artificiales:
            tabla[0, idx_art] = -1
        
        # Calcular W inicial
        w_val = sum(self.b[i] for i, idx_basica in enumerate(indices_basicas) 
                    if idx_basica in indices_artificiales)
        tabla[0, -1] = w_val
        
        # Actualizar fila W para que coeficientes de básicas sean 0
        for i, idx_basica in enumerate(indices_basicas):
            if abs(tabla[0, idx_basica]) > 1e-9:
                factor = tabla[0, idx_basica]
                tabla[0, :] -= factor * tabla[i + 1, :]
        
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
        
        self.registrar_paso("\nTABLA INICIAL DE FASE 1:")
        self.registrar_tabla(tabla, 0, variables_basicas, "Tabla inicial Fase 1 (minimizar W)", 
                           nombres_columnas=nombres_columnas, fase=1)
        
        # Iteraciones de Simplex para Fase 1 (minimización)
        iteracion = 0
        max_iteraciones = 100
        
        while iteracion < max_iteraciones:
            iteracion += 1
            self.registrar_paso(f"\n--- FASE 1 - ITERACIÓN {iteracion} ---")
            
            fila_w = tabla[0, :num_cols_totales]
            
            # Para minimización: buscamos valores positivos (más positivo reduce más)
            indices_positivos = np.where(fila_w > 1e-9)[0]
            if len(indices_positivos) == 0:
                self.registrar_paso("✓ Condición de optimalidad alcanzada en Fase 1")
                break
            
            col_entrante = int(indices_positivos[np.argmax(fila_w[indices_positivos])])
            
            # Nombre de variable entrante
            if col_entrante < num_vars:
                var_entrante_nombre = f"x{col_entrante + 1}"
            elif col_entrante < num_vars + num_holgura:
                var_entrante_nombre = f"s{col_entrante - num_vars + 1}"
            elif col_entrante < num_vars + num_holgura + num_exceso:
                var_entrante_nombre = f"e{col_entrante - num_vars - num_holgura + 1}"
            else:
                var_entrante_nombre = f"a{col_entrante - num_vars - num_holgura - num_exceso + 1}"
            
            self.registrar_paso(f"📌 VARIABLE ENTRANTE: {var_entrante_nombre}")
            
            # Calcular ratios
            ratios = []
            for i in range(num_rest):
                fila_rest = i + 1
                if tabla[fila_rest, col_entrante] > 1e-9:
                    ratio = float(tabla[fila_rest, -1] / tabla[fila_rest, col_entrante])
                    ratios.append(ratio)
                else:
                    ratios.append(np.inf)
            
            if all(np.isinf(r) for r in ratios):
                self.registrar_paso("\n⚠ Problema no acotado en Fase 1")
                return False, tabla, variables_basicas, indices_basicas
            
            fila_saliente = int(np.argmin(ratios))
            var_saliente_actual = variables_basicas[fila_saliente]
            
            self.registrar_paso(f"📌 VARIABLE SALIENTE: {var_saliente_actual}")
            
            # Pivoteo
            fila_pivote = fila_saliente + 1
            elemento_pivote = float(tabla[fila_pivote, col_entrante])
            
            variables_basicas[fila_saliente] = var_entrante_nombre
            indices_basicas[fila_saliente] = col_entrante
            
            # Normalizar fila pivote
            tabla[fila_pivote, :] /= elemento_pivote
            
            # Eliminación gaussiana
            for i in range(num_rest + 1):
                if i != fila_pivote:
                    factor = tabla[i, col_entrante]
                    tabla[i, :] -= factor * tabla[fila_pivote, :]
            
            w_val = tabla[0, -1]
            self.registrar_paso(f"Nuevo valor de W: {w_val:.6f}")
            
            self.registrar_tabla(tabla.copy(), iteracion, variables_basicas.copy(), 
                               f"Fase 1 - Iteración {iteracion}",
                               nombres_columnas=nombres_columnas,
                               col_entrante=col_entrante,
                               fila_saliente=fila_saliente,
                               elemento_pivote=elemento_pivote,
                               ratios=ratios,
                               fase=1)
        
        # Verificar si W = 0
        w_final = tabla[0, -1]
        self.registrar_paso(f"\n=== FIN DE FASE 1 ===")
        self.registrar_paso(f"Valor final de W: {w_final:.6f}")
        
        if abs(w_final) > 1e-6:
            self.registrar_paso("❌ W > 0: El problema es NO FACTIBLE")
            self.registrar_paso("Las restricciones son contradictorias.")
            return False, tabla, variables_basicas, indices_basicas
        else:
            self.registrar_paso("✓ W = 0: Se encontró una solución básica factible")
            self.registrar_paso("Procediendo a Fase 2...")
            return True, tabla, variables_basicas, indices_basicas
    
    def fase2(self, tabla_fase1, variables_basicas, indices_basicas, c_estandar, 
             num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales):
        """
        Fase 2: Eliminar artificiales y optimizar la función objetivo original.
        """
        self.registrar_paso("\n" + "="*60)
        self.registrar_paso("FASE 2: OPTIMIZAR FUNCIÓN OBJETIVO ORIGINAL")
        self.registrar_paso("="*60)
        
        num_rest = len(self.b)
        num_cols_totales = c_estandar.shape[0]
        
        # Si no había artificiales, crear tabla desde cero
        if tabla_fase1 is None:
            # Crear tabla estándar
            A_estandar = np.zeros((num_rest, num_vars + num_holgura + num_exceso + num_artificiales))
            col_actual = num_vars
            
            for i in range(num_rest):
                A_estandar[i, :num_vars] = self.A[i]
                if self.operadores[i] == '<=':
                    A_estandar[i, col_actual] = 1
                    col_actual += 1
            
            tabla = np.zeros((num_rest + 1, num_cols_totales + 1))
            tabla[1:, :num_cols_totales] = A_estandar
            tabla[1:, -1] = self.b
            
            # Variables básicas iniciales (todas holguras)
            variables_basicas = [f"s{i+1}" for i in range(num_rest)]
            indices_basicas = list(range(num_vars, num_vars + num_rest))
            
            # Fila Z
            tabla[0, :num_cols_totales] = -c_estandar
            z_val = 0
            tabla[0, -1] = z_val
        else:
            # Partir de tabla de Fase 1, restaurar fila Z
            tabla = tabla_fase1.copy()
            
            # Restaurar fila Z con función objetivo original
            tabla[0, :num_cols_totales] = -c_estandar
            
            # Calcular Z inicial
            z_val = sum(c_estandar[indices_basicas[i]] * self.b[i] for i in range(num_rest))
            tabla[0, -1] = z_val
            
            # Actualizar fila Z para básicas (costos reducidos)
            for i, idx_basica in enumerate(indices_basicas):
                if abs(tabla[0, idx_basica]) > 1e-9:
                    factor = tabla[0, idx_basica]
                    tabla[0, :] -= factor * tabla[i + 1, :]
        
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
        
        self.registrar_paso("\nTABLA INICIAL DE FASE 2:")
        self.registrar_tabla(tabla, 0, variables_basicas, "Tabla inicial Fase 2 (optimizar Z)", 
                           nombres_columnas=nombres_columnas, fase=2)
        
        # Iteraciones de Simplex para Fase 2
        iteracion = 0
        max_iteraciones = 100
        
        while iteracion < max_iteraciones:
            iteracion += 1
            self.registrar_paso(f"\n--- FASE 2 - ITERACIÓN {iteracion} ---")
            
            fila_z = tabla[0, :num_cols_totales]
            
            if self.objetivo == 'max':
                indices_negativos = np.where(fila_z < -1e-9)[0]
                if len(indices_negativos) == 0:
                    self.registrar_paso("✓ Condición de optimalidad alcanzada")
                    break
                col_entrante = int(indices_negativos[np.argmin(fila_z[indices_negativos])])
            else:  # min
                indices_positivos = np.where(fila_z > 1e-9)[0]
                if len(indices_positivos) == 0:
                    self.registrar_paso("✓ Condición de optimalidad alcanzada")
                    break
                col_entrante = int(indices_positivos[np.argmax(fila_z[indices_positivos])])
            
            # Nombre variable entrante
            if col_entrante < num_vars:
                var_entrante_nombre = f"x{col_entrante + 1}"
            elif col_entrante < num_vars + num_holgura:
                var_entrante_nombre = f"s{col_entrante - num_vars + 1}"
            elif col_entrante < num_vars + num_holgura + num_exceso:
                var_entrante_nombre = f"e{col_entrante - num_vars - num_holgura + 1}"
            else:
                var_entrante_nombre = f"a{col_entrante - num_vars - num_holgura - num_exceso + 1}"
            
            self.registrar_paso(f"📌 VARIABLE ENTRANTE: {var_entrante_nombre}")
            
            # Calcular ratios
            ratios = []
            for i in range(num_rest):
                fila_rest = i + 1
                if tabla[fila_rest, col_entrante] > 1e-9:
                    ratio = float(tabla[fila_rest, -1] / tabla[fila_rest, col_entrante])
                    ratios.append(ratio)
                else:
                    ratios.append(np.inf)
            
            if all(np.isinf(r) for r in ratios):
                self.registrar_paso("\n⚠ Problema no acotado")
                tablas_serializadas = [self._convertir_a_nativo(t) for t in self.tablas]
                return {
                    "status": "unbounded",
                    "tipo_solucion": "Problema No Acotado",
                    "explicacion": "El problema no tiene solución óptima finita. La región factible es no acotada.",
                    "pasos": self.pasos,
                    "tablas": tablas_serializadas
                }
            
            fila_saliente = int(np.argmin(ratios))
            var_saliente_actual = variables_basicas[fila_saliente]
            
            self.registrar_paso(f"📌 VARIABLE SALIENTE: {var_saliente_actual}")
            
            # Pivoteo
            fila_pivote = fila_saliente + 1
            elemento_pivote = float(tabla[fila_pivote, col_entrante])
            
            variables_basicas[fila_saliente] = var_entrante_nombre
            indices_basicas[fila_saliente] = col_entrante
            
            tabla[fila_pivote, :] /= elemento_pivote
            
            for i in range(num_rest + 1):
                if i != fila_pivote:
                    factor = tabla[i, col_entrante]
                    tabla[i, :] -= factor * tabla[fila_pivote, :]
            
            z_val = tabla[0, -1]
            self.registrar_paso(f"Nuevo valor de Z: {z_val:.4f}")
            
            self.registrar_tabla(tabla.copy(), iteracion, variables_basicas.copy(), 
                               f"Fase 2 - Iteración {iteracion}",
                               nombres_columnas=nombres_columnas,
                               col_entrante=col_entrante,
                               fila_saliente=fila_saliente,
                               elemento_pivote=elemento_pivote,
                               ratios=ratios,
                               fase=2)
        
        # Extraer solución
        solucion = np.zeros(num_vars)
        for i, idx_basica in enumerate(indices_basicas):
            if idx_basica < num_vars:
                fila_rest = i + 1
                solucion[idx_basica] = tabla[fila_rest, -1]
        
        z_optimo = float(tabla[0, -1])
        
        self.registrar_paso(f"\n=== SOLUCIÓN ÓPTIMA ===")
        self.registrar_paso(f"Valor óptimo de Z: {z_optimo:.4f}")
        for i in range(num_vars):
            self.registrar_paso(f"x{i+1} = {solucion[i]:.4f}")
        
        # Analizar tipo de solución
        fila_z_final = tabla[0, :num_cols_totales]
        
        # Contar variables NO básicas (excluyendo artificiales) con coeficiente cero en la fila Z
        vars_no_basicas_cero = 0
        nombres_vars_nb_cero = []
        
        for j in range(num_cols_totales):
            # Excluir variables artificiales del análisis
            es_artificial = (j >= num_vars + num_holgura + num_exceso)
            
            if j not in indices_basicas and not es_artificial:  # Variable no básica (no artificial)
                if abs(fila_z_final[j]) < 1e-9:  # Coeficiente aproximadamente cero
                    vars_no_basicas_cero += 1
                    # Determinar nombre para mostrar
                    if j < num_vars:
                        nombres_vars_nb_cero.append(f"x{j+1}")
                    elif j < num_vars + num_holgura:
                        nombres_vars_nb_cero.append(f"s{j - num_vars + 1}")
                    else:
                        nombres_vars_nb_cero.append(f"e{j - num_vars - num_holgura + 1}")
        
        # Verificar degeneración (variables básicas con valor cero)
        vars_basicas_cero = 0
        for i, idx_basica in enumerate(indices_basicas):
            # Excluir artificiales
            es_artificial = (idx_basica >= num_vars + num_holgura + num_exceso)
            if not es_artificial:
                fila_rest = i + 1
                if abs(tabla[fila_rest, -1]) < 1e-9:  # Valor en solución ≈ 0
                    vars_basicas_cero += 1
        
        # Determinar tipo de solución y explicación
        if vars_no_basicas_cero > 0:
            tipo_solucion = "Solución Múltiple (Infinitas Soluciones)"
            explicacion = (f"Se encontró una solución óptima, pero existen {vars_no_basicas_cero} variable(s) no básica(s) "
                         f"({', '.join(nombres_vars_nb_cero)}) con coeficiente cero en la fila Z. "
                         f"Esto significa que estas variables pueden entrar a la base sin cambiar el valor de Z, "
                         f"generando infinitas soluciones óptimas a lo largo de un borde de la región factible.")
        elif vars_basicas_cero > 0:
            tipo_solucion = "Solución Única (Degenerada)"
            explicacion = (f"Se encontró una solución óptima única, pero hay {vars_basicas_cero} variable(s) básica(s) "
                         f"con valor cero. Esto se llama degeneración y ocurre cuando múltiples restricciones se "
                         f"cruzan en el mismo punto óptimo. A pesar de la degeneración, la solución es única.")
        else:
            tipo_solucion = "Solución Única"
            explicacion = "Se encontró una solución óptima única."
        
        solucion_lista = [float(solucion[i]) for i in range(num_vars)]
        tablas_serializadas = [self._convertir_a_nativo(t) for t in self.tablas]
        
        return {
            "status": "optimal",
            "tipo_solucion": tipo_solucion,
            "explicacion": explicacion,
            "z_optimo": z_optimo,
            "solucion": solucion_lista,
            "iteraciones": iteracion,
            "pasos": self.pasos,
            "tablas": tablas_serializadas
        }
    
    def resolver(self):
        """Resuelve el problema usando el Método de las Dos Fases."""
        self.registrar_paso("=== MÉTODO DE LAS DOS FASES ===")
        
        # Formatear función objetivo
        objetivo_str = f"{self.c[0]}x₁"
        for i in range(1, len(self.c)):
            signo = '-' if self.c[i] < 0 else '+'
            abs_val = abs(self.c[i])
            objetivo_str += f" {signo} {abs_val}x₁₊₁".replace("₁₊₁", f"{i+1}")
        self.registrar_paso(f"FUNCIÓN OBJETIVO: {self.objetivo.upper()} Z = {objetivo_str}")
        
        self.registrar_paso("RESTRICCIONES:")
        for idx, (a_row, b_val, op) in enumerate(zip(self.A, self.b, self.operadores), 1):
            restriccion_str = f"{a_row[0]}x₁"
            for i in range(1, len(a_row)):
                signo = '-' if a_row[i] < 0 else '+'
                abs_val = abs(a_row[i])
                restriccion_str += f" {signo} {abs_val}x₁₊₁".replace("₁₊₁", f"{i+1}")
            self.registrar_paso(f"  R{idx}: {restriccion_str} {op} {b_val}")
        
        # Convertir a forma estándar
        (A_estandar, c_estandar, num_vars, num_holgura, num_exceso, 
         num_artificiales, indices_artificiales) = self.convertir_forma_estandar()
        
        # FASE 1
        factible, tabla_fase1, variables_basicas, indices_basicas = self.fase1(
            A_estandar, num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales
        )
        
        if not factible:
            tablas_serializadas = [self._convertir_a_nativo(t) for t in self.tablas]
            return {
                "status": "infeasible",
                "tipo_solucion": "Problema No Factible",
                "explicacion": "El problema no tiene solución factible. Las restricciones son contradictorias.",
                "pasos": self.pasos,
                "tablas": tablas_serializadas
            }
        
        # FASE 2
        resultado = self.fase2(tabla_fase1, variables_basicas, indices_basicas, c_estandar,
                              num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales)
        
        return resultado
