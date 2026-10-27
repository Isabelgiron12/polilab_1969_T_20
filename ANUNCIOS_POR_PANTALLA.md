# 📺 Anuncios por Cambio de Pantalla

Cada pantalla del juego tiene su **anuncio instructivo** que explica qué debe hacer el usuario.

---

## 🎯 Pantallas y Anuncios

### 1. Pantalla de Inicio
```javascript
Anuncios.decir('pantallaInicio');
// "Bienvenido. Lee la información de la misión y cuando estés listo, continúa."
```
**Cuándo**: Cuando se carga la pantalla inicial

---

### 2. Pantalla de Selección de Tripulantes
```javascript
Anuncios.decir('pantallaSeleccion', 6);  // 6 tripulantes
// "Selecciona 6 tripulantes para la misión. Elige sabiamente, cada uno tiene fortalezas."
```
**Cuándo**: Cuando aparece la pantalla de selección
**Parámetro**: Cantidad de tripulantes a seleccionar

---

### 3. Pantalla de Misión
```javascript
Anuncios.decir('pantallaMision');
// "La misión ha iniciado. Atiende los eventos y toma decisiones cuando sea necesario."
```
**Cuándo**: Cuando comienza la misión principal

---

### 4. Pantalla de Decisión (GO/NO-GO)
```javascript
Anuncios.decir('pantallaDecision');
// "Es momento de decidir. Elige GO para enviar o NO GO para cancelar. Piensa bien tu decisión."
```
**Cuándo**: Cuando aparece la opción de enviar o cancelar

---

### 5. Pantalla de Desafío
```javascript
Anuncios.decir('pantallaDesafio', 'jefatura');  // Nombre del área
// "Completa el desafío del área de jefatura. Debes ganarlo para continuar."
```
**Cuándo**: Cuando comienza un desafío
**Parámetro**: Nombre del área del desafío

---

### 6. Pantalla de Resultado
```javascript
Anuncios.decir('pantallaResultado');
// "Misión completada. Observa los resultados y reflexiona sobre tus decisiones."
```
**Cuándo**: Cuando termina la misión y se muestran resultados

---

### 7. Pantalla de Reflexión
```javascript
Anuncios.decir('pantallaReflexion');
// "Reflexiona sobre lo que pasó. Elige una reflexión o escribe la tuya propia."
```
**Cuándo**: Cuando se pide reflexión al usuario

---

### 8. Pantalla Final
```javascript
Anuncios.decir('pantallaFinal');
// "Fin del juego. Puedes comenzar con un nuevo equipo o revisar lo que aprendiste."
```
**Cuándo**: Cuando termina completamente el juego

---

## 🔌 Cómo Integrar en el Juego

En el `index.html`, donde cambian de pantalla, agrega:

```javascript
// Ejemplo: Al cambiar a pantalla de selección
function mostrarSeleccion() {
  // Renderizar UI
  renderSeleccion();
  
  // Anunciar instrucción
  Anuncios.decir('pantallaSeleccion', S.count);
}

// Ejemplo: Al iniciar desafío
function iniciarDesafio(area) {
  // Renderizar desafío
  renderDesafio(area);
  
  // Anunciar
  Anuncios.decir('pantallaDesafio', area);
}
```

---

## 📝 Checklista de Integración

- [ ] Pantalla Inicio → `pantallaInicio()`
- [ ] Pantalla Selección → `pantallaSeleccion(cantidad)`
- [ ] Pantalla Misión → `pantallaMision()`
- [ ] Pantalla Decisión → `pantallaDecision()`
- [ ] Pantalla Desafío → `pantallaDesafio(area)`
- [ ] Pantalla Resultado → `pantallaResultado()`
- [ ] Pantalla Reflexión → `pantallaReflexion()`
- [ ] Pantalla Final → `pantallaFinal()`

---

## 🎙️ Ejemplo Completo

```javascript
// En la función que cambia de pantalla
function cambiarPantalla(nuevaPantalla) {
  S.screen = nuevaPantalla;
  
  // Mapa de anuncios por pantalla
  const anunciosPorPantalla = {
    'intro': () => Anuncios.decir('pantallaInicio'),
    'seleccion': () => Anuncios.decir('pantallaSeleccion', 6),
    'mission': () => Anuncios.decir('pantallaMision'),
    'decision': () => Anuncios.decir('pantallaDecision'),
    'desafio': () => Anuncios.decir('pantallaDesafio', S.areaActual),
    'resultado': () => Anuncios.decir('pantallaResultado'),
    'reflexion': () => Anuncios.decir('pantallaReflexion'),
    'end': () => Anuncios.decir('pantallaFinal')
  };
  
  // Reproducir anuncio si existe para esta pantalla
  if(anunciosPorPantalla[nuevaPantalla]) {
    anunciosPorPantalla[nuevaPantalla]();
  }
  
  render();
}
```

---

## 💡 Tips

- Los anuncios se reproducen en **acento latino (es-MX)**
- Velocidad: **1.2x** (rápido y claro)
- Puedes ajustar velocidad por anuncio si necesitas énfasis
- Los anuncios son **opcionales** - si el navegador no soporta TTS, no falla
