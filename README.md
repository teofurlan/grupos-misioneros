# Grupos misioneros con niños

One-pager para difundir cómo replicar el modelo de trabajo de los grupos misioneros
con niños que funcionan a partir de la iglesia. Se reparte en el congreso
**I Will Go** mediante tarjetas con código QR.

El contenido son diez preguntas-título con sus respuestas, escritas en primera
persona plural por líderes de varios grupos misioneros de la universidad y la iglesia.

## Stack

Una sola página HTML estática. **Sin framework, sin build, sin dependencias que instalar.**

```
index.html          la página entera (contenido + estructura)
assets/styles.css   estilos
assets/script.js    barra de progreso, índice desplegable, aparición al scrollear
```

La decisión de no usar React/Vue es deliberada: en el congreso mucha gente va a abrir
la página al mismo tiempo, con datos móviles y mala señal. Una página estática abre
en un segundo; un bundle de JS puede quedarse en blanco varios segundos.

## Cómo verla localmente

Alcanza con abrir `index.html` en el navegador (doble clic). Si preferís servirla:

```bash
python -m http.server 8000
```

Y entrar a `http://localhost:8000`.

## Paleta

Tomada del material gráfico del congreso I Will Go:

| Uso | Color |
| --- | --- |
| Fondo pergamino | `#F4ECDB` / `#EBE0C8` |
| Azul marino (texto y cierre) | `#1D3B60` |
| Dorado (acentos, numeración, botón) | `#C6952F` / `#B8871F` |
| Celeste (sección 03) | `#DCE7EE` |

La sección 03 (trabajo con menores) usa el panel celeste frío **a propósito**: corta
la calidez del resto para que se lea como la parte seria del material.

## El PDF

El PDF **no** se exporta del Word: se genera imprimiendo esta misma página, así
conserva el diseño. La hoja de estilos `@media print` convierte cada sección en una
hoja A4 completa — quedan 13 páginas, una por pregunta.

Para regenerarlo después de cambiar contenido, con el server local levantado:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="C:\Users\teofu\Code\grupos-misioneros\assets\grupos-misioneros.pdf" --virtual-time-budget=8000 http://localhost:8123/
```

Desde el navegador, a mano: `Ctrl+P` → Guardar como PDF → activar
**"Gráficos de fondo"** (si no, sale en blanco y negro).

## Fotos

Deben ser imágenes donde **no se identifique a ningún niño** (de espaldas, manos
trabajando, detalles de las manualidades) — mismo criterio que ya se usa para las
redes del grupo.

Ideal: **5 o 6 fotos**, una por bloque:

| Sección | Qué mostraría |
| --- | --- |
| Quiénes somos | El equipo trabajando |
| 01 · Actividades del sábado | Un momento del programa (cantos o historia) |
| 04 · Motivación | Chicos en una manualidad o juego |
| 09 · Logística | La merienda, materiales reciclados |
| 10 · Impacto | Una escena grupal amplia |
| Cierre | Una foto abierta, de contexto |

Formato: horizontales, mínimo 1600 px de ancho, sin comprimir ni recortar
(se optimizan acá y se convierten a WebP).

## Pendientes antes de publicar

- [ ] **Número de WhatsApp** — en `index.html`, buscar `wa.me/NUMERO` y poner el número
      real en formato internacional sin `+` ni espacios (ej. `5493434123456`).
      Agregar también una línea `.print-url` con el número, para que salga en el PDF.
- [ ] **Fotos** — ver arriba.
- [ ] **URL real** — una vez publicado, reemplazar `grupos-misioneros.vercel.app` en el
      bloque `.print-url` de `index.html` y regenerar el PDF.
- [ ] **Datos del bloque "Quiénes somos"** — hoy son datos sacados del propio material
      (`10 preguntas` / `4 momentos por sábado` / `$0 de costo`). Se pueden cambiar por
      cuántos grupos participan y desde cuándo.
- [ ] **Logos institucionales** (UAP / SVA / IWG) — decidir si van y con qué permiso.
- [ ] **Fuentes** — hoy se cargan desde Google Fonts. Si se quiere cero dependencia
      externa, se pueden autohospedar en `assets/fonts/`.

## Nota importante sobre imágenes

La sección 03 del propio material dice que difundir fotos o videos de menores requiere
**autorización firmada de los tutores**. Una web pública es difusión, y más expuesta
que un grupo de WhatsApp.

Si se van a usar fotos reales, hay que confirmar que las autorizaciones existentes lo
cubran. Alternativa segura: fotos donde los chicos no sean identificables (de espaldas,
manos trabajando, detalles de las manualidades) o ilustraciones.

## Deploy

Pensado para Vercel conectado a este repo: cada push a `main` publica solo.
El subdominio gratuito (`*.vercel.app`) es estable y no expira.

**El QR de las tarjetas debe ser estático** — la URL va codificada dentro del patrón,
así no depende de ningún servicio que pueda caducar. Se genera una vez que la URL
esté definida y no se vuelve a tocar.

## Accesibilidad

- Respeta `prefers-reduced-motion` (desactiva todas las animaciones).
- Navegable por teclado, con foco visible.
- Hoja de estilos de impresión: se puede imprimir la página y sale legible.
