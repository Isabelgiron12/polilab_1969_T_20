# Caja Negra

Simulación de sala de control desarrollada para **METRO POLI Lab**, el laboratorio virtual de competencias del Politécnico Grancolombiano, por la Escuela de Psicología, Talento Humano y Sociedad y el grupo de investigación CVSSL.

## Uso

Abre `index.html` en un navegador (o publícalo con GitHub Pages). Pide el código de acceso al equipo antes de compartir el enlace.

## Código de acceso

La pantalla inicial pide un PIN de 4 dígitos antes de dejar entrar a la sala de control. Es un filtro básico contra el acceso casual, **no seguridad real**: cualquiera que revise el código fuente de la página puede verlo. Si necesitas control de acceso real, hay que moverlo a un backend.

El PIN se define en `index.html`, en la constante `ACCESS_PIN`. Cámbialo antes de distribuir el enlace ampliamente.

## Modo individual (virtual)

En la pantalla de Caja Negra, en **¿Cómo juegan?**, elige **Individual**. Una sola persona controla un sistema (al azar) y las demás jefaturas las juegan máquinas. La misión dura 10 minutos en vez de 20.

- La persona solo ve lo que cada máquina dice en la sala. Lo que una máquina calla o le cuenta en privado a la directora no se ve hasta el final.
- Las máquinas se contagian: si quien habló en voz alta sigue en el equipo, las siguientes hablan más; si lo despiden, callan más. Lo que hace la persona pesa más que lo que hace una máquina.
- Al abrir la caja negra aparece qué hizo de verdad cada máquina.
- Las frases de las máquinas están en `BOT_CONFIESA` y `BOT_CALLA` (`index.html`) y sus audios (`botDice*`, `botCalla*`) en `generar_audios_elevenlabs.py`.
