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

if __name__ == '__main__':
    app.run(debug=True)