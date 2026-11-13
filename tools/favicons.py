"""Renderiza as favicons a partir do monograma vetorizado (assets/img/mono.svg).
Em tamanhos pequenos o traço ganha espessura para não sumir. Uso: python tools/favicons.py"""
import os, re, io
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, 'assets', 'img')
CACAU = '#2B1A14'
mono = open(os.path.join(IMG, 'mono.svg'), encoding='utf-8').read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', mono).group(1).split()]
d = re.search(r' d="([^"]+)"', mono).group(1)
x, y, w, h = vb
lado = max(w, h)


def svg(margem, traco, ouro=True):
    L = lado * (1 + 2 * margem)
    cx, cy = x + w / 2, y + h / 2
    fill = 'url(#g)' if ouro else '#E3BD72'
    grad = ('<linearGradient id="g" x1="0" y1="0" x2=".3" y2="1">'
            '<stop offset="0" stop-color="#F0CD84"/><stop offset=".5" stop-color="#D7A851"/>'
            '<stop offset="1" stop-color="#C08C3E"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx - L / 2:.1f} {cy - L / 2:.1f} {L:.1f} {L:.1f}">'
            f'<defs>{grad}</defs><rect x="{cx - L / 2:.1f}" y="{cy - L / 2:.1f}" width="{L:.1f}" height="{L:.1f}" fill="{CACAU}"/>'
            f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{fill}" stroke-width="{traco}" stroke-linejoin="round"/></svg>')


# (arquivo, px, margem, traço em unidades do viewBox)
ALVOS = [('icon-512.png', 512, .16, 0), ('apple-touch-icon.png', 180, .16, 4),
         ('favicon-48.png', 48, .07, 16), ('favicon-32.png', 32, .05, 22), ('favicon-16.png', 16, .03, 30)]

open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8').write(svg(.08, 10))
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    g = b.new_page(viewport={'width': 600, 'height': 600})
    for nome, px, m, t in ALVOS:
        s = svg(m, t, ouro=px >= 48)
        # renderiza 4x maior e reduz com Lanczos para bordas limpas
        big = px * 4
        g.set_content(f'<style>html,body{{margin:0;background:{CACAU}}}svg{{display:block;width:{big}px;height:{big}px}}</style>{s}')
        png = g.locator('svg').screenshot()
        im = Image.open(io.BytesIO(png)).convert('RGB').resize((px, px), Image.LANCZOS)
        im.save(os.path.join(IMG, nome))
        print(nome)
    b.close()
ims = [Image.open(os.path.join(IMG, f'favicon-{n}.png')) for n in (16, 32, 48)]
ims[2].save(os.path.join(IMG, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ims[:2])
print('favicon.ico')
