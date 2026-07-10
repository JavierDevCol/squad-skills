# Manual de Sub-agentes Claude Code - Análisis Detallado

> **Fuente:** [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación y gestión de sub-agentes en Claude Code.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [Sub-agentes Integrados](#2-sub-agentes-integrados)
3. [Crear Sub-agentes Personalizados](#3-crear-sub-agentes-personalizados)
4. [Alcance y Prioridad](#4-alcance-y-prioridad)
5. [Campos del Frontmatter](#5-campos-del-frontmatter)
6. [Control de Herramientas](#6-control-de-herramientas)
7. [Modos de Permiso](#7-modos-de-permiso)
8. [Memoria Persistente](#8-memoria-persistente)
9. [Skills en Sub-agentes](#9-skills-en-sub-agentes)
10. [Servidores MCP](#10-servidores-mcp)
11. [Hooks (Ganchos de Ciclo de Vida)](#11-hooks-ganchos-de-ciclo-de-vida)
12. [Ejecución Foreground/Background](#12-ejecución-foregroundbackground)
13. [Sub-agentes Anidados](#13-sub-agentes-anidados)
14. [Aislamiento con Worktrees](#14-aislamiento-con-worktrees)
15. [Patrones de Uso](#15-patrones-de-uso)
16. [Ejemplos Prácticos](#16-ejemplos-prácticos)
17. [Buenas Prácticas](#17-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué es un Sub-agente en Claude Code?

Un **sub-agente** es un asistente de IA especializado que maneja tareas específicas en su propia ventana de contexto, con un system prompt personalizado, acceso a herramientas específico y permisos independientes.

**Características principales:**
- Ejecuta en su **propia ventana de contexto** (aislada)
- Tiene un **system prompt personalizado**
- Controla **qué herramientas** puede usar
- Tiene **permisos independientes**
- Devuelve **solo un resumen** al agente principal
- Se carga **bajo demanda** cuando Claude detecta una tarea coincidente

### Beneficios

| Beneficio | Descripción |
|-----------|-------------|
| **Preservar contexto** | Mantiene exploración e implementación fuera de la conversación principal |
| **Forzar restricciones** | Limita qué herramientas puede usar un sub-agente |
| **Reutilizar configuraciones** | Sub-agentes a nivel de usuario disponibles en todos los proyectos |
| **Especializar comportamiento** | System prompts enfocados para dominios específicos |
| **Controlar costos** | Enruta tareas a modelos más rápidos y baratos (Haiku) |

### Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────┐
│                 CONVERSACIÓN PRINCIPAL                   │
│                                                         │
│  1. Claude detecta tarea que coincide con descripción   │
│                          ↓                              │
│  2. Delega al sub-agente apropiado                      │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              SUB-AGENTE                          │   │
│  │  • System prompt personalizado                   │   │
│  │  • Herramientas específicas                      │   │
│  │  • Permisos independientes                       │   │
│  │  • Contexto aislado                              │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │                                │
│  3. Sub-agente devuelve SOLO el resumen                 │
│                          ↓                              │
│  4. Claude integra resultado en conversación principal  │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Sub-agentes Integrados

Claude Code incluye sub-agentes predefinidos que Claude usa automáticamente:

### 2.1 Explore

| Propiedad | Valor |
|-----------|-------|
| **Modelo** | Haiku (rárido y de baja latencia) |
| **Herramientas** | Solo lectura; Write y Edit denegados |
| **Propósito** | Descubrimiento de archivos, búsqueda de código, exploración de codebase |

**Uso:** Claude delega a Explore cuando necesita buscar o entender un codebase sin hacer cambios.

**Niveles de profundidad:**
- `quick` → Búsquedas dirigidas
- `medium` → Exploración equilibrada
- `very thorough` → Análisis completo

### 2.2 Plan

| Propiedad | Valor |
|-----------|-------|
| **Modelo** | Hereda de la conversación principal |
| **Herramientas** | Solo lectura; Write y Edit denegados |
| **Propósito** | Investigación de codebase para planificación |

**Uso:** Cuando estás en plan mode y Claude necesita entender tu codebase, delega investigación a Plan.

### 2.3 General-purpose

| Propiedad | Valor |
|-----------|-------|
| **Modelo** | Hereda de la conversación principal |
| **Herramientas** | Todas las herramientas |
| **Propósito** | Investigación compleja, operaciones de múltiples pasos, modificaciones de código |

**Uso:** Claude delega a general-purpose cuando la tarea requiere exploración y modificación, razonamiento complejo, o múltiples pasos dependientes.

### 2.4 Otros Agentes Integrados

| Agente | Modelo | Cuándo lo usa Claude |
|--------|--------|---------------------|
| `statusline-setup` | Sonnet | Al ejecutar `/statusline` |
| `claude-code-guide` | Haiku | Al preguntar sobre características de Claude Code |

### Restricciones de Sub-agentes Integrados

```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

```bash
claude --disallowedTools "Agent(Explore)"
```

---

## 3. Crear Sub-agentes Personalizados

### 3.1 Usando `/agents` (Recomendado)

1. Ejecutar `/agents` en Claude Code
2. Seleccionar pestaña **Library**
3. Seleccionar **Create new agent**
4. Elegir ubicación (Personal o Proyecto)
5. Seleccionar **Generate with Claude** o crear manualmente
6. Configurar herramientas, modelo, color, memoria
7. Guardar

### 3.2 Creación Manual (Archivos Markdown)

Crear archivos `.md` con frontmatter YAML en la ubicación correspondiente:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

Eres un revisor de código. Cuando te invoquen, analiza el código y proporciona
feedback específico y accionable sobre calidad, seguridad y mejores prácticas.
```

### 3.3 Usando CLI (`--agents`)

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

### 3.4 Ejecutar Todo el Sesion como Sub-agente

```bash
claude --agent code-reviewer
```

**Nota:** El system prompt del sub-agente reemplaza el system prompt por defecto de Claude Code.

---

## 4. Alcance y Prioridad

### Ubicaciones Soportadas

| Ubicación | Alcance | Prioridad |
|-----------|---------|-----------|
| Managed settings | Organización | 1 (más alta) |
| `--agents` CLI | Sesión actual | 2 |
| `.claude/agents/` | Proyecto actual | 3 |
| `~/.claude/agents/` | Todos tus proyectos | 4 |
| Plugin's `agents/` | Donde está habilitado el plugin | 5 (más baja) |

### Comportamiento de Herencia

- **Proyecto** (`.claude/agents/`): Se descubre subiendo desde el directorio de trabajo hasta la raíz del repo
- **Usuario** (`~/.claude/agents/`): Disponible en todos los proyectos
- **Plugins**: Escaneados recursivamente; subcarpetas se convierten en identificador con alcance
- **CLI**: Existen solo para esa sesión, no se guardan en disco

### Resolución de Nombres Duplicados

Cuando múltiples sub-agentes tienen el mismo `name`, Claude Code usa el de **mayor prioridad**.

---

## 5. Campos del Frontmatter

### Campos Obligatorios

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Identificador único (minúsculas y guiones) |
| `description` | string | Cuándo debe Claude delegar a este sub-agente |

### Campos Opcionales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `tools` | string | Herramientas permitidas (separadas por coma) |
| `disallowedTools` | string | Herramientas denegadas |
| `model` | string | Modelo: `sonnet`, `opus`, `haiku`, `fable`, ID completo, o `inherit` |
| `permissionMode` | string | Modo de permiso: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | number | Máximo de turnos antes de detenerse |
| `skills` | array | Skills a pre-cargar en el contexto |
| `mcpServers` | array | Servidores MCP disponibles |
| `hooks` | object | Hooks de ciclo de vida |
| `memory` | string | Alcance de memoria persistente: `user`, `project`, `local` |
| `background` | boolean | Ejecutar en segundo plano (default: `false`) |
| `effort` | string | Nivel de esfuerzo: `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | string | Aislamiento: `worktree` |
| `color` | string | Color: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | string | Primer turno de usuario automático |

---

## 6. Control de Herramientas

### Herramientas Disponibles por Defecto

Los sub-agentes **heredan** todas las herramientas de la conversación principal.

### Herramientas NO Disponibles (incluso si se listan)

| Herramienta | Razón |
|-------------|-------|
| `AskUserQuestion` | Depende del UI de la sesión principal |
| `EnterPlanMode` | Depende del estado de la sesión |
| `ExitPlanMode` | Solo funciona con `permissionMode: plan` |
| `ScheduleWakeup` | Depende del estado de la sesión |
| `WaitForMcpServers` | Depende del estado de la sesión |

### Restricción con Allowlist (`tools`)

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

**Efecto:** Solo puede usar Read, Grep, Glob y Bash. No puede editar, escribir, ni usar MCP tools.

### Restricción con Denylist (`disallowedTools`)

```yaml
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

**Efecto:** Hereda todo excepto Write y Edit.

### Patrones MCP

```yaml
---
name: local-only
description: Inherits every tool except those from the github MCP server
disallowedTools: mcp__github
---
```

| Patrón | Efecto |
|--------|--------|
| `mcp__<server>` | Agrega/elimina todas las herramientas de un servidor |
| `mcp__<server>__*` | Lo mismo que arriba |
| `mcp__*` | Elimina todas las herramientas MCP de cualquier servidor |

### Restringir Sub-agentes que se Pueden Invocar

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

**Nota:** `Agent(worker, researcher)` es una allowlist; solo puede invocar a `worker` y `researcher`.

---

## 7. Modos de Permiso

| Modo | Comportamiento |
|------|----------------|
| `default` | Verificación estándar con prompts |
| `acceptEdits` | Auto-acepta ediciones de archivos en directorio de trabajo |
| `auto` | Clasificador en segundo plano revisa comandos |
| `dontAsk` | Auto-deniega prompts de permiso |
| `bypassPermissions` | Omite prompts de permiso (usar con precaución) |
| `plan` | Modo plan (exploración solo lectura) |

### Herencia de Permisos

- Si el padre usa `bypassPermissions` o `acceptEdits`, tiene precedencia y no se puede sobrescribir
- Si el padre usa `auto`, el sub-agente hereda `auto` y cualquier `permissionMode` en frontmatter es ignorado

---

## 8. Memoria Persistente

### Configuración

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

Eres un revisor de código. A medida que revisas código, actualiza tu memoria del agente
con patrones, convenciones y problemas recurrentes que descubras.
```

### Alcances

| Alcance | Ubicación | Cuándo usar |
|---------|-----------|-------------|
| `user` | `~/.claude/agent-memory/<name>/` | Conocimiento aplicable a todos los proyectos |
| `project` | `.claude/agent-memory/<name>/` | Conocimiento específico del proyecto, compartible via control de versiones |
| `local` | `.claude/agent-memory-local/<name>/` | Conocimiento específico del proyecto, NO se sube a control de versiones |

### Comportamiento

- Se inyecta instrucciones de lectura/escritura en el system prompt
- Se carga las primeras 200 líneas o 25KB de `MEMORY.md`
- Se habilitan automáticamente Read, Write y Edit para gestionar memoria

---

## 9. Skills en Sub-agentes

### Pre-cargar Skills

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implementa endpoints API. Sigue las convenciones y patrones de los skills pre-cargados.
```

### Comportamiento

- El **contenido completo** de cada skill se inyecta en el contexto al inicio
- El campo `skills` controla qué se pre-carga, no qué puede acceder
- Sin este campo, el sub-agente puede descubrir y usar skills durante la ejecución

### Prevenir Acceso a Skills

```yaml
---
name: restricted
description: No skills allowed
disallowedTools: Skill
---
```

---

## 10. Servidores MCP

### Configuración

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Definición inline: solo para este sub-agente
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Referencia por nombre: reusa servidor ya configurado
  - github
---

Usa las herramientas de Playwright para navegar, capturar pantalla e interactuar con páginas.
```

### Tipos de Entrada

| Tipo | Descripción |
|------|-------------|
| **Inline definition** | Se conecta al inicio y desconecta al finalizar |
| **String reference** | Comparte conexión con la sesión padre |

---

## 11. Hooks (Ganchos de Ciclo de Vida)

### Hooks en Frontmatter del Sub-agente

```yaml
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

### Eventos Comunes

| Evento | Matcher | Cuándo se ejecuta |
|--------|---------|-------------------|
| `PreToolUse` | Nombre de herramienta | Antes de usar una herramienta |
| `PostToolUse` | Nombre de herramienta | Después de usar una herramienta |
| `Stop` | (ninguno) | Cuando el sub-agente termina |

### Hooks a Nivel de Proyecto

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

---

## 12. Ejecución Foreground/Background

### Foreground

- Bloquea la conversación principal hasta completar
- Los prompts de permiso se pasan al usuario

### Background

- Ejecuta concurrentemente mientras el usuario trabaja
- Los prompts de permiso aparecen en la sesión principal

### Control

| Método | Descripción |
|--------|-------------|
| `background: true` | Forzar ejecución en segundo plano |
| "run this in the background" | Pedir a Claude que ejecute en background |
| `Ctrl+B` | Mover tarea ejecutándose a background |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | Deshabilitar background tasks |

---

## 13. Sub-agentes Anidados

**Disponible desde:** v2.1.172

Un sub-agente puede invocar sus propios sub-agentes:

```
┌─────────────────────────────────────────────────┐
│           CONVERSACIÓN PRINCIPAL                 │
│                     │                            │
│                     ▼                            │
│  ┌─────────────────────────────────────────┐   │
│  │         SUB-AGENTE PADRE                │   │
│  │                  │                      │   │
│  │      ┌───────────┼───────────┐          │   │
│  │      ▼           ▼           ▼          │   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐       │   │
│  │  │ Hijo1 │  │ Hijo2 │  │ Hijo3 │       │   │
│  │  └───────┘  └───────┘  └───────┘       │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  Solo el resumen del padre llega aquí            │
└─────────────────────────────────────────────────┘
```

---

## 14. Aislamiento con Worktrees

### Configuración

```yaml
---
name: isolated-worker
description: Works in an isolated copy of the repository
isolation: worktree
---
```

### Comportamiento

- Crea un **git worktree temporal** con copia aislada del repo
- Se bifurca desde la **rama por defecto** (no desde HEAD de la sesión padre)
- Se limpia automáticamente si el sub-agente no hace cambios

---

## 15. Patrones de Uso

### 15.1 Aislar Operaciones de Alto Volumen

```text
Usa un sub-agente para ejecutar la suite de tests y reportar SOLO los tests fallidos con sus mensajes de error
```

### 15.2 Investigación en Paralelo

```text
Investiga los módulos de autenticación, base de datos y API en paralelo usando sub-agentes separados
```

### 15.3 Encadenar Sub-agentes

```text
Usa el sub-agente code-reviewer para encontrar problemas de rendimiento, luego usa el sub-agente optimizer para corregirlos
```

### 15.4 Cuándo Usar Sub-agentes vs Conversación Principal

| Usar Conversación Principal | Usar Sub-agentes |
|-----------------------------|------------------|
| Tarea necesita iteración frecuente | Tarea produce output verboso |
| Múltiples fases comparten contexto | Quieres restricciones de herramientas |
| Cambio rápido y dirigido | Trabajo autónomo que devuelve resumen |
| Latencia importa | Producción de logs/documentación extensa |

---

## 16. Ejemplos Prácticos

### 16.1 Revisor de Código (Solo Lectura)

```yaml
---
name: code-reviewer
description: Reviews code for quality and security. Use proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
color: blue
memory: project
---

Eres un revisor de código senior. Analiza el código y proporciona feedback sobre:

1. **Seguridad** - Vulnerabilidades OWASP Top 10
2. **Rendimiento** - Cuellos de botella y optimizaciones
3. **Calidad** - Legibilidad, mantenibilidad, patrones
4. **Bugs** - Errores potenciales y edge cases

Formato de salida:
- [CRITICAL/HIGH/MEDIUM/LOW] Descripción del problema
- Ubicación exacta (archivo:línea)
- Sugerencia de corrección

Actualiza tu memoria con patrones encontrados.
```

### 16.2 Debugger

```yaml
---
name: debugger
description: Debugging specialist for errors and test failures
tools: Read, Grep, Glob, Bash
model: sonnet
color: red
---

Eres un experto debugger. Cuando te invoquen:

1. Analiza el error o test fallido
2. Identifica la causa raíz
3. Proporciona fix concreto con código
4. Sugiere tests para prevenir recurrencia

Formato:
- **Error**: [descripción]
- **Causa raíz**: [explicación]
- **Fix**: [código de corrección]
- **Prevención**: [tests sugeridos]
```

### 16.3 Investigador de Dependencias

```yaml
---
name: dependency-researcher
description: Researches dependencies and their implications
tools: Read, Grep, Glob, Bash
model: haiku
color: green
---

Eres un investigador de dependencias. Analiza:

1. Dependencias desactualizadas
2. Vulnerabilidades conocidas
3. Dependencias no utilizadas
4. Licencias problemáticas
5. Alternativas más adecuadas

Output: Reporte priorizado con action items.
```

### 16.4 Coordinador con Sub-agentes Restringidos

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(code-reviewer, debugger), Read, Bash
model: sonnet
color: purple
---

Eres un coordinador. Puedes invocar:
- `code-reviewer` para revisiones de código
- `debugger` para debugging

No puedes invocar otros sub-agentes.
```

### 16.5 Sub-agente con MCP Playwright

```yaml
---
name: e2e-tester
description: Runs end-to-end tests in a real browser
tools: Read, Bash, mcp__playwright__*
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
model: sonnet
color: orange
---

Eres un tester E2E. Usa Playwright para:
1. Navegar a la aplicación
2. Ejecutar flujos de usuario
3. Capturar screenshots
4. Reportar resultados
```

---

## 17. Buenas Prácticas

### 17.1 Descripciones Claras

| Hacer | No Hacer |
|-------|----------|
| "Reviews code for quality and security" | "Helper" |
| "Debugging specialist for errors" | "Does stuff" |
| "Use proactively after code changes" | "Useful sometimes" |

### 17.2 Herramientas Mínimas Necesarias

```yaml
# ✅ Solo lo que necesita
tools: Read, Grep, Glob

# ❌ Hereda todo innecesariamente
# (omitar campo tools)
```

### 17.3 Modelo Apropiado

| Tarea | Modelo Recomendado |
|-------|-------------------|
| Exploración rápida | `haiku` |
| Revisión de código | `sonnet` |
| Análisis complejo | `opus` |
| Tareas repetitivas | `haiku` |

### 17.4 Memoria para Aprendizaje

```yaml
memory: project  # Recomendado por defecto
```

Incluir instrucciones en el system prompt:
```markdown
Actualiza tu memoria con patrones, convenciones y problemas recurrentes.
```

### 17.5 Seguridad

| Práctica | Descripción |
|----------|-------------|
| `tools` con allowlist | Limitar herramientas explícitamente |
| `disallowedTools` | Bloquear herramientas peligrosas |
| `permissionMode: default` | Pedir aprobación para operaciones |
| `isolation: worktree` | Aislar cambios del repositorio principal |

---

## Referencia Rápida

### Frontmatter

| Campo | Obligatorio | Tipo |
|-------|-------------|------|
| `name` | Sí | string |
| `description` | Sí | string |
| `tools` | No | string (comma-separated) |
| `disallowedTools` | No | string (comma-separated) |
| `model` | No | `sonnet`/`opus`/`haiku`/`fable`/ID/`inherit` |
| `permissionMode` | No | `default`/`acceptEdits`/`auto`/`dontAsk`/`bypassPermissions`/`plan` |
| `maxTurns` | No | number |
| `skills` | No | array |
| `mcpServers` | No | array |
| `hooks` | No | object |
| `memory` | No | `user`/`project`/`local` |
| `background` | No | boolean |
| `effort` | No | `low`/`medium`/`high`/`xhigh`/`max` |
| `isolation` | No | `worktree` |
| `color` | No | `red`/`blue`/`green`/`yellow`/`purple`/`orange`/`pink`/`cyan` |
| `initialPrompt` | No | string |

### Comandos CLI

| Comando | Descripción |
|---------|-------------|
| `/agents` | Abrir interfaz de gestión de sub-agentes |
| `claude --agent <name>` | Ejecutar sesión como sub-agente |
| `claude --agents '<json>'` | Definir sub-agentes via CLI |
| `claude --disallowedTools "Agent(name)"` | Bloquear sub-agente específico |

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `CLAUDE_CODE_SUBAGENT_MODEL` | Modelo para sub-agentes |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Deshabilitar background tasks |
| `CLAUDE_CODE_FORK_SUBAGENT` | Fork sub-agentes al background |
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` | Eliminar sub-agentes integrados |

---

*Manual generado a partir de la documentación oficial de Claude Code.*
*Última actualización de la fuente: 27 de junio de 2026.*
