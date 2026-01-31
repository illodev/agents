# 🎬 Agente de YouTube

Agente **totalmente autónomo** para creación y publicación de contenido en YouTube.

## 📋 Descripción

Este agente se encarga del ciclo completo de producción de videos **sin intervención humana**:

### 🚀 Setup Autónomo (Fase 0)

- **Investigación de nicho**: Analiza y decide qué nicho es más rentable
- **Creación de cuentas**: Crea cuenta Google/YouTube si no existe
- **Gestión de credenciales**: Almacena de forma segura y encriptada

### 📹 Producción de Contenido (Fases 1-9)

- Generación de ideas virales
- Escritura de guiones optimizados
- Producción de audio y video
- Optimización SEO
- Subida automatizada via Playwright
- Análisis y aprendizaje continuo

## 🚀 Cómo Usar

### 1. Activar el Agente (Sin configuración previa)

El agente es capaz de configurarse solo:

1. Abre [MASTER-PROMPT.md](MASTER-PROMPT.md)
2. Envíalo como contexto al chat de Copilot
3. Escribe `INICIAR`

El agente automáticamente:

- ✅ Detectará que no hay credenciales
- ✅ Investigará el mejor nicho
- ✅ Creará la cuenta necesaria (puede requerir verificación SMS)
- ✅ Configurará todo y comenzará a producir

### 2. Configuración Manual (Opcional)

Si prefieres configurar manualmente:

```bash
# Copiar credenciales
cp ../../config/credentials.env.example ../../config/credentials.env
nano ../../config/credentials.env

# Editar configuración
nano config/config.json
```

### 3. Comandos Disponibles

| Comando                  | Descripción                          |
| ------------------------ | ------------------------------------ |
| `INICIAR`                | Comenzar ejecución autónoma completa |
| `ESTADO`                 | Ver estado actual del pipeline       |
| `INVESTIGAR NICHO`       | Forzar nueva investigación de nicho  |
| `VERIFICAR CREDENCIALES` | Verificar estado de credenciales     |
| `CREAR CUENTA`           | Forzar creación de cuenta nueva      |
| `PAUSAR`                 | Detener ejecución                    |
| `LOGS`                   | Ver últimas acciones                 |
| `MÉTRICAS`               | Ver analytics                        |
| `CONFIG`                 | Ver/editar configuración             |

## 📁 Estructura

```
youtube/
├── MASTER-PROMPT.md      # Identidad del agente
├── README.md             # Este archivo
├── config/               # Configuración
│   ├── config.json       # Config principal
│   ├── state.json        # Estado actual
│   └── niche-research.json # Investigación de nicho
├── skills/               # Habilidades del agente
│   ├── content/          # Creación de contenido
│   ├── research/         # Investigación (nicho)
│   ├── platform/         # Cuentas, subida
│   ├── media/            # Manipulación de medios
│   ├── platform/         # Interacción con YouTube
│   └── automation/       # Automatización
├── assets/               # Contenido generado
│   ├── ideas/            # Ideas y metadata
│   ├── scripts/          # Guiones
│   ├── audio/            # Archivos de voz
│   ├── video/            # Videos
│   └── thumbnails/       # Miniaturas
├── logs/                 # Registros
├── analytics/            # Métricas
└── history/              # Historial
```

## 🧠 Skills

El agente puede usar y crear skills. Ver [skills/skills-index.json](skills/skills-index.json).

### Skills Incluidas

| Skill                   | Categoría  | Descripción                      |
| ----------------------- | ---------- | -------------------------------- |
| `generar-ideas-virales` | content    | Genera ideas con potencial viral |
| `crear-guion-short`     | content    | Guiones para Shorts              |
| `subir-video-youtube`   | platform   | Subida via Playwright            |
| `manejar-errores`       | automation | Sistema de errores               |

### Auto-Generación

El agente puede crear nuevas skills cuando:

- Detecta tareas repetitivas
- Descubre procesos más eficientes
- Necesita manejar errores nuevos

## 📊 Métricas

El agente rastrea:

- CTR (Click-Through Rate)
- Retención promedio
- Visualizaciones
- Engagement

Ver [analytics/metrics.json](analytics/metrics.json).

## ⚠️ Requisitos

- Playwright instalado
- Cuenta de YouTube/Google
- APIs configuradas (opcional):
  - ElevenLabs (TTS)
  - Pexels/Pixabay (stock media)

## 🔒 Seguridad

- Las credenciales van en `/config/credentials.env` (gitignored)
- Nunca subir credenciales a repositorios
- La sesión de Playwright se guarda localmente

---

_Parte del proyecto [Automated Content Agents](../README.md)_
