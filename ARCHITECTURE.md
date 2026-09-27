# Arquitectura

## 1. Propósito

Este documento define la arquitectura del repositorio de reusable agent skills, sus límites y las principales decisiones que deben preservarse durante su evolución.

El objetivo es permitir que una capacidad sea:

```text
AUTHOR
   ↓
CANONICAL SKILL
   ↓
VALIDATE
   ↓
VERSION
   ↓
REGISTRY
   ↓
RESOLVE
   ↓
INSTALL / RENDER
   ↓
┌─────────┬──────────┬──────────────┐
▼         ▼          ▼
Codex   OpenCode   Agent Runtime
```

La capacidad debe mantener su identidad independientemente de la superficie donde sea desplegada.

---

# 2. Componentes

## Canonical Skill

Unidad fundamental del sistema.

Contiene:

```text
instructions
metadata
resources
optional deterministic tools
tests
```

La definición canónica reside bajo:

```text
skills/
```

---

## Registry

Catálogo procesable de skills disponibles.

Responsabilidades:

- discovery;
- identificación;
- ubicación;
- metadata;
- versionado.

El registry debería eventualmente generarse a partir de las skills canónicas para evitar fuentes de verdad duplicadas.

---

## Resolver

Determina cómo satisfacer una solicitud de instalación.

Puede considerar:

- skill;
- versión;
- dependencias;
- compatibilidad;
- target;
- scope.

No debe ejecutar lógica específica de una surface directamente.

---

## Installer

Coordina:

```text
resolve
validate
prepare
install
record state
verify
```

No debe conocer detalles internos de cada target.

---

## Adapter

Implementa el comportamiento específico de una surface.

Ejemplos:

```text
CodexAdapter
OpenCodeAdapter
AgentsSDKAdapter
```

Responsabilidades posibles:

- descubrir instalación;
- determinar rutas;
- validar compatibilidad;
- renderizar;
- instalar;
- verificar;
- remover.

---

# 3. Flujo de instalación

```text
Canonical Skill
      │
      ▼
   Registry
      │
      ▼
   Resolver
      │
      ▼
  Installer
      │
      ▼
Target Adapter
      │
      ▼
Installed Skill
```

El resultado instalado es derivado.

Nunca reemplaza la definición canónica.

---

# 4. Estrategias de instalación

Los adapters pueden implementar diferentes estrategias.

## Copy

```text
canonical → copy → target
```

Adecuado cuando la surface consume archivos directamente.

## Symlink

```text
target → canonical
```

Útil en desarrollo local cuando la surface lo permite.

## Render

```text
canonical
    ↓
 adapter
    ↓
target-specific representation
```

Necesario cuando una surface requiere una representación diferente.

El modelo debe permitir incorporar otras estrategias sin modificar la definición de las skills.

---

# 5. Scope

Las instalaciones podrán diferenciar scopes como:

```text
user
project
workspace
agent
```

La semántica concreta pertenece al adapter porque cada surface puede interpretar los scopes de forma distinta.

---

# 6. Modelo de una Skill

Identidad:

```text
<category>/<skill-name>
```

Ejemplo:

```text
files/organize
```

Estructura:

```text
files/organize/
├── SKILL.md
├── skill.yaml
├── tools/
├── references/
├── templates/
├── schemas/
├── examples/
└── tests/
```

`SKILL.md` es el contrato semántico.

`skill.yaml` es el contrato procesable.

### 6.1 Autoría y procedencia

El repositorio distingue dos clases de contenido:

- **Skill propia ATO:** definición canónica mantenida bajo `skills/`. Usa la ruta
  `skills/<category>/ato_<slug>/`, el ID `<category>/ato-<slug>`, el nombre visible
  `ATO <título de slug>` y la etiqueta de integración `$ATO <título de slug>`.
- **Fuente importada:** repositorio upstream consumido como submódulo bajo
  `imports/<upstream-owner>/<repository>/`. No es una skill propia ni adquiere la
  licencia Apache-2.0 por estar anidada en este repositorio.

El gitlink del submódulo es la fuente técnica del commit fijado. El sidecar
`imports/<upstream-owner>/<repository>.provenance.md` conserva la evidencia de
procedencia, y `imports/CATALOG.md` mantiene el inventario y racional editorial. Los
tres artefactos deben coincidir en URL, commit y licencia.

Las importaciones no pueden usar referencias flotantes, actualizaciones remotas
automáticas ni modificaciones directas dentro del submódulo. Toda actualización exige
revisión humana de licencia, seguridad y compatibilidad, seguida de la actualización
del gitlink, sidecar y catálogo.

---

# 7. Metadata

El metadata debe evolucionar mediante un schema explícitamente versionado.

Modelo conceptual:

```yaml
schema_version: 1

id: files/organize
version: 1.0.0
category: files

runtime:
  python: ">=3.12"

tools: []

dependencies:
  python: []

capabilities:
  filesystem:
    read: true
    write: true
```

Los campos forman parte de un contrato y no deben proliferar sin necesidad.

---

# 8. Versionado

Las skills deberían utilizar Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

### PATCH

Corrección compatible.

### MINOR

Nueva capacidad compatible.

### MAJOR

Cambio incompatible de contrato o comportamiento.

El versionado representa compatibilidad funcional, no simplemente modificaciones Git.

---

# 9. Built-in CLI Tools

Una skill puede contener herramientas determinísticas.

Preferencia:

```text
Python
```

Estas herramientas existen cuando código convencional proporciona mayor:

- precisión;
- reproducibilidad;
- auditabilidad;
- eficiencia;
- seguridad

que delegar la operación al LLM.

El agente debe razonar **sobre los resultados**, no reinventar algoritmos determinísticos.

---

# 10. Contrato CLI

Cuando aplique, los CLI deben:

```text
arguments explícitos
--help
exit codes
stdout para resultados
stderr para diagnóstico
--json para automatización
--dry-run para mutaciones relevantes
```

Una operación que falla no debe devolver éxito simplemente porque produjo JSON válido.

---

# 11. Seguridad

Una skill es simultáneamente:

```text
instruction artifact
+
software artifact
```

Por ello forma parte de la supply chain.

Las capacidades relevantes deben poder declararse:

```yaml
capabilities:
  filesystem:
    read: true
    write: false

  network:
    outbound: false

  elevated_privileges: false
```

La declaración no concede permisos; el runtime decide si los concede.

---

# 12. Operaciones destructivas

Las mutaciones significativas deben favorecer:

```text
inspect
   ↓
analyze
   ↓
plan
   ↓
validate
   ↓
approval / policy
   ↓
apply
   ↓
verify
```

El diseño debe permitir intervención humana antes de cambios irreversibles.

---

# 13. Dependencias

Las dependencias deben ser declarativas.

Los scripts no deben instalar sus propias dependencias.

Las dependencias entre skills son posibles, pero deben evitarse cuando la composición pueda resolverse a nivel de agente o workflow.

Se prohíben ciclos:

```text
A → B → C → A
```

---

# 14. Estado de instalación

El sistema deberá poder conocer eventualmente:

```text
skill
version
target
scope
strategy
checksum
installation time
```

Esto permitirá:

```text
verify
diff
outdated
update
repair
```

El formato concreto se definirá cuando se implemente el installer.

---

# 15. Integridad

Las instalaciones deberían poder verificarse contra el source canónico.

El diseño debe permitir detectar:

- drift;
- modificaciones locales;
- instalaciones incompletas;
- corrupción;
- versiones antiguas.

Una actualización no debe destruir silenciosamente modificaciones locales detectadas.

---

# 16. Portabilidad

Las skills deben evitar asumir:

- rutas absolutas;
- home específico;
- shell particular;
- package manager particular;
- surface concreta;
- proveedor de LLM;
- acceso ilimitado a red.

Los requisitos específicos deben declararse.

---

# 17. Source vs Runtime

Separación obligatoria:

```text
SOURCE
├── skills
├── tools
├── schemas
├── tests
└── docs

RUNTIME
├── installations
├── cache
├── indexes
├── credentials
├── sessions
├── logs
└── agent memory
```

El runtime no debe contaminar el source canónico.

---

# 18. Estructura objetivo

```text
.
├── README.md
├── AGENTS.md
├── ARCHITECTURE.md
├── CATEGORIES.md
├── TO-DO.md
├── LICENSE
├── pyproject.toml
│
├── skills/
│   ├── development/
│   ├── memory/
│   ├── files/
│   ├── research/
│   ├── knowledge/
│   └── operations/
│
├── registry/
│   └── index.yaml
│
├── schemas/
│   ├── skill.schema.json
│   └── registry.schema.json
│
├── src/
│   └── skillctl/
│       ├── cli/
│       ├── registry/
│       ├── resolver/
│       ├── installer/
│       ├── adapters/
│       └── validation/
│
├── tools/
│   └── common/
│
├── tests/
│
└── docs/
```

Esta es una estructura objetivo.

No deben crearse componentes vacíos simplemente para parecer completa.

---

# 19. skillctl

El CLI del repositorio debe actuar como fachada de administración.

Interfaz objetivo aproximada:

```text
skillctl
├── list
├── search
├── info
├── validate
├── install
├── remove
├── update
├── outdated
├── verify
├── diff
└── registry
```

La arquitectura interna debe mantener:

```text
CLI
 ↓
Application Services
 ↓
Resolver / Installer / Registry
 ↓
Adapters
```

El CLI no debe contener directamente lógica de negocio significativa.

---

# 20. Shared Code

Las tools específicas permanecen dentro de su skill.

Cuando una responsabilidad estable sea compartida por múltiples skills, puede promoverse a:

```text
tools/common/
```

o a una librería interna.

No crear frameworks compartidos basándose únicamente en reutilización hipotética.

---

# 21. Registry

El registry debería derivarse automáticamente de:

```text
skills/**/skill.yaml
```

y no mantenerse manualmente si ello introduce duplicación.

La generación debe ser determinística.

El registry podrá permitir discovery por:

```text
id
category
tags
capabilities
compatibility
```

---

# 22. Validación

La arquitectura debe converger hacia:

```bash
skillctl validate
```

capaz de verificar:

- schema;
- identifiers;
- categorías;
- versiones;
- archivos declarados;
- tools;
- dependencias;
- capabilities;
- referencias;
- reglas de seguridad.

La validación debe poder ejecutarse tanto localmente como en CI.

---

# 23. CI

La integración continua debería evolucionar para comprobar:

```text
schema validation
repository validation
Python lint
tests
skill validation
registry consistency
secret detection
security checks
```

Los quality gates deben proteger invariantes, no limitarse a comprobar sintaxis.

---

# 24. Límites del repositorio

Este repositorio posee:

```text
skills
skill metadata
schemas
skill-local tools
validation
registry
distribution
target adapters
```

No posee principalmente:

```text
agents
agent orchestration
LLM serving
model routing
workflow engines
memory databases
secret stores
host provisioning
```

Puede integrarse con ellos sin absorber sus responsabilidades.

---

# 25. Invariantes arquitectónicos

### A1

Una skill representa una capacidad reusable.

### A2

Una skill canónica no depende innecesariamente de una surface.

### A3

Las particularidades de una surface pertenecen a adapters.

### A4

Una instalación nunca es fuente de verdad.

### A5

Source y runtime permanecen separados.

### A6

Las dependencias son explícitas.

### A7

Los secretos nunca pertenecen al source.

### A8

Las mutaciones peligrosas son visibles y controlables.

### A9

Las operaciones determinísticas deben favorecer herramientas determinísticas.

### A10

El LLM se utiliza para razonamiento, interpretación, síntesis y decisiones adaptativas.

### A11

La arquitectura debe poder comprenderse sin depender de una plataforma comercial concreta.

### A12

No introducir infraestructura cuya necesidad todavía no esté demostrada.

---

# 26. Regla de evolución

La arquitectura es estable, no inmutable.

Una decisión puede cambiar cuando exista evidencia técnica suficiente.

Los cambios que afecten invariantes, contratos públicos o fronteras de responsabilidad deben tratarse como **decisiones arquitectónicas explícitas**, no como efectos secundarios de una implementación.
