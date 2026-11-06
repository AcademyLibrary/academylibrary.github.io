# Grupa 131 · Inițiere în Ofițer — biblioteca de studiu

Biblioteca digitală a cursanților Grupei 131 (cursul de formare inițială a ofițerilor).
Toate materialele disciplinelor se citesc direct pe site, de pe telefon sau calculator.

**Site:** https://academylibrary.github.io/  
**Depozit:** https://github.com/AcademyLibrary/academylibrary.github.io

| Disciplina | Ce conține |
|---|---|
| Instrucția de front | prezentare, instrucțiune metodică (pasul de defilare), Regulamentul instrucției de front, Ordinele MAI nr. 493/2024 și nr. 54/2024, HG nr. 676/2023 |
| AROP | Tema 1–3: menținerea, asigurarea și restabilirea ordinii publice |
| Instrucția tragerii | 8 prezentări (măsuri de siguranță, codificări de alertă, balistică, cartușe…), suporturi de curs, Legile nr. 218/2012 și nr. 130/2012, Ordinele MAI nr. 222/2017 și nr. 311/2015, ghidul intervenției profesionale |
| Prim ajutor | Suport vital bazal, Serviciul 112, sinteză, IPSSM 15/2020, Manualul european de prim ajutor |
| TIP | Tema 1–5: tactica intervenției profesionale |

## Funcții

- interfață în **română** (implicit) și **rusă** — butoanele RO / RU; fiecare material are rezumat și idei principale în ambele limbi;
- butoane **A− / A / A+** pentru mărimea textului (pentru cei cu probleme de vedere) și temă întunecată;
- trei moduri de citire: **Slide-uri** (glisare, ecran complet), **Original** (paginile ca în document) și **Text** (se adaptează telefonului);
- **căutare** în tot conținutul (fără diacritice), cu trimitere directă la slide-ul sau pagina găsită;
- marcarea materialelor **studiate** și progresul pe discipline (salvate doar în browser);
- funcționează pe GitHub Pages și deschis direct de pe disc (`index.html`).

## Structura proiectului

```
index.html             pagina aplicației (o singură pagină, navigare prin #/…)
assets/css, js, fonts  stiluri, cod, fonturi (Inter, Oswald — SIL OFL)
data/catalog.js        discipline, secțiuni, titluri și rezumate RO/RU (generat)
data/search.js         indexul de căutare (generat)
content/<material>/    imaginile paginilor/slide-urilor + doc.js cu textul (generat)
tools/                 scripturile de conversie și catalogul materialelor
```

Fișierele originale (pptx/ppt/doc/pdf) nu sunt incluse în depozit — site-ul folosește versiunile convertite.

## Adăugarea sau actualizarea materialelor (Windows)

Necesar: Microsoft Office (Word, PowerPoint), Python 3 cu pachetele
`pymupdf pillow python-pptx mammoth winocr imageio-ffmpeg`.

1. Puneți fișierele în folderul disciplinei (`AROP`, `Prim ajutor`, `TIP`, `instructia front`, `instrucția tragerii`).
2. Adăugați materialul în `tools/catalog_data.py` (titlu, rezumat, idei principale RO/RU și secțiunea).
3. Rulați:
   ```
   powershell -ExecutionPolicy Bypass -File tools\convert_office.ps1
   python tools\build.py
   ```
4. Publicați modificările (`git add -A && git commit && git push`).

---

Site neoficial, cu scop exclusiv educațional. Materialele aparțin autorilor și instituțiilor emitente.
