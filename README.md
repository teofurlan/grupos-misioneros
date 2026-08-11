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

Las ocho que están puestas hoy, en `assets/fotos/` (WebP, ~1 MB en total, todas con
`loading="lazy"` para que no pesen en la carga inicial). Hay material de dos grupos
misioneros distintos, para que no se vea todo del mismo lugar:

| Archivo | Sección | Qué se ve |
| --- | --- | --- |
| `quienes.webp` | Quiénes somos | El grupo caminando por el barrio, de espaldas |
| `actividades.webp` | 01 · Actividades del sábado *(fondo)* | Los chicos sentados escuchando |
| `organizacion.webp` | 02 · Cómo nos organizamos | Adultos y chicos trabajando juntos, desde arriba |
| `motivacion.webp` | 04 · Motivación | Muchos chicos dibujando sobre mantas |
| `grupo.webp` | 05 · Organización del grupo *(fondo)* | Ronda de chicas alrededor de una hoja |
| `logistica.webp` | 09 · Logística | Manualidades terminadas, sin personas |
| `impacto.webp` | 10 · Impacto | El grupo reunido en el patio |
| `cierre.webp` | Cierre | Un chico pegando el cartel «Jesus loves me» |

Las secciones 03, 06, 07 y 08 van sin foto a propósito: dan respiro y evitan que el
recurso se agote. La 08 (familias) es la primera candidata cuando haya fotos de
talleres con padres.

**Dos tratamientos**, alternados para que no se vuelva repetitivo:

- `.q--split` — la foto ocupa un lateral a sangre, con corte limpio. El ancho lo define
  `--photo-col` por sección (van de 32% a 46%) y el lado alterna con `.split--reverse`.
- `.q--bg` — la foto ocupa el fondo completo con un velo azul encima y el texto en
  claro. Se usa en 01, 05 y el cierre: funcionan como puntuación visual.

**Encuadre:** las fotos son verticales y se recortan (franja apaisada en mobile,
columna angosta en escritorio), donde el centro geométrico no siempre es el motivo.
Cada una tiene su `object-position` en `styles.css` (buscar `#quienes .photo img`).
Al cambiar una foto, revisar ese valor.

Para reemplazarlas: se recortan las barras negras de los screenshots, se redimensionan
a 1300 px de lado largo y se guardan como WebP calidad ~66. Los originales sin
comprimir, mínimo 1600 px de lado largo.

## Pendientes antes de publicar

- [ ] **Número de WhatsApp** — en `index.html`, buscar `wa.me/NUMERO` y poner el número
      real en formato internacional sin `+` ni espacios (ej. `5493434123456`).
      Agregar también una línea `.print-url` con el número, para que salga en el PDF.
- [ ] **Fotos definitivas** — las actuales son provisorias, a la espera de más material.
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

Publicado en **https://grupos-misioneros.vercel.app** — Vercel conectado a este repo:
cada push a `main` publica solo. El subdominio gratuito es estable y no expira.

**El QR de las tarjetas debe ser estático** — la URL va codificada dentro del patrón,
así no depende de ningún servicio que pueda caducar. Se genera una vez que la URL
esté definida y no se vuelve a tocar.

## Accesibilidad

- Respeta `prefers-reduced-motion` (desactiva todas las animaciones).
- Navegable por teclado, con foco visible.
- Hoja de estilos de impresión: se puede imprimir la página y sale legible.
