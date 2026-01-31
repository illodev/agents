# 🎬 Skill: Generar Video con Stock (Pexels)

> **Categoría**: media  
> **Prioridad**: Alta  
> **Dependencias**: FFmpeg, Pexels API Key  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Genera videos atractivos para YouTube Shorts usando contenido de stock de Pexels como fondo, combinado con narración de audio y subtítulos profesionales.

---

## 🎯 Cuándo Usar

- Al crear videos para YouTube Shorts, TikTok o Reels
- Cuando se necesita contenido visual de alta calidad sin crear desde cero
- Para videos de formato vertical (9:16)
- Cuando el nicho requiere visuales específicos (naturaleza, espacio, ciudades, etc.)

---

## ⚙️ Requisitos

### Archivos de Entrada

- `audio_path`: Archivo MP3 con la narración
- `script_text`: Texto del guion (opcional, para subtítulos)

### Configuración

- Pexels API Key en `/config/credentials.env`
- FFmpeg instalado en el sistema

### Keywords

- Lista de palabras clave relacionadas con el contenido
- Ejemplo: `["stars", "space", "universe"]` para contenido de astronomía

---

## 📝 Proceso

### Paso 1: Preparar Entorno

```python
import sys
sys.path.insert(0, '/home/illodev/projects/automated-content')

from shared.scripts.video import VideoGenerator, VideoStyle
from shared.scripts.video import SubtitleGenerator
from shared.scripts.utils import get_duration
```

### Paso 2: Extraer Keywords del Guion

```python
def extract_keywords(script_text: str) -> list:
    """Extrae palabras clave relevantes del guion"""
    # Palabras comunes a ignorar
    stopwords = ['el', 'la', 'los', 'las', 'un', 'una', 'que', 'de', 'en', 'y', 'a']

    words = script_text.lower().split()
    keywords = []

    for word in words:
        word = word.strip('.,!?¿¡')
        if len(word) > 4 and word not in stopwords:
            if word not in keywords:
                keywords.append(word)

    return keywords[:5]  # Máximo 5 keywords
```

### Paso 3: Generar Subtítulos

```python
# Si hay texto de guion, generar subtítulos
if script_text:
    sub_gen = SubtitleGenerator(style="default")
    audio_duration = get_duration(audio_path)

    subtitle_path = sub_gen.from_text(
        text=script_text,
        duration=audio_duration,
        output_path=f"{output_dir}/subtitles.ass"
    )
```

### Paso 4: Generar Video

```python
generator = VideoGenerator()

result = generator.generate(
    audio_path=audio_path,
    output_path=output_path,
    style=VideoStyle.STOCK_VIDEO,  # Usar videos de Pexels
    keywords=keywords,
    subtitle_text=script_text,
    resolution="shorts"  # 1080x1920
)

if result["success"]:
    print(f"✅ Video generado: {result['output']}")
    print(f"   Duración: {result['duration']}s")
    print(f"   Tamaño: {result['size_mb']} MB")
else:
    print(f"❌ Error: {result['error']}")
```

---

## 🎨 Estilos Alternativos

Si Pexels no tiene contenido adecuado o se agotan requests:

```python
# Opción 1: Imágenes con Ken Burns
result = generator.generate(
    ...,
    style=VideoStyle.STOCK_IMAGES
)

# Opción 2: Fondo animado (sin API)
result = generator.generate(
    ...,
    style=VideoStyle.ANIMATED
)

# Opción 3: Fondo espacial (sin API)
result = generator.generate(
    ...,
    style=VideoStyle.SPACE
)

# Opción 4: Selección automática
result = generator.generate(
    ...,
    style=VideoStyle.AUTO  # Elige según disponibilidad
)
```

---

## 📊 Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                   GENERAR VIDEO STOCK                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Recibir audio + guion                                   │
│              ↓                                              │
│  2. Extraer keywords del guion                              │
│              ↓                                              │
│  3. Buscar videos en Pexels API                             │
│     └─ Si no hay → usar estilo alternativo                  │
│              ↓                                              │
│  4. Descargar mejor video                                   │
│              ↓                                              │
│  5. Escalar a 1080x1920 + loop                              │
│              ↓                                              │
│  6. Generar subtítulos ASS                                  │
│              ↓                                              │
│  7. Componer: fondo + audio + subtítulos                    │
│              ↓                                              │
│  8. Exportar MP4 (H.264, AAC)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Error: "No hay API key de Pexels"

1. Verificar que existe `/config/credentials.env`
2. Verificar que contiene `PEXELS_API_KEY=...`
3. La key debe tener permisos de lectura

### Error: "No se encontraron videos"

1. Probar con keywords más genéricos
2. Usar keywords en inglés (mejor cobertura)
3. Cambiar a estilo `ANIMATED` o `SPACE` como fallback

### Error: "Rate limit exceeded"

1. Esperar 1 hora (límite: 200/hora)
2. Usar estilos que no requieren API
3. Cachear videos descargados

---

## 📁 Archivos de Salida

```
youtube/assets/video/
├── raw/
│   ├── pexels_{id}.mp4      # Video de stock descargado
│   └── subtitles.ass        # Archivo de subtítulos
└── final/
    └── final-{idea_id}.mp4  # Video final compuesto
```

---

## 💡 Tips de Optimización

1. **Keywords en inglés**: Pexels tiene más contenido en inglés
2. **Ser específico**: "night sky stars" mejor que solo "stars"
3. **Caché de videos**: Guardar videos descargados para reutilizar
4. **Fallback automático**: Siempre tener plan B con estilos sin API

---

## 📚 Referencias

- Script principal: `/shared/scripts/video/video_generator.py`
- Cliente Pexels: `/shared/scripts/video/pexels_client.py`
- Subtítulos: `/shared/scripts/video/subtitle_generator.py`
- Documentación Pexels: https://www.pexels.com/api/documentation/
