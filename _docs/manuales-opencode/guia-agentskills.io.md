# Guía Agent Skills — agentskills.io

Análisis de la documentación oficial para la creación de skills.

## Estructura de una Skill

```
skill-name/
├── SKILL.md          # Obligatorio: frontmatter YAML + instrucciones
├── scripts/          # Opcional: código ejecutable
├── references/       # Opcional: documentación complementaria
├── assets/           # Opcional: plantillas, recursos
└── ...
```

## Frontmatter de SKILL.md

| Campo | Obligatorio | Restricciones |
|-------|-------------|---------------|
| `name` | Sí | Max 64 chars. Solo minúsculas, números y guiones. Sin empezar/terminar con guión. |
| `description` | Sí | Max 1024 chars. Describe qué hace y cuándo usarla. |
| `license` | No | Nombre de licencia o archivo. |
| `compatibility` | No | Max 500 chars. Requisitos de entorno. |
| `metadata` | No | Mapa clave-valor arbitrario. |
| `allowed-tools` | No | Tools pre-aprobadas (experimental). |

## Progressive Disclosure

Las skills se cargan en 3 etapas para minimizar consumo de contexto:

1. **Metadata** (~100 tokens): Solo `name` y `description` se cargan al inicio (para todas las skills).
2. **Instrucciones** (<5000 tokens): El cuerpo de `SKILL.md` se carga solo cuando la skill se activa.
3. **Recursos** (bajo demanda): Archivos en `scripts/`, `references/`, `assets/` se cargan solo si se necesitan.

Mantener `SKILL.md` bajo 500 líneas. Mover material detallado a archivos separados.

## Buenas Prácticas

### Lo que hace a una skill efectiva

- **Basada en expertise real**: No genéricas. Extraer de tareas reales ejecutadas con el agente.
- **Refinada con ejecución real**: Probar, corregir, iterar. Alimentar los resultados de vuelta a la skill.
- **Contexto preciso**: Agregar solo lo que el agente NO sabría sin la skill. Omitir lo obvio.
- **Granularidad coherente**: Ni muy específica (demasiadas skills) ni muy amplia (difícil de activar).
- **Nivel de detalle moderado**: Guía concisa paso a paso > documentación exhaustiva.

### Patrones de Instrucciones Efectivas

**Sección Gotchas:** Lista de hechos específicos del entorno que contradicen suposiciones razonables. Lo de mayor valor en muchas skills.

**Plantillas de formato:** Más confiable que describir el formato en prosa. Cortas van inline en SKILL.md, largas en assets/.

**Checklists multi-paso:** Ayudan al agente a no saltarse pasos. Útiles cuando hay dependencias entre pasos.

**Validación:** Indicar al agente que valide su propio trabajo antes de continuar. El patrón: hacer → validar → corregir → repetir.

**Planificar-validar-ejecutar:** Para operaciones destructivas o batch. Crear plan intermedio, validar contra fuente de verdad, luego ejecutar.

**Defaults no menús:** Elegir un default y mencionar alternativas brevemente. No presentar todas las opciones como iguales.

**Procedimientos sobre declaraciones:** Enseñar CÓMO abordar una clase de problemas, no QUÉ producir para un caso específico.

### Calibración de Control

- **Dar libertad** cuando múltiples enfoques son válidos (explicar el POR QUÉ).
- **Ser prescriptivo** cuando las operaciones son frágiles o el orden importa.
- Cada parte de la skill puede tener su propio nivel de especificidad.

### Scripts

- **Comandos one-off**: Usar `uvx`, `npx`, `pipx`, etc. para tools existentes. Pinear versiones.
- **Scripts autocontenidos**: PEP 723 (Python), `npm:` specifiers (Deno), `bun run` (Bun).
- **Diseño para agentes**: Sin prompts interactivos. `--help` descriptivo. Errores con sugerencias. Output estructurado (JSON). Idempotencia.

## Optimización de Descripciones

La `description` es el mecanismo principal para que el agente decida activar o no la skill.

- **Formulación imperativa**: "Usa esta skill cuando..." en vez de "Esta skill hace...".
- **Enfocada en intención del usuario**: No en la mecánica interna.
- **Ser insistente**: Listar contextos donde aplica, incluso si el usuario no nombra el dominio.
- **Concisa**: Unos pocos párrafos. Máximo 1024 caracteres.

### Eval Queries para Testing

Crear ~20 queries (8-10 que deberían trigger, 8-10 que no). Incluir:

- **Variedad de redacción**: Formales, casuales, con typos.
- **Explicitud**: Algunas nombrar el dominio, otras describir la necesidad sin nombrarlo.
- **Cercanas (near-misses)**: Las más valiosas. Comparten keywords pero necesitan otra cosa.
- **Realismo**: Paths de archivo, contexto personal, nombres específicos.

Ejecutar cada query 3 veces. Calcular trigger rate. Separar train/validation sets (60/40) para evitar overfitting.

## Referencia

- [Specification](https://agentskills.io/specification.md)
- [Best practices](https://agentskills.io/skill-creation/best-practices.md)
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md)
- [Using scripts](https://agentskills.io/skill-creation/using-scripts.md)
- [Quickstart](https://agentskills.io/skill-creation/quickstart.md)
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills.md)
