---
type: hilo
status: vigente
completitud: alta
aliases:
  - dashboard de lagunas
  - lagunas y deuda tecnica
  - deuda tecnica del vault
---

# Lagunas y deuda técnica

> **TL;DR:** Dashboard consolidado, verificado contra disco, de las **lagunas de validación** (checklist sin marcar en `## Lagunas`) y la **deuda técnica** declarada (`## Deuda técnica`) de las páginas tipo `hilo` del vault. Total: **4 lagunas** y **0 ítems de deuda técnica**.

## Resumen

Esta página se regenera con `py scripts/generar_lagunas_deuda.py` y consolida, en orden de cadena temporal, qué **falta para validar** y qué **quedó pendiente** en cada eslabón del hilo [[hilo-propuesta-growth-partner]]. No reemplaza a las fuentes: enlaza a cada una para que el detalle viva en su lugar canónico.

## Cadena temporal

| Eslabón | Status | Completitud | Lagunas | Deuda técnica |
|---------|--------|-------------|---------|---------------|
| [[hilo-propuesta-growth-partner]] | vigente | alta | 4 | 0 |
| [[lagunas-y-deuda-tecnica]] | vigente | alta | 0 | 0 |

## Lagunas

### [[hilo-propuesta-growth-partner]] (4)
- [ ] Reconciliar el kit de 3 kW del PDF (1 batería 25.6V/2.56kWh) con el que describe el análisis (2 baterías 12V/100Ah) — verificar la ficha real a despachar. *[depende de oferta-kit-sfv-hua-laien]*
- [ ] Validar el TC de referencia (300 CUP/USD) y el tipo de cambio implícito en las ofertas. *[depende de oferta-mayorista-paneles-hua-laien y modelo-financiero-*]*
- [ ] Confirmar respuesta del proveedor a la carta de verificación (no hay registro en raw/). *[depende de carta-verificacion-proveedor]*
- [ ] Confirmar si el chat de análisis de la propuesta (fuera de cadena) debería entrar a la secuencia. *[laguna del hub]*

### [[lagunas-y-deuda-tecnica]] (0)
- Nada abierto.


## Deuda técnica

## Fuentes

- _Generado por_ `scripts/generar_lagunas_deuda.py` (BOM-safe, idempotente).
- _Vault:_ [[index]].
