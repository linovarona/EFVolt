---
status: vigente
completitud: alta
---

# Guía de navegación

> **TL;DR:** Cómo está organizado el vault y por dónde entrar según lo que quieras hacer.

## Estructura

| Carpeta | Contenido | Rol |
|---|---|---|
| `raw/` | Fuentes originales (inmutables) | Fuente de verdad, nunca se modifica |
| `wiki/` | Páginas generadas y mantenidas por el LLM | Capa de conocimiento |
| `templates/` | Plantillas canónicas Obsidian (plugin Templates) | Origen de toda hoja nueva |
| `apps/` | Sandbox de código (repos git independientes) | Experimentos y herramientas |

## Puntos de entrada

- **Empiezo el día / quiero saber qué sigue:** [[hoy]]
- **Quiero la vista general de la síntesis:** [[overview]]
- **Busco una página puntual:** [[index]]
- **Quiero ver el historial de operaciones:** [[log]]

## Convenciones rápidas

- Toda hoja nace de una plantilla en `templates/` (`nueva-nota` es el embudo; luego se promueve al tipo elegido).
- Frontmatter obligatorio: `type`, `status`, `completitud`, `aliases` (y `source`/`origen` en fuentes).
- Secciones canónicas por tipo (ver `AGENTS.md`): `source`, `entity`, `concept`, `project`.
- Deuda y verificaciones pendientes viven en `## Deuda técnica` o `## Lagunas` con `- [ ]`.
- Referencias cruzadas con wikilinks `[[...]]`.
- Nombres de archivo en kebab-case.