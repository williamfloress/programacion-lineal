"""
Método de las Dos Fases para Programación Lineal.

Cuando hay restricciones >= o = se usan variables artificiales. En vez de Big M,
se hacen dos etapas:
- Fase 1: minimizar W = suma de artificiales hasta W = 0 → se obtiene una base factible.
- Fase 2: con esa base, optimizar la Z original (Simplex normal).
Si en Fase 1 W no llega a 0, el problema es infactible.

PASOS DEL ALGORITMO (resumen):
  1. Forma estándar (holgura, exceso, artificiales); en Z no se usa Big M.
  2. Fase 1: minimizar W (suma de artificiales); tabla con fila W; Simplex hasta W=0.
  3. Si W=0: Fase 2 con la tabla final, reemplazar fila W por Z y seguir Simplex hasta óptimo.
  4. Si W>0: problema infactible.
"""

import numpy as np


class MetodoDosFases:
    def __init__(self, c, A, b, operadores, objetivo='max'):
        """Mismo formato que Simplex: c, A, b, operadores, objetivo. Guardamos todo para las dos fases."""
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.operadores = operadores
        self.objetivo = objetivo
        self.pasos = []
        self.tablas = []   # tablas de Fase 1 y Fase 2 para mostrarlas

    def registrar_paso(self, mensaje):
        """Añado una línea al log."""
        self.pasos.append(mensaje)

    def _convertir_a_nativo(self, valor):
        """Convierto NumPy a tipos nativos para poder serializar a JSON (igual que en Simplex)."""
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
        """Guardo la tabla de esta iteración indicando si es Fase 1 o Fase 2."""
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
        """
        Forma estándar como en Simplex: <= holgura, >= exceso+artificial, = solo artificial.
        No se usa Big M en Z; Fase 1 minimiza W = suma de artificiales.
        Se guardan índices de columnas artificiales para armar la fila W.
        """
        self.registrar_paso("CONVERSIÓN A FORMA ESTÁNDAR:")
        objetivo_str = f"{self.c[0]}x₁"
        for i in range(1, len(self.c)):
            signo = '-' if self.c[i] < 0 else '+'
            abs_val = abs(self.c[i])
            objetivo_str += f" {signo} {abs_val}x₁₊₁".replace("₁₊₁", f"{i+1}")
        self.registrar_paso(f"Problema original: {self.objetivo.upper()} Z = {objetivo_str}")
        
        num_vars = len(self.c)
        num_rest = len(self.b)
        
        num_holgura = sum(1 for op in self.operadores if op == '<=')
        num_exceso = sum(1 for op in self.operadores if op == '>=')
        num_artificiales = sum(1 for op in self.operadores if op in ['>=', '='])

        self.registrar_paso(f"Variables de holgura necesarias: {num_holgura}")
        self.registrar_paso(f"Variables de exceso necesarias: {num_exceso}")
        self.registrar_paso(f"Variables artificiales necesarias: {num_artificiales}")
        
        A_estandar = np.zeros((num_rest, num_vars + num_holgura + num_exceso + num_artificiales))
        col_actual = num_vars
        idx_holgura = 0
        idx_exceso = 0
        idx_artificial = 0
        indices_artificiales = []   # columnas de artificiales (para fila W en Fase 1)

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
        
        # c extendido: coef. originales para x's, 0 para holgura/exceso/artificiales (en Fase 2 usamos esto para Z)
        c_estandar = np.zeros(num_vars + num_holgura + num_exceso + num_artificiales)
        c_estandar[:num_vars] = np.array(self.c)

        return (A_estandar, c_estandar, num_vars, num_holgura, num_exceso,
                num_artificiales, indices_artificiales)

    def fase1(self, A_estandar, num_vars, num_holgura, num_exceso, num_artificiales, indices_artificiales):
        """
        Fase 1: minimizar W = suma de artificiales (fila W con -1 en cada artificial).
        Simplex hasta que W=0 → base factible; si W>0 al terminar → infactible.
        Devuelve: (factible?, tabla final, variables_basicas, indices_basicas).
        """
        self.registrar_paso("\n" + "="*60)
        self.registrar_paso("FASE 1: MINIMIZAR W = SUMA DE VARIABLES ARTIFICIALES")
        self.registrar_paso("="*60)
        
        if num_artificiales == 0:
            self.registrar_paso("No hay variables artificiales. Saltando Fase 1.")
            return True, None, None, None
        num_rest = len(self.b)
        num_cols_totales = A_estandar.shape[1]
        # Base inicial: una variable por restricción (holgura o artificial)
        variables_basicas = []
        indices_basicas = []
        col_actual = num_vars
        for i in range(num_rest):
            if self.operadores[i] == '<=':
                var_name = f"s{len([v for v in variables_basicas if v.startswith('s')]) + 1}"
                variables_basicas.append(var_name)
                indices_basicas.append(col_actual)
                col_actual += 1
            elif self.operadores[i] == '>=':
                var_name = f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}"
                variables_basicas.append(var_name)
                indices_basicas.append(col_actual + 1)
                col_actual += 2
            elif self.operadores[i] == '=':
                var_name = f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}"
                variables_basicas.append(var_name)
                indices_basicas.append(col_actual)
                col_actual += 1
        
        tabla = np.zeros((num_rest + 1, num_cols_totales + 1))
        tabla[1:, :num_cols_totales] = A_estandar
        tabla[1:, -1] = self.b
        # Fila W: minimizar suma de artificiales → -1 en cada columna artificial
        for idx_art in indices_artificiales:
            tabla[0, idx_art] = -1
        # Expresar fila W solo en no básicas (anular coef. de básicas)
        for i, idx_basica in enumerate(indices_basicas):
            if abs(tabla[0, idx_basica]) > 1e-9:
                factor = tabla[0, idx_basica]
                tabla[0, :] -= factor * tabla[i + 1, :]
        
        # Generar nombres de columnas en el mismo orden que se construyó A_estandar
        nombres_columnas = []
        for i in range(num_vars):
            nombres_columnas.append(f"x{i+1}")
        
        # Agregar nombres de variables auxiliares en el orden que se crearon
        idx_holgura = 1
        idx_exceso = 1
        idx_artificial = 1
        for i in range(num_rest):
            if self.operadores[i] == '<=':
                nombres_columnas.append(f"s{idx_holgura}")
                idx_holgura += 1
            elif self.operadores[i] == '>=':
                nombres_columnas.append(f"e{idx_exceso}")
                idx_exceso += 1
                nombres_columnas.append(f"a{idx_artificial}")
                idx_artificial += 1
            elif self.operadores[i] == '=':
                nombres_columnas.append(f"a{idx_artificial}")
                idx_artificial += 1
        
        self.registrar_paso("\nTABLA INICIAL DE FASE 1:")
        self.registrar_tabla(tabla.copy(), 0, variables_basicas.copy(), "Tabla inicial Fase 1 (minimizar W)", 
                           nombres_columnas=nombres_columnas, fase=1)
        
        # Simplex minimizando W: entrante = mayor coef. positivo en W; saliente = ratio mínimo
        iteracion = 0
        max_iteraciones = 100

        while iteracion < max_iteraciones:
            iteracion += 1
            self.registrar_paso(f"\n--- FASE 1 - ITERACIÓN {iteracion} ---")

            fila_w = tabla[0, :num_cols_totales]
            indices_positivos = np.where(fila_w > 1e-9)[0]
            if len(indices_positivos) == 0:
                self.registrar_paso("✓ Condición de optimalidad alcanzada en Fase 1")
                break
            
            col_entrante = int(indices_positivos[np.argmax(fila_w[indices_positivos])])
            
            # Nombre de variable entrante (usar nombres_columnas ya calculado)
            var_entrante_nombre = nombres_columnas[col_entrante]

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

            fila_pivote = fila_saliente + 1
            elemento_pivote = float(tabla[fila_pivote, col_entrante])
            
            variables_basicas[fila_saliente] = var_entrante_nombre
            indices_basicas[fila_saliente] = col_entrante
            
            tabla[fila_pivote, :] /= elemento_pivote
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
        
        w_final = tabla[0, -1]
        self.registrar_paso(f"\n=== FIN DE FASE 1 ===")
        self.registrar_paso(f"Valor final de W: {w_final:.6f}")
        # Si W no es 0, alguna artificial sigue en base → infactible
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
        Fase 2: partir de tabla final de Fase 1; reemplazar fila W por Z (objetivo original).
        Simplex normal hasta óptimo; artificiales tienen coef. 0 en Z.
        """
        self.registrar_paso("\n" + "="*60)
        self.registrar_paso("FASE 2: OPTIMIZAR FUNCIÓN OBJETIVO ORIGINAL")
        self.registrar_paso("="*60)
        
        num_rest = len(self.b)
        num_cols_totales = c_estandar.shape[0]
        
        if tabla_fase1 is None:
            # Sin artificiales: tabla inicial solo con holguras y fila Z
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
            # Usar tabla de Fase 1 y poner fila Z con objetivo original (-c)
            tabla = tabla_fase1.copy()
            tabla[0, :num_cols_totales] = -c_estandar
            tabla[0, -1] = 0.0
            # Anular en Z los coeficientes de variables básicas (costos reducidos)
            for i, idx_basica in enumerate(indices_basicas):
                if abs(tabla[0, idx_basica]) > 1e-9:
                    factor = tabla[0, idx_basica]
                    tabla[0, :] -= factor * tabla[i + 1, :]
        
        # Generar nombres de columnas en el mismo orden que se construyó A_estandar
        nombres_columnas = []
        for i in range(num_vars):
            nombres_columnas.append(f"x{i+1}")
        
        # Agregar nombres de variables auxiliares en el orden que se crearon
        idx_holgura = 1
        idx_exceso = 1
        idx_artificial = 1
        for i in range(num_rest):
            if self.operadores[i] == '<=':
                nombres_columnas.append(f"s{idx_holgura}")
                idx_holgura += 1
            elif self.operadores[i] == '>=':
                nombres_columnas.append(f"e{idx_exceso}")
                idx_exceso += 1
                nombres_columnas.append(f"a{idx_artificial}")
                idx_artificial += 1
            elif self.operadores[i] == '=':
                nombres_columnas.append(f"a{idx_artificial}")
                idx_artificial += 1

        self.registrar_paso("\nTABLA INICIAL DE FASE 2:")
        self.registrar_tabla(tabla.copy(), 0, variables_basicas.copy(), "Tabla inicial Fase 2 (optimizar Z)",
                           nombres_columnas=nombres_columnas, fase=2)

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
            
            # Nombre variable entrante (usar nombres_columnas ya calculado)
            var_entrante_nombre = nombres_columnas[col_entrante]
            
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
        
        # Leer solución: x's básicas = RHS de su fila; resto 0
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
        
        # Variables NO básicas (excl. artificiales) con coeficiente cero en la fila Z
        nombres_vars_nb_cero = []
        existe_pivote_con_ratio_positivo = False  # ¿Podemos llegar a otro vértice con el mismo Z?
        
        for j in range(num_cols_totales):
            es_artificial = (j >= num_vars + num_holgura + num_exceso)
            if j not in indices_basicas and not es_artificial and abs(fila_z_final[j]) < 1e-9:
                if j < num_vars:
                    nombres_vars_nb_cero.append(f"x{j+1}")
                elif j < num_vars + num_holgura:
                    nombres_vars_nb_cero.append(f"s{j - num_vars + 1}")
                else:
                    nombres_vars_nb_cero.append(f"e{j - num_vars - num_holgura + 1}")
                # Si al pivotar j entrara, el ratio mínimo > 0 → hay otro vértice óptimo (solución múltiple)
                ratios = []
                for i in range(num_rest):
                    if tabla[i + 1, j] > 1e-9:
                        ratios.append(tabla[i + 1, -1] / tabla[i + 1, j])
                if ratios and min(ratios) > 1e-9:
                    existe_pivote_con_ratio_positivo = True
        
        # Verificar degeneración (variables básicas con valor cero)
        vars_basicas_cero = 0
        for i, idx_basica in enumerate(indices_basicas):
            es_artificial = (idx_basica >= num_vars + num_holgura + num_exceso)
            if not es_artificial:
                fila_rest = i + 1
                if abs(tabla[fila_rest, -1]) < 1e-9:
                    vars_basicas_cero += 1
        
        # Determinar tipo: múltiple SOLO si existe pivote que lleve a otro vértice (ratio > 0)
        if nombres_vars_nb_cero and existe_pivote_con_ratio_positivo:
            tipo_solucion = "Solución Múltiple (Infinitas Soluciones)"
            explicacion = (f"Se encontró una solución óptima, pero existen variable(s) no básica(s) "
                         f"({', '.join(nombres_vars_nb_cero)}) con coeficiente cero en la fila Z. "
                         f"Esto permite alcanzar otro vértice óptimo sin cambiar Z, generando infinitas "
                         f"soluciones óptimas a lo largo de un borde de la región factible.")
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
        """Ejecuta: forma estándar → Fase 1 (min W) → si W=0, Fase 2 (opt Z); si W>0 → infactible."""
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
