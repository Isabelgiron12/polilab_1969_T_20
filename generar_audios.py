#!/usr/bin/env python3
"""
Genera audios MP3 para el juego usando Google Cloud Text-to-Speech
Requiere: pip install google-cloud-texttospeech
"""

from google.cloud import texttospeech
import os
import json

# Configurar cliente
client = texttospeech.TextToSpeechClient()

# Frases del juego (extraídas de anuncios.js)
FRASES = {
    # INICIO CON CONTEXTO
    'bienvenida': 'Bienvenidos a la sala de control. Hoy comandarán una nave de investigación en una misión crítica. Cada decisión que tomen afectará no solo el éxito de la misión, sino la vida de los astronautas a bordo. Prepárense para lo que viene.',
    'contextoBienvenida': 'Somos un equipo. En esta misión, serán puestos a prueba en formas que no esperan. El sistema fallará. Los plazos apremiarán. La presión será inmensa. Pero recuerden: juntos, pueden lograr cualquier cosa. Prepárense.',
    'explicacionMision': 'La nave debe viajar al espacio profundo en una misión de investigación científica. Pero antes, deben decidir si es seguro lanzarla. Ustedes son los únicos que pueden tomar esa decisión. Y esa decisión será difícil.',
    'inicioConteo': 'Iniciando cuenta regresiva para el lanzamiento.',
    'lanzamiento': 'Lanzamiento en progreso. Todos a posiciones de seguridad.',
    'misionTerminada': 'Misión completada. Equipo, regresen a la sala de control.',
    'misionFallida': 'Se ha abortado la misión. Análisis de contingencia en progreso.',

    # FASES
    'faseNuevaLlegada': 'Nueva fase iniciada. Detectado evento de nave llegando.',
    'faseReunion': 'Fase de reunión de equipo. Todos a la sala principal.',
    'faseDecision': 'Es el momento crítico. La nave está lista para despegar. El equipo ha analizado el riesgo. Ahora deben decidir: ¿Proceden con el lanzamiento o lo abortan? Recuerden: no se trata solo de despegar. Se trata de despegar seguro.',
    'faseMiniJuego': 'Preparando desafío. Todos al área de entrenamiento.',
    'faseTiempoMuerto': 'Tiempo muerto de operaciones. Aprovechen para revisar sistemas.',
    'faseReflexion': 'Fase de reflexión. Registren sus observaciones.',
    'faseEvaluacion': 'Evaluación de desempeño. Preparense para resultados.',

    # EVENTOS
    'tripulanteElimina': 'Alerta: ha sido removido del equipo.',
    'tripulanteAprobado': 'Ha cumplido objetivos satisfactoriamente.',
    'sistemaBeneficio': 'Sistema optimizado.',
    'sistemaProblema': 'Sistema requiere atención inmediata.',
    'decisionGO': 'Decisión: GO. La nave despega. Que el equipo sepa que pusieron su fe en esta decisión. Ahora solo queda esperar.',
    'decisionNOGO': 'Decisión: NO GO. Se ha abortado el lanzamiento. A veces es más valiente no ir que ir sin estar listos. Habrá otra oportunidad.',

    # INSTRUCCIONES
    'pantallaInicio': 'Bienvenido. Lee la información de la misión y cuando estés listo, continúa.',
    'pantallaSeleccion': 'Selecciona tripulantes para la misión. Elige sabiamente, cada uno tiene fortalezas.',
    'pantallaMision': 'La misión ha iniciado. Monitorea los sistemas de la nave. El equipo necesita responder rápido a los eventos. La vida de los astronautas depende de sus decisiones.',
    'pantallaResultado': 'Misión completada. Observa los resultados y reflexiona sobre tus decisiones.',
    'pantallaReflexion': 'Reflexiona sobre lo que pasó. Elige una reflexión o escribe la tuya propia.',
    'pantallaFinal': 'Fin del juego. Puedes comenzar con un nuevo equipo o revisar lo que aprendiste.',

    # OPERACIONALES
    'llamadoSala': 'Llamado a sala de control. Se requiere presencia inmediata.',
    'proximoTurno': 'Turno siguiente. Equipos en posición. Preparados para continuar.',
    'llamadoDireccionUrgente': 'Comunicado urgente de dirección. Todos escuchen.',
    'conteoRegresivo': 'Cuenta regresiva para decisión. Prepárense.',

    # CONTEXTO DE SISTEMAS
    'sistemaPropulsion': 'Sistema de Propulsión: los motores son el corazón de la nave. Sin ellos, no hay movimiento, no hay vida.',
    'sistemaNavegacion': 'Sistema de Navegación: ustedes determinan el rumbo. Un error aquí puede significar que la nave nunca regrese a casa.',
    'sistemaComunicaciones': 'Sistema de Comunicaciones: es el único hilo que conecta la nave con la Tierra. Si se corta, están solos.',
    'sistemaEscudo': 'Sistema de Escudo Térmico: el reingreso sin escudo significa quema atmosférica. Sin escudo, la nave arde.',

    # CONTEXTODE SITUACIONES
    'sistemaFalla': 'Un sistema acaba de fallar. Ahora deben decidir: ¿continúan con la misión o la abortan? El tiempo corre.',
    'presionDecision': 'Esta es una decisión de vida o muerte. No hay vuelta atrás. Una vez lancen, la nave está en el espacio. No hay opción de detenerla.',
    'tiempoAgota': 'El tiempo se agota. Cada segundo que pasan deliberando es un segundo que pierden. Tomen una decisión.',

    # REFLEXIÓN FINAL
    'reflexionFinal': 'Hemos llegado al final. La nave ha despegado o no. Pero lo importante es que cada uno enfrentó una decisión real. En un equipo verdadero, no todos están de acuerdo. Algunos querían despegar, otros querían esperar. Pero todos trabajaron juntos. Eso define a un equipo. No la decisión correcta, sino la valentía de tomarla juntos. La próxima vez, sabrán que se pueden confiar. Y eso vale más que cualquier misión.',
    'leccionEquipo': 'Recuerden esto: no son máquinas ejecutando órdenes. Son humanos tomando decisiones bajo presión. Y eso, en sí mismo, es un logro.',
    'proximaOportunidad': 'Habrá otra oportunidad. Otra nave. Otra misión. Y cuando llegue, sabrán exactamente qué hacer porque aprendieron aquí. Hoy.',

    # DIRECCIÓN Y DESPIDOS
    'anuncioDespido': 'Anuncio de dirección. Se ha tomado una decisión. Continúen con la misión.',
    'tripulanteFueraDelJuego': 'Ha sido removido de la misión. No pueden continuar en el juego.',
}

def generar_audio(nombre_archivo, texto, idioma='es-MX'):
    """Genera un audio MP3 usando Google Cloud TTS"""

    # Configurar síntesis
    synthesis_input = texttospeech.SynthesisInput(text=texto)

    # Configurar voz (latino)
    voice = texttospeech.VoiceSelectionParams(
        language_code=idioma,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configurar audio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.2,  # Velocidad
        pitch=0.0,          # Pitch normal
    )

    # Generar
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    # Guardar
    with open(nombre_archivo, 'wb') as out:
        out.write(response.audio_content)

    print(f"✅ Generado: {nombre_archivo}")

def main():
    # Crear carpeta de audios
    output_dir = 'polilab_1969_T_20/audio'
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎙️ Generando {len(FRASES)} audios...")
    print(f"📁 Ubicación: {output_dir}/\n")

    # Generar cada audio
    for nombre, texto in FRASES.items():
        archivo = f'{output_dir}/{nombre}.mp3'
        generar_audio(archivo, texto)

    print(f"\n✨ ¡Listo! {len(FRASES)} audios generados.")
    print(f"📝 Próximo paso: Actualizar el juego para usar estos audios.")

if __name__ == '__main__':
    main()
