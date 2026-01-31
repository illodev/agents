# 📤 Skill: Subir Video a TikTok

> **Categoría**: platform  
> **Versión**: 1.0  
> **Última actualización**: 2026-01-31

---

## 📋 Descripción

Sube videos a TikTok utilizando Playwright MCP para automatizar el proceso completo de publicación.

---

## 🎯 Cuándo Usar

- Cuando un video está listo para publicar
- Para programar publicaciones
- Para subir múltiples videos en batch

---

## ⚙️ Requisitos

- Video final en `assets/video/final/`
- Sesión de TikTok activa en navegador
- Metadata del video (descripción, hashtags)

---

## 📝 Proceso

### Paso 1: Preparar Metadata

```python
metadata = {
    "video_path": "/tiktok/assets/video/final/video-001.mp4",
    "description": "El 90% no sabe esto 🤯 #curiosidades #aprendeentiktok #fyp",
    "hashtags": ["#curiosidades", "#aprendeentiktok", "#fyp", "#viral", "#sabiasque"],
    "allow_comments": True,
    "allow_duet": True,
    "allow_stitch": True,
    "schedule": None  # o datetime para programar
}
```

### Paso 2: Navegar a TikTok Upload

```
mcp_playwright_browser_navigate(url="https://www.tiktok.com/upload")
mcp_playwright_browser_snapshot()
```

**Verificar estado:**

- Si aparece login → Ejecutar flujo de autenticación
- Si aparece upload form → Continuar

### Paso 3: Verificar Sesión (si necesario)

```
Si requiere login:

1. mcp_playwright_browser_navigate(url="https://www.tiktok.com/login")
2. mcp_playwright_browser_snapshot()
3. Click en método de login (email/phone)
4. mcp_playwright_browser_type() - credenciales
5. Esperar verificación
6. Guardar sesión
```

### Paso 4: Subir Video

```
1. Identificar zona de upload en snapshot
2. mcp_playwright_browser_file_upload(
     paths=["/home/illodev/projects/automated-content/tiktok/assets/video/final/video-001.mp4"]
   )
3. mcp_playwright_browser_wait_for(text="Upload complete")
   // o esperar indicador de procesamiento
```

### Paso 5: Completar Descripción

```
1. mcp_playwright_browser_snapshot() - obtener ref del campo caption
2. mcp_playwright_browser_type(
     ref="[ref del campo caption]",
     text="El 90% no sabe esto 🤯 #curiosidades #aprendeentiktok #fyp"
   )
```

**Formato de Caption Óptimo:**

```
[Hook corto] [Emoji]

#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5

[CTA sutil opcional]
```

### Paso 6: Configurar Opciones

```
Según el snapshot, configurar:

1. "Who can watch": Everyone (por defecto)
2. "Allow comments": Activar
3. "Allow Duet": Según config
4. "Allow Stitch": Según config
5. "Disclose content": Si es necesario
```

### Paso 7: Publicar o Programar

**Publicar inmediatamente:**

```
mcp_playwright_browser_click(ref="[ref del botón Post]", element="Botón Publicar")
```

**Programar:**

```
1. mcp_playwright_browser_click(ref="[Schedule toggle]")
2. Seleccionar fecha y hora
3. mcp_playwright_browser_click(ref="[Schedule button]")
```

### Paso 8: Confirmar Publicación

```
mcp_playwright_browser_wait_for(text="Your video is being uploaded")
// o
mcp_playwright_browser_wait_for(text="Video posted")

mcp_playwright_browser_snapshot() - Capturar confirmación
```

### Paso 9: Extraer URL del Video

```
1. mcp_playwright_browser_navigate(url="https://www.tiktok.com/@username")
2. mcp_playwright_browser_snapshot()
3. Identificar el video más reciente
4. Extraer URL
```

### Paso 10: Registrar Publicación

```json
// history/published.json
{
  "videos": [
    {
      "id": "tiktok-001",
      "platform": "tiktok",
      "url": "https://www.tiktok.com/@username/video/123456",
      "published_at": "2026-01-31T15:00:00Z",
      "description": "El 90% no sabe esto...",
      "hashtags": ["#curiosidades", "#fyp"],
      "status": "published",
      "initial_metrics": null
    }
  ]
}
```

---

## 🔧 Troubleshooting

### Error: "Video processing failed"

1. Verificar formato del video (MP4, H.264)
2. Verificar resolución (1080x1920)
3. Verificar duración (<3 min)
4. Re-exportar con codec correcto

### Error: "Session expired"

1. Ejecutar flujo de login nuevamente
2. Verificar credenciales en credentials.env
3. Guardar nueva sesión

### Error: "Caption too long"

1. Máximo 2200 caracteres
2. Reducir descripción
3. Usar menos hashtags (5 max recomendado)

### Shadowban detectado

Señales:

- Views muy bajos consistentemente
- Video no aparece en FYP
- Video no aparece en búsqueda de hashtags

Acciones:

1. Pausar publicación 24-48 horas
2. Revisar contenido reciente por violaciones
3. Evitar CTAs agresivos
4. Variar formatos de contenido

---

## ⏰ Mejores Horarios para Publicar

| Día       | Horarios Óptimos (España) |
| --------- | ------------------------- |
| Lunes     | 7:00, 12:00, 22:00        |
| Martes    | 7:00, 12:00, 19:00        |
| Miércoles | 7:00, 11:00, 22:00        |
| Jueves    | 9:00, 12:00, 19:00        |
| Viernes   | 7:00, 11:00, 21:00        |
| Sábado    | 9:00, 12:00, 22:00        |
| Domingo   | 9:00, 12:00, 19:00        |

**Nota**: Espaciar publicaciones mínimo 3-4 horas entre cada una.

---

## 📁 Archivos Actualizados

- `history/published.json` - Registro de video publicado
- `config/state.json` - Estado actualizado
- `logs/daily/upload-{fecha}.json` - Log de la subida

---

## ✅ Criterios de Éxito

- [ ] Video subido sin errores
- [ ] Caption con hashtags correctos
- [ ] Configuración de privacidad correcta
- [ ] URL del video capturada
- [ ] Registro en published.json
