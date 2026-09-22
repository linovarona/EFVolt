#!/usr/bin/env python3
"""Extraccion de texto de PDFs para el LLM Wiki (reutilizable).

Dependencias: pypdf (requisitos en scripts/requirements.txt).

Uso:
  py scripts/extract_pdf.py <archivo.pdf> [mas.pdf ...] [opciones]

Opciones:
  --max-pages N    Procesar solo las primeras N paginas por archivo.
  --max-chars N    Truncar la salida de cada pagina a N caracteres.
  --out ARCHIVO    Escribir la salida a ARCHIVO en lugar de stdout.
  --list           Solo listar metadata de cada PDF (titulo, paginas).

Ejemplos:
  py scripts/extract_pdf.py raw/prg_Mavlink_For_Dummies_Part1_v.1.1.pdf
  py scripts/extract_pdf.py foo.pdf --max-pages 5 --max-chars 4000
"""

import argparse
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extrae texto de PDFs (adaptado del pipeline node/pdf-parse)."
    )
    ap.add_argument("files", nargs="+", help="archivos PDF")
    ap.add_argument("--max-pages", type=int, default=0,
                    help="procesar solo las primeras N paginas por archivo (0 = todas)")
    ap.add_argument("--max-chars", type=int, default=0,
                    help="truncar la salida de cada pagina a N caracteres (0 = sin limite)")
    ap.add_argument("--out", metavar="ARCHIVO",
                    help="escribir la salida a ARCHIVO (default: stdout)")
    ap.add_argument("--list", action="store_true",
                    help="solo mostrar metadata de cada PDF (no extrae texto)")
    args = ap.parse_args()

    from pypdf import PdfReader

    sink = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    try:
        for path in args.files:
            reader = PdfReader(path)
            meta = reader.metadata or {}
            total = len(reader.pages)
            title = (meta.get("/Title") or "").strip() or "(sin titulo)"
            header = f"{'=' * 78}\n==== {path} — {total} paginas — titulo: {title}\n{'=' * 78}\n"
            print(header, file=sink)
            if args.list:
                continue
            pages = reader.pages if not args.max_pages else reader.pages[: args.max_pages]
            for i, page in enumerate(pages, 1):
                text = page.extract_text() or ""
                if args.max_chars:
                    text = text[: args.max_chars]
                print(f"\n---- [pagina {i}/{total}] ----\n{text}", file=sink)
    finally:
        if sink is not sys.stdout:
            sink.close()


if __name__ == "__main__":
    main()