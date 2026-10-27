# 🎙️ Generar Audios con Google Cloud TTS

Script para generar audios MP3 de máxima calidad usando Google Cloud Text-to-Speech.

---

## 📋 Requisitos

1. **Cuenta Google Cloud** (ya la tienes)
2. **$300 en créditos gratis** (suficiente para ~20M caracteres)
3. **Python 3.7+**
4. **Google Cloud SDK configurado**

---

## 🚀 Pasos

### 1. Instalar dependencia
```bash
pip install google-cloud-texttospeech
```

### 2. Autenticar con Google Cloud
```bash
# Descargar JSON de credenciales desde Google Cloud Console
# Luego:
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

### 3. Generar audios
```bash
python generar_audios.py
```

Genera 30+ audios MP3 en `polilab_1969_T_20/audio/`

---

## 📊 Costo estimado

- **30 audios** ≈ 3,000 caracteres
- **Google Cloud TTS**: $16 por 1M caracteres
- **Total**: ~$0.05 por juego
- **Con $300**: Puedes generar 6,000+ juegos

---

## 🎵 Archivos generados

```
audio/
├── bienvenida.mp3
├── faseDecision.mp3
├── decisionGO.mp3
├── anuncioDespido.mp3
├── reflexionFinal.mp3
└── ... (30+ más)
```

---

## 🔌 Próximo paso

Una vez generes los audios, el juego puede reproducirlos:

```javascript
// En lugar de síntesis TTS
const audio = new Audio('audio/bienvenida.mp3');
audio.play();
```

---

## 💡 Ventajas

✅ Voces naturales profesionales
✅ Acento latino perfecto
✅ Sin latencia (audios pregrabados)
✅ Funciona offline
✅ Máxima calidad

---

## ⚠️ Importante

- Guarda los archivos de credenciales en `.gitignore`
- No commits credenciales a GitHub
- Los audios SÍ se pueden commitear (son archivos de media)
