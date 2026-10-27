# 📢 Anuncios de Dirección - Modo Crítico

## ¿Cuándo Usar?

Cuando aparezca un **anuncio o instrucción de la dirección** que sea importante que todos escuchen.

---

## 🎤 Ejemplos de Uso

### 1. Anuncio crítico simple
```javascript
// Cuando aparezca una directiva importante
Anuncios.anuncioCritico('direccionCritica');
// → "ATENCIÓN. Comunicado importante de la dirección. Todos deben escuchar."
```

### 2. Con instrucción específica
```javascript
// Cuando la dirección da una orden
Anuncios.anuncioCritico('direccionInstruccion', 'todos deben reportar a la sala principal');
// → "Directiva de la dirección: todos deben reportar a la sala principal. Cumplimiento obligatorio."
```

### 3. Con cambio de directriz
```javascript
// Cuando cambia algo importante
Anuncios.anuncioCritico('direccionCambio', 'se suspende la misión por razones de seguridad');
// → "Cambio de directriz de la dirección. se suspende la misión por razones de seguridad. Acaten inmediatamente."
```

### 4. Con decisión importante
```javascript
// Anunciar una decisión de dirección
Anuncios.anuncioCritico('direccionDecision', 'el equipo fue promovido por su desempeño');
// → "La dirección ha tomado una decisión. el equipo fue promovido por su desempeño. Todos deben conocerla."
```

---

## 🔊 Características del Anuncio Crítico

✅ **Acento Latino** (español de México)
✅ **Más lento** (0.85x velocidad) → Mayor énfasis
✅ **Tono ligeramente más alto** (1.1)
✅ **Volumen máximo** (100%)
✅ **Pausa antes de hablar** (300ms)

---

## 🎯 Dónde Integrarlo

En el juego, agrega esto cuando aparezca dirección:

```javascript
// En la función donde se muestre el anuncio de dirección
if(esAnuncioDirección) {
  // Trigger del anuncio crítico
  Anuncios.anuncioCritico('direccionCritica');
  
  // O con parámetro:
  Anuncios.anuncioCritico('direccionInstruccion', textoEspecifico);
}
```

---

## 📝 Frases Disponibles

| Clave | Parámetros | Ejemplo |
|-------|-----------|---------|
| `direccionCritica` | — | Comunicado importante de la dirección |
| `direccionLlamado` | — | Requiere atención inmediata |
| `direccionInstruccion` | texto | Directiva: [texto]. Cumplimiento obligatorio. |
| `direccionAviso` | aviso | Aviso urgente: [aviso] |
| `direccionDecision` | decision | La dirección ha tomado: [decision] |
| `direccionCambio` | cambio | Cambio de directriz: [cambio]. Acaten. |

---

## 🌍 Cambiar Acento

Para cambiar de **Latino (México)** a **Español (España)**:

```javascript
// Temporalmente
Anuncios.config.lang = 'es-ES';
Anuncios.anuncioCritico('direccionCritica');

// O permanentemente
Anuncios.config = Anuncios.configEspañol;
```

---

## 💡 Ejemplo Completo

```javascript
// Cuando el usuario ve el anuncio de dirección en pantalla
function mostrarAnuncioDirección(texto) {
  // Mostrar visualmente
  renderAnuncio(texto);
  
  // Reproducir con énfasis
  Anuncios.anuncioCritico('direccionInstruccion', texto);
}

// Uso
mostrarAnuncioDirección('Se convoca a reunión de emergencia en 5 minutos');
// → Anuncio visual + "Directiva de la dirección: Se convoca a reunión..."
```
