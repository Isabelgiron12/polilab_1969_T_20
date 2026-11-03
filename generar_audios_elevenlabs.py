#!/usr/bin/env python3
"""
Genera audios MP3 para el juego usando Elevenlabs API (HTTP directo)
"""

import os
import sys
import requests
from pathlib import Path

FRASES = {
    'inicio1': 'Lean con atención la presentación en pantalla.',
    'inicio2': 'Lean en pantalla cuál es su papel en esta nave.',
    'inicio3': 'Antes de empezar, lean cómo se tomarán las decisiones en esta misión.',
    'cajaNegra': 'Elijan cuántos juegan y toquen a los tripulantes que forman parte del equipo.',
    'bienvenida': 'Prepárense para la misión.',
    'contextoBienvenida': 'Somos un equipo. En esta misión, serán puestos a prueba en formas que no esperan. El sistema fallará. Los plazos apremiarán. La presión será inmensa. Pero recuerden: juntos, pueden lograr cualquier cosa. Prepárense.',
    'explicacionMision': 'La nave debe viajar al espacio profundo en una misión de investigación científica. Pero antes, deben decidir si es seguro lanzarla. Ustedes son los únicos que pueden tomar esa decisión. Y esa decisión será difícil.',
    'turno1': 'Jefatura de Propulsión, verifique su proceso.',
    'turno2': 'Jefatura de Oxígeno, verifique su proceso.',
    'turno3': 'Jefatura de Navegación, verifique su proceso.',
    'turno4': 'Jefatura de Comunicaciones, verifique su proceso.',
    'turno5': 'Jefatura de Escudo Térmico, verifique su proceso.',
    'turno6': 'Jefatura de Soporte Vital, verifique su proceso.',
    # Novedades: 'Dirección llama a sala…' + caso + arreglo
    'direccionLlamaSala': 'Dirección llama a sala y les notifica que:',
    'sigue1': 'Los directivos revisaron el caso de Jefatura de Propulsión. Sigue en el equipo.',
    'arreglo1': 'Como se dijo en voz alta, ya están arreglando Propulsión. Retraso de 2 días.',
    'arregloAun1': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Propulsión. Retraso de 2 días.',
    'despido1_1': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por una reestructuración del área. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'despido1_2': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'despido1_3': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por una evaluación interna. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'despido1_4': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'despido1_5': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por decisión del comité directivo. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'despido1_6': 'Se ha tomado la decisión de despedir a Jefatura de Propulsión por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Propulsión pierde el juego.',
    'sigue2': 'Los directivos revisaron el caso de Jefatura de Oxígeno. Sigue en el equipo.',
    'arreglo2': 'Como se dijo en voz alta, ya están arreglando Oxígeno. Retraso de 1 día.',
    'arregloAun2': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Oxígeno. Retraso de 1 día.',
    'despido2_1': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por una reestructuración del área. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'despido2_2': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'despido2_3': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por una evaluación interna. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'despido2_4': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'despido2_5': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por decisión del comité directivo. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'despido2_6': 'Se ha tomado la decisión de despedir a Jefatura de Oxígeno por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Oxígeno pierde el juego.',
    'sigue3': 'Los directivos revisaron el caso de Jefatura de Navegación. Sigue en el equipo.',
    'arreglo3': 'Como se dijo en voz alta, ya están arreglando Navegación. Retraso de 3 días.',
    'arregloAun3': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Navegación. Retraso de 3 días.',
    'despido3_1': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por una reestructuración del área. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'despido3_2': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'despido3_3': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por una evaluación interna. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'despido3_4': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'despido3_5': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por decisión del comité directivo. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'despido3_6': 'Se ha tomado la decisión de despedir a Jefatura de Navegación por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Navegación pierde el juego.',
    'sigue4': 'Los directivos revisaron el caso de Jefatura de Comunicaciones. Sigue en el equipo.',
    'arreglo4': 'Como se dijo en voz alta, ya están arreglando Comunicaciones. Retraso de 8 horas.',
    'arregloAun4': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Comunicaciones. Retraso de 8 horas.',
    'despido4_1': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por una reestructuración del área. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'despido4_2': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'despido4_3': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por una evaluación interna. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'despido4_4': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'despido4_5': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por decisión del comité directivo. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'despido4_6': 'Se ha tomado la decisión de despedir a Jefatura de Comunicaciones por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Comunicaciones pierde el juego.',
    'sigue5': 'Los directivos revisaron el caso de Jefatura de Escudo Térmico. Sigue en el equipo.',
    'arreglo5': 'Como se dijo en voz alta, ya están arreglando Escudo térmico. Retraso de 7 días.',
    'arregloAun5': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Escudo térmico. Retraso de 7 días.',
    'despido5_1': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por una reestructuración del área. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'despido5_2': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'despido5_3': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por una evaluación interna. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'despido5_4': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'despido5_5': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por decisión del comité directivo. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'despido5_6': 'Se ha tomado la decisión de despedir a Jefatura de Escudo Térmico por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Escudo Térmico pierde el juego.',
    'sigue6': 'Los directivos revisaron el caso de Jefatura de Soporte Vital. Sigue en el equipo.',
    'arreglo6': 'Como se dijo en voz alta, ya están arreglando Soporte vital. Retraso de 2 semanas.',
    'arregloAun6': 'Aun así, como se dijo en voz alta, el equipo ya está arreglando Soporte vital. Retraso de 2 semanas.',
    'despido6_1': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por una reestructuración del área. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
    'despido6_2': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por recorte de personal por presupuesto. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
    'despido6_3': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por una evaluación interna. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
    'despido6_4': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por un cambio en la política de la empresa. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
    'despido6_5': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por decisión del comité directivo. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
    'despido6_6': 'Se ha tomado la decisión de despedir a Jefatura de Soporte Vital por protocolo de seguridad de la misión. Continúen con la misión. Jefatura de Soporte Vital pierde el juego.',
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
    'pantallaInicio': 'Lee la información de la misión y cuando estés listo, continúa.',
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
