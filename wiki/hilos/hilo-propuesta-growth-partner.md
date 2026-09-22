---
type: hilo
status: vigente
completitud: alta
aliases:
  - hilo growth partner
  - cadena temporal growth partner
  - hilo-propuesta-growth-partner
---

# Hilo: Propuesta Growth Partner (V1 → V3)

> **TL;DR:** Trece eslabones marcan la evolución de una oportunidad de **club de compra solar en Cuba**: nace como plan de club, se formaliza en propuestas Growth Partner (V1→V3), se contrasta con ofertas reales (mayorista y kit SFV de Hua Laien) y due diligence de proveedor, y se cierra con dos modelos financieros (12 y 24 meses) que el club debe decidir. La cadena vive como `secuencia: hilo-propuesta-growth-partner` + `orden: N` en el frontmatter de cada fuente.

## Resumen

La temporalidad del vault se modela con un **hub `type: hilo`** y un **orden de eslabones** en el frontmatter de las fuentes (`secuencia` + `orden`). Esta página es el hub de la cadena **propuesta Growth Partner**: agrupa los 13 eslabones en orden y señala las lagunas que quedan para cerrar la validación del proyecto.

## Cadena temporal

| # | Eslabón | Qué aporta a la cadena |
|---|---------|------------------------|
| 1 | [[plan-club-de-compra-solar-cuba]] | La tesis fundacional: club de compra para paneles solares en Cuba. |
| 2 | [[propuesta-growth-partner-v1]] | Primera propuesta formal de Growth Partner (v1). |
| 3 | [[opinion-y-feedback-del-club]] | Feedback del club: dónde falla la propuesta. |
| 4 | [[chat-analisis-critico]] | Análisis crítico: riesgos y puntos ciegos de la oportunidad. |
| 5 | [[chat-analisis-oferta]] | Contraste de la oferta con la oportunidad. |
| 6 | [[oferta-mayorista-paneles-hua-laien]] | Oferta mayorista de paneles de Hua Laien. |
| 7 | [[oferta-kit-sfv-hua-laien]] | Kit SFV concreto (con BOM del proyecto). |
| 8 | [[carta-verificacion-proveedor]] | Due diligence del proveedor: carta de verificación. |
| 9 | [[propuesta-growth-partner-v2]] | Segunda iteración de la propuesta (v2). |
| 10 | [[modelo-financiero-12m]] | Modelo financiero a 12 meses. |
| 11 | [[modelo-financiero-24m]] | Modelo financiero a 24 meses. |
| 12 | [[chat-analisis-dos-modelos]] | Análisis comparado de los dos modelos. |
| 13 | [[propuesta-growth-partner-v3]] | Propuesta final (v3), integra lo aprendido. |

## Lagunas

- [ ] Reconciliar el kit de 3 kW del PDF (1 batería 25.6V/2.56kWh) con el que describe el análisis (2 baterías 12V/100Ah) — verificar la ficha real a despachar. *[depende de oferta-kit-sfv-hua-laien]*
- [ ] Validar el TC de referencia (300 CUP/USD) y el tipo de cambio implícito en las ofertas. *[depende de oferta-mayorista-paneles-hua-laien y modelo-financiero-*]*
- [ ] Confirmar respuesta del proveedor a la carta de verificación (no hay registro en raw/). *[depende de carta-verificacion-proveedor]*
- [ ] Confirmar si el chat de análisis de la propuesta (fuera de cadena) debería entrar a la secuencia. *[laguna del hub]*
