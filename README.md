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

## Pendientes antes de publicar

- [ ] **Número de WhatsApp** — en `index.html`, buscar `wa.me/NUMERO` y poner el número
      real en formato internacional sin `+` ni espacios (ej. `5493434123456`).
- [ ] **PDF descargable** — exportar el Word original a PDF, guardarlo como
      `assets/grupos-misioneros.pdf`.
- [ ] **Datos del bloque "Quiénes somos"** — cuántos grupos participan y desde cuándo
      (hoy están como `·` en `index.html`).
- [ ] **Ilustraciones o fotos** — hoy el fondo son círculos de color. Ver la nota de
      abajo sobre fotos de menores.
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
