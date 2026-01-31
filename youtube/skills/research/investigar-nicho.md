# Skill: investigar-nicho

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: research

## Descripción

Investiga y selecciona el nicho más rentable y viable para el canal de YouTube basándose en análisis de mercado, competencia y potencial de monetización.

## Trigger

- Primera ejecución del agente (nicho = "DEFINIR")
- Comando `INVESTIGAR NICHO`
- Rendimiento del canal por debajo de expectativas

## Prerequisitos

- Acceso a navegador (Playwright)
- Capacidad de búsqueda web

## Pasos

### 1. Definir Criterios de Evaluación

```
Un buen nicho debe cumplir:

┌─────────────────────────────────────────────────────────────┐
│                    CRITERIOS DE NICHO                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  💰 MONETIZACIÓN                                            │
│     └─ CPM estimado > $5                                    │
│     └─ Productos/servicios para promocionar                 │
│     └─ Audiencia con poder adquisitivo                      │
│                                                             │
│  📈 DEMANDA                                                 │
│     └─ Volumen de búsquedas alto                           │
│     └─ Tendencia estable o creciente                        │
│     └─ Interés en múltiples países                          │
│                                                             │
│  🎯 COMPETENCIA                                             │
│     └─ No saturado de grandes canales                       │
│     └─ Espacio para diferenciación                          │
│     └─ Canales pequeños creciendo                           │
│                                                             │
│  🤖 AUTOMATIZACIÓN                                          │
│     └─ Contenido generado sin cara visible                  │
│     └─ No requiere equipo especializado                     │
│     └─ Posible con IA y stock media                         │
│                                                             │
│  ♻️ ESCALABILIDAD                                           │
│     └─ Ideas infinitas de contenido                         │
│     └─ Evergreen (no caduca)                                │
│     └─ Múltiples formatos posibles                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Investigar Nichos Candidatos

```
Nichos probados para canales automatizados:

TIER 1 (Alto CPM, Alta demanda):
├── Finanzas personales / Inversión
├── Productividad / Desarrollo personal
├── Tecnología / IA / Gadgets
├── Salud y bienestar
└── Negocios / Emprendimiento

TIER 2 (CPM medio, Muy alta demanda):
├── Curiosidades / Datos interesantes
├── Historia / Misterios
├── Psicología / Mente humana
├── Ciencia explicada
└── Motivación / Frases

TIER 3 (CPM bajo, Volumen masivo):
├── Entretenimiento / Tops
├── Gaming / Resúmenes
├── Películas / Series explicadas
└── Memes / Humor

Proceso de investigación:
1. Buscar "mejores nichos YouTube [año actual]"
2. Analizar canales exitosos sin rostro
3. Verificar tendencias en Google Trends
4. Revisar CPM estimados por nicho
```

### 3. Analizar Competencia con Playwright

```javascript
// Buscar canales en el nicho
async function analyzeNiche(niche) {
  // 1. Ir a YouTube
  await page.goto("https://youtube.com");

  // 2. Buscar el nicho
  await page.fill('input[name="search_query"]', niche);
  await page.press('input[name="search_query"]', "Enter");

  // 3. Filtrar por canales
  await page.click("text=Filtros");
  await page.click("text=Canal");

  // 4. Analizar top 10 canales
  const channels = await page.$$eval("ytd-channel-renderer", (els) =>
    els.slice(0, 10).map((el) => ({
      name: el.querySelector("#channel-title").textContent,
      subscribers: el.querySelector("#subscribers").textContent,
      videos: el.querySelector("#video-count").textContent,
    })),
  );

  // 5. Evaluar saturación
  return analyzeCompetition(channels);
}
```

### 4. Evaluar y Puntuar

```
Sistema de puntuación (0-10 por criterio):

| Criterio      | Peso | Cómo evaluar                           |
|---------------|------|----------------------------------------|
| Monetización  | 25%  | CPM del nicho, sponsors potenciales    |
| Demanda       | 25%  | Búsquedas, views de videos similares   |
| Competencia   | 20%  | Canales grandes, espacio disponible    |
| Automatizable | 20%  | Posible sin rostro, con IA            |
| Escalabilidad | 10%  | Ideas infinitas, evergreen             |

Fórmula:
Score = (Mon*0.25) + (Dem*0.25) + (Comp*0.20) + (Auto*0.20) + (Esc*0.10)
```

### 5. Seleccionar Nicho y Sub-nicho

```
Ejemplo de decisión:

Nicho seleccionado: "Finanzas personales"
Puntuación: 8.5/10

Sub-nichos específicos:
1. "Errores financieros que evitar" (miedo + educación)
2. "Trucos de ahorro poco conocidos" (curiosidad + valor)
3. "Mentalidad de ricos vs pobres" (aspiracional)

Ángulo diferenciador:
"Finanzas explicadas en 60 segundos con datos impactantes"

Ventaja competitiva:
- Shorts de alto impacto
- Datos visuales sorprendentes
- Consejos accionables inmediatos
```

### 6. Guardar Decisión

```json
// Guardar en: youtube/config/niche-research.json
{
  "research_date": "2026-01-31",
  "niches_evaluated": [
    {
      "name": "Finanzas personales",
      "score": 8.5,
      "cpm_estimate": "$8-15",
      "competition": "media",
      "selected": true
    },
    {
      "name": "Productividad",
      "score": 7.8,
      "cpm_estimate": "$6-12",
      "competition": "alta",
      "selected": false
    }
  ],
  "final_selection": {
    "niche": "Finanzas personales",
    "sub_niche": "Errores financieros y trucos de ahorro",
    "angle": "Datos impactantes en 60 segundos",
    "target_audience": "18-35 años, hispanohablantes, interesados en mejorar finanzas",
    "content_pillars": [
      "Errores comunes",
      "Trucos de ahorro",
      "Mentalidad financiera",
      "Inversión básica"
    ]
  },
  "reasoning": "Alto CPM, demanda constante, posible automatizar con datos y gráficos"
}

// Actualizar config.json automáticamente
```

### 7. Actualizar Configuración

```javascript
// Actualizar youtube/config/config.json
const config = readConfig();
config.channel.niche = research.final_selection.niche;
config.channel.sub_niche = research.final_selection.sub_niche;
config.channel.target_audience = research.final_selection.target_audience;
config.channel.content_pillars = research.final_selection.content_pillars;
saveConfig(config);

// Registrar en logs
log("INFO", "niche-research", `Nicho seleccionado: ${config.channel.niche}`);
```

## Ejemplos

### Ejemplo: Investigación Completa

```
Entrada: Nicho no definido

Proceso:
1. Investigar 5 nichos candidatos
2. Analizar 50 canales (10 por nicho)
3. Evaluar métricas de cada uno
4. Calcular scores

Resultado:
┌──────────────────────┬───────┬─────────┬─────────────┐
│ Nicho                │ Score │ CPM     │ Competencia │
├──────────────────────┼───────┼─────────┼─────────────┤
│ Finanzas personales  │ 8.5   │ $8-15   │ Media       │
│ Productividad        │ 7.8   │ $6-12   │ Alta        │
│ Curiosidades         │ 7.2   │ $3-6    │ Media       │
│ Historia/Misterios   │ 7.0   │ $4-8    │ Baja        │
│ Motivación           │ 6.5   │ $2-5    │ Muy Alta    │
└──────────────────────┴───────┴─────────┴─────────────┘

Decisión: Finanzas personales
Razón: Mejor balance CPM/competencia, altamente automatizable
```

## Notas

- Re-evaluar nicho cada 3 meses o si métricas bajan
- Considerar nichos secundarios para diversificar
- Mantener flexibilidad para pivotar si es necesario
- Documentar razones de la elección para futuras referencias
