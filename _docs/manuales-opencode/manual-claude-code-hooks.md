# Manual de Hooks Claude Code - Análisis Detallado

> **Fuente:** [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la automatización de acciones con hooks en Claude Code.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [Primer Hook](#2-primer-hook)
3. [Casos de Uso Comunes](#3-casos-de-uso-comunes)
4. [Eventos de Hook](#4-eventos-de-hook)
5. [Tipos de Hook](#5-tipos-de-hook)
6. [Cómo Funcionan los Hooks](#6-cómo-funcionan-los-hooks)
7. [Input y Output de Hooks](#7-input-y-output-de-hooks)
8. [Matchers (Filtros)](#8-matchers-filtros)
9. [Ubicación de Configuración](#9-ubicación-de-configuración)
10. [Hooks Basados en Prompt](#10-hooks-basados-en-prompt)
11. [Hooks Basados en Agente](#11-hooks-basados-en-agente)
12. [Hooks HTTP](#12-hooks-http)
13. [Ejemplos Prácticos](#13-ejemplos-prácticos)
14. [Buenas Prácticas](#14-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué son los Hooks?

Los **hooks** son comandos shell definidos por el usuario que se ejecutan en puntos específicos del ciclo de vida de Claude Code. Proporcionan control **determinista** sobre el comportamiento, asegurando que ciertas acciones siempre sucedan en lugar de depender de que el LLM elija ejecutarlas.

**Características principales:**
- Ejecutan en **puntos específicos** del ciclo de vida
- Son **deterministas** (siempre se ejecutan cuando se cumple la condición)
- Pueden **bloquear** acciones
- Pueden **inyectar** contexto
- Pueden **automatizar** tareas repetitivas
- Pueden **integrar** con herramientas existentes

### Cuándo Usar Hooks vs Skills vs Sub-agentes

| Necesidad | Usar |
|-----------|------|
| Acción que siempre debe pasar | **Hook** |
| Acción que requiere juicio | **Skill** o **Prompt hook** |
| Verificación que necesita archivos | **Agent hook** |
| Conocimiento reutilizable | **Skill** |
| Tarea en contexto aislado | **Sub-agente** |

---

## 2. Primer Hook

### Hook de Notificación de Escritorio

Agregar a `~/.claude/settings.json`:

**macOS:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

**Windows (PowerShell):**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

### Verificar Configuración

Ejecutar `/hooks` en Claude Code para ver todos los hooks configurados.

---

## 3. Casos de Uso Comunes

### 3.1 Notificaciones

| Matcher | Se ejecuta cuando |
|---------|-------------------|
| `permission_prompt` | Claude necesita aprobación |
| `idle_prompt` | Claude terminó y espera input |
| `auth_success` | Autenticación completada |
| `elicitation_dialog` | MCP abre formulario |

### 3.2 Auto-formato

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### 3.3 Bloquear Archivos Protegidos

Script `.claude/hooks/protect-files.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

Configuración:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

### 3.4 Re-inyectar Contexto después de Compaction

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

### 3.5 Auditar Cambios de Configuración

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

### 3.6 Recargar Entorno con direnv

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ],
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

### 3.7 Auto-aprobar Permisos

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

---

## 4. Eventos de Hook

### Referencia Completa de Eventos

| Evento | Cuándo se ejecuta |
|--------|-------------------|
| `SessionStart` | Sesión inicia o se reanuda |
| `Setup` | Claude Code inicia con `--init-only` |
| `UserPromptSubmit` | Envías un prompt, antes de que Claude lo procese |
| `UserPromptExpansion` | Comando se expande en prompt |
| `PreToolUse` | Antes de ejecutar un tool call. Puede bloquear |
| `PermissionRequest` | Cuando aparece diálogo de permiso |
| `PermissionDenied` | Tool call denegado por auto mode |
| `PostToolUse` | Después de que tool call exitoso |
| `PostToolUseFailure` | Después de que tool call falla |
| `PostToolBatch` | Después de batch de tool calls paralelos |
| `Notification` | Claude Code envía notificación |
| `MessageDisplay` | Mientras se muestra texto del asistente |
| `SubagentStart` | Sub-agente se spawn |
| `SubagentStop` | Sub-agente termina |
| `TaskCreated` | Tarea se crea via `TaskCreate` |
| `TaskCompleted` | Tarea se marca como completada |
| `Stop` | Claude termina de responder |
| `StopFailure` | Turno termina por error API |
| `TeammateIdle` | Teammate de agent team va a idle |
| `InstructionsLoaded` | CLAUDE.md o rules se carga |
| `ConfigChange` | Archivo de configuración cambia |
| `CwdChanged` | Directorio de trabajo cambia |
| `FileChanged` | Archivo watched cambia en disco |
| `WorktreeCreate` | Worktree se crea |
| `WorktreeRemove` | Worktree se elimina |
| `PreCompact` | Antes de compaction |
| `PostCompact` | Después de compaction |
| `Elicitation` | MCP server solicita input |
| `ElicitationResult` | Usuario responde a elicitation MCP |
| `SessionEnd` | Sesión termina |

---

## 5. Tipos de Hook

### Tipos Disponibles

| Tipo | Descripción |
|------|-------------|
| `command` | Ejecuta comando shell (el más común) |
| `http` | POST datos a URL endpoint |
| `mcp_tool` | Llama tool en servidor MCP conectado |
| `prompt` | Evaluación LLM de un solo turno |
| `agent` | Verificación multi-turno con acceso a herramientas (experimental) |

### Ejemplo de Cada Tipo

**Command:**
```json
{
  "type": "command",
  "command": "prettier --write $FILE"
}
```

**HTTP:**
```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/tool-use",
  "headers": {
    "Authorization": "Bearer $MY_TOKEN"
  }
}
```

**Prompt:**
```json
{
  "type": "prompt",
  "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains\"}."
}
```

**Agent:**
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite and check the results.",
  "timeout": 120
}
```

---

## 6. Cómo Funcionan los Hooks

### Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────┐
│                 EVENTO SE DISPARA                        │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Todos los hooks matching ejecutan EN PARALELO   │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Cada hook completa su ejecución                  │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │                                │
│                        ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Claude Code combina resultados                   │   │
│  │  Para PreToolUse: más restrictivo gana           │   │
│  │  (deny > defer > ask > allow)                    │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Combinar Múltiples Hooks

- Cada hook ejecuta **hasta completar** antes de que Claude Code combine resultados
- Un hook que retorna `deny` **no detiene** hooks hermanos
- Para `PreToolUse`: el resultado **más restrictivo** gana
- Texto de `additionalContext` se combina de todos los hooks

---

## 7. Input y Output de Hooks

### Input (stdin)

Cada evento envía JSON específico. Ejemplo `PreToolUse`:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/user/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

### Output (stdout/stderr + exit codes)

| Exit Code | Significado |
|-----------|-------------|
| `0` | Sin objeción, acción procede normalmente |
| `2` | Acción bloqueada. Razón en stderr |
| Otro | Acción procede, error en debug log |

### Output JSON Estructurado

Para más control, usar exit 0 con JSON en stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

### Decisiones para PreToolUse

| Decisión | Efecto |
|----------|--------|
| `"allow"` | Saltar prompt de permiso interactivo |
| `"deny"` | Cancelar tool call, enviar razón a Claude |
| `"ask"` | Mostrar prompt de permiso normal |

### Decisiones para PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

---

## 8. Matchers (Filtros)

### Sintaxis

| Evento | Qué filtra el matcher | Ejemplos |
|--------|----------------------|----------|
| `PreToolUse`, `PostToolUse` | Nombre del tool | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | Cómo inició la sesión | `startup`, `resume`, `clear`, `compact` |
| `Notification` | Tipo de notificación | `permission_prompt`, `idle_prompt` |
| `SubagentStart` | Tipo de agente | `Explore`, `Plan`, `general-purpose` |
| `ConfigChange` | Fuente de configuración | `user_settings`, `project_settings` |
| `FileChanged` | Archivos a watch | `.envrc\|.env` |
| `SessionEnd` | Razón de fin | `clear`, `resume`, `logout` |

### Campo `if` para Filtrado por Argumentos

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(git *)",
            "command": "./scripts/check-git-policy.sh"
          }
        ]
      }
    ]
  }
}
```

| Patrón `if` | Comando Bash | ¿Ejecuta? |
|-------------|--------------|-----------|
| `Bash(git *)` | `git push` | Sí |
| `Bash(git *)` | `npm test && git push` | Sí (subcomando matchea) |
| `Bash(git *)` | `echo $(git log)` | Sí (dentro de $() matchea) |
| `Bash(git *)` | `echo $(date)` | No |
| `Bash(git push *)` | `echo $(date)` | Sí (patrón específico) |

---

## 9. Ubicación de Configuración

### Alcance por Ubicación

| Ubicación | Alcance | Compartible |
|-----------|---------|-------------|
| `~/.claude/settings.json` | Todos tus proyectos | No |
| `.claude/settings.json` | Proyecto actual | Sí (commit) |
| `.claude/settings.local.json` | Proyecto actual | No (gitignored) |
| Managed settings | Organización | Sí (admin) |
| Plugin `hooks/hooks.json` | Plugin habilitado | Sí |
| Skill/Agent frontmatter | Mientras está activo | Sí |

### Deshabilitar Todos los Hooks

```json
{
  "disableAllHooks": true
}
```

---

## 10. Hooks Basados en Prompt

### Configuración

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

### Respuesta del Modelo

- `"ok": true` → La acción procede
- `"ok": false` → Comportamiento según evento:
  - `Stop`/`SubagentStop`: `reason` se alimenta a Claude para que siga trabajando
  - `PreToolUse`: Tool call denegado, `reason` como error
  - Otros: Turno termina, `reason` como warning

### Cuándo Usar

- Cuando el **input del hook** es suficiente para decidir
- Para juicio que requiere razonamiento
- Para validaciones que no necesitan acceder al filesystem

---

## 11. Hooks Basados en Agente

### Configuración

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### Características

| Característica | Valor |
|----------------|-------|
| **Timeout default** | 60 segundos |
| **Máximo de turnos** | 50 tool-use turns |
| **Herramientas** | Acceso a Read, Grep, Glob, Bash, etc. |
| **Estado** | Experimental |

### Cuándo Usar

- Cuando necesitas **verificar el estado del codebase**
- Para validaciones que requieren **leer archivos** o **ejecutar comandos**
- Cuando el input del hook **no es suficiente** para decidir

---

## 12. Hooks HTTP

### Configuración

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            }
          }
        ]
      }
    ]
  }
}
```

### Características

- POST datos del evento a URL
- Recibe mismo JSON que command hook en stdin
- Retorna resultados via HTTP response body
- Útil para servicios compartidos de auditoría

---

## 13. Ejemplos Prácticos

### 13.1 Logging de Comandos Bash

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 13.2 Logging de Herramientas MCP

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
          }
        ]
      }
    ]
  }
}
```

### 13.3 Limpieza al Final de Sesión

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "clear",
        "hooks": [
          {
            "type": "command",
            "command": "rm -f /tmp/claude-scratch-*.txt"
          }
        ]
      }
    ]
  }
}
```

### 13.4 Verificación de Tests antes de Parar

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results.",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### 13.5 Auditoría de Cambios de Archivo

```json
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash > \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

### 13.6 Notificación por Plataforma

**macOS:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Permission needed\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Permission needed'"
          }
        ]
      }
    ]
  }
}
```

---

## 14. Buenas Prácticas

### 14.1 Matchers

| Hacer | No Hacer |
|-------|----------|
| Matchers específicos (`Edit\|Write`) | Matchers vacíos para todo |
| `if` para filtrar por argumentos | Filtrar toda la lógica en el script |
| Match exacto para eventos simples | Regex complejos innecesarios |

### 14.2 Seguridad

| Hacer | No Hacer |
|-------|----------|
| Scripts con permisos `chmod +x` | Scripts sin permisos de ejecución |
| Validar input con `jq` | Asumir estructura del input |
| Exit 2 para bloquear | Exit 1 para errores |
| Usar `$CLAUDE_PROJECT_DIR` | Rutas hardcodeadas |

### 14.3 Rendimiento

| Hacer | No Hacer |
|-------|----------|
| Scripts ligeros y rápidos | Scripts que toman segundos |
| Deduplicación automática | Múltiples hooks idénticos |
| Hooks paralelos | Hooks secuenciales innecesarios |

### 14.4 Mantenimiento

| Hacer | No Hacer |
|-------|----------|
| Organizar en `.claude/hooks/` | Scripts sueltos en root |
| Documentar propósito del hook | Hooks sin comentarios |
| Usar `/hooks` para verificar | Adivinar qué hooks están activos |

### 14.5 Debugging

| Herramienta | Descripción |
|-------------|-------------|
| `/hooks` | Ver todos los hooks configurados |
| Debug log | stderr va a debug log |
| `jq` | Parsear input JSON |
| Test manual | Ejecutar script directamente |

---

## Referencia Rápida

### Eventos Principales

| Evento | Uso Común |
|--------|-----------|
| `PreToolUse` | Bloquear/comandos, logging |
| `PostToolUse` | Formato auto, notificaciones |
| `Notification` | Alertas de escritorio |
| `SessionStart` | Re-inyectar contexto |
| `Stop` | Verificación final |
| `ConfigChange` | Auditoría |
| `CwdChanged` | Recargar entorno |
| `FileChanged` | Reaccionar a cambios |

### Exit Codes

| Code | Significado |
|------|-------------|
| `0` | Sin objeción |
| `2` | Bloqueado (razón en stderr) |
| Otro | Error, va a debug log |

### Tipos de Hook

| Tipo | Descripción |
|------|-------------|
| `command` | Shell command |
| `http` | POST a URL |
| `mcp_tool` | Tool MCP |
| `prompt` | LLM evaluación |
| `agent` | Sub-agente verificador |

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Directorio del proyecto |
| `$CLAUDE_ENV_FILE` | Archivo de entorno |

---

*Manual generado a partir de la documentación oficial de Claude Code.*
*Última actualización de la fuente: 27 de junio de 2026.*
