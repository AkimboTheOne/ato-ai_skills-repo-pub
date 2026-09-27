# Catálogo de importaciones

Este catálogo es el inventario editorial de repositorios upstream. Explica qué se
importa, por qué se conserva y sus límites; no es un registry ni reemplaza el gitlink
del submódulo.

## Inventario

| Importación | Estado | URL upstream | Commit fijado | Licencia | Capacidades aprovechadas | Racional | Límites de uso |
|---|---|---|---|---|---|---|---|

No hay importaciones registradas todavía.

## Mantenimiento

Los estados permitidos son:

- `propuesto`: evaluado, pero aún no incorporado como submódulo ni sidecar;
- `activo`: submódulo fijado y disponible para el alcance documentado;
- `retirado`: sidecar conservado como registro histórico, sin uso nuevo.

Una fila `activo` representa exactamente un sidecar
`imports/<upstream-owner>/<repository>.provenance.md` y un submódulo del mismo ID.
Una fila `retirado` conserva su sidecar. La URL, el commit y la licencia de cada fila
con sidecar deben coincidir con él. El racional debe justificar por qué se importa en
vez de desarrollar una capability propia, y los límites deben indicar explícitamente
qué contenido o usos no adopta el repositorio.
