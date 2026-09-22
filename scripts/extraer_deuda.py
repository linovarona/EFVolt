#!/usr/bin/env python3
"""Extrae el dashboard vivo de lagunas + deuda técnica del vault.

- Lagunas: checkbox `- [ ]` dentro de `## Lagunas` de cada página (type source/entity/concept/project/hilo).
- Deuda técnica: ítems dentro de `## Deuda técnica` / `## Lagunas` de páginas type concept/project/hilo,
  más el frontmatter `deuda` si existe.
Uso: py scripts/extraer_deuda.py
"""
import pathlib, re, io, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def load():
    pages = {}
    for p in WIKI.rglob("*.md"):
        b = p.read_bytes()
        bom = b.startswith(b"\xef\xbb\xbf")
        t = b[3:].decode("utf-8") if bom else b.decode("utf-8")
        t = t.lstrip("\ufeff")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        fm = {}
        if m:
            for ln in m.group(1).splitlines():
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    fm.setdefault(k.strip(), []).append(v.strip())
        pages[p.stem] = {"path": p, "text": t, "fm": fm}
    return pages

def seccion(texto, titulo):
    m = re.search(rf"^## {titulo}\n(.*?)(?=\n## |\Z)", texto, re.S | re.M)
    return m.group(1) if m else ""

def items_lagunas(texto):
    out = []
    for ln in seccion(texto, "Lagunas").splitlines():
        s = ln.strip()
        if s.startswith("- [ ]"):
            out.append(re.sub(r"^-\s*\[\s*\]\s*", "", s))
    return out

def items_deuda(texto):
    out = []
    for ln in seccion(texto, "Deuda técnica").splitlines():
        s = ln.strip()
        if s.startswith(("- [ ]", "- ")):
            out.append(re.sub(r"^-\s*(?:\[\s*\]\s*)?", "", s))
    return out

pages = load()
lagunas = []
deuda = []
for slug, pg in sorted(pages.items()):
    tipo = (pg["fm"].get("type") or ["?"])[0]
    status = (pg["fm"].get("status") or ["?"])[0]
    comp = (pg["fm"].get("completitud") or ["?"])[0]
    li = items_lagunas(pg["text"])
    di = items_deuda(pg["text"])
    # deuda declarada en frontmatter
    d_fm = pg["fm"].get("deuda") or []
    if li:
        lagunas.append((slug, tipo, status, comp, li))
    if di or d_fm:
        deuda.append((slug, tipo, status, comp, di, d_fm))

print(f"== LAGUNAS ({sum(len(x[4]) for x in lagunas)} totales) ==")
for slug, tipo, status, comp, li in lagunas:
    print(f"[{slug}] {tipo}/{status}/{comp}: {len(li)}")
    for it in li:
        print(f"   - {it}")
print(f"\n== DEUDA TECNICA ({sum(len(x[4]) + len(x[5]) for x in deuda)} total) ==")
for slug, tipo, status, comp, di, d_fm in deuda:
    n = len(di) + len(d_fm)
    print(f"[{slug}] {tipo}/{status}/{comp}: {n}")
    for it in di:
        print(f"   - {it}")
    for it in d_fm:
        print(f"   (fm) {it}")