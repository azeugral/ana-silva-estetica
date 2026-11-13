# -*- coding: utf-8 -*-
"""Fotos de página inteira (desktop e telemóvel). Uso: python tools/fotos.py [url]"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
URL = next((a for a in sys.argv[1:] if a.startswith('http')), 'http://127.0.0.1:8893/')
SAI = Path(__file__).resolve().parent.parent.parent / '_ref' / 'ana-silva' / 'fotos'; SAI.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for nome, vp, m in [('pc', (1440, 900), False), ('cel', (390, 844), True)]:
        c = b.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=1, is_mobile=m, has_touch=m)
        g = c.new_page(); g.goto(URL); g.wait_for_timeout(4800)
        g.screenshot(path=str(SAI / f'{nome}-hero.png'))
        # rola devagar para disparar todas as revelações
        h = g.evaluate('document.body.scrollHeight')
        for y in range(0, h, 500):
            g.mouse.wheel(0, 500); g.wait_for_timeout(120)
        g.wait_for_timeout(1800)
        g.evaluate("window.scrollTo(0,0)"); g.wait_for_timeout(600)
        g.screenshot(path=str(SAI / f'{nome}-full.png'), full_page=True)
        larg = g.evaluate('[document.documentElement.scrollWidth, innerWidth]')
        print(nome, 'altura', h, 'largura doc/vp', larg)
        c.close()
    b.close()
print('ok', SAI)
