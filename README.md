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
| `quienes.webp` | Quiénes somos | Chicos y líderes jugando en el patio, de espaldas |
| `actividades.webp` | 01 · Actividades del sábado *(fondo)* | Los chicos sentados en el pasto, todos de espaldas |
| `organizacion.webp` | 02 · Cómo nos organizamos | Adultos y chicos trabajando juntos, desde arriba |
| `motivacion.webp` | 04 · Motivación | Muchos chicos dibujando sobre mantas |
| `grupo.webp` | 05 · Organización del grupo *(fondo)* | Ronda de chicas alrededor de una hoja |
| `logistica.webp` | 09 · Logística | Manualidades terminadas, sin personas |
| `impacto.webp` | 10 · Impacto | Chicos en una manualidad, desde arriba (recortada) |
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

Para reemplazarlas: se redimensionan a ~1300 px de lado largo y se guardan como WebP
calidad 58-72 (según cuánto detalle fino tenga la foto). Los originales sin comprimir.

Si la foto es un **screenshot de teléfono**, hay que sacarle las barras negras, y no
alcanza con escanear hacia adentro desde el borde: la barrita clara del home del
teléfono queda *por debajo* de la banda negra, así que el escaneo se detiene en la
primera fila clara y deja la banda entera adentro (esto dejó un borde negro en la 09
durante dos intentos). El método que sí funciona: marcar cada fila como oscura o no
(≥75% de píxeles por debajo de 40) y quedarse con la **racha contigua de filas no
oscuras más larga**, sin importar qué haya en los bordes.

Para verificar, no mirar solo la última fila: hay que recorrer hacia adentro desde
cada borde contando filas/columnas oscuras. Con esa comprobación las ocho fotos dan
cero en los cuatro bordes.

## Pendientes antes de publicar

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

## Contacto

El botón del cierre apunta a `https://wa.me/5493434285941` con un mensaje
prellenado. El número también va visible como texto, así aparece en el PDF
(donde el enlace no sirve de nada).

## Deploy

Publicado en **https://grupos-misioneros.vercel.app** — Vercel conectado a este repo:
cada push a `main` publica solo. El subdominio gratuito es estable y no expira.

## El QR

Se genera con `scripts/generar-qr.py`, que además **verifica** lo que produce
(decodifica el resultado y lo prueba a tamaños chicos y desenfocado):

```bash
python scripts/generar-qr.py                                          # liso
python scripts/generar-qr.py --estilo iwg --logo assets/qr/logo-iwg-globo.png
```

| Archivo | Qué es | Mínimo impreso |
| --- | --- | --- |
| `qr-iwg.svg` / `.png` | **El recomendado.** Azul IWG, módulos redondeados, globo del logo al centro | 2,5 × 2,5 cm |
| `qr-grupos-misioneros.svg` / `.png` | Liso, negro. Menos denso, el más tolerante | 2 × 2 cm |
| `qr-iwg-logo-completo.svg` / `.png` | Con el lockup completo. **No usar en tarjeta**: a ese tamaño el texto es una manchita | — |

`logo-iwg-globo.png` es el globo extraído de `IWG.png`, umbralado para sacarle
la trama de puntitos del fondo y la textura de la tinta, que a 5 mm sólo son
suciedad. El logo completo se conserva en `logo-iwg-completo.png`.

Los tres son **estáticos**: la URL va codificada dentro del patrón, sin servicio
intermedio, así que no pueden caducar. Si la URL cambia hay que regenerarlos, y
las tarjetas ya impresas dejan de servir.

### Tres trampas, todas invisibles a ojo

Están documentadas en el script porque cada una produjo un QR que se veía
perfecto y no se podía leer:

1. **No reescalar.** Generar chico y agrandar con LANCZOS deja halos en los
   bordes que rompen la decodificación. El tamaño se controla con `U` (px por
   módulo) para que salga grande de entrada.
2. **El radio de las esquinas tiene techo.** Con módulos casi circulares
   (radio ≥ 0,42 del lado) los vecinos se tocan en un punto, el antialiasing se
   come la unión y se pierde la grilla. Medido rasterizando el SVG en el
   navegador: 0,42 no lee nunca, 0,32 sólo en grande, 0,25 siempre. Se usa 0,22.
3. **En el SVG hay que fusionar los módulos contiguos de cada fila** en un solo
   rect, con un solape mínimo. Un rect por módulo deja costuras claras entre
   vecinos al rasterizar a tamaños no enteros.

El logo tapa módulos, y eso funciona sólo por la corrección de errores nivel H
(~30%). El costo es que el código pasa de versión 3 a 5 (37×37 módulos en vez
de 29×29), o sea más denso, o sea que pide más tamaño impreso — de ahí los
2,5 cm en vez de 2.

### Al imprimir

- **No recortar el margen blanco.** Es el error más común y deja el QR ilegible.
- Oscuro sobre claro, nunca invertido.
- Poner también la URL en texto, para quien no pueda escanear.
- Imprimir una prueba y escanearla con varios teléfonos antes de la tirada.

## Accesibilidad

- Respeta `prefers-reduced-motion` (desactiva todas las animaciones).
- Navegable por teclado, con foco visible.
- Hoja de estilos de impresión: se puede imprimir la página y sale legible.
