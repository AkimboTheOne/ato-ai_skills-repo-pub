# Contribuir

## Preparar el entorno

El repositorio requiere Python 3.12 o posterior y [uv](https://docs.astral.sh/uv/).
Después de clonar el repositorio, ejecuta:

```bash
uv sync --all-groups
```

No instales dependencias desde scripts del repositorio. `uv.lock` es la resolución
versionada de las dependencias de desarrollo.

## Validación local

Ejecuta estas comprobaciones antes de abrir una contribución:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

Para aplicar formato de forma explícita:

```bash
uv run ruff format .
```

No hay hooks pre-commit ni integración continua durante la fase bootstrap. Las
comprobaciones anteriores son el control local vigente.

## Convenciones de commits

Usa Conventional Commits:

```text
<type>(<scope>): <descripción imperativa>
```

Tipos habituales: `feat`, `fix`, `docs`, `test`, `build`, `ci`, `refactor` y `chore`.
El scope es opcional y debe describir un área estable, por ejemplo `docs` o `taxonomy`.

## Releases

Los releases son manuales hasta que exista automatización justificada. Antes de crear
un tag, valida el árbol de trabajo, ejecuta las comprobaciones locales y actualiza la
versión de proyecto cuando corresponda. Usa tags SemVer con prefijo `v`, por ejemplo
`v0.1.0`. La versión refleja compatibilidad funcional, no cada cambio de Git.

## Autoría ATO e importaciones

Las skills propias deben usar la convención editorial `ato_` en su carpeta,
`ato-` en su ID, `ATO ` en su nombre visible y `$ATO ` en etiquetas de integración.
Por ejemplo, `skills/development/ato_code-review/` corresponde a
`development/ato-code-review`, `ATO Code Review` y `$ATO Code Review`.

Las fuentes de terceros se incorporan exclusivamente mediante submódulos Git bajo
`imports/<upstream-owner>/<repository>/`. Antes de añadir o actualizar una importación:

1. selecciona un commit SHA completo; no uses ramas, tags sin fijar ni
   `git submodule update --remote`;
2. revisa manualmente licencia, avisos, seguridad y compatibilidad;
3. conserva la licencia y avisos upstream sin atribuir el contenido a ATO;
4. actualiza el gitlink, el sidecar `.provenance.md` y `imports/CATALOG.md` en el
   mismo cambio.

No edites contenido dentro de un submódulo. Las correcciones deben realizarse upstream
o convertirse explícitamente en una nueva skill propia ATO.

## Límites del bootstrap

No agregues todavía `skillctl`, schemas, registry, adapters, instalaciones ni una
skill concreta. Esos componentes pertenecen a fases posteriores del roadmap y deben
partir de contratos estables.
