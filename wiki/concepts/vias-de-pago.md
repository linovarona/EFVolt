---
type: concept
status: vigente
completitud: media
aliases:
  - vías de pago
  - vías de cobro
  - via a divisas
  - via b cup
---

# Vías de pago

> **TL;DR:** Dos mecanismos de cobro del club: **Vía A en divisas (USD)** y **Vía B en CUP**, con comisión referenciada al precio DDP. La mezcla 60/40 y el riesgo de cambio condicionan la viabilidad del modelo.

## Definición

El club define cómo cobra a sus miembros y cómo recibe su comisión del proveedor. Distingue:

- **Vía A (divisas):** pagos en MLC/USD, típicamente contra verificación de pago del cliente y salida del pedido del proveedor. La comisión se cobra en el exterior para mitigar el riesgo de retención burocrática en Cuba.
- **Vía B (CUP):** pago en pesos cubanos a yuanes ajustados por el club o el proveedor. Más frágil: depende del tipo de cambio informal y de la política cambiaria.

## Relevancia para el proyecto

- La **palanca central no es el precio sino la confianza** en el cobro: la [[carta-verificacion-proveedor]] es condición previa a cualquier pago del 100% anticipado ([[due-diligence-proveedor]]).
- El modelo financiero asume una mezcla realista de **60% Vía A / 40% Vía B**; si la Vía B muere (devaluación), el escenario base se estresa.
- Comisión típica **8% sobre precio USD**, cobrada **100% contra verificación de pago** y salida de pedido, sin esperar la entrega final en Cuba.

## Deuda técnica

- [ ] Validar el tipo de cambio CUP/USD que usa cada vía y su sensibilidad.
- [ ] Definir quién retiene y transfiere la comisión (club vs proveedor) y en qué lote.
- [ ] Estresar el modelo asumiendo 90% Vía A (poca red de remesas en el exterior).

## Fuentes

- [[chat-analisis-dos-modelos]]
- [[modelo-financiero-12m]]
- [[modelo-financiero-24m]]
- [[propuesta-growth-partner-v3]]
