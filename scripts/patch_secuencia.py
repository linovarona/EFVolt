#!/usr/bin/env python3
"""patch_secuencia.py — marca la cadena temporal en las 13 fuentes del vault
club-compra (BOM-safe, idempotente, no re-marca lo que ya tiene).

Cadena (orden 1..13): plan-club-de-compra-solar-cuba · propuesta-growth-partner-v1
· opinion-y-feedback-del-club · chat-analisis-critico · chat-analisis-oferta ·
oferta-mayorista-paneles-hua-laien · oferta-kit-sfv-hua-laien ·
carta-verificacion-proveedor · propuesta-growth-partner-v2 · modelo-financiero-12m
· modelo-financiero-24m · chat-analisis-dos-modelos · propuesta-growth-partner-v3

Uso: py scripts/patch_secuencia.py   (desde la raíz del vault)
"""
import pathlib
import re
import sys

BOM = b"\xef\xbb\xbf"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "wiki" / "sources"

CADENA = [
    ("plan-club-de-compra-solar-cuba", 1),
    ("propuesta-growth-partner-v1", 2),
    ("opinion-y-feedback-del-club", 3),
    ("chat-analisis-critico", 4),
    ("chat-analisis-oferta", 5),
    ("oferta-mayorista-paneles-hua-laien", 6),
    ("oferta-kit-sfv-hua-laien", 7),
    ("carta-verificacion-proveedor", 8),
    ("propuesta-growth-partner-v2", 9),
    ("modelo-financiero-12m", 10),
    ("modelo-financiero-24m", 11),
    ("chat-analisis-dos-modelos", 12),
    ("propuesta-growth-partner-v3", 13),
]


def procesar(p, orden):
    """Inserta `secuencia`+`orden` tras `status:` (si falta) y devuelve
    ('OK'|'SALTO'|'FALLA') + razón."""
    b = SRC.joinpath(p + ".md").read_bytes()
    bom = b.startswith(BOM)
    t = (b[3:].decode("utf-8") if bom else b.decode("utf-8")).lstrip("\ufeff")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        return "SIN-FRONTMATTER", p
    fm = m.group(1)
    if re.search(r"(?m)^secuencia:\s*", fm):
        return "SALTO", p
    if not re.search(r"(?m)^status:\s*", fm):
        return "SIN-STATUS", p
    # insertar tras la línea `status: ...` (preservando el resto)
    lines = fm.split("\n")
    out = []
    insertado = False
    for ln in lines:
        out.append(ln)
        if not insertado and re.match(r"^status:\s*\S+", ln):
            out.append("secuencia: hilo-propuesta-growth-partner")
            out.append("orden: %d" % orden)
            insertado = True
    if not insertado:
        return "SIN-STATUS-LINEA", p
    fm2 = "\n".join(out)
    t2 = "---\n" + fm2 + "\n---\n" + t[m.end():]
    SRC.joinpath(p + ".md").write_bytes((BOM + t2.encode("utf-8")) if bom else t2.encode("utf-8"))
    return "OK", p


def main():
    total_ok = 0
    total_salto = 0
    for p, orden in CADENA:
        r, slug = procesar(p, orden)
        if r == "OK":
            total_ok += 1
        elif r == "SALTO":
            total_salto += 1
        print("  %-9s %s (orden=%d)" % (r, slug, orden))
    print("== resumen: OK=%d SALTO=%d (13 total) ==" % (total_ok, total_salto))
    return 0 if total_ok + total_salto == 13 else 1


if __name__ == "__main__":
    sys.exit(main())
