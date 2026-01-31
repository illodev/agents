# Assets - Ideas

Este directorio almacena las ideas generadas por el agente.

## Estructura de Archivos

- `ideas-{YYYY-MM-DD}.json` - Ideas generadas por día
- `metadata-{idea_id}.json` - Metadata SEO para cada idea producida

## Formato de Ideas

```json
{
  "date": "2026-01-31",
  "ideas": [
    {
      "id": "idea-001",
      "title": "Título de trabajo",
      "hook": "Gancho principal",
      "angle": "Ángulo único",
      "emotion": "curiosidad",
      "score": 8,
      "format": "short",
      "status": "pending"
    }
  ]
}
```

## Estados de Ideas

| Estado        | Descripción                  |
| ------------- | ---------------------------- |
| `pending`     | Generada, sin procesar       |
| `selected`    | Seleccionada para producción |
| `in_progress` | En proceso de producción     |
| `produced`    | Video completado             |
| `published`   | Publicada en YouTube         |
| `rejected`    | Descartada                   |
