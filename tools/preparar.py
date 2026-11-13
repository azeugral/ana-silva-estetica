# Gera as imagens do site a partir de ../_ref/ana-silva/ig (posts públicos do Instagram).
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

def salva(im, nome, larg, q=82):
    im = im.copy(); h = round(larg * im.size[1] / im.size[0])
    im = im.resize((larg, h), Image.LANCZOS)
    im.save(os.path.join(OUT, nome + '.webp'), quality=q, method=6)
    print(nome, im.size)

# (nome, origem, proporção, largura, fx, fy, zoom, caixa)
J = [
 ('hero-ana',      'DeH6LTjiBIS_4', 3/4, 960, .5, .42, 1.0, None),
 ('hero-sorriso',  'DHJ1GMMMWZC_1', 3/4, 640, .55, .5, 1.0, None),
 ('hero-pose',     'DeH6LTjiBIS_5', 3/4, 640, .5, .45, 1.0, None),
 ('sobre-ana',     'DeH6LTjiBIS_0', 4/5, 900, .5, .5, 1.0, None),
 ('sobre-perfil',  'DeH6LTjiBIS_1', 3/4, 600, .5, .5, 1.0, None),
 ('sobre-mao',     'DeH6LTjiBIS_3', 3/4, 600, .5, .45, 1.0, None),
 ('branq-tablet',  'DHJ1GMMMWZC_0', 4/5, 900, .45, .5, 1.0, None),
 ('branq-sessao',  'DexAJ-Cjol7_2', 4/3, 900, .5, .5, 1.0, (0, .52, 1, 1)),
 ('branq-cuidado', 'DexAJ-Cjol7_1', 4/3, 900, .5, .5, 1.0, (0, .055, 1, .5)),
 ('espaco-caixa',  'DexAJ-Cjol7_2', 4/3, 900, .5, .5, 1.0, (0, .055, 1, .5)),
 ('espaco-certif', 'DexAJ-Cjol7_1', 4/3, 900, .5, .5, 1.0, (0, .52, 1, 1)),
 ('form-ana',      'DeH6LTjiBIS_2', 3/4, 720, .5, .4, 1.0, None),
 ('imp-fama',      'DexAJ-Cjol7_0', 4/5, 720, .5, .4, 1.0, (0, .055, 1, .70)),
 ('imp-palais',    'Dfo4vykCIPE_0', 4/5, 720, .5, .4, 1.0, (0, 0, 1, .68)),
 ('imp-brinde',    'Dfo4vykCIPE_1', 4/5, 720, .5, .45, 1.0, (0, 0, 1, .70)),
 ('imp-mesa',      'Dfo4vykCIPE_2', 4/5, 720, .5, .4, 1.0, (0, 0, 1, .47)),
 ('mimate',        'DfUO7GRtGct_0', 4/5, 900, .5, .45, 1.0, None),
 ('reel-sorriso',  'reel_DfNibzTyMgw_0', 9/16, 360, .5, .5, 1.0, None),
 ('reel-gems',     'reel_DewLHUUq5B__0', 9/16, 360, .5, .5, 1.0, None),
 ('reel-sessao',   'reel_DfAcWK3T-dT_0', 9/16, 360, .5, .5, 1.0, None),
 ('reel-rua',      'reel_DeFQY9JINnk_0', 9/16, 540, .5, .5, 1.0, None),
 ('reel-caixa',    'reel_DabNx5yI-yH_0', 9/16, 360, .5, .5, 1.0, None),
 ('reel-luz',      'reel_Dfk0r7DyMdl_0', 9/16, 360, .5, .5, 1.0, None),
]
for nome, src, ar, larg, fx, fy, z, cx in J:
    salva(recorta(abre(src), ar, fx, fy, z, cx), nome, larg)

# destaques (150 px) para medalhões
for i, n in [(4, 'd-branq'), (1, 'd-micro'), (3, 'd-lifting'), (0, 'd-gems'), (5, 'd-cetim')]:
    salva(abre(f'destaque_{i}'), n, 150, 88)

# voucher: a caixa com o logótipo, em quadrado
salva(recorta(abre('DexAJ-Cjol7_2'), 1, .6, .55, 1.4, (0.18, .12, .82, .42)), 'd-voucher', 300, 86)

