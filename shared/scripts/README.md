# 🛠️ Scripts Compartidos

> Scripts y utilidades reutilizables por todos los agentes del sistema.

---

## 📁 Estructura

```
shared/scripts/
├── README.md                  # Esta documentación
├── tiktok_producer.py         # Pipeline completo TikTok
├── video/                     # Scripts de generación de video
│   ├── video_generator.py     # Generador principal de videos
│   ├── pexels_client.py       # Cliente API de Pexels
│   └── subtitle_generator.py  # Generador de subtítulos ASS
├── audio/                     # Scripts de audio
│   └── tts_generator.py       # Generador TTS (Edge-TTS)
└── utils/                     # Utilidades generales
    └── ffmpeg_utils.py        # Funciones helper de FFmpeg
```

---

## 🎬 Scripts de Video

### video_generator.py

**Propósito**: Generación completa de videos para plataformas (YouTube Shorts, TikTok, Instagram Reels).

**Características**:

- Múltiples fuentes de fondo (stock, animado, espacio)
- Soporte para Pexels API (videos e imágenes)
- Efecto Ken Burns en imágenes
- Fondos animados generados con FFmpeg
- Subtítulos ASS profesionales

**Uso**:

```python
from shared.scripts.video.video_generator import ShortVideoGenerator

generator = ShortVideoGenerator(pexels_api_key="TU_KEY")
result = generator.generate_short(
    audio_path="/path/to/audio.mp3",
    subtitle_path="/path/to/subs.ass",  # Opcional
    output_path="/path/to/output.mp4",
    keywords=["space", "stars"],
    style="stock_video"  # stock_video | stock_images | animated | space
)
```

**Estilos disponibles**:

| Estilo         | Descripción                 | Requisitos     |
| -------------- | --------------------------- | -------------- |
| `stock_video`  | Videos de Pexels como fondo | API Key Pexels |
| `stock_images` | Imágenes con Ken Burns      | API Key Pexels |
| `animated`     | Gradientes y partículas     | Solo FFmpeg    |
| `space`        | Estrellas y nebulosas       | Solo FFmpeg    |
| `auto`         | Selección automática        | -              |

---

### tiktok_producer.py

**Propósito**: Pipeline completo de producción de videos TikTok. Integra TTS, stock videos, composición y subtítulos en un solo script.

**Características**:

- Generación automática de audio TTS (Edge-TTS)
- Descarga inteligente de videos stock (Pexels)
- Composición de video 9:16 (1080x1920)
- Subtítulos ASS con estilo viral (palabras clave resaltadas)
- Limpieza automática de temporales

**Uso como módulo**:

```python
from shared.scripts.tiktok_producer import TikTokProducer

producer = TikTokProducer(
    output_dir="/path/to/tiktok/assets",
    config={
        "voice": "es-ES-AlvaroNeural",
        "voice_rate": "+5%",
        "resolution": (1080, 1920),
        "fps": 30
    }
)

result = producer.produce(
    script_text="Tu guion aquí...",
    video_id="idea-001",
    keywords=["mirror", "brain", "psychology"]
)
```

**Uso CLI**:

```bash
python tiktok_producer.py \
    --script "Texto del guion..." \
    --id "video-001" \
    --output "/tiktok/assets" \
    --keywords mirror brain psychology
```

**Resultado**:

```json
{
  "video_id": "idea-001",
  "success": true,
  "duration": 30.14,
  "size_mb": 16.2,
  "files": {
    "audio": "audio/narration-idea-001.mp3",
    "video": "video/final/idea-001-final.mp4",
    "subtitles_ass": "video/subtitles-idea-001.ass"
  }
}
```

---

### pexels_client.py

**Propósito**: Interactuar con la API de Pexels para obtener videos e imágenes gratuitos.

**Límites gratuitos**:

- 200 requests/hora
- 20,000 requests/mes
- Sin atribución obligatoria para videos

**Uso**:

```python
from shared.scripts.video.pexels_client import PexelsClient

client = PexelsClient(api_key="TU_KEY")

# Buscar videos verticales
videos = client.search_videos(
    query="stars space",
    orientation="portrait",
    count=5
)

# Buscar imágenes
images = client.search_images(
    query="nature landscape",
    orientation="portrait",
    count=10
)

# Descargar video
local_path = client.download_video(videos[0], "/tmp/video.mp4")
```

---

### subtitle_generator.py

**Propósito**: Generar subtítulos en formato ASS con estilos profesionales.

**Uso**:

```python
from shared.scripts.video.subtitle_generator import SubtitleGenerator

gen = SubtitleGenerator()

# Desde texto dividido en líneas
gen.from_text(
    text="Línea uno\nLínea dos\nLínea tres",
    duration=30.0,
    output_path="/path/to/subs.ass"
)

# Desde archivo de script
gen.from_script(
    script_path="/path/to/script.md",
    audio_duration=60.0,
    output_path="/path/to/subs.ass"
)
```

---

## 🎙️ Scripts de Audio

### tts_generator.py

**Propósito**: Generar narración con Text-to-Speech usando Edge-TTS.

**Voces recomendadas (español)**:

- `es-ES-AlvaroNeural` - Masculina, clara
- `es-ES-ElviraNeural` - Femenina, profesional
- `es-MX-JorgeNeural` - Mexicana masculina
- `es-AR-ElenaNeural` - Argentina femenina

**Uso**:

```python
from shared.scripts.audio.tts_generator import TTSGenerator

tts = TTSGenerator(voice="es-ES-AlvaroNeural")

# Generar audio
audio_path = tts.generate(
    text="Tu texto para narrar aquí...",
    output_path="/path/to/audio.mp3",
    rate="+0%",  # Velocidad (-50% a +100%)
    pitch="+0Hz"  # Tono (-50Hz a +50Hz)
)
```

---

## 🔧 Utilidades

### ffmpeg_utils.py

**Funciones disponibles**:

```python
from shared.scripts.utils.ffmpeg_utils import (
    get_duration,        # Obtener duración de audio/video
    get_video_info,      # Obtener info completa del video
    normalize_audio,     # Normalizar volumen
    concat_videos,       # Concatenar videos
    add_audio_to_video,  # Añadir pista de audio
    scale_video,         # Redimensionar video
    loop_video           # Hacer loop de video
)

# Ejemplos
duration = get_duration("/path/to/file.mp4")
info = get_video_info("/path/to/video.mp4")
```

---

## ⚙️ Configuración

Los scripts buscan configuración en estos archivos (en orden):

1. `/config/credentials.env` - API keys y credenciales
2. `/config/global.json` - Configuración general
3. Variables de entorno del sistema

### Ejemplo credentials.env

```env
PEXELS_API_KEY=tu_key_aqui
PIXABAY_API_KEY=opcional
DEFAULT_VIDEO_STYLE=stock_video
ENABLE_KEN_BURNS=true
```

---

## 📋 Dependencias

```bash
# Python
pip install requests edge-tts

# Sistema
sudo apt install ffmpeg
```

---

## 🔗 Uso desde Agentes

Los agentes pueden importar estos scripts desde sus carpetas:

```python
import sys
sys.path.insert(0, '/home/illodev/projects/automated-content')

from shared.scripts.video.video_generator import ShortVideoGenerator
from shared.scripts.audio.tts_generator import TTSGenerator
```

O usando paths relativos desde el workspace.
