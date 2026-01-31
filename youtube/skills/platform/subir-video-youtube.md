# Skill: subir-video-youtube

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: platform

## Descripción

Automatiza el proceso completo de subida de video a YouTube Studio usando Playwright.

## Trigger

- Video final listo en `assets/video/final/`
- Metadata generada en `assets/ideas/metadata-{id}.json`
- Comando de subida ejecutado

## Prerequisitos

- Playwright instalado y configurado
- Sesión de Google/YouTube activa o credenciales disponibles
- Video en formato compatible (MP4, MOV, etc.)
- Metadata completa (título, descripción, tags)

## Pasos

### 1. Preparación

```javascript
// Verificar archivos necesarios
const videoPath = "assets/video/final/final-{idea_id}.mp4";
const metadataPath = "assets/ideas/metadata-{idea_id}.json";

// Cargar metadata
const metadata = JSON.parse(fs.readFileSync(metadataPath));
/*
{
  "title": "Título del video",
  "description": "Descripción completa...",
  "tags": ["tag1", "tag2"],
  "hashtags": ["#hashtag1", "#hashtag2"],
  "category": "Education",
  "visibility": "public|private|unlisted",
  "schedule": "2026-01-31T18:00:00Z" // opcional
}
*/
```

### 2. Navegar a YouTube Studio

```
Pasos Playwright:

1. Abrir navegador (preferiblemente con sesión guardada)
   → browser.launch({ headless: false })

2. Ir a YouTube Studio
   → page.goto('https://studio.youtube.com')

3. Verificar login
   → Si aparece login → ejecutar flujo de autenticación
   → Si ya logueado → continuar

4. Esperar carga completa
   → page.waitForSelector('[aria-label="Upload videos"]')
```

### 3. Iniciar Subida

```
Pasos Playwright:

1. Click en botón "Crear"
   → page.click('button[aria-label="Create"]')

2. Seleccionar "Subir video"
   → page.click('text=Upload video')

3. Seleccionar archivo
   → const input = page.locator('input[type="file"]')
   → input.setInputFiles(videoPath)

4. Esperar procesamiento inicial
   → page.waitForSelector('text=Upload complete', { timeout: 300000 })
```

### 4. Completar Metadata

```
Pasos Playwright:

1. Título
   → page.fill('[aria-label="Title"]', metadata.title)

2. Descripción
   → page.fill('[aria-label="Description"]', metadata.description)

3. Playlist (si aplica)
   → page.click('text=Select')
   → page.click(`text=${metadata.playlist}`)

4. Audiencia
   → page.click('[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')

5. Click "NEXT" → Elementos de video
   → page.click('text=Next')

6. Click "NEXT" → Comprobaciones
   → page.click('text=Next')

7. Click "NEXT" → Visibilidad
   → page.click('text=Next')
```

### 5. Configurar Visibilidad

```
Pasos Playwright:

SI visibility = "public":
   → page.click('[name="PUBLIC"]')

SI visibility = "private":
   → page.click('[name="PRIVATE"]')

SI visibility = "unlisted":
   → page.click('[name="UNLISTED"]')

SI schedule existe:
   → page.click('text=Schedule')
   → page.fill('[aria-label="Date"]', formatDate(metadata.schedule))
   → page.fill('[aria-label="Time"]', formatTime(metadata.schedule))
```

### 6. Subir Thumbnail (Opcional)

```
Pasos Playwright:

SI thumbnailPath existe:
   → page.click('text=Upload thumbnail')
   → const thumbInput = page.locator('input[accept="image/*"]')
   → thumbInput.setInputFiles(thumbnailPath)
   → page.waitForSelector('text=Thumbnail uploaded')
```

### 7. Publicar/Programar

```
Pasos Playwright:

1. Click en botón final
   → page.click('text=Publish') // o "Schedule" si está programado

2. Esperar confirmación
   → page.waitForSelector('text=Video published')

3. Capturar URL del video
   → const videoUrl = await page.locator('a[href*="youtu.be"]').getAttribute('href')
```

### 8. Registrar Resultado

```
Actualizar: history/published.json

{
  "videos": [
    {
      "idea_id": "idea-001",
      "youtube_url": "https://youtu.be/xxxxx",
      "published_at": "2026-01-31T18:00:00Z",
      "status": "published",
      "metadata": {
        "title": "...",
        "visibility": "public"
      }
    }
  ]
}
```

## Manejo de Errores

| Error            | Causa               | Solución                        |
| ---------------- | ------------------- | ------------------------------- |
| Login requerido  | Sesión expirada     | Re-autenticar con credenciales  |
| Upload failed    | Archivo corrupto    | Verificar video, reintentar     |
| Processing stuck | Servidor lento      | Esperar más tiempo, reintentar  |
| Copyright claim  | Contenido detectado | Registrar y revisar manualmente |
| Daily limit      | Demasiadas subidas  | Esperar 24h                     |

## Código de Ejemplo Completo

```javascript
const { chromium } = require("playwright");

async function uploadToYouTube(videoPath, metadata) {
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  });

  const context = await browser.newContext({
    storageState: "youtube-session.json", // Sesión guardada
  });

  const page = await context.newPage();

  try {
    // Navegar a Studio
    await page.goto("https://studio.youtube.com");
    await page.waitForLoadState("networkidle");

    // Click Crear
    await page.click('[aria-label="Create"]');
    await page.click("text=Upload video");

    // Subir archivo
    const fileInput = await page.locator('input[type="file"]');
    await fileInput.setInputFiles(videoPath);

    // Esperar procesamiento
    await page.waitForSelector("text=Upload complete", {
      timeout: 300000,
    });

    // Llenar metadata...
    // (continúa según pasos anteriores)

    // Publicar
    await page.click("text=Publish");

    // Obtener URL
    const url = await page.locator('a[href*="youtu.be"]').getAttribute("href");

    return { success: true, url };
  } catch (error) {
    return { success: false, error: error.message };
  } finally {
    await browser.close();
  }
}
```

## Notas

- Guardar sesión del navegador para evitar login cada vez
- Respetar límites de YouTube (subidas por día)
- Verificar que el video no tenga claims antes de publicar
- Hacer capturas de pantalla en caso de error para debugging
