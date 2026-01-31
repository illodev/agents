# 🔍 Skill: Investigar Trends TikTok

> **Categoría**: research  
> **Versión**: 1.0  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Investiga sonidos trending, hashtags virales y formatos populares actuales en TikTok para maximizar el alcance en el FYP.

---

## 🎯 Cuándo Usar

- Al inicio de cada sesión de producción
- Cada 6-12 horas (los trends cambian rápido)
- Cuando el engagement baja significativamente
- Para planificar contenido del día

---

## ⚙️ Requisitos

- Sesión activa de TikTok en navegador
- Acceso a TikTok Discover/Creative Center

---

## 📝 Proceso

### Paso 1: Navegar a TikTok Discover

```
mcp_playwright_browser_navigate → "https://www.tiktok.com/explore"
mcp_playwright_browser_snapshot → Capturar estado
```

### Paso 2: Extraer Trending Sounds

```
1. Identificar sección de "Trending sounds"
2. Para cada sonido visible:
   - Nombre del sonido
   - Artista/Creador
   - Número de videos que lo usan
   - Categoría (si disponible)
```

### Paso 3: Extraer Trending Hashtags

```
1. Identificar sección de hashtags
2. Para cada hashtag:
   - Nombre del hashtag
   - Número de views
   - Tendencia (rising/stable/falling)
```

### Paso 4: Navegar a Creative Center (Opcional)

```
mcp_playwright_browser_navigate → "https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en"

Extraer:
- Top ads por engagement
- Formatos más efectivos
- Hooks que funcionan
```

### Paso 5: Filtrar por Nicho

```python
def filter_trends_by_niche(trends, niche_keywords):
    """Filtrar trends relevantes para el nicho"""
    relevant = []
    for trend in trends:
        # Verificar si el trend es aplicable al nicho
        if any(kw in trend['name'].lower() for kw in niche_keywords):
            trend['niche_fit'] = True
            relevant.append(trend)
        elif trend['uses'] > 100000:  # Trends muy virales siempre considerar
            trend['niche_fit'] = 'adaptable'
            relevant.append(trend)
    return relevant
```

### Paso 6: Guardar Resultados

```json
// config/trending-sounds.json
{
  "last_updated": "2026-01-31T10:00:00Z",
  "sounds": [
    {
      "id": "sound-123",
      "name": "Original Sound - Creator",
      "uses": 150000,
      "category": "comedy",
      "niche_fit": true,
      "url": "https://tiktok.com/music/..."
    }
  ],
  "hashtags": [
    {
      "tag": "#curiosidades",
      "views": "5.2B",
      "velocity": "rising",
      "niche_fit": true
    }
  ],
  "formats": [
    {
      "type": "storytime",
      "description": "Narración personal con text overlay",
      "avg_engagement": 8.5
    },
    {
      "type": "ranking",
      "description": "Top X de algo",
      "avg_engagement": 7.2
    }
  ]
}
```

---

## 📊 Scoring de Trends

```
Trend Score = (Popularidad * 0.3) + (Velocidad * 0.3) + (Niche Fit * 0.4)

Donde:
- Popularidad: 1-10 basado en número de usos
- Velocidad: 1-10 basado en crecimiento reciente
- Niche Fit: 1-10 qué tan aplicable es al nicho
```

---

## 🔧 Troubleshooting

### No se cargan trends

1. Verificar que la sesión está activa
2. Cambiar a otra región si es necesario
3. Usar VPN si hay restricciones geográficas

### Trends no relevantes

1. Expandir keywords del nicho
2. Buscar en cuentas del mismo nicho
3. Analizar competidores directamente

---

## 📁 Archivos Generados

- `config/trending-sounds.json` - Trends actualizados
- `logs/daily/trends-{fecha}.json` - Historial de trends

---

## ✅ Criterios de Éxito

- [ ] Al menos 10 sonidos trending identificados
- [ ] Al menos 15 hashtags relevantes
- [ ] Al menos 3 formatos virales documentados
- [ ] Archivo trending-sounds.json actualizado
