#!/usr/bin/env python3
"""Genera el QR de la tarjeta del congreso.

    python scripts/generar-qr.py                            # liso, negro
    python scripts/generar-qr.py --estilo iwg               # azul IWG, centro reservado
    python scripts/generar-qr.py --estilo iwg --logo iwg.png

El QR es **estático**: la URL va codificada dentro del patrón, sin ningún
servicio intermedio que pueda caducar. Si la URL cambia hay que regenerarlo,
y las tarjetas ya impresas dejan de funcionar.

Tres cosas que se aprendieron rompiéndolo (todas invisibles a ojo):

1. **No reescalar.** Generar chico y agrandar con LANCZOS deja halos en los
   bordes que impiden decodificar. El tamaño se controla con `U` (px por
   módulo) para que salga grande de entrada, sin resamplear nunca.

2. **El radio de los módulos tiene techo.** Con módulos casi circulares
   (radio ≥ 0.42 del lado) los vecinos se tocan en un punto, el antialiasing
   se come esa unión y la grilla se pierde. Verificado rasterizando el SVG en
   el navegador: 0.42 no lee nunca, 0.32 lee sólo en grande, 0.25 lee siempre.
   Se usa 0.22 para tener margen.

3. **El logo tapa módulos**, y eso funciona sólo porque el nivel de corrección
   H reconstruye hasta ~30% del patrón. El costo es que el código pasa de
   versión 3 a 5 (37x37 módulos en vez de 29x29), o sea más denso, o sea que
   necesita más tamaño impreso.

Por eso el script termina siempre decodificando lo que generó.
"""

import argparse
import base64
import os
import subprocess
import sys
import tempfile

import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFilter

URL = "https://grupos-misioneros.vercel.app"

NAVY = (29, 59, 96)       # #1D3B60 — azul marino IWG
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)   # blanco puro: máximo contraste para el escaneo

BORDE = 4        # zona muda, en módulos. Obligatoria, no se recorta al imprimir.
U = 40           # px por módulo en el PNG
RADIO = 0.22     # radio de esquina como fracción del módulo (techo seguro: 0.25)
HUECO = 0.20     # lado del hueco central como fracción del QR con borde


def matriz(correccion):
    qr = qrcode.QRCode(version=None, error_correction=correccion,
                       box_size=1, border=BORDE)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr, qr.get_matrix()     # la matriz ya incluye el borde


def zona_hueco(n, con_hueco):
    """Rango [ini, fin) de módulos que ocupa el hueco central."""
    if not con_hueco:
        return 0, 0
    h = int(n * HUECO)
    h += h % 2                     # par, para que quede centrado exacto
    ini = (n - h) // 2
    return ini, ini + h


def dibujar_png(m, color, radio, con_hueco, logo_path):
    n = len(m)
    lado = n * U
    ini, fin = zona_hueco(n, con_hueco)
    img = Image.new("RGB", (lado, lado), BLANCO)
    d = ImageDraw.Draw(img)
    r = U * radio
    for y in range(n):
        for x in range(n):
            if not m[y][x] or (ini <= x < fin and ini <= y < fin):
                continue
            d.rounded_rectangle([x * U, y * U, x * U + U, y * U + U],
                                radius=r, fill=color)
    if not con_hueco:
        return img

    x0, hs = ini * U, (fin - ini) * U
    d.rounded_rectangle([x0, x0, x0 + hs, x0 + hs], radius=hs // 6, fill=BLANCO)
    if logo_path is None:
        d.rounded_rectangle([x0, x0, x0 + hs, x0 + hs], radius=hs // 6,
                            outline=color, width=max(2, lado // 250))
        return img

    logo = Image.open(logo_path).convert("RGBA")
    margen = int(hs * 0.12)
    caja = hs - 2 * margen
    logo.thumbnail((caja, caja), Image.LANCZOS)
    img.paste(logo, (x0 + margen + (caja - logo.size[0]) // 2,
                     x0 + margen + (caja - logo.size[1]) // 2), logo)
    return img


def dibujar_svg(m, color, radio, con_hueco, logo_path, u=10):
    """Mismo dibujo que el PNG, en vector. Misma matriz, mismo radio."""
    n = len(m)
    lado = n * u
    ini, fin = zona_hueco(n, con_hueco)
    css = f"rgb({color[0]},{color[1]},{color[2]})"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" '
         f'xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'viewBox="0 0 {lado} {lado}" width="{lado}" height="{lado}" '
         f'shape-rendering="geometricPrecision">',
         f'<rect width="{lado}" height="{lado}" fill="#FFFFFF"/>',
         f'<g fill="{css}">']
    # Se fusionan los módulos contiguos de cada fila en un solo rect y se
    # solapan una fracción de unidad. Con un rect por módulo, al rasterizar
    # a un tamaño no entero el antialiasing deja costuras claras entre
    # vecinos y el decodificador pierde la grilla.
    eps = u * 0.006
    for y in range(n):
        x = 0
        while x < n:
            tapado = ini <= x < fin and ini <= y < fin
            if not m[y][x] or tapado:
                x += 1
                continue
            x0 = x
            while x < n and m[y][x] and not (ini <= x < fin and ini <= y < fin):
                x += 1
            p.append(f'<rect x="{x0*u-eps:.2f}" y="{y*u-eps:.2f}" '
                     f'width="{(x-x0)*u+2*eps:.2f}" height="{u+2*eps:.2f}" '
                     f'rx="{u*radio:.2f}"/>')
    p.append('</g>')

    if con_hueco:
        x0, hs = ini * u, (fin - ini) * u
        p.append(f'<rect x="{x0}" y="{x0}" width="{hs}" height="{hs}" '
                 f'rx="{hs/6:.1f}" fill="#FFFFFF"/>')
        if logo_path:
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            pad = hs * 0.12
            p.append(f'<image x="{x0+pad:.1f}" y="{x0+pad:.1f}" '
                     f'width="{hs-2*pad:.1f}" height="{hs-2*pad:.1f}" '
                     f'preserveAspectRatio="xMidYMid meet" '
                     f'xlink:href="data:image/png;base64,{b64}"/>')
        else:
            p.append(f'<rect x="{x0}" y="{x0}" width="{hs}" height="{hs}" '
                     f'rx="{hs/6:.1f}" fill="none" stroke="{css}" '
                     f'stroke-width="{u*0.32:.1f}"/>')
    p.append('</svg>')
    return "\n".join(p)


def verificar(img, etiqueta):
    try:
        from pyzbar.pyzbar import decode
    except ImportError:
        print(f"  [{etiqueta}] pyzbar no instalado, SIN VERIFICAR "
              "(pip install pyzbar)")
        return True

    g = img.convert("L")
    leido = decode(g)
    if not leido or leido[0].data.decode() != URL:
        print(f"  [{etiqueta}] *** NO DECODIFICA o devuelve otra cosa ***")
        return False
    print(f"  [{etiqueta}] decodifica -> {leido[0].data.decode()}")

    minimo = None
    for lado in (400, 300, 240, 200, 160, 120, 90, 70):
        c = g.resize((lado, lado), Image.LANCZOS)
        if bool(decode(c)) and bool(decode(c.filter(
                ImageFilter.GaussianBlur(radius=max(0.6, lado / 120))))):
            minimo = lado
    print(f"  [{etiqueta}] lee hasta {minimo}px de lado, nítido y desenfocado")
    return True


def verificar_svg(ruta_svg, etiqueta, chrome=None):
    """Rasteriza el SVG con Chrome y lo decodifica.

    El PNG y el SVG salen de la misma matriz, pero el renderizador del
    navegador antialiasea distinto que PIL, y ahí es donde el radio de las
    esquinas rompía la lectura. Vale verificarlo aparte.
    """
    chrome = chrome or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome):
        print(f"  [{etiqueta}] Chrome no encontrado, SVG sin verificar")
        return True
    try:
        from pyzbar.pyzbar import decode
    except ImportError:
        return True

    d = tempfile.mkdtemp()
    png = os.path.join(d, "r.png")
    html = os.path.join(d, "r.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset=utf-8>'
                '<style>body{margin:0;background:#fff}'
                'img{width:700px;height:700px;display:block}</style>'
                f'<img src="file:///{os.path.abspath(ruta_svg)}">')
    subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files",
                    "--window-size=720,720", f"--screenshot={png}",
                    "--virtual-time-budget=4000", f"file:///{html}"],
                   capture_output=True)
    if not os.path.exists(png):
        print(f"  [{etiqueta}] no se pudo rasterizar el SVG")
        return True
    r = decode(Image.open(png).convert("L"))
    ok = bool(r) and r[0].data.decode() == URL
    print(f"  [{etiqueta}] SVG rasterizado a 700px: "
          f"{'decodifica' if ok else '*** NO DECODIFICA ***'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estilo", choices=["liso", "iwg"], default="liso")
    ap.add_argument("--logo", help="PNG con transparencia para el centro")
    ap.add_argument("--salida", default="assets/qr")
    args = ap.parse_args()

    if args.logo and args.estilo == "liso":
        ap.error("el logo necesita --estilo iwg (que usa corrección H)")

    if args.estilo == "liso":
        qr, m = matriz(ERROR_CORRECT_M)
        color, radio, hueco = NEGRO, 0.0, False
        base = f"{args.salida}/qr-grupos-misioneros"
        nivel = "M (~15%)"
    else:
        qr, m = matriz(ERROR_CORRECT_H)
        color, radio, hueco = NAVY, RADIO, True
        base = f"{args.salida}/qr-iwg"
        nivel = "H (~30%)"

    img = dibujar_png(m, color, radio, hueco, args.logo)
    img.save(base + ".png")
    with open(base + ".svg", "w", encoding="utf-8") as f:
        f.write(dibujar_svg(m, color, radio, hueco, args.logo))

    print(f"Versión {qr.version} ({qr.modules_count}x{qr.modules_count} módulos "
          f"+ borde {BORDE}), corrección {nivel}")
    print(f"  {base}.png  ({img.size[0]}x{img.size[1]} px, sin reescalar)")
    print(f"  {base}.svg")

    ok = verificar(img, args.estilo)
    ok = verificar_svg(base + ".svg", args.estilo) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
