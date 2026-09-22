# Esquema del LLM Wiki (AGENTS.md)

Este archivo es el **schema** del wiki: define su estructura, convenciones y flujos de trabajo. Leelo completo antes de operar sobre el wiki. La idea general está en `docs/LLM_Wiki.md`.

## Estructura del vault

- `raw/` — fuentes originales. **Inmutables**: leerlas, nunca modificarlas.
  - `raw/assets/` — imágenes/adjuntos descargados localmente.
- `wiki/` — páginas generadas y mantenidas por el LLM.
  - `wiki/index.md` — catálogo orientado a contenido (todas las páginas, enlaces + resumen de 1 línea). Actualizar en cada ingest/query/lint.
  - `wiki/log.md` — registro cronológico append-only. Actualizar en cada operación.
  - `wiki/overview.md` — síntesis viva y punto de entrada.
  - `wiki/hoy.md` — estado de la semana y próxima acción concreta (punto de entrada diario, efímero: no acumula historial).
  - `wiki/sources/` — una página por fuente ingerida: resumen, puntos clave, posición en la síntesis.
  - `wiki/entities/` — entidades recurrentes (personas, organizaciones, lugares, productos).
  - `wiki/concepts/` — conceptos/ideas que cruzan varias fuentes.
- `templates/` — plantillas canónicas Obsidian (configurar el plugin Templates para que apunte acá).
- `apps/` — sandbox de código (repos git **independientes**, no trackeados por el git del vault). La wiki los referencia por ruta de archivo, no por wikilink.

## Convenciones de páginas

- **Toda hoja nace de una plantilla** en `templates/` (`nueva-nota` es el embudo de clasificación; luego se "promueve" a la plantilla del tipo elegido). Una hoja sin `type` y `status` definidos no se considera parte del esquema.
- Frontmatter obligatorio (habilita Dataview y filtros de deuda/completitud):
  - `type`: `concept | entity | source | project | tbd`.
  - `status`: `vigente | superada | pendiente-validacion | abierta` (estado del contenido).
  - `completitud`: `alta | media | baja` (qué tan completa está la info del tema).
  - `aliases`: siglas/nombres alternativos (desambiguar `sora`, `MOE`, `CETA`, etc.).
  - `source` y `origen` (solo `type: source`): `origen: documento | url | chat-usuario`. El chat aporta contexto **no citable** (validar/dimensionar en `## Lagunas`); `documento|url` es verificable contra `raw/`.
- **Secciones canónicas por tipo** (nombre fijo, no intercambiables — relegan el "Rol en el proyecto" a entidades y la "Relevancia para el proyecto" a conceptos):

| Tipo    | Secciones (en orden)                                                                                               |
| ------- | ------------------------------------------------------------------------------------------------------------------ |
| source  | `## Resumen` · `## Puntos clave` · `## Implicancias para el proyecto` · `## Posición en la síntesis` · `## Lagunas |
| entity  | `## Ficha` · `## Rol en el proyecto` · `## Puntos clave` · `## Fuentes`                                            |
| concept | `## Definición` · `## Relevancia para el proyecto` · `## Deuda técnica` · `## Fuentes`                             |
| project | `## Resumen` · `## Estado hoy` · `## Roadmap` · `## Decisiones abiertas` · `## Deuda técnica` · `## Fuentes`       |

- Toda página empieza con un bloque `> **TL;DR:**` tras el título (1–2 líneas).
- Las páginas de **infraestructura** del wiki (`index.md`, `overview.md`, `log.md`, `hoy.md`, `guia-de-navegacion.md`) no siguen el mapa por tipo: son navegación, no contenido. Sí conservan `status`/`completitud` en su frontmatter.
- Deuda/verificaciones pendientes: sección canónica de cada página (`## Deuda técnica` o `## Lagunas` con `- [ ]`). Las lagunas globales viven en `overview.md`.
- Usar wikilinks de Obsidian `[[...]]` para referencias cruzadas; enlazar un concepto la primera vez que aparece.
- Nombres de archivo: kebab-case (`deep-dive-llm.md`).
- Idioma: español, o el idioma de la fuente si pediste citarlo; si dudás, confirmá con el usuario.
- No inventar datos: si faltan, anotarlo como laguna en vez de completar.
- Clasificar una página bajo la categoría correcta y mantener `index.md` sincronizado.

## Flujos de trabajo

### Ingest
1. Leer la fuente en `raw/` (texto primero; imágenes después, por separado).
2. Discutir con el usuario los takeaways clave antes de escribir.
3. Escribir `wiki/sources/<slug>.md` con resumen y puntos clave.
4. Crear/actualizar páginas de entidades y conceptos que toque la fuente.
5. Actualizar `wiki/overview.md` si la síntesis cambia.
6. Actualizar `wiki/index.md`.
7. Agregar entrada al `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Título>`.
8. Hacer commit cuando el usuario lo pida (nunca por iniciativa propia).

### Query
1. Leer `wiki/index.md` para ubicar páginas relevantes.
2. Leer las páginas candidatas y sintetizar la respuesta con citas a `[[página]]`.
3. Si la respuesta es valiosa y persistente, proponer archivarla como página nueva.

### Lint
Auditar el wiki buscando: contradicciones entre páginas, claims viejos superados, páginas huérfanas, conceptos mencionados sin página propia, referencias faltantes, lagunas de datos. Sugerir preguntas nuevas y posibles fuentes.

### Actualización de `hoy.md`

`hoy.md` es un punto de entrada diario **efímero**: no acumula historial (el registro cronológico vive en `log.md`). No se actualiza por sí solo ni por cron; **se refresca por defecto en cada `ingest`/`query`/`lint` cuando el estado cambie** (decisión tomada, bloqueante nuevo, arranque de tarea, trabajo de saneamiento relevante), avisando al usuario en la respuesta. Al actualizarla: reemplazar `## Estado (fecha)` con la fecha vigente y el estado actual, y ajustar `## Próxima acción`. Si el usuario la solicita explícitamente, alinearla con lo vigente (cambios de la sesión, pendientes, commits recientes).

## Formato del log

Cada entrada empieza con el prefijo `## [YYYY-MM-DD] tipo | título` para poder parsearla con unix tools:

```bash
grep "^## \[" wiki/log.md | tail -5
```

Tipos: `ingest`, `query`, `lint`, `init`, `misc`.

## Convención de commits (Conventional Commits)

Los commits del vault siguen **Conventional Commits**: `tipo(scope): resumen`.

- **Tipos**: `feat` (nueva página/ingesta), `fix` (corrección), `docs` (contenido/navegación), `refactor` (reestructura), `chore` (mantenimiento, config), `style` (formato), `test` (scripts), `build`/`ci` (herramientas).
- **Scope** opcional y contextual al área afectada (p.ej. `feat(sources):`, `fix(entities):`, `docs(index):`).
- **Resumen**: en español, minúsculas, imperativo, <70 caracteres. Cuerpo o `BREAKING CHANGE:` solo si es necesario.
- El commit inicial de arranque usa el tipo `init` (excepción).
- Ejemplos:

```
feat(sources): ingerir resolución 206/2021 del MINEM
fix(entities): corregir precio del kit 5kW de Correos
docs(log): registrar lint de verificación de lagunas
```

## Herramientas auxiliares

- **`scripts/extract_pdf.py`** — extracción de texto de PDFs para ingest de fuentes (el modelo de la sesión no acepta PDFs como adjunto). Dependencia: `pypdf` (`py -m pip install --user pypdf`, requisitos en `scripts/requirements.txt`). En Windows invocar con el launcher: `py scripts/extract_pdf.py <archivo.pdf> [--max-pages N] [--max-chars N] [--out salida.txt] [--list]`.
- La salida de la extracción se descarta salvo que se genere `--out` en un directorio temporal; `raw/` nunca se modifica.