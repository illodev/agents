# 🎙️ Skill: Generar Audio con TTS

> **Categoría**: media  
> **Prioridad**: Alta  
> **Dependencias**: edge-tts (Python package)  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Genera narración de voz de alta calidad usando Edge-TTS, el servicio de síntesis de voz de Microsoft. Gratuito y sin límites.

---

## 🎯 Cuándo Usar

- Al convertir guiones escritos a audio narrado
- Para crear voiceover de videos de YouTube
- Cuando se necesita voz natural en español u otros idiomas

---

## ⚙️ Requisitos

### Instalación

```bash
pip install edge-tts
```

### Verificar

```bash
edge-tts --list-voices | grep "es-"
```

---

## 📝 Proceso

### Paso 1: Preparar Texto

```python
# Limpiar texto para TTS
def preparar_texto(guion: str) -> str:
    # Eliminar marcas de markdown
    texto = guion.replace('**', '').replace('*', '')
    texto = texto.replace('[', '').replace(']', '')

    # Eliminar líneas de metadata
    lineas = []
    for linea in texto.split('\n'):
        if not linea.startswith('#'):
            if ':' not in linea[:20]:  # No es metadata
                lineas.append(linea)

    return ' '.join(lineas)
```

### Paso 2: Usar Script Compartido

```python
import sys
sys.path.insert(0, '/home/illodev/projects/automated-content')

from shared.scripts.audio import TTSGenerator, generate_narration

# Opción 1: Función rápida
audio_path = generate_narration(
    text="Tu guion preparado aquí...",
    output_path="/youtube/assets/audio/narration.mp3",
    voice="es-ES-AlvaroNeural",
    rate="+0%"  # Velocidad normal
)

# Opción 2: Con más control
tts = TTSGenerator(
    voice="es-ES-AlvaroNeural",
    rate="+5%",   # Un poco más rápido
    pitch="+0Hz"  # Tono normal
)
audio_path = tts.generate(texto, output_path)
```

### Paso 3: Generar Audio con Subtítulos SRT

```python
# Genera audio + timestamps sincronizados
result = tts.generate_with_srt(
    text=guion,
    audio_path="/youtube/assets/audio/narration.mp3",
    srt_path="/youtube/assets/audio/narration.srt",
    voice="es-ES-AlvaroNeural"
)

print(f"Audio: {result['audio']}")
print(f"SRT: {result['srt']}")
```

---

## 🎤 Voces Recomendadas

### Español

| ID de Voz            | Género    | Región    | Estilo              |
| -------------------- | --------- | --------- | ------------------- |
| `es-ES-AlvaroNeural` | Masculino | España    | Claro, profesional  |
| `es-ES-ElviraNeural` | Femenino  | España    | Profesional, cálido |
| `es-MX-JorgeNeural`  | Masculino | México    | Neutral             |
| `es-MX-DaliaNeural`  | Femenino  | México    | Amigable            |
| `es-AR-TomasNeural`  | Masculino | Argentina | Regional            |
| `es-AR-ElenaNeural`  | Femenino  | Argentina | Regional            |

### Inglés (para contenido internacional)

| ID de Voz           | Género    | Región |
| ------------------- | --------- | ------ |
| `en-US-GuyNeural`   | Masculino | USA    |
| `en-US-JennyNeural` | Femenino  | USA    |
| `en-GB-RyanNeural`  | Masculino | UK     |

### Listar todas las voces

```python
from shared.scripts.audio import TTSGenerator

# Todas las voces de español
voces = TTSGenerator.list_voices("es")
for v in voces:
    print(v["id"])
```

---

## ⚡ Ajustes de Velocidad y Tono

### Rate (Velocidad)

```python
# Más lento (para contenido técnico)
rate="-10%"

# Normal
rate="+0%"

# Más rápido (para energía)
rate="+15%"

# Máximo permitido
rate="+100%"  # o "-50%"
```

### Pitch (Tono)

```python
# Más grave
pitch="-20Hz"

# Normal
pitch="+0Hz"

# Más agudo
pitch="+20Hz"
```

---

## 📊 Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                   GENERAR AUDIO TTS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Recibir guion/script                                    │
│              ↓                                              │
│  2. Limpiar texto (quitar markdown, metadata)               │
│              ↓                                              │
│  3. Seleccionar voz según nicho/idioma                      │
│              ↓                                              │
│  4. Configurar velocidad/tono                               │
│              ↓                                              │
│  5. Generar con Edge-TTS                                    │
│              ↓                                              │
│  6. (Opcional) Normalizar volumen                           │
│              ↓                                              │
│  7. Exportar MP3                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Post-procesamiento

### Normalizar Volumen

```python
from shared.scripts.utils import normalize_audio

normalize_audio(
    input_path="/youtube/assets/audio/raw.mp3",
    output_path="/youtube/assets/audio/normalized.mp3",
    target_level=-16.0  # LUFS estándar
)
```

### Obtener Duración

```python
from shared.scripts.utils import get_duration

duracion = get_duration("/youtube/assets/audio/narration.mp3")
print(f"Duración: {duracion:.2f} segundos")
```

---

## 💡 Tips

1. **Pausas naturales**: Añade puntos y comas para pausas
2. **Énfasis**: Usa palabras cortas al inicio de frases para impacto
3. **Números**: Escríbelos como texto ("cien" no "100")
4. **Acrónimos**: Usa puntos para deletrear ("N.A.S.A.")

---

## 📁 Archivos de Salida

```
youtube/assets/audio/
├── narration-{fecha}-{id}.mp3     # Audio narrado
└── narration-{fecha}-{id}.srt     # Subtítulos (opcional)
```

---

## 📚 Referencias

- Script: `/shared/scripts/audio/tts_generator.py`
- Edge-TTS Docs: https://github.com/rany2/edge-tts
- Voces disponibles: `edge-tts --list-voices`
