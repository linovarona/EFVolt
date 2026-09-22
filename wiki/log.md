---
status: vigente
completitud: alta
---

# Log

Registro cronológico append-only de operaciones. Parseable con: `grep "^## \[" wiki/log.md | tail -5`.

## [2026-09-19] init | Creación de la estructura base del wiki

Se creó la estructura del vault según `AGENTS.md`:

- `raw/` (+ `raw/assets/`) — fuentes originales, inmutables.
- `wiki/` — `index.md`, `log.md`, `overview.md`, `hoy.md`, `guia-de-navegacion.md`, `sources/`, `entities/`, `concepts/`.
- `templates/` — `nueva-nota.md` y plantillas por tipo (`source`, `entity`, `concept`, `project`).
- `apps/` — sandbox de código (repos git independientes).

## [2026-09-19] ingest | Plan de acción: club de compra de sistemas solares en Cuba

- Se movió `docs/chat_club_de_compra.md` → `raw/chat_club_de_compra.md`.
- Páginas: `sources/plan-club-de-compra-solar-cuba` · `club-de-compra-solar` (project) · entidades: `cimex`, `trd`, `tiendas-caribe`, `copextel`, `correos-de-cuba`, `ecensol`, `unee`, `geComex`, `kits-solares` · conceptos: `club-de-compra`, `importacion-sin-aranceles`, `costo-ddp`.
- Actualizados: `index.md`, `overview.md`, `hoy.md`.
- Nota: primera entrada del log; se dejó la entrada de `init` como la más antigua y esta como la más reciente (orden cronológico del archivo: init → ingest).

## [2026-09-19] misc | Adopción de Conventional Commits en AGENTS.md

- Se agregó la sección `## Convención de commits (Conventional Commits)` al `AGENTS.md` (tipos, scope, resumen en español, `init` como excepción para el commit inicial).

## [2026-09-20] ingest | Ingesta de 11 fuentes: oferta, due diligence, modelo financiero y canales

- Se movieron 11 archivos de `docs/` a `raw/` (2 PDF extraídos con `scripts/extract_pdf.py`: `doc_Oferta_Kit_SFV.pdf`, `doc_Oferta_Mayorista.pdf`). `docs/` quedó vacía.
- Páginas nuevas en `sources/`: `chat-analisis-oferta`, `oferta-mayorista-paneles-hua-laien`, `chat-analisis-critico`, `carta-verificacion-proveedor`, `modelo-financiero-12m`, `modelo-financiero-24m`, `chat-analisis-propuesta`, `propuesta-growth-partner-v1`, `propuesta-growth-partner-v2`, `opinion-y-feedback-del-club`, `oferta-kit-sfv-hua-laien`.
- Entidades nuevas: `habana-agro-surl`, `hua-laien-shanghai`, `sunevo-sunark`, `sumai-sa`. Actualizadas: `cimex`, `trd`, `tiendas-caribe`, `copextel`, `correos-de-cuba`, `ecensol`, `unee`, `geComex`, `kits-solares`.
- Conceptos nuevos: `due-diligence-proveedor`, `vias-de-pago`. Actualizados: `club-de-compra`, `importacion-sin-aranceles`, `costo-ddp`.
- Actualizados: `index.md`, `overview.md`, `hoy.md`.
- **Takeaway central:** la tesis pasó de "precio" a "confianza" — la palanca de desplazamiento es la [[carta-verificacion-proveedor]] (due diligence excluyente antes de pagar 100% anticipado).
## [2026-09-20] lint | Verificaci?n de integridad del wiki (38 p?ginas)

Lint completo de la ingesta 2 (script `scripts/lint_wiki.py`). Resultado: **0 errores reales pendientes**.

- Frontmatter incompleto (7): status `pendiente-validacion` = correcto por disee&#xF1;o (6 fuentes chat no citables + 2 entidades bajo due diligence pendiente [[carta-verificacion-proveedor]]).
- Secciones can?nicas faltantes (1): `chat-analisis-dos-modelos` no ten?a `## Posici?n en la s?ntesis` ? **agregada**.
- Wikilinks rotos (2): dobles corchetes `[[[[...]]]]` por error de escritura en `chat-analisis-dos-modelos` ? **corregidos**.
- Falso positivo (1): `guia-de-navegacion.md:32` documenta la sintaxis `[[...]]` con un literal, no es un link.
- Orfan??a: sin hu?rfanos bloqueantes (infraestructura navegable por [[index]]).
