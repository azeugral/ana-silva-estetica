"""Gera a sombra de ramos (oliveira) usada apagada no hero e no agendamento.
Saída: assets/img/sombra-ramo.webp (cacau com alfa). Uso: python tools/sombra.py"""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, 'assets', 'img', 'sombra-ramo.webp')
S = 1800
random.seed(7)


def bezier(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def folha(d, cx, cy, ang, comp, larg):
    pts = []
    for k in range(40):
        u = k / 39 * math.pi * 2
        x = math.cos(u) * comp / 2
        y = math.sin(u) * larg / 2 * (1 - .35 * math.cos(u))  # ponta mais fina
        pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
    d.polygon(pts, fill=255)


def ramo(d, p0, p1, p2, n, comp, esp):
    d.line([bezier(p0, p1, p2, t / 60) for t in range(61)], fill=255, width=esp)
    for i in range(n):
        t = .08 + .9 * i / n
        x, y = bezier(p0, p1, p2, t)
        x2, y2 = bezier(p0, p1, p2, min(t + .01, 1))
        base = math.atan2(y2 - y, x2 - x)
        lado = 1 if i % 2 else -1
        ang = base + lado * (math.radians(38) + random.uniform(-.2, .2))
        c = comp * random.uniform(.75, 1.1) * (1 - .35 * t)
        folha(d, x + math.cos(ang) * c / 2, y + math.sin(ang) * c / 2, ang, c, c * .24)


def camada(ramos, blur):
    im = Image.new('L', (S, S), 0)
    d = ImageDraw.Draw(im)
    for r in ramos:
        ramo(d, *r)
    return im.filter(ImageFilter.GaussianBlur(blur))


perto = camada([((0, 120), (520, 300), (1150, 980), 22, 230, 9),
                ((300, 230), (520, 560), (560, 1050), 12, 170, 6)], 7)
longe = camada([((0, 560), (600, 600), (1450, 1500), 20, 260, 10),
                ((0, -40), (700, 40), (1250, 420), 16, 210, 8)], 22)
alfa = Image.eval(perto, lambda v: v * .95)
alfa = Image.composite(alfa, Image.eval(longe, lambda v: v * .55), perto.point(lambda v: 255 if v > 4 else 0))
alfa = Image.fromarray(__import__('numpy').maximum(__import__('numpy').array(perto) * .95, __import__('numpy').array(longe) * .55).astype('uint8'))
cor = Image.new('RGBA', (S, S), (43, 26, 20, 0))
cor.putalpha(alfa)
cor = cor.resize((1200, 1200), Image.LANCZOS)
cor.save(OUT, quality=88, method=6)
print(OUT)
