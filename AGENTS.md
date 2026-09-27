# AGENTS.md

## Propósito

Este archivo contiene el contexto principal y las reglas de trabajo para cualquier agente que modifique este repositorio.

Antes de realizar cambios significativos, el agente debe leer este documento.

Cuando una tarea afecte decisiones estructurales, contratos, distribución, seguridad o modelo de skills, también debe consultar [ARCHITECTURE.md](ARCHITECTURE.md).

Para conocer la taxonomía y las skills existentes o planificadas, consultar [CATEGORIES.md](CATEGORIES.md).

Para conocer prioridades y estado de implementación, consultar [TO-DO.md](TO-DO.md).

---

# 1. Contexto

Este repositorio es la fuente canónica de **skills reutilizables para agentes de IA**.

Una skill representa una capacidad coherente que puede ser utilizada por diferentes agentes, proyectos y superficies.

Las skills no deben quedar innecesariamente acopladas a:

- un agente concreto;
- un proyecto;
- Codex;
- OpenCode;
- OpenAI Agents SDK;
- un proveedor de modelos;
- un LLM concreto.

---

# 2. Conceptos fundamentales

Mantener separados:

```text
Skill
    capacidad reutilizable

Tool
    operación determinística

Agent
    entidad que razona y consume skills/tools

Workflow
    orquestación

Context
    información particular de proyecto o ejecución

Surface
    entorno que consume skills

Adapter
    adaptación entre una skill canónica y una surface
```

No mezclar estas responsabilidades por conveniencia de implementación.

---

# 3. Fuente de verdad

La definición canónica de las skills vive en:

```text
skills/
```

Los siguientes elementos NO son fuentes canónicas:

- instalaciones de Codex;
- instalaciones de OpenCode;
- contenido renderizado;
- cachés;
- índices runtime;
- workspaces;
- copias instaladas;
- memoria de agentes;
- estado temporal.

Una instalación debe poder reconstruirse a partir del repositorio canónico.

---

# 4. Estructura de una Skill

Estructura esperada:

```text
skills/<category>/<skill-name>/
├── SKILL.md
├── skill.yaml
├── tools/
├── references/
├── templates/
├── schemas/
├── examples/
└── tests/
```

No crear directorios vacíos únicamente para satisfacer esta estructura.

Una skill sencilla puede contener solamente:

```text
SKILL.md
skill.yaml
```

---

# 5. SKILL.md

`SKILL.md` describe el comportamiento de la capacidad.

Debe centrarse en:

- propósito;
- cuándo utilizarla;
- cuándo no utilizarla;
- entradas;
- resultados esperados;
- procedimiento;
- decisiones;
- restricciones;
- herramientas disponibles;
- validación;
- manejo de errores;
- seguridad.

No introducir detalles específicos de una surface salvo que sean esenciales para comprender la capacidad.

---

# 6. skill.yaml

`skill.yaml` representa metadata procesable por herramientas.

Como mínimo debe permitir evolucionar hacia información como:

```yaml
schema_version: 1

id: files/organize
name: File Organization
version: 1.0.0
category: files

description: >
  Analiza y organiza colecciones de archivos.

tools: []

dependencies:
  python: []

capabilities:
  filesystem:
    read: true
    write: true
```

No agregar campos nuevos al contrato sin considerar su impacto sobre:

- schema;
- validación;
- compatibilidad;
- instalador;
- adapters.

---

# 7. Identidad

Los identificadores de skills siguen:

```text
<category>/<skill-name>
```

Ejemplos:

```text
development/code-review
memory/consolidate
files/organize
```

Usar:

- minúsculas;
- ASCII;
- nombres separados mediante `-`.

Los identificadores deben considerarse estables.

### Autoría ATO e importaciones

Las skills propias de este repositorio usan una convención editorial adicional:

```text
Ruta:     skills/<category>/ato_<slug>/
ID:       <category>/ato-<slug>
Nombre:   ATO <título de slug>
Etiqueta: $ATO <título de slug>
```

La etiqueta se reserva para integraciones de CLI, IDE o adapters; no es todavía un
campo de metadata canónica. El guion bajo separa únicamente el prefijo `ato_` en la
ruta; el identificador mantiene guiones y minúsculas ASCII.

El contenido de terceros no se presenta como autoría ATO ni se copia bajo `skills/`.
Se importa exclusivamente como submódulo bajo `imports/<upstream-owner>/<repository>/`
y conserva su licencia, avisos y procedencia upstream. Cada importación requiere un
sidecar de procedencia y una entrada con racional en `imports/CATALOG.md`.

---

# 8. Reutilización

Una skill debe representar una capacidad reutilizable.

Evitar:

```text
development/review-alfred-python
```

Preferir:

```text
development/code-review
```

y proporcionar externamente:

```text
contexto: ALFRED
lenguaje: Python
repositorio: ...
```

El contexto particular no debe contaminar la capacidad general.

---

# 9. Tools

Una skill puede incorporar herramientas determinísticas bajo:

```text
tools/
```

Python es el lenguaje preferido.

Los CLI deben, cuando corresponda:

- aceptar argumentos explícitos;
- implementar `--help`;
- usar exit codes correctamente;
- separar stdout y stderr;
- ofrecer salida JSON para consumo automático;
- evitar prompts interactivos por defecto;
- evitar efectos secundarios ocultos;
- ser testeables.

Las operaciones destructivas deberían soportar `--dry-run`.

---

# 10. Python

El código Python debe preferir:

- `pathlib`;
- type hints;
- standard library cuando sea suficiente;
- dependencias mínimas;
- separación entre lógica y CLI;
- `main()` explícito.

Patrón recomendado:

```python
def execute(...):
    ...

def build_parser():
    ...

def main() -> int:
    ...

if __name__ == "__main__":
    raise SystemExit(main())
```

No instalar dependencias desde los propios scripts.

---

# 11. Dependencias

Las dependencias deben declararse.

Nunca hacer:

```python
subprocess.run(["pip", "install", "..."])
```

El instalador o entorno runtime es responsable de resolver dependencias.

Evitar dependencias entre skills salvo que sean realmente intrínsecas.

Las dependencias circulares están prohibidas.

---

# 12. Seguridad

Las skills deben tratarse como artefactos de supply chain.

Pueden contener:

```text
instrucciones
+
código ejecutable
```

Ambos representan superficies de riesgo.

Nunca almacenar:

- passwords;
- API keys;
- tokens;
- private keys;
- cookies;
- credenciales.

Una skill puede declarar que necesita un secreto, pero nunca contener su valor.

---

# 13. Privilegios

Aplicar mínimo privilegio.

Una skill no debe asumir:

- `sudo`;
- permisos administrativos;
- acceso irrestricto a red;
- escritura global;
- modificación del sistema.

Las necesidades deben declararse explícitamente.

---

# 14. Mutaciones

Para operaciones de impacto significativo preferir:

```text
INSPECT
   ↓
ANALYZE
   ↓
PLAN
   ↓
VALIDATE
   ↓
APPROVE / POLICY
   ↓
APPLY
   ↓
VERIFY
```

No toda skill necesita todas las etapas.

Las operaciones destructivas nunca deben ocultarse.

---

# 15. Separación runtime

No introducir en el repositorio canónico:

- logs;
- cachés;
- sesiones;
- índices runtime;
- memoria operacional;
- instalaciones locales;
- credenciales;
- archivos temporales.

Los schemas o ejemplos de dichos elementos sí pueden pertenecer al repositorio.

---

# 16. Cambios

Antes de modificar arquitectura o contratos:

1. identificar qué responsabilidad cambia;
2. revisar `ARCHITECTURE.md`;
3. comprobar contratos afectados;
4. determinar compatibilidad;
5. evitar refactorizaciones no relacionadas.

Los cambios deben ser pequeños y revisables cuando sea posible.

---

# 17. Testing

Las herramientas ejecutables deben tener tests cuando su complejidad lo justifique.

Las herramientas destructivas deben probar explícitamente sus mecanismos de seguridad.

Cubrir cuando corresponda:

- happy path;
- entradas inválidas;
- límites;
- permisos;
- errores;
- comportamiento destructivo;
- comportamiento multiplataforma.

---

# 18. Documentación

La documentación debe describir el estado real.

Distinguir cuando sea necesario:

```text
Implementado
Planificado
Experimental
Deprecated
```

No documentar funcionalidad futura como existente.

---

# 19. Código compartido

No duplicar innecesariamente código entre skills.

Pero tampoco crear abstracciones globales prematuramente.

Cuando una responsabilidad aparezca consistentemente en múltiples skills, evaluar promoverla a infraestructura compartida.

---

# 20. Target-specific behavior

Las peculiaridades de Codex, OpenCode u otra surface pertenecen a adapters.

Una skill canónica no debe conocer rutas específicas como:

```text
~/.codex/...
```

salvo documentación explícitamente relacionada con una integración.

---

# 21. Generated Content

El contenido generado debe distinguirse del contenido canónico.

Cuando sea apropiado indicar:

```text
GENERATED FILE — DO NOT EDIT DIRECTLY
```

La generación debe ser reproducible.

---

# 22. Reglas para agentes de coding

Al recibir una tarea:

1. leer este archivo;
2. inspeccionar el código relevante;
3. consultar documentación adicional sólo cuando corresponda;
4. identificar contratos afectados;
5. implementar el cambio coherente mínimo;
6. actualizar tests;
7. actualizar documentación si cambia comportamiento;
8. ejecutar validaciones relevantes.

No rediseñar componentes adyacentes sin necesidad.

---

# 23. Conflictos arquitectónicos

Si una solicitud contradice una decisión documentada, señalar la contradicción.

Distinguir entre:

```text
solicitud de implementación
```

y:

```text
cambio arquitectónico
```

No convertir accidentalmente la primera en la segunda.

---

# 24. Invariantes principales

Mantener estos principios:

1. Las skills representan capacidades reutilizables.
2. Los agentes consumen skills; no son skills.
3. Las tools no son automáticamente skills.
4. Las skills canónicas son independientes de surfaces cuando sea razonable.
5. Los detalles específicos de una surface pertenecen a adapters.
6. Las instalaciones no son fuente de verdad.
7. Runtime y source permanecen separados.
8. Las dependencias son explícitas.
9. Los secretos nunca pertenecen a una skill.
10. Las operaciones destructivas deben ser visibles y protegidas.
11. El trabajo determinístico debe ejecutarse determinísticamente cuando ello mejore confiabilidad.
12. El razonamiento LLM debe reservarse para interpretación, juicio, síntesis y adaptación.
13. La portabilidad tiene prioridad sobre conveniencias específicas de una plataforma.
14. La complejidad debe estar justificada por necesidades reales.

---

# 25. Criterio de decisión

Ante nueva funcionalidad:

```text
¿Capacidad reutilizable?
        → skills/

¿Tool exclusiva de una skill?
        → skills/.../tools/

¿Código reutilizado por múltiples skills?
        → evaluar infraestructura compartida

¿Instalación o distribución?
        → skillctl

¿Comportamiento específico de una surface?
        → adapter

¿Estado runtime?
        → fuera del source canónico

¿Contexto de un proyecto?
        → fuera de la skill reusable

¿Agent?
        → fuera de este repositorio

¿Workflow?
        → fuera de este repositorio
```

En caso de duda, preservar las fronteras antes de introducir una nueva abstracción.
