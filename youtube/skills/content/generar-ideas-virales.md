# Skill: generar-ideas-virales

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: content

## Descripción

Genera ideas de contenido con alto potencial de viralidad y retención basándose en patrones probados y tendencias actuales.

## Trigger

- Inicio de ciclo de producción
- Cuando se necesitan nuevas ideas
- Inventario de ideas < 5

## Prerequisitos

- Configuración de nicho cargada
- Acceso a analytics de videos anteriores (opcional)

## Pasos

### 1. Cargar Contexto

```
- Leer config.json para obtener nicho y estilo
- Leer analytics/insights.json para patrones exitosos
- Leer últimas ideas generadas para evitar repetición
```

### 2. Investigar Tendencias

```
- Identificar temas trending en el nicho
- Buscar preguntas frecuentes del público
- Analizar qué funciona en canales similares
```

### 3. Aplicar Fórmulas de Viralidad

```
Usar una o más de estas fórmulas:

A) CURIOSIDAD
   "¿Por qué [cosa común] hace [efecto inesperado]?"
   "El secreto detrás de [fenómeno conocido]"

B) CONTRARIAN
   "Por qué [consejo popular] está equivocado"
   "[Cosa que todos hacen] te está perjudicando"

C) LISTA + BENEFICIO
   "[Número] formas de [lograr beneficio] que nadie conoce"

D) MIEDO/URGENCIA
   "Lo que [autoridad] no quiere que sepas sobre [tema]"
   "Deja de hacer [cosa] inmediatamente"

E) TRANSFORMACIÓN
   "De [estado negativo] a [estado positivo] en [tiempo]"
```

### 4. Generar 10 Ideas

```
Para cada idea incluir:
- Título de trabajo
- Hook principal (primeros 3 segundos)
- Ángulo único
- Emoción principal
- Puntuación estimada (1-10)
```

### 5. Filtrar y Seleccionar

```
Criterios de filtrado:
- Puntuación mínima: 7/10
- No repetir temas recientes
- Viable con recursos disponibles
- Alineado con políticas de YouTube
```

### 6. Guardar

```
Exportar a: assets/ideas/ideas-{YYYY-MM-DD}.json

Formato:
{
  "date": "2026-01-31",
  "ideas": [
    {
      "id": "idea-001",
      "title": "...",
      "hook": "...",
      "angle": "...",
      "emotion": "curiosidad",
      "score": 8,
      "format": "short",
      "status": "pending"
    }
  ]
}
```

## Ejemplos

### Ejemplo 1: Nicho Productividad

```
Idea generada:
- Título: "Por qué madrugar no funciona (y qué hacer en su lugar)"
- Hook: "Te han mentido sobre madrugar toda tu vida"
- Ángulo: Contrarian + Solución alternativa
- Emoción: Curiosidad + Alivio
- Score: 9
```

### Ejemplo 2: Nicho Finanzas

```
Idea generada:
- Título: "El error de ahorro que comete el 90% de personas"
- Hook: "¿Estás guardando dinero? Probablemente lo estás haciendo mal"
- Ángulo: Miedo + Educación
- Emoción: Preocupación → Solución
- Score: 8
```

## Notas

- Evitar temas polémicos que puedan causar strikes
- Priorizar temas evergreen sobre tendencias pasajeras
- Actualizar fórmulas según métricas reales
