# 🎬 Agente de Carga

Este documento explica cómo cargar y activar agentes en el sistema.

## Concepto

Cada agente es un rol especializado que el asistente de IA (Copilot) puede asumir. Al proporcionar el `MASTER-PROMPT.md` como contexto, el agente "cobra vida" y opera de forma autónoma.

## Cómo Cargar un Agente

### Método 1: Contexto Directo

1. Abre el archivo `MASTER-PROMPT.md` del agente
2. Selecciona todo el contenido (Ctrl+A)
3. En el chat de Copilot, adjunta el archivo como contexto
4. Escribe: "Asume este rol y ejecuta"

### Método 2: Referencia en Chat

```
@workspace Carga el agente de YouTube desde /youtube/MASTER-PROMPT.md y ejecuta el pipeline completo
```

### Método 3: Instrucción Directa

```
Lee el archivo /youtube/MASTER-PROMPT.md, asume ese rol y comienza la ejecución autónoma.
```

## Flujo de Activación

```
┌─────────────────────────────────────────────────────────────┐
│                    CARGA DEL AGENTE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Usuario proporciona MASTER-PROMPT.md                    │
│                    ↓                                        │
│  2. IA procesa e internaliza el rol                         │
│                    ↓                                        │
│  3. IA carga configuración (config.json)                    │
│                    ↓                                        │
│  4. IA verifica skills disponibles                          │
│                    ↓                                        │
│  5. IA inicia ejecución autónoma                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Persistencia de Estado

Aunque cada sesión de chat es independiente, el agente persiste su estado mediante:

- **config.json**: Configuración actual
- **state.json**: Estado de la última ejecución
- **logs/**: Historial de acciones
- **skills/**: Habilidades generadas

Al recargar el agente, debe leer estos archivos para recuperar contexto.

## Comandos de Control

El usuario puede controlar el agente con comandos:

| Comando     | Acción                    |
| ----------- | ------------------------- |
| `INICIAR`   | Comenzar ejecución        |
| `PAUSAR`    | Detener temporalmente     |
| `ESTADO`    | Mostrar estado actual     |
| `LOGS`      | Mostrar últimos logs      |
| `REINICIAR` | Reset y comenzar de nuevo |

## Múltiples Agentes

Para ejecutar múltiples agentes:

1. Abrir una ventana/sesión de chat por agente
2. Cargar cada agente en su sesión
3. Los agentes comparten recursos de `shared/`
4. Cada agente mantiene su propio estado

## Consideraciones

- El agente debe validar su configuración antes de ejecutar
- Si falta configuración, debe crearla o solicitarla
- Los errores críticos deben documentarse en logs
- El agente debe ser resiliente a fallos
