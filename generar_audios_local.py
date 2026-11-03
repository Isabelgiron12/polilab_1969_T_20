#!/usr/bin/env python3
"""
Genera los audios MP3 del juego en local (sin internet ni API) con Piper.

Usa las mismas frases que generar_audios_elevenlabs.py.

Requisitos:
    pip install piper-tts lameenc
    Voz: un .onnx y su .onnx.json de https://huggingface.co/rhasspy/piper-voices
    En Mac, copiar piper/espeak-ng-data a ~/.cache/piper/ (espeak falla con rutas largas)

Uso:
    python3 generar_audios_local.py RUTA/voz.onnx            # genera los que faltan en audio/
    python3 generar_audios_local.py RUTA/voz.onnx --todos    # regenera todos
    python3 generar_audios_local.py RUTA/voz.onnx --solo inicio1 inicio2
"""

import ast
import os
import sys
from pathlib import Path

import lameenc
from piper import PiperVoice, SynthesisConfig

AQUI = Path(__file__).parent
ESPEAK = Path(os.path.expanduser('~/.cache/piper/espeak-ng-data'))


def leer_frases():
    """Lee el diccionario FRASES de generar_audios_elevenlabs.py sin importarlo."""
    arbol = ast.parse((AQUI / 'generar_audios_elevenlabs.py').read_text(encoding='utf-8'))
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and nodo.targets[0].id == 'FRASES':
            return ast.literal_eval(nodo.value)
    raise SystemExit('No encontré FRASES en generar_audios_elevenlabs.py')


def a_mp3(voz, texto, config):
    pcm = bytearray()
    tasa = voz.config.sample_rate
    for trozo in voz.synthesize(texto, config):
        pcm += trozo.audio_int16_bytes
        # Pausa corta entre oraciones
        pcm += bytes(int(tasa * 0.25) * 2)
    enc = lameenc.Encoder()
    enc.set_bit_rate(96)
    enc.set_in_sample_rate(tasa)
    enc.set_channels(1)
    enc.set_quality(2)
    return enc.encode(bytes(pcm)) + enc.flush()


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    voz = PiperVoice.load(args[0], espeak_data_dir=ESPEAK) if ESPEAK.exists() else PiperVoice.load(args[0])
    frases = leer_frases()
    if '--solo' in args:
        claves = args[args.index('--solo') + 1:]
        frases = {k: frases[k] for k in claves}
    todos = '--todos' in args or '--solo' in args

    salida = AQUI / 'audio'
    salida.mkdir(exist_ok=True)
    # Un poco más lento que el ritmo por defecto, para que se entienda en sala
    config = SynthesisConfig(length_scale=1.08)

    hechos = 0
    for nombre, texto in frases.items():
        archivo = salida / f'{nombre}.mp3'
        if archivo.exists() and not todos:
            continue
        archivo.write_bytes(a_mp3(voz, texto, config))
        hechos += 1
        print(f'✅ {nombre}.mp3')
    print(f'\n✨ {hechos} audios generados en {salida}/')


if __name__ == '__main__':
    main()
