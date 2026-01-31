# Skill: crear-guion-short

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: content

## Descripción

Crea guiones optimizados para YouTube Shorts (≤60 segundos) con estructura de máxima retención.

## Trigger

- Idea seleccionada lista para producción
- Comando de crear guion específico

## Prerequisitos

- Idea con hook definido
- Configuración de estilo cargada
- Duración objetivo (máx 60s)

## Pasos

### 1. Cargar Idea

```
- Leer idea desde assets/ideas/
- Extraer: título, hook, ángulo, emoción
- Determinar duración objetivo (45-60s recomendado)
```

### 2. Estructurar Guion

```markdown
## ESTRUCTURA SHORT (60s)

[SEGUNDO 0-3: HOOK]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• UNA frase de impacto
• Máximo 10 palabras
• Genera intriga inmediata
• NO revelar la conclusión

[SEGUNDO 3-15: CONTEXTO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Establece el problema/situación
• Conecta emocionalmente
• "Esto le pasa a [audiencia]..."

[SEGUNDO 15-45: DESARROLLO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 2-3 puntos principales
• Cada punto = 10 segundos
• Mini-ganchos entre puntos
• Escalada de valor

[SEGUNDO 45-55: REVELACIÓN]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• El punto más importante
• Momento "ajá"
• Máximo impacto

[SEGUNDO 55-60: CIERRE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• CTA suave o final abierto
• "Sígueme para más"
• O pregunta que genera comentarios
```

### 3. Aplicar Reglas de Redacción

```
✅ HACER:
• Frases de máximo 10-12 palabras
• Lenguaje de conversación
• Segunda persona ("tú", "tu")
• Verbos activos
• Palabras sensoriales
• Pausas dramáticas (...)

❌ NO HACER:
• Frases largas o subordinadas
• Jerga técnica sin explicar
• Voz pasiva
• Introducciones lentas
• Despedidas largas
```

### 4. Calcular Timing

```
Regla: ~150 palabras por minuto (hablando rápido)
60 segundos = ~150 palabras máximo

Distribución:
- Hook: 10-15 palabras
- Contexto: 25-30 palabras
- Desarrollo: 70-80 palabras
- Revelación: 20-25 palabras
- Cierre: 10-15 palabras
```

### 5. Validar

```
Checklist:
☐ Hook en primeros 3 segundos
☐ No excede 150 palabras
☐ Cada frase aporta valor
☐ Emoción clara y consistente
☐ CTA o loop presente
☐ Sin contenido problemático
```

### 6. Guardar

```
Exportar a: assets/scripts/script-{idea_id}.md

Formato:
---
idea_id: idea-001
title: "Título del video"
duration_target: 55
word_count: 142
created: 2026-01-31T10:00:00Z
---

[HOOK]
Tu primera frase de impacto aquí.

[CONTEXTO]
Párrafo de contexto...

[DESARROLLO]
Punto 1...
Punto 2...
Punto 3...

[REVELACIÓN]
El momento clave...

[CIERRE]
CTA o final abierto.
```

## Ejemplos

### Ejemplo: Short de Productividad

```markdown
---
idea_id: idea-prod-001
title: "El truco de 2 minutos que cambió mi vida"
duration_target: 55
word_count: 138
---

[HOOK]
Si una tarea toma menos de 2 minutos, hazla ahora.

[CONTEXTO]
Tu lista de pendientes nunca termina, ¿verdad?
Siempre hay algo que "harás después".
Ese "después" se convierte en nunca.

[DESARROLLO]
David Allen descubrió algo simple pero brutal.
Las tareas pequeñas que postpones te roban más energía mental que hacerlas.
Responder ese mensaje: 30 segundos.
Pensarlo 10 veces al día: 5 minutos de estrés.

[REVELACIÓN]
El truco no es hacer más.
Es eliminar la fricción de decidir.
Si toma menos de 2 minutos, ya está hecho.

[CIERRE]
¿Qué tarea de 2 minutos llevas semanas evitando?
```

## Notas

- Leer guion en voz alta para verificar naturalidad
- Ajustar según feedback de retención real
- Crear variantes para A/B testing si es necesario
