# Reusable Agent Skills

Repositorio canónico de **skills reutilizables para agentes de IA**.

El proyecto define, organiza, valida y distribuye capacidades que pueden ser utilizadas por diferentes agentes, proyectos y superficies de ejecución sin quedar acopladas a un runtime, modelo o proveedor específico.

Una skill puede contener instrucciones para el agente, referencias, esquemas, plantillas, ejemplos y herramientas determinísticas —principalmente CLI en Python— necesarias para ejecutar una capacidad coherente.

## Estado del bootstrap

El repositorio se encuentra en su fase de fundación. La base de desarrollo usa Python
3.12 o posterior, [uv](https://docs.astral.sh/uv/), Ruff y Pytest. Consulta
[CONTRIBUTING.md](CONTRIBUTING.md) para preparar el entorno y ejecutar las
validaciones locales.

Todavía no se implementan `skillctl`, schemas, registry, adapters, instalaciones ni
skills concretas. Esos componentes siguen el roadmap y se incorporarán cuando sus
contratos sean estables.

Las skills propias usarán la marca editorial ATO. Las fuentes de terceros se
mantendrán como submódulos fijados por commit y se documentarán en
[`imports/CATALOG.md`](imports/CATALOG.md); su licencia y procedencia upstream se
preservan.

## Objetivos

El repositorio busca que una skill sea:

- reutilizable;
- portable;
- versionada;
- auditable;
- verificable;
- testeable;
- instalable;
- componible;
- independiente de una superficie concreta.

El objetivo no es mantener una colección de prompts, sino tratar las skills como **capacidades de software duraderas y gobernadas**.

## Modelo conceptual

```text
                    Repositorio
                         │
                         ▼
                       Skill
                         │
                ┌────────┴────────┐
                │                 │
          Instrucciones       Recursos
                │                 │
                │          ┌──────┼──────┐
                │          │      │      │
                ▼          ▼      ▼      ▼
            SKILL.md     Tools  Schemas  References
                │
                └────────┬────────┘
                         │
                         ▼
                 Skill Registry
                         │
                         ▼
                 Instalación / Adaptación
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           Codex      OpenCode     Otros
```

La definición canónica de una skill permanece independiente de las superficies que la consumen.

## Qué es una Skill

Una **skill** representa una capacidad reutilizable que enseña a un agente cómo resolver una clase coherente de problemas.

Ejemplos:

```text
development/code-review
development/testing
memory/consolidate
files/organize
research/source-validation
knowledge/classify
operations/log-analysis
```

Una skill puede incluir:

```text
<skill>/
├── SKILL.md
├── skill.yaml
├── tools/
├── references/
├── templates/
├── schemas/
├── examples/
└── tests/
```

No todos estos componentes son obligatorios.

`SKILL.md` contiene el contrato semántico e instrucciones de la capacidad.

`skill.yaml` contiene metadata y contratos procesables por herramientas.

## Qué no es una Skill

El repositorio mantiene una separación explícita entre:

| Concepto | Responsabilidad |
|---|---|
| Skill | Capacidad reutilizable |
| Tool | Operación determinística |
| Agent | Entidad que razona y consume skills |
| Workflow | Orquestación de agentes, skills y herramientas |
| Context | Información particular de un proyecto o ejecución |
| Surface | Entorno que consume skills |

Los agentes, workflows, modelos y runtimes no son responsabilidad principal de este repositorio.

## Categorías

Las categorías raíz iniciales son:

```text
development
memory
files
research
knowledge
operations
```

El catálogo y las reglas de clasificación se mantienen en [CATEGORIES.md](CATEGORIES.md).

## Herramientas integradas

Una skill puede incluir herramientas CLI determinísticas cuando sea preferible ejecutar una operación mediante software en lugar de delegarla al razonamiento del LLM.

Python es el lenguaje preferido para estas herramientas.

Ejemplo conceptual:

```bash
python tools/find_duplicates.py /workspace --json
```

Las herramientas orientadas a agentes deberían producir resultados estructurados cuando sea razonable.

Las operaciones destructivas deben incorporar mecanismos de protección, particularmente planificación, validación y `--dry-run`.

## Portabilidad

Las skills canónicas no deben depender innecesariamente de:

- Codex;
- OpenCode;
- OpenAI Agents SDK;
- un proveedor de LLM;
- un modelo concreto;
- un sistema operativo;
- rutas locales específicas;
- un proyecto particular.

Las diferencias entre superficies deben resolverse mediante adaptadores o mecanismos de instalación.

## Distribución

El proyecto contempla un CLI de administración de skills, provisionalmente denominado:

```text
skillctl
```

Su evolución puede incluir operaciones como:

```bash
skillctl list
skillctl info files/organize
skillctl validate files/organize

skillctl install files/organize --target codex
skillctl update files/organize --target codex
skillctl verify files/organize --target codex
skillctl remove files/organize --target codex
```

Las skills instaladas nunca sustituyen a la definición canónica del repositorio.

## Documentación

### [AGENTS.md](AGENTS.md)

Contexto operativo y reglas que deben respetar los agentes que modifiquen este repositorio.

### [ARCHITECTURE.md](ARCHITECTURE.md)

Arquitectura, contratos, límites, invariantes y decisiones de diseño.

### [CATEGORIES.md](CATEGORIES.md)

Taxonomía inicial e inventario de skills.

### [TO-DO.md](TO-DO.md)

Roadmap de implementación hacia la versión `1.0`.

### [CONTRIBUTING.md](CONTRIBUTING.md)

Preparación del entorno, validaciones locales y convenciones de contribución.

## Estado

El repositorio se encuentra en construcción.

Las capacidades descritas en la documentación pueden representar:

- decisiones arquitectónicas;
- funcionalidad implementada;
- funcionalidad planificada.

La documentación debe distinguir estos estados y nunca presentar funcionalidad futura como si ya estuviera disponible.

## Principio rector

Una skill debe poder:

> definirse una vez, comprenderse independientemente, validarse mecánicamente y desplegarse en diferentes superficies compatibles sin reescribir su comportamiento fundamental.

## Licencia

Este repositorio se distribuye bajo [Apache License 2.0](LICENSE).
