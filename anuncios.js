// Sistema de anuncios con Text-to-Speech
const Anuncios = (() => {
  let synth = null;
  let currentUtterance = null;

  const config = {
    lang: 'es-MX',  // Acento latino (México)
    rate: 1.2,  // Más rápido para fluidez
    pitch: 1,
    volume: 1
  };

  // Variante con acento español si se necesita
  const configEspañol = {
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

    faseMiniJuego: (area = 'entrenamiento') =>
      `Preparando desafío. Diríjase al área de ${area}.`,

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
      `Decisión: GO. La nave despega. Que el equipo sepa que pusieron su fe en esta decisión. Ahora solo queda esperar.`,

    decisionNOGO: () =>
      `Decisión: NO GO. Se ha abortado el lanzamiento. A veces es más valiente no ir que ir sin estar listos. Habrá otra oportunidad.`,

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
      `Bienvenido. Lee la información de la misión y cuando estés listo, continúa.`,

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

  // Reproducir una frase predefinida
  const decir = (clave, ...args) => {
    if (frases[clave]) {
      const texto = typeof frases[clave] === 'function'
        ? frases[clave](...args)
        : frases[clave];
      return anunciar(texto);
    }
  };

  // Anuncio crítico de dirección (CON ÉNFASIS)
  const anuncioCritico = (clave, ...args) => {
    if (!synth) init();
    synth.cancel();

    const texto = typeof frases[clave] === 'function'
      ? frases[clave](...args)
      : frases[clave];

    currentUtterance = new SpeechSynthesisUtterance(texto);
    currentUtterance.lang = config.lang;
    currentUtterance.rate = 0.85;  // Más lento para énfasis
    currentUtterance.pitch = 1.1;   // Tono ligeramente más alto
    currentUtterance.volume = 1;    // Volumen máximo

    // Pausa antes de hablar
    setTimeout(() => {
      synth.speak(currentUtterance);
    }, 300);

    return currentUtterance;
  };

  return {
    anunciar,
    decir,
    anuncioCritico,  // Para anuncios de dirección importantes
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
