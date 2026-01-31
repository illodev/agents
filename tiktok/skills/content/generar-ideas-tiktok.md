# 💡 Skill: Generar Ideas TikTok

> **Categoría**: content  
> **Versión**: 1.0  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Genera ideas de contenido optimizadas para viralidad en TikTok, considerando trends actuales, formatos que funcionan y el nicho específico.

---

## 🎯 Cuándo Usar

- Planificación diaria de contenido (3-5 ideas)
- Cuando se agotan las ideas en cola
- Después de actualizar trending sounds
- Para experimentar con nuevos formatos

---

## ⚙️ Requisitos

- `config/config.json` - Nicho y estilo definidos
- `config/trending-sounds.json` - Trends actualizados (opcional pero recomendado)
- `analytics/insights.json` - Datos de rendimiento pasado (si existe)

---

## 📝 Proceso

### Paso 1: Cargar Contexto

```python
import json

# Cargar configuración
with open('/tiktok/config/config.json') as f:
    config = json.load(f)

# Cargar trends (si existen)
try:
    with open('/tiktok/config/trending-sounds.json') as f:
        trends = json.load(f)
except FileNotFoundError:
    trends = None

# Cargar insights pasados (si existen)
try:
    with open('/tiktok/analytics/insights.json') as f:
        insights = json.load(f)
except FileNotFoundError:
    insights = None
```

### Paso 2: Definir Fórmulas Virales

```
FÓRMULAS PROBADAS TIKTOK:

1. CONTRARIAN
   "Por qué [creencia popular] está completamente MAL"
   "Lo que nadie te dice sobre [tema]"

2. REVELACIÓN
   "El secreto que [grupo] no quiere que sepas"
   "Acabo de descubrir algo INCREÍBLE sobre [tema]"

3. STORYTIME
   "La vez que [situación dramática]..."
   "No vas a creer lo que me pasó con [tema]"

4. RANKING
   "Top 3 [cosas] que [hacen algo]"
   "Las 5 [cosas] más [adjetivo] del mundo"

5. POV
   "POV: Eres [situación relateable]"
   "POV: Descubres que [revelación]"

6. DATO IMPACTANTE
   "[Dato específico] que te va a volar la cabeza"
   "Sabías que [dato] y nadie habla de esto"

7. TUTORIAL RÁPIDO
   "Cómo [lograr algo] en 30 segundos"
   "El truco de [tema] que todos necesitan"

8. COMPARACIÓN
   "[Cosa A] vs [Cosa B]: cuál gana?"
   "La diferencia entre [A] y [B] que nadie nota"
```

### Paso 3: Generar Ideas

```
Para cada idea (generar 5-10):

1. Seleccionar fórmula viral aleatoria o rotativa
2. Aplicar al nicho configurado
3. Incorporar trend (si hay uno relevante)
4. Crear hook de 1 segundo
5. Puntuar potencial viral
```

### Paso 4: Puntuar Ideas

```
CRITERIOS DE PUNTUACIÓN (1-10 cada uno):

- Hook Power: ¿El gancho genera curiosidad inmediata?
- Relatability: ¿El público se identifica?
- Shareability: ¿La gente querrá compartirlo?
- Trend Fit: ¿Aprovecha algún trend actual?
- Uniqueness: ¿Es diferente a lo que hay?
- Production Ease: ¿Es fácil de producir?

SCORE FINAL = (Hook*0.25) + (Relat*0.15) + (Share*0.20) +
               (Trend*0.15) + (Unique*0.15) + (Ease*0.10)
```

### Paso 5: Formatear y Guardar

```json
// assets/ideas/ideas-{fecha}.json
{
  "date": "2026-01-31",
  "ideas": [
    {
      "id": "tiktok-001",
      "formula": "dato_impactante",
      "hook": "El 90% de la gente no sabe esto sobre [tema]",
      "concept": "Descripción completa del concepto...",
      "format": "voiceover + stock footage",
      "duration_target": 30,
      "trending_sound": null,
      "hashtags": ["#curiosidades", "#sabiasque", "#aprendeentiktok"],
      "scores": {
        "hook_power": 8,
        "relatability": 7,
        "shareability": 8,
        "trend_fit": 5,
        "uniqueness": 7,
        "production_ease": 9
      },
      "viral_score": 7.5,
      "status": "pending",
      "created": "2026-01-31T10:00:00Z"
    }
  ]
}
```

---

## 🎯 Plantillas de Ideas por Nicho

### Curiosidades/Datos

```
- "El [objeto común] esconde un secreto que nadie conoce"
- "[Número]% de personas no saben esto sobre [tema]"
- "La razón real por la que [fenómeno] pasa"
```

### Espacio/Ciencia

```
- "Lo que pasaría si [escenario hipotético]"
- "El lugar más [adjetivo] del universo"
- "Por qué [fenómeno espacial] es ATERRADOR"
```

### Motivación

```
- "POV: Finalmente entiendes que [revelación]"
- "La frase que cambió mi vida completamente"
- "Por qué [consejo común] está ARRUINANDO tu vida"
```

### Historia

```
- "El evento más [adjetivo] de la historia que nadie enseña"
- "[Personaje histórico] hizo ESTO y nadie habla de ello"
- "La verdadera razón por la que [evento] ocurrió"
```

---

## 🔄 Rotación de Formatos

```
Para evitar que el algoritmo penalice por repetición:

Día 1: 2x datos + 1x storytime
Día 2: 2x ranking + 1x POV
Día 3: 2x revelación + 1x tutorial
Día 4: Repetir ciclo con variaciones
```

---

## 📁 Archivos Generados

- `assets/ideas/ideas-{fecha}.json` - Ideas del día
- `analytics/insights.json` - Actualizar con patrones exitosos

---

## ✅ Criterios de Éxito

- [ ] Mínimo 5 ideas generadas
- [ ] Todas con viral_score > 6
- [ ] Al menos 2 formatos diferentes
- [ ] Hooks de máximo 10 palabras
- [ ] Archivo de ideas guardado correctamente
