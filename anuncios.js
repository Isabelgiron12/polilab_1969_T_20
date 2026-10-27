// Sistema de anuncios con Text-to-Speech
const Anuncios = (() => {
  let synth = null;
  let currentUtterance = null;

  const config = {
    lang: 'es-ES',
    rate: 0.95,
    pitch: 1,
    volume: 1
  };

  const init = () => {
    synth = window.speechSynthesis;
  };

  const anunciar = (texto, opciones = {}) => {
    if (!synth) init();

    // Cancelar anuncio anterior si está en progreso
    synth.cancel();

    const opts = { ...config, ...opciones };

    currentUtterance = new SpeechSynthesisUtterance(texto);
    currentUtterance.lang = opts.lang;
    currentUtterance.rate = opts.rate;
    currentUtterance.pitch = opts.pitch;
    currentUtterance.volume = opts.volume;

    synth.speak(currentUtterance);

    return currentUtterance;
  };

  const detener = () => {
    if (synth) synth.cancel();
  };

  const frases = {
    // INICIO Y FIN
    bienvenida: () =>
      `Bienvenidos a la sala de control. Prepárense para la misión.`,

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

    faseMiniJuego: () =>
      `Activando mini desafío. Todos al área de entrenamiento.`,

    faseTiempoMuerto: () =>
      `Tiempo muerto de operaciones. Aprovechen para revisar sistemas.`,

    faseReflexion: () =>
      `Fase de reflexión. Registren sus observaciones.`,

    faseEvaluacion: () =>
      `Evaluación de desempeño. Preparense para resultados.`,

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
      `Decisión: GO. Procediendo con envío.`,

    decisionNOGO: () =>
      `Decisión: NO GO. Abortando envío.`,

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
      `Procediéndose a siguiente etapa.`
  };

  // Reproducir una frase predefinida
  const decir = (clave, ...args) => {
    if (frases[clave]) {
      const texto = typeof frases[clave] === 'function'
        ? frases[clave](...args)
        : frases[clave];
      return anunciar(texto);
    }
  };

  return {
    anunciar,
    decir,
    detener,
    frases,
    config
  };
})();

// Ejemplo de uso en eventos del juego:
// Anuncios.decir('cambioArea', 'Marketing');
// Anuncios.anunciar('El equipo debe reunirse en la sala de juntas');
// Anuncios.detener();
