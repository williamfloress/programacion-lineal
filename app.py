from flask import Flask, render_template, request, jsonify
from solver import MetodoGrafico, MetodoSimplex, convertir_restricciones_relacionales # Importamos las clases y funciones

app = Flask(__name__)

@app.route('/')
def home():
    # Muestra la pagina web (index.html)
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json # Recibe los datos de Javascript
    
    # Extraemos los datos del JSON
    c = [float(data['z_x']), float(data['z_y'])]
    objetivo = data['objetivo']
    
    restricciones = data['restricciones']
    A = []
    b = []
    operadores = []
    
    for r in restricciones:
        A.append([float(r['x']), float(r['y'])])
        b.append(float(r['val']))
        operadores.append(r['op'])
        
    # Llamamos a TU lógica
    solver = MetodoGrafico(c, A, b, operadores, objetivo)
    resultado = solver.resolver()
    
    return jsonify(resultado) # Enviamos la respuesta a Javascript

@app.route('/calcular-simplex', methods=['POST'])
def calcular_simplex():
    data = request.json # Recibe los datos de Javascript
    
    # Extraemos los datos del JSON
    # El frontend puede enviar múltiples variables
    c = [float(x) for x in data['z_coefs']]  # Lista de coeficientes
    objetivo = data['objetivo']
    
    restricciones = data['restricciones']
    A = []
    b = []
    operadores = []
    
    for r in restricciones:
        # Cada restricción tiene coeficientes para todas las variables
        A.append([float(x) for x in r['coefs']])
        b.append(float(r['val']))
        operadores.append(r['op'])
        
    # Llamamos al método Simplex
    solver = MetodoSimplex(c, A, b, operadores, objetivo)
    resultado = solver.resolver()
    
    return jsonify(resultado) # Enviamos la respuesta a Javascript

@app.route('/convertir-restricciones', methods=['POST'])
def convertir_restricciones():
    """Endpoint para convertir restricciones en forma natural a formato estándar."""
    data = request.json
    restricciones_str = data.get('restricciones', [])
    
    try:
        A, b, operadores = convertir_restricciones_relacionales(restricciones_str)
        
        # Formatear respuesta
        restricciones_convertidas = []
        for i, (a_row, b_val, op) in enumerate(zip(A, b, operadores), 1):
            restricciones_convertidas.append({
                'x': float(a_row[0]),
                'y': float(a_row[1]),
                'val': float(b_val),
                'op': op,
                'original': restricciones_str[i-1] if i-1 < len(restricciones_str) else ''
            })
        
        return jsonify({
            'status': 'success',
            'restricciones': restricciones_convertidas
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/convertir-restricciones-simplex', methods=['POST'])
def convertir_restricciones_simplex():
    """Endpoint para convertir restricciones en forma natural a formato estándar para Simplex (múltiples variables)."""
    import re
    
    data = request.json
    restricciones_str = data.get('restricciones', [])
    num_variables = data.get('num_variables', 2)
    
    try:
        restricciones_convertidas = []
        
        for restriccion_str in restricciones_str:
            # Limpiar espacios pero mantener estructura
            restriccion = restriccion_str.strip()
            # Normalizar espacios alrededor de operadores y comas
            restriccion = re.sub(r'\s*([<>=,+])\s*', r'\1', restriccion)
            # Normalizar espacios alrededor de signos menos
            restriccion = re.sub(r'\s*-\s*', r'-', restriccion)
            
            # Detectar operador
            if ">=" in restriccion:
                partes = restriccion.split(">=", 1)
                op = ">="
            elif "<=" in restriccion:
                partes = restriccion.split("<=", 1)
                op = "<="
            elif "=" in restriccion and ">=" not in restriccion and "<=" not in restriccion:
                partes = restriccion.split("=", 1)
                op = "="
            else:
                raise ValueError(f"No se pudo detectar el operador en: {restriccion_str}")
            
            lado_izq = partes[0]
            lado_der = partes[1]
            
            # Parsear lado izquierdo para obtener coeficientes
            coefs = [0.0] * num_variables
            
            # Extraer todos los términos del lado izquierdo
            # Primero intentar con patrón x1, x2, etc.
            patron_subindices = r'([+-]?)(\d*)(x\d+)'
            matches_subindices = re.findall(patron_subindices, lado_izq)
            
            # Si no hay coincidencias con subíndices y hay 2 variables, intentar con x e y
            if not matches_subindices and num_variables == 2:
                # Patrón para x e y (sin subíndices, case-insensitive)
                patron_xy = r'([+-]?)(\d*)([xyXY])'
                matches_xy = re.findall(patron_xy, lado_izq)
                
                for signo, coef_str, var in matches_xy:
                    # x corresponde a índice 0, y corresponde a índice 1
                    if var.lower() == 'x':
                        var_idx = 0
                    elif var.lower() == 'y':
                        var_idx = 1
                    else:
                        continue
                    
                    # Calcular coeficiente
                    coef = float(coef_str) if coef_str else 1.0
                    if signo == '-':
                        coef = -coef
                    
                    coefs[var_idx] = coef
                
                matches = matches_xy
            else:
                # Usar el patrón con subíndices
                matches = matches_subindices
                
                for signo, coef_str, var in matches:
                    # Extraer índice de variable (x1, x2, etc.)
                    var_match = re.match(r'x(\d+)', var)
                    if var_match:
                        var_idx = int(var_match.group(1)) - 1  # Convertir a índice 0-based
                        
                        if var_idx >= num_variables:
                            raise ValueError(f"Variable x{var_idx+1} excede el número de variables definidas ({num_variables})")
                        
                        # Calcular coeficiente
                        coef = float(coef_str) if coef_str else 1.0
                        if signo == '-':
                            coef = -coef
                        elif signo == '+' or not signo:
                            # Si no hay signo al inicio y es el primer término, es positivo
                            pass
                        
                        coefs[var_idx] = coef
            
            # Manejar términos sueltos sin variable (pasar al lado derecho)
            # Si hay términos que no coinciden con el patrón, asumimos que son constantes
            terminos_restantes = lado_izq
            if matches:
                for match in matches:
                    if len(match) == 3:
                        signo, coef_str, var = match
                        # Construir el término completo para eliminarlo
                        # Manejar diferentes casos: "x", "2x", "+x", "-x", "+2x", "-2x"
                        if coef_str:
                            termino_completo = signo + coef_str + var
                        elif signo:
                            termino_completo = signo + var
                        else:
                            termino_completo = var
                        # Reemplazar solo la primera ocurrencia
                        if termino_completo in terminos_restantes:
                            terminos_restantes = terminos_restantes.replace(termino_completo, '', 1)
            
            # Parsear lado derecho para obtener el valor b
            try:
                b_val = float(lado_der)
            except ValueError:
                # Si el lado derecho tiene variables, mover al izquierdo
                # Por simplicidad, asumimos que el lado derecho es solo un número
                raise ValueError(f"El lado derecho debe ser un número en: {restriccion_str}")
            
            # Mover constantes del lado izquierdo al derecho
            if terminos_restantes:
                # Buscar números sueltos en el lado izquierdo
                constantes = re.findall(r'([+-]?\d+\.?\d*)', terminos_restantes)
                for const_str in constantes:
                    try:
                        const_val = float(const_str)
                        b_val -= const_val  # Mover al lado derecho (cambiar signo)
                    except:
                        pass
            
            restricciones_convertidas.append({
                'coefs': coefs,
                'op': op,
                'val': float(b_val),
                'original': restriccion_str
            })
        
        return jsonify({
            'status': 'success',
            'restricciones': restricciones_convertidas
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)