# -*- coding: utf-8 -*-
"""Study guide for "Instrucția tragerii" (our own material, not an official document).

The guide is written as HTML (p*.html + style.css in this folder). This script
    1. prints it to PDF with headless Microsoft Edge (two passes, to fill in the page numbers
       of the table of contents), adds bookmarks and metadata;
    2. writes text.html - a reflowable version for the site's "Text" view
       (tools/build.py uses it through DOCS['trg-ghid-pregatire']['text_html']).

    python tools/ghid-tragere/make.py                      # PDF into "instrucția tragerii/" + text.html
    python tools/ghid-tragere/make.py --text-only          # only text.html (no Edge needed)
    python tools/ghid-tragere/make.py --pdf X.pdf --preview DIR

Afterwards rebuild the site: python tools/build.py
"""
import argparse
import html as htmlmod
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.join(ROOT, '_build', 'ghid-tragere')
PDF_NAME = 'Instructia_Tragerii_Ghid_de_pregatire.pdf'
TEXT_OUT = os.path.join(HERE, 'text.html')
TITLE = 'Instrucția tragerii – Ghid de pregătire'
PARTS = ['p0_cover.html', 'p1a_siguranta.html', 'p1b_siguranta.html', 'p2_makarov.html',
         'p3a_legea.html', 'p3b_legea.html', 'p4_recap.html']
EDGE_PATHS = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


def course_dir():
    """The course source folder ("instrucția tragerii"), whatever the diacritics normalization."""
    def fold(s):
        s = unicodedata.normalize('NFD', s)
        return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    for d in os.listdir(ROOT):
        if fold(d) == 'instructia tragerii' and os.path.isdir(os.path.join(ROOT, d)):
            return os.path.join(ROOT, d)
    sys.exit('Course folder "instrucția tragerii" not found')


def assemble(pages=None):
    """Whole guide as one HTML page; {{pg:id}} = page number of section id (00 on the first pass)."""
    body = '\n'.join(read(p) for p in PARTS).replace('{{svg}}', read('p2_svg.html'))
    body = re.sub(r'\{\{pg:([\w-]+)\}\}', lambda m: str((pages or {}).get(m.group(1), '00')), body)
    left = re.findall(r'\{\{[^}]*\}\}', body)
    assert not left, left
    return (f'<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>{TITLE}</title>'
            f'<style>{read("style.css")}</style></head><body>{body}</body></html>')


# ----------------------------------------------------------------------------- PDF
def edge_exe():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    p = shutil.which('msedge')
    if not p:
        sys.exit('Microsoft Edge not found (needed to print the PDF); use --text-only')
    return p


def render(html_text, pdf_path):
    src = os.path.join(WORK, 'guide.html')
    with open(src, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html_text)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    cmd = [edge_exe(), '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
           '--user-data-dir=' + os.path.join(WORK, 'edge-profile'), '--no-pdf-header-footer',
           '--print-to-pdf-no-header', '--print-to-pdf=' + pdf_path, 'file:///' + src.replace('\\', '/')]
    subprocess.run(cmd, check=True, timeout=180, capture_output=True)
    assert os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 10_000, 'PDF not produced'


def anchor_pages(pdf_path, ids):
    """Section id -> 1-based page number (from the named destinations Edge writes for the TOC links)."""
    doc = fitz.open(pdf_path)
    names = doc.resolve_names()
    doc.close()
    return {i: names[i]['page'] + 1 for i in ids if i in names and names[i].get('page', -1) >= 0}


def build_pdf(out_pdf, preview_dir=None):
    cover = read('p0_cover.html')
    toc = re.findall(r'<a class="toc-row" href="#([\w-]+)"><span class="t">(.*?)</span>', cover)
    ids = [i for i, _ in toc]
    draft = os.path.join(WORK, 'draft.pdf')
    render(assemble(), draft)
    pages = anchor_pages(draft, ids)
    missing = [i for i in ids if i not in pages]
    assert not missing, f'sections without a page: {missing}'
    final_raw = os.path.join(WORK, 'final_raw.pdf')
    render(assemble(pages), final_raw)
    pages2 = anchor_pages(final_raw, ids)
    assert pages2 == pages, ('pagination shifted between the two passes', pages, pages2)

    # bookmarks: the part titles of the TOC, sections under them
    parts = re.findall(r'<div class="toc-part (p\d)">\s*<h5>(.*?)</h5>(.*?)</div>', cover, re.S)
    outline = [[1, 'Copertă, cuprins, cele 10 lucruri esențiale', 1]]
    for _, ptitle, block in parts:
        rows = re.findall(r'href="#([\w-]+)"><span class="t">(.*?)</span>', block)
        outline.append([1, htmlmod.unescape(ptitle), pages[rows[0][0]]])
        outline += [[2, htmlmod.unescape(t), pages[i]] for i, t in rows]
    doc = fitz.open(final_raw)
    w, h = doc[0].rect.width, doc[0].rect.height
    assert abs(w - 595) < 3 and abs(h - 842) < 3, f'unexpected page size {w}x{h} (A4 expected)'
    doc.set_toc(outline)
    doc.set_metadata({'title': TITLE, 'subject': 'Măsurile de siguranță, pistolul Makarov (PM), Legea nr. 218/2012',
                      'keywords': 'instrucția tragerii, Makarov, PM, măsuri de siguranță, Legea 218',
                      'creator': 'HTML + Microsoft Edge', 'producer': 'PyMuPDF', 'author': ''})
    tmp = out_pdf + '.tmp'
    doc.save(tmp, garbage=3, deflate=True)
    n = doc.page_count
    doc.close()
    os.replace(tmp, out_pdf)
    if preview_dir:
        os.makedirs(preview_dir, exist_ok=True)
        doc = fitz.open(out_pdf)
        for p in doc:
            p.get_pixmap(dpi=70).save(os.path.join(preview_dir, f'page{p.number + 1:02d}.png'))
        doc.close()
    print(f'PDF: {out_pdf} — {n} pages, {os.path.getsize(out_pdf) // 1024} KB')
    print('sections:', pages)


# ----------------------------------------------------------------------------- text version
VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'col', 'source', 'wbr'}
BLOCK = {'p', 'div', 'ul', 'ol', 'table', 'h2', 'h3', 'h4', 'h5', 'figure', 'section'}
INLINE = {'b': 'strong', 'strong': 'strong', 'i': 'em', 'em': 'em', 'u': 'u', 'sup': 'sup', 'sub': 'sub'}
# sentences that only make sense on paper
TEXT_FIXES = [('Diferențele sunt marcate cu galben.', 'Diferențele sunt subliniate.'),
              ('verifică-te cu răspunsurile de pe pagina următoare', 'verifică-te cu răspunsurile de mai jos')]


class Node:
    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def has(self, c):
        return c in (self.attrs.get('class') or '').split()

    def find(self, pred):
        for c in self.children:
            if isinstance(c, Node):
                if pred(c):
                    return c
                r = c.find(pred)
                if r is not None:
                    return r
        return None

    def text(self):
        return ''.join(c if isinstance(c, str) else c.text() for c in self.children)


class Tree(HTMLParser):
    def __init__(self, html_text):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', {})
        self.stack = [self.root]
        self.feed(html_text)
        self.close()

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def inline(n, skip=None):
    """Inline HTML of a node's children (b/i -> strong/em, highlighted differences -> u)."""
    out = []
    for c in n.children:
        if isinstance(c, str):
            out.append(esc(c))
        elif c is skip or c.tag in ('style', 'script'):
            continue
        elif c.tag == 'br':
            out.append('<br/>')
        elif c.tag in INLINE:
            out.append(f'<{INLINE[c.tag]}>{inline(c)}</{INLINE[c.tag]}>')
        elif c.tag == 'span' and c.has('diff'):
            out.append(f'<u>{inline(c)}</u>')
        elif c.tag == 'span' and c.has('code'):
            out.append(f'<strong>{inline(c)}</strong>')
        else:
            out.append(inline(c))
    return norm(''.join(out))


def strong(s):
    return s if s.startswith('<strong>') and s.endswith('</strong>') else f'<strong>{s}</strong>'


def li_html(li):
    """List item: inline content, nested lists/paragraphs as blocks."""
    parts, buf = [], Node('span', {})
    for c in li.children:
        if isinstance(c, Node) and c.tag in BLOCK:
            if inline(buf):
                parts.append(inline(buf))
            buf = Node('span', {})
            parts.extend(block(c))
        else:
            buf.children.append(c)
    if inline(buf):
        parts.append(inline(buf))
    return ''.join(parts)


def table_html(t):
    def rows(container):
        out = []
        for tr in container.children:
            if not (isinstance(tr, Node) and tr.tag == 'tr'):
                continue
            cells = []
            for td in tr.children:
                if not (isinstance(td, Node) and td.tag in ('td', 'th')):
                    continue
                span = ''.join(f' {a}="{esc(td.attrs[a])}"' for a in ('colspan', 'rowspan') if td.attrs.get(a))
                content = inline(td)
                if td.has('k') and content:
                    content = strong(content)
                cells.append(f'<{td.tag}{span}>{content}</{td.tag}>')
            out.append('<tr>' + ''.join(cells) + '</tr>')
        return ''.join(out)
    out = []
    for c in t.children:
        if isinstance(c, Node) and c.tag in ('thead', 'tbody'):
            out.append(f'<{c.tag}>{rows(c)}</{c.tag}>')
    if not out:
        out.append('<tbody>' + rows(t) + '</tbody>')
    return '<table>' + ''.join(out) + '</table>'


def blocks(n):
    out = []
    for c in n.children:
        if isinstance(c, str):
            if c.strip():
                out.append(f'<p>{esc(norm(c))}</p>')
        else:
            out.extend(block(c))
    return out


def block(c):
    tag = c.tag
    if tag in ('style', 'script', 'a') or c.has('toc') or c.has('cover-band') or c.has('farrow'):
        return []
    if tag == 'section' and c.has('cover'):
        out = []
        for ch in c.children:
            if isinstance(ch, Node) and ch.tag == 'h3':
                out.append(f'<h2>{inline(ch)}</h2>')
            elif isinstance(ch, Node) and ch.tag == 'p':
                out.append(f'<p><em>{inline(ch)}</em></p>')
            elif isinstance(ch, Node):
                out.extend(block(ch))
        return out
    if c.has('part-head'):
        num = c.find(lambda x: x.has('part-num'))
        title = c.find(lambda x: x.has('part-title'))
        sub = c.find(lambda x: x.has('part-sub'))
        out = [f'<h2>{norm(num.text())}. {inline(title)}</h2>']
        if sub is not None:
            out.append(f'<p><em>{inline(sub)}</em></p>')
        return out
    if c.has('qh'):
        qn = c.find(lambda x: x.has('qn'))
        return [f'<h4>{norm(qn.text())}. {inline(c, skip=qn)}</h4>' if qn is not None else f'<h4>{inline(c)}</h4>']
    if c.has('box'):
        inner = []
        for ch in c.children:
            if isinstance(ch, Node) and ch.has('bt'):
                inner.append(f'<p>{strong(inline(ch))}</p>')
            elif isinstance(ch, Node):
                inner.extend(block(ch))
            elif ch.strip():
                inner.append(f'<p>{esc(norm(ch))}</p>')
        return ['<blockquote>' + ''.join(inner) + '</blockquote>']
    if c.has('card'):
        out = []
        for ch in c.children:
            if isinstance(ch, Node) and ch.tag == 'h5':
                out.append(f'<h4>{inline(ch)}</h4>')
            elif isinstance(ch, Node):
                out.extend(block(ch))
        return out
    if c.has('somatie'):  # "Stai! …" -> "Stai că trag!" -> ... as a numbered list
        items = []
        for d in c.children:
            if isinstance(d, Node):
                big = d.find(lambda x: x.has('big'))
                items.append(f'<li><strong>{inline(big)}</strong> – {inline(d, skip=big)}</li>')
        return ['<ol>' + ''.join(items) + '</ol>']
    if c.has('flow'):  # algorithm: steps with the side notes under them
        items = []
        for d in c.children:
            if not isinstance(d, Node):
                continue
            if d.has('fstep'):
                t = d.find(lambda x: x.has('t'))
                items.append([f'<strong>{inline(t)}</strong> {inline(d, skip=t)}'])
            elif d.has('fside') and items:
                items[-1].append(f'<br/>→ {inline(d)}')
        return ['<ol>' + ''.join(f'<li>{"".join(x)}</li>' for x in items) + '</ol>']
    if c.has('mcq'):  # test question: options one per line
        qq = c.find(lambda x: x.has('qq'))
        opts = [inline(li) for li in c.find(lambda x: x.tag in ('ol', 'ul')).children if isinstance(li, Node)]
        return [f'<p><strong>{inline(qq)}</strong><br/>' + '<br/>'.join(opts) + '</p>']
    if c.has('ans'):  # answer key as a table
        rows = []
        for d in c.children:
            if not isinstance(d, Node):
                continue
            spans = [s for s in d.children if isinstance(s, Node)]
            m = re.match(r'(\d+)\s*[–-]\s*(\w)', norm(spans[0].text()))
            rows.append(f'<tr><td>{m.group(1)}</td><td><strong>{m.group(2)}</strong></td><td>{esc(norm(spans[1].text()))}</td></tr>')
        return ['<table><thead><tr><th>Întrebarea</th><th>Răspunsul</th><th>Explicația în ghid</th></tr></thead>'
                '<tbody>' + ''.join(rows) + '</tbody></table>']
    if tag == 'figure':  # the pistol schema: the SVG itself, then its legend and caption
        out = ['<figure>' + SVG_MARK + '</figure>']
        for d in c.children:
            if isinstance(d, Node) and d.tag != 'svg':
                for ch in d.children if d.tag == 'div' else [d]:
                    if isinstance(ch, Node) and ch.tag == 'figcaption':
                        out.append(f'<p><em>{inline(ch)}</em></p>')
                    elif isinstance(ch, Node):
                        out.extend(block(ch))
        return out
    if tag in ('section', 'div'):
        return blocks(c)
    if tag in ('h2', 'h3'):
        return [f'<{tag}>{inline(c)}</{tag}>']
    if tag in ('h4', 'h5'):
        return [f'<p>{strong(inline(c))}</p>']
    if tag == 'p':
        s = inline(c)
        return [f'<p>{s}</p>'] if s else []
    if tag in ('ul', 'ol'):
        items = [f'<li>{li_html(li)}</li>' for li in c.children if isinstance(li, Node) and li.tag == 'li']
        typ = ' type="a"' if c.has('alpha') else ''
        return [f'<{tag}{typ}>' + ''.join(items) + f'</{tag}>']
    if tag == 'table':
        return [table_html(c)]
    if tag == 'svg':
        return []
    s = inline(c)
    return [f'<p>{s}</p>'] if s else []


SVG_MARK = '<!--svg-->'


def build_text():
    html_text = '\n'.join(read(p) for p in PARTS).replace('{{svg}}', read('p2_svg.html'))
    html_text = re.sub(r'\{\{pg:[\w-]+\}\}', '', html_text)
    for a, b in TEXT_FIXES:
        assert a in html_text, f'text fix not applicable any more: {a!r}'
        html_text = html_text.replace(a, b)
    out = '\n'.join(blocks(Tree(html_text).root))
    # the schema: the original SVG markup (case-sensitive attributes such as viewBox), without
    # comments and the fixed print width; the site's CSS sizes it
    svg = re.search(r'<svg\b.*?</svg>', read('p2_svg.html'), re.S).group(0)
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'(<svg\b[^>]*?)\s+width="[^"]*"', r'\1', svg, count=1)
    svg = re.sub(r'>\s+<', '><', svg).strip()
    assert out.count(SVG_MARK) == 1
    out = out.replace(SVG_MARK, svg)
    ET.fromstring('<root>' + out + '</root>')  # tools/build.py parses it as XML
    with open(TEXT_OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out + '\n')
    heads = re.findall(r'<h([234])>(.*?)</h\1>', out)
    print(f'text: {TEXT_OUT} — {len(out) // 1024} KB, {len(heads)} headings')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--text-only', action='store_true', help='only write text.html')
    ap.add_argument('--pdf', help='where to write the PDF (default: the course folder)')
    ap.add_argument('--preview', help='also render PNG previews of the pages into this folder')
    args = ap.parse_args()
    build_text()
    if not args.text_only:
        os.makedirs(WORK, exist_ok=True)
        build_pdf(args.pdf or os.path.join(course_dir(), PDF_NAME), args.preview)


if __name__ == '__main__':
    main()
