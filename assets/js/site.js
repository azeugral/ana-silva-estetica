/* Ana Silva Estética — movimento calmo: Lenis + GSAP ScrollTrigger */
(() => {
  const html = document.documentElement;
  html.classList.add('js');
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const toque = matchMedia('(pointer: coarse)').matches;
  const temGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  if (temGsap && !reduz) html.classList.add('has-motion');

  /* ---------- loader ---------- */
  const loader = document.querySelector('.loader');
  let sair;
  const fimLoader = new Promise(res => { sair = res; });
  if (loader) {
    if (reduz) { loader.classList.add('fora'); sair(); }
    else {
      requestAnimationFrame(() => requestAnimationFrame(() => loader.classList.add('a-desenhar')));
      const fecha = () => { if (loader.classList.contains('fora')) return; loader.classList.add('fora'); sair(); };
      const heroImg = document.querySelector('.arco-centro img');
      const pronta = heroImg && !heroImg.complete ? new Promise(r => { heroImg.addEventListener('load', r, { once: true }); heroImg.addEventListener('error', r, { once: true }); }) : Promise.resolve();
      Promise.all([pronta, new Promise(r => setTimeout(r, 1800))]).then(fecha);
      setTimeout(fecha, 3200); // segurança
    }
  } else sair();

  /* ---------- menu ---------- */
  const bt = document.querySelector('.nav-menu');
  const menu = document.getElementById('menu');
  let lenis;
  const abreMenu = (abrir) => {
    bt.setAttribute('aria-expanded', String(abrir));
    bt.setAttribute('aria-label', abrir ? 'Fechar menu' : 'Abrir menu');
    if (abrir) {
      menu.hidden = false;
      requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('aberto')));
      lenis && lenis.stop();
      document.body.style.overflow = 'hidden';
    } else {
      menu.classList.remove('aberto');
      setTimeout(() => { if (!menu.classList.contains('aberto')) menu.hidden = true; }, 600);
      lenis && lenis.start();
      document.body.style.overflow = '';
    }
  };
  bt && bt.addEventListener('click', () => abreMenu(bt.getAttribute('aria-expanded') !== 'true'));
  menu && menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => abreMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && bt.getAttribute('aria-expanded') === 'true') abreMenu(false); });

  /* ---------- nav: esconde ao descer ---------- */
  const nav = document.querySelector('.nav');
  let ultimo = 0;
  const aoRolar = (y) => {
    if (y > 240 && y > ultimo + 4) nav.classList.add('esconde');
    else if (y < ultimo - 4 || y < 240) nav.classList.remove('esconde');
    ultimo = y;
  };

  if (!temGsap || reduz) {
    addEventListener('scroll', () => aoRolar(scrollY), { passive: true });
    return;
  }

  /* ---------- GSAP + Lenis ---------- */
  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'power3.out', duration: .9 });

  if (typeof window.Lenis !== 'undefined') {
    lenis = new window.Lenis({ lerp: .085, smoothWheel: true, wheelMultiplier: .9, anchors: { offset: -20 } });
    lenis.on('scroll', ({ scroll }) => { ScrollTrigger.update(); aoRolar(scroll); });
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.stop();
    fimLoader.then(() => lenis.start());
  } else addEventListener('scroll', () => aoRolar(scrollY), { passive: true });

  /* hero: entrada coreografada depois do loader */
  const heroIn = gsap.utils.toArray('.hero-in').sort((a, b) => a.dataset.h - b.dataset.h);
  const letras = gsap.utils.toArray('.hn-l');
  gsap.set(heroIn, { autoAlpha: 0, y: 30 });
  gsap.set(letras, { yPercent: 70, autoAlpha: 0, filter: 'blur(14px)' });
  fimLoader.then(() => {
    const tl = gsap.timeline({ delay: .15 });
    tl.to('.arco-centro', { autoAlpha: 1, y: 0, duration: 1.4, ease: 'power4.out' }, 0)
      .fromTo('.arco-centro img', { scale: 1.14 }, { scale: 1, duration: 2.2, ease: 'power3.out' }, 0)
      .to('.chapeu.hero-in', { autoAlpha: 1, y: 0, duration: 1 }, .25)
      .to('.arco-lado', { autoAlpha: .92, y: 0, duration: 1.3, stagger: .12, ease: 'power4.out' }, .35)
      .to(letras, { yPercent: 0, autoAlpha: 1, filter: 'blur(0px)', duration: 1.5, stagger: .14, ease: 'power4.out' }, .5)
      .to('.hero-frase', { autoAlpha: 1, y: 0, duration: 1 }, 1.05)
      .to('.hero .botoes', { autoAlpha: 1, y: 0, duration: 1 }, 1.2);
  });

  /* texto palavra a palavra */
  const divide = (el) => {
    const frag = document.createDocumentFragment();
    const walk = (node, emWrap) => {
      node.childNodes.forEach(n => {
        if (n.nodeType === 3) {
          n.textContent.split(/(\s+)/).forEach(p => {
            if (!p) return;
            if (!p.trim()) { frag.appendChild(document.createTextNode(p)); return; }
            const m = document.createElement('span'); m.className = 'motion-word-mask'; m.setAttribute('aria-hidden', 'true');
            const w = document.createElement(emWrap ? 'em' : 'span'); w.className = 'motion-word'; w.textContent = p;
            m.appendChild(w); frag.appendChild(m);
          });
        } else if (n.nodeType === 1) walk(n, n.tagName === 'EM' || emWrap);
      });
    };
    const label = el.textContent.replace(/\s+/g, ' ').trim();
    walk(el, false);
    el.textContent = ''; el.appendChild(frag); el.setAttribute('aria-label', label);
  };
  gsap.utils.toArray('[data-motion-text]').forEach(el => {
    divide(el);
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(el.querySelectorAll('.motion-word'), { yPercent: 105, autoAlpha: 0 }, {
      yPercent: 0, autoAlpha: 1, duration: 1.1, ease: 'power4.out', stagger: .045,
      scrollTrigger: { trigger: el, start: 'top 84%', once: true }
    });
  });

  /* grupos */
  gsap.utils.toArray('[data-reveal-group]').forEach(g => {
    const itens = g.querySelectorAll('[data-reveal-item]');
    gsap.set(g, { autoAlpha: 1 });
    gsap.fromTo(itens, { y: 40, autoAlpha: 0 }, {
      y: 0, autoAlpha: 1, duration: 1.1, ease: 'power4.out', stagger: .09,
      scrollTrigger: { trigger: g, start: 'top 84%', once: true }
    });
  });

  /* elementos soltos */
  const presets = {
    'fade-up': [{ y: 30, autoAlpha: 0 }, { y: 0, autoAlpha: 1 }],
    'scale': [{ scale: .9, autoAlpha: 0 }, { scale: 1, autoAlpha: 1 }],
  };
  gsap.utils.toArray('[data-reveal]:not([data-reveal-item])').forEach(el => {
    const [de, para] = presets[el.dataset.reveal] || presets['fade-up'];
    gsap.fromTo(el, de, { ...para, duration: 1.1, ease: 'power4.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
  });

  /* arcos: revelação por máscara */
  gsap.utils.toArray('[data-image-reveal]').forEach(fig => {
    const img = fig.querySelector('img');
    gsap.set(fig, { autoAlpha: 1 });
    const tl = gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 85%', once: true } });
    tl.fromTo(fig, { clipPath: 'inset(100% 0 0 0 round 999px 999px 22px 22px)' }, { clipPath: 'inset(-12% -12% -12% -12% round 999px 999px 22px 22px)', duration: 1.6, ease: 'power4.out' })
      .fromTo(img, { scale: 1.16 }, { scale: 1, duration: 2, ease: 'power3.out' }, 0)
      .set(fig, { clearProps: 'clipPath' });
  });

  /* parallax suave */
  gsap.utils.toArray('[data-parallax-image]').forEach(img => {
    gsap.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.closest('figure'), start: 'top bottom', end: 'bottom top', scrub: 1.2 } });
  });
  gsap.utils.toArray('[data-parallax-layer]').forEach(l => {
    const v = Number(l.dataset.parallaxSpeed || .1);
    gsap.fromTo(l, { y: () => innerHeight * v }, { y: () => -innerHeight * v, ease: 'none', scrollTrigger: { trigger: l.closest('[data-parallax-section]') || l, start: 'top bottom', end: 'bottom top', scrub: 1.3, invalidateOnRefresh: true } });
  });

  /* traços dourados desenhados ao rolar */
  gsap.utils.toArray('.traco path').forEach(p => {
    gsap.fromTo(p, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: p.closest('section'), start: 'top 70%', end: 'bottom 40%', scrub: 1.4 } });
  });

  /* hero: leve afastamento ao sair */
  gsap.to('.hero-palco', { yPercent: 10, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 } });
  gsap.to('.hn', { yPercent: -18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 } });

  /* ---------- só ponteiro fino ---------- */
  if (!toque) {
    gsap.utils.toArray('[data-magnetic]').forEach(el => {
      const xTo = gsap.quickTo(el, 'x', { duration: .5, ease: 'power3.out' });
      const yTo = gsap.quickTo(el, 'y', { duration: .5, ease: 'power3.out' });
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        xTo((e.clientX - r.left - r.width / 2) * .16); yTo((e.clientY - r.top - r.height / 2) * .22);
      });
      el.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
    });

    const cur = document.querySelector('.cursor');
    if (cur) {
      const cx = gsap.quickTo(cur, 'x', { duration: .35, ease: 'power3.out' });
      const cy = gsap.quickTo(cur, 'y', { duration: .35, ease: 'power3.out' });
      addEventListener('pointermove', e => { cur.classList.add('on'); cx(e.clientX); cy(e.clientY); }, { passive: true });
      document.addEventListener('pointerleave', () => cur.classList.remove('on'));
      document.querySelectorAll('a, button, .carta, .b').forEach(t => {
        t.addEventListener('pointerenter', () => cur.classList.add('grande'));
        t.addEventListener('pointerleave', () => cur.classList.remove('grande'));
      });
    }

    document.querySelectorAll('[data-mouse-parallax]').forEach(sec => {
      const camadas = [...sec.querySelectorAll('[data-mouse-depth]')].map(l => ({
        d: Number(l.dataset.mouseDepth), x: gsap.quickTo(l, 'x', { duration: 1.2, ease: 'power3.out' }), y: gsap.quickTo(l, 'y', { duration: 1.2, ease: 'power3.out' })
      }));
      sec.addEventListener('pointermove', e => {
        const r = sec.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        camadas.forEach(c => { c.x(x * c.d); c.y(y * c.d); });
      });
      sec.addEventListener('pointerleave', () => camadas.forEach(c => { c.x(0); c.y(0); }));
    });
  }

  addEventListener('load', () => ScrollTrigger.refresh());
  document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh());
})();
