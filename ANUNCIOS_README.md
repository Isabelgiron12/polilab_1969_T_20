# 🎙️ Sistema de Anuncios - Caja Negra

## ✅ Integración Completada

El módulo de **Text-to-Speech** (TTS) está completamente integrado en el juego.

### Archivos:
- **`anuncios.js`** — Módulo principal (en raíz y en `polilab_1969_T_20/`)
- **`demo-anuncios.html`** — Interfaz de prueba interactiva
- **`polilab_1969_T_20/index.html`** — Juego con anuncios integrados

---

## 🎤 Frases Disponibles

### Inicio y Fin
```javascript
Anuncios.decir('bienvenida');
// "Bienvenidos a la sala de control. Prepárense para la misión."

Anuncios.decir('inicioConteo');
// "Iniciando cuenta regresiva para el lanzamiento."

Anuncios.decir('lanzamiento');
// "Lanzamiento en progreso. Todos a posiciones de seguridad."

Anuncios.decir('misionTerminada');
// "Misión completada. Equipo, regresen a la sala de control."

Anuncios.decir('misionFallida');
// "Se ha abortado la misión. Análisis de contingencia en progreso."
```

### Fases del Juego
```javascript
Anuncios.decir('faseNuevaLlegada');
// "Nueva fase iniciada. Detectado evento de nave llegando."

Anuncios.decir('faseReunion');
// "Fase de reunión de equipo. Todos a la sala principal."

Anuncios.decir('faseDecision');
// "Es momento crítico. Se requiere toma de decisión del equipo."

Anuncios.decir('faseMiniJuego');
// "Activando mini desafío. Todos al área de entrenamiento."

Anuncios.decir('faseReflexion');
// "Fase de reflexión. Registren sus observaciones."
```

### Eventos y Alertas
```javascript
Anuncios.decir('tripulanteElimina', 'Juan');
// "Alerta: Juan ha sido removido del equipo."

Anuncios.decir('tripulanteAprobado', 'María');
// "María ha cumplido objetivos satisfactoriamente."

Anuncios.decir('decisionGO');
// "Decisión: GO. Procediendo con envío."

Anuncios.decir('decisionNOGO');
// "Decisión: NO GO. Abortando envío."
```

---

## 🔌 Integración en el Juego

### Funciones donde están los Anuncios:

1. **`startMission()`** 
   - Anuncio: `'bienvenida'`
   - Se dispara cuando inicia la misión

2. **`confirmLaunchDecision()`** 
   - Anuncio: `'decisionGO'`
   - Se dispara al confirmar lanzamiento

3. **`decisionNOGO()`** (nueva función)
   - Anuncio: `'decisionNOGO'`
   - Se dispara al cancelar lanzamiento

4. **`advanceNow()`** 
   - Anuncio: depende del tipo de fase
   - Se dispara al avanzar entre fases

5. **`finishNow()`** 
   - Anuncio: `'misionTerminada'`
   - Se dispara al terminar el juego

6. **`tttRetry()`** 
   - Anuncio: `'faseMiniJuego'`
   - Se dispara cuando se reinicia el minijuego

---

## 🎯 Uso Manual

Puedes añadir anuncios en cualquier parte del código:

```javascript
// Anuncio simple
Anuncios.anunciar("El equipo debe reunirse en 5 minutos");

// Anuncio con parámetros
Anuncios.decir('tripulanteElimina', 'Carlos López');

// Detener un anuncio
Anuncios.detener();

// Personalizar configuración
Anuncios.config.rate = 1.2;      // velocidad
Anuncios.config.volume = 0.8;    // volumen (0-1)
Anuncios.config.pitch = 1.1;     // tono (0.5-2)
```

---

## 🧪 Probar los Anuncios

### Opción 1: Demo Interactiva
```bash
# Abre demo-anuncios.html en el navegador
# Botones para cada anuncio + personalizados
```

### Opción 2: En la Consola del Navegador
```javascript
// En las DevTools (F12)
Anuncios.decir('bienvenida');
Anuncios.anunciar('Prueba de anuncio personalizado');
```

### Opción 3: Durante el Juego
- Inicia el juego
- Los anuncios se disparan automáticamente en eventos clave
- Abre DevTools (F12) → Console para ver logs

---

## 📝 Notas Técnicas

- **Lenguaje**: Español (es-ES) por defecto
- **API**: Web Speech API nativa (funciona en Chrome, Edge, Safari)
- **Compatibilidad**: Todos los navegadores modernos
- **Fallback**: Si el navegador no soporta TTS, no falla (es opcional)
- **Guardias**: Usa `Anuncios?.decir?.()` para evitar errores

---

## 🚀 Próximos Pasos

1. **Agregar más frases** según eventos específicos del juego
2. **Personalizar voces** según género/tipo de personaje
3. **Integrar con sonido** (música de fondo + anuncios)
4. **Permite que usuarios graben sus propias frases** (si lo deseas)

---

## 📞 Soporte

Si quieres agregar más frases o cambiar cómo funcionan los anuncios, edita:
- `anuncios.js` → Módulo principal
- `polilab_1969_T_20/index.html` → Dónde se disparan
