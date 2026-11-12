# -*- coding: utf-8 -*-
"""Builds the static library website data from the original course materials.

    1. powershell -ExecutionPolicy Bypass -File tools\\convert_office.ps1   (Office -> PDF, needs MS Office)
    2. python tools\\build.py [--force] [--only id1,id2] [--jobs 6]

Produces:
    content/<doc-id>/p001.webp ...   page / slide images
    content/<doc-id>/t001.webp ...   thumbnails
    content/<doc-id>/doc.js          text, table of contents, slide notes, media
    data/catalog.js                  courses, sections, document metadata (RO/RU)
    data/search.js                   full-text search index
"""
import argparse
import asyncio
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

import fitz  # PyMuPDF
import mammoth
from PIL import Image, ImageFilter, ImageStat
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_data import COURSES, DOCS, GENERAL, SECTION_TITLES, SITE, TYPES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, '_build')
CONTENT = os.path.join(ROOT, 'content')
DATA = os.path.join(ROOT, 'data')
IMG_VERSION = 1  # bump to re-render every page image
TXT_VERSION = 3  # bump to regenerate the text / search data of every document (fast)

SLIDE_W, PAGE_W, THUMB_W = 1280, 1100, 320
Q_SLIDE, Q_PAGE, Q_SCAN, Q_THUMB = 80, 74, 64, 70

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# ----------------------------------------------------------------------------- helpers
def fold(s):
    """lowercase, without diacritics (ș/ş/ţ/ț unified) - for file matching."""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s.replace('\\', '/')).strip().lower()


def source_index():
    dirs = [l.strip() for l in open(os.path.join(ROOT, 'tools', 'source_dirs.txt'), encoding='utf-8') if l.strip()]
    idx = {}
    for d in dirs:
        for dp, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.startswith('~$'):
                    continue
                full = os.path.join(dp, f)
                idx[fold(os.path.relpath(full, ROOT))] = full
    return idx


def derived_paths(src):
    rel = os.path.relpath(src, ROOT)
    ext = os.path.splitext(src)[1].lower()
    pdf = src if ext == '.pdf' else os.path.join(BUILD, 'pdf', rel + '.pdf')
    ox = {'.ppt': os.path.join(BUILD, 'ox', rel + '.pptx'), '.doc': os.path.join(BUILD, 'ox', rel + '.docx'),
          '.pptx': src, '.docx': src}.get(ext)
    return pdf, ox


def clean_ws(s):
    s = s.replace(' ', ' ').replace('​', '').replace('­', '')
    return re.sub(r'\s+', ' ', s).strip()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def save_webp(img, path, quality):
    if img.mode not in ('RGB', 'L'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.convert('RGBA').split()[-1])
        img = bg
    img.save(path, 'WEBP', quality=quality, method=5)


def pix_to_image(pix):
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def encode_page(img, path, kind):
    """Write the smallest good-looking WebP: text pages compress best as quantized lossless grayscale,
    photos and slides as lossy colour."""
    cands = []
    small = img.resize((160, max(1, round(160 * img.height / img.width))))
    gray = kind != 'slides' and ImageStat.Stat(small.convert('HSV')).mean[1] < 6
    if gray:
        th = 205 if kind == 'scan' else 245  # whiten the paper background
        lum = img.convert('L').point(lambda v: 255 if v > th else int(v * 255 / th))
        cands.append((lum.point(lambda v: 255 if v == 255 else (v // 16) * 16 + 8), {'lossless': True, 'quality': 80, 'method': 6}))
        cands.append((lum, {'quality': 62 if kind == 'scan' else 70, 'method': 5}))
    else:
        cands.append((img, {'quality': {'slides': Q_SLIDE, 'scan': Q_SCAN}.get(kind, Q_PAGE), 'method': 5}))
        if small.getcolors(6000) is not None:  # flat graphics / text: lossless is often smaller (skip for photos)
            cands.append((img, {'lossless': True, 'quality': 80, 'method': 6}))
    best = None
    for im, kw in cands:
        buf = io.BytesIO()
        im.save(buf, 'WEBP', **kw)
        if best is None or buf.tell() < best.tell():
            best = buf
    with open(path, 'wb') as f:
        f.write(best.getvalue())


# ----------------------------------------------------------------------------- page images
class Redactor:
    """Hides personal data: literal strings (meta['redact']) and regex patterns (meta['redact_re'])."""

    def __init__(self, meta):
        self.words = set(meta.get('redact') or [])
        self.patterns = [re.compile(p) for p in meta.get('redact_re') or []]

    def collect(self, text):
        for p in self.patterns:
            self.words.update(m.group(0) for m in p.finditer(text))

    def __call__(self, s):
        for w in sorted(self.words, key=len, reverse=True):
            s = s.replace(w, '•••')
        for p in self.patterns:
            s = p.sub('•••', s)
        return s


def open_pdf(pdf_path, redactor):
    doc = fitz.open(pdf_path)
    if redactor.patterns or redactor.words:
        for page in doc:
            redactor.collect(page.get_text())
        for page in doc:
            hit = False
            for s in redactor.words:
                for r in page.search_for(s):
                    page.add_redact_annot(r + (-2, -2, 2, 2), fill=(0.82, 0.84, 0.88))
                    hit = True
            if hit:
                page.apply_redactions()
    return doc


def render_pages(doc, out_dir, kind, keep, blur=()):
    """Render the kept pages to WebP. Returns [(w, h), ...] in display order.
    Pages listed in `blur` (original 1-based numbers) are blurred beyond recognition."""
    target = SLIDE_W if kind == 'slides' else PAGE_W
    sizes = []
    for n, pno in enumerate(keep, 1):
        page = doc[pno]
        zoom = target / page.rect.width
        img = pix_to_image(page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False))
        if pno + 1 in blur:
            img = img.resize((max(1, img.width // 24), max(1, img.height // 24)), Image.BILINEAR)
            img = img.resize((target, round(target * page.rect.height / page.rect.width)), Image.BILINEAR)
            img = img.filter(ImageFilter.GaussianBlur(8))
        encode_page(img, os.path.join(out_dir, f'p{n:03d}.webp'), kind)
        if kind == 'slides' or n == 1:
            th = img.copy()
            th.thumbnail((THUMB_W, THUMB_W * 2), Image.LANCZOS)
            save_webp(th, os.path.join(out_dir, f't{n:03d}.webp'), Q_THUMB)
        sizes.append([img.width, img.height])
    return sizes


# ----------------------------------------------------------------------------- slides (pptx)
def iter_shapes(shapes):
    items = []
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            items.extend(iter_shapes(sh.shapes))
        else:
            items.append(sh)
    return items


def shape_pos(sh):
    try:
        return (int(sh.top or 0) // 300000, int(sh.left or 0))
    except Exception:
        return (0, 0)


def is_title(sh):
    try:
        return sh.is_placeholder and sh.placeholder_format.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE)
    except Exception:
        return False


def slide_html(slide, red):
    """Structured HTML + plain text of a slide's own text (titles, bullets, tables)."""
    parts, plain = [], []
    shapes = sorted(iter_shapes(slide.shapes), key=lambda s: (0 if is_title(s) else 1, shape_pos(s)))
    for sh in shapes:
        if getattr(sh, 'has_table', False) and sh.has_table:
            rows = []
            for row in sh.table.rows:
                cells = [esc(red(clean_ws(c.text))) for c in row.cells]
                if any(cells):
                    rows.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
                    plain.append(' | '.join(c for c in cells if c))
            if rows:
                parts.append('<table>' + ''.join(rows) + '</table>')
            continue
        if not sh.has_text_frame:
            continue
        paras = [(p.level, red(clean_ws(''.join(r.text for r in p.runs) or p.text)))
                 for p in sh.text_frame.paragraphs]
        paras = [(lv, t) for lv, t in paras if t]
        if not paras:
            continue
        if is_title(sh):
            t = ' '.join(t for _, t in paras)
            parts.append(f'<div class="stitle">{esc(t)}</div>')
            plain.append(t)
            continue
        many = len(paras) > 1
        for lv, t in paras:
            cls = 'lvl2' if lv >= 1 else ('lvl1' if many else '')
            parts.append(f'<p class="{cls}">{esc(t)}</p>' if cls else f'<p>{esc(t)}</p>')
            plain.append(t)
    notes = ''
    if slide.has_notes_slide:
        notes = red(clean_ws(slide.notes_slide.notes_text_frame.text))
    return ''.join(parts), '\n'.join(plain), notes


MEDIA_RE = re.compile(r'\.(mp4|m4v|mov|avi|wmv|mpg|mpeg|mp3|wav|m4a|wma)$', re.I)


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which('ffmpeg')


def export_media(blob, name, out_dir, n):
    """Write a slide audio/video blob as a web friendly file. Returns (type, relative path) or None."""
    ext = os.path.splitext(name)[1].lower()
    is_video = ext in ('.mp4', '.m4v', '.mov', '.avi', '.wmv', '.mpg', '.mpeg')
    media_dir = os.path.join(out_dir, 'media')
    os.makedirs(media_dir, exist_ok=True)
    done = os.path.join(media_dir, f'video{n}.mp4' if is_video else f'audio{n}.mp3')
    if os.path.exists(done):  # encoded by an earlier build (the folder is wiped when the source changes)
        return ('video' if is_video else 'audio'), 'media/' + os.path.basename(done)
    tmp = os.path.join(BUILD, f'tmp_media_{os.getpid()}_{n}{ext}')
    with open(tmp, 'wb') as f:
        f.write(blob)
    ff = ffmpeg_exe()
    try:
        if is_video:
            out = os.path.join(media_dir, f'video{n}.mp4')
            if not ff:
                return None
            subprocess.run([ff, '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp, '-vf', 'scale=-2:720',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', out], check=True)
            return 'video', f'media/video{n}.mp4'
        out = os.path.join(media_dir, f'audio{n}.mp3')
        if ext == '.mp3':
            shutil.copyfile(tmp, out)
        elif ff:
            subprocess.run([ff, '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp, '-b:a', '64k', out], check=True)
        else:
            return None
        return 'audio', f'media/audio{n}.mp3'
    finally:
        os.remove(tmp)


def build_slides(meta, ox, pdf_doc, out_dir, keep, red):
    prs = Presentation(ox)
    slides = list(prs.slides)
    policy = meta.get('media', 'all')  # all | video | none
    data, search = [], []
    media_count = 0
    for n, pno in enumerate(keep, 1):
        s = slides[pno] if pno < len(slides) else None
        html, plain, notes = slide_html(s, red) if s else ('', '', '')
        pdf_text = clean_ws(pdf_doc[pno].get_text()) if pno < len(pdf_doc) else ''
        if not plain and pdf_text:  # SmartArt / diagrams: fall back to the rendered text
            html = f'<p>{esc(pdf_text)}</p>'
        if pno + 1 in (meta.get('blur_pages') or ()):  # blurred slide: say why instead of showing its text
            html, plain, pdf_text = ('<p class="empty-note">Video și imagini prezentate doar la curs — '
                                     'nu sunt publicate pe site.</p>'), '', ''
        media = []
        if s is not None and policy != 'none':
            seen = set()
            for rel in s.part.rels.values():
                if rel.is_external:
                    continue
                pn = str(rel.target_part.partname)
                if not MEDIA_RE.search(pn) or pn in seen:
                    continue
                seen.add(pn)
                is_video = re.search(r'\.(mp4|m4v|mov|avi|wmv|mpg|mpeg)$', pn, re.I)
                if policy == 'video' and not is_video:
                    continue
                media_count += 1
                res = export_media(rel.target_part.blob, pn, out_dir, media_count)
                if res:
                    media.append({'t': res[0], 's': res[1]})
        item = {'h': html}
        if notes:
            item['n'] = esc(notes)
        if media:
            item['m'] = media
        data.append(item)
        search.append([n, clean_ws(' '.join(x for x in (plain or pdf_text, notes) if x))])
    return data, search


# ----------------------------------------------------------------------------- Word (docx) -> HTML
INLINE = {'strong', 'em', 'u', 's', 'sup', 'sub', 'a', 'span'}
LABEL_RE = re.compile(r'^(TITLUL|Titlul|PARTEA|Partea|CAPITOLUL|Capitolul|SEC[ŢȚ]IUNEA|Sec[ţț]iunea|ANEXA|Anexa)'
                      r'(\s+(nr\.\s*)?([IVXLC]+|\d+|a\s+\d+-a|[IVXLC]+\.))?\.?$')
JUNK_RE = re.compile(r'ID intern unic|Fişa actului juridic|Fișa actului juridic|Версия на русском|Versiunea originala')


def flatten(el, marks=()):
    """Element -> list of tokens: ('t', text, marks) | ('br',) | ('img', element)."""
    toks = []
    if el.text:
        toks.append(('t', el.text, marks))
    for ch in el:
        tag = ch.tag
        if tag == 'br':
            toks.append(('br',))
        elif tag == 'img':
            toks.append(('img', ET.Element('img', dict(ch.attrib))))  # copy without .tail
        elif tag in INLINE:
            attrs = tuple(sorted(ch.attrib.items())) if tag == 'a' else ()
            toks.extend(flatten(ch, marks + ((tag, attrs),)))
        else:
            toks.extend(flatten(ch, marks))
        if ch.tail:
            toks.append(('t', ch.tail, marks))
    return toks


def build_inline(parent, toks):
    """Rebuild inline markup from tokens under `parent` (merging equal marks)."""
    stack = [(parent, ())]
    for tok in toks:
        if tok[0] == 'img':
            while len(stack) > 1:
                stack.pop()
            stack[0][0].append(tok[1])
            continue
        _, text, marks = tok
        # pop until current marks are a prefix of the token marks
        while len(stack) > 1 and stack[-1][1] != marks[:len(stack[-1][1])]:
            stack.pop()
        cur_el, cur_marks = stack[-1]
        for m in marks[len(cur_marks):]:
            child = ET.SubElement(cur_el, m[0], dict(m[1]))
            cur_marks = cur_marks + (m,)
            stack.append((child, cur_marks))
            cur_el = child
        if len(cur_el):
            last = cur_el[-1]
            last.tail = (last.tail or '') + text
        else:
            cur_el.text = (cur_el.text or '') + text


def tok_text(toks):
    return clean_ws(''.join(t[1] for t in toks if t[0] == 't'))


def all_bold(toks):
    texts = [t for t in toks if t[0] == 't' and t[1].strip()]
    return bool(texts) and all(any(m[0] == 'strong' for m in t[2]) for t in texts)


NOT_HEADING_RE = re.compile(r'^(Ministru|MINISTRU|Ministrul|PRIM-MINISTRU|Prim-ministru|Prim-ministrul|Şef|Șef|Secretar|COORDONAT|'
                            r'Coordonat|Contrasemnează|CONTRASEMNEAZĂ|Tabelul de distribuire|Întocmit|Aprobat|APROB|Avizat|'
                            r'Viceministru|Comisar|comisar|Nr\.\s*\d)')


def heading_level(text, bold):
    if len(text) > 220 or NOT_HEADING_RE.match(text):
        return 0
    if re.match(r'^(TITLUL|Titlul|PARTEA|Partea|CAPITOLUL|Capitolul)\s+([IVXLC]+|\d+)\b', text) and len(text) < 140:
        return 2
    if re.match(r'^(ANEXA|Anexa)\b', text) and len(text) < 80:
        return 2
    if re.match(r'^(SEC[ŢȚ]IUNEA|Sec[ţț]iunea)\b', text):
        return 3
    if re.match(r'^Articolul\s+\d+', text) and len(text) < 200:
        return 4
    if not bold or len(text) > 140 or text.endswith((',', ';')) or len(text) < 3:
        return 0
    if re.match(r'^(TEMA|Tema)\b', text):
        return 2
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.8:
        return 3
    return 4


def docx_html(docx_path, doc_id, out_dir, page_texts=None):
    img_dir = os.path.join(out_dir, 'img')
    counter = [0]

    def convert_image(image):
        counter[0] += 1
        n = counter[0]
        if 'emblem' in (getattr(image, 'alt_text', None) or '').lower():
            return {'src': ''}
        try:
            with image.open() as f:
                data = f.read()
            im = Image.open(io.BytesIO(data))
            im.load()
            if im.width < 12 or im.height < 12:
                return {'src': ''}
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            os.makedirs(img_dir, exist_ok=True)
            save_webp(im, os.path.join(img_dir, f'i{n}.webp'), 80)
            return {'src': f'content/{doc_id}/img/i{n}.webp', 'width': str(im.width), 'height': str(im.height)}
        except Exception as e:  # unsupported vector formats etc.
            print(f'      ! image {n} skipped ({image.content_type}): {e}')
            return {'src': ''}

    with open(docx_path, 'rb') as f:
        res = mammoth.convert_to_html(f, convert_image=mammoth.images.img_element(convert_image))
    root = ET.fromstring('<root>' + res.value.replace('&nbsp;', ' ') + '</root>')

    out = ET.Element('root')

    def add_block(el):
        tag = el.tag
        if tag == 'table':
            for row in el.findall('.//tr'):  # drop web-page header rows (copied from legis.md)
                if JUNK_RE.search(''.join(row.itertext())):
                    for parent in el.iter():
                        if row in list(parent):
                            parent.remove(row)
                            break
            rows = el.findall('.//tr')
            if not rows:
                return
            if all(len(r.findall('td')) + len(r.findall('th')) == 1 for r in rows):
                for row in rows:  # unwrap single column layout tables
                    for cell in row:
                        for ch in list(cell):
                            add_block(ch)
                return
            out.append(el)
            return
        if tag in ('ul', 'ol'):
            out.append(el)
            return
        if tag not in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            out.append(el)
            return
        toks = flatten(el)
        bold = all_bold(toks)
        if tag == 'p' and not bold and any(t[0] == 'br' for t in toks):
            groups, cur = [], []
            for t in toks:
                if t[0] == 'br':
                    groups.append(cur)
                    cur = []
                else:
                    cur.append(t)
            groups.append(cur)
        else:
            groups = [[t if t[0] != 'br' else ('t', ' ', ()) for t in toks]]
        for g in groups:
            text = tok_text(g)
            has_img = any(t[0] == 'img' and t[1].get('src') for t in g)
            g = [t for t in g if not (t[0] == 'img' and 'emblem' in (t[1].get('alt') or '').lower())]
            has_img = any(t[0] == 'img' and t[1].get('src') for t in g)
            if not text and not has_img:
                continue
            if JUNK_RE.search(text):
                continue
            # strip leading indentation spaces
            for i, t in enumerate(g):
                if t[0] == 't':
                    g[i] = ('t', t[1].lstrip(), t[2])
                    if g[i][1]:
                        break
            if tag.startswith('h'):  # Word heading style - but sometimes misused for body text
                lvl = int(tag[1]) if len(text) <= 160 and not NOT_HEADING_RE.match(text) else 0
            else:
                lvl = heading_level(text, all_bold(g))
            if has_img and not text:
                lvl = 0
            new = ET.Element(f'h{max(2, min(lvl, 4))}' if lvl else 'p')
            build_inline(new, [t for t in g if not (t[0] == 'img' and not t[1].get('src'))])
            out.append(new)

    for el in list(root):
        add_block(el)

    # merge "CAPITOLUL I" + "DISPOZIŢII GENERALE" and multi-line upper-case titles
    def upper_ratio(s):
        letters = [c for c in s if c.isalpha()]
        return sum(c.isupper() for c in letters) / max(1, len(letters))

    blocks = list(out)
    merged = []
    for el in blocks:
        prev = merged[-1] if merged else None
        txt = clean_ws(''.join(el.itertext()))
        if prev is not None and prev.tag in ('h2', 'h3', 'h4') and el.tag in ('h2', 'h3', 'h4', 'p'):
            ptxt = clean_ws(''.join(prev.itertext()))
            short = len(txt) < 170 and not re.match(r'^(TITLUL|CAPITOLUL|SEC[ŢȚ]IUNEA|Capitolul|Sec[ţț]iunea|Titlul|ANEXA|Anexa)\b', txt)
            upper = bool(txt) and upper_ratio(txt) > 0.8
            if (LABEL_RE.match(ptxt) and short and (el.tag != 'p' or upper)) or \
               (el.tag != 'p' and upper and short and not ptxt.endswith(('.', ':')) and not LABEL_RE.match(txt) and
                    upper_ratio(ptxt) > 0.8 and len(ptxt) + len(txt) < 200 and not NOT_HEADING_RE.match(txt)):
                sep = ' — ' if LABEL_RE.match(ptxt) else ' '
                for ch in list(prev):
                    prev.remove(ch)
                prev.text = ptxt + sep + txt
                if LABEL_RE.match(ptxt) and prev.tag == 'h4':
                    prev.tag = 'h3'
                continue
        merged.append(el)

    if page_texts and len(page_texts) > 1:
        merged = insert_page_markers(merged, page_texts)
    return finish_html(merged)


def _fold_txt(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^0-9a-zа-яё]+', '', s)  # letters and digits only: robust to spacing/punctuation differences


def insert_page_markers(blocks, page_texts):
    """Put <div class="page-sep"> before the block where each PDF page starts (Word documents)."""
    folded = [_fold_txt(''.join(el.itertext())) for el in blocks]
    marks = {0: 1}
    pos = 0
    for pno, text in enumerate(page_texts[1:], 2):
        probe = None
        for line in text.splitlines():
            f = _fold_txt(re.sub(r'^\s*([\d\.\)\-–•●▪]+\s*)+', '', line))
            if len(f) >= 18 and not f.isdigit():
                probe = f[:28]
                break
        if not probe:
            continue
        for i in range(pos, len(blocks)):
            if probe in folded[i] or (i + 1 < len(blocks) and probe in folded[i] + folded[i + 1] and probe not in folded[i + 1]):
                if i not in marks:
                    marks[i] = pno
                pos = i
                break
    out = []
    for i, el in enumerate(blocks):
        if i in marks:
            out.append(ET.Element('div', {'class': 'page-sep', 'id': f'pg-{marks[i]}', 'data-p': str(marks[i])}))
        out.append(el)
    return out


def finish_html(blocks):
    """Assign heading ids, build the table of contents, serialize."""
    toc = []
    n = 0
    for el in blocks:
        if el.tag in ('h2', 'h3', 'h4'):
            n += 1
            el.set('id', f'h{n}')
            toc.append([f'h{n}', int(el.tag[1]), clean_ws(''.join(el.itertext()))[:140]])
    if len(toc) > 160:  # very long documents: keep the TOC to chapters / sections
        toc = [t for t in toc if t[1] <= 3]
    html = ''.join(ET.tostring(el, encoding='unicode', method='html') for el in blocks)
    html = re.sub(r'<p>\s*</p>', '', html)
    return html, toc


# ----------------------------------------------------------------------------- PDF text -> HTML
BULLET_RE = re.compile(r'^(\(?\d{1,3}[\.\)]\s|\(?[a-zăîâșțşţ][\)\.]\s|[-–—•●▪■►✓]\s?|\d{1,2}\.\d{1,2}\.?\s)')
TERMINAL = ('.', '!', '?', ':', ';', '»', '”', '"')


def pdf_lines(doc, keep):
    pages = []
    for pno in keep:
        page = doc[pno]
        h = page.rect.height
        blocks = []
        for b in page.get_text('dict')['blocks']:
            if b.get('type') != 0:
                continue
            lines = []
            for l in b['lines']:
                spans = [s for s in l['spans'] if s['text'].strip()]
                if not spans:
                    continue
                text = clean_ws(''.join(s['text'] for s in l['spans']))
                size = max(s['size'] for s in spans)
                bold = all((s['flags'] & 16) or re.search(r'bold|black|heavy', s['font'], re.I) for s in spans)
                lines.append({'t': text, 'x0': l['bbox'][0], 'x1': l['bbox'][2], 'y0': l['bbox'][1], 'y1': l['bbox'][3],
                              'size': size, 'bold': bool(bold)})
            if lines:
                blocks.append(lines)
        pages.append((h, blocks))
    return pages


def pdf_html(doc, keep):
    pages = pdf_lines(doc, keep)
    sizes = Counter()
    edge = Counter()
    for h, blocks in pages:
        for lines in blocks:
            for l in lines:
                sizes[round(l['size'])] += len(l['t'])
                if l['y0'] < h * 0.07 or l['y1'] > h * 0.93:
                    edge[re.sub(r'\d+', '#', l['t'])] += 1
    body = sizes.most_common(1)[0][0] if sizes else 12
    repeated = {k for k, v in edge.items() if v >= max(3, len(pages) * 0.3)}

    paras = []  # dicts: kind (p|h|page), text, size, page
    lower = re.compile(r'[a-zăîâșțşţ]')
    for pi, (h, blocks) in enumerate(pages, 1):
        paras.append({'kind': 'page', 'page': pi})
        lines = []
        for bl in blocks:
            for l in bl:
                at_edge = l['y0'] < h * 0.07 or l['y1'] > h * 0.93
                if at_edge and (re.fullmatch(r'[\d\s\-–/]+', l['t']) or re.sub(r'\d+', '#', l['t']) in repeated):
                    continue
                lines.append(l)
        if not lines:
            continue
        body_lines = [l for l in lines if len(l['t']) > 40] or lines
        left = min(l['x0'] for l in body_lines)
        right = max(l['x1'] for l in body_lines)
        width = max(1.0, right - left)
        cur = prev = None
        for l in lines:
            t = l['t']
            is_head = (l['size'] >= body + 1.5 or l['bold']) and len(t) < 160
            if prev is not None and abs(l['y0'] - prev['y0']) < 2 and l['x0'] >= prev['x1'] - 1:
                same_line = True  # pieces of one visual line
            else:
                same_line = False
            if cur is None:
                start = True
            elif same_line:
                start = False
            else:
                lh = max(1.0, prev['y1'] - prev['y0'])
                gap = l['y0'] - prev['y1']
                prev_short = prev['x1'] < right - width * 0.15
                start = bool(
                    BULLET_RE.match(t)
                    or (cur['kind'] == 'h') != is_head
                    or gap > lh * 0.7 or gap < -lh * 1.5
                    or (cur['text'].endswith(TERMINAL) and (prev_short or l['x0'] > left + 15))
                    or (prev['x1'] < right - width * 0.4 and not lower.match(t))
                )
                if lower.match(t) and not BULLET_RE.match(t) and (cur['kind'] == 'h') == is_head and -lh < gap <= lh * 1.2:
                    start = False  # a line starting in lower case continues the sentence
            if start:
                cur = {'kind': 'h' if is_head else 'p', 'text': t, 'size': l['size'], 'page': pi}
                paras.append(cur)
            else:
                joiner = '' if (cur['text'].endswith('-') and lower.match(t)) else ' '
                cur['text'] += joiner + t
                cur['size'] = max(cur['size'], l['size'])
            prev = l

    # continue paragraphs across page breaks
    out = []
    for p in paras:
        if p['kind'] == 'p' and out:
            prev_text = next((q for q in reversed(out) if q['kind'] != 'page'), None)
            if (prev_text is not None and prev_text['kind'] == 'p' and out[-1]['kind'] == 'page' and
                    not prev_text['text'].endswith(TERMINAL) and re.match(r'[a-zăîâșțşţ]', p['text'])):
                prev_text['text'] += ' ' + p['text']
                continue
        out.append(p)

    head_sizes = sorted({round(p['size']) for p in out if p['kind'] == 'h' and round(p['size']) > body + 1}, reverse=True)
    blocks = []
    for p in out:
        if p['kind'] == 'page':
            el = ET.Element('div', {'class': 'page-sep', 'id': f"pg-{p['page']}", 'data-p': str(p['page'])})
            blocks.append(el)
            continue
        text = p['text']
        if p['kind'] == 'h':
            if round(p['size']) in head_sizes[:1] and len(head_sizes) > 0:
                lvl = 2
            elif round(p['size']) > body + 1:
                lvl = 3
            else:
                lvl = heading_level(text, True) or 4
                lvl = max(lvl, 3)
            el = ET.Element(f'h{lvl}')
        else:
            el = ET.Element('p')
        el.text = text
        blocks.append(el)
    # drop page separator when the document has a single page
    if len(pages) <= 1:
        blocks = [b for b in blocks if b.tag != 'div']
    return finish_html(blocks)


# ----------------------------------------------------------------------------- OCR (scanned PDFs)
def ocr_fix(s):
    s = s.replace('ä', 'ă').replace('Ä', 'Ă').replace('§', 'ș')
    s = re.sub(r'(?<=[A-Za-zăîâ])!(?=[a-zăîâ])', 'ț', s)
    s = re.sub(r'(?<=[A-Za-zăîâ])\$(?=[a-zăîâ])', 'ș', s)
    s = re.sub(r'(?<=\s)\$(?=[a-zăîâ])', 'ș', s)
    return s


def ocr_pages(doc, keep, cache_path):
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, encoding='utf-8') as f:
            cache = json.load(f)
    import winocr

    async def run(img):
        return await winocr.recognize_pil(img, 'en')

    texts = []
    for pno in keep:
        key = str(pno)
        if key not in cache:
            page = doc[pno]
            zoom = 1800 / page.rect.width
            img = pix_to_image(page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False))
            res = asyncio.run(run(img))
            cache[key] = '\n'.join(l.text for l in res.lines)
        texts.append(cache[key])
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False)
    return [ocr_fix(clean_ws(t)) for t in texts]


# ----------------------------------------------------------------------------- one document
def _sha(obj):
    return hashlib.sha1(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def stamps_of(meta, src):
    """(images stamp, text stamp): page images are re-rendered only when the source or the redactions change."""
    st = os.stat(src)
    base = [st.st_size, int(st.st_mtime), {k: meta.get(k) for k in ('kind', 'redact', 'redact_re', 'skip_pages', 'src')}]
    if meta.get('blur_pages'):  # only where used, so the stamps of the other documents stay valid
        base.append({'blur_pages': meta['blur_pages']})
    return _sha([IMG_VERSION, base]), _sha([TXT_VERSION, base, meta.get('media')])


def legacy_stamp(meta, src):  # stamp format of the first builds (images + text together, BUILD_VERSION 4)
    st = os.stat(src)
    relevant = {k: meta.get(k) for k in ('kind', 'redact', 'skip_pages', 'media', 'src')}
    return _sha([4, st.st_size, int(st.st_mtime), relevant])


def read_doc_js(path):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    return json.loads(s[s.index(',') + 1:s.rindex(')')])


def build_doc(doc_id, meta, src, force=False):
    t0 = time.time()
    out_dir = os.path.join(CONTENT, doc_id)
    doc_js = os.path.join(out_dir, 'doc.js')
    stamp_file = os.path.join(BUILD, 'stamps', doc_id + '.json')
    img_stamp, txt_stamp = stamps_of(meta, src)
    old = {}
    if os.path.exists(stamp_file):
        with open(stamp_file, encoding='utf-8') as f:
            old = json.load(f)
        if 'stamp' in old and old['stamp'] == legacy_stamp(meta, src):  # migrate the first builds
            old = {'img': img_stamp, 'txt': '', 'result': old['result']}
    if not force and old.get('img') == img_stamp and old.get('txt') == txt_stamp and os.path.exists(doc_js):
        return old['result']

    pdf, ox = derived_paths(src)
    if not os.path.exists(pdf):
        raise FileNotFoundError(f'{doc_id}: PDF missing ({pdf}) - run tools/convert_office.ps1 first')

    kind = meta['kind']
    red = Redactor(meta)
    doc = open_pdf(pdf, red)
    skip = {p - 1 for p in meta.get('skip_pages', [])}
    keep = [i for i in range(len(doc)) if i not in skip]

    sizes = None
    if not force and old.get('img') == img_stamp and os.path.exists(doc_js):
        try:
            sizes = read_doc_js(doc_js)['pages']
            if len(sizes) != len(keep) or not os.path.exists(os.path.join(out_dir, f'p{len(keep):03d}.webp')):
                sizes = None
        except Exception:
            sizes = None
    if sizes is None:  # full rebuild
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)
        sizes = render_pages(doc, out_dir, kind, keep, set(meta.get('blur_pages') or ()))
    else:  # text only: keep page images (and already encoded media), drop old document images
        if os.path.isdir(os.path.join(out_dir, 'img')):
            shutil.rmtree(os.path.join(out_dir, 'img'))

    payload = {'kind': kind, 'pages': sizes}
    search = []
    if kind == 'slides':
        slides, search = build_slides(meta, ox, doc, out_dir, keep, red)
        payload['slides'] = slides
    elif kind == 'doc':
        html, toc = docx_html(ox, doc_id, out_dir, [red(doc[p].get_text()) for p in keep])
        payload['html'], payload['toc'] = html, toc
    elif kind == 'pdf':
        html, toc = pdf_html(doc, keep)
        payload['html'], payload['toc'] = html, toc
    if kind in ('doc', 'pdf'):
        search = [[n, clean_ws(red(doc[p].get_text()))] for n, p in enumerate(keep, 1)]
    if kind == 'scan':
        texts = ocr_pages(doc, keep, os.path.join(BUILD, 'ocr', doc_id + '.json'))
        search = [[n, t] for n, t in enumerate(texts, 1)]
        payload['ocr'] = True

    with open(os.path.join(out_dir, 'doc.js'), 'w', encoding='utf-8') as f:
        f.write('LIB.doc(' + json.dumps(doc_id) + ',' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + ');\n')

    size = sum(os.path.getsize(os.path.join(dp, fn)) for dp, _, fns in os.walk(out_dir) for fn in fns)
    result = {
        'pages': len(sizes), 'ar': sizes[0] if sizes else [4, 3],
        'hasText': kind in ('doc', 'pdf', 'slides'), 'ocr': kind == 'scan',
        'media': any('m' in s for s in payload.get('slides', [])),
        'size': size, 'search': search,
    }
    os.makedirs(os.path.dirname(stamp_file), exist_ok=True)
    with open(stamp_file, 'w', encoding='utf-8') as f:
        json.dump({'img': img_stamp, 'txt': txt_stamp, 'result': result}, f, ensure_ascii=False)
    print(f'  ✓ {doc_id:24s} {kind:6s} {len(sizes):4d} pages  {size / 1048576:6.1f} MB  {time.time() - t0:5.1f}s', flush=True)
    return result


def _worker(args):
    doc_id, meta, src, force = args
    try:
        return doc_id, build_doc(doc_id, meta, src, force), None
    except Exception as e:  # report and continue with the other documents
        import traceback
        return doc_id, None, traceback.format_exc()


# ----------------------------------------------------------------------------- catalog + search
def write_js(path, var, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'window.{var}=' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + ';\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true', help='rebuild every document')
    ap.add_argument('--only', default='', help='comma separated document ids to (re)build')
    ap.add_argument('--jobs', type=int, default=max(1, min(6, (os.cpu_count() or 2) - 1)))
    args = ap.parse_args()

    idx = source_index()
    srcs = {}
    for doc_id, meta in DOCS.items():
        key = fold(meta['src'])
        if key not in idx:
            sys.exit(f'Source not found for {doc_id}: {meta["src"]}')
        srcs[doc_id] = idx[key]
    used = set(DOCS)
    for c in COURSES:
        for _, ids in c['sections']:
            for i in ids:
                assert i in DOCS, i
    only = {s.strip() for s in args.only.split(',') if s.strip()}

    print(f'Building {len(DOCS)} documents with {args.jobs} workers…')
    results, errors = {}, {}
    tasks = [(d, DOCS[d], srcs[d], args.force or d in only) for d in DOCS]
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(_worker, t) for t in tasks]
        for fut in as_completed(futs):
            doc_id, res, err = fut.result()
            if err:
                errors[doc_id] = err
                print(f'  ✗ {doc_id}\n{err}')
            else:
                results[doc_id] = res
    if errors:
        sys.exit(f'{len(errors)} document(s) failed: {", ".join(errors)}')

    # remove content folders of documents that no longer exist
    if os.path.isdir(CONTENT):
        for d in os.listdir(CONTENT):
            if d not in used:
                shutil.rmtree(os.path.join(CONTENT, d))

    doc_course = {}
    for c in COURSES:
        for _, ids in c['sections']:
            for i in ids:
                doc_course[i] = c['id']
    docs_out = {}
    for doc_id, meta in DOCS.items():
        r = results[doc_id]
        kind = meta['kind']
        docs_out[doc_id] = {
            'course': doc_course.get(doc_id), 'kind': kind, 'type': meta['type'],
            'kicker': meta.get('kicker'), 'title': meta['title'], 'summary': meta.get('summary'),
            'points': meta.get('points'),
            'mode': meta.get('mode') or {'slides': 'slides', 'scan': 'pages'}.get(kind, 'text'),
            'pages': r['pages'], 'ar': r['ar'], 'hasText': r['hasText'], 'ocr': r['ocr'], 'media': r['media'],
            'size': r['size'], 'words': sum(len(text.split()) for _, text in r['search']),
        }
    courses_out = []
    for c in COURSES:
        cc = {k: v for k, v in c.items() if k != 'sections'}
        cc['sections'] = [{'key': key, 'title': SECTION_TITLES[key], 'docs': ids} for key, ids in c['sections']]
        courses_out.append(cc)
    stats = {
        'courses': len(COURSES), 'docs': len(DOCS),
        'slides': sum(d['pages'] for d in docs_out.values() if d['kind'] == 'slides'),
        'pages': sum(d['pages'] for d in docs_out.values() if d['kind'] != 'slides'),
    }
    catalog = {'built': time.strftime('%Y-%m-%d'), 'site': SITE, 'types': TYPES, 'courses': courses_out,
               'general': GENERAL, 'docs': docs_out, 'stats': stats}
    write_js(os.path.join(DATA, 'catalog.js'), 'LIB_CATALOG', catalog)

    order = list(DOCS)
    items = []
    for di, doc_id in enumerate(order):
        for page, text in results[doc_id]['search']:
            if text:
                items.append([di, page, text])
    write_js(os.path.join(DATA, 'search.js'), 'LIB_SEARCH', {'docs': order, 'items': items})

    total = sum(d['size'] for d in docs_out.values())
    print(f'Done: {stats["docs"]} documents, {stats["slides"]} slides, {stats["pages"]} pages, {total / 1048576:.1f} MB of content.')


if __name__ == '__main__':
    main()
