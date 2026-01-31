# 🤖 Automated Content Agents

Sistema de agentes autónomos para generación y monetización de contenido digital.

## 📋 Descripción

Este proyecto implementa un ecosistema de agentes AI especializados que operan de forma autónoma para crear, publicar y optimizar contenido en múltiples plataformas. Cada agente tiene su propio dominio de responsabilidad y puede auto-generar nuevas habilidades (skills) según las necesidades.

## 🏗️ Arquitectura

```
automated-content/
├── README.md                    # Este archivo
├── config/                      # Configuración global
│   ├── global.json             # Configuración compartida
│   └── credentials.env         # Variables de entorno (gitignore)
├── core/                        # Núcleo del sistema
│   ├── agent-loader.md         # Cómo cargar agentes
│   └── skill-generator.md      # Sistema de auto-generación de skills
├── shared/                      # Recursos compartidos
│   ├── prompts/                # Prompts reutilizables
│   └── utils/                  # Utilidades comunes
└── youtube/                     # Agente de YouTube
    ├── MASTER-PROMPT.md        # Prompt principal del agente
    ├── config/                 # Configuración del agente
    ├── skills/                 # Habilidades del agente
    ├── assets/                 # Assets generados
    ├── logs/                   # Registros de actividad
    └── analytics/              # Métricas y análisis
```

## 🎯 Agentes Disponibles

| Agente      | Estado       | Descripción                      |
| ----------- | ------------ | -------------------------------- |
| **YouTube** | 🟢 Activo    | Creación y publicación de videos |
| TikTok      | 🔴 Pendiente | Próximamente                     |
| Blog        | 🔴 Pendiente | Próximamente                     |

## 🚀 Cómo Usar

### 1. Configuración Inicial

```bash
# Copiar configuración de ejemplo
cp config/credentials.env.example config/credentials.env

# Editar con tus credenciales
nano config/credentials.env
```

### 2. Activar un Agente

En VS Code con Copilot:

1. Abre el archivo `MASTER-PROMPT.md` del agente deseado
2. Selecciona todo el contenido
3. Envíalo como contexto al agente de Copilot
4. El agente asumirá ese rol automáticamente

### 3. Ejecución Autónoma

El agente ejecutará su pipeline de forma autónoma:

- Generará contenido según su configuración
- Usará Playwright para interacciones web
- Registrará todas las acciones en logs
- Auto-generará nuevas skills si es necesario

## 🧠 Sistema de Skills

Los agentes pueden auto-generar nuevas habilidades:

1. **Detección**: El agente detecta una tarea repetitiva o nueva necesidad
2. **Análisis**: Evalúa si existe una skill similar
3. **Generación**: Crea una nueva skill documentada
4. **Registro**: La añade a su inventario de skills
5. **Uso**: La utiliza en futuras ejecuciones

Ver [core/skill-generator.md](core/skill-generator.md) para más detalles.

## 📊 Monitoreo

Cada agente mantiene:

- **Logs diarios**: Registro de todas las acciones
- **Analytics**: Métricas de rendimiento
- **Historial**: Contenido generado y publicado

## ⚠️ Consideraciones

- Todo contenido debe ser **original y transformado**
- Cumplir con las **políticas de cada plataforma**
- No infringir **copyright**
- Priorizar **calidad sobre cantidad**

## 📄 Licencia

Uso privado - No redistribuir sin autorización.

---

_Última actualización: Enero 2026_
