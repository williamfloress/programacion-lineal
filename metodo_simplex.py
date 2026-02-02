"""
Método Simplex para Programación Lineal.

Sirve para problemas con muchas variables. La idea: convertir todo a forma estándar
(igualdades con variables de holgura/exceso/artificiales), armar una tabla y en cada
iteración entrar una variable que mejore Z y salir otra que mantenga factibilidad;
cuando ya no se puede mejorar, tenemos el óptimo. Uso Big M cuando hay restricciones >= o =.
"""

import numpy as np


class MetodoSimplex:
    def __init__(self, c, A, b, operadores, objetivo='max'):
        """
        Recibo el problema: c (coef. de Z), A y b (restricciones), operadores por fila,
        y si queremos maximizar o minimizar. Todo lo guardo como arrays de numpy.
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.operadores = operadores
        self.objetivo = objetivo
        self.pasos = []   # log de texto para el usuario
        self.tablas = []  # cada tabla del Simplex para mostrarla en la interfaz

    def registrar_paso(self, mensaje):
        """Añado una línea al log de pasos."""
        self.pasos.append(mensaje)

    def _convertir_a_nativo(self, valor):
        """NumPy usa tipos que JSON no entiende (np.int64, np.float64, etc.). Convierto a int/float/list para poder serializar."""
        if isinstance(valor, (np.integer, np.int64, np.int32)):
            return int(valor)
        elif isinstance(valor, (np.floating, np.float64, np.float32)):
            # Verificar si es infinito antes de convertir a float
            if np.isinf(valor) or valor == float('inf') or valor == float('-inf'):
                return None  # Usar None para representar infinito en JSON
            return float(valor)
        elif isinstance(valor, np.ndarray):
            return valor.tolist()
        elif isinstance(valor, list):
            return [self._convertir_a_nativo(v) for v in valor]
        elif isinstance(valor, dict):
            return {k: self._convertir_a_nativo(v) for k, v in valor.items()}
        elif valor == np.inf or valor == float('inf'):
            return None  # Usar None para representar infinito en JSON
        elif valor == -np.inf or valor == float('-inf'):
            return None  # Usar None para representar infinito negativo en JSON
        else:
            return valor
    
    def registrar_tabla(self, tabla, iteracion, variables_basicas=None, explicacion="",
                       nombres_columnas=None, col_entrante=None, fila_saliente=None,
                       elemento_pivote=None, ratios=None):
        """Guardo una foto de la tabla en esta iteración (con variable entrante, saliente, pivote, ratios) para mostrarla después."""
        # Paso todo a tipos nativos para que el front pueda serializar a JSON
        tabla_lista = tabla.tolist()
        tabla_nativa = self._convertir_a_nativo(tabla_lista)
        
        # Convertir ratios si existen
        ratios_nativo = None
        if ratios is not None:
            ratios_nativo = []
            for r in ratios:
                if r == np.inf or r == float('inf') or (isinstance(r, (float, np.floating)) and np.isinf(r) and r > 0):
                    ratios_nativo.append(None)  # Usar None para representar infinito en JSON
                elif r == -np.inf or r == float('-inf') or (isinstance(r, (float, np.floating)) and np.isinf(r) and r < 0):
                    ratios_nativo.append(None)  # Usar None para representar infinito negativo en JSON
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
        """
        Paso el problema a forma estándar: todas las restricciones en igualdad.
        - Si es <= añado variable de holgura (slack) con +1.
        - Si es >= añado variable de exceso con -1 y variable artificial con +1 (para tener base factible).
        - Si es = añado solo variable artificial.
        La función objetivo la extiendo con coeficiente 0 para holgura/exceso y M (Big M) para artificiales.
        """
        self.registrar_paso("CONVERSIÓN A FORMA ESTÁNDAR:")
        self.registrar_paso(f"Problema original: {self.objetivo.upper()} Z = {' + '.join([f'{self.c[i]}x{i+1}' for i in range(len(self.c))])}")
        
        num_vars = len(self.c)
        num_rest = len(self.b)
        
        # Cuento cuántas variables auxiliares necesito según los operadores
        num_holgura = sum(1 for op in self.operadores if op == '<=')
        num_exceso = sum(1 for op in self.operadores if op == '>=')
        num_artificiales = sum(1 for op in self.operadores if op in ['>=', '='])

        self.registrar_paso(f"Variables de holgura necesarias: {num_holgura}")
        self.registrar_paso(f"Variables de exceso necesarias: {num_exceso}")
        self.registrar_paso(f"Variables artificiales necesarias: {num_artificiales}")
        
        # Construyo la matriz A ampliada: mismas filas, más columnas (x's + holguras + excesos + artificiales)
        A_estandar = np.zeros((num_rest, num_vars + num_holgura + num_exceso + num_artificiales))
        col_actual = num_vars

        idx_holgura = 0
        idx_exceso = 0
        idx_artificial = 0
        
        for i in range(num_rest):
            # Primero copio los coeficientes de las x's de esa restricción
            if len(self.A[i]) != num_vars:
                raise ValueError(
                    f"La restricción {i+1} tiene {len(self.A[i])} variables, "
                    f"pero la función objetivo tiene {num_vars} variables. "
                    f"Todas las restricciones deben tener el mismo número de variables que el objetivo."
                )
            A_estandar[i, :num_vars] = self.A[i]
            
            if self.operadores[i] == '<=':
                A_estandar[i, col_actual] = 1   # holgura: ax + ... + s = b
                self.registrar_paso(f"R{i+1}: Agregada variable de holgura s{idx_holgura+1}")
                col_actual += 1
                idx_holgura += 1
            elif self.operadores[i] == '>=':
                A_estandar[i, col_actual] = -1   # exceso: ax - e + a = b (luego la artificial)
                self.registrar_paso(f"R{i+1}: Agregada variable de exceso e{idx_exceso+1}")
                col_actual += 1
                idx_exceso += 1
                A_estandar[i, col_actual] = 1     # artificial para tener columna con 1 y formar base
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                col_actual += 1
                idx_artificial += 1
            elif self.operadores[i] == '=':
                A_estandar[i, col_actual] = 1      # solo artificial
                self.registrar_paso(f"R{i+1}: Agregada variable artificial a{idx_artificial+1}")
                col_actual += 1
                idx_artificial += 1

        # Función objetivo extendida: coef. originales para x's, 0 para holgura/exceso, M para artificiales (Big M)
        c_estandar = np.zeros(num_vars + num_holgura + num_exceso + num_artificiales)
        c_estandar[:num_vars] = np.array(self.c)

        M = 10000   # penalización para que el Simplex expulse las artificiales lo antes posible
        if num_artificiales > 0:
            idx_art = num_vars + num_holgura + num_exceso
            for i in range(num_artificiales):
                c_estandar[idx_art + i] = M
        
        return A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales
    
    def resolver(self):
        """
        Resuelvo el problema: convierto a forma estándar, armo tabla inicial (fila Z + restricciones),
        y en cada iteración elijo variable entrante (la que más mejora Z), variable saliente (ratio mínimo),
        pivoteo y repito hasta que la fila Z indique optimalidad o detecte no acotado / no factible.
        """
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
        
        # Paso 1: llevar el problema a forma estándar (A ampliada, c ampliado)
        A_estandar, c_estandar, num_vars, num_holgura, num_exceso, num_artificiales = self.convertir_forma_estandar()

        num_rest = len(self.b)
        num_cols_totales = A_estandar.shape[1]

        # La base inicial son las columnas que tienen un 1 por fila: holguras y artificiales
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
                indices_basicas.append(col_actual + 1)  # La artificial está después del exceso
                col_actual += 2
            elif self.operadores[i] == '=':
                variables_basicas.append(f"a{len([v for v in variables_basicas if v.startswith('a')]) + 1}")
                indices_basicas.append(col_actual)
                col_actual += 1
        
        # Armo la tabla: fila 0 = Z, filas 1..num_rest = restricciones, última columna = solución (RHS)
        tabla = np.zeros((num_rest + 1, num_cols_totales + 1))

        tabla[1:, :num_cols_totales] = A_estandar
        tabla[1:, -1] = self.b

        # Fila Z: en forma Z - c'x = 0, así que en la tabla pongo -c_j; cuando todos sean >= 0 (max) o <= 0 (min) es óptimo
        tabla[0, :num_cols_totales] = -c_estandar

        # Valor actual de Z = suma de (coef. en Z de variable básica * valor en RHS) para cada fila básica
        z_val = 0
        for i, idx_basica in enumerate(indices_basicas):
            z_val += c_estandar[idx_basica] * self.b[i]
        tabla[0, -1] = z_val

        # Dejo la fila Z en términos de variables no básicas (coef. de básicas = 0) haciendo combinaciones con las filas de restricción
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
        
        self.registrar_paso("\nTABLA INICIAL:")
        self.registrar_tabla(tabla, 0, variables_basicas, "Tabla inicial del Simplex", 
                           nombres_columnas=nombres_columnas)
        
        iteracion = 0
        max_iteraciones = 100
        
        while iteracion < max_iteraciones:
            iteracion += 1
            self.registrar_paso(f"\n--- ITERACIÓN {iteracion} ---")

            fila_z = tabla[0, :num_cols_totales]

            # Condición de parada: en max, si todos los coef. en Z son >= 0 ya no podemos mejorar; en min, si son <= 0
            if self.objetivo == 'max':
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
            
            # Variable saliente: la que limita más el crecimiento de la entrante. Ratio = RHS / coef. entrante (solo si coef. > 0); el mínimo ratio gana
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
                    ratios.append(np.inf)  # Usar np.inf internamente
                    self.registrar_paso(f"   {var_basica_actual}: No se calcula (coeficiente ≤ 0 o muy pequeño)")
            
            # Verificar si todos los ratios son infinito usando np.isinf
            if all(np.isinf(r) for r in ratios):
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
            # Convertir ratio_minimo a float para mostrar, manejando infinito
            if np.isinf(ratio_minimo):
                ratio_minimo_float = None  # Para JSON, pero para mostrar usaremos "∞"
                ratio_minimo_str = "∞"
            else:
                ratio_minimo_float = float(ratio_minimo)
                ratio_minimo_str = f"{ratio_minimo_float:.4f}"
            var_saliente_actual = variables_basicas[fila_saliente] if fila_saliente < len(variables_basicas) else f"Fila {fila_saliente + 1}"
            
            self.registrar_paso(f"\n📌 VARIABLE SALIENTE: {var_saliente_actual}")
            self.registrar_paso(f"   Razón: Tiene el ratio mínimo ({ratio_minimo_str}).")
            if not np.isinf(ratio_minimo):
                self.registrar_paso(f"   El ratio mínimo asegura que al hacer {var_entrante_nombre} = {ratio_minimo_str}, la variable {var_saliente_actual} se vuelve cero (sale de la base).")
            
            # Guardar valor anterior de Z antes del pivoteo
            z_val_anterior = float(tabla[0, -1])
            
            # Actualizar variable básica (usar var_entrante_nombre que ya está definido)
            variables_basicas[fila_saliente] = var_entrante_nombre
            indices_basicas[fila_saliente] = col_entrante
            
            # Pivoteo: normalizar la fila del pivote (dividir por el elemento pivote) y luego hacer ceros en esa columna en el resto de filas
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
            
            # Eliminación gaussiana: en cada otra fila resto (coef. en col. entrante) * fila_pivote para dejar 0 en esa columna
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
            if not np.isinf(ratio_minimo):
                mejora = z_val - z_val_anterior
                self.registrar_paso(f"   Mejora en Z: {mejora:+.4f} ({'aumento' if mejora > 0 else 'disminución' if mejora < 0 else 'sin cambio'})")
            self.registrar_paso(f"   Nueva base: {', '.join(variables_basicas)}")
            if not np.isinf(ratio_minimo):
                self.registrar_paso(f"   {var_entrante_nombre} ahora es básica (valor = {ratio_minimo_str}), {var_saliente_actual} sale de la base (valor = 0)")
            else:
                self.registrar_paso(f"   {var_entrante_nombre} ahora es básica, {var_saliente_actual} sale de la base (valor = 0)")
            
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
        
        # Leo la solución: las x's que están en la base toman el valor del RHS de su fila; las que no están están a 0
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
        
        # Si alguna variable artificial sigue en la base con valor > 0, el problema original es infactible
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
        
        # Clasifico la solución: única, múltiple (alguna no básica con coef. 0 en Z), o degenerada (alguna básica con valor 0)
        fila_z_final = tabla[0, :num_cols_totales]
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
