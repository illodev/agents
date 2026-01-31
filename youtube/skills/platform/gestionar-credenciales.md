# Skill: gestionar-credenciales

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: platform

## Descripción

Gestiona de forma segura las credenciales y sesiones necesarias para operar el canal de YouTube y servicios externos.

## Trigger

- Inicio del agente
- Credenciales expiradas o inválidas
- Comando `VERIFICAR CREDENCIALES`
- Error de autenticación

## Prerequisitos

- Sistema de archivos accesible
- Permisos de escritura en /config

## Estructura de Credenciales

```
automated-content/
├── config/
│   ├── credentials.env           # Credenciales principales (gitignored)
│   ├── credentials.env.example   # Template público
│   └── credentials.backup.enc    # Backup encriptado
└── youtube/
    └── config/
        ├── youtube-session.json  # Sesión de navegador
        └── api-tokens.json       # Tokens de APIs (gitignored)
```

## Pasos

### 1. Verificar Credenciales Existentes

```javascript
async function checkCredentials() {
  const requiredCreds = ["GOOGLE_EMAIL", "GOOGLE_PASSWORD"];

  const optionalCreds = [
    "ELEVENLABS_API_KEY",
    "PEXELS_API_KEY",
    "PIXABAY_API_KEY",
    "OPENAI_API_KEY",
  ];

  const credPath =
    "/home/illodev/projects/automated-content/config/credentials.env";

  if (!fs.existsSync(credPath)) {
    return {
      valid: false,
      missing: requiredCreds,
      reason: "Archivo de credenciales no existe",
    };
  }

  const creds = parseEnvFile(credPath);
  const missing = requiredCreds.filter(
    (key) => !creds[key] || creds[key] === "tu_password",
  );
  const available = optionalCreds.filter(
    (key) => creds[key] && !creds[key].includes("xxxx"),
  );

  return {
    valid: missing.length === 0,
    missing,
    available,
    reason: missing.length > 0 ? `Faltan: ${missing.join(", ")}` : "OK",
  };
}
```

### 2. Guardar Credenciales Nuevas

```javascript
async function saveCredentials(credentials) {
  const credPath =
    "/home/illodev/projects/automated-content/config/credentials.env";

  // Leer existentes si hay
  let existing = {};
  if (fs.existsSync(credPath)) {
    existing = parseEnvFile(credPath);
  }

  // Merge con nuevas
  const merged = { ...existing, ...credentials };

  // Generar contenido
  const content = generateEnvContent(merged);

  // Guardar con permisos seguros
  fs.writeFileSync(credPath, content);
  fs.chmodSync(credPath, 0o600); // Solo owner puede leer/escribir

  log("INFO", "credentials", "Credenciales actualizadas");

  // Crear backup encriptado
  await createEncryptedBackup(merged);

  return { success: true };
}

function generateEnvContent(creds) {
  return `# ================================
# CREDENCIALES - AUTOMATED CONTENT
# Última actualización: ${new Date().toISOString()}
# ================================
# ⚠️ NO SUBIR A GIT - Este archivo está en .gitignore

# YouTube / Google (REQUERIDO)
GOOGLE_EMAIL=${creds.GOOGLE_EMAIL || ""}
GOOGLE_PASSWORD=${creds.GOOGLE_PASSWORD || ""}

# Canal Info
YOUTUBE_CHANNEL_NAME=${creds.YOUTUBE_CHANNEL_NAME || ""}
YOUTUBE_CHANNEL_ID=${creds.YOUTUBE_CHANNEL_ID || ""}
YOUTUBE_CHANNEL_URL=${creds.YOUTUBE_CHANNEL_URL || ""}

# APIs de IA (OPCIONAL)
OPENAI_API_KEY=${creds.OPENAI_API_KEY || ""}
ELEVENLABS_API_KEY=${creds.ELEVENLABS_API_KEY || ""}

# APIs de Stock Media (OPCIONAL)
PEXELS_API_KEY=${creds.PEXELS_API_KEY || ""}
PIXABAY_API_KEY=${creds.PIXABAY_API_KEY || ""}

# Configuración Playwright
PLAYWRIGHT_HEADLESS=${creds.PLAYWRIGHT_HEADLESS || "false"}
`;
}
```

### 3. Gestionar Sesión de Navegador

```javascript
async function manageSession() {
  const sessionPath =
    "/home/illodev/projects/automated-content/youtube/config/youtube-session.json";

  // Verificar si existe sesión
  if (fs.existsSync(sessionPath)) {
    const sessionAge = getFileAge(sessionPath);

    // Sesiones mayores a 7 días pueden expirar
    if (sessionAge < 7 * 24 * 60 * 60 * 1000) {
      log("INFO", "session", "Sesión válida encontrada");
      return { valid: true, path: sessionPath };
    } else {
      log("WARNING", "session", "Sesión puede estar expirada, verificando...");
    }
  }

  // Intentar login y crear nueva sesión
  return await createNewSession();
}

async function createNewSession() {
  const creds = loadCredentials();

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Login en Google
    await page.goto("https://accounts.google.com/signin");

    // Email
    await page.fill('input[type="email"]', creds.GOOGLE_EMAIL);
    await page.click('button:has-text("Siguiente")');

    // Password
    await page.waitForSelector('input[type="password"]');
    await page.fill('input[type="password"]', creds.GOOGLE_PASSWORD);
    await page.click('button:has-text("Siguiente")');

    // Esperar login completo
    await page.waitForURL("**/myaccount.google.com/**", { timeout: 60000 });

    // Verificar acceso a YouTube
    await page.goto("https://studio.youtube.com");
    await page.waitForSelector('ytcp-button[id="create-button"]', {
      timeout: 30000,
    });

    // Guardar sesión
    const sessionPath =
      "/home/illodev/projects/automated-content/youtube/config/youtube-session.json";
    await context.storageState({ path: sessionPath });

    log("INFO", "session", "Nueva sesión creada y guardada");

    return { valid: true, path: sessionPath };
  } catch (error) {
    log("ERROR", "session", `Error creando sesión: ${error.message}`);
    return { valid: false, error: error.message };
  } finally {
    await browser.close();
  }
}
```

### 4. Rotar/Actualizar Credenciales

```javascript
async function rotateCredentials(type) {
  switch (type) {
    case "password":
      // Generar nueva contraseña
      const newPassword = generateSecurePassword();
      // Cambiar en Google (requiere Playwright)
      await changeGooglePassword(newPassword);
      // Actualizar archivo
      await saveCredentials({ GOOGLE_PASSWORD: newPassword });
      break;

    case "api_tokens":
      // Regenerar tokens de APIs
      await regenerateAPITokens();
      break;

    case "session":
      // Forzar nuevo login
      await createNewSession();
      break;
  }
}
```

### 5. Backup y Recuperación

```javascript
async function createEncryptedBackup(credentials) {
  const crypto = require("crypto");
  const backupPath =
    "/home/illodev/projects/automated-content/config/credentials.backup.enc";

  // Usar clave derivada del sistema
  const key = crypto.scryptSync(process.env.USER + os.hostname(), "salt", 32);
  const iv = crypto.randomBytes(16);

  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);

  let encrypted = cipher.update(JSON.stringify(credentials), "utf8", "hex");
  encrypted += cipher.final("hex");

  const authTag = cipher.getAuthTag();

  const backup = {
    iv: iv.toString("hex"),
    authTag: authTag.toString("hex"),
    data: encrypted,
    created: new Date().toISOString(),
  };

  fs.writeFileSync(backupPath, JSON.stringify(backup));
  fs.chmodSync(backupPath, 0o600);

  log("INFO", "backup", "Backup encriptado creado");
}

async function restoreFromBackup() {
  const crypto = require("crypto");
  const backupPath =
    "/home/illodev/projects/automated-content/config/credentials.backup.enc";

  if (!fs.existsSync(backupPath)) {
    throw new Error("No existe backup para restaurar");
  }

  const backup = JSON.parse(fs.readFileSync(backupPath));

  const key = crypto.scryptSync(process.env.USER + os.hostname(), "salt", 32);
  const iv = Buffer.from(backup.iv, "hex");
  const authTag = Buffer.from(backup.authTag, "hex");

  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(authTag);

  let decrypted = decipher.update(backup.data, "hex", "utf8");
  decrypted += decipher.final("utf8");

  const credentials = JSON.parse(decrypted);
  await saveCredentials(credentials);

  log("INFO", "backup", "Credenciales restauradas desde backup");
}
```

### 6. Validar APIs Externas

```javascript
async function validateExternalAPIs() {
  const creds = loadCredentials();
  const results = {};

  // ElevenLabs
  if (creds.ELEVENLABS_API_KEY) {
    try {
      const response = await fetch("https://api.elevenlabs.io/v1/user", {
        headers: { "xi-api-key": creds.ELEVENLABS_API_KEY },
      });
      results.elevenlabs = response.ok;
    } catch {
      results.elevenlabs = false;
    }
  }

  // Pexels
  if (creds.PEXELS_API_KEY) {
    try {
      const response = await fetch(
        "https://api.pexels.com/v1/search?query=test&per_page=1",
        {
          headers: { Authorization: creds.PEXELS_API_KEY },
        },
      );
      results.pexels = response.ok;
    } catch {
      results.pexels = false;
    }
  }

  // OpenAI
  if (creds.OPENAI_API_KEY) {
    try {
      const response = await fetch("https://api.openai.com/v1/models", {
        headers: { Authorization: `Bearer ${creds.OPENAI_API_KEY}` },
      });
      results.openai = response.ok;
    } catch {
      results.openai = false;
    }
  }

  log("INFO", "api-validation", `APIs validadas: ${JSON.stringify(results)}`);
  return results;
}
```

## Flujo de Inicio

```
┌─────────────────────────────────────────────────────────────┐
│              GESTIÓN DE CREDENCIALES AL INICIO              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ¿Existe credentials.env?                                │
│     └─ NO → ¿Existe backup? → Restaurar : Crear cuenta      │
│     └─ SÍ → Continuar                                       │
│                    ↓                                        │
│  2. ¿Credenciales válidas?                                  │
│     └─ Verificar formato y campos requeridos                │
│     └─ Si faltan → Solicitar o crear                        │
│                    ↓                                        │
│  3. ¿Sesión de navegador válida?                            │
│     └─ NO → Crear nueva sesión con login                    │
│     └─ SÍ → Verificar que no esté expirada                  │
│                    ↓                                        │
│  4. Validar APIs externas (opcional)                        │
│     └─ Marcar cuáles están disponibles                      │
│                    ↓                                        │
│  5. Actualizar estado                                       │
│     └─ Guardar en config/state.json                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Seguridad

```
MEJORES PRÁCTICAS:

✅ HACER:
• Permisos 600 en archivos de credenciales
• Encriptar backups
• Rotar contraseñas periódicamente
• Verificar credenciales antes de usar
• Guardar sesiones para evitar logins frecuentes

❌ NO HACER:
• Subir credenciales a git
• Guardar en texto plano sin protección
• Compartir archivos de sesión
• Usar contraseñas débiles
• Ignorar errores de autenticación
```

## Notas

- El archivo credentials.env NUNCA debe subirse a git
- Las sesiones de Playwright evitan logins repetitivos
- Los backups encriptados permiten recuperación
- Validar APIs al inicio evita errores durante ejecución
- Rotar credenciales periódicamente por seguridad
