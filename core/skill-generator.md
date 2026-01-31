# 🧬 Sistema de Auto-Generación de Skills

Los agentes pueden crear nuevas habilidades (skills) de forma autónoma para mejorar su eficiencia.

## Concepto de Skill

Una **skill** es una capacidad documentada y reutilizable que el agente puede invocar. Cada skill tiene:

- **Nombre**: Identificador único
- **Descripción**: Qué hace
- **Trigger**: Cuándo usarla
- **Pasos**: Cómo ejecutarla
- **Ejemplos**: Casos de uso

## Estructura de una Skill

```markdown
# Skill: [nombre-de-la-skill]

## Metadata

- Versión: 1.0
- Creada: [fecha]
- Autor: auto-generada | manual
- Categoría: [categoría]

## Descripción

[Qué hace esta skill]

## Trigger

[Cuándo debe activarse esta skill]

## Prerequisitos

- [Lo que necesita estar disponible]

## Pasos

1. [Paso 1]
2. [Paso 2]
   ...

## Ejemplos

### Ejemplo 1: [Caso]

[Descripción del caso y resultado esperado]

## Notas

[Consideraciones adicionales]
```

## Proceso de Auto-Generación

```
┌─────────────────────────────────────────────────────────────┐
│              AUTO-GENERACIÓN DE SKILLS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DETECCIÓN                                               │
│     └─ El agente detecta patrón repetitivo o nueva tarea   │
│                    ↓                                        │
│  2. ANÁLISIS                                                │
│     └─ Revisa skills existentes en /skills                  │
│     └─ Determina si existe skill similar                    │
│                    ↓                                        │
│  3. DECISIÓN                                                │
│     └─ Si existe similar → usar existente                   │
│     └─ Si no existe → crear nueva                           │
│                    ↓                                        │
│  4. GENERACIÓN                                              │
│     └─ Documenta la nueva skill                             │
│     └─ Incluye ejemplos de uso                              │
│                    ↓                                        │
│  5. REGISTRO                                                │
│     └─ Guarda en /skills/[categoria]/[nombre].md            │
│     └─ Actualiza skills-index.json                          │
│                    ↓                                        │
│  6. USO                                                     │
│     └─ La skill queda disponible para futuras ejecuciones   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Categorías de Skills

| Categoría    | Descripción                 | Ejemplos                              |
| ------------ | --------------------------- | ------------------------------------- |
| `content`    | Creación de contenido       | generar-guion, crear-titulo-viral     |
| `media`      | Manipulación de medios      | generar-voz, editar-video             |
| `platform`   | Interacción con plataformas | subir-youtube, programar-post         |
| `analysis`   | Análisis de datos           | extraer-metricas, analizar-tendencias |
| `automation` | Automatización general      | manejar-errores, reintentar-accion    |

## Archivo skills-index.json

Cada agente mantiene un índice de sus skills:

```json
{
  "version": "1.0",
  "updated": "2026-01-31",
  "skills": [
    {
      "name": "generar-guion-viral",
      "category": "content",
      "file": "content/generar-guion-viral.md",
      "auto_generated": true,
      "usage_count": 15,
      "success_rate": 0.93
    }
  ]
}
```

## Triggers para Auto-Generación

El agente debe crear una nueva skill cuando:

1. **Repetición**: Realiza la misma secuencia de pasos 3+ veces
2. **Complejidad**: Una tarea tiene más de 5 pasos
3. **Error frecuente**: Un proceso falla repetidamente y requiere manejo especial
4. **Optimización**: Descubre una forma más eficiente de hacer algo
5. **Nueva capacidad**: Aprende a hacer algo nuevo

## Ejemplo de Skill Auto-Generada

```markdown
# Skill: generar-titulo-viral

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: auto-generada
- Categoría: content

## Descripción

Genera títulos optimizados para CTR usando patrones probados de viralidad.

## Trigger

Cuando se necesita crear un título para nuevo contenido.

## Prerequisitos

- Tema del video definido
- Nicho configurado

## Pasos

1. Identificar la emoción principal del tema (curiosidad, miedo, deseo)
2. Aplicar una de las estructuras virales:
   - "[Número] [Cosas] que [Resultado Impactante]"
   - "Por qué [Cosa Común] es [Revelación Sorprendente]"
   - "[Acción] en [Tiempo Corto] | [Beneficio]"
   - "No [Hagas Esto] hasta ver [Consecuencia]"
3. Incluir palabras de poder: secreto, revelado, increíble, ahora
4. Mantener bajo 60 caracteres
5. Generar 3 variantes
6. Seleccionar el de mayor potencial

## Ejemplos

### Ejemplo 1: Video de productividad

Tema: "Técnicas para madrugar"
Títulos generados:

1. "5 Trucos para Madrugar Sin Sufrir (El #3 es Increíble)"
2. "Por Qué Fracasas al Madrugar | La Ciencia lo Explica"
3. "Madruga en 7 Días con Este Método Secreto"

## Notas

- Evitar clickbait extremo que no cumpla
- Ajustar según métricas de CTR reales
```

## Mejora Continua

Las skills se mejoran automáticamente:

1. **Tracking**: Se registra cada uso de la skill
2. **Métricas**: Se mide tasa de éxito
3. **Análisis**: Se identifican patrones de fallo
4. **Iteración**: Se actualiza la skill con mejoras

## Implementación

El agente debe mantener esta lógica en su ejecución:

```
ANTES de ejecutar una tarea:
  1. Buscar si existe skill relacionada
  2. Si existe y tiene buena tasa de éxito → usarla
  3. Si no existe → ejecutar y considerar crear skill

DESPUÉS de ejecutar una tarea:
  1. ¿Fue exitosa? → Registrar
  2. ¿Es repetitiva? → Crear skill
  3. ¿Skill existente falló? → Actualizar
```
