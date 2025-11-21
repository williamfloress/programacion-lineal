async function resolverProblema() {
    // A. Recolectar datos
    const objetivo = document.getElementById('objetivo').value;
    const z_x = parseFloat(document.getElementById('z_x').value);
    const z_y = parseFloat(document.getElementById('z_y').value);

    // Recolectar restricciones
    const filas = document.querySelectorAll('.fila-restriccion');
    let restricciones = [];
    filas.forEach(fila => {
        restricciones.push({
            x: parseFloat(fila.querySelector('.res-x').value),
            y: parseFloat(fila.querySelector('.res-y').value),
            op: fila.querySelector('.res-op').value,
            val: parseFloat(fila.querySelector('.res-val').value)
        });
    });

    // B. Enviar a Python
    const respuesta = await fetch('/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objetivo, z_x, z_y, restricciones })
    });

    // C. Mostrar Resultados
    const datos = await respuesta.json();
    document.getElementById('resultados').style.display = 'block';

    // 1. CREAR RESUMEN (mostrado por defecto)
    crearResumen(datos);

    // 2. MOSTRAR PASOS DETALLADOS (ocultos por defecto) - Con agrupación visual mejorada
    const logDiv = document.getElementById('log-container');
    logDiv.innerHTML = ''; 
    
    let currentGroup = null;
    let groupContainer = null;
    let currentSection = null;
    
    datos.pasos.forEach((paso, index) => {
        // Detectar inicio de secciones principales
        if (paso.includes("FUNCIÓN OBJETIVO:") || paso.includes("RESTRICCIONES:")) {
            if (currentSection) logDiv.appendChild(currentSection);
            currentSection = document.createElement('div');
            currentSection.className = 'calculation-section';
            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `<span class="section-icon">📋</span><span class="section-title">${paso}</span>`;
            currentSection.appendChild(header);
            const content = document.createElement('div');
            content.className = 'section-content';
            currentSection.appendChild(content);
            currentGroup = null;
            groupContainer = content;
        }
        // Sección de intersecciones
        else if (paso.includes("CÁLCULO DE INTERSECCIONES:")) {
            if (currentSection) logDiv.appendChild(currentSection);
            currentSection = document.createElement('div');
            currentSection.className = 'calculation-section intersection-section';
            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `<span class="section-icon">🔀</span><span class="section-title">${paso}</span>`;
            currentSection.appendChild(header);
            const content = document.createElement('div');
            content.className = 'section-content';
            currentSection.appendChild(content);
            currentGroup = null;
            groupContainer = content;
        }
        // Sección de factibilidad
        else if (paso.includes("VERIFICACIÓN DE FACTIBILIDAD:")) {
            if (currentSection) logDiv.appendChild(currentSection);
            currentSection = document.createElement('div');
            currentSection.className = 'calculation-section feasibility-section';
            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `<span class="section-icon">✅</span><span class="section-title">${paso}</span>`;
            currentSection.appendChild(header);
            const content = document.createElement('div');
            content.className = 'section-content';
            currentSection.appendChild(content);
            currentGroup = null;
            groupContainer = content;
        }
        // Sección de evaluación
        else if (paso.includes("EVALUACIÓN DE VÉRTICES:")) {
            if (currentSection) logDiv.appendChild(currentSection);
            currentSection = document.createElement('div');
            currentSection.className = 'calculation-section evaluation-section';
            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `<span class="section-icon">📊</span><span class="section-title">${paso}</span>`;
            currentSection.appendChild(header);
            const content = document.createElement('div');
            content.className = 'section-content';
            currentSection.appendChild(content);
            currentGroup = null;
            groupContainer = content;
        }
        // Agrupar intersecciones individuales
        else if ((paso.includes("∩") || (paso.includes(" n ") && (paso.includes("R") || paso.includes("Eje")))) && 
                 (paso.includes("R") || paso.includes("Eje"))) {
            if (!currentGroup || currentGroup.className !== 'intersection-group') {
                if (groupContainer) {
                    currentGroup = document.createElement('div');
                    currentGroup.className = 'intersection-group';
                    groupContainer.appendChild(currentGroup);
                }
            }
            if (currentGroup && groupContainer) {
                const intersectionCard = document.createElement('div');
                intersectionCard.className = 'intersection-card';
                const title = paso.trim();
                intersectionCard.innerHTML = `<div class="intersection-title">${title}</div>`;
                currentGroup.appendChild(intersectionCard);
            }
        }
        // Sistema y solución de intersección
        else if (paso.includes("Sistema:") || paso.includes("Solución:")) {
            if (currentGroup && currentGroup.className === 'intersection-group') {
                const lastCard = currentGroup.lastElementChild;
                const detail = document.createElement('div');
                detail.className = paso.includes("Sistema:") ? 'intersection-system' : 'intersection-solution';
                detail.innerHTML = paso;
                lastCard.appendChild(detail);
            }
        }
        // Agrupar verificaciones de un punto
        else if (paso.includes("Punto P(") && paso.includes(":")) {
            if (currentGroup) {
                // Cerrar grupo anterior si existe
            }
            currentGroup = document.createElement('div');
            currentGroup.className = 'point-verification-group';
            const pointHeader = document.createElement('div');
            pointHeader.className = 'point-header';
            pointHeader.innerHTML = `<span class="point-icon">📍</span><span class="point-coords">${paso}</span>`;
            currentGroup.appendChild(pointHeader);
            const checksContainer = document.createElement('div');
            checksContainer.className = 'checks-container';
            currentGroup.appendChild(checksContainer);
            groupContainer.appendChild(currentGroup);
        }
        // Verificaciones individuales
        else if (paso.includes("✓") || paso.includes("✗")) {
            if (currentGroup && currentGroup.className === 'point-verification-group') {
                const checksContainer = currentGroup.querySelector('.checks-container');
                const checkItem = document.createElement('div');
                checkItem.className = `check-item ${paso.includes("✓") ? 'check-valid' : 'check-invalid'}`;
                checkItem.innerHTML = paso;
                checksContainer.appendChild(checkItem);
            }
        }
        // Conclusión de factibilidad
        else if (paso.includes("→") && (paso.includes("es FACTIBLE") || paso.includes("NO es factible"))) {
            if (currentGroup && currentGroup.className === 'point-verification-group') {
                const conclusion = document.createElement('div');
                conclusion.className = `point-conclusion ${paso.includes("FACTIBLE") ? 'conclusion-valid' : 'conclusion-invalid'}`;
                conclusion.innerHTML = paso;
                currentGroup.appendChild(conclusion);
            }
        }
        // Evaluación de vértice
        else if (paso.includes("Vértice (") && paso.includes("Z =")) {
            if (currentGroup) {
                // Cerrar grupo anterior
            }
            currentGroup = document.createElement('div');
            currentGroup.className = 'vertex-evaluation-group';
            const vertexHeader = document.createElement('div');
            vertexHeader.className = 'vertex-header';
            vertexHeader.innerHTML = `<span class="vertex-icon">🎯</span><span class="vertex-title">${paso}</span>`;
            currentGroup.appendChild(vertexHeader);
            groupContainer.appendChild(currentGroup);
        }
        // Cálculo de Z
        else if (paso.match(/^\s+Z = /)) {
            if (currentGroup && currentGroup.className === 'vertex-evaluation-group') {
                const zCalc = document.createElement('div');
                zCalc.className = 'z-calculation';
                zCalc.innerHTML = paso;
                currentGroup.appendChild(zCalc);
            }
        }
        // Restricciones listadas
        else if (paso.trim().startsWith("R") && paso.includes(":") && !paso.includes("∩")) {
            if (currentSection && groupContainer) {
                const restrictionItem = document.createElement('div');
                restrictionItem.className = 'restriction-item';
                restrictionItem.innerHTML = paso;
                groupContainer.appendChild(restrictionItem);
            }
        }
        // Resumen de optimización
        else if (paso.includes("Valores de Z") || paso.includes("Objetivo:") || paso.includes("Mejor Z:") || paso.includes("Vértices óptimos:")) {
            if (currentGroup && currentGroup.className === 'vertex-evaluation-group') {
                const summaryItem = document.createElement('div');
                summaryItem.className = 'optimization-summary';
                summaryItem.innerHTML = paso;
                currentGroup.appendChild(summaryItem);
            }
        }
        // Vértices óptimos
        else if (paso.includes("→") && paso.includes("con Z =")) {
            if (currentGroup && currentGroup.className === 'vertex-evaluation-group') {
                const optimalItem = document.createElement('div');
                optimalItem.className = 'optimal-vertex';
                optimalItem.innerHTML = paso;
                currentGroup.appendChild(optimalItem);
            }
        }
        // Otros pasos - crear sección genérica si no hay una activa
        else {
            if (!currentSection) {
                currentSection = document.createElement('div');
                currentSection.className = 'calculation-section';
                const content = document.createElement('div');
                content.className = 'section-content';
                currentSection.appendChild(content);
                groupContainer = content;
            }
            if (groupContainer) {
                const card = document.createElement('div');
                card.className = 'step-card';
                card.innerHTML = `<span class="step-detail">${paso}</span>`;
                groupContainer.appendChild(card);
            }
        }
    });
    
    // Añadir la última sección
    if (currentSection) {
        logDiv.appendChild(currentSection);
    }

    // 3. DIBUJAR GRÁFICA (en el medio)
    if(datos.status !== 'infeasible') {
        dibujarGrafica(datos, restricciones);
    } else {
        document.getElementById('grafico').innerHTML = "<p style='text-align:center; color:#e74c3c; padding:20px;'>No se puede graficar: Problema no factible</p>";
    }

    // 4. LLENAR TABLA
    const tbody = document.getElementById('cuerpo-tabla');
    tbody.innerHTML = '';
    
    // Convertimos los puntos ganadores a strings para comparar fácil
    const ganadoresStr = datos.puntos_ganadores.map(p => JSON.stringify(p));

    datos.vertices.forEach(v => {
        const x = v[0];
        const y = v[1];
        const z_calc = (parseFloat(z_x) * x) + (parseFloat(z_y) * y);
        
        const tr = document.createElement('tr');
        
        // Verificamos si este punto está en la lista de ganadores
        const esGanador = ganadoresStr.includes(JSON.stringify(v));
        
        if (esGanador) tr.className = 'fila-optima';

        tr.innerHTML = `
            <td>(${x}, ${y})</td>
            <td>${z_calc.toFixed(2)}</td>
            <td>${esGanador ? '★ ÓPTIMO' : ''}</td>
        `;
        tbody.appendChild(tr);
    });

    // 5. MOSTRAR ANÁLISIS Y EXPLICACIÓN FINAL (al final)
    const tituloTipo = document.getElementById('titulo-tipo-solucion');
    const textoExplicacion = document.getElementById('texto-explicacion');
    const cajaFinal = document.getElementById('caja-resultado-final');

    tituloTipo.innerText = datos.tipo_solucion || "Resultado";
    textoExplicacion.innerText = datos.explicacion || "Analizando...";

    if(datos.status === 'infeasible') {
        tituloTipo.style.color = "red";
        document.getElementById('analisis-box').style.borderLeftColor = "red";
        cajaFinal.innerHTML = "No hay solución";
        document.getElementById('cuerpo-tabla').innerHTML = "";
        return;
    }

    // Si es factible:
    tituloTipo.style.color = (datos.tipo_solucion.includes("Múltiple")) ? "#d35400" : "#27ae60"; // Naranja si es múltiple, Verde si es única
    document.getElementById('analisis-box').style.borderLeftColor = (datos.tipo_solucion.includes("Múltiple")) ? "#d35400" : "#27ae60";

    cajaFinal.innerHTML = `Valor Óptimo Z = <strong>${datos.z_optimo}</strong>`;
}

function dibujarGrafica(datos, restricciones) {
    let traces = [];

    // 1. Determinar el rango de la gráfica (Escala)
    // Buscamos el valor más alto entre los vértices para saber qué tan grande hacer el dibujo
    let maxVal = 0;
    datos.vertices.forEach(v => {
        maxVal = Math.max(maxVal, v[0], v[1]);
    });
    const rango = maxVal * 1.5 || 10; // Un poco más de espacio (o 10 por defecto)

    // 2. Dibujar Región Factible (El área sombreada)
    // Necesitamos ordenar los vértices por ángulo para que el polígono se pinte bien
    const verticesOrdenados = ordenarVertices(datos.vertices);
    
    // Añadimos el primer punto al final para cerrar el polígono visualmente
    let x_poly = verticesOrdenados.map(v => v[0]);
    let y_poly = verticesOrdenados.map(v => v[1]);
    x_poly.push(x_poly[0]);
    y_poly.push(y_poly[0]);

    traces.push({
        x: x_poly,
        y: y_poly,
        fill: 'toself',
        type: 'scatter',
        mode: 'lines',
        name: 'Región Factible',
        fillcolor: 'rgba(0, 255, 0, 0.2)', // Verde transparente
        line: {color: 'green'}
    });

    // 3. Dibujar las Líneas de Restricción
    restricciones.forEach((res, index) => {
        // Ecuación: ax + by = val
        // Calculamos dos puntos extremos para dibujar la línea a través de toda la pantalla
        let x1 = 0, y1 = 0, x2 = 0, y2 = 0;

        if (res.y !== 0) {
            // Si y no es 0, calculamos y cuando x=0 y x=rango
            x1 = 0; 
            y1 = res.val / res.y;
            x2 = rango; 
            y2 = (res.val - res.x * rango) / res.y;
        } else {
            // Línea vertical (x = val/a)
            x1 = res.val / res.x;
            y1 = 0;
            x2 = x1;
            y2 = rango;
        }

        traces.push({
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'lines',
            name: `R${index+1}: ${res.x}x + ${res.y}y ${res.op} ${res.val}`,
            line: {dash: 'dot', width: 1} // Línea punteada
        });
    });

    // 4. Marcar el Punto Óptimo
    traces.push({
        x: [datos.punto_optimo[0]],
        y: [datos.punto_optimo[1]],
        type: 'scatter',
        mode: 'markers',
        name: 'Solución Óptima',
        marker: {color: 'red', size: 12}
    });

    // Configuración del Layout
    const layout = {
        title: 'Método Gráfico',
        xaxis: {range: [-1, rango], title: 'Variable X'},
        yaxis: {range: [-1, rango], title: 'Variable Y'},
        showlegend: true,
        hovermode: 'closest'
    };

    Plotly.newPlot('grafico', traces, layout);
}

// Función auxiliar matemática para ordenar puntos en sentido anti-horario
// Esto evita que el polígono se pinte como un "moño" cruzado
function ordenarVertices(puntos) {
    // 1. Calcular centroide
    let cx = 0, cy = 0;
    puntos.forEach(p => { cx += p[0]; cy += p[1]; });
    cx /= puntos.length;
    cy /= puntos.length;

    // 2. Ordenar por ángulo respecto al centroide
    return puntos.sort((a, b) => {
        return Math.atan2(a[1] - cy, a[0] - cx) - Math.atan2(b[1] - cy, b[0] - cx);
    });
}

// Crear resumen corto de los cálculos
function crearResumen(datos) {
    const summaryDiv = document.getElementById('calculations-summary');
    let html = '<div class="summary-box">';
    
    if (datos.status === 'infeasible') {
        html += `
            <div class="summary-item">
                <strong style="color: #e74c3c;">❌ Problema No Factible</strong>
                <p>No existe ningún punto que cumpla todas las restricciones.</p>
            </div>
        `;
    } else {
        // Extraer información clave de los pasos
        const objetivo = datos.pasos.find(p => p.includes("FUNCIÓN OBJETIVO:"));
        const numVertices = datos.vertices ? datos.vertices.length : 0;
        const mejorZ = datos.z_optimo;
        const tipoSol = datos.tipo_solucion;
        
        html += `
            <div class="summary-item">
                <strong>📊 Función Objetivo:</strong>
                <span>${objetivo ? objetivo.replace("FUNCIÓN OBJETIVO: ", "") : "N/A"}</span>
            </div>
            <div class="summary-item">
                <strong>📍 Vértices Encontrados:</strong>
                <span>${numVertices} vértices factibles</span>
            </div>
            <div class="summary-item">
                <strong>🎯 Solución:</strong>
                <span style="color: ${tipoSol.includes("Múltiple") ? "#d35400" : "#27ae60"}; font-weight: bold;">
                    ${tipoSol} - Z = ${mejorZ.toFixed(2)}
                </span>
            </div>
            <div class="summary-item">
                <strong>✅ Vértices Óptimos:</strong>
                <span>${datos.puntos_ganadores.map(p => `(${p[0].toFixed(2)}, ${p[1].toFixed(2)})`).join(", ")}</span>
            </div>
        `;
    }
    
    html += '</div>';
    summaryDiv.innerHTML = html;
}

// Toggle para mostrar/ocultar cálculos detallados
function toggleCalculations() {
    const logContainer = document.getElementById('log-container');
    const summaryDiv = document.getElementById('calculations-summary');
    const toggleBtn = document.getElementById('toggle-calculations');
    const isHidden = logContainer.style.display === 'none' || logContainer.style.display === '';
    
    if (isHidden) {
        // Mostrar detalles
        logContainer.style.display = 'block';
        summaryDiv.style.display = 'none';
        toggleBtn.innerHTML = '<span id="toggle-icon">▲</span> Ocultar Detalles';
    } else {
        // Ocultar detalles
        logContainer.style.display = 'none';
        summaryDiv.style.display = 'block';
        toggleBtn.innerHTML = '<span id="toggle-icon">▼</span> Ver Detalles';
    }
}

