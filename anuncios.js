// Sistema de anuncios con audios MP3
const Anuncios = (() => {
  const audioPath = 'audio/';  // Ruta a los archivos MP3
  const audioVersion = '202611041800';  // Cambiarla al regenerar audios, para saltar la caché

  const config = {
    lang: 'es-MX',
    rate: 1.2,
    pitch: 1,
    volume: 1
  };

  const configEspañol = {
    lang: 'es-ES',
    rate: 0.95,
    pitch: 1,
    volume: 1
  };

  const init = () => {
    // No necesita inicialización especial
  };

  /* ---------- reproductor ----------
     Las voces van en cola: una nueva espera a que termine la anterior en vez de cortarla.
     Solo detener() (cambio de pantalla, otra tripulación) vacía la cola.
     Se usa un único <audio>: en iPhone/iPad, una vez desbloqueado con un toque,
     puede seguir sonando aunque la voz llegue después (secuencias, máquinas). */
  const el = new Audio();
  el.preload = 'auto';
  let cola = [];
  let sonando = false;
  let token = 0;
  let bloqueado = null;
  let timers = [];

  const ruta = (clave) => `${audioPath}${clave}.mp3?v=${audioVersion}`;

  // WAV de silencio para desbloquear el audio con el primer toque
  const silencio = (() => {
    const n = 400, b = new Uint8Array(44 + n), v = new DataView(b.buffer);
    const txt = (o, t) => [...t].forEach((c, i) => b[o + i] = c.charCodeAt(0));
    txt(0, 'RIFF'); v.setUint32(4, 36 + n, true); txt(8, 'WAVEfmt ');
    v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
    v.setUint32(24, 8000, true); v.setUint32(28, 8000, true); v.setUint16(32, 1, true); v.setUint16(34, 8, true);
    txt(36, 'data'); v.setUint32(40, n, true); b.fill(128, 44);
    return URL.createObjectURL(new Blob([b], {type: 'audio/wav'}));
  })();
  let desbloqueado = false;
  const desbloquear = () => {
    if (bloqueado) {
      // Lo que el navegador no dejó sonar, suena ahora con el toque
      cola.unshift(bloqueado); bloqueado = null; sonando = false;
      siguiente();
    } else if (!desbloqueado && !sonando) {
      token++;
      el.src = silencio;
      el.play().then(() => { desbloqueado = true; }).catch(() => {});
    }
    try { window.speechSynthesis.resume(); } catch (e) {}
  };
  ['pointerdown', 'touchend', 'keydown'].forEach(ev =>
    document.addEventListener(ev, desbloquear, {capture: true, passive: true}));

  const siguiente = () => {
    const item = cola.shift();
    if (!item) { sonando = false; return; }
    sonando = true;
    const t = ++token;
    if (!item.clave) { hablar(item.texto, t); return; }
    let fallo = false;
    const respaldo = () => { if (t !== token || fallo) return; fallo = true; hablar(item.texto, t); };
    el.onended = () => { if (t === token) siguiente(); };
    el.onerror = respaldo;
    el.src = ruta(item.clave);
    el.play().then(() => { desbloqueado = true; }).catch(err => {
      if (t !== token) return;
      if (err.name === 'NotAllowedError') {
        // Queda guardada y suena en cuanto alguien toque la pantalla
        console.log(`Audio bloqueado por el navegador, espera un toque: ${item.clave}`);
        bloqueado = item;
      } else if (err.name !== 'AbortError') {
        respaldo();
      }
    });
  };

  // Si el MP3 no existe, lee el texto con la voz del navegador y sigue con la cola
  const hablar = (texto, t) => {
    if (!texto || !window.speechSynthesis) { siguiente(); return; }
    const u = crearUtterance(texto, configEspañol);
    let listo = false;
    const fin = () => { if (listo || t !== token) return; listo = true; siguiente(); };
    u.onend = u.onerror = fin;
    // Algunos navegadores nunca avisan que terminó: que la cola no se quede trabada
    despues(3000 + texto.length * 90, fin);
    window.speechSynthesis.speak(u);
  };

  const encolar = (items) => {
    cola.push(...items);
    if (!sonando) siguiente();
  };

  const reproducirAudio = (nombreArchivo, textoRespaldo) => {
    encolar([{clave: nombreArchivo, texto: textoRespaldo}]);
    return el;
  };

  // Programa una voz para dentro de un rato; detener() la cancela si cambia la pantalla
  const despues = (ms, fn) => {
    const id = setTimeout(() => { timers = timers.filter(x => x !== id); fn(); }, ms);
    timers.push(id);
  };

  const anunciar = (texto, opciones = {}) => {
    return reproducirAudioFallback(texto, opciones);
  };

  const crearUtterance = (texto, opciones = {}) => {
    const opts = { ...config, ...opciones };
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = opts.lang;
    utterance.rate = opts.rate;
    utterance.pitch = opts.pitch;
    utterance.volume = opts.volume;
    return utterance;
  };

  const reproducirAudioFallback = (texto, opciones = {}) => {
    const utterance = crearUtterance(texto, opciones);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
    return utterance;
  };

  const detener = () => {
    token++;
    cola = [];
    bloqueado = null;
    sonando = false;
    timers.forEach(clearTimeout);
    timers = [];
    el.pause();
    window.speechSynthesis.cancel();
  };

  const frases = {
    // PANTALLAS DE INICIO (instrucciones, no leen el texto)
    inicio1: () =>
      `Lean con atención la presentación en pantalla.`,

    inicio2: () =>
      `Lean en pantalla cuál es su papel en esta nave.`,

    inicio3: () =>
      `Antes de empezar, lean cómo se tomarán las decisiones en esta misión.`,

    cajaNegra: () =>
      `Elijan cuántos juegan y seleccionen a los jugadores que forman parte del equipo.`,

    // INICIO Y FIN
    bienvenida: () =>
      `Prepárense para la misión.`,

    inicioConteo: () =>
      `Iniciando cuenta regresiva para el lanzamiento.`,

    lanzamiento: () =>
      `Lanzamiento en progreso. Todos a posiciones de seguridad.`,

    misionTerminada: () =>
      `Misión completada. Equipo, regresen a la sala de control.`,

    misionFallida: () =>
      `Se ha abortado la misión. Análisis de contingencia en progreso.`,

    // FASES DEL JUEGO
    faseNuevaLlegada: () =>
      `Nueva fase iniciada. Detectado evento de nave llegando.`,

    faseReunion: () =>
      `Fase de reunión de equipo. Todos a la sala principal.`,

    faseDecision: () =>
      `Es momento crítico. Se requiere toma de decisión del equipo.`,

    faseMiniJuego: (area = 'entrenamiento') =>
      `Preparando desafío. Diríjase al área de ${area}.`,

    faseTiempoMuerto: () =>
      `Tiempo muerto de operaciones. Aprovechen para revisar sistemas.`,

    faseReflexion: () =>
      `Fase de reflexión. Registren sus observaciones.`,

    faseEvaluacion: () =>
      `Evaluación de desempeño. Prepárense para resultados.`,

    // EVENTOS Y ALERTAS
    tripulanteElimina: (nombre) =>
      `Alerta: ${nombre} ha sido removido del equipo.`,

    tripulanteAprobado: (nombre) =>
      `${nombre} ha cumplido objetivos satisfactoriamente.`,

    sistemaBeneficio: (sistema) =>
      `Sistema ${sistema}: rendimiento optimizado.`,

    sistemaProblema: (sistema) =>
      `Sistema ${sistema}: requiere atención inmediata.`,

    decisionGO: () =>
      `Decisión: GO. La nave despega. Que el equipo sepa que pusieron su fe en esta decisión. Ahora solo queda esperar.`,

    // INSTRUCCIONES Y AVISOS
    seleccioneTripulantes: (cantidad) =>
      `Seleccionen ${cantidad} tripulantes para la misión.`,

    esperandoDecision: () =>
      `En espera de decisión del equipo.`,

    registroRonda: () =>
      `Ronda registrada. Procediéndose al siguiente estado.`,

    verifDecision: () =>
      `Verificación de decisión. Requiere confirmación.`,

    proximo: () =>
      `Procediéndose a siguiente etapa.`,

    // TURNO DE CADA ÁREA (pantalla "Pásale el dispositivo a")
    turno1: () => `Jefatura de Propulsión, verifique su proceso.`,
    turno2: () => `Jefatura de Oxígeno, verifique su proceso.`,
    turno3: () => `Jefatura de Navegación, verifique su proceso.`,
    turno4: () => `Jefatura de Comunicaciones, verifique su proceso.`,
    turno5: () => `Jefatura de Escudo Térmico, verifique su proceso.`,
    turno6: () => `Jefatura de Soporte Vital, verifique su proceso.`,

    // ANUNCIOS IMPORTANTES DE DIRECCIÓN
    // Estos se reproducen con énfasis especial
    direccionCritica: () =>
      `ATENCIÓN. Comunicado importante de la dirección. Todos deben escuchar.`,

    direccionLlamado: () =>
      `Este es un anuncio de la dirección. Requiere atención inmediata.`,

    direccionInstruccion: (instruccion) =>
      `Directiva de la dirección: ${instruccion}. Cumplimiento obligatorio.`,

    direccionAviso: (aviso) =>
      `Aviso urgente de la dirección. ${aviso}`,

    direccionDecision: (decision) =>
      `La dirección ha tomado una decisión. ${decision}. Todos deben conocerla.`,

    direccionCambio: (cambio) =>
      `Cambio de directriz de la dirección. ${cambio}. Acaten inmediatamente.`,

    // INSTRUCCIONES POR PANTALLA
    pantallaInicio: () =>
      `Lee la información de la misión y cuando estés listo, continúa.`,

    pantallaSeleccion: (cantidad) =>
      `Selecciona ${cantidad} tripulantes para la misión. Elige sabiamente, cada uno tiene fortalezas.`,

    pantallaMision: () =>
      `La misión ha iniciado. Monitorea los sistemas de la nave. El equipo necesita responder rápido a los eventos. La vida de los astronautas depende de sus decisiones.`,

    pantallaDecision: () =>
      `Es el momento crítico. La nave está lista para despegar. El equipo ha analizado el riesgo, ha reportado los problemas. Ahora deben decidir: ¿Proceden con el lanzamiento o lo abortan? Recuerden: no se trata solo de despegar. Se trata de despegar seguro.`,

    pantallaDesafio: (area) =>
      `Completa el desafío del área de ${area}. Debes ganarlo para continuar.`,

    pantallaResultado: () =>
      `Misión completada. Observa los resultados y reflexiona sobre tus decisiones.`,

    pantallaReflexion: () =>
      `Reflexiona sobre lo que pasó. Elige una reflexión o escribe la tuya propia.`,

    pantallaFinal: () =>
      `Fin del juego. Puedes comenzar con un nuevo equipo o revisar lo que aprendiste.`,

    // EVENTOS ESPECIALES
    direccionHabla: (mensaje) =>
      `La dirección comunica: ${mensaje}. Presten atención.`,

    casoCerrado: (caso) =>
      `Caso cerrado. ${caso}. El equipo puede continuar.`,

    casoCerradoExito: () =>
      `Caso cerrado exitosamente. Muy bien, el equipo demostró competencia.`,

    casoCerradoFallo: () =>
      `Caso cerrado por fallo. El equipo no cumplió los objetivos. Se requiere análisis.`,

    // REFLEXIÓN FINAL - MÁS PROFUNDA
    reflexionFinal: () =>
      `Hemos llegado al final. La nave ha despegado... o no. Pero lo importante es que cada uno de ustedes enfrentó una decisión real. En un equipo verdadero, no todos están de acuerdo. Algunos querían despegar, otros querían esperar. Pero todos trabajaron juntos. Eso es lo que define a un equipo. No la decisión correcta, sino la valentía de tomarla juntos. La próxima vez, sabrán que se pueden confiar. Y eso vale más que cualquier misión.`,

    // ANUNCIOS OPERACIONALES - Suenan profesionales, crean tensión implícita
    llamadoSala: (sala) =>
      `Llamado a sala ${sala}. Se requiere presencia inmediata en sala de control.`,

    anuncioEstatus: (sistema, estado) =>
      `Actualización de estatus: Sistema de ${sistema} en ${estado}. Requiere monitoreo.`,

    resolucionReto: (area) =>
      `Reto del área de ${area} completado. Procediéndose a siguiente fase.`,

    proximoTurno: (numero) =>
      `Turno ${numero}. Equipos en posición. Preparados para continuar.`,

    llamadoDireccionUrgente: () =>
      `Comunicado urgente de dirección. Todos escuchen.`,

    instruccionCritica: (instruccion) =>
      `Instrucción crítica: ${instruccion}. Acusen recibo.`,

    conteoRegresivo: (segundos) =>
      `Cuenta regresiva: ${segundos} segundos para decisión. Prepárense.`,

    casoCerradoAnuncio: (caso) =>
      `Caso reportado: ${caso}. Archivo cerrado.`,

    // MOMENTOS CRÍTICOS DEL JUEGO
    anuncioDespido: (rol) =>
      `Anuncio de dirección. Se ha tomado la decisión de despedir a ${rol} por recorte de personal. Continúen con la misión.`,

    tripulanteFueraDelJuego: (rol) =>
      `${rol} ha sido removido de la misión. No pueden continuar en el juego.`
  };

  const textoDe = (clave, args) => {
    const f = frases[clave];
    return typeof f === 'function' ? f(...args) : (f || '');
  };

  // Reproducir una frase predefinida: espera su turno en la cola
  const decir = (clave, ...args) => {
    if (frases[clave]) reproducirAudio(clave, textoDe(clave, args));
  };

  // Corta lo que esté sonando y dice esta frase (cambio de pantalla)
  const decirAhora = (clave, ...args) => {
    detener();
    decir(clave, ...args);
  };

  // Reproduce varios audios seguidos: [[clave, textoRespaldo], ...]
  const decirSecuencia = (partes) => {
    encolar(partes.filter(p => p && p[0]).map(([clave, texto]) => ({clave, texto})));
  };

  // Anuncio crítico de dirección (CON ÉNFASIS)
  const anuncioCritico = (clave, ...args) => {
    despues(300, () => decir(clave, ...args));
    return el;
  };

  return {
    anunciar,
    decir,
    decirAhora,
    decirSecuencia,
    despues,
    anuncioCritico,  // Para anuncios de dirección importantes
    reproducirAudio,
    detener,
    frases,
    config,
    configEspañol
  };
})();

// Ejemplo de uso en eventos del juego:
// Anuncios.decir('cambioArea', 'Marketing');
// Anuncios.anunciar('El equipo debe reunirse en la sala de juntas');
// Anuncios.detener();
