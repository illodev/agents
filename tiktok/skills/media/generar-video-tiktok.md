# 🎬 Skill: Generar Video TikTok

> **Categoría**: media  
> **Versión**: 1.0  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Genera videos optimizados para TikTok usando los scripts compartidos. Incluye visuales de stock, subtítulos estilo TikTok y optimización para el formato vertical.

---

## 🎯 Cuándo Usar

- Después de tener audio generado
- Para producir el video final
- Cuando se necesita re-renderizar con diferente estilo

---

## ⚙️ Requisitos

### Archivos de Entrada

- `audio_path`: MP3 con narración
- `script_text`: Texto del guion (para subtítulos)
- `keywords`: Lista de palabras clave para stock footage

### Configuración

- Pexels API Key en `/config/credentials.env`
- FFmpeg instalado

---

## 📐 Especificaciones TikTok

| Parámetro   | Valor Requerido   |
| ----------- | ----------------- |
| Resolución  | 1080x1920 (9:16)  |
| FPS         | 30                |
| Codec Video | H.264             |
| Codec Audio | AAC 128kbps       |
| Duración    | 15-60s (max 180s) |
| Formato     | MP4               |

---

## 📝 Proceso

### Paso 1: Preparar Entorno

```python
import sys
sys.path.insert(0, '/home/illodev/projects/automated-content')

from shared.scripts.video import VideoGenerator, VideoStyle, create_short
from shared.scripts.video import SubtitleGenerator
from shared.scripts.audio import TTSGenerator
from shared.scripts.utils import get_duration
```

### Paso 2: Analizar Audio

```python
audio_path = "/home/illodev/projects/automated-content/tiktok/assets/audio/narration.mp3"
duration = get_duration(audio_path)

print(f"Duración del audio: {duration}s")

# Verificar que está dentro de límites TikTok
if duration > 180:
    raise ValueError("Audio demasiado largo para TikTok (max 3 min)")
```

### Paso 3: Extraer Keywords del Guion

```python
# Ejemplo de keywords basadas en el guion
script_content = """
El 90% de las personas no saben ESTO.
Hay más estrellas en el universo que granos de arena en la Tierra.
"""

# Keywords para buscar en Pexels
keywords = ["stars", "universe", "space", "galaxy", "night sky"]
```

### Paso 4: Generar Video con Script Compartido

```python
# Opción 1: Función rápida
result = create_short(
    audio_path="/tiktok/assets/audio/narration.mp3",
    output_path="/tiktok/assets/video/final/tiktok-001.mp4",
    keywords=["stars", "space", "universe"],
    subtitle_text=script_content,
    style="stock_video"  # Usar videos de Pexels
)

print(f"Video generado: {result['output_path']}")
print(f"Duración: {result['duration']}s")
```

```python
# Opción 2: Con más control
generator = VideoGenerator()

result = generator.generate(
    audio_path="/tiktok/assets/audio/narration.mp3",
    output_path="/tiktok/assets/video/final/tiktok-001.mp4",
    style=VideoStyle.STOCK_VIDEO,
    keywords=["stars", "space", "galaxy"],
    subtitle_text=script_content,
    resolution="shorts",  # 1080x1920
    fps=30,
    subtitle_style="bold_center"  # Estilo TikTok
)
```

### Paso 5: Subtítulos Estilo TikTok

```python
# Si necesitas generar subtítulos por separado
from shared.scripts.video import SubtitleGenerator

gen = SubtitleGenerator(style="bold_center")

# Configuración TikTok-specific
gen.font_size = 85  # Más grande para TikTok
gen.margin_v = 500  # Más arriba (evitar UI de TikTok)
gen.max_words = 3   # Menos palabras por frame

gen.from_text(
    text=script_content,
    duration=duration,
    output_path="/tiktok/assets/video/raw/subs.ass"
)
```

### Paso 6: Estilos de Video Disponibles

| Estilo         | Descripción                  | Uso Recomendado               |
| -------------- | ---------------------------- | ----------------------------- |
| `stock_video`  | Videos de Pexels             | General, mejor engagement     |
| `stock_images` | Imágenes con Ken Burns       | Datos, educativo              |
| `animated`     | Gradientes animados          | Cuando no hay stock relevante |
| `space`        | Fondo espacial con estrellas | Contenido de espacio/cosmos   |
| `auto`         | Selección automática         | Por defecto                   |

### Paso 7: Post-procesamiento TikTok

```python
# Ajustes específicos para TikTok (si necesario)
import subprocess

input_video = "/tiktok/assets/video/final/tiktok-001.mp4"
output_video = "/tiktok/assets/video/final/tiktok-001-optimized.mp4"

# Asegurar codec y bitrate óptimos para TikTok
cmd = [
    "ffmpeg", "-i", input_video,
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "18",           # Alta calidad
    "-c:a", "aac",
    "-b:a", "128k",
    "-movflags", "+faststart",  # Importante para streaming
    "-y", output_video
]

subprocess.run(cmd, check=True)
```

---

## 🎨 Safe Zones TikTok

```
┌──────────────────────────────────┐
│                                  │ ← Top 150px: Username, etc
│   ┌──────────────────────────┐   │
│   │                          │   │
│   │    ZONA SEGURA           │   │
│   │    PARA CONTENIDO        │   │
│   │    Y SUBTÍTULOS          │   │
│   │                          │   │
│   │                          │   │
│   └──────────────────────────┘   │ ← Right 100px: Botones
│                                  │
│   [Caption/descripción]          │ ← Bottom 200px: Caption area
└──────────────────────────────────┘

Subtítulos: Centrar verticalmente, evitar extremos
```

---

## 🔧 Troubleshooting

### Error: "No se encontraron videos en Pexels"

```python
# Solución: Usar keywords más genéricos o cambiar estilo
result = create_short(
    ...
    keywords=["abstract", "colorful", "motion"],  # Más genérico
    style="animated"  # Fallback sin API
)
```

### Error: "Video muy largo"

```python
# Verificar duración antes de generar
duration = get_duration(audio_path)
if duration > 60:
    print("Advertencia: Video largo para TikTok, considerar editar")
```

### Error: "Subtítulos fuera de frame"

```python
# Ajustar margin para TikTok
gen = SubtitleGenerator()
gen.margin_v = 500  # Subir subtítulos para evitar UI
```

---

## 📁 Archivos Generados

```
tiktok/assets/video/
├── raw/
│   ├── background.mp4      # Video de fondo descargado
│   └── subs.ass            # Subtítulos generados
└── final/
    └── tiktok-001.mp4      # Video final listo para subir
```

---

## ✅ Criterios de Éxito

- [ ] Resolución: 1080x1920
- [ ] Duración: 15-60 segundos
- [ ] Codec: H.264 + AAC
- [ ] Subtítulos visibles y en safe zone
- [ ] Sin contenido estático >2 segundos
- [ ] Archivo final <100MB (límite TikTok)
