# EFVolt - Club de Energía Fotovoltaica

Wiki colaborativo para la gestión y documentación del club de compra de kits solares fotovoltaicos en Cuba.

## 📋 Descripción

Este repositorio contiene la base de conocimiento del **EFVolt**, un club de energía fotovoltaica que facilita la importación y distribución de kits solares en Cuba mediante compras colectivas. El wiki documenta entidades, conceptos, fuentes y el estado del proyecto.

## 🗂️ Estructura del Repositorio

```
├── raw/                    # Fuentes originales (documentos, chats, PDFs) - Inmutables
│   └── assets/             # Imágenes y adjuntos locales
├── wiki/                   # Páginas generadas y mantenidas
│   ├── index.md            # Catálogo de todas las páginas
│   ├── log.md              # Registro cronológico de operaciones
│   ├── overview.md         # Síntesis del proyecto
│   ├── hoy.md              # Estado actual y próxima acción
│   ├── concepts/           # Conceptos transversales
│   └── entities/           # Entidades (organizaciones, productos, etc.)
├── templates/              # Plantillas Obsidian para nuevas notas
├── scripts/                # Herramientas de procesamiento
└── AGENTS.md               # Schema y convenciones del wiki
```

## 📁 Contenido por Directorio

### `raw/` - Fuentes Originales
Documentación fuente sin modificar:
- Ofertas de proveedores
- Chats de análisis y discusiones
- Documentación legal y regulatoria
- Información financiera

### `wiki/` - Base de Conocimiento

#### Concepts (`wiki/concepts/`)
- [[club-de-compra]] - Modelo de compra colectiva
- [[costo-ddp]] - Costo Delivery Duty Paid
- [[due-diligence-proveedor]] - Verificación de proveedores
- [[importacion-sin-aranceles]] - Marco regulatorio de importación
- [[vias-de-pago]] - Mecanismos de pago disponibles

#### Entities (`wiki/entities/`)
- **Organizaciones**: CIMEX, COPXTEL, Correos de Cuba, Ecensol, SUMAI SA, Tiendas Caribe
- **Proveedores**: Hua Laien (Shanghai), Sunevo/Sunark
- **Productos**: Kits solares de diferentes capacidades
- **Instituciones**: TRD, UNEE

### `templates/` - Plantillas
Plantillas canónicas para Obsidian:
- `nueva-nota.md` - Embudo de clasificación inicial
- `template-concept.md` - Para conceptos
- `template-entity.md` - Para entidades
- `template-project.md` - Para proyectos
- `template-source.md` - Para fuentes documentales

### `scripts/` - Herramientas
- `extract_pdf.py` - Extracción de texto de PDFs
- `lint_wiki.py` - Auditoría de consistencia del wiki
- `generar_pagina_deuda.py` - Generación de reportes de deuda
- Otros scripts de procesamiento

## 🔧 Requisitos y Herramientas

### Dependencias Python
```bash
pip install pypdf  # Para extracción de PDFs
```

Ver `scripts/requirements.txt` para el listado completo.

### Obsidian
Este vault está diseñado para usarse con [Obsidian](https://obsidian.md/). Configurar:
- Plugin **Templates**: apuntar a `templates/`
- Plugin **Dataview**: habilitado para consultas

## 📝 Convenciones

### Frontmatter Obligatorio
Todas las páginas deben incluir:
```yaml
---
type: concept | entity | source | project | tbd
status: vigente | superada | pendiente-validacion | abierta
completitud: alta | media | baja
aliases: []  # Nombres alternativos
---
```

### Nomenclatura
- Archivos: kebab-case (`nombre-de-archivo.md`)
- Referencias: wikilinks de Obsidian `[[nombre-pagina]]`
- Idioma: español

### Tipos de Página y Secciones

| Tipo    | Secciones Canónicas                                                                 |
| ------- | ----------------------------------------------------------------------------------- |
| source  | Resumen · Puntos clave · Implicancias · Posición en síntesis · Lagunas              |
| entity  | Ficha · Rol en el proyecto · Puntos clave · Fuentes                                 |
| concept | Definición · Relevancia · Deuda técnica · Fuentes                                   |
| project | Resumen · Estado hoy · Roadmap · Decisiones abiertas · Deuda técnica · Fuentes      |

## 🔄 Flujos de Trabajo

### Ingest (Ingesta de Nueva Fuente)
1. Leer fuente en `raw/`
2. Discutir takeaways clave
3. Crear `wiki/sources/<slug>.md`
4. Actualizar entidades y conceptos relacionados
5. Actualizar `overview.md` si corresponde
6. Actualizar `index.md`
7. Registrar en `log.md`

### Query (Consulta)
1. Consultar `index.md` para ubicar páginas relevantes
2. Sintetizar respuesta con citas
3. Proponer archivar como página nueva si es valioso

### Lint (Auditoría)
- Detectar contradicciones entre páginas
- Identificar claims obsoletos
- Encontrar páginas huérfanas o conceptos sin página
- Sugerir verificaciones pendientes

## 📊 Estado del Proyecto

Para el estado actual y próximas acciones, consultar:
- [[hoy]] - Punto de entrada diario
- [[overview]] - Síntesis general del proyecto
- [[index]] - Catálogo completo de contenido

## 🤝 Contribución

Este wiki sigue el esquema definido en `AGENTS.md`. Antes de contribuir:
1. Leer `AGENTS.md` completo
2. Usar las plantillas apropiadas
3. Mantener `index.md` sincronizado
4. Registrar cambios en `log.md`

## 📄 Licencia

[Información de licencia si aplica]

---

**EFVolt** - Facilitando el acceso a energía solar en Cuba mediante compras colectivas.
