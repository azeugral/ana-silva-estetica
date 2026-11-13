"""Vetoriza a logo oficial (../_ref/ana-silva/logo/logo-oficial.webp) e gera favicons.

Saídas em assets/img/:
  logo.svg        logo inteira (monograma + ANA SILVA + ESTÉTICA), cor via currentColor
  logo-ouro.svg   logo inteira com degradê dourado (para og/impressão)
  mono.svg        só o monograma AS
  favicon.svg / favicon-32.png / apple-touch-icon.png / icon-512.png / favicon.ico
"""
import os, sys
import numpy as np
import potrace
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SRC = os.path.join(RAIZ, '..', '_ref', 'ana-silva', 'logo', 'logo-minimal.webp')
OUT = os.path.join(RAIZ, 'assets', 'img')

OURO = [(0, '#E7C074'), (.35, '#D2A04B'), (.6, '#B9853A'), (.8, '#D6A956'), (1, '#C08C3E')]
CACAU = '#2B1A14'


def mascara(im, escala=2):
    a = np.array(im.split()[-1])
    big = Image.fromarray(a).resize((a.shape[1] * escala, a.shape[0] * escala), Image.LANCZOS)
    return np.array(big) > 110


def tracar(bits, escala):
    bmp = potrace.Bitmap(~bits)  # potracer trata False como tinta
    path = bmp.trace(turdsize=6, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    f = lambda p: f"{p.x / escala:.2f} {p.y / escala:.2f}"
    for curve in path:
        d.append('M' + f(curve.start_point))
        for seg in curve.segments:
            if seg.is_corner:
                d.append('L' + f(seg.c) + 'L' + f(seg.end_point))
            else:
                d.append('C' + f(seg.c1) + ' ' + f(seg.c2) + ' ' + f(seg.end_point))
        d.append('Z')
    return ''.join(d)


def bbox(bits):
    ys, xs = np.where(bits)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def grad(id_):
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in OURO)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2=".22" y2="1">{stops}</linearGradient>'


def svg(d, box, fill, defs='', pad=0):
    x0, y0, x1, y1 = box
    vb = f"{x0 - pad:.1f} {y0 - pad:.1f} {x1 - x0 + 2 * pad:.1f} {y1 - y0 + 2 * pad:.1f}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
            f'{("<defs>" + defs + "</defs>") if defs else ""}'
            f'<path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>')


def main():
    im = Image.open(SRC).convert('RGBA')
    E = 2
    bits = mascara(im, E)
    # monograma: tudo à esquerda da coluna vazia entre o "Q" e o "A" de ANA
    cols = bits.any(axis=0)
    w = bits.shape[1]
    corte = None
    for x in range(int(w * .38), int(w * .48)):
        if not cols[x:x + 6].any():
            corte = x
            break
    if corte is None:
        # o rabo do S passa por baixo do A; corta acima da linha de ESTÉTICA
        corte = int(w * .425)
    mono_bits = bits.copy(); mono_bits[:, corte:] = False
    d_full = tracar(bits, E)
    d_mono = tracar(mono_bits, E)
    bf = [v / E for v in bbox(bits)]
    bm = [v / E for v in bbox(mono_bits)]

    open(os.path.join(OUT, 'logo.svg'), 'w').write(svg(d_full, bf, 'currentColor'))
    open(os.path.join(OUT, 'logo-ouro.svg'), 'w').write(svg(d_full, bf, 'url(#g)', grad('g')))
    open(os.path.join(OUT, 'mono.svg'), 'w').write(svg(d_mono, bm, 'currentColor'))
    open(os.path.join(OUT, 'mono-ouro.svg'), 'w').write(svg(d_mono, bm, 'url(#g)', grad('g')))

    # favicon: monograma dourado sobre quadrado cacau
    x0, y0, x1, y1 = bm
    lado = max(x1 - x0, y1 - y0) * 1.32
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    vb = f"{cx - lado / 2:.1f} {cy - lado / 2:.1f} {lado:.1f} {lado:.1f}"
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><defs>{grad("g")}</defs>'
           f'<rect x="{cx - lado / 2:.1f}" y="{cy - lado / 2:.1f}" width="{lado:.1f}" height="{lado:.1f}" fill="{CACAU}"/>'
           f'<path fill="url(#g)" fill-rule="evenodd" d="{d_mono}"/></svg>')
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(fav)

    print('corte', corte / E, 'full', bf, 'mono', bm, len(d_full), len(d_mono))


if __name__ == '__main__':
    main()
