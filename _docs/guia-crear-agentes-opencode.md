# Guía para Crear Agentes y Skills en OpenCode

> Basada en la documentación oficial: https://opencode.ai/docs/es/agents/ y https://opencode.ai/docs/es/skills/

---

## 1. Conceptos Fundamentales

| Concepto | Descripción |
|----------|-------------|
| **Agente primario** | Asistente principal con el que interactúas (Build, Plan). Se navega con Tab. |
| **Subagente** | Asistente especializado invocado por agentes primarios o mediante `@nombre`. |
| **Skill** | Instrucciones reutilizables en formato SKILL.md, cargadas bajo demanda con la herramienta `skill`. |
| **Tool** | Herramienta nativa (write, edit, bash, read, grep, glob, etc.) que un agente puede usar. |
| **Task tool** | Mecanismo para que un agente delegue trabajo a otro subagente. |

### Agentes Integrados

| Agente | Tipo | Modo | Herramientas |
|--------|------|------|-------------|
| **Build** | Primary | `primary` | Todas habilitadas |
| **Plan** | Primary | `primary` | Solo lectura (write/edit/bash en `ask`) |
| **General** | Subagent | `subagent` | Todas (excepto todowrite) |
| **Explore** | Subagent | `subagent` | Solo lectura |
| **Scout** | Subagent | `subagent` | Solo lectura + clonar dependencias |

---

## 2. Dónde Colocar Agentes y Skills

### Agentes (archivos .md)

| Ubicación | Ámbito |
|-----------|--------|
| `~/.config/opencode/agents/<nombre>.agent.md` | Global |
| `.opencode/agents/<nombre>.agent.md` | Por proyecto |

### Skills (directorios con SKILL.md)

| Ubicación | Ámbito |
|-----------|--------|
| `~/.config/opencode/skills/<name>/SKILL.md` | Global |
| `.opencode/skills/<name>/SKILL.md` | Proyecto |
| `~/.claude/skills/<name>/SKILL.md` | Compatibilidad Claude |
| `.claude/skills/<name>/SKILL.md` | Compatibilidad Claude (proyecto) |
| `~/.agents/skills/<name>/SKILL.md` | Compatibilidad agents.md |
| `.agents/skills/<name>/SKILL.md` | Compatibilidad agents.md (proyecto) |

Estructura de directorio de una skill:

```
skill-name/
├── SKILL.md          # Obligatorio: frontmatter YAML + instrucciones
├── scripts/          # Opcional: código ejecutable
├── references/       # Opcional: documentación complementaria
├── assets/           # Opcional: plantillas, recursos
└── ...
```

---

## 3. Formato de Agentes (Markdown)

Los agentes se definen como archivos `.agent.md` con frontmatter YAML:

```markdown
---
description: "Descripción de qué hace y cuándo usarlo (OBLIGATORIO)"
mode: subagent          # primary | subagent | all
model: provider/model   # Opcional (hereda del agente padre si es subagente)
temperature: 0.1        # 0.0-1.0 (default: 0)
steps: 10               # Máximo de iteraciones (opcional)
disable: false          # true para deshabilitar
prompt: "{file:./ruta/al/prompt.txt}"  # Prompt personalizado
color: "#FF5733"        # Color en la UI (hex o theme color)
top_p: 0.9              # Diversidad de respuesta (opcional)
tools:
  write: false
  edit: false
  bash: false
  skill: false          # Deshabilita skills completamente
permission:
  edit: deny            # deny | ask | allow
  bash:
    "*": ask
    "git status *": allow
  webfetch: deny
  task:
    "*": deny
    "orchestrator-*": allow
    "code-reviewer": ask
hidden: true            # Oculta del menú @ (solo subagent)
---
Instrucciones del agente...
```

### Formato JSON (alternativa en opencode.json)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "reviewer": {
      "description": "Revisa código y buenas prácticas",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "Eres un revisor de código...",
      "temperature": 0.1,
      "tools": {
        "write": false,
        "edit": false,
        "bash": false
      }
    }
  }
}
```

---

## 4. Formato de Skills (SKILL.md)

```markdown
---
name: mi-skill
description: >
  Usa esta skill cuando... (máx 1024 chars, formato imperativo).
  Describe la intención del usuario, no la mecánica interna.
license: MIT                            # Opcional
compatibility: "opencode >= 1.0"        # Opcional (máx 500 chars)
metadata:                               # Opcional (mapa clave-valor)
  author: equipo
  version: 1.0.0
allowed-tools: [bash, read]             # Opcional (experimental)
---

# Skill: Nombre descriptivo

## Instrucciones detalladas...
```

### Reglas de validación de `name`

- 1–64 caracteres
- Solo minúsculas, números y guiones (`^[a-z0-9]+(-[a-z0-9]+)*$`)
- No empezar/terminar con guión
- Sin `--` consecutivos
- Debe coincidir con el nombre del directorio contenedor

---

## 5. Progressive Disclosure (Skills)

Las skills se cargan en 3 etapas para minimizar tokens:

1. **Metadata** (~100 tokens): Solo `name` y `description` al inicio de sesión
2. **Instrucciones** (<5000 tokens): Cuerpo de SKILL.md, solo cuando se activa
3. **Recursos** (bajo demanda): `scripts/`, `references/`, `assets/` solo si se necesitan

> Mantener SKILL.md bajo 500 líneas. Mover material detallado a archivos separados.

---

## 6. Configuración de Permisos

### Por comando bash (glob patterns)

```json
{
  "permission": {
    "bash": {
      "git push": "ask",
      "grep *": "allow",
      "*": "ask"
    }
  }
}
```

> Las reglas se evalúan en orden y **la última coincidente gana**.

### Por agente

```json
{
  "agent": {
    "plan": {
      "permission": {
        "edit": "deny",
        "bash": { "*": "ask", "git log*": "allow" }
      }
    }
  }
}
```

### Skills: permisos globales

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

---

## 7. Buenas Prácticas para Skills Efectivas

### Qué hacer

- **Basada en expertise real**: Extraer de tareas reales, no genéricas
- **Refinada con ejecución real**: Probar, corregir, iterar
- **Contexto preciso**: Solo lo que el agente no sabría sin la skill
- **Granularidad coherente**: Ni muy específica ni muy amplia
- **Formato imperativo en description**: "Usa esta skill cuando..." en vez de "Esta skill hace..."
- **Checklists multi-paso**: Ayudan a no saltarse pasos
- **Validación**: Indicar al agente que valide su propio trabajo
- **Procedimientos sobre declaraciones**: Enseñar CÓMO, no QUÉ

### Patrones de instrucciones

| Patrón | Cuándo usarlo |
|--------|---------------|
| **Sección Gotchas** | Hechos del entorno que contradicen suposiciones razonables |
| **Plantillas de formato** | Más confiable que describir formato en prosa |
| **Checklists multi-paso** | Cuando hay dependencias entre pasos |
| **Planificar-validar-ejecutar** | Operaciones destructivas o batch |
| **Defaults no menús** | Elegir default, mencionar alternativas brevemente |

### Calibración de Control

- **Dar libertad**: Múltiples enfoques válidos → explicar el POR QUÉ
- **Ser prescriptivo**: Operaciones frágiles o el orden importa

---

## 8. Comandos Útiles

```bash
# Crear agente interactivamente
opencode agent create

# Listar modelos disponibles
opencode models
```

---

## 9. Diagrama de Arquitectura de Agentes

```
┌─────────────────────────────────────────────────────┐
│                   USUARIO                            │
└─────────────────────┬───────────────────────────────┘
                      │  Tab / @mention / task tool
                      ▼
┌──────────────────────────────────────────────────────┐
│              AGENTE PRIMARIO (Build/Plan)            │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │ Permisos     │  │ Tools        │                 │
│  │ (allow/ask/  │  │ (write,edit, │                 │
│  │  deny)       │  │  bash,skill) │                 │
│  └──────────────┘  └──────────────┘                 │
└────────────────────┬─────────────────────────────────┘
                     │  task tool
                     ▼
┌──────────────────────────────────────────────────────┐
│              SUBAGENTE (General/Explore/Scout)       │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │ Modelo propio │  │ Prompt       │                 │
│  │ (opcional)    │  │ específico   │                 │
│  └──────────────┘  └──────────────┘                 │
└────────────────────┬─────────────────────────────────┘
                     │  skill tool
                     ▼
┌──────────────────────────────────────────────────────┐
│   SKILL (SKILL.md - instrucciones bajo demanda)      │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │ Scripts      │  │ Assets/      │                 │
│  │ (autónomos)  │  │ Plantillas   │                 │
│  └──────────────┘  └──────────────┘                 │
└──────────────────────────────────────────────────────┘
```

---

## 10. Resumen de Opciones de Configuración

| Opción | Tipo | Obligatoria | Descripción |
|--------|------|-------------|-------------|
| `description` | string | **Sí** | Qué hace el agente y cuándo usarlo |
| `mode` | string | No (default: all) | `primary`, `subagent`, `all` |
| `temperature` | number | No | 0.0–1.0 (control de creatividad) |
| `steps` | number | No | Máximo de iteraciones agente |
| `disable` | boolean | No | true = deshabilitado |
| `prompt` | string | No | Ruta a archivo de prompt |
| `model` | string | No | Anula el modelo para este agente |
| `tools` | object | No | Habilita/deshabilita herramientas |
| `permission` | object | No | ask/allow/deny por herramienta/comando |
| `hidden` | boolean | No | Oculta del menú @ (solo subagent) |
| `permission.task` | object | No | Controla qué subagentes puede invocar |
| `color` | string | No | Color en UI (hex o theme) |
| `top_p` | number | No | 0.0–1.0 (diversidad) |
| *adicional* | any | No | Se pasa directo al proveedor del modelo |

---

*Fuentes: https://opencode.ai/docs/es/agents/ · https://opencode.ai/docs/es/skills/ · https://agentskills.io/specification.md*
