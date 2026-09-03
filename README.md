# Caja Negra

Simulación de sala de control desarrollada para **POLILab**, el laboratorio virtual de competencias del Politécnico Grancolombiano, por la Escuela de Psicología, Talento Humano y Sociedad y el grupo de investigación CVSSL.

## Uso

Abre `index.html` en un navegador (o publícalo con GitHub Pages). Pide el código de acceso al equipo antes de compartir el enlace.

## Código de acceso

La pantalla inicial pide un PIN de 4 dígitos antes de dejar entrar a la sala de control. Es un filtro básico contra el acceso casual, **no seguridad real**: cualquiera que revise el código fuente de la página puede verlo. Si necesitas control de acceso real, hay que moverlo a un backend.

El PIN se define en `index.html`, en la constante `ACCESS_PIN`. Cámbialo antes de distribuir el enlace ampliamente.
