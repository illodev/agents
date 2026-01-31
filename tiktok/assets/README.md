# 🎵 Agente TikTok - Assets

Esta carpeta contiene los assets generados por el agente de TikTok.

## 📁 Estructura

```
assets/
├── ideas/           # Ideas generadas (JSON)
├── scripts/         # Guiones escritos (MD)
├── audio/           # Narraciones TTS (MP3)
├── video/
│   ├── raw/         # Videos en proceso
│   └── final/       # Videos listos para publicar
└── thumbnails/      # (No usado en TikTok pero disponible)
```

## 🔄 Flujo de Archivos

1. `ideas/ideas-{fecha}.json` → Ideas del día
2. `scripts/script-{id}.md` → Guion de la idea
3. `audio/audio-{id}.mp3` → Narración generada
4. `video/final/tiktok-{id}.mp4` → Video final

## 📏 Especificaciones de Video

- **Resolución**: 1080x1920 (9:16)
- **FPS**: 30
- **Codec**: H.264 + AAC
- **Duración**: 15-60 segundos (óptimo 30s)
- **Tamaño máximo**: 287.6 MB (pero preferir <100MB)

## 🧹 Limpieza

Los archivos en `raw/` pueden borrarse después de generar el video final.
Los archivos en `final/` se mantienen como backup hasta confirmar publicación exitosa.
