#!/usr/bin/env python3
"""Dashboard determinístico de lagunas + deuda técnica del vault club-compra.

Lee wiki/sources/*.md + todas las páginas, extrae `## Lagunas` (checkbox sin
marcar) y `## Deuda técnica` (concepts/projects/hilo), y vuelca un reporte
completo a un archivo UTF-8 en %TEMP% — evita la truncación de consola.
No modifica el vault. Uso: py <ruta>
"""
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\PrjWiki\club-compra")
WIKI = ROOT / "wiki"
BOM = b"\xef\xbb\xbf"

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
    pages = {}
    for p in WIKI.rglob("*.md"):
        b = p.read_bytes()
        bom = b.startswith(BOM)
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
    m = re.search(rf"^## {re.escape(titulo)}\n(.*?)(?=\n## |\Z)", texto, re.S | re.M)
    return m.group(1) if m else ""


def items_de_seccion(texto, titulo, prefijo=("-", "*")):
    out = []
    for ln in seccion(texto, titulo).splitlines():
        s = ln.strip()
        for pr in prefijo:
            if s.startswith(pr):
                s = s[len(pr):].strip()
                break
        if s and not s.startswith("["):
            out.append(s)
    return out


def main():
    pages = load_pages()
    buf = io.StringIO()
    w = buf.write

    lagunas = []
    deuda = []
    for slug in sorted(pages):
        pg = pages[slug]
        fm = pg["fm"]
        tipo = (fm.get("type") or ["?"])[0]
        status = (fm.get("status") or ["?"])[0]
        comp = (fm.get("completitud") or ["?"])[0]
        lis = items_de_seccion(pg["text"], "Lagunas")
        deudas = items_de_seccion(pg["text"], "Deuda técnica")
        if lis:
            lagunas.append((slug, tipo, status, comp, lis))
        if deudas:
            deuda.append((slug, tipo, status, comp, deudas))

    w("== LAGUNAS (en fuentes) ==\n")
    total_lag = sum(len(x[4]) for x in lagunas)
    w(f"TOTAL_LAGUNAS={total_lag}\n\n")
    for slug, tipo, status, comp, lis in lagunas:
        w(f"[{slug}] {tipo}/{status}/{comp}: {len(lis)}\n")
        for it in lis:
            w(f"   - [ ] {it}\n")
        w("\n")

    w("== DEUDA TECNICA (concepts/projects/hilo) ==\n")
    total_deuda = sum(len(x[4]) for x in deuda)
    w(f"TOTAL_DEUDA={total_deuda}\n\n")
    for slug, tipo, status, comp, deudas in deuda:
        w(f"[{slug}] {tipo}/{status}/{comp}: {len(deudas)}\n")
        for it in deudas:
            w(f"   - {it}\n")
        w("\n")

    dump = pathlib.Path(r"D:\PrjWiki\club-compra").resolve()
    out = pathlib.Path.home() / f"lagunas_deuda_dump_{slug}.txt"
    out = pathlib.Path(r"\prjwiki\club-compra\scripts") / "lagunas_deuda_dump.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(BOM + buf.getvalue().encode("utf-8"))
    print(f"DUMP OK -> {out} ({out.stat().st_size} B)")


if __name__ == "__main__":
    main()
