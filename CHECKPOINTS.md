# 📋 Checkpoints: Mejoras de UX/UI y Funcionalidad

Este documento contiene los checkpoints paso a paso para mejorar la aplicación de Programación Lineal.

---

## 🎨 Mejoras de UX/UI

### Checkpoint 1: Implementar Dark Mode ✅

- [x] **Analizar la estructura actual de CSS**
  - [x] Revisar `static/css/style.css` para entender el sistema de colores actual
  - [x] Identificar todos los elementos que necesitan adaptarse al modo oscuro
  - [x] Determinar la estrategia de implementación (CSS variables vs clases)

- [x] **Definir paleta de colores para Dark Mode**
  - [x] Seleccionar colores de fondo oscuros (#1a1a1a, #2d2d2d, etc.)
  - [x] Seleccionar colores de texto claros (#ffffff, #e0e0e0, etc.)
  - [x] Ajustar colores de acentos y botones para buen contraste
  - [x] Documentar la paleta en comentarios del CSS

- [x] **Implementar toggle de Dark Mode**
  - [x] Agregar botón/interruptor en la interfaz para cambiar entre modos
  - [x] Guardar preferencia del usuario en `localStorage`
  - [x] Detectar preferencia del sistema del usuario (`prefers-color-scheme`)
  - [x] Aplicar modo oscuro por defecto según preferencia del sistema

- [x] **Aplicar estilos Dark Mode a todos los componentes**
  - [x] Body y contenedores principales
  - [x] Tabs y botones
  - [x] Campos de entrada (inputs)
  - [x] Tablas y resultados
  - [x] Gráficos y visualizaciones
  - [x] Mensajes de error y validación
  - [x] Modales y popups (si existen)

- [x] **Probar transiciones suaves**
  - [x] Implementar transiciones CSS para cambio de tema
  - [x] Verificar que no hay parpadeos durante el cambio
  - [x] Asegurar que los gráficos se actualizan correctamente

- [x] **Validar contraste y accesibilidad**
  - [x] Verificar que todos los textos cumplen con WCAG AA (contraste mínimo 4.5:1)
  - [x] Probar con herramientas de accesibilidad
  - [x] Ajustar colores si es necesario para mejorar legibilidad

---

### Checkpoint 2: Mantener Responsividad (Mobile-First) ✅

- [x] **Revisar diseño actual en móviles**
  - [x] Probar en diferentes tamaños de viewport (320px, 375px, 414px, etc.)
  - [x] Identificar elementos que se rompen o no se adaptan bien
  - [x] Documentar problemas encontrados

- [x] **Optimizar navegación en móvil**
  - [x] Verificar que los tabs son fáciles de usar en pantallas táctiles
  - [x] Asegurar tamaño mínimo de área táctil (44x44px)
  - [x] Optimizar espaciado entre elementos interactivos

- [x] **Ajustar formularios para móvil**
  - [x] Verificar que los inputs son cómodos de usar en móvil
  - [x] Optimizar teclado virtual (usar tipos de input apropiados)
  - [x] Mejorar espaciado vertical entre campos
  - [x] Asegurar que los botones son accesibles sin scroll

- [x] **Optimizar gráficos para móvil**
  - [x] Verificar que los gráficos se adaptan correctamente al tamaño de pantalla
  - [x] Asegurar que los controles del gráfico son táctiles
  - [x] Optimizar para orientación horizontal y vertical

- [x] **Probar en dispositivos reales**
  - [x] iOS Safari
  - [x] Chrome Android
  - [x] Firefox Mobile
  - [x] Probar diferentes tamaños de pantalla

- [x] **Ajustar Dark Mode para móvil**
  - [x] Verificar que el toggle de dark mode es accesible en móvil
  - [x] Asegurar que los colores se ven bien en pantallas pequeñas

**Notas (Checkpoint 2):** Breakpoints en `style.css`: 360px, 480px, 768px, 896px (landscape). Touch targets ≥44×44px; `touch-action: manipulation` en táctiles. Inputs con `inputmode="decimal"`. Plotly con `responsive: true`, `autosize: true` y resize en `resize`/`orientationchange`. Toggle dark mode fijo; `padding-right` en body en móvil para no solaparse con el título. Tablas Simplex y de vértices con scroll horizontal en móvil. Variables CSS en media queries para Dark Mode en móvil.

---

## 💾 Persistencia de Datos

### Checkpoint 3: Implementar Persistencia de Datos entre Métodos

- [ ] **Analizar flujo actual de datos**
  - [ ] Revisar cómo se manejan los datos en el frontend (`static/js/main.js`)
  - [ ] Identificar dónde se pierden los datos al cambiar de método
  - [ ] Documentar el flujo actual de datos

- [ ] **Diseñar sistema de almacenamiento**
  - [ ] Decidir estrategia: `localStorage`, `sessionStorage`, o estado en memoria
  - [ ] Definir estructura de datos a persistir:
    - [ ] Función objetivo (coeficientes, tipo: max/min)
    - [ ] Restricciones (coeficientes, operador, valor)
    - [ ] Configuraciones del usuario

- [ ] **Implementar guardado automático**
  - [ ] Guardar función objetivo cuando el usuario la ingresa
  - [ ] Guardar cada restricción cuando se agrega o modifica
  - [ ] Guardar preferencias de método seleccionado

- [ ] **Implementar restauración de datos**
  - [ ] Cargar datos guardados al cambiar de método
  - [ ] Cargar datos guardados al recargar la página
  - [ ] Mantener datos activos durante toda la sesión

- [ ] **Manejar sincronización de estado**
  - [ ] Asegurar que ambos métodos (Gráfico y Simplex) comparten los mismos datos
  - [ ] Actualizar ambos formularios cuando se cambia un dato
  - [ ] Mantener consistencia visual entre métodos

- [ ] **Probar persistencia**
  - [ ] Ingresar datos en método Gráfico
  - [ ] Cambiar a método Simplex y verificar que los datos están presentes
  - [ ] Cambiar de vuelta a Gráfico y verificar que los datos persisten
  - [ ] Recargar la página y verificar que los datos se mantienen

---

## 🔄 Flujo de Usuario Mejorado

### Checkpoint 4: Reorganizar Flujo - Input Primero, Método Después

- [ ] **Analizar estructura actual de la interfaz**
  - [ ] Revisar `templates/index.html` para entender el layout actual
  - [ ] Identificar cómo está organizado el flujo actual (tabs de métodos primero)
  - [ ] Documentar el flujo actual vs el flujo deseado

- [ ] **Rediseñar la estructura de la página**
  - [ ] Mover sección de función objetivo al principio (antes de elegir método)
  - [ ] Mover sección de restricciones después de función objetivo
  - [ ] Colocar selección de método después de ingresar datos
  - [ ] Asegurar que el diseño sigue siendo responsive

- [ ] **Implementar validaciones paso a paso**
  - [ ] Validar función objetivo antes de permitir agregar restricciones
    - [ ] Verificar que hay coeficientes válidos
    - [ ] Verificar que hay tipo seleccionado (max/min)
  - [ ] Validar que hay al menos una restricción antes de habilitar métodos
  - [ ] Mostrar mensajes de error claros y útiles

- [ ] **Habilitar/deshabilitar métodos dinámicamente**
  - [ ] Deshabilitar tabs de métodos hasta que los datos sean válidos
  - [ ] Mostrar indicadores visuales de qué falta completar
  - [ ] Habilitar métodos gradualmente según datos disponibles

- [ ] **Mejorar mensajes de guía al usuario**
  - [ ] Agregar texto de ayuda: "Primero ingresa la función objetivo"
  - [ ] Agregar texto: "Luego agrega tus restricciones"
  - [ ] Agregar texto: "Finalmente, selecciona un método para resolver"
  - [ ] Usar iconos o números para indicar el orden (1, 2, 3)

- [ ] **Probar el nuevo flujo**
  - [ ] Intentar seleccionar método sin datos → debe estar deshabilitado
  - [ ] Ingresar función objetivo → verificar validaciones
  - [ ] Agregar restricciones → verificar que se guardan
  - [ ] Seleccionar método → verificar que funciona con datos ingresados
  - [ ] Cambiar método → verificar que los datos persisten

---

## 📝 Sistema de Log de Operaciones

### Checkpoint 5: Implementar Log Temporal de Operaciones

- [ ] **Diseñar estructura del log**
  - [ ] Definir qué información guardar:
    - [ ] Función objetivo usada
    - [ ] Restricciones aplicadas
    - [ ] Método utilizado
    - [ ] Resultados obtenidos
    - [ ] Timestamp de la operación
  - [ ] Decidir formato de almacenamiento (JSON en localStorage)
  - [ ] Definir límite de operaciones a guardar (ej: últimas 10)

- [ ] **Crear interfaz para mostrar historial**
  - [ ] Diseñar botón/icono para mostrar/ocultar historial
  - [ ] Crear panel lateral o modal para mostrar el log
  - [ ] Diseñar tarjetas o lista para cada operación previa
  - [ ] Asegurar que es responsive y funciona en móvil

- [ ] **Implementar guardado de operaciones**
  - [ ] Guardar operación después de calcular solución exitosamente
  - [ ] Asignar ID único a cada operación
  - [ ] Mantener solo las últimas N operaciones (eliminar las más antiguas)
  - [ ] Guardar en localStorage con clave identificable

- [ ] **Implementar visualización del log**
  - [ ] Mostrar lista de operaciones previas
  - [ ] Mostrar función objetivo de cada operación
  - [ ] Mostrar número de restricciones
  - [ ] Mostrar método usado
  - [ ] Mostrar fecha/hora de la operación
  - [ ] Mostrar resultado (opcional, resumido)

- [ ] **Implementar funcionalidad de restaurar**
  - [ ] Agregar botón "Usar" o "Restaurar" en cada entrada del log
  - [ ] Al hacer clic, restaurar datos de esa operación al formulario
  - [ ] Actualizar interfaz con los datos restaurados
  - [ ] Permitir calcular de nuevo con esos datos

- [ ] **Implementar funcionalidad de eliminar**
  - [ ] Agregar botón para eliminar una operación específica del log
  - [ ] Agregar opción para limpiar todo el historial
  - [ ] Confirmar antes de eliminar (especialmente si es todo el historial)

- [ ] **Hacer el log opcional/colapsable**
  - [ ] Ocultar por defecto
  - [ ] Botón para mostrar/ocultar
  - [ ] Animación suave al mostrar/ocultar
  - [ ] Guardar preferencia de mostrar/ocultar en localStorage

- [ ] **Probar funcionalidad completa**
  - [ ] Realizar varias operaciones
  - [ ] Verificar que todas se guardan
  - [ ] Abrir log y verificar que se muestran correctamente
  - [ ] Restaurar una operación anterior
  - [ ] Verificar que los datos se cargan correctamente
  - [ ] Eliminar una operación y verificar que desaparece
  - [ ] Limpiar todo el historial y verificar que se vacía

---

## ✅ Validaciones Adicionales

### Checkpoint 6: Mejorar Validaciones del Sistema

- [ ] **Validaciones de función objetivo**
  - [ ] Verificar que los coeficientes son números válidos
  - [ ] Permitir números negativos si corresponde
  - [ ] Verificar que no todos los coeficientes son cero
  - [ ] Validar formato de entrada (permitir decimales)

- [ ] **Validaciones de restricciones**
  - [ ] Verificar que los coeficientes son números válidos
  - [ ] Verificar que hay un operador seleccionado
  - [ ] Verificar que el valor de la restricción es numérico
  - [ ] Validar que no hay restricciones duplicadas
  - [ ] Verificar que hay al menos una restricción antes de calcular

- [ ] **Validaciones antes de calcular**
  - [ ] Función objetivo válida
  - [ ] Al menos una restricción válida
  - [ ] Método seleccionado
  - [ ] Mostrar mensajes de error específicos si algo falta

- [ ] **Validaciones durante el cálculo**
  - [ ] Manejar errores matemáticos (división por cero, etc.)
  - [ ] Mostrar mensajes de error claros al usuario
  - [ ] No romper la interfaz si hay un error

- [ ] **Probar todas las validaciones**
  - [ ] Probar casos límite
  - [ ] Probar entradas inválidas
  - [ ] Probar casos de error
  - [ ] Verificar que los mensajes son claros y útiles

---

## 🧪 Testing y Verificación Final

### Checkpoint 7: Testing Completo

- [ ] **Testing de Dark Mode**
  - [ ] Probar cambio entre modos
  - [ ] Verificar que se guarda la preferencia
  - [ ] Probar en diferentes navegadores
  - [ ] Verificar que los gráficos se adaptan correctamente

- [ ] **Testing de Responsividad**
  - [ ] Probar en viewports móviles (320px - 768px)
  - [ ] Probar en tablets (768px - 1024px)
  - [ ] Probar en desktop (> 1024px)
  - [ ] Probar en diferentes orientaciones (portrait/landscape)

- [ ] **Testing de Persistencia**
  - [ ] Ingresar datos y cambiar de método varias veces
  - [ ] Recargar la página y verificar que los datos persisten
  - [ ] Probar con diferentes combinaciones de datos
  - [ ] Verificar que no se pierden datos inesperadamente

- [ ] **Testing de Flujo de Usuario**
  - [ ] Seguir el flujo completo desde cero
  - [ ] Intentar saltarse pasos (debe estar bloqueado)
  - [ ] Verificar que las validaciones funcionan correctamente
  - [ ] Verificar que los mensajes de guía son claros

- [ ] **Testing del Log de Operaciones**
  - [ ] Realizar múltiples operaciones
  - [ ] Verificar que se guardan correctamente
  - [ ] Restaurar diferentes operaciones
  - [ ] Eliminar operaciones y verificar
  - [ ] Verificar límite de operaciones guardadas

- [ ] **Testing Cross-Browser**
  - [ ] Chrome/Edge
  - [ ] Firefox
  - [ ] Safari
  - [ ] Navegadores móviles

- [ ] **Testing de Performance**
  - [ ] Verificar que la carga inicial es rápida
  - [ ] Verificar que el cambio de modo oscuro es instantáneo
  - [ ] Verificar que el guardado/restauración es rápido
  - [ ] Optimizar si es necesario

---

## 📝 Notas Finales

- **Prioridad sugerida**: 
  1. Persistencia de datos (Checkpoint 3) - Esencial para buena UX
  2. Flujo de usuario mejorado (Checkpoint 4) - Mejora significativa
  3. Dark Mode (Checkpoint 1) - Mejora visual importante
  4. Log de operaciones (Checkpoint 5) - Funcionalidad adicional
  5. Validaciones (Checkpoint 6) - Ya debería estar parcialmente implementado

- **Consideraciones técnicas**:
  - Usar `localStorage` para persistencia (es más simple que sessionStorage)
  - Considerar usar CSS variables para facilitar el cambio de tema
  - Mantener el código modular y fácil de mantener
  - Documentar cambios importantes en el código

- **Recursos útiles**:
  - [MDN: prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
  - [MDN: localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
  - [WCAG Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

---

**¡Buena suerte con las mejoras! 🚀**

