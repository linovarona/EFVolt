#!/usr/bin/env python3
"""Lint del vault club-compra. Revisa integridad estructural del wiki.

Dependencias: ninguna (std + regex + pathlib).
Uso:  py scripts/lint_wiki.py [--strict]
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

TIPOS = {
    "source":  ["## Resumen", "## Puntos clave", "## Implicancias para el proyecto",
                "## Posición en la síntesis", "## Lagunas"],
    "entity":  ["## Ficha", "## Rol en el proyecto", "## Puntos clave", "## Fuentes"],
    "concept": ["## Definición", "## Relevancia para el proyecto", "## Deuda técnica", "## Fuentes"],
    "project": ["## Resumen", "## Estado hoy", "## Roadmap", "## Decisiones abiertas",
                "## Deuda técnica", "## Fuentes"],
    "hilo":    ["## Resumen", "## Cadena temporal", "## Lagunas"],
}

INFRA = {"index", "overview", "hoy", "log", "guia-de-navegacion", "club-de-compra-solar"}
INFRA_EJS = {"guia-de-navegacion", "log"}   # paginas con ejemplos literales [[...]]

def load_pages():
    pages = {}   # slug -> {type, path, text}
    aliases = {}
    for p in WIKI.rglob("*.md"):
        text = p.read_text(encoding="utf-8").lstrip("\ufeff")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        fm = {}
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm.setdefault(k.strip(), []).append(v.strip())
            aliases.setdefault(p.stem, [])
            for k, vals in fm.items():
                if k in ("aliases",):
                    aliases[p.stem].extend(vals)
        pages[p.stem] = {"path": p, "text": text, "fm": fm}
    return pages, aliases

def check_frontmatter(pages):
    errs = []
    for slug, pg in pages.items():
        if slug in INFRA:
            # infra: no requiere type (navegacion) pero si frontmatter
            if pg["path"].parent == WIKI:
                continue
        fm = pg["fm"]
        for req in ("type", "status"):
            if req not in fm:
                errs.append(f"[{pg['path'].relative_to(ROOT)}] falta `{req}` en frontmatter")
        if fm.get("status", [""])[0] == "pendiente-validacion":
            errs.append(f"[{pg['path'].relative_to(ROOT)}] status 'pendiente-validacion' (a revisar)")
    return errs

def check_sections(pages):
    errs = []
    for slug, pg in pages.items():
        if slug in INFRA and pg["path"].parent == WIKI:
            continue
        tp = (pg["fm"].get("type") or [""])[0]
        if tp not in TIPOS:
            continue
        text = pg["text"]
        for sec in TIPOS[tp]:
            if sec not in text:
                errs.append(f"[{pg['path'].relative_to(ROOT)}] type={tp}: falta secci\u00f3n `{sec}`")
    return errs

def check_links(pages, aliases):
    errs = []
    slugs = set(pages)
    aset = set()
    for a in aliases.values():
        aset.update(x for x in a if x)
    resolvable = slugs | aset
    for slug, pg in pages.items():
        for m in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]|]+)?\]\]", pg["text"]):
            target = m.group(1).strip()
            if target not in resolvable:
                errs.append(f"[{pg['path'].relative_to(ROOT)}] wikilink roto: [[{target}]]")
    return errs, slugs

def check_orphans(pages):
    """Paginas sin enlaces entrantes (excluye infra y uniones de fuentes)."""
    back = {s: 0 for s in pages}
    for pg in pages.values():
        for m in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]|]+)?\]\]", pg["text"]):
            t = m.group(1).strip()
            if t in back:
                back[t] += 1
    return [s for s, n in back.items() if n == 0 and s not in INFRA]

def check_secuencia(pages):
    """Coherencia de la cadena temporal: `secuencia`+`orden` en fuentes y hub `type: hilo`.

    Regla derivada de la ingesta temporal:
      - una fuente con `secuencia` DEBE tener `orden` (int >= 1);
      - el valor de `secuencia` DEBE apuntar a un hub tipo `hilo` existente;
      - el `orden` dentro de una misma `secuencia` no puede repetirse ni dejar huecos
        (los eslabones se leen con `check_links`/wikilinks, no se reordenan solos).
    """
    errs = []
    hubs = {s for s, pg in pages.items() if (pg["fm"].get("type") or [""])[0] == "hilo"}
    por_secuencia = {}
    for slug, pg in pages.items():
        fm = pg["fm"]
        sec = (fm.get("secuencia") or [""])[0]
        if not sec:
            continue
        ords = fm.get("orden") or []
        if not ords:
            errs.append(f"[{slug}] secuencia `{sec}` sin `orden`")
            continue
        try:
            o = int(ords[0])
        except ValueError:
            errs.append(f"[{slug}] orden `{ords[0]}` no es entero")
            continue
        if sec not in hubs:
            errs.append(f"[{slug}] secuencia `{sec}` no apunta a un hub `type: hilo`")
        por_secuencia.setdefault(sec, []).append(o)
    for sec, ords in por_secuencia.items():
        for i in sorted(set(ords)):
            if ords.count(i) > 1:
                errs.append(f"[secuencia `{sec}`] orden {i} duplicado")
        esperados = set(range(1, max(ords) + 1))
        faltantes = sorted(esperados - set(ords))
        if faltantes:
            errs.append(f"[secuencia `{sec}`] huecos de orden: {', '.join(map(str, faltantes))}")
    return errs


def main():
    strict = "--strict" in sys.argv
    pages, aliases = load_pages()
    fm_errs = check_frontmatter(pages)
    sec_errs = check_sections(pages)
    link_errs, slugs = check_links(pages, aliases)
    orphans = check_orphans(pages)
    seq_errs = check_secuencia(pages)

    code = 0
    def emit(title, items, warn_only=False):
        nonlocal code
        items = sorted(set(items))
        if items:
            print(f"\n== {title} ({len(items)}) ==")
            for i in items:
                print(f"  - {i}")
            if not warn_only:
                code = 1

    print("== Resumen ==")
    print(f"  paginas: {len(pages)}")
    emit("Frontmatter incompleto", fm_errs)
    emit("Secciones canonicas faltantes", sec_errs)
    emit("Wikilinks rotos", link_errs)
    emit("Posibles paginas huerfanas", ["[[" + o + "]]" for o in orphans], warn_only=True)

    print(f"\n{'OK: sin errores criticos' if code == 0 else 'HALLAZGOS: revisar arriba'}")
    sys.exit(code)

if __name__ == "__main__":
    main()
