# Fuentes importadas

Este directorio contiene repositorios de terceros consumidos por el proyecto. Una
importación no es una skill propia ATO ni sustituye la definición canónica upstream.

## Estructura

```text
imports/
├── CATALOG.md
└── <upstream-owner>/
    ├── <repository>/                 # submódulo Git
    └── <repository>.provenance.md    # evidencia mantenida por este repositorio
```

El submódulo debe fijarse en un commit SHA completo. `.gitmodules` y el gitlink del
árbol principal son la fuente técnica de URL y commit; no se permiten ramas flotantes
ni `git submodule update --remote`.

## Procedencia

Cada sidecar usa front matter con estas claves obligatorias:

```text
---
import_id: <upstream-owner>/<repository>
upstream_url: <URL canónica>
commit: <SHA completo de 40 caracteres>
upstream_ref: <tag o rama informativa>
license: <identificador SPDX o referencia clara>
reviewed_by: <responsable>
reviewed_on: <YYYY-MM-DD>
---
```

El cuerpo debe explicar los avisos de licencia preservados y el alcance exacto del
contenido utilizado. El catálogo añade el racional editorial y debe coincidir con el
sidecar en identificador, URL, commit y licencia.

Antes de importar o actualizar, revisa licencia, avisos, seguridad y compatibilidad.
No modifiques el submódulo: contribuye upstream o crea una nueva skill propia ATO si
existe una necesidad independiente.
