#!/usr/bin/env python3
"""generar_lagunas_deuda.py — genera la página-hub de lagunas y deuda técnica
del vault club-compra, leyendo frontmatter + secciones `## Lagunas`/`## Deuda
técnica` de las páginas en disco (BOM-safe, idempotente, no modifica fuentes).

Salida: wiki/hilos/lagunas-y-deuda-tecnica.md  (type: hilo, con BOM).
Uso:    py scripts/generar_lagunas_deuda.py
"""
import io
import pathlib
import re

BOM = b"\xef\xbb\xbf"
ROOT = pathlib.Path(r"D:\PrjWiki\club-compra")
WIKI = ROOT / "wiki"
HILOS = WIKI / "hilos"
OUT = HILOS / "lagunas-y-deuda-tecnica.md"

TIPOS_HILO = ["hilo"]
INFRA = {"index", "overview", "hoy", "log", "guia-de-navegacion", "club-de-compra-solar"}
SECS_REQ = {"hilo": ["## Resumen", "## Cadena temporal", "## Lagunas"]}


def leer(p):
    b = p.read_bytes()
    t = b[3:].decode("utf-8") if b.startswith(BOM) else b.decode("utf-8")
    t = t.lstrip("\ufeff")
    return t


def frontmatter(t):
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    fm = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                fm.setdefault(k.strip(), []).append(v.strip())
    return fm


def seccion(t, titulo):
    m = re.search(r"^## %s\n(.*?)(?=^## |\Z)" % re.escape(titulo), t, re.M | re.S)
    return m.group(1) if m else ""


def items(t, titulo, solo_checklist=False):
    """Items de una sección por líneas: bullets `-`/`*` (y checklist si se pide)."""
    out = []
    for ln in seccion(t, titulo).splitlines():
        s = ln.strip()
        if not s:
            continue
        if solo_checklist:
            m = re.match(r"^- \[[ xX]\]\s+(.*)", s)
            if m:
                out.append(m.group(1))
        else:
            m = re.match(r"^[-*]\s+(.*)", s)
            if m and not re.match(r"^[-*]\s+\[[ xX]\]", s):
                out.append(m.group(1))
    return out


def main():
    cadena = []
    deuda = []

    todos = sorted(WIKI.rglob("*.md"))
    for p in todos:
        if p.parent.name == "sources":
            continue
        t = leer(p)
        fm = frontmatter(t)
        tipo = (fm.get("type") or ["?"])[0]
        if tipo not in TIPOS_HILO:
            continue

        comp = (fm.get("completitud") or ["?"])[0]
        status = (fm.get("status") or ["?"])[0]
        lags = items(t, "Lagunas", solo_checklist=True)
        deudas = items(t, "Deuda técnica")

        cadena.append(
            {"slug": p.stem, "tipo": tipo, "status": status, "comp": comp,
             "n": len(lags), "lags": lags, "deudas": deudas}
        )

    cadena.sort(key=lambda r: r["slug"])
    total_lag = sum(r["n"] for r in cadena)
    total_deuda = sum(len(r["deudas"]) for r in cadena)

    buf = io.StringIO()
    w = buf.write
    w("---\n")
    w("type: hilo\n")
    w("status: vigente\n")
    w("completitud: alta\n")
    w("aliases:\n")
    w("  - dashboard de lagunas\n")
    w("  - lagunas y deuda tecnica\n")
    w("  - deuda tecnica del vault\n")
    w("---\n\n")
    w("# Lagunas y deuda técnica\n\n")
    w("> **TL;DR:** Dashboard consolidado, verificado contra disco, de las ")
    w("**lagunas de validación** (checklist sin marcar en `## Lagunas`) y la ")
    w("**deuda técnica** declarada (`## Deuda técnica`) de las páginas tipo ")
    w("`hilo` del vault. Total: **%d lagunas** y **%d ítems de deuda técnica**.\n\n"
      % (total_lag, total_deuda))

    w("## Resumen\n\n")
    w("Esta página se regenera con `py scripts/generar_lagunas_deuda.py` y ")
    w("consolida, en orden de cadena temporal, qué **falta para validar** y qué ")
    w("**quedó pendiente** en cada eslabón del hilo ")
    w("[[hilo-propuesta-growth-partner]]. No reemplaza a las fuentes: enlaza a ")
    w("cada una para que el detalle viva en su lugar canónico.\n\n")

    w("## Cadena temporal\n\n")
    w("| Eslabón | Status | Completitud | Lagunas | Deuda técnica |\n")
    w("|---------|--------|-------------|---------|---------------|\n")
    for r in cadena:
        w("| [[%s]] | %s | %s | %d | %d |\n"
          % (r["slug"], r["status"], r["comp"], r["n"], len(r["deudas"])))
    w("\n")

    w("## Lagunas\n\n")
    if not cadena:
        w("_(vault sin páginas tipo `hilo` — probablemente el patron de cadena "
          "aún no se usó)_\n")
    for r in cadena:
        w("### [[%s]] (%d)\n" % (r["slug"], r["n"]))
        w("")
        if not r["lags"]:
            w("- Nada abierto.\n\n")
        for it in r["lags"]:
            w("- [ ] %s\n" % it)
        w("\n")

    w("## Deuda técnica\n\n")
    for r in cadena:
        if not r["deudas"]:
            continue
        w("### [[%s]]\n" % r["slug"])
        w("")
        for it in r["deudas"]:
            w("- %s\n" % it)
        w("\n")

    w("## Fuentes\n\n")
    w("- _Generado por_ `scripts/generar_lagunas_deuda.py` (BOM-safe, idempotente).\n")
    w("- _Vault:_ [[index]].\n")

    texto = buf.getvalue()
    OUT.write_bytes(BOM + texto.encode("utf-8"))
    print("PAGINA OK -> %s (%d B · %d hilo · %d lagunas · %d deuda)"
          % (OUT, OUT.stat().st_size, len(cadena), total_lag, total_deuda))


if __name__ == "__main__":
    main()
