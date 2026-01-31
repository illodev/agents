# Skill: crear-cuenta-youtube

## Metadata

- Versión: 1.0
- Creada: 2026-01-31
- Autor: manual
- Categoría: platform

## Descripción

Crea de forma autónoma una cuenta de Google/YouTube y configura el canal para comenzar a publicar contenido.

## Trigger

- No existen credenciales configuradas
- Comando `CREAR CUENTA`
- Primera ejecución sin cuenta

## Prerequisitos

- Acceso a Playwright
- Posibilidad de recibir SMS (para verificación)
- Conexión a internet estable

## ⚠️ Consideraciones Legales

```
IMPORTANTE:
- Crear cuentas automatizadas puede violar ToS de Google
- Esta skill es para fines educativos/de documentación
- El usuario es responsable del uso que le dé
- Considerar usar cuenta existente cuando sea posible
```

## Pasos

### 1. Verificar Estado Actual

```javascript
// Verificar si ya hay credenciales
async function checkExistingCredentials() {
  const credPath = "../../../config/credentials.env";

  if (fs.existsSync(credPath)) {
    const creds = parseEnv(credPath);
    if (creds.GOOGLE_EMAIL && creds.GOOGLE_PASSWORD) {
      log("INFO", "account", "Credenciales existentes encontradas");
      return true;
    }
  }

  log("INFO", "account", "No hay credenciales, procediendo a crear cuenta");
  return false;
}
```

### 2. Generar Datos de Cuenta

```javascript
// Generar información para la cuenta
function generateAccountData(niche) {
  const timestamp = Date.now();

  // Generar nombre basado en nicho
  const channelNames = {
    finanzas: ["FinanzasFacil", "DineroInteligente", "AhorraYa"],
    productividad: ["ProductivoHoy", "HazMas", "TiempoSmart"],
    curiosidades: ["SabiasQue", "DatoCurioso", "MenteInquieta"],
  };

  const baseName = channelNames[niche]?.[0] || "MiCanal";
  const uniqueName = `${baseName}${timestamp.toString().slice(-4)}`;

  return {
    firstName: generateName(),
    lastName: generateName(),
    email: `${uniqueName.toLowerCase()}@gmail.com`,
    password: generateSecurePassword(),
    channelName: uniqueName,
    birthDate: generateAdultBirthDate(),
  };
}

function generateSecurePassword() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789!@#$%";
  let password = "";
  for (let i = 0; i < 16; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return password;
}
```

### 3. Crear Cuenta de Google (Playwright)

```javascript
async function createGoogleAccount(data) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Ir a crear cuenta
    await page.goto("https://accounts.google.com/signup");

    // Paso 1: Nombre
    await page.fill('input[name="firstName"]', data.firstName);
    await page.fill('input[name="lastName"]', data.lastName);
    await page.click('button:has-text("Siguiente")');

    // Paso 2: Fecha de nacimiento
    await page.waitForSelector('input[name="day"]');
    await page.fill('input[name="day"]', data.birthDate.day);
    await page.selectOption('select[name="month"]', data.birthDate.month);
    await page.fill('input[name="year"]', data.birthDate.year);
    await page.selectOption('select[name="gender"]', "Prefiero no decirlo");
    await page.click('button:has-text("Siguiente")');

    // Paso 3: Email
    await page.waitForSelector('input[name="Username"]');
    await page.fill('input[name="Username"]', data.email.split("@")[0]);
    await page.click('button:has-text("Siguiente")');

    // Paso 4: Contraseña
    await page.waitForSelector('input[name="Passwd"]');
    await page.fill('input[name="Passwd"]', data.password);
    await page.fill('input[name="PasswdAgain"]', data.password);
    await page.click('button:has-text("Siguiente")');

    // Paso 5: Verificación telefónica (REQUIERE INTERVENCIÓN)
    log("WARNING", "account", "Verificación telefónica requerida");
    // Aquí el proceso necesita intervención manual o servicio de SMS

    // Paso 6: Aceptar términos
    await page.waitForSelector('button:has-text("Acepto")');
    await page.click('button:has-text("Acepto")');

    // Verificar éxito
    await page.waitForURL("**/myaccount.google.com/**");

    return { success: true, email: data.email };
  } catch (error) {
    log("ERROR", "account", `Error creando cuenta: ${error.message}`);
    return { success: false, error: error.message };
  }
}
```

### 4. Crear Canal de YouTube

```javascript
async function createYouTubeChannel(page, channelName) {
  // Ir a YouTube
  await page.goto("https://www.youtube.com");

  // Click en avatar / crear canal
  await page.click('button[aria-label="Avatar"]');
  await page.click("text=Crear un canal");

  // Configurar nombre del canal
  await page.waitForSelector('input[aria-label="Nombre"]');
  await page.fill('input[aria-label="Nombre"]', channelName);

  // Aceptar foto por defecto o subir una
  // await page.click('text=Subir imagen'); // Opcional

  // Crear canal
  await page.click('button:has-text("Crear canal")');

  // Esperar confirmación
  await page.waitForSelector("text=Tu canal");

  return { success: true, channelName };
}
```

### 5. Configurar Canal

```javascript
async function configureChannel(page, config) {
  // Ir a YouTube Studio
  await page.goto("https://studio.youtube.com");

  // Ir a personalización
  await page.click("text=Personalización");

  // Configurar información básica
  await page.click("text=Información básica");

  // Descripción del canal
  const description = generateChannelDescription(config);
  await page.fill('textarea[aria-label="Descripción"]', description);

  // Configurar branding (opcional)
  // await page.click('text=Branding');
  // await uploadLogo();
  // await uploadBanner();

  // Guardar cambios
  await page.click('button:has-text("Publicar")');

  return { success: true };
}

function generateChannelDescription(config) {
  return `
🎯 ${config.channel.niche}

Bienvenido a ${config.channelName}!
Aquí encontrarás contenido sobre ${config.channel.sub_niche}.

📺 Nuevo video cada día
🔔 Activa la campana para no perderte nada

#${config.channel.niche.replace(/\s/g, "")} #Shorts
  `.trim();
}
```

### 6. Guardar Credenciales de Forma Segura

```javascript
async function saveCredentials(data) {
  const credentialsPath =
    "/home/illodev/projects/automated-content/config/credentials.env";

  const content = `
# ================================
# CREDENCIALES - GENERADAS AUTOMÁTICAMENTE
# Fecha: ${new Date().toISOString()}
# ================================

# YouTube / Google
GOOGLE_EMAIL=${data.email}
GOOGLE_PASSWORD=${data.password}

# Canal
YOUTUBE_CHANNEL_NAME=${data.channelName}
YOUTUBE_CHANNEL_ID=${data.channelId || "PENDING"}

# Notas
# - Cambiar contraseña periódicamente
# - Habilitar 2FA cuando sea posible
# - NO compartir este archivo
`.trim();

  fs.writeFileSync(credentialsPath, content);

  // Asegurar permisos restrictivos (solo owner)
  fs.chmodSync(credentialsPath, 0o600);

  log("INFO", "credentials", `Credenciales guardadas en ${credentialsPath}`);

  // También guardar backup encriptado
  await saveEncryptedBackup(data);
}

async function saveEncryptedBackup(data) {
  const backupPath = "../config/credentials.backup.enc";
  // Encriptar con clave del sistema
  // ... implementación de encriptación
}
```

### 7. Guardar Sesión de Navegador

```javascript
async function saveSession(context) {
  const sessionPath =
    "/home/illodev/projects/automated-content/youtube/config/youtube-session.json";

  // Guardar estado del navegador (cookies, localStorage, etc.)
  await context.storageState({ path: sessionPath });

  log("INFO", "session", "Sesión guardada para futuros usos");
}
```

### 8. Verificar Setup Completo

```javascript
async function verifySetup() {
  const checks = {
    credentials: fs.existsSync("../../../config/credentials.env"),
    session: fs.existsSync("../config/youtube-session.json"),
    channelAccess: await verifyChannelAccess(),
  };

  if (Object.values(checks).every((v) => v)) {
    log("INFO", "setup", "Setup completo verificado ✓");
    return true;
  } else {
    log("ERROR", "setup", `Setup incompleto: ${JSON.stringify(checks)}`);
    return false;
  }
}
```

## Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                 CREAR CUENTA AUTÓNOMA                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Verificar si hay credenciales existentes                │
│     └─ Si existen → Usar existentes                         │
│     └─ Si no → Continuar                                    │
│                    ↓                                        │
│  2. Generar datos de cuenta                                 │
│     └─ Nombre basado en nicho                               │
│     └─ Email único                                          │
│     └─ Contraseña segura                                    │
│                    ↓                                        │
│  3. Crear cuenta Google                                     │
│     └─ ⚠️ Puede requerir verificación SMS                   │
│                    ↓                                        │
│  4. Crear canal de YouTube                                  │
│     └─ Nombre del canal                                     │
│     └─ Configuración básica                                 │
│                    ↓                                        │
│  5. Guardar credenciales                                    │
│     └─ credentials.env (permisos 600)                       │
│     └─ Backup encriptado                                    │
│                    ↓                                        │
│  6. Guardar sesión                                          │
│     └─ youtube-session.json                                 │
│                    ↓                                        │
│  7. Verificar setup                                         │
│     └─ Confirmar acceso al canal                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Manejo de Errores

| Error             | Causa                    | Solución                   |
| ----------------- | ------------------------ | -------------------------- |
| Email en uso      | Email ya registrado      | Generar nuevo email        |
| Verificación SMS  | Google requiere teléfono | Pausar, notificar usuario  |
| CAPTCHA           | Detección de bot         | Usar modo menos detectable |
| Cuenta suspendida | Actividad sospechosa     | Crear desde otra IP        |

## Notas

- Esta skill tiene limitaciones por políticas de Google
- Preferir usar cuentas existentes cuando sea posible
- La verificación SMS suele requerir intervención manual
- Guardar sesión para evitar logins repetidos
- Cambiar contraseña después de la creación automática
- Habilitar 2FA manualmente para mayor seguridad
