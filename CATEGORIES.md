# Categorías de Skills

Este documento es la fuente de verdad para la taxonomía del repositorio. Una categoría
agrupa capacidades reutilizables; no representa un agente, workflow, proyecto ni
surface de ejecución.

## Categorías raíz

| Categoría | Propósito | Ejemplos planificados |
|---|---|---|
| `development` | Ingeniería de software, calidad y mantenimiento de código. | `development/code-review` |
| `memory` | Consolidación y mantenimiento gobernado de conocimiento persistente. | `memory/consolidate` |
| `files` | Análisis y operaciones seguras sobre colecciones de archivos. | `files/organize` |
| `research` | Investigación, validación y síntesis de fuentes. | — |
| `knowledge` | Clasificación, estructuración y recuperación de conocimiento. | — |
| `operations` | Diagnóstico y análisis de sistemas y operaciones. | — |

## Reglas de clasificación

- El identificador de una skill tiene la forma `<category>/<skill-name>`.
- Categorías y nombres usan minúsculas ASCII; los nombres compuestos se separan con
  guiones.
- Selecciona la categoría según la capacidad principal, no según el agente, proyecto,
  modelo, surface ni una herramienta incidental.
- Una skill que combine varias capacidades debe mantener una responsabilidad coherente.
  Si sus responsabilidades dejan de ser coherentes, divídela o coordínala desde un
  workflow externo.
- Una categoría se materializa bajo `skills/<category>/` solamente al crear su primera
  skill canónica; no se versionan directorios vacíos.

## Convención de autoría ATO

Una skill propia usa un prefijo editorial sin alterar la gramática de su identificador:

| Elemento | Convención | Ejemplo |
|---|---|---|
| Ruta | `skills/<category>/ato_<slug>/` | `skills/development/ato_code-review/` |
| ID | `<category>/ato-<slug>` | `development/ato-code-review` |
| Nombre visible | `ATO <título de slug>` | `ATO Code Review` |
| Etiqueta de integración | `$ATO <título de slug>` | `$ATO Code Review` |

La etiqueta se utiliza solamente en CLIs, IDEs o adapters cuando esas integraciones
existan. El contenido importado de terceros no usa la marca ATO y se inventaría en
[`imports/CATALOG.md`](imports/CATALOG.md).

## Estado del inventario

Las siguientes skills son referencias de diseño planificadas, no implementaciones:

- `development/code-review`
- `memory/consolidate`
- `files/organize`

La incorporación de una skill requiere completar primero el contrato de metadata y
validación definidos en el roadmap.
