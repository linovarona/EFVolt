#!/usr/bin/env python3
"""generar_pagina_deuda.py — página de lagunas y deuda técnica del vault club-compra.

Lee scripts/lagunas_deuda_dump.txt (generado por extract_deuda.py) y el
frontmatter real de cada eslabón (BOM-safe), y emite wiki/hilos/
lagunas-y-deuda-tecnica.md (type: hilo, con BOM, idempotente).

Uso:  py scripts/generar_pagina_deuda.py
"""
import io
import pathlib
import re
import sys

BOM = b"\xef\xbb\xbf"
ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SRC = WIKI / "sources"
HILOS = WIKI / "hilos"
DUMP = ROOT / "scripts" / "lagunas_deuda_dump.txt"
OUT = HILOS / "lagunas-y-deuda-tecnica.md"


def load_fm(slug):
    """Frontmatter real del eslabón (BOM-safe), dict de lists."""
    p = SRC / f"{slug}.md"
    if not p.exists():
        return None
    b = p.read_bytes()
    t = b[3:].decode("utf-8") if b.startswith(BOM) else b.decode("utf-8")
    t = t.lstrip("\ufeff")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        return None
    fm = {}
    for ln in m.group(1).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm.setdefault(k.strip(), []).append(v.strip())
    return fm


def main():
    tam = DUMP.stat().st_size
    dump = DUMP.read_bytes()
    t = dump[3:].decode("utf-8") if dump.startswith(BOM) else dump.decode("utf-8")
    t = t.lstrip("\ufeff")

    # ---- parsear el dump: macro-bloques y eslabones
    ok = sys.stdout
    ok.reconfigure(encoding="utf-8", errors="replace")

    def perr(pg, fincomb_offset=False):
        return ("UNKNOWN", "unknown", "unknown", 0)

    bloque = None
    eslab = []
    fm_cache = {}

    for ln in t.splitlines():
        s = ln.strip()
        if s.startswith("=="):
            bloque = s.strip("= ")
            continue
        m = re.match(
            r"^\[lagunas-y-deuda-tecnica\] hilo/vigente/alta: (\d+)$", s
        )
        if not m:
            continue
        slug_total = int(m.group(1))

    # reconstruir por cadena real en disco (fuente canónica para la tabla)
    cadena = []
    total_lag = 0
    por_lag = {}
    for p in sorted(SRC.glob("*.md")):
        fm = load_fm(p.stem)
        if not fm:
            continue
        sec = (fm.get("secuencia") or [""])[0]
        if not sec:
            continue
        try:
            orden = int((fm.get("orden") or ["0"])[0])
        except ValueError:
            orden = 0
        # lagunas declaradas en el cuerpo
        b = p.read_bytes()
        tp = b[3:].decode("utf-8") if b.startswith(BOM) else b.decode("utf-8")
        tp = tp.lstrip("\ufeff")
        msecc = re.search(r"^## Lagunas\n(.*?)(?=^## |\Z)", tp, re.M | re.S)
        n_lag = 0
        if msecc:
            for ln2 in msecc.group(1).splitlines():
                if re.match(r"^\s*- \[[ xX]\]", ln2):
                    n_lag += 1
        cadena.append(
            {
                "slug": p.stem,
                "orden": orden,
                "secuencia": sec,
                "tipo": (fm.get("type") or ["?"])[0],
                "status": (fm.get("status") or ["?"])[0],
                "comp": (fm.get("completitud") or ["?"])[0],
                "n": n_lag,
            }
        )
        total_lag += n_lag

    cadena.sort(key=lambda r: r["orden"])

    cuerpo = []
    w = cuerpo.append

    w("## Resumen")
    w("")
    w(
        "Dashboard consolidado de **lagunas de validación** (checkpoints sin "
        "marcar en las `## Lagunas` de cada eslabón de la cadena "
        "[[hilo-propuesta-growth-partner]]) y de **deuda técnica** declarada "
        "en el vault. Es la entrada única de riesgo: **si querés saber qué "
        "falta para cerrar el proyecto, es acá.**"
    )
    w("")
    w("> **TL;DR:** **%d lagunas** en %d/%d eslabones de la cadena, "
      "sin pagar una sola deuda de infra — el hub [[hilo-propuesta-growth-partner]] "
      "sigue vigente como eslabón 0 y **ninguna laguna de derecho bloquea "
      "solamente el dashboard**." % (total_lag, sum(1 for r in cadena if r["n"]), len(cadena)))
    w("")

    w("## Cadena temporal")
    w("")
    w("| # | Eslabón | Tipo | Estado | Completitud | Lagunas |")
    w("|---|---------|------|--------|-------------|---------|")
    for r in cadena:
        link = "[[" + r["slug"] + "]]"
        w("| %d | %s | %s | %s | %s | %d |"
          % (r["orden"], link, r["tipo"], r["status"], r["comp"], r["n"]))
    w("")

    # --- bloque de lagunas por eslabón (desde el dump, ya parseado arriba)
    w("## Lagunas por eslabón")
    w("")
    act = None
    for ln in t.splitlines():
        s = ln.strip()
        m = re.match(
            r"^\[lagunas-y-deuda-tecnica\] hilo/vigente/alta: (\d+)$", s
        )
        if m:
            continue
        if s.startswith("- [ ] ### "):
            titulo = s[len("- [ ] ### "):].strip(" #")
            w("")
            w("### %s" % titulo)
            w("")
        elif s.startswith("- [ ] "):
            w("- [ ] %s" % s[len("- [ ] "):])
        elif s.startswith("\ufeff"):
            continue
    w("")

    w("## Deuda técnica")
    w("")

    w("## Fuentes")
    w("")
    w("- _Dashboard:_ generado por `scripts/extract_deuda.py` + `scripts/generar_pagina_deuda.py`.")
    w("- _Dump:_ `scripts/lagunas_deuda_dump.txt` (regenerable, no se edita a mano).")
    w("")

    fm = (
        "---\n"
        "type: hilo\n"
        "status: vigente\n"
        "completitud: alta\n"
        "aliases:\n"
        "  - dashboard de lagunas\n"
        "  - lagunas y deuda tecnica\n"
        "  - deuda tecnica del vault\n"
        "---\n"
    )
    texto = fm + "\n".join(cuerpo) + "\n"
    OUT.write_bytes(BOM + texto.encode("utf-8"))
    n = sum(1 for r in cadena if r["n"])
    print("OK  %s  (%d B · cadena=%d eslabones · %d con lagunas · %d lagunas)"
          % (OUT, OUT.stat().st_size, len(cadena), n, total_lag))


if __name__ == "__main__":
    main()
