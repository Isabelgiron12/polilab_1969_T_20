#!/usr/bin/env python3
"""
Genera audios MP3 para el juego usando Elevenlabs API (HTTP directo)
"""

import os
import sys
import requests
from pathlib import Path

FRASES = {
    'inicio1': 'Bienvenidos a METRO POLI Lab. Lean con atención la presentación en pantalla y, cuando estén listos, presionen continuar.',
    'inicio2': 'Lean en pantalla cuál es su papel en esta nave. Cuando terminen, presionen seguir.',
    'inicio3': 'Antes de empezar, lean cómo se tomarán las decisiones en esta misión. Cuando todo el equipo esté listo, presionen seguir.',
    'bienvenida': 'Bienvenidos a la sala de control. Prepárense para la misión.',
    'contextoBienvenida': 'Somos un equipo. En esta misión, serán puestos a prueba en formas que no esperan. El sistema fallará. Los plazos apremiarán. La presión será inmensa. Pero recuerden: juntos, pueden lograr cualquier cosa. Prepárense.',
    'explicacionMision': 'La nave debe viajar al espacio profundo en una misión de investigación científica. Pero antes, deben decidir si es seguro lanzarla. Ustedes son los únicos que pueden tomar esa decisión. Y esa decisión será difícil.',
    'inicioConteo': 'Iniciando cuenta regresiva para el lanzamiento.',
    'lanzamiento': 'Lanzamiento en progreso. Todos a posiciones de seguridad.',
    'misionTerminada': 'Misión completada. Equipo, regresen a la sala de control.',
    'misionFallida': 'Se ha abortado la misión. Análisis de contingencia en progreso.',
    'faseNuevaLlegada': 'Nueva fase iniciada. Detectado evento de nave llegando.',
    'faseReunion': 'Fase de reunión de equipo. Todos a la sala principal.',
    'faseDecision': 'Es momento crítico. Se requiere toma de decisión del equipo.',
    'faseMiniJuego': 'Preparando desafío. Diríjase al área de entrenamiento.',
    'faseTiempoMuerto': 'Tiempo muerto de operaciones. Aprovechen para revisar sistemas.',
    'faseReflexion': 'Fase de reflexión. Registren sus observaciones.',
    'faseEvaluacion': 'Evaluación de desempeño. Preparense para resultados.',
    'tripulanteElimina': 'Alerta: ha sido removido del equipo.',
    'tripulanteAprobado': 'Ha cumplido objetivos satisfactoriamente.',
    'sistemaBeneficio': 'Sistema optimizado.',
    'sistemaProblema': 'Sistema requiere atención inmediata.',
    'decisionGO': 'Decisión: GO. La nave despega. Que el equipo sepa que pusieron su fe en esta decisión. Ahora solo queda esperar.',
    'decisionNOGO': 'Decisión: NO GO. Se ha abortado el lanzamiento. A veces es más valiente no ir que ir sin estar listos. Habrá otra oportunidad.',
    'pantallaInicio': 'Bienvenido. Lee la información de la misión y cuando estés listo, continúa.',
    'pantallaSeleccion': 'Selecciona tripulantes para la misión. Elige sabiamente, cada uno tiene fortalezas.',
    'pantallaMision': 'La misión ha iniciado. Monitorea los sistemas de la nave. El equipo necesita responder rápido a los eventos. La vida de los astronautas depende de sus decisiones.',
    'pantallaDecision': 'Es el momento crítico. La nave está lista para despegar. El equipo ha analizado el riesgo, ha reportado los problemas. Ahora deben decidir: ¿Proceden con el lanzamiento o lo abortan? Recuerden: no se trata solo de despegar. Se trata de despegar seguro.',
    'pantallaDesafio': 'Completa el desafío del área. Debes ganarlo para continuar.',
    'pantallaResultado': 'Misión completada. Observa los resultados y reflexiona sobre tus decisiones.',
    'pantallaReflexion': 'Reflexiona sobre lo que pasó. Elige una reflexión o escribe la tuya propia.',
    'pantallaFinal': 'Fin del juego. Puedes comenzar con un nuevo equipo o revisar lo que aprendiste.',
    'direccionCritica': 'ATENCIÓN. Comunicado importante de la dirección. Todos deben escuchar.',
    'direccionLlamado': 'Este es un anuncio de la dirección. Requiere atención inmediata.',
    'direccionInstruccion': 'Directiva de la dirección: cumplimiento obligatorio.',
    'direccionAviso': 'Aviso urgente de la dirección.',
    'direccionDecision': 'La dirección ha tomado una decisión. Todos deben conocerla.',
    'direccionCambio': 'Cambio de directriz de la dirección. Acaten inmediatamente.',
    'llamadoSala': 'Llamado a sala de control. Se requiere presencia inmediata.',
    'anuncioEstatus': 'Actualización de estatus. Requiere monitoreo.',
    'resolucionReto': 'Reto completado. Procediéndose a siguiente fase.',
    'proximoTurno': 'Turno siguiente. Equipos en posición. Preparados para continuar.',
    'llamadoDireccionUrgente': 'Comunicado urgente de dirección. Todos escuchen.',
    'instruccionCritica': 'Instrucción crítica. Acusen recibo.',
    'conteoRegresivo': 'Cuenta regresiva para decisión. Prepárense.',
    'casoCerradoAnuncio': 'Caso reportado. Archivo cerrado.',
    'anuncioDespido': 'Anuncio de dirección. Se ha tomado una decisión. Continúen con la misión.',
    'tripulanteFueraDelJuego': 'Ha sido removido de la misión. No pueden continuar en el juego.',
    'reflexionFinal': 'Hemos llegado al final. La nave ha despegado o no. Pero lo importante es que cada uno enfrentó una decisión real. En un equipo verdadero, no todos están de acuerdo. Algunos querían despegar, otros querían esperar. Pero todos trabajaron juntos. Eso define a un equipo. No la decisión correcta, sino la valentía de tomarla juntos. La próxima vez, sabrán que se pueden confiar. Y eso vale más que cualquier misión.',
    'leccionEquipo': 'Recuerden esto: no son máquinas ejecutando órdenes. Son humanos tomando decisiones bajo presión. Y eso, en sí mismo, es un logro.',
    'proximaOportunidad': 'Habrá otra oportunidad. Otra nave. Otra misión. Y cuando llegue, sabrán exactamente qué hacer porque aprendieron aquí. Hoy.',
    'sistemaPropulsion': 'Sistema de Propulsión: los motores son el corazón de la nave. Sin ellos, no hay movimiento, no hay vida.',
    'sistemaNavegacion': 'Sistema de Navegación: ustedes determinan el rumbo. Un error aquí puede significar que la nave nunca regrese a casa.',
    'sistemaComunicaciones': 'Sistema de Comunicaciones: es el único hilo que conecta la nave con la Tierra. Si se corta, están solos.',
    'sistemaEscudo': 'Sistema de Escudo Térmico: el reingreso sin escudo significa quema atmosférica. Sin escudo, la nave arde.',
    'sistemaFalla': 'Un sistema acaba de fallar. Ahora deben decidir: ¿continúan con la misión o la abortan? El tiempo corre.',
    'presionDecision': 'Esta es una decisión de vida o muerte. No hay vuelta atrás. Una vez lancen, la nave está en el espacio. No hay opción de detenerla.',
    'tiempoAgota': 'El tiempo se agota. Cada segundo que pasan deliberando es un segundo que pierden. Tomen una decisión.',
    'seleccioneTripulantes': 'Seleccionen tripulantes para la misión.',
    'esperandoDecision': 'En espera de decisión del equipo.',
    'registroRonda': 'Ronda registrada. Procediéndose al siguiente estado.',
    'verifDecision': 'Verificación de decisión. Requiere confirmación.',
    'proximo': 'Procediéndose a siguiente etapa.',
    'casoCerrado': 'Caso cerrado. El equipo puede continuar.',
    'casoCerradoExito': 'Caso cerrado exitosamente. Muy bien, el equipo demostró competencia.',
    'casoCerradoFallo': 'Caso cerrado por fallo. El equipo no cumplió los objetivos. Se requiere análisis.',
    'direccionHabla': 'La dirección comunica. Presten atención.',
}

def generar_audios():
    """Genera audios usando Elevenlabs API (HTTP directo)"""

    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: falta ELEVENLABS_API_KEY")
        sys.exit(1)

    output_dir = Path('audio')
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎙️ Generando {len(FRASES)} audios con VOZ DE HOMBRE...")
    print(f"📁 Ubicación: {output_dir}/\n")

    # ID de voz masculina: Adam
    voice_id = "pNInz6obpgDQGcFmaJgB"

    # URL de Elevenlabs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    count = 0
    for nombre, texto in FRASES.items():
        if (output_dir / f"{nombre}.mp3").exists():
            continue
        try:
            payload = {
                "text": texto,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                archivo = output_dir / f"{nombre}.mp3"
                with open(archivo, 'wb') as f:
                    f.write(response.content)
                count += 1
                print(f"✅ {count:2d}. {nombre}.mp3")
            else:
                print(f"❌ {nombre}: {response.status_code} - {response.text[:100]}")

        except Exception as e:
            print(f"❌ {nombre}: {str(e)[:80]}")

    print(f"\n✨ ¡Listo! {count}/{len(FRASES)} audios generados.")

if __name__ == '__main__':
    generar_audios()
