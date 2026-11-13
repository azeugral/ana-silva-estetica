# Gera as imagens do site a partir de ../_ref/ana-silva/ig (posts públicos do Instagram).
# Cada imagem sai já na proporção exibida e com ~2x o tamanho em tela (limitada à resolução original).
import os
from PIL import Image, ImageOps
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IG = os.path.join(RAIZ, '..', '_ref', 'ana-silva', 'ig')
OUT = os.path.join(RAIZ, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)


def abre(n): return ImageOps.exif_transpose(Image.open(os.path.join(IG, n + '.jpg'))).convert('RGB')


def recorta(im, ar, fx=.5, fy=.5, zoom=1.0, caixa=None):
    if caixa:  # caixa relativa (x0,y0,x1,y1)
        w, h = im.size; im = im.crop((int(caixa[0]*w), int(caixa[1]*h), int(caixa[2]*w), int(caixa[3]*h)))
    w, h = im.size
    if w / h > ar: ch = h / zoom; cw = ch * ar
    else: cw = w / zoom; ch = cw / ar
    x = min(max(fx * w - cw / 2, 0), w - cw); y = min(max(fy * h - ch / 2, 0), h - ch)
    return im.crop((round(x), round(y), round(x + cw), round(y + ch)))


def salva(im, nome, larg, q=86):
    larg = min(larg, im.size[0])
    h = round(larg * im.size[1] / im.size[0])
    im = im.resize((larg, h), Image.LANCZOS)
    im.save(os.path.join(OUT, nome + '.webp'), quality=q, method=6)
    print(nome, im.size)


# (nome, origem, proporção, largura, fx, fy, zoom, caixa)
J = [
 ('a-tablet',   'DHJ1GMMMWZC_1', 4/5, 1200, .5, .5, 1.0, None),
 ('a-sobre',    'DeH6LTjiBIS_4', 4/5, 1200, .5, .45, 1.0, None),
 ('a-form',     'DeH6LTjiBIS_0', 4/5, 1200, .5, .42, 1.0, None),
 ('a-sessao',   'DexAJ-Cjol7_2', 4/3, 1200, .45, .6, 1.1, (0, .54, 1, 1)),
 ('a-cuidado',  'DexAJ-Cjol7_1', 4/3, 1200, .5, .5, 1.0, (0, .055, 1, .5)),
 ('a-caixa',    'DexAJ-Cjol7_2', 4/3, 1200, .5, .45, 1.1, (0, .07, 1, .47)),
 ('a-certif',   'DexAJ-Cjol7_1', 4/3, 1200, .5, .5, 1.0, (0, .52, 1, 1)),
 ('a-fama',     'DexAJ-Cjol7_0', 4/5, 900, .5, .4, 1.0, (0, .055, 1, .70)),
 ('a-palais',   'Dfo4vykCIPE_0', 4/5, 900, .5, .4, 1.0, (0, 0, 1, .68)),
 ('a-brinde',   'Dfo4vykCIPE_1', 4/5, 900, .5, .45, 1.0, (0, 0, 1, .70)),
 ('a-mesa',     'Dfo4vykCIPE_2', 4/5, 900, .5, .4, 1.0, (0, 0, 1, .47)),
 ('a-mimate',   'DfUO7GRtGct_0', 4/5, 1200, .5, .45, 1.0, None),
]
for nome, src, ar, larg, fx, fy, z, cx in J:
    salva(recorta(abre(src), ar, fx, fy, z, cx), nome, larg)

# imagem de partilha (og): logo oficial sobre porcelana
og = Image.new('RGB', (1200, 630), '#F7F3EC')
logo = Image.open(os.path.join(RAIZ, '..', '_ref', 'ana-silva', 'logo', 'logo-oficial.webp')).convert('RGBA')
logo = logo.crop(logo.getbbox()); logo.thumbnail((860, 300), Image.LANCZOS)
og.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2), logo)
og.save(os.path.join(OUT, 'og.jpg'), quality=90)
print('og')
