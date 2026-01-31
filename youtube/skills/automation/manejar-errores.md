# Skill: manejar-errores

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: automation

## Descripción

Sistema estandarizado para detectar, registrar y recuperarse de errores durante la ejecución autónoma.

## Trigger

- Cualquier excepción o fallo en el pipeline
- Resultado inesperado de una operación
- Timeout en operaciones

## Prerequisitos

- Acceso a sistema de archivos para logs
- Estructura de logs creada

## Niveles de Error

### INFO

```
Situaciones normales que vale la pena registrar.
Acción: Solo registrar, continuar ejecución.

Ejemplos:
- Proceso completado exitosamente
- Archivo creado correctamente
- Conexión establecida
```

### WARNING

```
Algo no ideal pero manejable.
Acción: Registrar, intentar alternativa, continuar.

Ejemplos:
- API lenta (retry exitoso)
- Archivo no encontrado (usar default)
- Credencial por expirar
```

### ERROR

```
Fallo que impide completar una tarea.
Acción: Registrar, reintentar (max 3), saltar tarea si persiste.

Ejemplos:
- API no responde
- Archivo corrupto
- Timeout de operación
```

### CRITICAL

```
Fallo que impide continuar ejecución.
Acción: Registrar, detener ejecución, notificar.

Ejemplos:
- Sin acceso a YouTube
- Credenciales inválidas
- Sin espacio en disco
```

## Estructura de Log

```json
{
  "timestamp": "2026-01-31T10:30:00Z",
  "level": "ERROR",
  "component": "youtube-upload",
  "message": "Upload failed after 3 retries",
  "details": {
    "video_id": "idea-001",
    "error_code": "UPLOAD_TIMEOUT",
    "attempts": 3,
    "last_error": "Connection timeout after 60s"
  },
  "action_taken": "Skipped video, marked for manual review",
  "stack_trace": "..."
}
```

## Pasos de Manejo

### 1. Detectar Error

```
try {
  // Operación riesgosa
} catch (error) {
  handleError(error, context);
}
```

### 2. Clasificar Nivel

```
function classifyError(error) {
  if (error.code === 'AUTH_FAILED') return 'CRITICAL';
  if (error.code === 'TIMEOUT') return 'ERROR';
  if (error.code === 'RATE_LIMIT') return 'WARNING';
  return 'ERROR';
}
```

### 3. Registrar

```
function logError(level, component, message, details) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    component,
    message,
    details
  };

  // Guardar en logs/errors/error-{date}.json
  appendToLog(entry);

  // También a logs/daily/{date}.log
  appendToDailyLog(entry);
}
```

### 4. Decidir Acción

```
switch (level) {
  case 'INFO':
    continue();
    break;

  case 'WARNING':
    tryAlternative() || continue();
    break;

  case 'ERROR':
    for (let i = 0; i < 3; i++) {
      if (retry()) break;
      wait(30 * (i + 1)); // Backoff exponencial
    }
    if (!success) skipTask();
    break;

  case 'CRITICAL':
    stopExecution();
    notifyUser();
    break;
}
```

### 5. Recuperación

```
Estrategias de recuperación:

1. RETRY CON BACKOFF
   - Esperar tiempo incremental
   - 30s → 60s → 120s

2. ALTERNATIVA
   - Si API A falla, usar API B
   - Si TTS falla, usar otro provider

3. DEGRADACIÓN
   - Publicar sin thumbnail si falla generación
   - Usar descripción básica si SEO falla

4. SKIP
   - Saltar video y continuar con siguiente
   - Marcar para revisión manual
```

## Ejemplos de Manejo

### Ejemplo 1: API Timeout

```
Error: TTS API no responde
Nivel: ERROR
Acción:
  1. Registrar error
  2. Reintentar 3 veces con backoff
  3. Si falla: cambiar a edge-tts local
  4. Si todo falla: saltar este video
```

### Ejemplo 2: YouTube Login Fallido

```
Error: Autenticación rechazada
Nivel: CRITICAL
Acción:
  1. Registrar error con detalles
  2. Detener pipeline de subida
  3. Continuar con generación de contenido
  4. Marcar videos para subida manual
```

### Ejemplo 3: Video Corrupto

```
Error: FFmpeg no puede procesar video
Nivel: ERROR
Acción:
  1. Registrar error
  2. Intentar regenerar video desde audio
  3. Si falla: usar template de backup
  4. Si todo falla: saltar video
```

## Guardar Logs

```
Estructura:
logs/
├── daily/
│   └── 2026-01-31.log      # Log general del día
└── errors/
    └── error-2026-01-31.json  # Errores detallados

Formato daily.log:
[2026-01-31 10:30:00] [INFO] Pipeline started
[2026-01-31 10:30:05] [INFO] Generated 10 ideas
[2026-01-31 10:35:00] [ERROR] TTS API timeout
[2026-01-31 10:35:30] [WARNING] Retry 1 of 3
[2026-01-31 10:36:00] [INFO] TTS successful on retry
```

## Notas

- Nunca silenciar errores críticos
- Incluir suficiente contexto para debugging
- Limpiar logs antiguos (>30 días)
- Considerar alertas para errores críticos frecuentes
