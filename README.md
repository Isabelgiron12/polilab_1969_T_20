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

## Resultados compartidos (Supabase)

El tablero y el muro se guardan en Supabase, así se ven iguales desde cualquier equipo. Mientras `NUBE` esté vacía en `index.html`, cada navegador guarda solo lo suyo.

Para conectarlo:

1. Crea un proyecto gratuito en [supabase.com](https://supabase.com).
2. En **SQL Editor**, pega y ejecuta `supabase/schema.sql`.
3. En **Connect** (o **Settings > API Keys**), copia la URL del proyecto y la **publishable key** (`sb_publishable_...`). Nunca uses la secret key.
4. Ponlas en `index.html`, en la constante `NUBE`, y publica el cambio.

Cómo funciona:

- La publishable key queda visible en el código, y es normal. Solo permite leer y agregar filas; nadie puede editar ni borrar con ella. Cualquiera que la copie sí podría agregar filas falsas o frases al muro.
- Para limpiar datos, entra al **Table Editor** de Supabase.
- Si no hay conexión, la partida queda en el navegador y se envía sola después.
- Lo que un navegador tenía guardado se sube una sola vez, la primera vez que abre el juego ya conectado.
- Los planes gratuitos de Supabase pausan los proyectos sin actividad. Si el tablero deja de cargar tras un tiempo sin usarlo, reactiva el proyecto desde el panel.
- Para analizar los datos, exporta `partidas` a CSV desde el **Table Editor**.
