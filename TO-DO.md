# Roadmap hacia v1.0

Este documento mantiene el roadmap de implementación del repositorio hasta alcanzar una primera versión estable `v1.0`.

No sustituye a [ARCHITECTURE.md](ARCHITECTURE.md). Las decisiones de diseño pertenecen allí.

El inventario de skills pertenece a [CATEGORIES.md](CATEGORIES.md).

---

# Estado

```text
Versión objetivo: v1.0
Estado actual: diseño / bootstrap
```

La versión `v1.0` debe representar un sistema suficientemente estable para:

```text
Author Skill
     ↓
Validate
     ↓
Register
     ↓
Discover
     ↓
Install
     ↓
Use
     ↓
Verify
     ↓
Update / Remove
```

sobre al menos una surface real.

---

# Fase 1 — Fundación del repositorio

Objetivo: establecer contratos y estructura antes de construir infraestructura significativa.

- [x] Crear estructura inicial del repositorio.
- [x] Incorporar `README.md`.
- [x] Incorporar `AGENTS.md`.
- [x] Incorporar `ARCHITECTURE.md`.
- [x] Incorporar `CATEGORIES.md`.
- [x] Incorporar `TO-DO.md`.
- [x] Definir `LICENSE`.
- [x] Crear `pyproject.toml`.
- [x] Establecer versión mínima soportada de Python.
- [x] Configurar entorno de desarrollo Python.
- [x] Configurar formatter/linter.
- [x] Configurar framework de testing.
- [x] Crear `.gitignore`.
- [x] Definir convenciones básicas de commits y releases.

### Gate

El repositorio puede clonarse y prepararse para desarrollo mediante un procedimiento documentado y reproducible.

---

# Fase 2 — Contrato de Skill

Objetivo: formalizar qué constituye una skill válida.

- [ ] Diseñar `skill.yaml` v1.
- [ ] Crear `schemas/skill.schema.json`.
- [ ] Definir campos obligatorios.
- [ ] Definir identidad `<category>/<skill-name>`.
- [ ] Definir reglas de versionado.
- [ ] Definir capabilities.
- [ ] Definir dependencias.
- [ ] Definir metadata de built-in tools.
- [ ] Definir requisitos runtime.
- [ ] Definir compatibilidad de plataformas.
- [ ] Definir política de recursos.
- [ ] Crear template recomendado de `SKILL.md`.
- [ ] Documentar reglas de authoring.

### Gate

Una skill puede describirse mediante un contrato estable y validarse independientemente de cualquier surface.

---

# Fase 3 — Skills de referencia

Objetivo: probar el modelo con capacidades reales antes de estabilizar infraestructura alrededor de él.

Construir inicialmente:

- [ ] `development/code-review`
- [ ] `memory/consolidate`
- [ ] `files/organize`

Estas tres skills deben probar diferentes aspectos del diseño.

### `development/code-review`

Validar:

- razonamiento intensivo;
- análisis de repositorios;
- resultados estructurados;
- referencias.

### `memory/consolidate`

Validar:

- provenance;
- relaciones;
- conflictos;
- confidence;
- propuestas de mutación;
- aprobación humana.

### `files/organize`

Validar:

- built-in Python tools;
- lectura/escritura filesystem;
- planificación;
- `--dry-run`;
- mutaciones;
