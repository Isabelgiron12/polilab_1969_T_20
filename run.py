#!/usr/bin/env python3
import os
import subprocess
import sys

# Descarga el logo si no existe
if not os.path.exists('logo.webp'):
    print("📥 Descargando logo...")
    result = os.system('curl -o logo.webp https://github.com/Isabelgiron12/polilab_1969_T_20/raw/main/logo.webp')
    if result == 0:
        print("✓ Logo descargado")
    else:
        print("⚠ No se pudo descargar, descárgalo manualmente")

# Levanta el servidor
print("\n" + "="*50)
print("✓ Servidor corriendo")
print("="*50)
print("\n🌐 Abre en tu navegador: http://localhost:8000\n")
print("Presiona Ctrl+C para detener el servidor\n")

os.system('python3 -m http.server 8000')
