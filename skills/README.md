# Skills canónicas

Este directorio es la fuente canónica de las skills reutilizables del repositorio.
Las instalaciones, caches, índices, sesiones, credenciales y otros estados runtime no
pertenecen aquí.

No se crean categorías ni estructuras de skill vacías. Cuando el contrato de skill
esté definido y se incorpore una capacidad real, créala en:

```text
skills/<category>/<skill-name>/
```

La categoría debe existir en [CATEGORIES.md](../CATEGORIES.md). Una skill sencilla
podrá contener solamente `SKILL.md` y `skill.yaml`; los recursos adicionales se
añaden únicamente cuando la capacidad los necesita.

Las skills propias siguen la convención editorial `ato_` en la carpeta y `ato-` en el
ID. Por ejemplo, `skills/development/ato_code-review/` expone el ID
`development/ato-code-review`, el nombre `ATO Code Review` y la etiqueta de
integración `$ATO Code Review`. No coloques contenido de terceros en este directorio:
usa [imports/](../imports/README.md) para conservar su procedencia upstream.

En esta fase no hay skills implementadas.
