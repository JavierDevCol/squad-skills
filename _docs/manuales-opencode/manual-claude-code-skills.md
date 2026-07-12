# Manual de Skills Claude Code - Análisis Detallado

> **Fuente:** [https://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación y gestión de skills en Claude Code.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [Skills Bundled (Integrados)](#2-skills-bundled-integrados)
3. [Crear tu Primer Skill](#3-crear-tu-primer-skill)
4. [Ubicaciones y Alcance](#4-ubicaciones-y-alcance)
5. [Estructura de un Skill](#5-estructura-de-un-skill)
6. [Campos del Frontmatter](#6-campos-del-frontmatter)
7. [Control de Invocación](#7-control-de-invocación)
8. [Ciclo de Vida del Contenido](#8-ciclo-de-vida-del-contenido)
9. [Archivos de Soporte](#9-archivos-de-soporte)
10. [Inyección de Contexto Dinámico](#10-inyección-de-contexto-dinámico)
11. [Substituciones de Strings](#11-substituciones-de-strings)
12. [Skills en Sub-agentes](#12-skills-en-sub-agentes)
13. [Herramientas Permitidas/Prohibidas](#13-herramientas-permitidasprohibidas)
14. [Patrones Avanzados](#14-patrones-avanzados)
15. [Evaluar y Iterar](#15-evaluar-y-iterar)
16. [Compartir Skills](#16-compartir-skills)
17. [Ejemplos Prácticos](#17-ejemplos-prácticos)
18. [Buenas Prácticas](#18-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué es un Skill en Claude Code?

Un **skill** es una extensión de las capacidades de Claude. Creas un archivo `SKILL.md` con instrucciones, y Claude lo añade a su toolkit. Claude usa skills cuando son relevantes, o puedes invocar uno directamente con `/skill-name`.

**Características principales:**
- Carga **bajo demanda** (no consume tokens hasta que se usa)
- Puede ser invocado **automáticamente** por Claude o **manualmente** por el usuario
- Soporta **archivos de soporte** (scripts, templates, ejemplos)
- **Reutilizable** entre proyectos y sesiones
- Sigue el estándar abierto [Agent Skills](https://agentskills.io)

### Cuándo Crear un Skill

| Situación | Crear Skill |
|-----------|-------------|
| Copias las mismas instrucciones repetidamente | ✅ |
| Una sección de CLAUDE.md creció demasiado | ✅ |
| Tienes un checklist que usas frecuentemente | ✅ |
| Procedimiento de múltiples pasos recurrente | ✅ |
| Pregunta simple y directa | ❌ |

### Diferencia con CLAUDE.md

| Característica | CLAUDE.md | Skill |
|----------------|-----------|-------|
| Carga | Al inicio de sesión | Bajo demanda |
| Tokens | Siempre en contexto | Solo cuando se usa |
| Complejidad | Hechos y convenciones | Procedimientos y workflows |
| Invocación | Automática | Automática o manual |

---

## 2. Skills Bundled (Integrados)

### Skills Incluidos

| Skill | Propósito |
|-------|-----------|
| `/code-review` | Revisión de código |
| `/batch` | Procesamiento por lotes |
| `/debug` | Depuración de errores |
| `/loop` | Ejecución en bucle |
| `/claude-api` | API de Claude |
| `/run` | Lanzar y verificar app |
| `/verify` | Construir y verificar cambio |
| `/run-skill-generator` | Enseñar a `/run` y `/verify` |

### Skills de Ejecución y Verificación

| Skill | Propósito |
|-------|-----------|
| `/run` | Lanzar y manejar tu app para ver un cambio funcionando |
| `/verify` | Construir y ejecutar tu app para confirmar que un cambio funciona |
| `/run-skill-generator` | Enseñar a `/run` y `/verify` cómo construir y lanzar tu proyecto |

**`/run-skill-generator`:**
- Obtiene tu app funcionando desde un entorno limpio
- Captura qué funcionó (comandos de instalación, variables de entorno, scripts de lanzamiento)
- Lo guarda como skill por proyecto en `.claude/skills/run-<name>/`
- Ejecutar una vez por proyecto, y de nuevo si el proceso de build cambia

### Deshabilitar Skills Bundled

```json
{
  "disableBundledSkills": true
}
```

---

## 3. Crear tu Primer Skill

### Paso 1: Crear Directorio

```bash
mkdir -p ~/.claude/skills/summarize-changes
```

### Paso 2: Escribir SKILL.md

```yaml
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points, then list any risks
you notice such as missing error handling, hardcoded values, or tests that need
updating. If the diff is empty, say there are no uncommitted changes.
```

### Paso 3: Probar

**Invocación automática:**
```text
What did I change?
```

**Invocación directa:**
```text
/summarize-changes
```

---

## 4. Ubicaciones y Alcance

### Ubicaciones Soportadas

| Ubicación | Ruta | Aplica a |
|-----------|------|----------|
| Enterprise | Managed settings | Todos los usuarios de la organización |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | Todos tus proyectos |
| Proyecto | `.claude/skills/<skill-name>/SKILL.md` | Solo este proyecto |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Donde está habilitado el plugin |

### Prioridad de Resolución

```
Enterprise > Personal > Proyecto > Plugin (con namespace)
```

### Skills Anidados en Monorepos

```
proyecto/
├── .claude/skills/deploy/SKILL.md          → /deploy
└── apps/web/.claude/skills/deploy/SKILL.md → /apps/web:deploy
```

- El anidado aparece bajo nombre calificado por directorio
- Su descripción indica a qué directorio aplica
- Claude selecciona la variante que coincida con los archivos que está trabajando

### Detección de Cambios en Vivo

Claude Code monitorea directorios de skills para cambios:
- Agregar, editar o eliminar un skill toma efecto **sin reiniciar**
- Crear un directorio de skills nuevo que no existía al inicio requiere reiniciar

### Descubrimiento Automático

- Skills del proyecto se cargan desde `.claude/skills/` en el directorio inicial y cada directorio padre hasta la raíz del repo
- Cuando trabajas con archivos en subdirectorios, Claude descubre skills de `.claude/skills/` anidados bajo demanda

---

## 5. Estructura de un Skill

### Estructura de Directorio

```
my-skill/
├── SKILL.md           # Instrucciones principales (requerido)
├── template.md        # Template para que Claude llene
├── examples/
│   └── sample.md      # Ejemplo de output esperado
└── scripts/
    └── validate.sh    # Script que Claude puede ejecutar
```

### Contenido del SKILL.md

```yaml
---
name: my-skill
description: Qué hace el skill y cuándo usarlo
disable-model-invocation: true
allowed-tools: Read Grep
---

## Instrucciones

Aquí van las instrucciones que Claude sigue cuando el skill se ejecuta.
```

---

## 6. Campos del Frontmatter

### Referencia Completa

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `name` | No | Nombre para mostrar. Default: nombre del directorio |
| `description` | Recomendado | Qué hace el skill y cuándo usarlo |
| `when_to_use` | No | Contexto adicional para cuándo invocar |
| `argument-hint` | No | Hint en autocomplete: `[issue-number]` |
| `arguments` | No | Argumentos posicionales nombrados |
| `disable-model-invocation` | No | `true` = solo usuario puede invocar |
| `user-invocable` | No | `false` = oculto del menú `/` |
| `allowed-tools` | No | Herramientas auto-aprobadas |
| `disallowed-tools` | No | Herramientas removidas del pool |
| `model` | No | Modelo a usar cuando el skill está activo |
| `effort` | No | Nivel de esfuerzo: `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | No | `fork` = ejecutar en sub-agente aislado |
| `agent` | No | Tipo de sub-agente cuando `context: fork` |
| `hooks` | No | Hooks de ciclo de vida |
| `paths` | No | Glob patterns para activación condicional |
| `shell` | No | `bash` (default) o `powershell` |

### Ejemplo Completo

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
disallowed-tools: AskUserQuestion
model: sonnet
effort: high
context: fork
agent: general-purpose
paths: src/**, tests/**
shell: bash
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

---

## 7. Control de Invocación

### Matriz de Control

| Frontmatter | Usuario puede invocar | Claude puede invocar | Cuándo carga en contexto |
|-------------|----------------------|---------------------|--------------------------|
| (default) | Sí | Sí | Descripción siempre, contenido al invocar |
| `disable-model-invocation: true` | Sí | No | No carga hasta que usuario invoca |
| `user-invocable: false` | No | Sí | Descripción siempre, contenido al invocar |

### Ejemplo: Deploy Solo Manual

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

### Ejemplo: Conocimiento de Fondo Solo Automático

```yaml
---
name: legacy-system-context
description: How the legacy system works
user-invocable: false
---

The legacy system uses...
```

---

## 8. Ciclo de Vida del Contenido

### Carga

1. **Descripción** → Siempre en contexto (para que Claude sepa qué skills existen)
2. **Contenido completo** → Solo cuando se invoca el skill
3. **Permanece** → En el contexto por el resto de la sesión

### Auto-Compacción

- Cuando el contexto se llena, Claude Code re-adjunta los skills más recientes después del resumen
- Preserva los primeros **5,000 tokens** de cada skill
- Presupuesto combinado de **25,000 tokens** para skills re-adjuntos
- Skills más antiguos pueden eliminarse después de compacción

### Si un Skill deja de influir

1. Verificar que el contenido sigue presente
2. Fortalecer `description` e instrucciones
3. Usar hooks para forzar comportamiento
4. Re-invocar el skill después de compacción

---

## 9. Archivos de Soporte

### Tipos de Archivos

| Tipo | Propósito | Ejemplo |
|------|-----------|---------|
| **Templates** | Templates para que Claude llene | `template.md` |
| **Ejemplos** | Output esperado | `examples/sample.md` |
| **Scripts** | Scripts ejecutables | `scripts/validate.sh` |
| **Referencia** | Documentación detallada | `reference.md` |

### Referenciar Archivos

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

### Recomendación

Mantener `SKILL.md` bajo **500 líneas**. Mover material de referencia detallado a archivos separados.

---

## 10. Inyección de Contexto Dinámico

### Sintaxis Inline

```yaml
## Current changes
!`git diff HEAD`
```

**Comportamiento:**
1. `!`<command>` ` se ejecuta **antes** de que Claude vea el contenido
2. El output reemplaza el placeholder
3. Claude recibe el prompt con datos reales

### Sintaxis Multi-línea

````markdown
## Environment
```!
node --version
npm --version
git status --short
```
````

### Reglas

- `!` debe estar al inicio de línea o después de whitespace
- El output se inserta como **texto plano** (no se re-escanea para más placeholders)
- Para deshabilitar: `"disableSkillShellExecution": true` en settings

---

## 11. Substituciones de Strings

### Variables Disponibles

| Variable | Descripción |
|----------|-------------|
| `$ARGUMENTS` | Todos los argumentos como cadena |
| `$ARGUMENTS[N]` | Argumento por índice (0-based) |
| `$N` | Shorthand de `$ARGUMENTS[N]` |
| `$name` | Argumento nombrado del frontmatter |
| `${CLAUDE_SESSION_ID}` | ID de la sesión actual |
| `${CLAUDE_EFFORT}` | Nivel de esfuerzo actual |
| `${CLAUDE_SKILL_DIR}` | Directorio del skill |

### Ejemplo con Argumentos Nombrados

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
arguments: [component, from, to]
---

Migrate the $component component from $from to $to.
Preserve all existing behavior and tests.
```

**Uso:** `/migrate-component SearchBar React Vue`

### Ejemplo con Índices

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

### Escapar `$`

Para incluir un `$` literal antes de un número: `\$1.00`

---

## 12. Skills en Sub-agentes

### Skills con `context: fork`

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

### Comparativa: Skill vs Sub-agente

| Enfoque | System Prompt | Tarea | También carga |
|---------|---------------|-------|---------------|
| Skill con `context: fork` | Del tipo de agente | Contenido SKILL.md | CLAUDE.md (excepto Explore/Plan) |
| Sub-agente con campo `skills` | Body del markdown del sub-agente | Mensaje de delegación de Claude | Skills pre-cargados + CLAUDE.md |

### Built-in Agents

| Agent | Carga CLAUDE.md | Carga git status |
|-------|-----------------|------------------|
| Explore | No | No |
| Plan | No | No |
| general-purpose | Sí | Sí |
| Custom | Sí | Sí |

---

## 13. Herramientas Permitidas/Prohibidas

### `allowed-tools`

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

**Efecto:** Git commands se ejecutan sin pedir permiso.

### `disallowed-tools`

```yaml
---
name: autonomous-task
description: Run autonomous task
disallowed-tools: AskUserQuestion
---
```

**Efecto:** Claude no puede preguntar al usuario. La restricción se limpia en el siguiente mensaje.

### Restringir Acceso a Skills

```text
# Deshabilitar todos los skills
Skill

# Permitir solo específicos
Skill(commit)
Skill(review-pr *)

# Bloquear específicos
Skill(deploy *)
```

---

## 14. Patrones Avanzados

### Skill de Investigación con Explore

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

### Skill de Visualización

```yaml
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization
allowed-tools: Bash(python3 *)
---

Run the visualization script:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```
```

### Skill con Hooks

```yaml
---
name: auto-lint
description: Run linter after code changes
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---
```

### Skill con Paths Condicionales

```yaml
---
name: frontend-lint
description: Linting rules for frontend code
paths: src/components/**, src/pages/**
---

Apply frontend-specific linting rules...
```

---

## 15. Evaluar y Iterar

### Plugin skill-creator

```text
/plugin install skill-creator@claude-plugins-official
```

### Características

| Función | Descripción |
|---------|-------------|
| **Test cases** | Guarda prompts, archivos de input y comportamiento esperado |
| **Isolated runs** | Spawn sub-agente por test case con contexto limpio |
| **Grading** | Verifica assertions contra output |
| **Benchmark** | Agrega pass rate, tiempo y tokens |
| **Version comparison** | A/B blind entre versiones del skill |
| **Description tuning** | Genera prompts should-trigger/should-not-trigger |

### Uso

```text
evaluate my summarize-changes skill with skill-creator
```

---

## 16. Compartir Skills

### Opciones de Distribución

| Método | Alcance | Audience |
|--------|---------|----------|
| **Project skills** | `.claude/skills/` en version control | Equipo |
| **Plugins** | Directorio `skills/` en plugin | Usuarios del plugin |
| **Managed** | Managed settings | Toda la organización |

### Generar Output Visual

```yaml
---
name: codebase-visualizer
description: Generate interactive tree visualization
allowed-tools: Bash(python3 *)
---

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```
```

El script genera un HTML interactivo con:
- Vista de árbol colapsable
- Tamaños de archivos
- Colores por tipo de archivo
- Totales de directorio

---

## 17. Ejemplos Prácticos

### 17.1 Resumen de Cambios

```yaml
---
description: Summarizes uncommitted changes and flags anything risky
---

## Current changes
!`git diff HEAD`

## Instructions
Summarize the changes in two or three bullet points, then list any risks.
```

### 17.2 Fix de Issue

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

### 17.3 PR Summary

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

### 17.4 Deploy

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

### 17.5 API Conventions

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

---

## 18. Buenas Prácticas

### 18.1 Descripciones

| Hacer | No Hacer |
|-------|----------|
| "Summarizes uncommitted changes and flags risky patterns" | "Helper" |
| "Fix a GitHub issue following coding standards" | "Does stuff" |
| Poner el caso de uso clave primero | Descripciones vagas |

### 18.2 Contenido

| Hacer | No Hacer |
|-------|----------|
| Ser conciso (costo recurrente de tokens) | Narrar cómo o por qué |
| Estado qué hacer, no cómo | Instrucciones redundantes |
| Archivos de soporte para referencia detallada | Todo en un solo archivo |
| SKILL.md < 500 líneas | Archivos gigantes |

### 18.3 Control de Invocación

| Situación | Configuración |
|-----------|---------------|
| Workflow con side effects (deploy, commit) | `disable-model-invocation: true` |
| Conocimiento de fondo no actionable | `user-invocable: false` |
| Skill que solo el usuario debe ejecutar | `disable-model-invocation: true` |

### 18.4 Herramientas

| Situación | Configuración |
|-----------|---------------|
| Skill que necesita git | `allowed-tools: Bash(git *)` |
| Skill autónomo sin preguntas | `disallowed-tools: AskUserQuestion` |
| Skill de solo lectura | `allowed-tools: Read Grep Glob` |

### 18.5 Reutilización

1. **Proyecto** → `.claude/skills/` en version control
2. **Personal** → `~/.claude/skills/` para todos los proyectos
3. **Enterprise** → Managed settings para la organización

---

## Referencia Rápida

### Frontmatter

| Campo | Tipo | Default |
|-------|------|---------|
| `name` | string | Nombre del directorio |
| `description` | string | Primer párrafo del contenido |
| `disable-model-invocation` | boolean | `false` |
| `user-invocable` | boolean | `true` |
| `allowed-tools` | string | — |
| `disallowed-tools` | string | — |
| `model` | string | `inherit` |
| `effort` | string | hereda de sesión |
| `context` | string | `inline` |
| `agent` | string | `general-purpose` |
| `paths` | string | — |
| `shell` | string | `bash` |

### Substituciones

| Variable | Descripción |
|----------|-------------|
| `$ARGUMENTS` | Todos los argumentos |
| `$N` | Argumento por posición |
| `$name` | Argumento nombrado |
| `${CLAUDE_SESSION_ID}` | ID de sesión |
| `${CLAUDE_EFFORT}` | Nivel de esfuerzo |
| `${CLAUDE_SKILL_DIR}` | Directorio del skill |

### Comandos

| Comando | Descripción |
|---------|-------------|
| `/skill-name` | Invocar skill directamente |
| `/skills` | Gestionar skills |
| `/reload-plugins` | Recargar plugins |

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` | Habilitar PowerShell |
| `disableSkillShellExecution: true` | Deshabilitar shell en skills |

---

*Manual generado a partir de la documentación oficial de Claude Code.*
*Última actualización de la fuente: 27 de junio de 2026.*
