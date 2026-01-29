async function resolverProblema() {
    // A. Recolectar datos
    const objetivo = document.getElementById('objetivo').value;
    
    // Recolectar coeficientes de la función objetivo
    const zCoefs = Array.from(document.querySelectorAll('.z-coef-grafico')).map(input => parseFloat(input.value || 0));
    
    // Recolectar operadores de la función objetivo
    const zOps = Array.from(document.querySelectorAll('.z-op-grafico')).map(select => select.value);
    
    // Validar que haya exactamente 2 variables (X e Y) para el método gráfico
    if (zCoefs.length !== 2) {
        alert('Error: El método gráfico requiere exactamente 2 variables (X e Y)');
        return;
    }
    
    let z_x = zCoefs[0];
    let z_y = zCoefs[1];
    
    // Aplicar operador al segundo coeficiente
    if (zOps.length > 0 && zOps[0] === '-') {
        z_y = -z_y;
    }

    // Verificar qué modo de entrada está activo
    const modoActivoBtn = document.querySelector('.restriction-mode-btn.active');
    const modoActivo = modoActivoBtn ? modoActivoBtn.getAttribute('data-mode') : 'coeficientes';
    let restricciones = [];
    
    if (modoActivo === 'natural') {
        // Modo forma natural: convertir primero
        const textarea = document.getElementById('restricciones-natural');
        const texto = textarea.value.trim();
        
        if (!texto) {
            alert('Error: Debe ingresar al menos una restricción en forma natural.');
            return;
        }
        
        // Dividir por líneas y limpiar
        const restriccionesStr = texto.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
        
        if (restriccionesStr.length === 0) {
            alert('Error: No se encontraron restricciones válidas.');
            return;
        }
        
        try {
            // Convertir a formato estándar
            const respuesta = await fetch('/convertir-restricciones', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ restricciones: restriccionesStr })
            });
            
            const datos = await respuesta.json();
            
            if (datos.status === 'error') {
                alert(`Error al convertir restricciones: ${datos.message}`);
                return;
            }
            
            // Formatear restricciones para el solver
            restricciones = datos.restricciones.map(rest => ({
                x: rest.x,
                y: rest.y,
                op: rest.op,
                val: rest.val
            }));
            
        } catch (error) {
            alert(`Error al convertir restricciones: ${error.message}`);
            return;
        }
    } else {
        // Modo coeficientes: usar el método actual
        const filas = document.querySelectorAll('.fila-restriccion');
        
        if (filas.length === 0) {
            alert('Error: Debe agregar al menos una restricción.');
            return;
        }
        
        filas.forEach(fila => {
            let x = parseFloat(fila.querySelector('.res-x').value || 0);
            let y = parseFloat(fila.querySelector('.res-y').value || 0);
            
            // Aplicar operador entre X e Y
            const opVar = fila.querySelector('.res-op-var');
            if (opVar && opVar.value === '-') {
                y = -y;
            }
            
            restricciones.push({
                x: x,
                y: y,
                op: fila.querySelector('.res-op').value,
                val: parseFloat(fila.querySelector('.res-val').value || 0)
            });
        });
    }

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

    // Recolectar operadores nuevamente para el cálculo de Z en la tabla
    const zOpsRecalc = Array.from(document.querySelectorAll('.z-op-grafico')).map(select => select.value);
    const zCoefsRecalc = Array.from(document.querySelectorAll('.z-coef-grafico')).map(input => parseFloat(input.value || 0));
    let z_y_recalc = zCoefsRecalc[1];
    const signo_y = zOpsRecalc.length > 0 && zOpsRecalc[0] === '-' ? '-' : '+';
    if (zOpsRecalc.length > 0 && zOpsRecalc[0] === '-') {
        z_y_recalc = -z_y_recalc;
    }
    
    const coef_x = zCoefsRecalc[0];
    const coef_y_abs = Math.abs(zCoefsRecalc[1]);
    
    datos.vertices.forEach(v => {
        const x = v[0];
        const y = v[1];
        const z_calc = (coef_x * x) + (z_y_recalc * y);
        
        // Calcular paso a paso para mostrar
        const termino_x = coef_x * x;
        const termino_y = z_y_recalc * y;
        const calculo_paso = `${coef_x}·${x.toFixed(2)} ${signo_y} ${coef_y_abs}·${y.toFixed(2)} = ${termino_x.toFixed(2)} ${signo_y} ${Math.abs(termino_y).toFixed(2)} = ${z_calc.toFixed(2)}`;
        
        const tr = document.createElement('tr');
        
        // Verificamos si este punto está en la lista de ganadores
        const esGanador = ganadoresStr.includes(JSON.stringify(v));
        
        if (esGanador) tr.className = 'fila-optima';

        tr.innerHTML = `
            <td>(${x.toFixed(2)}, ${y.toFixed(2)})</td>
            <td><strong>${z_calc.toFixed(2)}</strong></td>
            <td class="calculo-z" title="Cálculo detallado: ${calculo_paso}">${calculo_paso}</td>
            <td>${esGanador ? '<span style="color: #27ae60; font-weight: bold;">★ ÓPTIMO</span>' : ''}</td>
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
        // Ecuación: ax + by = val (donde b ya puede ser negativo si se eligió operador -)
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
        
        // Formatear el signo para mostrar en la leyenda
        const signoY = res.y >= 0 ? '+' : '-';
        const absY = Math.abs(res.y);

        traces.push({
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'lines',
            name: `R${index+1}: ${res.x}x ${signoY} ${absY}y ${res.op} ${res.val}`,
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

    // Configuración del Layout con soporte para dark mode
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const bgColor = currentTheme === 'dark' ? '#1a1a1a' : '#ffffff';
    const textColor = currentTheme === 'dark' ? '#e0e0e0' : '#333';
    const gridColor = currentTheme === 'dark' ? '#444' : '#ddd';
    
    const layout = {
        title: {
            text: 'Método Gráfico',
            font: { color: textColor }
        },
        xaxis: {
            range: [-1, rango], 
            title: { text: 'Variable X', font: { color: textColor } },
            gridcolor: gridColor,
            linecolor: gridColor,
            zerolinecolor: gridColor,
            tickfont: { color: textColor }
        },
        yaxis: {
            range: [-1, rango], 
            title: { text: 'Variable Y', font: { color: textColor } },
            gridcolor: gridColor,
            linecolor: gridColor,
            zerolinecolor: gridColor,
            tickfont: { color: textColor }
        },
        plot_bgcolor: bgColor,
        paper_bgcolor: bgColor,
        font: { color: textColor },
        showlegend: true,
        hovermode: 'closest',
        legend: {
            font: { color: textColor },
            bgcolor: 'transparent'
        },
        autosize: true
    };

    const config = { responsive: true };
    Plotly.newPlot('grafico', traces, layout, config);
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

// ========== FUNCIONES PARA MÉTODO SIMPLEX ==========

// Cambiar entre métodos
function cambiarMetodo(metodo) {
    // Actualizar tabs
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.includes(metodo === 'grafico' ? 'Gráfico' : 'Simplex')) {
            btn.classList.add('active');
        }
    });
    
    // Mostrar/ocultar secciones
    if (metodo === 'grafico') {
        document.getElementById('metodo-grafico').style.display = 'block';
        document.getElementById('metodo-simplex').style.display = 'none';
        document.getElementById('resultados').style.display = 'none';
        document.getElementById('resultados-simplex').style.display = 'none';
    } else {
        document.getElementById('metodo-grafico').style.display = 'none';
        document.getElementById('metodo-simplex').style.display = 'block';
        document.getElementById('resultados').style.display = 'none';
        document.getElementById('resultados-simplex').style.display = 'none';
        
        // Inicializar simplex con una restricción si no hay ninguna
        const container = document.getElementById('lista-restricciones-simplex');
        if (!container) {
            console.error('Error: No se encontró el contenedor de restricciones Simplex');
            return;
        }
        
        // Verificar si hay variables en la función objetivo antes de agregar restricción
        const numVars = obtenerNumVariables();
        if (numVars > 0 && container.children.length === 0) {
            try {
                agregarRestriccionSimplex();
            } catch (error) {
                console.error('Error al inicializar restricción Simplex:', error);
            }
        }
    }
}

// ========== FUNCIONES PARA MÉTODO GRÁFICO ==========

// Cambiar entre modos de entrada de restricciones
function cambiarModoRestricciones(modo) {
    const modoCoef = document.getElementById('modo-coeficientes');
    const modoNatural = document.getElementById('modo-natural');
    
    // Actualizar botones activos
    const botones = document.querySelectorAll('.restriction-mode-btn');
    botones.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-mode') === modo) {
            btn.classList.add('active');
        }
    });
    
    if (modo === 'coeficientes') {
        modoCoef.style.display = 'block';
        modoNatural.style.display = 'none';
    } else {
        modoCoef.style.display = 'none';
        modoNatural.style.display = 'block';
    }
}

// Convertir restricciones naturales a coeficientes
async function convertirRestriccionesNaturales() {
    const textarea = document.getElementById('restricciones-natural');
    const texto = textarea.value.trim();
    
    if (!texto) {
        alert('Por favor, ingresa al menos una restricción.');
        return;
    }
    
    // Dividir por líneas y limpiar
    const restricciones = texto.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0);
    
    if (restricciones.length === 0) {
        alert('No se encontraron restricciones válidas.');
        return;
    }
    
    try {
        // Llamar al endpoint de conversión
        const respuesta = await fetch('/convertir-restricciones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ restricciones: restricciones })
        });
        
        const datos = await respuesta.json();
        
        if (datos.status === 'error') {
            alert(`Error al convertir restricciones: ${datos.message}`);
            return;
        }
        
        // Limpiar restricciones existentes
        const container = document.getElementById('lista-restricciones');
        container.innerHTML = '';
        
        // Agregar restricciones convertidas
        datos.restricciones.forEach(rest => {
            agregarRestriccionGraficoDesdeDatos(rest);
        });
        
        // Cambiar a modo coeficientes y mostrar
        cambiarModoRestricciones('coeficientes');
        
        // Mostrar mensaje de éxito
        const mensaje = document.createElement('div');
        mensaje.style.cssText = 'margin-top: 10px; padding: 10px; background: #d4edda; color: #155724; border-radius: 4px;';
        mensaje.textContent = `✓ ${datos.restricciones.length} restricción(es) convertida(s) exitosamente.`;
        container.parentElement.insertBefore(mensaje, container.nextSibling);
        
        // Remover mensaje después de 3 segundos
        setTimeout(() => {
            mensaje.remove();
        }, 3000);
        
    } catch (error) {
        alert(`Error al convertir restricciones: ${error.message}`);
    }
}

// Agregar restricción desde datos ya convertidos
function agregarRestriccionGraficoDesdeDatos(datos) {
    const container = document.getElementById('lista-restricciones');
    
    const nuevaFila = document.createElement('div');
    nuevaFila.className = 'fila-restriccion';
    
    // Determinar signo de Y
    const signoY = datos.y >= 0 ? '+' : '-';
    const absY = Math.abs(datos.y);
    
    nuevaFila.innerHTML = `
        <input type="number" class="res-x" value="${datos.x}" style="width: 50px;" inputmode="decimal" autocomplete="off"> X 
        <select class="res-op-var" style="width: 50px; margin: 0 5px; padding: 4px; text-align: center; font-size: 1.2em; font-weight: bold;">
            <option value="+" ${signoY === '+' ? 'selected' : ''}>+</option>
            <option value="-" ${signoY === '-' ? 'selected' : ''}>−</option>
        </select>
        <input type="number" class="res-y" value="${absY}" style="width: 50px;" inputmode="decimal" autocomplete="off"> Y 
        <select class="res-op">
            <option value="<=" ${datos.op === '<=' ? 'selected' : ''}>&le;</option>
            <option value=">=" ${datos.op === '>=' ? 'selected' : ''}>&ge;</option>
            <option value="=" ${datos.op === '=' ? 'selected' : ''}>=</option>
        </select>
        <input type="number" class="res-val" value="${datos.val}" style="width: 60px;" inputmode="decimal" autocomplete="off">
    `;
    
    container.appendChild(nuevaFila);
}

// Agregar una nueva restricción al método gráfico
function agregarRestriccionGrafico() {
    const container = document.getElementById('lista-restricciones');
    
    const nuevaFila = document.createElement('div');
    nuevaFila.className = 'fila-restriccion';
    nuevaFila.innerHTML = `
        <input type="number" class="res-x" value="1" style="width: 50px;" inputmode="decimal" autocomplete="off"> X 
        <select class="res-op-var" style="width: 50px; margin: 0 5px; padding: 4px; text-align: center; font-size: 1.2em; font-weight: bold;">
            <option value="+">+</option>
            <option value="-">−</option>
        </select>
        <input type="number" class="res-y" value="1" style="width: 50px;" inputmode="decimal" autocomplete="off"> Y 
        <select class="res-op">
            <option value="<=">&le;</option>
            <option value=">=">&ge;</option>
            <option value="=">=</option>
        </select>
        <input type="number" class="res-val" value="10" style="width: 60px;" inputmode="decimal" autocomplete="off">
    `;
    
    container.appendChild(nuevaFila);
}

// Eliminar la última restricción del método gráfico
function eliminarRestriccionGrafico() {
    const container = document.getElementById('lista-restricciones');
    const restricciones = container.querySelectorAll('.fila-restriccion');
    
    if (restricciones.length === 0) {
        alert('No hay restricciones para eliminar');
        return;
    }
    
    const ultimaRestriccion = restricciones[restricciones.length - 1];
    container.removeChild(ultimaRestriccion);
}

// Obtener número de variables actuales
function obtenerNumVariables() {
    return document.querySelectorAll('.z-coef').length;
}

// Agregar una nueva restricción con todas las variables actuales
function agregarRestriccionSimplex() {
    const numVars = obtenerNumVariables();
    
    if (numVars === 0) {
        alert('Primero debe agregar al menos una variable a la función objetivo');
        return;
    }
    
    const container = document.getElementById('lista-restricciones-simplex');
    
    // Crear nueva fila de restricción
    const nuevaFila = document.createElement('div');
    nuevaFila.className = 'fila-restriccion-simplex';
    nuevaFila.style.marginBottom = '10px';
    
    // Crear inputs para cada variable usando DOM en lugar de innerHTML para mejor control
    for (let i = 0; i < numVars; i++) {
        const subindice = numeroASubindice(i + 1);
        const esUltima = (i === numVars - 1);
        
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'res-coef';
        input.value = '0';
        input.style.width = '50px';
        input.setAttribute('data-var', i);
        input.setAttribute('inputmode', 'decimal');
        input.setAttribute('autocomplete', 'off');
        nuevaFila.appendChild(input);
        
        const textoVar = document.createTextNode(` X${subindice}${esUltima ? ' ' : ' '}`);
        nuevaFila.appendChild(textoVar);
        
        // Agregar operador entre variables (excepto después de la última)
        if (!esUltima) {
            const operadorSelect = document.createElement('select');
            operadorSelect.className = 'res-op-var-simplex';
            operadorSelect.setAttribute('data-var', i + 1);
            operadorSelect.style.width = '50px';
            operadorSelect.style.margin = '0 5px';
            operadorSelect.style.padding = '4px';
            operadorSelect.style.textAlign = 'center';
            operadorSelect.style.fontSize = '1.2em';
            operadorSelect.style.fontWeight = 'bold';
            operadorSelect.innerHTML = `
                <option value="+">+</option>
                <option value="-">−</option>
            `;
            nuevaFila.appendChild(operadorSelect);
        }
    }
    
    // Agregar selector de operador
    const select = document.createElement('select');
    select.className = 'res-op-simplex';
    select.innerHTML = `
        <option value="<=">&le;</option>
        <option value=">=">&ge;</option>
        <option value="=">=</option>
    `;
    nuevaFila.appendChild(select);
    
    // Agregar input para el valor
    const inputVal = document.createElement('input');
    inputVal.type = 'number';
    inputVal.className = 'res-val-simplex';
    inputVal.value = '0';
    inputVal.style.width = '60px';
    inputVal.setAttribute('inputmode', 'decimal');
    inputVal.setAttribute('autocomplete', 'off');
    nuevaFila.appendChild(inputVal);
    
    container.appendChild(nuevaFila);
}

// Eliminar la última restricción
function eliminarRestriccionSimplex() {
    const container = document.getElementById('lista-restricciones-simplex');
    const restricciones = container.querySelectorAll('.fila-restriccion-simplex');
    
    if (restricciones.length === 0) {
        alert('No hay restricciones para eliminar');
        return;
    }
    
    const ultimaRestriccion = restricciones[restricciones.length - 1];
    container.removeChild(ultimaRestriccion);
}

// Función auxiliar para convertir número a subíndice
function numeroASubindice(num) {
    const subindices = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉'];
    return num.toString().split('').map(d => subindices[parseInt(d)]).join('');
}

// Agregar variable al método Simplex
function agregarVariableSimplex() {
    const numVars = obtenerNumVariables();
    const nuevaVar = numVars + 1;
    const subindice = numeroASubindice(nuevaVar);
    
    // Agregar a función objetivo
    const container = document.getElementById('z-coefs-container');
    
    // Si hay variables existentes, agregar operador antes de la nueva
    if (numVars > 0) {
        // Crear dropdown de operador
        const operadorSelect = document.createElement('select');
        operadorSelect.className = 'z-op';
        operadorSelect.setAttribute('data-var', numVars);
        operadorSelect.style.width = '50px';
        operadorSelect.style.margin = '0 5px';
        operadorSelect.style.padding = '4px';
        operadorSelect.style.textAlign = 'center';
        operadorSelect.style.fontSize = '1.2em';
        operadorSelect.style.fontWeight = 'bold';
        operadorSelect.innerHTML = `
            <option value="+">+</option>
            <option value="-">−</option>
        `;
        
        // Encontrar el último nodo de texto de variable y insertar después de él
        const ultimoInput = container.querySelector('.z-coef:last-of-type');
        if (ultimoInput) {
            // Buscar el texto de la última variable
            let nodoActual = ultimoInput.nextSibling;
            while (nodoActual) {
                if (nodoActual.nodeType === 3 && nodoActual.textContent.trim().match(/^X[₀₁₂₃₄₅₆₇₈₉]+$/)) {
                    // Insertar el operador después del texto de variable
                    container.insertBefore(operadorSelect, nodoActual.nextSibling);
                    break;
                }
                nodoActual = nodoActual.nextSibling;
            }
            // Si no encontramos el nodo de texto, insertar al final
            if (!nodoActual || !nodoActual.nextSibling) {
                container.appendChild(operadorSelect);
            }
        } else {
            container.appendChild(operadorSelect);
        }
    }
    
    // Crear los nuevos elementos
    const nuevoInput = document.createElement('input');
    nuevoInput.type = 'number';
    nuevoInput.className = 'z-coef';
    nuevoInput.value = '0';
    nuevoInput.style.width = '50px';
    nuevoInput.setAttribute('data-var', numVars);
    nuevoInput.setAttribute('inputmode', 'decimal');
    nuevoInput.setAttribute('autocomplete', 'off');
    
    const textoVar = document.createTextNode(` X${subindice}`);
    
    // Insertar al final del contenedor
    container.appendChild(nuevoInput);
    container.appendChild(textoVar);
    
    // Agregar a TODAS las restricciones existentes
    const filasRestricciones = document.querySelectorAll('.fila-restriccion-simplex');
    
    filasRestricciones.forEach(fila => {
        const ultimoCoef = fila.querySelector('.res-coef:last-of-type');
        const selectOp = fila.querySelector('.res-op-simplex');
        
        if (ultimoCoef) {
            // Buscar el texto de la última variable
            let nodoTexto = ultimoCoef.nextSibling;
            while (nodoTexto) {
                if (nodoTexto.nodeType === 3 && nodoTexto.textContent.trim().match(/^X[₀₁₂₃₄₅₆₇₈₉]+$/)) {
                    // Crear dropdown de operador para restricciones
                    const operadorSelect = document.createElement('select');
                    operadorSelect.className = 'res-op-var-simplex';
                    operadorSelect.setAttribute('data-var', numVars);
                    operadorSelect.style.width = '50px';
                    operadorSelect.style.margin = '0 5px';
                    operadorSelect.style.padding = '4px';
                    operadorSelect.style.textAlign = 'center';
                    operadorSelect.style.fontSize = '1em';
                    operadorSelect.innerHTML = `
                        <option value="+">+</option>
                        <option value="-">-</option>
                    `;
                    
                    // Insertar el operador después del texto de variable
                    fila.insertBefore(operadorSelect, nodoTexto.nextSibling);
                    
                    // Crear el nuevo coeficiente y su texto
                    const nuevoCoef = document.createElement('input');
                    nuevoCoef.type = 'number';
                    nuevoCoef.className = 'res-coef';
                    nuevoCoef.value = '0';
                    nuevoCoef.style.width = '50px';
                    nuevoCoef.setAttribute('data-var', numVars);
                    nuevoCoef.setAttribute('inputmode', 'decimal');
                    nuevoCoef.setAttribute('autocomplete', 'off');
                    const textoVarRest = document.createTextNode(` X${subindice}`);
                    fila.insertBefore(nuevoCoef, operadorSelect.nextSibling);
                    fila.insertBefore(textoVarRest, operadorSelect.nextSibling);
                    break;
                }
                nodoTexto = nodoTexto.nextSibling;
            }
        } else if (selectOp) {
            const nuevoCoef = document.createElement('input');
            nuevoCoef.type = 'number';
            nuevoCoef.className = 'res-coef';
            nuevoCoef.value = '0';
            nuevoCoef.style.width = '50px';
            nuevoCoef.setAttribute('data-var', numVars);
            nuevoCoef.setAttribute('inputmode', 'decimal');
            nuevoCoef.setAttribute('autocomplete', 'off');
            const textoVarRest = document.createTextNode(` X${subindice}`);
            fila.insertBefore(nuevoCoef, selectOp);
            fila.insertBefore(textoVarRest, selectOp);
        }
    });
}

// Función auxiliar para sincronizar una restricción con el número correcto de variables
function sincronizarRestriccion(fila, numVarsEsperado) {
    const coeficientes = fila.querySelectorAll('.res-coef');
    const numVarsActual = coeficientes.length;
    
    if (numVarsActual < numVarsEsperado) {
        // Agregar variables faltantes
        for (let i = numVarsActual; i < numVarsEsperado; i++) {
            const nuevaVar = i + 1;
            const subindice = numeroASubindice(nuevaVar);
            const ultimoCoef = fila.querySelector('.res-coef:last-of-type');
            
            if (ultimoCoef) {
                let nodoVariable = ultimoCoef.nextSibling;
                while (nodoVariable) {
                    if (nodoVariable.nodeType === 3 && nodoVariable.textContent.includes('X')) {
                        const textoOriginal = nodoVariable.textContent.trim();
                        nodoVariable.textContent = textoOriginal + ' + ';
                        break;
                    }
                    nodoVariable = nodoVariable.nextSibling;
                }
                
                const nuevoCoef = document.createElement('input');
                nuevoCoef.type = 'number';
                nuevoCoef.className = 'res-coef';
                nuevoCoef.value = '0';
                nuevoCoef.style.width = '50px';
                nuevoCoef.setAttribute('data-var', i);
                nuevoCoef.setAttribute('inputmode', 'decimal');
                nuevoCoef.setAttribute('autocomplete', 'off');
                const textoVar = document.createTextNode(` X${subindice}`);
                if (nodoVariable) {
                    const puntoInsercion = nodoVariable.nextSibling;
                    fila.insertBefore(textoVar, puntoInsercion);
                    fila.insertBefore(nuevoCoef, puntoInsercion);
                } else {
                    fila.appendChild(nuevoCoef);
                    fila.appendChild(textoVar);
                }
            }
        }
    }
}

// Función para re-indexar todas las variables después de eliminar
function reindexarVariablesSimplex() {
    // Re-indexar función objetivo
    const container = document.getElementById('z-coefs-container');
    const inputs = Array.from(container.querySelectorAll('.z-coef'));
    
    inputs.forEach((input, index) => {
        // Actualizar el atributo data-var
        input.setAttribute('data-var', index);
        
        // Encontrar y actualizar el nodo de texto de la variable (debe ser el siguiente nodo)
        const nodoTexto = input.nextSibling;
        if (nodoTexto && nodoTexto.nodeType === 3) {
            const texto = nodoTexto.textContent;
            const nuevoSubindice = numeroASubindice(index + 1);
            // Reemplazar el subíndice manteniendo el formato
            const textoLimpio = texto.replace(/X[₀₁₂₃₄₅₆₇₈₉]+/, `X${nuevoSubindice}`);
            nodoTexto.textContent = textoLimpio;
        }
    });
    
    // Re-indexar todas las restricciones
    const filasRestricciones = document.querySelectorAll('.fila-restriccion-simplex');
    filasRestricciones.forEach(fila => {
        const coeficientes = Array.from(fila.querySelectorAll('.res-coef'));
        coeficientes.forEach((coef, index) => {
            // Actualizar el atributo data-var
            coef.setAttribute('data-var', index);
            
            // Encontrar y actualizar el nodo de texto de la variable (debe ser el siguiente nodo)
            const nodoTexto = coef.nextSibling;
            if (nodoTexto && nodoTexto.nodeType === 3) {
                const texto = nodoTexto.textContent;
                const nuevoSubindice = numeroASubindice(index + 1);
                // Reemplazar el subíndice manteniendo el formato
                const textoLimpio = texto.replace(/X[₀₁₂₃₄₅₆₇₈₉]+/, `X${nuevoSubindice}`);
                nodoTexto.textContent = textoLimpio;
            }
        });
    });
}

// Eliminar variable del método Simplex
function eliminarVariableSimplex() {
    const numVars = obtenerNumVariables();
    if (numVars <= 0) {
        alert('No hay variables para eliminar');
        return;
    }
    
    // Eliminar de función objetivo
    const container = document.getElementById('z-coefs-container');
    const inputs = Array.from(container.querySelectorAll('.z-coef'));
    
    if (inputs.length === 0) {
        return;
    }
    
    const ultimoInput = inputs[inputs.length - 1];
    const elementosAEliminar = [];
    
    // Encontrar el texto de la variable después del último input
    let nodoActual = ultimoInput.nextSibling;
    while (nodoActual) {
        if (nodoActual.nodeType === 3 && nodoActual.textContent.trim().match(/^X[₀₁₂₃₄₅₆₇₈₉]+$/)) {
            elementosAEliminar.push(nodoActual);
            break;
        }
        nodoActual = nodoActual.nextSibling;
    }
    
    // Si hay más de una variable, encontrar el operador antes de esta variable
    if (inputs.length > 1) {
        // Estructura: Input1 -> Text " X₁" -> Operator -> Input2 -> Text " X₂"
        // Necesitamos encontrar el operador que viene justo antes de Input2
        const inputAnterior = inputs[inputs.length - 2];
        nodoActual = inputAnterior.nextSibling;
        
        // Buscar todos los nodos entre inputAnterior y ultimoInput
        while (nodoActual && nodoActual !== ultimoInput) {
            if (nodoActual.nodeType === 1 && nodoActual.classList.contains('z-op')) {
                elementosAEliminar.push(nodoActual);
                break;
            }
            nodoActual = nodoActual.nextSibling;
        }
    }
    
    // Eliminar todos los elementos encontrados
    elementosAEliminar.forEach(elem => {
        if (elem.parentNode) {
            elem.parentNode.removeChild(elem);
        }
    });
    
    // Finalmente eliminar el input
    container.removeChild(ultimoInput);
    
    // Eliminar de TODAS las restricciones - esto es crítico
    const filasRestricciones = document.querySelectorAll('.fila-restriccion-simplex');
    
    filasRestricciones.forEach(fila => {
        const coefs = Array.from(fila.querySelectorAll('.res-coef'));
        
        if (coefs.length === 0) {
            return;
        }
        
        const ultimoCoef = coefs[coefs.length - 1];
        const elementosAEliminar = [];
        
        // Encontrar el texto de la variable después del último coeficiente
        let nodoActual = ultimoCoef.nextSibling;
        while (nodoActual) {
            // Si encontramos el select de operador de restricción, significa que no hay texto
            if (nodoActual.nodeType === 1 && nodoActual.classList.contains('res-op-simplex')) {
                break;
            }
            if (nodoActual.nodeType === 3 && nodoActual.textContent.trim().match(/^X[₀₁₂₃₄₅₆₇₈₉]+$/)) {
                elementosAEliminar.push(nodoActual);
                break;
            }
            nodoActual = nodoActual.nextSibling;
        }
        
        // Si hay más de una variable, encontrar el operador antes de este coeficiente
        if (coefs.length > 1) {
            const coefAnterior = coefs[coefs.length - 2];
            nodoActual = coefAnterior.nextSibling;
            
            // Buscar todos los nodos entre coefAnterior y ultimoCoef
            while (nodoActual && nodoActual !== ultimoCoef) {
                if (nodoActual.nodeType === 1 && nodoActual.classList.contains('res-op-var-simplex')) {
                    elementosAEliminar.push(nodoActual);
                    break;
                }
                nodoActual = nodoActual.nextSibling;
            }
        }
        
        // Eliminar todos los elementos encontrados
        elementosAEliminar.forEach(elem => {
            if (elem.parentNode) {
                elem.parentNode.removeChild(elem);
            }
        });
        
        // Finalmente eliminar el coeficiente
        fila.removeChild(ultimoCoef);
    });
    
    // Re-indexar todas las variables después de eliminar
    reindexarVariablesSimplex();
}

// Resolver problema con Simplex
async function resolverSimplex() {
    // Recolectar datos
    const objetivo = document.getElementById('objetivo-simplex').value;
    const zCoefsInputs = Array.from(document.querySelectorAll('.z-coef'));
    const zOpsInputs = Array.from(document.querySelectorAll('.z-op'));
    
    // Recolectar coeficientes y aplicar operadores
    let zCoefs = [];
    zCoefsInputs.forEach((input, index) => {
        let coef = parseFloat(input.value || 0);
        // Aplicar operador si existe (el operador está antes de este coeficiente)
        if (index > 0) {
            const opIndex = index - 1;
            if (opIndex < zOpsInputs.length) {
                const op = zOpsInputs[opIndex].value;
                if (op === '-') {
                    coef = -coef;
                }
            }
        }
        zCoefs.push(coef);
    });
    
    const numVarsObjetivo = zCoefs.length;
    
    // Validar que haya al menos una variable
    if (numVarsObjetivo === 0) {
        alert('Error: Debe agregar al menos una variable a la función objetivo.');
        return;
    }
    
    // Verificar qué modo de entrada está activo
    const modoActivoBtn = document.querySelector('.restriction-mode-btn-simplex.active');
    const modoActivo = modoActivoBtn ? modoActivoBtn.getAttribute('data-mode') : 'coeficientes';
    let restricciones = [];
    
    if (modoActivo === 'natural') {
        // Modo forma natural: convertir primero
        const textarea = document.getElementById('restricciones-natural-simplex');
        const texto = textarea.value.trim();
        
        if (!texto) {
            alert('Error: Debe ingresar al menos una restricción en forma natural.');
            return;
        }
        
        // Dividir por líneas y limpiar
        const restriccionesStr = texto.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
        
        if (restriccionesStr.length === 0) {
            alert('Error: No se encontraron restricciones válidas.');
            return;
        }
        
        try {
            // Convertir a formato estándar
            const respuesta = await fetch('/convertir-restricciones-simplex', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    restricciones: restriccionesStr,
                    num_variables: numVarsObjetivo
                })
            });
            
            const datos = await respuesta.json();
            
            if (datos.status === 'error') {
                alert(`Error al convertir restricciones: ${datos.message}`);
                return;
            }
            
            // Formatear restricciones para el solver
            restricciones = datos.restricciones.map(rest => ({
                coefs: rest.coefs,
                op: rest.op,
                val: rest.val
            }));
            
        } catch (error) {
            alert(`Error al convertir restricciones: ${error.message}`);
            return;
        }
    } else {
        // Modo coeficientes: usar el método actual
        const filas = document.querySelectorAll('.fila-restriccion-simplex');
        
        if (filas.length === 0) {
            alert('Error: Debe agregar al menos una restricción.');
            return;
        }
        
        filas.forEach((fila, index) => {
        const coefsInputs = Array.from(fila.querySelectorAll('.res-coef'));
        const opsInputs = Array.from(fila.querySelectorAll('.res-op-var-simplex'));
        
        // Aplicar operadores a los coeficientes
        let coefs = [];
        coefsInputs.forEach((input, idx) => {
            let coef = parseFloat(input.value || 0);
            // Aplicar operador si existe (el operador está antes de este coeficiente)
            if (idx > 0) {
                const opIndex = idx - 1;
                if (opIndex < opsInputs.length) {
                    const op = opsInputs[opIndex].value;
                    if (op === '-') {
                        coef = -coef;
                    }
                }
            }
            coefs.push(coef);
        });
        
        // Validar que la restricción tenga el mismo número de variables que el objetivo
        if (coefs.length !== numVarsObjetivo) {
            alert(`Error: La restricción ${index + 1} tiene ${coefs.length} variables pero el objetivo tiene ${numVarsObjetivo}. Por favor, sincronice las restricciones.`);
            return;
        }
        
        const opSelect = fila.querySelector('.res-op-simplex');
        const valInput = fila.querySelector('.res-val-simplex');
        
        if (!opSelect || !valInput) {
            alert(`Error: La restricción ${index + 1} está incompleta.`);
            return;
        }
        
            restricciones.push({
                coefs: coefs,
                op: opSelect.value,
                val: parseFloat(valInput.value || 0)
            });
        });
    }
    
    // Validar que todas las restricciones tengan el mismo número de variables
    const todasTienenMismoNumero = restricciones.every(r => r.coefs.length === numVarsObjetivo);
    if (!todasTienenMismoNumero || restricciones.length === 0) {
        alert('Error: Todas las restricciones deben tener el mismo número de variables que la función objetivo.');
        return;
    }
    
    // Enviar a Python (los operadores ya están aplicados en los coeficientes)
    const respuesta = await fetch('/calcular-simplex', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objetivo, z_coefs: zCoefs, restricciones })
    });
    
    // Mostrar resultados
    const datos = await respuesta.json();
    document.getElementById('resultados-simplex').style.display = 'block';
    
    // Mostrar pasos
    mostrarPasosSimplex(datos);
    
    // Mostrar tablas
    mostrarTablasSimplex(datos);
    
    // Mostrar solución final
    mostrarSolucionSimplex(datos);
}

// Mostrar pasos del Simplex
function mostrarPasosSimplex(datos) {
    const logDiv = document.getElementById('log-container-simplex');
    logDiv.innerHTML = '';
    
    datos.pasos.forEach(paso => {
        const pasoDiv = document.createElement('div');
        pasoDiv.className = 'step-card';
        pasoDiv.innerHTML = `<span class="step-detail">${paso}</span>`;
        logDiv.appendChild(pasoDiv);
    });
    
    // Crear resumen
    crearResumenSimplex(datos);
}

// Crear resumen para Simplex
function crearResumenSimplex(datos) {
    const summaryDiv = document.getElementById('calculations-summary-simplex');
    let html = '<div class="summary-box">';
    
    if (datos.status === 'infeasible') {
        html += `
            <div class="summary-item">
                <strong style="color: #e74c3c;">❌ Problema No Factible</strong>
                <p>${datos.explicacion}</p>
            </div>
        `;
    } else if (datos.status === 'unbounded') {
        html += `
            <div class="summary-item">
                <strong style="color: #e67e22;">⚠ Problema No Acotado</strong>
                <p>${datos.explicacion}</p>
            </div>
        `;
    } else {
        html += `
            <div class="summary-item">
                <strong>📊 Iteraciones:</strong>
                <span>${datos.iteraciones} iteraciones realizadas</span>
            </div>
            <div class="summary-item">
                <strong>🎯 Solución:</strong>
                <span style="color: #27ae60; font-weight: bold;">
                    Z = ${datos.z_optimo.toFixed(4)}
                </span>
            </div>
            <div class="summary-item">
                <strong>✅ Variables:</strong>
                <span>${datos.solucion.map((val, idx) => `x${idx+1} = ${val.toFixed(4)}`).join(', ')}</span>
            </div>
        `;
    }
    
    html += '</div>';
    summaryDiv.innerHTML = html;
}

// Mostrar tablas del Simplex
function mostrarTablasSimplex(datos) {
    const container = document.getElementById('tablas-simplex-container');
    container.innerHTML = '';
    
    console.log('Datos recibidos:', datos);
    console.log('Tablas:', datos.tablas);
    
    if (!datos.tablas || datos.tablas.length === 0) {
        container.innerHTML = '<p style="color: red;">No hay tablas para mostrar. (datos.tablas está vacío o no existe)</p>';
        return;
    }
    
    // Agregar explicación general sobre las tablas
    const explicacionGeneral = document.createElement('div');
    explicacionGeneral.style.cssText = 'margin-bottom: 20px; padding: 15px; background: #e8f4f8; border-radius: 8px; border-left: 4px solid #9b59b6;';
    explicacionGeneral.innerHTML = `
        <strong>💡 Explicación de las Tablas del Simplex:</strong>
        <ul style="margin: 10px 0 0 20px; padding: 0;">
            <li><strong>Variables Básicas:</strong> Variables que están en la solución actual (tienen valor distinto de cero).</li>
            <li><strong>Fila Z:</strong> Muestra los coeficientes reducidos. Valores negativos (max) o positivos (min) indican que se puede mejorar la solución.</li>
            <li><strong>Columna Solución:</strong> Muestra el valor actual de las variables básicas y el valor de Z.</li>
            <li><strong>Elemento Pivote:</strong> Intersección de la variable entrante y la fila de la variable saliente. Se usa para realizar el pivoteo.</li>
            <li><strong>Ratios:</strong> Se calculan dividiendo la columna Solución entre la columna de la variable entrante. El menor ratio determina la variable saliente.</li>
        </ul>
    `;
    container.appendChild(explicacionGeneral);
    
    datos.tablas.forEach((tablaInfo, idx) => {
        const tablaDiv = document.createElement('div');
        tablaDiv.className = 'simplex-table-container';
        tablaDiv.style.marginBottom = '30px';
        tablaDiv.style.background = 'white';
        tablaDiv.style.padding = '15px 10px'; // Reducido padding horizontal para mejor scroll
        tablaDiv.style.borderRadius = '10px';
        tablaDiv.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        // Asegurar que el overflow funcione
        tablaDiv.style.overflowX = 'auto';
        tablaDiv.style.overflowY = 'visible';
        tablaDiv.style.webkitOverflowScrolling = 'touch';
        
        const titulo = document.createElement('h4');
        titulo.textContent = `Iteración ${tablaInfo.iteracion}`;
        titulo.style.color = '#9b59b6';
        titulo.style.borderBottom = '2px solid #9b59b6';
        titulo.style.paddingBottom = '10px';
        titulo.style.marginBottom = '15px';
        tablaDiv.appendChild(titulo);
        
        if (tablaInfo.explicacion) {
            const explicacion = document.createElement('p');
            explicacion.textContent = tablaInfo.explicacion;
            explicacion.style.fontStyle = 'italic';
            explicacion.style.color = '#666';
            explicacion.style.marginBottom = '15px';
            explicacion.style.padding = '10px';
            explicacion.style.background = '#f8f9fa';
            explicacion.style.borderRadius = '5px';
            tablaDiv.appendChild(explicacion);
        }
        
        // Mostrar información sobre variable entrante/saliente si está disponible
        if (tablaInfo.col_entrante !== undefined && tablaInfo.fila_saliente !== undefined) {
            const infoDiv = document.createElement('div');
            infoDiv.style.cssText = 'margin-bottom: 15px; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 5px;';
            const nombresCols = tablaInfo.nombres_columnas || [];
            const varEntrante = nombresCols[tablaInfo.col_entrante] || `Columna ${tablaInfo.col_entrante + 1}`;
            const varSaliente = tablaInfo.variables_basicas && tablaInfo.variables_basicas[tablaInfo.fila_saliente] 
                ? tablaInfo.variables_basicas[tablaInfo.fila_saliente] 
                : `Fila ${tablaInfo.fila_saliente + 1}`;
            
            infoDiv.innerHTML = `
                <strong>🔄 Operación de Pivoteo:</strong><br>
                • <strong>Variable Entrante:</strong> ${varEntrante} (mejora la solución)<br>
                • <strong>Variable Saliente:</strong> ${varSaliente} (sale de la base)<br>
                ${tablaInfo.elemento_pivote !== undefined && tablaInfo.elemento_pivote !== null ? `• <strong>Elemento Pivote:</strong> ${tablaInfo.elemento_pivote.toFixed(4)}` : ''}
            `;
            tablaDiv.appendChild(infoDiv);
        }
        
        // Mostrar ratios si están disponibles
        if (tablaInfo.ratios && tablaInfo.ratios.length > 0) {
            const ratiosDiv = document.createElement('div');
            ratiosDiv.style.cssText = 'margin-bottom: 15px; padding: 12px; background: #d1ecf1; border-left: 4px solid #17a2b8; border-radius: 5px;';
            let ratiosHtml = '<strong>📊 Ratios (Solución ÷ Variable Entrante):</strong><br>';
            tablaInfo.ratios.forEach((ratio, idx) => {
                const varBasica = tablaInfo.variables_basicas && tablaInfo.variables_basicas[idx] 
                    ? tablaInfo.variables_basicas[idx] 
                    : `Fila ${idx + 1}`;
                // Manejar None (null en JSON) como infinito
                const esInfinito = ratio === null || ratio === Infinity || ratio === undefined;
                const ratioStr = esInfinito ? '∞' : ratio.toFixed(4);
                // Filtrar ratios finitos para encontrar el mínimo
                const ratiosFinitos = tablaInfo.ratios.filter(r => r !== null && r !== Infinity && r !== undefined);
                const esMinimo = !esInfinito && ratiosFinitos.length > 0 && ratio === Math.min(...ratiosFinitos);
                ratiosHtml += `• ${varBasica}: ${ratioStr} ${esMinimo ? '<strong style="color: #27ae60;">(Mínimo → Variable Saliente)</strong>' : ''}<br>`;
            });
            ratiosDiv.innerHTML = ratiosHtml;
            tablaDiv.appendChild(ratiosDiv);
        }
        
        // Crear wrapper interno para scroll
        const tableWrapper = document.createElement('div');
        tableWrapper.style.cssText = 'overflow-x: auto; overflow-y: visible; -webkit-overflow-scrolling: touch; margin-top: 15px; width: 100%;';
        
        const tabla = document.createElement('table');
        tabla.className = 'simplex-table';
        tabla.style.width = 'auto'; // Cambiar a auto para que se expanda según contenido
        tabla.style.minWidth = '500px'; // Ancho mínimo
        tabla.style.marginTop = '0';
        tabla.style.borderCollapse = 'collapse';
        tabla.style.fontSize = '0.95em';
        tabla.style.margin = '0 auto'; // Centrar la tabla
        
        // Crear encabezados
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headerRow.style.background = '#9b59b6';
        headerRow.style.color = 'white';
        
        // Columna de variables básicas
        const thVB = document.createElement('th');
        thVB.textContent = 'VB';
        thVB.title = 'Variables Básicas';
        thVB.style.padding = '10px';
        thVB.style.border = '1px solid #ddd';
        thVB.style.textAlign = 'center';
        thVB.style.fontWeight = 'bold';
        headerRow.appendChild(thVB);
        
        // Encabezados de variables
        const numVars = tablaInfo.tabla[0].length - 1;
        const nombresColumnas = tablaInfo.nombres_columnas || [];
        for (let i = 0; i < numVars; i++) {
            const th = document.createElement('th');
            const nombreVar = nombresColumnas[i] || `x${i+1}`;
            th.textContent = nombreVar;
            th.style.padding = '10px';
            th.style.border = '1px solid #ddd';
            th.style.textAlign = 'center';
            th.style.fontWeight = 'bold';
            
            // Resaltar columna entrante (solo si no es la tabla inicial)
            if (tablaInfo.col_entrante !== undefined && tablaInfo.col_entrante !== null && 
                tablaInfo.col_entrante === i) {
                th.style.background = '#ffc107';
                th.style.color = '#000';
                th.title = 'Variable Entrante';
            }
            
            headerRow.appendChild(th);
        }
        
        // Encabezado de solución
        const thSol = document.createElement('th');
        thSol.textContent = 'Solución';
        thSol.title = 'Valores de las variables básicas y Z';
        thSol.style.padding = '10px';
        thSol.style.border = '1px solid #ddd';
        thSol.style.textAlign = 'center';
        thSol.style.fontWeight = 'bold';
        headerRow.appendChild(thSol);
        
        thead.appendChild(headerRow);
        tabla.appendChild(thead);
        
        // Crear cuerpo
        const tbody = document.createElement('tbody');
        const numFilas = tablaInfo.tabla.length - 1; // Excluir fila Z
        
        tablaInfo.tabla.forEach((fila, filaIdx) => {
            const tr = document.createElement('tr');
            // Z está ahora en la primera fila (índice 0), no en la última
            const esFilaZ = filaIdx === 0;
            
            if (esFilaZ) {
                tr.style.background = '#e8d5f2';
                tr.style.fontWeight = 'bold';
            } else {
                // Resaltar fila saliente
                // Las restricciones están en índices 1 a num_rest, así que fila_saliente corresponde a filaIdx - 1
                if (tablaInfo.fila_saliente !== undefined && tablaInfo.fila_saliente !== null && 
                    tablaInfo.fila_saliente === filaIdx - 1) {
                    tr.style.background = '#fff3cd';
                }
            }
            
            // Columna de variable básica
            const tdVB = document.createElement('td');
            if (esFilaZ) {
                tdVB.textContent = 'Z';
                tdVB.style.fontWeight = 'bold';
            } else {
                // Las variables básicas están indexadas desde 0, pero las restricciones empiezan en filaIdx 1
                const idxVarBasica = filaIdx - 1;  // Ajustar índice porque Z está en 0
                const varBasica = tablaInfo.variables_basicas && idxVarBasica >= 0 && 
                    idxVarBasica < tablaInfo.variables_basicas.length
                    ? tablaInfo.variables_basicas[idxVarBasica] 
                    : '-';
                tdVB.textContent = varBasica;
                tdVB.style.fontWeight = 'bold';
                tdVB.style.color = '#9b59b6';
            }
            tdVB.style.padding = '8px';
            tdVB.style.border = '1px solid #ddd';
            tdVB.style.textAlign = 'center';
            tdVB.style.background = esFilaZ ? '#e8d5f2' : '#f8f9fa';
            tr.appendChild(tdVB);
            
            // Valores de la fila
            fila.forEach((valor, colIdx) => {
                const td = document.createElement('td');
                td.textContent = valor.toFixed(4);
                td.style.padding = '8px';
                td.style.border = '1px solid #ddd';
                td.style.textAlign = 'center';
                
                // Resaltar columna de solución
                if (colIdx === numVars) {
                    td.style.background = '#f0f0f0';
                    td.style.fontWeight = 'bold';
                }
                
                // Resaltar elemento pivote
                // Las restricciones están en índices 1 a num_rest, así que fila_saliente corresponde a filaIdx - 1
                if (tablaInfo.fila_saliente !== undefined && tablaInfo.fila_saliente !== null &&
                    tablaInfo.fila_saliente === filaIdx - 1 && tablaInfo.col_entrante === colIdx && 
                    tablaInfo.elemento_pivote !== undefined && tablaInfo.elemento_pivote !== null) {
                    td.style.background = '#ffc107';
                    td.style.color = '#000';
                    td.style.fontWeight = 'bold';
                    td.style.border = '3px solid #ff9800';
                    td.title = `Elemento Pivote: ${tablaInfo.elemento_pivote.toFixed(4)}`;
                }
                
                // Resaltar columna entrante (solo en filas de restricciones, no en Z)
                if (tablaInfo.col_entrante === colIdx && !esFilaZ) {
                    td.style.background = '#fff3cd';
                }
                
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        tabla.appendChild(tbody);
        // Agregar tabla al wrapper y wrapper al contenedor
        tableWrapper.appendChild(tabla);
        tablaDiv.appendChild(tableWrapper);
        container.appendChild(tablaDiv);
    });
}

// Mostrar solución final del Simplex
function mostrarSolucionSimplex(datos) {
    const titulo = document.getElementById('titulo-tipo-solucion-simplex');
    const explicacion = document.getElementById('texto-explicacion-simplex');
    const cajaFinal = document.getElementById('caja-resultado-final-simplex');
    
    titulo.textContent = datos.tipo_solucion || "Resultado";
    explicacion.textContent = datos.explicacion || "Analizando...";
    
    if (datos.status === 'infeasible') {
        titulo.style.color = "#e74c3c";
        document.getElementById('analisis-box-simplex').style.borderLeftColor = "#e74c3c";
        cajaFinal.innerHTML = "No hay solución factible";
    } else if (datos.status === 'unbounded') {
        titulo.style.color = "#e67e22";
        document.getElementById('analisis-box-simplex').style.borderLeftColor = "#e67e22";
        cajaFinal.innerHTML = "Problema no acotado";
    } else {
        titulo.style.color = "#27ae60";
        document.getElementById('analisis-box-simplex').style.borderLeftColor = "#27ae60";
        
        let solucionHtml = `Valor Óptimo Z = <strong>${datos.z_optimo.toFixed(4)}</strong><br>`;
        solucionHtml += `<div style="margin-top: 10px;">`;
        datos.solucion.forEach((val, idx) => {
            solucionHtml += `x<sub>${idx+1}</sub> = ${val.toFixed(4)}<br>`;
        });
        solucionHtml += `</div>`;
        cajaFinal.innerHTML = solucionHtml;
    }
}

// Cambiar entre modos de entrada de restricciones para Simplex
function cambiarModoRestriccionesSimplex(modo) {
    const modoCoef = document.getElementById('modo-coeficientes-simplex');
    const modoNatural = document.getElementById('modo-natural-simplex');
    
    // Actualizar botones activos
    const botones = document.querySelectorAll('.restriction-mode-btn-simplex');
    botones.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-mode') === modo) {
            btn.classList.add('active');
        }
    });
    
    if (modo === 'coeficientes') {
        modoCoef.style.display = 'block';
        modoNatural.style.display = 'none';
    } else {
        modoCoef.style.display = 'none';
        modoNatural.style.display = 'block';
    }
}

// Convertir restricciones naturales a coeficientes para Simplex
async function convertirRestriccionesNaturalesSimplex() {
    const textarea = document.getElementById('restricciones-natural-simplex');
    const texto = textarea.value.trim();
    
    if (!texto) {
        alert('Por favor, ingresa al menos una restricción.');
        return;
    }
    
    // Obtener número de variables del objetivo
    const numVars = obtenerNumVariables();
    if (numVars === 0) {
        alert('Error: Primero debes definir al menos una variable en la función objetivo.');
        return;
    }
    
    // Dividir por líneas y limpiar
    const restricciones = texto.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0);
    
    if (restricciones.length === 0) {
        alert('No se encontraron restricciones válidas.');
        return;
    }
    
    try {
        // Llamar al endpoint de conversión para Simplex (necesitamos crearlo)
        const respuesta = await fetch('/convertir-restricciones-simplex', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                restricciones: restricciones,
                num_variables: numVars
            })
        });
        
        const datos = await respuesta.json();
        
        if (datos.status === 'error') {
            alert(`Error al convertir restricciones: ${datos.message}`);
            return;
        }
        
        // Limpiar restricciones existentes
        const container = document.getElementById('lista-restricciones-simplex');
        container.innerHTML = '';
        
        // Agregar restricciones convertidas
        datos.restricciones.forEach(rest => {
            agregarRestriccionSimplexDesdeDatos(rest, numVars);
        });
        
        // Cambiar a modo coeficientes y mostrar
        cambiarModoRestriccionesSimplex('coeficientes');
        
        // Mostrar mensaje de éxito
        const mensaje = document.createElement('div');
        mensaje.style.cssText = 'margin-top: 10px; padding: 10px; background: #d4edda; color: #155724; border-radius: 4px;';
        mensaje.textContent = `✓ ${datos.restricciones.length} restricción(es) convertida(s) exitosamente.`;
        container.parentElement.insertBefore(mensaje, container.nextSibling);
        
        // Remover mensaje después de 3 segundos
        setTimeout(() => {
            mensaje.remove();
        }, 3000);
        
    } catch (error) {
        alert(`Error al convertir restricciones: ${error.message}`);
    }
}

// Agregar restricción desde datos ya convertidos (para Simplex)
function agregarRestriccionSimplexDesdeDatos(datos, numVars) {
    const container = document.getElementById('lista-restricciones-simplex');
    
    const nuevaFila = document.createElement('div');
    nuevaFila.className = 'fila-restriccion-simplex';
    
    let html = '';
    for (let i = 0; i < numVars; i++) {
        const coef = datos.coefs[i] || 0;
        const subindice = numeroASubindice(i + 1);
        const absCoef = Math.abs(coef);
        
        if (i === 0) {
            html += `<input type="number" class="res-coef" value="${absCoef}" style="width: 50px;" data-var="${i}" inputmode="decimal" autocomplete="off"> X${subindice} `;
        } else {
            const signo = coef >= 0 ? '+' : '-';
            html += `<select class="res-op-var-simplex" data-var="${i-1}" style="width: 50px; margin: 0 5px; padding: 4px; text-align: center; font-size: 1em;">
                <option value="+" ${signo === '+' ? 'selected' : ''}>+</option>
                <option value="-" ${signo === '-' ? 'selected' : ''}>-</option>
            </select>`;
            html += `<input type="number" class="res-coef" value="${absCoef}" style="width: 50px;" data-var="${i}" inputmode="decimal" autocomplete="off"> X${subindice} `;
        }
    }
    
    html += `
        <select class="res-op-simplex">
            <option value="<=" ${datos.op === '<=' ? 'selected' : ''}>&le;</option>
            <option value=">=" ${datos.op === '>=' ? 'selected' : ''}>&ge;</option>
            <option value="=" ${datos.op === '=' ? 'selected' : ''}>=</option>
        </select>
        <input type="number" class="res-val-simplex" value="${datos.val}" style="width: 60px;" inputmode="decimal" autocomplete="off">
    `;
    
    nuevaFila.innerHTML = html;
    container.appendChild(nuevaFila);
}

// Toggle para cálculos Simplex
function toggleCalculationsSimplex() {
    const logContainer = document.getElementById('log-container-simplex');
    const summaryDiv = document.getElementById('calculations-summary-simplex');
    const toggleBtn = document.getElementById('toggle-calculations-simplex');
    const isHidden = logContainer.style.display === 'none' || logContainer.style.display === '';
    
    if (isHidden) {
        logContainer.style.display = 'block';
        summaryDiv.style.display = 'none';
        toggleBtn.innerHTML = '<span id="toggle-icon-simplex">▲</span> Ocultar Detalles';
    } else {
        logContainer.style.display = 'none';
        summaryDiv.style.display = 'block';
        toggleBtn.innerHTML = '<span id="toggle-icon-simplex">▼</span> Ver Detalles';
    }
}

// Inicialización cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    // Verificar que todos los elementos necesarios existan
    try {
        // Asegurar que el método gráfico esté visible por defecto
        const metodoGrafico = document.getElementById('metodo-grafico');
        const metodoSimplex = document.getElementById('metodo-simplex');
        
        if (!metodoGrafico) {
            console.error('Error: No se encontró el elemento metodo-grafico');
            return;
        }
        
        if (!metodoSimplex) {
            console.error('Error: No se encontró el elemento metodo-simplex');
            return;
        }
        
        // Asegurar estado inicial correcto
        metodoGrafico.style.display = 'block';
        metodoSimplex.style.display = 'none';
        
        // Ocultar resultados inicialmente
        const resultadosGrafico = document.getElementById('resultados');
        const resultadosSimplex = document.getElementById('resultados-simplex');
        if (resultadosGrafico) resultadosGrafico.style.display = 'none';
        if (resultadosSimplex) resultadosSimplex.style.display = 'none';
        
        // Verificar que las funciones críticas existan
        if (typeof cambiarMetodo !== 'function') {
            console.error('Error: función cambiarMetodo no está definida');
        }
        if (typeof agregarRestriccionSimplex !== 'function') {
            console.error('Error: función agregarRestriccionSimplex no está definida');
        }
        if (typeof resolverProblema !== 'function') {
            console.error('Error: función resolverProblema no está definida');
        }
        if (typeof resolverSimplex !== 'function') {
            console.error('Error: función resolverSimplex no está definida');
        }
        
        // Responsive Plotly: resize chart on viewport/orientation change (Checkpoint 2)
        let resizeTimeout;
        function debouncedPlotlyResize() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function() {
                const el = document.getElementById('grafico');
                if (el && el.querySelector('.js-plotly-plot') && typeof Plotly !== 'undefined') {
                    try { Plotly.Plots.resize('grafico'); } catch (e) { /* ignore */ }
                }
            }, 150);
        }
        window.addEventListener('resize', debouncedPlotlyResize);
        window.addEventListener('orientationchange', debouncedPlotlyResize);

        console.log('Aplicación cargada correctamente');
    } catch (error) {
        console.error('Error durante la inicialización:', error);
        alert('Error al cargar la aplicación. Por favor, recarga la página. Error: ' + error.message);
    }
});

// ========================================
// DARK MODE FUNCTIONALITY
// ========================================

/**
 * Initialize dark mode based on user preference or system preference
 */
function initDarkMode() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Determine initial theme
    let theme = 'light';
    if (savedTheme) {
        theme = savedTheme;
    } else if (prefersDark) {
        theme = 'dark';
    }
    
    // Apply theme
    applyTheme(theme);
    
    // Listen for system theme changes (only if no saved preference)
    if (!savedTheme) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            applyTheme(e.matches ? 'dark' : 'light');
        });
    }
}

/**
 * Apply the specified theme
 * @param {string} theme - 'light' or 'dark'
 */
function applyTheme(theme) {
    const html = document.documentElement;
    const toggleButton = document.getElementById('dark-mode-toggle');
    const icon = document.getElementById('dark-mode-icon');
    
    if (theme === 'dark') {
        html.setAttribute('data-theme', 'dark');
        if (icon) icon.textContent = '☀️';
        if (toggleButton) toggleButton.setAttribute('title', 'Cambiar a modo claro');
    } else {
        html.setAttribute('data-theme', 'light');
        if (icon) icon.textContent = '🌙';
        if (toggleButton) toggleButton.setAttribute('title', 'Cambiar a modo oscuro');
    }
    
    // Save preference
    localStorage.setItem('theme', theme);
    
    // Update Plotly charts if they exist
    updatePlotlyCharts(theme);
}

/**
 * Toggle between light and dark mode
 */
function toggleDarkMode() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

/**
 * Update Plotly charts to match the current theme
 * @param {string} theme - 'light' or 'dark'
 */
function updatePlotlyCharts(theme) {
    const plotlyDivs = document.querySelectorAll('.js-plotly-plot');
    plotlyDivs.forEach(div => {
        if (div.data && Plotly) {
            const layout = div.layout || {};
            const bgColor = theme === 'dark' ? '#1a1a1a' : '#ffffff';
            const textColor = theme === 'dark' ? '#e0e0e0' : '#333';
            const gridColor = theme === 'dark' ? '#444' : '#ddd';
            
            Plotly.relayout(div, {
                'plot_bgcolor': bgColor,
                'paper_bgcolor': bgColor,
                'font.color': textColor,
                'xaxis.gridcolor': gridColor,
                'yaxis.gridcolor': gridColor,
                'xaxis.linecolor': gridColor,
                'yaxis.linecolor': gridColor,
                'xaxis.zerolinecolor': gridColor,
                'yaxis.zerolinecolor': gridColor
            });
        }
    });
}

// Initialize dark mode when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDarkMode);
} else {
    initDarkMode();
}

// Add event listener to toggle button
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('dark-mode-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleDarkMode);
    }
});

