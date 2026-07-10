# Manual de Comandos OpenCode - Análisis Detallado

> **Fuente:** [https://opencode.ai/docs/es/commands/](https://opencode.ai/docs/es/commands/)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación y uso de comandos personalizados en OpenCode.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [Comandos Integrados](#2-comandos-integrados)
3. [Crear Comandos Personalizados](#3-crear-comandos-personalizados)
4. [Configuración JSON](#4-configuración-json)
5. [Configuración Markdown](#5-configuración-markdown)
6. [Marcadores de Posición](#6-marcadores-de-posición)
7. [Opciones de Configuración](#7-opciones-de-configuración)
8. [Patrones de Uso](#8-patrones-de-uso)
9. [Ejemplos Prácticos](#9-ejemplos-prácticos)
10. [Buenas Prácticas](#10-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué es un comando en OpenCode?

Un **comando** es un atajo personalizado que ejecuta un prompt predefinido cuando se escribe `/` seguido del nombre del comando en la TUI.

**Características principales:**
- Se invoca con `/nombre-comando`
- Contiene un prompt que se envía al LLM
- Puede usar argumentos variables
- Puede inyectar salida de comandos shell
- Puede referenciar archivos específicos
- Se suma a los comandos integrados (`/init`, `/undo`, `/redo`, `/share`, `/help`)

### Diferencia entre Comando y Herramienta

| Característica | Comando | Herramienta |
|----------------|---------|-------------|
| Invocación | `/nombre` | `>nombre` |
| Complejidad | Prompt simple | Proceso paso a paso |
| Estado | Sin estado | Puede mantener contexto |
| Archivos | No modifica | Modifica archivos del sistema |
| Uso | Tareas rápidas | Flujos de trabajo complejos |

---

## 2. Comandos Integrados

OpenCode incluye comandos predefinidos que no se pueden eliminar pero pueden ser **sobrescritos**:

| Comando | Función |
|---------|---------|
| `/init` | Inicializar proyecto |
| `/undo` | Deshacer último cambio |
| `/redo` | Rehacer cambio |
| `/share` | Compartir sesión |
| `/help` | Mostrar ayuda |
| `/models` | Seleccionar modelo |
| `/connect` | Conectar proveedor |

**Nota:** Si defines un comando personalizado con el mismo nombre que uno integrado, el personalizado **sobrescribe** al integrado.

---

## 3. Crear Comandos Personalizados

### 3.1 Usando Archivos Markdown (Recomendado)

Crear archivos `.md` en el directorio correspondiente:

| Alcance | Ubicación |
|---------|-----------|
| Global | `~/.config/opencode/commands/` |
| Por proyecto | `.opencode/commands/` |

**Estructura de un archivo de comando:**

```markdown
---
description: Descripción breve del comando
agent: nombre-del-agente
model: provider/model-id
---

Aquí va el prompt que se enviará al LLM.
Puedes usar $ARGUMENTS para recibir parámetros.
```

**El nombre del archivo se convierte en el nombre del comando:**
- `test.md` → `/test`
- `review.md` → `/review`
- `create-component.md` → `/create-component`

### 3.2 Usando JSON

Agregar en `opencode.json` bajo la clave `command`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Ejecuta la suite de tests con cobertura y muestra fallos.",
      "description": "Ejecutar tests con cobertura",
      "agent": "build",
      "model": "opencode/deepseek-v4-flash-free"
    }
  }
}
```

---

## 4. Configuración JSON

### Estructura Completa

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "nombre-comando": {
      "template": "Prompt que se enviará al LLM",
      "description": "Descripción breve (se muestra en TUI)",
      "agent": "nombre-agente",
      "model": "provider/model-id",
      "subtask": true
    }
  }
}
```

### Ejemplo Múltiples Comandos

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Ejecuta tests con cobertura y reporta fallos.",
      "description": "Ejecutar tests",
      "agent": "build"
    },
    "review": {
      "template": "Revisa el código buscando problemas de seguridad y rendimiento.",
      "description": "Revisión de código",
      "agent": "plan",
      "subtask": true
    },
    "docs": {
      "template": "Genera documentación para el módulo $ARGUMENTS.",
      "description": "Generar documentación",
      "agent": "build",
      "model": "opencode/deepseek-v4-flash-free"
    }
  }
}
```

---

## 5. Configuración Markdown

### Plantilla Base

```markdown
---
description: Descripción del comando
agent: nombre-del-agente
model: provider/model-id
subtask: true/false
---

Prompt aquí. Puedes usar:
- $ARGUMENTS para todos los argumentos
- $1, $2, $3 para argumentos individuales
- !`comando` para inyectar salida de shell
- @ruta/archivo para incluir archivos
```

### Ejemplo Completo

```markdown
---
description: Revisa cambios recientes de git
agent: plan
model: opencode/deepseek-v4-flash-free
subtask: true
---

Recent git commits:
!`git log --oneline -10`

Review these changes and suggest improvements.
Focus on:
- Code quality
- Potential bugs
- Performance issues
```

---

## 6. Marcadores de Posición

### 6.1 Todos los Argumentos (`$ARGUMENTS`)

Captura **todos** los argumentos como una sola cadena:

```markdown
---
description: Crear componente
---

Crea un componente React llamado $ARGUMENTS con soporte TypeScript.
```

**Uso:** `/component Button`
**Resultado:** `$ARGUMENTS` = `Button`

### 6.2 Argumentos Posicionales (`$1`, `$2`, `$3`...)

Accede a argumentos individuales por posición:

```markdown
---
description: Crear archivo con contenido
---

Crea un archivo llamado $1 en el directorio $2
con el siguiente contenido: $3
```

**Uso:** `/create-file config.json src "{ \"key\": \"value\" }"`
**Resultado:**
- `$1` = `config.json`
- `$2` = `src`
- `$3` = `{ "key": "value" }`

### 6.3 Salida de Shell (`!`comando``)

Inyecta la salida de un comando bash en el prompt:

```markdown
---
description: Analizar cobertura de tests
---

Aquí están los resultados actuales de tests:
!`npm test`

Basado en estos resultados, sugiere mejoras para aumentar cobertura.
```

**Comandos shell útiles:**
- `!`git log --oneline -10`` → Últimos 10 commits
- `!`npm test`` → Resultados de tests
- `!`ls -la`` → Listar archivos
- `!`git diff`` → Cambios pendientes
- `!`git status`` → Estado del repositorio

### 6.4 Referencias de Archivos (`@`)

Incluye el contenido de un archivo específico:

```markdown
---
description: Revisar componente
---

Revisa el componente en @src/components/Button.tsx.
Busca problemas de rendimiento y sugiere mejoras.
```

---

## 7. Opciones de Configuración

### 7.1 Template (`template`) - **Obligatoria**

Define el mensaje que se enviará al LLM:

```json
{
  "command": {
    "test": {
      "template": "Ejecuta la suite de tests completa con cobertura."
    }
  }
}
```

**Nota:** En Markdown, el contenido después del frontmatter ES el template.

### 7.2 Descripción (`description`)

Breve descripción que se muestra en la TUI:

```json
{
  "command": {
    "test": {
      "description": "Ejecutar tests con cobertura"
    }
  }
}
```

### 7.3 Agente (`agent`)

Especifica qué agente ejecuta el comando:

```json
{
  "command": {
    "review": {
      "agent": "plan"
    }
  }
}
```

**Comportamiento:**
- Si el agente es un **subagente**, el comando activa invocación de subagente por defecto
- Si no se especifica, usa el agente actual

### 7.4 Subtarea (`subtask`)

Fuerza al comando a ejecutarse como subagente:

```json
{
  "command": {
    "analyze": {
      "subtask": true
    }
  }
}
```

**Uso:** Útil cuando quieres que el comando NO contamine el contexto principal.

### 7.5 Modelo (`model`)

Anula el modelo predeterminado para este comando:

```json
{
  "command": {
    "analyze": {
      "model": "opencode/deepseek-v4-flash-free"
    }
  }
}
```

---

## 8. Patrones de Uso

### 8.1 Comando Simple (Sin argumentos)

```markdown
---
description: Ejecutar tests
---

Ejecuta la suite de tests completa y reporta fallos.
```

**Uso:** `/test`

### 8.2 Comando con Argumentos

```markdown
---
description: Crear componente
---

Crea un componente React llamado $ARGUMENTS con:
- TypeScript
- Props tipadas
- Export default
```

**Uso:** `/component UserProfile`

### 8.3 Comando con Múltiples Argumentos

```markdown
---
description: Crear archivo
---

Crea un archivo $1 en $2 con el contenido:
$3
```

**Uso:** `/create utils.ts src/utils "export const foo = () => {}"`

### 8.4 Comando con Shell

```markdown
---
description: Revisar cambios recientes
---

Últimos commits:
!`git log --oneline -5`

Revisa estos cambios y sugiere mejoras.
```

**Uso:** `/review-recent`

### 8.5 Comando con Archivo

```markdown
---
description: Revisar componente
---

Revisa el componente en @src/components/$ARGUMENTS.tsx.
Busca bugs, problemas de rendimiento y sugiere mejoras.
```

**Uso:** `/review Button`

### 8.6 Comando como Subtarea

```markdown
---
description: Análisis profundo
subtask: true
model: opencode/deepseek-v4-flash-free
---

Analiza la arquitectura del proyecto y sugiere mejoras.
Enfócate en:
- Patrones de diseño
- Separación de responsabilidades
- Manifiesto de dependencias
```

**Uso:** `/analyze-arch`
**Efecto:** Se ejecuta como subagente, contexto aislado.

---

## 9. Ejemplos Prácticos

### 9.1 Test Runner

**Archivo:** `.opencode/commands/test.md`

```markdown
---
description: Ejecutar tests con cobertura
agent: build
---

Ejecuta la suite de tests completa con reporte de cobertura:
!`npm test -- --coverage`

Analiza los resultados:
1. Tests fallidos → Identifica causa raíz
2. Cobertura baja → Sugiere tests adicionales
3. Warnings → Recomienda correcciones

Presenta un resumen ejecutivo.
```

### 9.2 Code Review

**Archivo:** `.opencode/commands/review.md`

```markdown
---
description: Revisión de código completa
agent: plan
subtask: true
---

Revisa los cambios recientes:
!`git diff HEAD~1`

Enfócate en:
- Bugs potenciales
- Problemas de seguridad
- Rendimiento
- Legibilidad
- Cumplimiento de estándares

Proporciona feedback actionable con sugerencias específicas.
```

### 9.3 Documentation Generator

**Archivo:** `.opencode/commands/docs.md`

```markdown
---
description: Generar documentación
agent: build
---

Genera documentación para: $ARGUMENTS

Incluye:
1. Descripción del propósito
2. Parámetros de entrada
3. Valor de retorno
4. Ejemplo de uso
5. Casos edge conocidos

Usa formato Markdown limpio.
```

### 9.4 Git Commit Helper

**Archivo:** `.opencode/commands/commit.md`

```markdown
---
description: Generar mensaje de commit
agent: build
---

Analiza los cambios staged:
!`git diff --cached`

Genera un mensaje de commit siguiendo Convencional Commits:
- type(scope): description
- Incluir contexto relevante
- Ser conciso pero descriptivo

Presenta 3 opciones de mensaje.
```

### 9.5 Dependency Audit

**Archivo:** `.opencode/commands/audit.md`

```markdown
---
description: Auditar dependencias
agent: plan
subtask: true
model: opencode/deepseek-v4-flash-free
---

Analiza las dependencias del proyecto:
!`cat package.json`

Verifica:
1. Dependencias desactualizadas
2. Vulnerabilidades conocidas
3. Dependencias no utilizadas
4. Licencias problemáticas

Presenta reporte priorizado.
```

### 9.6 Component Creator (Multi-arg)

**Archivo:** `.opencode/commands/create.md`

```markdown
---
description: Crear componente completo
agent: build
---

Crea el componente $1 con esta estructura:

Directorio: $2
Tipo: $3 (functional/class)

Archivos a crear:
- $1.tsx (componente principal)
- $1.styles.ts (estilos)
- $1.test.tsx (tests)
- $1.stories.tsx (Storybook)

Incluye:
- TypeScript estricto
- Props tipadas
- Tests básicos
- Documentación JSDoc
```

**Uso:** `/create Button src/components/ui functional`

---

## 10. Buenas Prácticas

### 10.1 Nomenclatura

- Usa nombres descriptivos y cortos
- Usa guiones largos para nombres compuestos: `/code-review`, no `/cr`
- Evita nombres que colisionen con comandos integrados

### 10.2 Prompts

- Sé específico y directo
- Incluye el formato de salida esperado
- Usa estructura con pasos o listas
- Referencia archivos relevantes con `@`

### 10.3 Argumentos

- Usa `$ARGUMENTS` para argumentos simples
- Usa `$1`, `$2` cuando necesites separar parámetros
- Documenta los argumentos esperados en la descripción

### 10.4 Shell Commands

- Usa `!`comando`` para contexto dinámico
- Mantén los comandos shell ligeros (no bloqueantes)
- Evita comandos que modifiquen el estado del sistema

### 10.5 Modelos y Agentes

- Usa modelos económicos para tareas simples
- Usa `subtask: true` para análisis que no deben contaminar el contexto
- Especifica el agente cuando el comando tiene un propósito claro

### 10.6 Organización

- Coloca comandos por proyecto en `.opencode/commands/`
- Usa comandos globales en `~/.config/opencode/commands/` para tareas universales
- Documenta cada comando con descripción clara

---

## Referencia Rápida

| Opción | Tipo | Obligatorio | Descripción |
|--------|------|-------------|-------------|
| `template` | string | Sí | Prompt que se envía al LLM |
| `description` | string | No | Descripción mostrada en TUI |
| `agent` | string | No | Agente que ejecuta el comando |
| `model` | string | No | Modelo a usar |
| `subtask` | boolean | No | Ejecutar como subagente |

| Marcador | Descripción |
|----------|-------------|
| `$ARGUMENTS` | Todos los argumentos como cadena |
| `$1`, `$2`, `$3`... | Argumentos posicionales |
| `` !`comando` `` | Salida de comando shell |
| `@ruta/archivo` | Contenido de archivo |

---

*Manual generado a partir de la documentación oficial de OpenCode.*
*Última actualización de la fuente: 26 de junio de 2026.*
