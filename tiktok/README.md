# 🎵 Agente Autónomo TikTok

Agente especializado en creación y publicación de contenido viral en TikTok.

## 🚀 Inicio Rápido

1. Abre `MASTER-PROMPT.md` en VS Code
2. Selecciona todo el contenido
3. Envíalo como contexto al agente de Copilot
4. Usa el comando `INICIAR`

## 📊 Estado Actual

Ver `config/state.json` para el estado de la sesión actual.

## 🎯 Diferencias con YouTube

| Aspecto    | TikTok           | YouTube            |
| ---------- | ---------------- | ------------------ |
| Duración   | 15-60s           | 60s-10min          |
| Hook       | 0.5-1s           | 3s                 |
| Frecuencia | 3-5/día          | 1-2/día            |
| Algoritmo  | FYP + engagement | Suscriptores + SEO |
| Música     | Trending sounds  | Opcional           |

## 📁 Estructura

```
tiktok/
├── MASTER-PROMPT.md      # Prompt principal
├── README.md             # Este archivo
├── config/
│   ├── config.json       # Configuración
│   ├── state.json        # Estado actual
│   └── trending-sounds.json
├── skills/               # Habilidades del agente
├── assets/               # Contenido generado
├── analytics/            # Métricas
├── history/              # Historial
└── logs/                 # Registros
```

## 🔗 Scripts Compartidos

Este agente usa los scripts compartidos en `/shared/scripts/`:

```python
from shared.scripts.video import VideoGenerator, create_short
from shared.scripts.audio import TTSGenerator, generate_narration
from shared.scripts.utils import get_duration
```

## ⚠️ Notas Importantes

- TikTok requiere hooks en el primer segundo
- Evitar CTAs agresivos (riesgo de shadowban)
- Publicar 3-5 videos diarios para mejor alcance
- Los trending sounds aumentan significativamente el FYP
