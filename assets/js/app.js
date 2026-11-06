/* Grupa 131 · Inițiere în Ofițer — biblioteca de studiu
   Vanilla JS, hash routing; works on GitHub Pages and when opened from disk (file://). */
(() => {
  'use strict';

  const C = window.LIB_CATALOG;
  const I = window.I18N;
  const DOCS = C.docs;
  const main = document.getElementById('main');
  const courseById = Object.fromEntries(C.courses.map(c => [c.id, c]));

  // ------------------------------------------------------------------ storage & preferences
  const store = {
    get(k, d) { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  const prefs = Object.assign({ lang: 'ro', scale: 1, theme: null, summary: null, zoom: 1 }, store.get('g131.prefs', {}));
  const studied = new Set(store.get('g131.studied', []).filter(id => DOCS[id]));
  let recent = store.get('g131.recent', []).filter(r => DOCS[r.id]);
  const positions = store.get('g131.pos', {});
  const savePrefs = () => store.set('g131.prefs', prefs);
  const savePositions = () => store.set('g131.pos', positions);

  // ------------------------------------------------------------------ i18n
  const urlLang = /[?&]lang=(ro|ru)\b/.exec(location.search);  // shareable link: …/?lang=ru
  if (urlLang) prefs.lang = urlLang[1];
  let lang = prefs.lang === 'ru' ? 'ru' : 'ro';
  const t = (key, vars) => {
    let s = I[lang] && I[lang][key] != null ? I[lang][key] : (I.ro[key] != null ? I.ro[key] : key);
    if (vars) s = s.replace(/\{(\w+)\}/g, (_, k) => (vars[k] != null ? vars[k] : ''));
    return s;
  };
  const L = o => (o == null ? '' : typeof o === 'string' ? o : (o[lang] || o.ro || ''));
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const pad = n => String(n).padStart(3, '0');
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const icon = (id, cls) => `<svg class="ico${cls ? ' ' + cls : ''}" aria-hidden="true"><use href="#${id}"/></svg>`;

  // ------------------------------------------------------------------ text folding (diacritics-insensitive search)
  const MARKS = /[̀-ͯ]/g;
  const foldFast = s => s.normalize('NFD').replace(MARKS, '').toLowerCase().replace(/\s+/g, ' ');
  const foldMap = new Map();
  function foldKeep(s) { // same length as the input, so positions can be mapped back
    let out = '';
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      const c = ch.charCodeAt(0);
      if (c < 128) { out += c >= 65 && c <= 90 ? String.fromCharCode(c + 32) : (c === 9 || c === 10 || c === 13 ? ' ' : ch); continue; }
      let f = foldMap.get(ch);
      if (f === undefined) {
        f = /\s/.test(ch) ? ' ' : ch.normalize('NFD').replace(MARKS, '').toLowerCase();
        if (f.length !== 1) { const l = ch.toLowerCase(); f = l.length === 1 ? l : ch; }
        foldMap.set(ch, f);
      }
      out += f;
    }
    return out;
  }
  // light stemming, so that "somarea" also finds "somare/somări" and "codul" finds "cod"
  const RO_SUFFIXES = ['urilor', 'urile', 'ilor', 'elor', 'ului', 'ile', 'ele', 'lor', 'lui', 'ul', 'ei', 'ii', 'ea', 'le', 'a', 'e', 'i', 'u'];
  function stem(w) {
    if (/[а-яё]/.test(w)) return w.length >= 5 ? w.replace(/[аяыиуюеоьй]+$/, '') : w;
    for (const s of ['ului', 'ul']) if (w.endsWith(s) && w.length - s.length >= 3) return w.slice(0, -s.length);  // definite article
    if (w.length < 6) return w;
    for (const s of RO_SUFFIXES) if (w.endsWith(s) && w.length - s.length >= 5) return w.slice(0, -s.length);
    return w;
  }
  const splitTerms = fq => [...new Set(fq.split(/[\s,.;:!?()"„”“«»'’/\\-]+/).filter(w => w.length >= 2).map(stem))];

  /** sorted, non-overlapping [start, end) ranges of the phrase (or else of the terms) inside folded text */
  function matchRanges(ft, phrase, terms) {
    const ranges = [];
    const scan = w => { let i = ft.indexOf(w); while (i >= 0) { ranges.push([i, i + w.length]); i = ft.indexOf(w, i + w.length); } };
    if (phrase && phrase.length >= 2) scan(phrase);
    if (!ranges.length) terms.forEach(scan);
    ranges.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
    const out = [];
    for (const r of ranges) { if (!out.length || r[0] >= out[out.length - 1][1]) out.push(r); }
    return out;
  }

  // ------------------------------------------------------------------ helpers for catalog data
  const docOrder = c => c.sections.reduce((a, s) => a.concat(s.docs), []);
  const accentOf = d => (courseById[d.course] || {}).color || '#1f4fa8';
  const typeLabel = d => L(C.types[d.type]);
  const typeIcon = d => (C.types[d.type] || {}).icon || 'i-doc';
  const kindIcon = d => (d.kind === 'slides' ? 'i-slides' : d.kind === 'scan' ? 'i-scan' : typeIcon(d));
  const countLabel = d => d.kind === 'slides' ? t('nSlides', { n: d.pages }) : (d.pages === 1 ? t('nPage1') : t('nPages', { n: d.pages }));
  const minutes = d => Math.max(1, Math.round(d.kind === 'slides' ? d.pages * 0.6 : (d.words || d.pages * 250) / 170));
  const docUrl = (id, params) => '#/doc/' + id + (params ? '?' + new URLSearchParams(params).toString() : '');
  const courseTitle = c => L(c.title);
  const courseFull = c => (c.subtitle ? `${L(c.title)} — ${L(c.subtitle)}` : L(c.title));
  const nMaterials = n => (n === 1 ? t('material1') : t('materials', { n }));
  const courseProgress = c => { const ids = docOrder(c); const done = ids.filter(id => studied.has(id)).length; return { done, total: ids.length, pct: ids.length ? Math.round(done * 100 / ids.length) : 0 }; };
  const thumbOf = id => `content/${id}/t001.webp`;

  // ------------------------------------------------------------------ script loading (works on file:// too)
  const scripts = {};
  function loadScript(src) {
    if (!scripts[src]) {
      scripts[src] = new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = src; s.async = true;
        s.onload = () => resolve();
        s.onerror = () => { delete scripts[src]; s.remove(); reject(new Error('Cannot load ' + src)); };
        document.head.appendChild(s);
      });
    }
    return scripts[src];
  }
  const docData = {};
  window.LIB = { doc(id, data) { docData[id] = data; } };
  async function getDoc(id) {
    if (!docData[id]) await loadScript(`content/${id}/doc.js?v=${C.built}`);
    if (!docData[id]) throw new Error('No data for ' + id);
    return docData[id];
  }
  let searchIndex = null;
  async function getSearchIndex() {
    if (!searchIndex) {
      await loadScript(`data/search.js?v=${C.built}`);
      const S = window.LIB_SEARCH;
      searchIndex = { docs: S.docs, items: S.items, folded: S.items.map(it => foldFast(it[2])) };
    }
    return searchIndex;
  }
  const metaFold = {};
  function docMeta(id) {
    if (!metaFold[id]) {
      const d = DOCS[id];
      const parts = [];
      ['ro', 'ru'].forEach(l => {
        parts.push(d.title && d.title[l], d.kicker && d.kicker[l], d.summary && d.summary[l]);
        if (d.points && d.points[l]) parts.push(d.points[l].join(' '));
        if (C.types[d.type]) parts.push(C.types[d.type][l]);
        const c = courseById[d.course];
        if (c) parts.push(c.title[l], c.subtitle && c.subtitle[l]);
      });
      metaFold[id] = { all: foldFast(parts.filter(Boolean).join(' ')), title: foldFast([d.title.ro, d.title.ru, d.kicker && d.kicker.ro, d.kicker && d.kicker.ru].filter(Boolean).join(' ')) };
    }
    return metaFold[id];
  }

  // ------------------------------------------------------------------ UI chrome: toast, theme, font size, language
  const toastEl = document.getElementById('toast');
  let toastTimer = 0;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toastEl.hidden = true; }, 2200);
  }

  const SCALES = [0.9, 1, 1.12, 1.25, 1.4, 1.6];
  function applyScale() {
    document.documentElement.style.setProperty('--fs-scale', prefs.scale);
    document.querySelectorAll('[data-fs="0"]').forEach(b => b.setAttribute('aria-pressed', String(prefs.scale === 1)));
    const v = document.getElementById('fsValue');
    if (v) v.textContent = Math.round(prefs.scale * 100) + '%';
  }
  function setScale(dir) {
    let i = SCALES.indexOf(prefs.scale);
    if (i < 0) i = 1;
    prefs.scale = dir === 0 ? 1 : SCALES[clamp(i + dir, 0, SCALES.length - 1)];
    savePrefs();
    applyScale();
    toast(t('fontToast', { n: Math.round(prefs.scale * 100) }));
  }

  function applyTheme() {
    const dark = prefs.theme ? prefs.theme === 'dark' : window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = dark ? '#050f20' : '#0b2447';
    document.querySelectorAll('[data-theme-set]').forEach(b => b.setAttribute('aria-pressed', String((b.dataset.themeSet === 'dark') === dark)));
    return dark;
  }
  function setTheme(name) {
    prefs.theme = name;
    savePrefs();
    toast(applyTheme() ? t('themeDark') : t('themeLight'));
  }

  function applyStatic() {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll('[data-i18n-aria]').forEach(el => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); el.title = t(el.dataset.i18nAria); });
    document.querySelectorAll('[data-i18n-ph]').forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
    document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    buildDrawer();
  }
  function setLang(l) {
    if (l === lang) return;
    lang = l;
    prefs.lang = l;
    savePrefs();
    applyStatic();
    route({ keepScroll: true });
    toast(t('langChanged'));
  }

  // ------------------------------------------------------------------ drawer (mobile menu)
  const drawer = document.getElementById('drawer');
  const backdrop = document.getElementById('drawerBackdrop');
  const menuBtn = document.getElementById('menuBtn');
  function buildDrawer() {
    const body = document.getElementById('drawerBody');
    const link = (href, ico, label, sub, accent) =>
      `<a class="navlink" href="${href}"${accent ? ` style="--accent:${accent}"` : ''}><span class="navlink__ico">${icon(ico)}</span><span>${esc(label)}${sub ? `<small>${esc(sub)}</small>` : ''}</span></a>`;
    body.innerHTML =
      link('#/', 'i-home', t('home')) +
      link('#/cautare', 'i-search', t('search')) +
      '<div class="drawer__sep"></div>' +
      C.courses.map(c => { const p = courseProgress(c); return link('#/curs/' + c.id, c.icon, courseTitle(c), c.subtitle ? L(c.subtitle) : t('progress', p), c.color); }).join('') +
      '<div class="drawer__sep"></div>' +
      C.general.map(id => link(docUrl(id), 'c-info', L(DOCS[id].title), L(DOCS[id].kicker))).join('') +
      link('#/despre', 'i-info', t('about'));
    markActiveNav();
  }
  function markActiveNav() {
    const h = location.hash || '#/';
    document.querySelectorAll('#drawerBody .navlink').forEach(a => {
      const href = a.getAttribute('href');
      const on = href === '#/' ? (h === '#/' || h === '#' || h === '') : h.split('?')[0] === href;
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
  }
  function openDrawer() {
    drawer.hidden = false; backdrop.hidden = false;
    menuBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    document.getElementById('drawerClose').focus();
  }
  function closeDrawer(focusBack) {
    if (drawer.hidden) return;
    drawer.hidden = true; backdrop.hidden = true;
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    if (focusBack) menuBtn.focus();
  }

  // ------------------------------------------------------------------ studied / recent
  function syncStudyButtons(id) {
    document.querySelectorAll(`[data-study="${id}"]`).forEach(b => {
      const on = studied.has(id);
      b.setAttribute('aria-pressed', String(on));
      if (b.dataset.label === 'long') b.innerHTML = icon('i-check') + `<span>${esc(on ? t('unmark') : t('markStudied'))}</span>`;
      else b.title = on ? t('studied') : t('markStudied');
      if (b.dataset.label !== 'long') b.setAttribute('aria-label', b.title);
    });
    document.querySelectorAll('[data-progress]').forEach(el => {
      const c = courseById[el.dataset.progress];
      if (!c) return;
      const p = courseProgress(c);
      const bar = el.querySelector('.progress > span');
      if (bar) bar.style.width = p.pct + '%';
      const lab = el.querySelector('.progress-label');
      if (lab) lab.textContent = t('progress', p);
    });
    document.querySelectorAll(`[data-studied-chip="${id}"]`).forEach(el => { el.hidden = !studied.has(id); });
  }
  function toggleStudied(id) {
    if (studied.has(id)) { studied.delete(id); toast(t('toastUnstudied')); } else { studied.add(id); toast(t('toastStudied')); }
    store.set('g131.studied', [...studied]);
    syncStudyButtons(id);
    buildDrawer();
  }
  function pushRecent(id) {
    recent = [{ id, at: Date.now() }].concat(recent.filter(r => r.id !== id)).slice(0, 8);
    store.set('g131.recent', recent);
  }

  // ------------------------------------------------------------------ shared fragments
  const progressBlock = c => {
    const p = courseProgress(c);
    return `<div class="course-card__foot" data-progress="${c.id}"><div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${p.pct}"><span style="width:${p.pct}%"></span></div><span class="progress-label">${esc(t('progress', p))}</span></div>`;
  };

  function courseCard(c, i) {
    const ids = docOrder(c);
    const slides = ids.reduce((a, id) => a + (DOCS[id].kind === 'slides' ? DOCS[id].pages : 0), 0);
    const pages = ids.reduce((a, id) => a + (DOCS[id].kind !== 'slides' ? DOCS[id].pages : 0), 0);
    return `<a class="course-card" href="#/curs/${c.id}" style="--accent:${c.color};animation-delay:${i * 50}ms">
      <div class="course-card__top">
        <span class="course-card__icon">${icon(c.icon)}</span>
        <div>
          <div class="course-card__code">${esc(c.code || t('discipline'))}</div>
          <h3 class="course-card__title">${esc(courseTitle(c))}</h3>
        </div>
      </div>
      ${c.subtitle ? `<p class="course-card__desc" style="flex:0;font-weight:650;color:var(--text)">${esc(L(c.subtitle))}</p>` : ''}
      <p class="course-card__desc">${esc(L(c.short))}</p>
      <div class="course-card__meta">
        <span class="chip">${icon('i-book')}${esc(nMaterials(ids.length))}</span>
        ${slides ? `<span class="chip">${icon('i-slides')}${esc(t('nSlides', { n: slides }))}</span>` : ''}
        ${pages ? `<span class="chip">${icon('i-pages')}${esc(t('nPages', { n: pages }))}</span>` : ''}
      </div>
      ${progressBlock(c)}
    </a>`;
  }

  function itemCard(id, i) {
    const d = DOCS[id];
    const on = studied.has(id);
    return `<div class="item" style="--accent:${accentOf(d)};animation-delay:${Math.min(i, 12) * 35}ms">
      <div class="item__thumb${d.kind === 'slides' ? '' : ' item__thumb--page'}"><img src="${thumbOf(id)}" alt="" loading="lazy" decoding="async"><span class="item__type">${icon(kindIcon(d))}</span></div>
      <div>
        ${d.kicker ? `<div class="item__kicker">${esc(L(d.kicker))}</div>` : ''}
        <a class="item__title item__link" href="${docUrl(id)}">${esc(L(d.title))}</a>
        <p class="item__desc">${esc(L(d.summary))}</p>
        <div class="item__meta">
          <span class="chip">${icon(typeIcon(d))}${esc(typeLabel(d))}</span>
          <span class="chip">${esc(countLabel(d))}</span>
          <span class="chip">${icon('i-clock')}${esc(t('minutes', { n: minutes(d) }))}</span>
          ${d.media ? `<span class="chip chip--gold">${icon('i-video')}${esc(t('video'))}</span>` : ''}
          <span class="chip chip--ok" data-studied-chip="${id}"${on ? '' : ' hidden'}>${icon('i-check')}${esc(t('studied'))}</span>
        </div>
      </div>
      <div class="item__side">
        <button type="button" class="item__done" data-study="${id}" aria-pressed="${on}" title="${esc(on ? t('studied') : t('markStudied'))}" aria-label="${esc(on ? t('studied') : t('markStudied'))}">${icon('i-check')}</button>
        ${icon('i-chev-r', 'item__go')}
      </div>
    </div>`;
  }

  function crumbs(list) {
    return `<nav class="crumbs" aria-label="breadcrumb">${list.map((c, i) =>
      (i ? icon('i-chev-r') : '') + (c.href ? `<a href="${c.href}">${esc(c.label)}</a>` : `<span>${esc(c.label)}</span>`)).join('')}</nav>`;
  }

  function setTitle(s) { document.title = (s ? s + ' · ' : '') + 'Grupa 131 · Inițiere în Ofițer'; }

  // ------------------------------------------------------------------ views
  const QUICK = [
    { ro: 'Codul roșu', ru: 'Красный код', q: 'codul roșu' },
    { ro: 'Somarea', ru: 'Окрик (somare)', q: 'somarea' },
    { ro: 'Intervenția graduală', ru: 'Поэтапное вмешательство', q: 'intervenția graduală' },
    { ro: 'Cordonul de ordine', ru: 'Оцепление', q: 'cordonul de ordine' },
    { ro: 'Poziția „Drepți”', ru: 'Стойка «Смирно»', q: 'poziția drepți' },
    { ro: 'Lanțul supraviețuirii', ru: 'Цепочка выживания', q: 'lanțul supraviețuirii' },
    { ro: 'Legitimarea', ru: 'Проверка документов', q: 'legitimarea' }
  ];

  function viewHome() {
    setTitle('');
    const s = C.stats;
    const rec = recent.filter(r => DOCS[r.id]).slice(0, 6);
    main.innerHTML = `
      <section class="hero">
        <svg class="hero__badge" viewBox="0 0 64 72" aria-hidden="true"><use href="#logo-badge"/></svg>
        <div class="wrap">
          <span class="hero__kicker">${icon('i-star')}${esc(t('heroKicker'))}</span>
          <h1 class="hero__title">${t('heroTitle')}</h1>
          <p class="hero__lead">${esc(t('heroLead'))}</p>
          <form class="hero-search" role="search" id="heroSearch">
            ${icon('i-search')}
            <input type="search" name="q" enterkeyhint="search" autocomplete="off" placeholder="${esc(t('searchPh'))}" aria-label="${esc(t('search'))}">
            <button type="submit">${esc(t('searchBtn'))}</button>
          </form>
          <div class="hero__chips" aria-label="${esc(t('quick'))}">
            ${QUICK.map(q => `<button type="button" data-q="${esc(q.q)}">${esc(q[lang] || q.ro)}</button>`).join('')}
          </div>
        </div>
      </section>
      <div class="wrap">
        <div class="stats">
          <div class="stat"><span class="stat__ico">${icon('i-grid')}</span><div><div class="stat__num">${s.courses}</div><div class="stat__label">${esc(t('statCourses'))}</div></div></div>
          <div class="stat"><span class="stat__ico">${icon('i-book')}</span><div><div class="stat__num">${s.docs}</div><div class="stat__label">${esc(t('statDocs'))}</div></div></div>
          <div class="stat"><span class="stat__ico">${icon('i-slides')}</span><div><div class="stat__num">${s.slides}</div><div class="stat__label">${esc(t('statSlides'))}</div></div></div>
          <div class="stat"><span class="stat__ico">${icon('i-pages')}</span><div><div class="stat__num">${s.pages}</div><div class="stat__label">${esc(t('statPages'))}</div></div></div>
        </div>
        ${rec.length ? `
        <section class="section">
          <div class="section__head">
            <div><h2 class="section__title">${esc(t('continueTitle'))}</h2><p class="section__sub">${esc(t('continueSub'))}</p></div>
            <button type="button" class="btn btn--ghost btn--sm" id="clearRecent">${icon('i-history')}${esc(t('clearRecent'))}</button>
          </div>
          <div class="recent">${rec.map(r => {
            const d = DOCS[r.id]; const p = positions[r.id];
            const where = p && p.p > 1 ? ` · ${d.kind === 'slides' ? t('slide') : t('page')} ${p.p}` : '';
            return `<a class="recent__item" href="${docUrl(r.id)}" style="--accent:${accentOf(d)}"><img class="recent__thumb" src="${thumbOf(r.id)}" alt="" loading="lazy"><div><div class="recent__title">${esc(L(d.title))}</div><div class="recent__meta">${esc((courseById[d.course] ? courseTitle(courseById[d.course]) : L(d.kicker)) + where)}</div></div></a>`;
          }).join('')}</div>
        </section>` : ''}
        <section class="section" id="courses">
          <div class="section__head"><div><h2 class="section__title">${esc(t('coursesTitle'))}</h2><p class="section__sub">${esc(t('coursesSub'))}</p></div></div>
          <div class="courses">${C.courses.map(courseCard).join('')}</div>
        </section>
        <section class="section">
          ${C.general.map(id => `<a class="about-card" href="${docUrl(id)}">
            <span class="about-card__ico">${icon('c-info')}</span>
            <div><h3>${esc(t('aboutCourseTitle'))}</h3><p>${esc(t('aboutCourseText'))}</p></div>
            <span class="btn btn--gold">${esc(t('open'))}${icon('i-chev-r')}</span>
          </a>`).join('')}
        </section>
        <section class="section">
          <div class="section__head"><h2 class="section__title">${esc(t('tipsTitle'))}</h2></div>
          <div class="tips">
            <div class="tip"><span class="tip__ico">${icon('i-text')}</span><div><b>${esc(t('tip1'))}</b><p>${esc(t('tip1t'))}</p></div></div>
            <div class="tip"><span class="tip__ico">${icon('i-globe')}</span><div><b>${esc(t('tip2'))}</b><p>${esc(t('tip2t'))}</p></div></div>
            <div class="tip"><span class="tip__ico">${icon('i-search')}</span><div><b>${esc(t('tip3'))}</b><p>${esc(t('tip3t'))}</p></div></div>
            <div class="tip"><span class="tip__ico">${icon('i-check')}</span><div><b>${esc(t('tip4'))}</b><p>${esc(t('tip4t'))}</p></div></div>
          </div>
        </section>
      </div>`;
    const form = document.getElementById('heroSearch');
    form.addEventListener('submit', e => { e.preventDefault(); goSearch(form.q.value); });
    main.querySelectorAll('.hero__chips [data-q]').forEach(b => b.addEventListener('click', () => goSearch(b.dataset.q)));
    const clr = document.getElementById('clearRecent');
    if (clr) clr.addEventListener('click', () => { recent = []; store.set('g131.recent', recent); route({ keepScroll: true }); });
  }

  function viewCourse(c) {
    setTitle(courseTitle(c));
    const ids = docOrder(c);
    const slides = ids.reduce((a, id) => a + (DOCS[id].kind === 'slides' ? DOCS[id].pages : 0), 0);
    const pages = ids.reduce((a, id) => a + (DOCS[id].kind !== 'slides' ? DOCS[id].pages : 0), 0);
    const p = courseProgress(c);
    let n = 0;
    main.innerHTML = `
      <section class="phead" style="--accent:${c.color}">
        <div class="wrap">
          ${crumbs([{ href: '#/', label: t('home') }, { label: courseTitle(c) }])}
          <div class="phead__row">
            <span class="phead__icon">${icon(c.icon)}</span>
            <div>
              <div class="phead__kicker">${esc(c.code ? t('discipline') + ' · ' + c.code : t('discipline'))}</div>
              <h1 class="phead__title">${esc(courseTitle(c))}</h1>
              ${c.subtitle ? `<div style="font-weight:650;color:#e3ebf7">${esc(L(c.subtitle))}</div>` : ''}
            </div>
          </div>
          <p class="phead__desc">${esc(L(c.desc))}</p>
          <div class="phead__meta">
            <span class="chip chip--gold">${icon('i-book')}${esc(nMaterials(ids.length))}</span>
            ${slides ? `<span class="chip">${icon('i-slides')}${esc(t('nSlides', { n: slides }))}</span>` : ''}
            ${pages ? `<span class="chip">${icon('i-pages')}${esc(t('nPages', { n: pages }))}</span>` : ''}
            <span class="course-card__foot" data-progress="${c.id}" style="padding:0"><span class="progress"><span style="width:${p.pct}%"></span></span><span class="progress-label">${esc(t('progress', p))}</span></span>
          </div>
        </div>
      </section>
      <div class="wrap course-layout">
        <div>
          ${c.sections.map(s => `
            <section class="group" id="sec-${s.key}">
              <h2 class="group__title">${esc(L(s.title))} <span class="count">${s.docs.length}</span></h2>
              <div class="items">${s.docs.map(id => itemCard(id, n++)).join('')}</div>
            </section>`).join('')}
        </div>
        <aside class="course-aside">
          ${c.sections.length > 1 ? `<div class="panel"><h2 class="panel__title">${icon('i-list')}${esc(t('courseContents'))}</h2>
            <nav class="toc">${c.sections.map(s => `<button type="button" data-scroll="sec-${s.key}">${esc(L(s.title))} (${s.docs.length})</button>`).join('')}</nav></div>` : ''}
          ${c.related && c.related.length ? `<div class="panel"><h2 class="panel__title">${icon('i-book')}${esc(t('relatedTitle'))}</h2>
            <nav class="toc">${c.related.map(id => `<a href="${docUrl(id)}">${esc(L(DOCS[id].title))}<br><small style="color:var(--muted)">${esc(courseTitle(courseById[DOCS[id].course]))}</small></a>`).join('')}</nav></div>` : ''}
          <div class="panel"><h2 class="panel__title">${icon('i-grid')}${esc(t('otherCourses'))}</h2>
            <nav class="toc">${C.courses.filter(x => x.id !== c.id).map(x => `<a href="#/curs/${x.id}">${esc(courseFull(x))}</a>`).join('')}</nav></div>
        </aside>
      </div>`;
    main.querySelectorAll('[data-scroll]').forEach(b => b.addEventListener('click', () => {
      const el = document.getElementById(b.dataset.scroll);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  }

  // ------------------------------------------------------------------ document viewer
  function viewDoc(id, params) {
    const d = DOCS[id];
    const course = courseById[d.course];
    const accent = accentOf(d);
    const isSlides = d.kind === 'slides';
    const saved = positions[id] || {};
    const q = (params.get('q') || '').trim();
    const modes = isSlides ? ['slides', 'text'] : d.hasText ? ['text', 'pages'] : ['pages'];
    let mode = params.get('m') || (q ? (isSlides ? 'slides' : d.hasText ? 'text' : 'pages') : '') || saved.m || d.mode;
    if (!modes.includes(mode)) mode = modes[0];
    const explicitPage = params.get('p');
    let page = clamp(parseInt(explicitPage || saved.p || 1, 10) || 1, 1, d.pages);
    let zoom = prefs.zoom || 1;
    let data = null;
    let modeCleanup = null;
    let restoreY = !explicitPage && !q && saved.m === mode ? saved.y : null;
    pushRecent(id);
    setTitle(L(d.title));

    const order = course ? docOrder(course) : [];
    const oi = order.indexOf(id);
    const prevId = oi > 0 ? order[oi - 1] : null;
    const nextId = oi >= 0 && oi < order.length - 1 ? order[oi + 1] : null;
    const crumbList = [{ href: '#/', label: t('home') }];
    if (course) crumbList.push({ href: '#/curs/' + course.id, label: courseTitle(course) });
    crumbList.push({ label: L(d.kicker) || typeLabel(d) });
    const modeLabel = m => (m === 'slides' ? t('modeSlides') : m === 'pages' ? t('modePages') : t('modeText'));
    const modeIcon = m => (m === 'slides' ? 'i-slides' : m === 'pages' ? 'i-pages' : 'i-text');
    const summaryHtml = (d.summary || d.points) ? `
      <details class="summary" id="summary"${(prefs.summary == null ? lang === 'ru' : prefs.summary) ? ' open' : ''}>
        <summary>${icon('i-bulb')}<span>${esc(t('summaryTitle'))}</span>${icon('i-chev-d')}</summary>
        <div class="summary__body">
          ${d.summary ? `<p>${esc(L(d.summary))}</p>` : ''}
          ${d.points && d.points[lang] ? `<ul>${d.points[lang].map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}
        </div>
      </details>` : '';

    main.innerHTML = `
      <section class="phead vhead" style="--accent:${accent}">
        <div class="wrap">
          ${crumbs(crumbList)}
          <div class="phead__kicker">${esc([L(d.kicker), typeLabel(d)].filter(Boolean).join(' · '))}</div>
          <h1 class="phead__title">${esc(L(d.title))}</h1>
          <div class="vhead__row">
            <div class="phead__meta">
              <span class="chip chip--gold">${icon(kindIcon(d))}${esc(typeLabel(d))}</span>
              <span class="chip">${esc(countLabel(d))}</span>
              <span class="chip">${icon('i-clock')}${esc(t('minutes', { n: minutes(d) }))}</span>
              ${d.ocr ? `<span class="chip">${icon('i-scan')}OCR</span>` : ''}
              ${d.media ? `<span class="chip">${icon('i-video')}${esc(t('video'))}</span>` : ''}
            </div>
            <div class="vhead__actions">
              <button type="button" class="btn btn--sm btn--toggle" data-study="${id}" data-label="long" aria-pressed="${studied.has(id)}">${icon('i-check')}<span>${esc(studied.has(id) ? t('unmark') : t('markStudied'))}</span></button>
              ${course ? `<a class="btn btn--sm" href="#/curs/${course.id}">${icon('i-arrow-l')}<span>${esc(t('backToCourse'))}</span></a>` : `<a class="btn btn--sm" href="#/">${icon('i-arrow-l')}<span>${esc(t('home'))}</span></a>`}
            </div>
          </div>
        </div>
      </section>
      <div class="vbar" id="vbar"><div class="wrap vbar__inner">
        ${modes.length > 1 ? `<div class="tabs" role="tablist">${modes.map(m => `<button type="button" role="tab" data-mode="${m}" aria-selected="${m === mode}">${icon(modeIcon(m))}<span>${esc(modeLabel(m))}</span></button>`).join('')}</div>`
          : `<div class="tabs"><button type="button" aria-selected="true" tabindex="-1">${icon(modeIcon(mode))}<span>${esc(modeLabel(mode))}</span></button></div>`}
        <span class="vbar__spacer"></span>
        <div id="vtools" style="display:flex;align-items:center;gap:.4rem;flex-wrap:wrap"></div>
      </div></div>
      <div class="wrap vbody">
        <div id="vinfo">
          ${summaryHtml}
          ${lang === 'ru' ? `<p class="notice">${icon('i-globe')}<span>${esc(t('langNotice'))}</span></p>` : ''}
          ${d.ocr ? `<p class="notice">${icon('i-info')}<span>${esc(t('ocrNote'))}</span></p>` : ''}
        </div>
        <div id="vcontent"><div class="loading"><span class="spinner"></span>${esc(t('loading'))}</div></div>
        ${course ? `<nav class="docnav">
          ${prevId ? `<a href="${docUrl(prevId)}"><small>${icon('i-chev-l')}${esc(t('prevDoc'))}</small><span>${esc(L(DOCS[prevId].title))}</span></a>` : '<span></span>'}
          ${nextId ? `<a class="next" href="${docUrl(nextId)}"><small>${esc(t('nextDoc'))}${icon('i-chev-r')}</small><span>${esc(L(DOCS[nextId].title))}</span></a>` : '<span></span>'}
        </nav>` : ''}
      </div>`;

    const content = document.getElementById('vcontent');
    const tools = document.getElementById('vtools');
    const sumEl = document.getElementById('summary');
    if (sumEl) sumEl.addEventListener('toggle', () => { prefs.summary = sumEl.open; savePrefs(); });

    function remember(extra) {
      positions[id] = Object.assign({ m: mode, p: page }, extra || {});
      savePositions();
      const params = new URLSearchParams();
      if (mode !== d.mode) params.set('m', mode);
      if (page > 1) params.set('p', page);
      const h = docUrl(id) + (params.toString() ? '?' + params : '');
      if (location.hash !== h) history.replaceState(null, '', h);
    }

    // ---------------- slides
    function renderSlides() {
      const N = d.pages;
      const [w, h] = data.pages[0] || [16, 9];
      const src = n => `content/${id}/p${pad(n)}.webp`;
      content.innerHTML = `
        <div class="stage" id="stage" style="--ar:${w}/${h};--ar-num:${(w / h).toFixed(4)}">
          <div class="stage__frame"><img id="slideImg" src="${src(page)}" width="${w}" height="${h}" alt=""></div>
          <button type="button" class="stage__nav stage__nav--prev" id="sPrev" aria-label="${esc(t('prevSlide'))}">${icon('i-chev-l')}</button>
          <button type="button" class="stage__nav stage__nav--next" id="sNext" aria-label="${esc(t('nextSlide'))}">${icon('i-chev-r')}</button>
          <button type="button" class="stage__fs" id="sFs" aria-label="${esc(t('fullscreen'))}" title="${esc(t('fullscreen'))} (F)">${icon('i-expand')}</button>
          <span class="stage__media" id="sMedia" hidden>${icon('i-video')}${esc(t('mediaOnSlide'))}</span>
          <span class="stage__count" id="sCount"></span>
        </div>
        <div class="progressbar"><span id="sBar"></span></div>
        <div class="thumbs" id="thumbs" style="--ar:${w}/${h}">${data.pages.map((_, i) =>
          `<button type="button" data-n="${i + 1}" aria-label="${esc(t('slide'))} ${i + 1}"><img src="content/${id}/t${pad(i + 1)}.webp" alt="" loading="lazy" decoding="async"><span>${i + 1}</span></button>`).join('')}</div>
        <div class="slide-text" id="sText" lang="ro"></div>`;
      tools.innerHTML = `
        <div class="pager">
          <button type="button" class="btn btn--sm btn--icon" id="tPrev" aria-label="${esc(t('prevSlide'))}">${icon('i-chev-l')}</button>
          <span>${esc(t('slide'))} <b id="tNum"></b> ${esc(t('of'))} ${N}</span>
          <button type="button" class="btn btn--sm btn--icon" id="tNext" aria-label="${esc(t('nextSlide'))}">${icon('i-chev-r')}</button>
        </div>`;
      const img = document.getElementById('slideImg');
      const stage = document.getElementById('stage');
      const thumbs = document.getElementById('thumbs');
      const textEl = document.getElementById('sText');
      const preload = n => { if (n >= 1 && n <= N) { const im = new Image(); im.src = src(n); } };

      function show(n, scrollThumb) {
        page = clamp(n, 1, N);
        img.src = src(page);
        const s = data.slides[page - 1] || {};
        const title = (s.h || '').match(/<div class="stitle">(.*?)<\/div>/);
        img.alt = `${t('slide')} ${page}` + (title ? ': ' + title[1].replace(/<[^>]+>/g, '') : '');
        document.getElementById('sCount').textContent = `${page} / ${N}`;
        document.getElementById('tNum').textContent = page;
        document.getElementById('sBar').style.width = (page / N * 100) + '%';
        ['sPrev', 'tPrev'].forEach(x => { document.getElementById(x).disabled = page === 1; });
        ['sNext', 'tNext'].forEach(x => { document.getElementById(x).disabled = page === N; });
        thumbs.querySelectorAll('button').forEach(b => b.setAttribute('aria-current', String(+b.dataset.n === page)));
        if (scrollThumb !== false) {
          const tb = thumbs.querySelector(`[data-n="${page}"]`);
          if (tb) thumbs.scrollTo({ left: tb.offsetLeft - thumbs.clientWidth / 2 + tb.clientWidth / 2, behavior: 'smooth' });
        }
        const media = (s.m || []).map(m => m.t === 'video'
          ? `<div class="media-item"><div class="media-item__label">${icon('i-video')}${esc(t('video'))}</div><video controls playsinline preload="metadata" src="content/${id}/${m.s}" poster="${src(page)}"></video></div>`
          : `<div class="media-item"><div class="media-item__label">${icon('i-volume')}${esc(t('audio'))}</div><audio controls preload="none" src="content/${id}/${m.s}"></audio></div>`).join('');
        document.getElementById('sMedia').hidden = !media;
        textEl.innerHTML = `<div class="slide-text__head">${icon('i-text')}${esc(t('slideText'))} ${page}</div>
          <div class="slide-text__body">${s.h || '<p class="empty-note">—</p>'}</div>
          ${s.n ? `<div class="slide-notes"><b>${esc(t('notes'))}</b>${s.n}</div>` : ''}
          ${media ? `<div class="media-list" id="mediaList">${media}</div>` : ''}`;
        if (q) highlightIn(textEl, q);
        preload(page + 1); preload(page - 1);
        remember();
      }
      const go = dlt => show(page + dlt);
      document.getElementById('sPrev').onclick = () => go(-1);
      document.getElementById('sNext').onclick = () => go(1);
      document.getElementById('tPrev').onclick = () => go(-1);
      document.getElementById('tNext').onclick = () => go(1);
      document.getElementById('sMedia').onclick = () => { const ml = document.getElementById('mediaList'); if (ml) ml.scrollIntoView({ behavior: 'smooth', block: 'center' }); };
      thumbs.addEventListener('click', e => { const b = e.target.closest('button[data-n]'); if (b) show(+b.dataset.n, false); });

      // fullscreen (native, with a CSS fallback for iPhone)
      let fakeFs = false;
      function toggleFs() {
        if (document.fullscreenElement) { document.exitFullscreen(); return; }
        if (fakeFs) { fakeFs = false; stage.classList.remove('is-fs'); document.body.style.overflow = ''; return; }
        if (stage.requestFullscreen && document.fullscreenEnabled) stage.requestFullscreen().catch(() => {});
        else { fakeFs = true; stage.classList.add('is-fs'); document.body.style.overflow = 'hidden'; }
      }
      document.getElementById('sFs').onclick = toggleFs;
      img.addEventListener('dblclick', toggleFs);

      // swipe
      let sx = null, sy = 0;
      stage.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') { sx = e.clientX; sy = e.clientY; } });
      stage.addEventListener('pointerup', e => {
        if (sx == null) return;
        const dx = e.clientX - sx, dy = e.clientY - sy;
        sx = null;
        if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) go(dx < 0 ? 1 : -1);
      });
      stage.addEventListener('pointercancel', () => { sx = null; });

      const onKey = e => {
        if (e.target.closest('input, textarea, select, [contenteditable]')) return;
        if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(1); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(-1); }
        else if (e.key === 'Home') { e.preventDefault(); show(1); }
        else if (e.key === 'End') { e.preventDefault(); show(N); }
        else if (e.key === 'f' || e.key === 'F') toggleFs();
        else if (e.key === 'Escape' && fakeFs) toggleFs();
      };
      document.addEventListener('keydown', onKey);
      show(page);
      return () => {
        document.removeEventListener('keydown', onKey);
        if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
        document.body.style.overflow = '';
      };
    }

    // ---------------- original pages
    function renderPages() {
      const N = d.pages;
      const ZOOMS = [0.5, 0.75, 1, 1.25, 1.5, 2];
      content.innerHTML = `<div class="pages-wrap"><div class="pages" id="pages" style="--zoom:${zoom}">${data.pages.map((s, i) =>
        `<figure class="page" id="page-${i + 1}" style="--ar:${s[0]}/${s[1]}"><img src="content/${id}/p${pad(i + 1)}.webp" width="${s[0]}" height="${s[1]}" loading="lazy" decoding="async" alt="${esc(t('page'))} ${i + 1}"><span class="page__no">${i + 1}</span></figure>`).join('')}</div></div>`;
      tools.innerHTML = `
        <button type="button" class="btn btn--sm btn--icon" id="zOut" aria-label="${esc(t('zoomOut'))}" title="${esc(t('zoomOut'))}">${icon('i-zoom-out')}</button>
        <span class="zoom-label" id="zLab"></span>
        <button type="button" class="btn btn--sm btn--icon" id="zIn" aria-label="${esc(t('zoomIn'))}" title="${esc(t('zoomIn'))}">${icon('i-zoom-in')}</button>
        <form class="pager" id="pForm"><label><span class="sr-only">${esc(t('jumpTo'))}</span><input type="number" inputmode="numeric" min="1" max="${N}" id="pInput" value="${page}" aria-label="${esc(t('jumpTo'))}"></label><span>/ ${N}</span></form>`;
      const pagesEl = document.getElementById('pages');
      const zLab = document.getElementById('zLab');
      const pInput = document.getElementById('pInput');
      const setZoom = z => {
        zoom = z; prefs.zoom = z; savePrefs();
        pagesEl.style.setProperty('--zoom', z);
        zLab.textContent = Math.round(z * 100) + '%';
        document.getElementById('zOut').disabled = z <= ZOOMS[0];
        document.getElementById('zIn').disabled = z >= ZOOMS[ZOOMS.length - 1];
      };
      const jump = (n, smooth) => { const el = document.getElementById('page-' + clamp(n, 1, N)); if (el) el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' }); };
      setZoom(zoom);
      document.getElementById('zOut').onclick = () => { const p = page; setZoom(ZOOMS[Math.max(0, ZOOMS.indexOf(zoom) - 1)] || 1); jump(p); };
      document.getElementById('zIn').onclick = () => { const p = page; setZoom(ZOOMS[Math.min(ZOOMS.length - 1, ZOOMS.indexOf(zoom) + 1)] || 1); jump(p); };
      document.getElementById('pForm').addEventListener('submit', e => { e.preventDefault(); jump(+pInput.value || 1, true); });
      pInput.addEventListener('change', () => jump(+pInput.value || 1, true));

      const io = new IntersectionObserver(entries => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            page = +en.target.id.slice(5);
            if (document.activeElement !== pInput) pInput.value = page;
            remember();
          }
        });
      }, { rootMargin: '-40% 0px -55% 0px' });
      pagesEl.querySelectorAll('.page').forEach(el => io.observe(el));
      if (page > 1) requestAnimationFrame(() => jump(page));
      if (q && explicitPage) toast(t('foundOnPage', { p: page }));
      return () => io.disconnect();
    }

    // ---------------- reflowable text
    function slidesAsText() {
      const toc = [];
      const html = data.slides.map((s, i) => {
        const m = (s.h || '').match(/<div class="stitle">(.*?)<\/div>/);
        const title = m ? m[1] : '';
        const body = (s.h || '').replace(/<div class="stitle">.*?<\/div>/, '');
        toc.push([`sl-${i + 1}`, 3, `${i + 1}. ${title.replace(/<[^>]+>/g, '') || t('slide') + ' ' + (i + 1)}`]);
        return `<section class="slide-block" id="sl-${i + 1}"><h3><small>${esc(t('slide'))} ${i + 1}</small> ${title}</h3>${body}${s.n ? `<div class="slide-notes"><b>${esc(t('notes'))}</b>${s.n}</div>` : ''}</section>`;
      }).join('');
      return { html, toc };
    }

    function renderText() {
      const src = isSlides ? slidesAsText() : { html: data.html || '', toc: data.toc || [] };
      const toc = src.toc;
      const hasToc = toc.length > 2;
      const tocHtml = toc.map(x => `<button type="button" class="l${x[1]}" data-target="${x[0]}">${esc(x[2])}</button>`).join('');
      const imgNote = d.kind === 'pdf' && d.mode === 'pages';
      content.innerHTML = `
        <div class="vgrid${hasToc ? '' : ' vgrid--full'}">
          <div>
            ${hasToc ? `<details class="toc-mobile panel"><summary>${icon('i-list')} ${esc(t('toc'))}</summary><nav class="toc" style="margin-top:.6rem">${tocHtml}</nav></details>` : ''}
            ${imgNote ? `<p class="notice">${icon('i-info')}<span>${esc(t('imagesNote'))}</span></p>` : ''}
            <article class="prose" id="prose" lang="ro">${src.html}</article>
          </div>
          ${hasToc ? `<aside class="vside"><div class="panel"><div class="panel__title">${icon('i-list')}${esc(t('toc'))}</div><nav class="toc">${tocHtml}</nav></div></aside>` : ''}
        </div>`;
      tools.innerHTML = `
        <div class="find">${icon('i-search')}<input type="search" id="fInput" placeholder="${esc(t('findPh'))}" aria-label="${esc(t('findPh'))}" value="${esc(q)}" autocomplete="off"></div>
        <span class="find__count" id="fCount"></span>
        <button type="button" class="btn btn--sm btn--icon" id="fPrev" aria-label="${esc(t('prev'))}">${icon('i-chev-l')}</button>
        <button type="button" class="btn btn--sm btn--icon" id="fNext" aria-label="${esc(t('next'))}">${icon('i-chev-r')}</button>`;
      const prose = document.getElementById('prose');
      prose.querySelectorAll('.page-sep').forEach(el => { el.textContent = `${t('page')} ${el.dataset.p}`; });
      prose.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (href.startsWith('#')) { a.removeAttribute('href'); a.setAttribute('role', 'text'); }
        else { a.target = '_blank'; a.rel = 'noopener'; }
      });
      prose.querySelectorAll('img').forEach(im => { im.loading = 'lazy'; im.decoding = 'async'; im.alt = im.alt || ''; });
      const scrollToEl = el => {
        const offset = document.getElementById('topbar').offsetHeight + document.getElementById('vbar').offsetHeight + 12;
        window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - offset, behavior: 'smooth' });
      };
      content.querySelectorAll('.toc [data-target]').forEach(b => b.addEventListener('click', () => {
        const el = document.getElementById(b.dataset.target);
        if (el) scrollToEl(el);
        const det = b.closest('details'); if (det) det.open = false;
      }));

      // find in text
      const fInput = document.getElementById('fInput');
      const fCount = document.getElementById('fCount');
      let marks = [], cur = -1;
      const setActive = (i, scroll, instant) => {
        if (!marks.length) return;
        if (cur >= 0 && marks[cur]) marks[cur].classList.remove('is-active');
        cur = (i + marks.length) % marks.length;
        marks[cur].classList.add('is-active');
        fCount.textContent = `${cur + 1}/${marks.length}`;
        if (scroll) marks[cur].scrollIntoView({ block: 'center', behavior: instant ? 'auto' : 'smooth' });
      };
      const runFind = (val, scroll) => {
        marks = highlightIn(prose, val);
        cur = -1;
        fCount.textContent = val.trim().length >= 2 ? (marks.length ? `0/${marks.length}` : '0') : '';
        if (marks.length && scroll) setActive(0, true);
      };
      let ft = 0;
      fInput.addEventListener('input', () => { clearTimeout(ft); ft = setTimeout(() => runFind(fInput.value, true), 250); });
      fInput.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); setActive(cur + (e.shiftKey ? -1 : 1), true); } });
      document.getElementById('fPrev').onclick = () => setActive(cur - 1, true);
      document.getElementById('fNext').onclick = () => setActive(cur + 1, true);

      // active TOC entry + reading progress + position memory
      const bar = document.createElement('div');
      bar.className = 'reading-progress';
      document.body.appendChild(bar);
      const heads = toc.map(x => document.getElementById(x[0])).filter(Boolean);
      const seps = [...prose.querySelectorAll('.page-sep')];
      const tocBtns = [...content.querySelectorAll('.vside .toc [data-target]')];
      let ticking = false;
      let lastActive = null;
      const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          ticking = false;
          const r = prose.getBoundingClientRect();
          const total = r.height - window.innerHeight * 0.6;
          bar.style.width = clamp((-r.top + 120) / Math.max(1, total) * 100, 0, 100) + '%';
          const line = 140;
          let active = null;
          for (const h of heads) { if (h.getBoundingClientRect().top < line) active = h; else break; }
          const activeId = active ? active.id : '';
          if (activeId !== lastActive) {
            lastActive = activeId;
            tocBtns.forEach(b => b.classList.toggle('is-active', b.dataset.target === activeId));
            const btn = tocBtns.find(b => b.dataset.target === activeId);
            const side = btn && btn.closest('.vside');
            if (side) side.scrollTop = Math.max(0, btn.offsetTop - side.clientHeight / 2);
          }
          let pg = 1;
          for (const s of seps) { if (s.getBoundingClientRect().top < line) pg = +s.dataset.p; else break; }
          if (isSlides) { for (const h of heads) { if (h.getBoundingClientRect().top < line) pg = +h.id.slice(3); else break; } }
          page = pg;
          remember({ y: Math.round(window.scrollY) });
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });

      const anchorFor = n => { // the marker of page n, or the closest one before it
        for (let k = n; k >= 1; k--) { const el = document.getElementById((isSlides ? 'sl-' : 'pg-') + k); if (el) return el; }
        return null;
      };
      requestAnimationFrame(() => {
        if (q) {
          fInput.value = q;
          marks = highlightIn(prose, q);
          fCount.textContent = marks.length ? `0/${marks.length}` : '0';
          if (marks.length) {
            // words searched separately: start from the rarest one (e.g. "roșu" rather than "cod")
            const counts = {};
            marks.forEach(m => { const k = foldKeep(m.textContent); counts[k] = (counts[k] || 0) + 1; });
            const rare = Object.keys(counts).sort((a, b) => counts[a] - counts[b])[0];
            const ok = m => Object.keys(counts).length < 2 || foldKeep(m.textContent) === rare;
            const anchor = explicitPage ? anchorFor(page) : null;
            const after = m => !anchor || (anchor.compareDocumentPosition(m) & Node.DOCUMENT_POSITION_FOLLOWING);
            let start = marks.findIndex(m => after(m) && ok(m));
            if (start < 0) start = marks.findIndex(after);
            setActive(Math.max(0, start), true, true);
          }
        } else if (restoreY != null) {
          window.scrollTo(0, restoreY);
        } else if (page > 1) {
          const anchor = anchorFor(page);
          if (anchor) scrollToEl(anchor);
        }
        restoreY = null;
        onScroll();
      });
      return () => { window.removeEventListener('scroll', onScroll); bar.remove(); };
    }

    function render() {
      if (modeCleanup) { modeCleanup(); modeCleanup = null; }
      document.querySelectorAll('#vbar [data-mode]').forEach(b => b.setAttribute('aria-selected', String(b.dataset.mode === mode)));
      const info = document.getElementById('vinfo');
      content.before(info);  // summary above the content…
      modeCleanup = mode === 'slides' ? renderSlides() : mode === 'pages' ? renderPages() : renderText();
      if (mode === 'slides') document.getElementById('thumbs').after(info);  // …but below the slide in presentations
    }
    document.querySelectorAll('#vbar [data-mode]').forEach(b => b.addEventListener('click', () => {
      if (b.dataset.mode === mode) return;
      mode = b.dataset.mode;
      remember();
      const top = document.getElementById('vbar').offsetTop;
      if (window.scrollY > top) window.scrollTo(0, top);
      render();
    }));

    let alive = true;
    const load = () => getDoc(id).then(res => {
      if (!alive) return;
      data = res;
      render();
    }).catch(() => {
      if (!alive) return;
      content.innerHTML = `<div class="empty">${icon('i-info')}<p>${esc(t('loadError'))}</p><button type="button" class="btn" id="retry">${esc(t('retry'))}</button></div>`;
      document.getElementById('retry').onclick = () => { content.innerHTML = `<div class="loading"><span class="spinner"></span>${esc(t('loading'))}</div>`; load(); };
    });
    load();
    return () => { alive = false; if (modeCleanup) modeCleanup(); };
  }

  /** highlight the query inside `root` (diacritics-insensitive); returns the <mark> elements */
  function highlightIn(root, query) {
    root.querySelectorAll('mark.fm').forEach(m => m.replaceWith(document.createTextNode(m.textContent)));
    root.normalize();
    const fq = foldKeep(query.trim()).replace(/\s+/g, ' ');
    if (fq.length < 2) return [];
    const terms = splitTerms(fq);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => (n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT) });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // phrase first; if the phrase is not found inside a single text node, highlight the single words
    const folded = nodes.map(n => foldKeep(n.nodeValue));
    const usePhrase = folded.some(f => f.includes(fq));
    const marks = [];
    for (let k = 0; k < nodes.length; k++) {
      const node = nodes[k];
      const text = node.nodeValue;
      const ranges = matchRanges(folded[k], usePhrase ? fq : '', usePhrase ? [] : terms);
      if (!ranges.length) continue;
      const frag = document.createDocumentFragment();
      let last = 0;
      for (const [a, b] of ranges) {
        if (a > last) frag.appendChild(document.createTextNode(text.slice(last, a)));
        const m = document.createElement('mark');
        m.className = 'fm';
        m.textContent = text.slice(a, b);
        frag.appendChild(m);
        marks.push(m);
        last = b;
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    }
    return marks;
  }

  // ------------------------------------------------------------------ search
  function goSearch(qs) {
    const q = (qs || '').trim();
    location.hash = '#/cautare' + (q ? '?q=' + encodeURIComponent(q) : '');
  }

  function searchAll(idx, query, filter) {
    const fq = foldFast(query.trim());
    const terms = splitTerms(fq);
    if (!terms.length) return null;
    const exact = fq.split(/[\s,.;:!?()"„”“«»'’/\\-]+/).filter(w => w.length >= 3);  // unstemmed words rank higher
    const docsHit = new Map();
    const entry = id => { let e = docsHit.get(id); if (!e) { e = { id, score: 0, meta: false, hits: [] }; docsHit.set(id, e); } return e; };
    const pass = id => !filter || (filter === 'general' ? !DOCS[id].course : DOCS[id].course === filter);
    Object.keys(DOCS).forEach(id => {
      if (!pass(id)) return;
      const m = docMeta(id);
      if (terms.every(w => m.all.includes(w))) {
        const e = entry(id);
        e.meta = true;
        e.score += 40 + (terms.every(w => m.title.includes(w)) ? 60 : 0) + (m.title.includes(fq) ? 40 : 0);
      }
    });
    const items = idx.items;
    for (let i = 0; i < items.length; i++) {
      const id = idx.docs[items[i][0]];
      if (!pass(id)) continue;
      const ft = idx.folded[i];
      let score = 0, ok = true;
      for (const w of terms) {
        let p = ft.indexOf(w);
        if (p < 0) { ok = false; break; }
        let c = 0;
        while (p >= 0 && c < 6) { c++; p = ft.indexOf(w, p + w.length); }
        score += c;
      }
      if (!ok) continue;
      if (terms.length > 1 && ft.includes(fq)) score += 10;
      for (const w of exact) if (ft.includes(w)) score += 3;
      const e = entry(id);
      e.hits.push({ i, p: items[i][1], s: score });
      e.score += score;
    }
    const list = [...docsHit.values()];
    list.forEach(e => { e.hits.sort((a, b) => b.s - a.s || a.p - b.p); e.score += e.hits.slice(0, 3).reduce((a, h) => a + h.s, 0); });
    list.sort((a, b) => b.score - a.score);
    return { list, fq, terms, total: list.reduce((a, e) => a + Math.max(1, e.hits.length), 0) };
  }

  function snippet(text, fq, terms) {
    const ft = foldKeep(text);
    let pos = terms.length > 1 ? ft.indexOf(fq) : -1;
    if (pos < 0) pos = Math.max(0, ft.indexOf(terms[0]));
    let a = Math.max(0, pos - 70), b = Math.min(text.length, pos + 170);
    if (a > 0) { const sp = text.indexOf(' ', a); if (sp > 0 && sp < pos) a = sp + 1; }
    if (b < text.length) { const sp = text.lastIndexOf(' ', b); if (sp > pos + 20) b = sp; }
    const sub = text.slice(a, b);
    const ranges = matchRanges(ft.slice(a, b), terms.length > 1 ? fq : '', terms);
    let out = '', last = 0;
    for (const [x, y] of ranges) { out += esc(sub.slice(last, x)) + '<mark>' + esc(sub.slice(x, y)) + '</mark>'; last = y; }
    out += esc(sub.slice(last));
    return (a > 0 ? '… ' : '') + out + (b < text.length ? ' …' : '');
  }

  function viewSearch(q0, filter0) {
    setTitle(t('searchTitle'));
    let filter = filter0;
    main.innerHTML = `
      <section class="phead search-head">
        <div class="wrap">
          ${crumbs([{ href: '#/', label: t('home') }, { label: t('searchTitle') }])}
          <h1 class="phead__title">${esc(t('searchTitle'))}</h1>
          <p class="phead__desc">${esc(t('searchLead'))}</p>
          <form class="search-box" id="sForm" role="search">${icon('i-search')}<input type="search" id="sInput" name="q" value="${esc(q0)}" placeholder="${esc(t('searchPh'))}" aria-label="${esc(t('search'))}" autocomplete="off" enterkeyhint="search"></form>
        </div>
      </section>
      <div class="wrap">
        <div class="filters" id="sFilters">
          <button type="button" data-f="" aria-pressed="${!filter}">${esc(t('allCourses'))}</button>
          ${C.courses.map(c => `<button type="button" data-f="${c.id}" style="--accent:${c.color}" aria-pressed="${filter === c.id}"><span class="dot"></span>${esc(courseTitle(c))}</button>`).join('')}
          <button type="button" data-f="general" aria-pressed="${filter === 'general'}">${esc(t('general'))}</button>
        </div>
        <div class="results-info" id="sInfo" aria-live="polite"></div>
        <div class="results" id="sResults"></div>
      </div>`;
    const input = document.getElementById('sInput');
    const info = document.getElementById('sInfo');
    const out = document.getElementById('sResults');
    let idx = null;
    let timer = 0;

    function run() {
      const q = input.value.trim();
      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (filter) params.set('c', filter);
      history.replaceState(null, '', '#/cautare' + (params.toString() ? '?' + params : ''));
      const top = document.getElementById('topSearchInput');
      if (top && document.activeElement !== top) top.value = q;
      if (foldFast(q).replace(/\s/g, '').length < 2) { info.textContent = t('searchStart'); out.innerHTML = ''; return; }
      if (!idx) { info.innerHTML = `<span class="loading" style="justify-content:flex-start;padding:0"><span class="spinner"></span>${esc(t('loadingIndex'))}</span>`; return; }
      const res = searchAll(idx, q, filter);
      if (!res || !res.list.length) {
        info.textContent = '';
        out.innerHTML = `<div class="empty">${icon('i-search')}<p><b>${esc(t('noResults', { q }))}</b></p><p>${esc(/[а-яё]/i.test(q) ? t('ruHint') : t('noResultsHint'))}</p></div>`;
        return;
      }
      info.textContent = t('results', { n: res.total, d: res.list.length });
      out.innerHTML = res.list.slice(0, 60).map((e, k) => {
        const d = DOCS[e.id];
        const c = courseById[d.course];
        const hits = e.hits.slice(0, 3).map(h => `<a class="hit" href="${docUrl(e.id, { p: h.p, q })}"><span class="hit__page">${esc(d.kind === 'slides' ? t('slide') : t('page'))} ${h.p}</span><span>${snippet(idx.items[h.i][2], res.fq, res.terms)}</span></a>`).join('');
        return `<article class="result" style="--accent:${accentOf(d)};animation-delay:${Math.min(k, 10) * 30}ms">
          <div class="result__head"><span class="result__course">${esc(c ? courseTitle(c) : t('general'))}</span><span class="chip">${esc(typeLabel(d))}</span>${e.meta ? `<span class="chip chip--gold">${icon('i-star')}${esc(t('titleMatch'))}</span>` : ''}</div>
          <a class="result__title" href="${docUrl(e.id, e.hits.length ? { p: e.hits[0].p, q } : null)}">${esc(L(d.title))}</a>
          ${e.meta && !e.hits.length ? `<p class="item__desc" style="margin-top:.35rem">${esc(L(d.summary))}</p>` : ''}
          ${hits ? `<div class="result__hits">${hits}</div>` : ''}
          ${e.hits.length > 3 ? `<div class="result__more">${esc(t('moreHits', { n: e.hits.length - 3 }))}</div>` : ''}
        </article>`;
      }).join('');
    }
    input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 180); });
    document.getElementById('sForm').addEventListener('submit', e => { e.preventDefault(); clearTimeout(timer); run(); input.blur(); });
    document.getElementById('sFilters').addEventListener('click', e => {
      const b = e.target.closest('button[data-f]');
      if (!b) return;
      filter = b.dataset.f;
      document.querySelectorAll('#sFilters button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      run();
    });
    run();
    getSearchIndex().then(ix => { idx = ix; run(); }).catch(() => { info.textContent = t('loadError'); });
    if (!q0 && window.matchMedia('(min-width: 821px)').matches) input.focus();
  }

  // ------------------------------------------------------------------ about / 404
  const ABOUT = {
    ro: `<h2>Ce este această bibliotecă</h2>
      <p>Un site creat pentru cursanții <b>Grupei 131</b> („Inițiere în Ofițer”) — cursul de formare inițială a ofițerilor. Aici sunt adunate toate materialele de studiu ale disciplinelor: prezentări, suporturi de curs, regulamente și acte normative, care se citesc direct pe site, fără descărcarea fișierelor.</p>
      <h2>Cum este organizat</h2>
      <ul><li><b>Disciplinele</b> — Instrucția de front, AROP, Instrucția tragerii, Prim ajutor și TIP. Fiecare disciplină are temele și materialele sale, grupate pe secțiuni.</li>
      <li><b>Pe scurt</b> — fiecare material are un rezumat și ideile principale, în română și în rusă.</li>
      <li><b>Trei moduri de citire</b>: <i>Slide-uri</i> (prezentări, cu glisare pe telefon și ecran complet), <i>Original</i> (paginile documentului exact ca în original) și <i>Text</i> (se adaptează ecranului telefonului și se mărește cu A− / A+).</li>
      <li><b>Căutarea</b> găsește orice cuvânt în tot conținutul și deschide direct slide-ul sau pagina potrivită. Diacriticele nu contează.</li></ul>
      <h2>Accesibilitate</h2>
      <p>Butoanele <b>A− / A / A+</b> schimbă mărimea textului pe tot site-ul, butonul lunii comută tema întunecată, iar <b>RO / RU</b> schimbă limba interfeței. Pe telefon, aceste setări se găsesc în meniu (☰).</p>
      <h2>Confidențialitate</h2>
      <p>Site-ul nu folosește cookie-uri, conturi sau statistici. Preferințele, progresul („Studiat”) și istoricul se păstrează doar în browserul dispozitivului vostru. Numerele de telefon personale din materiale au fost ascunse.</p>
      <h2>Notă</h2>
      <p>Site neoficial, realizat de cursanți în scop exclusiv educațional. Materialele aparțin autorilor și instituțiilor emitente; pentru documentele oficiale consultați sursele oficiale.</p>`,
    ru: `<h2>Что это за библиотека</h2>
      <p>Сайт для курсантов <b>Группы 131</b> («Initiere în Ofițer») — курс первоначальной подготовки офицеров. Здесь собраны все учебные материалы дисциплин: презентации, конспекты, уставы и нормативные акты. Всё читается прямо на сайте, без скачивания файлов.</p>
      <h2>Как устроено</h2>
      <ul><li><b>Дисциплины</b> — Строевая подготовка, AROP, Огневая подготовка, Первая помощь и TIP. У каждой дисциплины свои темы и материалы, сгруппированные по разделам.</li>
      <li><b>Кратко</b> — у каждого материала есть краткое изложение и главные мысли на румынском и русском.</li>
      <li><b>Три режима чтения</b>: <i>Слайды</i> (презентации, листание свайпом и полноэкранный режим), <i>Оригинал</i> (страницы документа как в оригинале) и <i>Текст</i> (подстраивается под экран телефона, увеличивается кнопками A− / A+).</li>
      <li><b>Поиск</b> находит любое слово во всём содержании и открывает нужный слайд или страницу. Диакритика не важна.</li></ul>
      <h2>Доступность</h2>
      <p>Кнопки <b>A− / A / A+</b> меняют размер текста на всём сайте, кнопка с луной включает тёмную тему, а <b>RO / RU</b> переключает язык интерфейса. На телефоне эти настройки находятся в меню (☰).</p>
      <h2>Конфиденциальность</h2>
      <p>Сайт не использует cookie, аккаунты или статистику. Настройки, прогресс («Изучено») и история хранятся только в браузере вашего устройства. Личные номера телефонов в материалах скрыты.</p>
      <h2>Примечание</h2>
      <p>Неофициальный сайт, созданный курсантами исключительно в учебных целях. Материалы принадлежат их авторам и издавшим их учреждениям; официальные документы сверяйте с официальными источниками.</p>`
  };

  function viewAbout() {
    setTitle(t('aboutTitle'));
    const s = C.stats;
    main.innerHTML = `
      <section class="phead">
        <div class="wrap">
          ${crumbs([{ href: '#/', label: t('home') }, { label: t('aboutTitle') }])}
          <h1 class="phead__title">${esc(t('aboutTitle'))}</h1>
          <p class="phead__desc">${esc(t('aboutLead'))}</p>
        </div>
      </section>
      <div class="wrap about">
        <article class="prose">${ABOUT[lang]}</article>
        <aside class="course-aside">
          <div class="panel">
            <dl class="kv">
              <dt>${esc(t('statCourses'))}</dt><dd>${s.courses}</dd>
              <dt>${esc(t('statDocs'))}</dt><dd>${s.docs}</dd>
              <dt>${esc(t('statSlides'))}</dt><dd>${s.slides}</dd>
              <dt>${esc(t('statPages'))}</dt><dd>${s.pages}</dd>
            </dl>
            <p style="color:var(--muted);font-size:.85rem;margin-top:.8rem">${esc(t('builtOn', { d: C.built }))}</p>
          </div>
          ${C.general.map(id => `<a class="about-card" href="${docUrl(id)}" style="grid-template-columns:auto 1fr"><span class="about-card__ico">${icon('c-info')}</span><div><h3 style="font-size:1.05rem">${esc(t('aboutCourseTitle'))}</h3><p style="font-size:.88rem">${esc(t('aboutCourseText'))}</p></div></a>`).join('')}
          <div class="panel"><h2 class="panel__title">${icon('i-grid')}${esc(t('coursesTitle'))}</h2>
            <nav class="toc">${C.courses.map(x => `<a href="#/curs/${x.id}">${esc(courseFull(x))}</a>`).join('')}</nav></div>
        </aside>
      </div>`;
  }

  function viewNotFound() {
    setTitle(t('notFound'));
    main.innerHTML = `<div class="wrap"><div class="empty" style="padding:5rem 1rem">${icon('i-info')}<h1 class="section__title" style="justify-content:center">${esc(t('notFound'))}</h1><p>${esc(t('notFoundText'))}</p><p><a class="btn btn--primary" href="#/">${icon('i-home')}${esc(t('goHome'))}</a></p></div></div>`;
  }

  // ------------------------------------------------------------------ router
  let viewCleanup = null;
  let lastPath = null;
  function route(opts) {
    const raw = (location.hash || '#/').slice(1) || '/';
    const [path, qs] = raw.split('?');
    const parts = path.split('/').filter(Boolean);
    const params = new URLSearchParams(qs || '');
    if (viewCleanup) { try { viewCleanup(); } catch (e) { /* ignore */ } viewCleanup = null; }
    closeDrawer();
    const [a, b] = parts;
    let cleanupFn;
    if (!a) viewHome();
    else if (a === 'curs' && courseById[b]) viewCourse(courseById[b]);
    else if (a === 'doc' && DOCS[b]) cleanupFn = viewDoc(b, params);
    else if (a === 'cautare') viewSearch(params.get('q') || '', params.get('c') || '');
    else if (a === 'despre') viewAbout();
    else viewNotFound();
    viewCleanup = cleanupFn || null;
    markActiveNav();
    const top = document.getElementById('topSearchInput');
    if (top && a !== 'cautare') top.value = '';
    if (!(opts && opts.keepScroll) && path !== lastPath) window.scrollTo(0, 0);
    lastPath = path;
  }

  // ------------------------------------------------------------------ global events
  const fsBtn = document.getElementById('fsBtn');
  const fsPop = document.getElementById('fsPop');
  const closeFsPop = () => { if (!fsPop.hidden) { fsPop.hidden = true; fsBtn.setAttribute('aria-expanded', 'false'); } };
  fsBtn.addEventListener('click', e => {
    e.stopPropagation();
    fsPop.hidden = !fsPop.hidden;
    fsBtn.setAttribute('aria-expanded', String(!fsPop.hidden));
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.fs-wrap')) closeFsPop();
    const fs = e.target.closest('[data-fs]');
    if (fs) { setScale(+fs.dataset.fs); return; }
    const lg = e.target.closest('[data-lang]');
    if (lg) { setLang(lg.dataset.lang); return; }
    const th = e.target.closest('[data-theme-set]');
    if (th) { setTheme(th.dataset.themeSet); return; }
    const st = e.target.closest('[data-study]');
    if (st) { e.preventDefault(); toggleStudied(st.dataset.study); return; }
    const item = e.target.closest('.item');
    if (item && !e.target.closest('a, button')) { const a = item.querySelector('.item__link'); if (a) a.click(); }
    const nav = e.target.closest('#drawer a');
    if (nav) closeDrawer();
  });
  document.getElementById('themeBtn').addEventListener('click', () => {
    setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });
  if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (!prefs.theme) applyTheme(); });
  menuBtn.addEventListener('click', openDrawer);
  document.getElementById('drawerClose').addEventListener('click', () => closeDrawer(true));
  backdrop.addEventListener('click', () => closeDrawer(true));
  document.getElementById('searchBtn').addEventListener('click', () => goSearch(''));
  const topForm = document.getElementById('topSearch');
  topForm.addEventListener('submit', e => { e.preventDefault(); goSearch(document.getElementById('topSearchInput').value); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !fsPop.hidden) { closeFsPop(); fsBtn.focus(); return; }
    if (e.key === 'Escape' && !drawer.hidden) { closeDrawer(true); return; }
    if (e.key === '/' && !e.target.closest('input, textarea, select, [contenteditable]')) {
      const box = document.getElementById('sInput') || (getComputedStyle(topForm).display !== 'none' ? document.getElementById('topSearchInput') : null);
      if (box) { e.preventDefault(); box.focus(); box.select(); } else { e.preventDefault(); goSearch(''); }
    }
  });
  const toTop = document.getElementById('toTop');
  let tt = false;
  window.addEventListener('scroll', () => {
    if (tt) return;
    tt = true;
    requestAnimationFrame(() => { tt = false; toTop.hidden = window.scrollY < 700; });
  }, { passive: true });
  toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('hashchange', () => route());

  // ------------------------------------------------------------------ start
  applyTheme();
  applyScale();
  applyStatic();
  route();
})();
