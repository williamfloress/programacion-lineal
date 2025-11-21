from flask import Flask, render_template, request, jsonify
from solver import MetodoGrafico # Importamos tu clase

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

if __name__ == '__main__':
    app.run(debug=True)