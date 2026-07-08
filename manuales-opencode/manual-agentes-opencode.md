# Manual de Agentes OpenCode - Análisis Detallado

> **Fuente:** [https://opencode.ai/docs/es/agents/](https://opencode.ai/docs/es/agents/)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación, configuración y uso de agentes y subagentes en OpenCode.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [Tipos de Agentes](#2-tipos-de-agentes)
3. [Agentes Integrados](#3-agentes-integrados)
4. [Subagentes Integrados](#4-subagentes-integrados)
5. [Agentes del Sistema](#5-agentes-del-sistema)
6. [Configuración de Agentes](#6-configuración-de-agentes)
7. [Opciones de Configuración](#7-opciones-de-configuración)
8. [Creación de Agentes Personalizados](#8-creación-de-agentes-personalizados)
9. [Casos de Uso](#9-casos-de-uso)
10. [Buenas Prácticas](#10-buenas-prácticas)
11. [Ejemplos Prácticos](#11-ejemplos-prácticos)

---

## 1. Conceptos Fundamentales

### ¿Qué es un agente en OpenCode?

Un **agente** es un asistente de IA especializado que se puede configurar para tareas y flujos de trabajo específicos. Cada agente tiene:

- **Indicaciones personalizadas** (prompt): Define el comportamiento y propósito del agente.
- **Modelo asignado**: Puede usar un modelo diferente al global.
- **Acceso a herramientas**: Controla qué operaciones puede realizar.
- **Permisos**: Gestiona qué acciones requieren aprobación.

### Diferencia entre Agente y Subagente

| Característica | Agente Primario | Subagente |
|----------------|-----------------|-----------|
| Acceso directo del usuario | Sí (con Tab) | Sí (con @mención) |
| Inicia sesiones | Sí | Puede crear subsesiones |
| Modo por defecto | `primary` | `subagent` |
| Uso principal | Conversación principal | Tareas especializadas |

---

## 2. Tipos de Agentes

### 2.1 Agentes Primarios (`mode: primary`)

Son los asistentes principales con los que interactúas directamente. Se puede navegar entre ellos con la tecla **Tab** o la combinación de teclas `switch_agent`.

**Características:**
- Manejan la conversación principal del usuario.
- Tienen acceso a herramientas según sus permisos configurados.
- Pueden invocar subagentes para tareas especializadas.

### 2.2 Subagentes (`mode: subagent`)

Son asistentes especializados que los agentes primarios pueden invocar para tareas específicas. También se pueden invocar manualmente con **@mención**.

**Características:**
- Ejecutan tareas delegadas por agentes primarios.
- Pueden crear sus propias sesiones secundarias.
- Se pueden ocultar del menú de autocompletar con `hidden: true`.
- Se pueden invocar programáticamente a través de la herramienta Tarea.

### 2.3 Modo `all`

Si no se especifica `mode`, el valor predeterminado es `all`, lo que permite al agente funcionar tanto como primario como subagente.

---

## 3. Agentes Integrados

### 3.1 Build

```json
{
  "mode": "primary",
  "description": "Agente principal predeterminado con todas las herramientas habilitadas"
}
```

- **Modo:** `primary`
- **Propósito:** Trabajo de desarrollo completo con acceso total.
- **Herramientas:** Todas habilitadas (write, edit, bash, etc.)
- **Uso:** Desarrollo estándar donde se necesita acceso completo a archivos y comandos.

### 3.2 Plan

```json
{
  "mode": "primary",
  "description": "Agente restringido para planificación y análisis"
}
```

- **Modo:** `primary`
- **Propósito:** Análisis y planificación sin realizar cambios.
- **Herramientas:** Restringidas (file edits y bash configurados en `ask`).
- **Uso:** Cuando se desea que LLM analice código, sugiera cambios o cree planes sin modificaciones reales.

**Configuración predeterminada de permisos:**
- `file edits`: ask
- `bash`: ask

---

## 4. Subagentes Integrados

### 4.1 General

```json
{
  "mode": "subagent",
  "description": "Agente de uso general para investigar preguntas complejas"
}
```

- **Acceso:** Completo a herramientas (excepto tareas pendientes).
- **Uso:** Ejecutar varias unidades de trabajo en paralelo.
- **Ejemplo de invocación:** `@general ayúdame a buscar esta función`

### 4.2 Explore

```json
{
  "mode": "subagent",
  "description": "Agente rápido y de solo lectura para explorar bases de código"
}
```

- **Acceso:** Solo lectura. No se pueden modificar archivos.
- **Uso:** Buscar archivos por patrones, buscar palabras clave, responder preguntas sobre el código.

### 4.3 Scout

```json
{
  "mode": "subagent",
  "description": "Agente de solo lectura para investigar documentación externa"
}
```

- **Acceso:** Solo lectura.
- **Uso:** Clonar repositorios de dependencias, inspeccionar código fuente de librerías, contrastar código local con implementaciones upstream.

---

## 5. Agentes del Sistema

Estos agentes son ocultos y se ejecutan automáticamente. No se pueden seleccionar en la interfaz de usuario.

| Agente | Función |
|--------|---------|
| **Compactación** | Compacta contextos largos en resúmenes más pequeños. Se ejecuta automáticamente. |
| **Título** | Genera títulos de sesión cortos. Se ejecuta automáticamente. |
| **Resumen** | Crea resúmenes de sesiones. Se ejecuta automáticamente. |

---

## 6. Configuración de Agentes

### 6.1 Configuración JSON

Los agentes se definen en el archivo `opencode.json` bajo la clave `agent`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/build.txt}",
      "tools": {
        "write": true,
        "edit": true,
        "bash": true
      }
    },
    "plan": {
      "mode": "primary",
      "model": "anthropic/claude-haiku-4-20250514",
      "tools": {
        "write": false,
        "edit": false,
        "bash": false
      }
    },
    "code-reviewer": {
      "description": "Revisa código en busca de mejores prácticas y problemas potenciales",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "Eres un revisor de código. Enfócate en seguridad, rendimiento y mantenibilidad.",
      "tools": {
        "write": false,
        "edit": false
      }
    }
  }
}
```

### 6.2 Configuración Markdown

Los agentes se definen como archivos `.md` en:
- **Global:** `~/.config/opencode/agents/`
- **Por proyecto:** `.opencode/agents/`

**Estructura de un archivo Markdown:**

```markdown
---
description: Revisa código para calidad y mejores prácticas
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
---

Eres un revisor de código. Enfócate en:
- Calidad del código y mejores prácticas
- Bugs potenciales y casos extremos
- Implicaciones de rendimiento
- Consideraciones de seguridad

Proporciona comentarios constructivos sin hacer cambios directos.
```

> **Nota:** El nombre del archivo se convierte en el nombre del agente. Por ejemplo, `review.md` crea un agente `review`.

---

## 7. Opciones de Configuración

### 7.1 Descripción (`description`) - **Obligatoria**

Breve descripción de lo que hace el agente y cuándo usarlo.

```json
{
  "agent": {
    "review": {
      "description": "Revisa código para mejores prácticas y problemas potenciales"
    }
  }
}
```

### 7.2 Temperatura (`temperature`)

Controla la aleatoriedad y creatividad de las respuestas.

| Rango | Comportamiento | Ideal para |
|-------|----------------|------------|
| 0.0 - 0.2 | Muy enfocado y determinista | Análisis, planificación de código |
| 0.3 - 0.5 | Equilibrado con algo de creatividad | Desarrollo general |
| 0.6 - 1.0 | Creativo y variado | Lluvia de ideas, exploración |

**Valores predeterminados:**
- La mayoría de modelos: `0`
- Modelos Qwen: `0.55`

```json
{
  "agent": {
    "analyze": { "temperature": 0.1 },
    "build": { "temperature": 0.3 },
    "brainstorm": { "temperature": 0.7 }
  }
}
```

### 7.3 Pasos Máximos (`steps`)

Controla el número máximo de iteraciones antes de responder solo con texto.

```json
{
  "agent": {
    "quick-thinker": {
      "description": "Razonamiento rápido con iteraciones limitadas",
      "prompt": "Resuelve problemas con pasos mínimos.",
      "steps": 5
    }
  }
}
```

**Nota:** El campo heredado `maxSteps` está en desuso. Usar `steps`.

**Precaución:** Si no se establece, el agente continuará iterando hasta que el modelo decida detenerse o el usuario interrumpa.

### 7.4 Deshabilitar (`disable`)

```json
{
  "agent": {
    "review": { "disable": true }
  }
}
```

### 7.5 Indicación (`prompt`)

Especifica un archivo de aviso del sistema personalizado:

```json
{
  "agent": {
    "review": {
      "prompt": "{file:./prompts/code-review.txt}"
    }
  }
}
```

**Nota:** La ruta es relativa a donde se encuentra el archivo de configuración.

### 7.6 Modelo (`model`)

Anula el modelo para un agente específico. Formato: `provider/model-id`.

```json
{
  "agent": {
    "plan": {
      "model": "anthropic/claude-haiku-4-20250514"
    }
  }
}
```

**Comportamiento predeterminado:**
- Agentes primarios: usan el modelo global configurado.
- Subagentes: usan el modelo del agente primario que los invocó.

### 7.7 Herramientas (`tools`)

Controla qué herramientas están disponibles. Se pueden usar comodines:

```json
{
  "agent": {
    "readonly": {
      "tools": {
        "mymcp_*": false,
        "write": false,
        "edit": false
      }
    }
  }
}
```

**Nota:** La configuración específica del agente anula la configuración global.

### 7.8 Permisos (`permission`)

Gestiona acciones con tres niveles:
- `"ask"`: Solicitar aprobación antes de ejecutar.
- `"allow"`: Permitir todas las operaciones sin aprobación.
- `"deny"`: Desactiva la herramienta.

**Herramientas configurables:** `edit`, `bash`, `webfetch`

**Permisos globales:**
```json
{
  "permission": {
    "edit": "deny"
  }
}
```

**Permisos por agente:**
```json
{
  "agent": {
    "build": {
      "permission": {
        "edit": "ask"
      }
    }
  }
}
```

**Permisos para comandos bash específicos:**
```json
{
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git status *": "allow",
          "git push": "ask"
        }
      }
    }
  }
}
```

**Regla importante:** Las reglas se evalúan en orden y la **última regla coincidente gana**.

### 7.9 Modo (`mode`)

- `primary`: Solo agente primario.
- `subagent`: Solo subagente.
- `all` (predeterminado): Puede funcionar como ambos.

### 7.10 Oculto (`hidden`)

Oculta subagentes del menú de autocompletar `@`:

```json
{
  "agent": {
    "internal-helper": {
      "mode": "subagent",
      "hidden": true
    }
  }
}
```

**Nota:** Solo aplica para agentes con `mode: subagent`. El modelo aún puede invocar agentes ocultos a través de la herramienta Tarea si los permisos lo permiten.

### 7.11 Permisos de Tarea (`permission.task`)

Controla qué subagentes puede invocar un agente:

```json
{
  "agent": {
    "orchestrator": {
      "mode": "primary",
      "permission": {
        "task": {
          "*": "deny",
          "orchestrator-*": "allow",
          "code-reviewer": "ask"
        }
      }
    }
  }
}
```

**Comportamiento:** Cuando se establece en `deny`, el subagente se elimina de la descripción de la herramienta Tarea.

### 7.12 Color (`color`)

Personaliza la apariencia visual del agente:

```json
{
  "agent": {
    "creative": { "color": "#ff6b6b" },
    "code-reviewer": { "color": "accent" }
  }
}
```

**Opciones:** Color hexadecimal o temas: `primary`, `secondary`, `accent`, `success`, `warning`, `error`, `info`.

### 7.13 Top P (`top_p`)

Alternativa a la temperatura para controlar la diversidad de respuestas. Rango: 0.0 - 1.0.

```json
{
  "agent": {
    "brainstorm": { "top_p": 0.9 }
  }
}
```

### 7.14 Opciones Adicionales

Cualquier otra opción se pasa directamente al proveedor como opciones de modelo:

```json
{
  "agent": {
    "deep-thinker": {
      "description": "Agente que usa esfuerzo de razonamiento alto",
      "model": "openai/gpt-5",
      "reasoningEffort": "high",
      "textVerbosity": "low"
    }
  }
}
```

---

## 8. Creación de Agentes Personalizados

### 8.1 Usando el Comando Interactivo

```bash
opencode agent create
```

Este comando interactivo:
1. Pregunta dónde guardar el agente (global o por proyecto).
2. Solicita una descripción del propósito del agente.
3. Genera un prompt e identificador del sistema adecuados.
4. Permite seleccionar a qué herramientas puede acceder el agente.
5. Crea un archivo Markdown con la configuración.

### 8.2 Creación Manual

#### Opción A: Archivo JSON en `opencode.json`

Agregar la definición del agente en la sección `agent` del archivo de configuración.

#### Opción B: Archivo Markdown

Crear un archivo `.md` en la carpeta correspondiente:
- **Global:** `~/.config/opencode/agents/`
- **Por proyecto:** `.opencode/agents/`

**Plantilla base:**

```markdown
---
description: DESCRIPCIÓN_DEL_AGENTE
mode: subagent
model: provider/model-id
temperature: 0.3
tools:
  write: false
  edit: false
  bash: false
---

Eres un asistente especializado en [PROPÓSITO].

Enfócate en:
- [CAPACIDAD_1]
- [CAPACIDAD_2]
- [CAPACIDAD_3]
```

---

## 9. Casos de Uso

| Caso de Uso | Agente Recomendado | Configuración Sugerida |
|-------------|--------------------|------------------------|
| Desarrollo completo | Build | Todas las herramientas habilitadas |
| Análisis sin cambios | Plan | Herramientas de escritura en `ask` o `deny` |
| Revisión de código | Review (personalizado) | Solo lectura + herramientas de documentación |
| Depuración | Debug (personalizado) | Bash y herramientas de lectura habilitadas |
| Documentación | Docs (personalizado) | Archivos permitidos, bash deshabilitado |
| Auditoría de seguridad | Security (personalizado) | Solo lectura |
| Investigación externa | Scout | Solo lectura, acceso a repositorios externos |
| Exploración de código | Explore | Solo lectura, búsqueda rápida |

---

## 10. Buenas Prácticas

### 10.1 Selección de Modelos

- Usa modelos más rápidos (ej. Haiku) para tareas de planificación.
- Usa modelos más capaces (ej. Sonnet) para implementación compleja.
- Define el modelo por agente para optimizar costos y rendimiento.

### 10.2 Gestión de Permisos

- Usa `deny` para agentes de solo lectura (Plan, Review).
- Usa `ask` para agentes que necesitan aprobación en operaciones sensibles.
- Configura permisos específicos por comando bash para mayor control.
- Coloca el comodín `*` primero y las reglas específicas después.

### 10.3 Temperatura

- **Análisis/Planificación:** 0.0 - 0.2
- **Desarrollo general:** 0.3 - 0.5
- **Creatividad/Exploración:** 0.6 - 1.0

### 10.4 Organización

- Usa archivos Markdown para agentes por proyecto (`.opencode/agents/`).
- Usa archivos JSON para configuración global.
- Nombra los archivos descriptivamente (ej. `code-review.md`, `security-audit.md`).

### 10.5 Subagentes

- Oculta subagentes internos con `hidden: true`.
- Usa `permission.task` para controlar qué subagentes puede invocar cada agente.
- Aprovecha la navegación entre sesiones con `<Leader>+Right/Left`.

---

## 11. Ejemplos Prácticos

### 11.1 Agente de Documentación

**Archivo:** `~/.config/opencode/agents/docs-writer.md`

```markdown
---
description: Escribe y mantiene la documentación del proyecto
mode: subagent
tools:
  bash: false
---

Eres un escritor técnico. Crea documentación clara y completa.
Enfócate en:
- Explicaciones claras
- Estructura adecuada
- Ejemplos de código
- Lenguaje amigable para el usuario
```

### 11.2 Auditor de Seguridad

**Archivo:** `~/.config/opencode/agents/security-auditor.md`

```markdown
---
description: Realiza auditorías de seguridad e identifica vulnerabilidades
mode: subagent
tools:
  write: false
  edit: false
---

Eres un experto en seguridad. Enfócate en identificar problemas de seguridad potenciales.
Busca:
- Vulnerabilidades de validación de entrada
- Fallos de autenticación y autorización
- Riesgos de exposición de datos
- Vulnerabilidades de dependencias
- Problemas de configuración de seguridad
```

### 11.3 Agente de Code Review con Permisos Detallados

**Archivo:** `.opencode/agents/review.md`

```markdown
---
description: Revisión de código con permisos detallados
mode: subagent
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
    "git log*": allow
    "grep *": allow
  webfetch: deny
---

Eres un revisor de código senior. Analiza el código y sugiere mejoras.
Enfócate en:
- Calidad del código
- Mejores prácticas
- Bugs potenciales
- Rendimiento
- Seguridad
```

### 11.4 Orquestador con Control de Tareas

**Configuración JSON:**

```json
{
  "agent": {
    "orchestrator": {
      "description": "Orquesta tareas delegando a subagentes especializados",
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "permission": {
        "task": {
          "*": "deny",
          "explore": "allow",
          "review": "ask"
        }
      }
    }
  }
}
```

### 11.5 Agente Creativo

```json
{
  "agent": {
    "creative": {
      "description": "Agente creativo para lluvia de ideas y exploración",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0.8,
      "top_p": 0.9,
      "color": "#ff6b6b",
      "prompt": "{file:./prompts/creative.txt}"
    }
  }
}
```

---

## Referencia Rápida

| Opción | Tipo | Obligatorio | Descripción |
|--------|------|-------------|-------------|
| `description` | string | Sí | Descripción del agente |
| `mode` | string | No | `primary`, `subagent`, `all` (default) |
| `model` | string | No | Modelo a usar (`provider/model-id`) |
| `prompt` | string | No | Archivo de indicaciones |
| `temperature` | number | No | Aleatoriedad (0.0-1.0) |
| `top_p` | number | No | Diversidad de respuestas (0.0-1.0) |
| `steps` | number | No | Iteraciones máximas |
| `tools` | object | No | Herramientas habilitadas/deshabilitadas |
| `permission` | object | No | Permisos de acciones |
| `disable` | boolean | No | Deshabilitar agente |
| `hidden` | boolean | No | Ocultar del menú @ |
| `color` | string | No | Color de la interfaz |

---

*Manual generado a partir de la documentación oficial de OpenCode.*
*Última actualización de la fuente: 26 de junio de 2026.*
