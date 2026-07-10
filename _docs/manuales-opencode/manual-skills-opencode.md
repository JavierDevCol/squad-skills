# Manual de Skills (Habilidades) OpenCode - Análisis Detallado

> **Fuente:** [https://opencode.ai/docs/es/skills/](https://opencode.ai/docs/es/skills/)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación y gestión de skills (habilidades) en OpenCode.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [¿Skills vs Agentes vs Comandos?](#2-skills-vs-agentes-vs-comandos)
3. [Estructura de un Skill](#3-estructura-de-un-skill)
4. [Ubicaciones](#4-ubicaciones)
5. [Descubrimiento de Skills](#5-descubrimiento-de-skills)
6. [Frontmatter (Metadatos)](#6-frontmatter-metadatos)
7. [Validación de Nombres](#7-validación-de-nombres)
8. [Descripción del Skill](#8-descripción-del-skill)
9. [Cuerpo del Skill (Contenido)](#9-cuerpo-del-skill-contenido)
10. [Permisos](#10-permisos)
11. [Anulación por Agente](#11-anulación-por-agente)
12. [Deshabilitar Skills](#12-deshabilitar-skills)
13. [Solución de Problemas](#13-solución-de-problemas)
14. [Ejemplos Prácticos](#14-ejemplos-prácticos)
15. [Buenas Prácticas](#15-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué es un Skill en OpenCode?

Un **skill** (habilidad) es una definición reutilizable de comportamiento que OpenCode descubre y carga bajo demanda desde tu repositorio o directorio de inicio.

**Características principales:**
- Son **archivos Markdown** con frontmatter YAML
- Se cargan **bajo demanda** cuando el agente los necesita
- Son **reutilizables** entre múltiples agentes
- Tienen **permisos granulares** por agente
- Se descubren **automáticamente** por el sistema

### Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────┐
│                    OPENCODE                              │
│                                                         │
│  1. Escanea ubicaciones buscando SKILL.md               │
│                          ↓                              │
│  2. Registra skills disponibles en herramienta `skill`  │
│                          ↓                              │
│  3. Agente ve lista de skills en descripción            │
│                          ↓                              │
│  4. Agente llama a skill({ name: "nombre" })            │
│                          ↓                              │
│  5. OpenCode carga contenido completo del SKILL.md      │
│                          ↓                              │
│  6. Instrucciones se inyectan en contexto del agente    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. ¿Skills vs Agentes vs Comandos?

| Característica | Skill | Agente | Comando |
|----------------|-------|--------|---------|
| **Propósito** | Instrucciones reutilizables | Asistente especializado | Atajo para prompts |
| **Invocación** | Automática por agente | Manual o por herramienta | `/nombre` |
| **Estado** | Sin estado | Mantiene contexto | Sin estado |
| **Modific código** | No | Sí (según permisos) | No |
| **Reutilización** | Alta (multi-agente) | Media | Baja |
| **Ubicación** | `skills/*/SKILL.md` | `agents/*.rol.md` | `commands/*.md` |
| **Carga** | Bajo demanda | Al inicio de sesión | Al ejecutar |

### Cuándo usar cada uno

| Necesidad | Usar |
|-----------|------|
| Guía de cómo hacer algo específico | **Skill** |
| Asistente completo con personalidad y herramientas | **Agente** |
| Atajo para ejecutar un prompt frecuente | **Comando** |
| Instrucciones compartidas entre múltiples agentes | **Skill** |
| Flujos de trabajo complejos con estado | **Agente** |
| Acciones rápidas sin contexto | **Comando** |

---

## 3. Estructura de un Skill

### Archivo Requerido

Cada skill es un **archivo `SKILL.md`** dentro de una carpeta con el nombre del skill:

```
.opencode/skills/
├── git-release/
│   └── SKILL.md          ← Archivo requerido
├── code-review/
│   └── SKILL.md
└── api-design/
    └── SKILL.md
```

### Estructura del Archivo

```markdown
---
name: skill-name
description: Descripción del skill
license: MIT
compatibility: opencode
metadata:
  key: value
---

## Qué hago
- Instrucción 1
- Instrucción 2

## Cuándo usar
- Caso de uso 1
- Caso de uso 2

## Ejemplo
[Ejemplo de uso]
```

---

## 4. Ubicaciones

### Ubicaciones Soportadas

| Ubicación | Ruta | Alcance |
|-----------|------|---------|
| **Proyecto (OpenCode)** | `.opencode/skills/<name>/SKILL.md` | Proyecto actual |
| **Global (OpenCode)** | `~/.config/opencode/skills/<name>/SKILL.md` | Todos los proyectos |
| **Proyecto (Claude)** | `.claude/skills/<name>/SKILL.md` | Compatible con Claude |
| **Global (Claude)** | `~/.claude/skills/<name>/SKILL.md` | Compatible con Claude |
| **Proyecto (Agentes)** | `.agents/skills/<name>/SKILL.md` | Compatible con agentes |
| **Global (Agentes)** | `~/.agents/skills/<name>/SKILL.md` | Compatible con agentes |

### Recomendaciones

| Tipo de Skill | Ubicación Recomendada |
|---------------|----------------------|
| Específico del proyecto | `.opencode/skills/` |
| Reutilizable entre proyectos | `~/.config/opencode/skills/` |
| Compatible con Claude | `.claude/skills/` |
| Genérico del sistema | `~/.config/opencode/skills/` |

---

## 5. Descubrimiento de Skills

### Proceso de Descubrimiento

Para rutas locales del proyecto:

1. OpenCode **sube** desde el directorio de trabajo actual
2. Busca el **árbol de trabajo de git** (raíz del repositorio)
3. Carga cualquier `skills/*/SKILL.md` coincidente en:
   - `.opencode/`
   - `.claude/skills/*/SKILL.md`
   - `.agents/skills/*/SKILL.md`

Para rutas globales:

4. Carga desde `~/.config/opencode/skills/*/SKILL.md`
5. Carga desde `~/.claude/skills/*/SKILL.md`
6. Carga desde `~/.agents/skills/*/SKILL.md`

### Visualización en la Herramienta `skill`

OpenCode enumera las habilidades disponibles en la descripción de la herramienta `skill`:

```xml
<available_skills>
  <skill>
    <name>git-release</name>
    <description>Create consistent releases and changelogs</description>
  </skill>
  <skill>
    <name>code-review</name>
    <description>Review code for quality and security</description>
  </skill>
</available_skills>
```

### Carga de un Skill

El agente carga un skill llamando a la herramienta:

```javascript
skill({ name: "git-release" })
```

Esto inyecta el contenido completo del `SKILL.md` en el contexto del agente.

---

## 6. Frontmatter (Metadatos)

### Campos Soportados

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `name` | string | **Sí** | Nombre único del skill (1-64 caracteres) |
| `description` | string | **Sí** | Descripción (1-1024 caracteres) |
| `license` | string | No | Licencia del skill (ej: MIT, Apache-2.0) |
| `compatibility` | string | No | Compatibilidad (ej: opencode, vscode) |
| `metadata` | map | No | Mapa de cadena a cadena con metadatos adicionales |

### Campos Ignorados

Cualquier campo no listado arriba es **ignorado** por OpenCode.

### Ejemplo de Frontmatter Completo

```yaml
---
name: git-release
description: Create consistent releases and changelogs from merged PRs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
  language: en
---
```

---

## 7. Validación de Nombres

### Reglas para `name`

| Regla | Ejemplo Válido | Ejemplo Inválido |
|-------|----------------|------------------|
| 1-64 caracteres | `code-review` | `cr` (muy corto) |
| Solo minúsculas | `git-release` | `Git-Release` |
| Alfanuméricos | `api-design` | `api_design` |
| Separadores guión | `my-skill` | `my_skill` |
| No empezar con guión | `start-here` | `-start-here` |
| No terminar con guión | `end-here` | `here-` |
| No `--` consecutivos | `my--skill` | `my--skill` |

### Expresión Regular

```regex
^[a-z0-9]+(-[a-z0-9]+)*$
```

### Ejemplos Válidos

```
✅ git-release
✅ code-review
✅ api-design
✅ my-skill-123
✅ skill
```

### Ejemplos Inválidos

```
❌ Git-Release      (mayúsculas)
❌ git_release      (guión bajo)
❌ -git-release     (empieza con guión)
❌ git-release-     (termina con guión)
❌ git--release     (doble guión)
❌ git release      (espacio)
```

### Coincidencia con Directorio

**Importante:** El nombre en `name` **debe coincidir** con el nombre del directorio que contiene `SKILL.md`.

```
.opencode/skills/git-release/SKILL.md
                    ↑
                    nombre del directorio = name en frontmatter
```

---

## 8. Descripción del Skill

### Reglas para `description`

| Regla | Detalle |
|-------|---------|
| Longitud | 1-1024 caracteres |
| Especificidad | Lo suficientemente clara para que el agente elija correctamente |
| Contenido | Qué hace el skill y cuándo usarlo |

### Buenas Descripciones

```
✅ "Create consistent releases and changelogs from merged PRs"
✅ "Review code for security vulnerabilities and performance issues"
✅ "Generate TypeScript types from OpenAPI schemas"
✅ "Analyze database queries for optimization opportunities"
```

### Malas Descripciones

```
❌ "Helper" (demasiado vago)
❌ "Does stuff with code" (no explica qué)
❌ "A comprehensive solution for..." (demasiado largo, poco específico)
```

---

## 9. Cuerpo del Skill (Contenido)

### Estructura Recomendada

```markdown
---
name: skill-name
description: Descripción clara
---

## Qué hago
- [Lista de capacidades del skill]
- [Qué puede hacer cuando se carga]

## Cuándo usar
- [Caso de uso 1]
- [Caso de uso 2]
- [Cuándo NO usar este skill]

## Instrucciones
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Ejemplo
[Ejemplo concreto de uso]

## Restricciones
- [Lo que NO debe hacer]
- [Límites del skill]
```

### Elementos Clave del Contenido

| Elemento | Propósito | Ejemplo |
|----------|-----------|---------|
| **Qué hago** | Define capacidades | "Draft release notes from merged PRs" |
| **Cuándo usar** | Guía de activación | "Use when preparing a tagged release" |
| **Instrucciones** | Pasos a seguir | "1. Analyze PRs... 2. Generate notes..." |
| **Ejemplo** | Caso concreto | "Input: v1.2.0 → Output: changelog.md" |
| **Restricciones** | Límites claros | "DO NOT modify code, only read" |

---

## 10. Permisos

### Configuración Global

Controla a qué agentes pueden acceder a los skills en `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

### Niveles de Permiso

| Permiso | Comportamiento |
|---------|----------------|
| `allow` | La habilidad se carga inmediatamente sin preguntar |
| `deny` | Habilidad oculta al agente, acceso rechazado |
| `ask` | Se solicita al usuario aprobación antes de cargar |

### Patrones con Comodines

| Patrón | Coincide con |
|--------|--------------|
| `*` | Todos los skills |
| `internal-*` | `internal-docs`, `internal-tools`, etc. |
| `*-review` | `code-review`, `pr-review`, etc. |
| `api-*` | `api-design`, `api-docs`, etc. |

---

## 11. Anulación por Agente

### Para Agentes Personalizados (Frontmatter)

```markdown
---
name: my-agent
description: Agente especializado
permission:
  skill:
    "documents-*": "allow"
    "internal-*": "deny"
---
```

### Para Agentes Integrados (opencode.json)

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow",
          "experimental-*": "ask"
        }
      }
    },
    "build": {
      "permission": {
        "skill": {
          "*": "allow"
        }
      }
    }
  }
}
```

### Prioridad de Permisos

```
Permiso específico del agente > Permiso global
```

Si un agente tiene permisos definidos, estos **anulan** los permisos globales.

---

## 12. Deshabilitar Skills

### Para Agentes Personalizados

Deshabilitar la herramienta `skill` completamente:

```markdown
---
name: restricted-agent
description: Agente sin acceso a skills
tools:
  skill: false
  read: true
  search: true
---
```

### Para Agentes Integrados

```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

### Efecto

Cuando `skill: false`:
- La sección `<available_skills>` se **omite por completo**
- El agente no ve ningún skill disponible
- No puede cargar ningún skill

---

## 13. Solución de Problemas

### Checklist de Verificación

| # | Verificar | Cómo |
|---|-----------|------|
| 1 | Archivo se llama `SKILL.md` | Debe ser en MAYÚSCULAS, no `skill.md` |
| 2 | Frontmatter tiene `name` y `description` | Campos obligatorios |
| 3 | Nombre cumple regex | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| 4 | Nombre coincide con directorio | `skills/mi-skill/SKILL.md` → `name: mi-skill` |
| 5 | Nombres únicos | No hay dos skills con el mismo nombre |
| 6 | Permisos no bloquean | Verificar `permission.skill` en config |
| 7 | Descripción clara | 1-1024 caracteres, específica |

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Skill no aparece | Archivo no se llama `SKILL.md` | Renombrar a mayúsculas |
| Skill no carga | Falta `name` o `description` | Agregar campos obligatorios |
| Permission denied | Permiso en `deny` | Cambiar a `allow` o `ask` |
| Nombre inválido | Usa mayúsculas o guiones bajos | Usar solo minúsculas y guiones |
| Skill duplicado | Mismo nombre en múltiples ubicaciones | Renombrar uno de ellos |

### Pasos de Debug

1. **Verificar estructura de archivos:**
   ```
   .opencode/skills/mi-skill/SKILL.md  ✅
   .opencode/skills/mi-skill/skill.md  ❌
   .opencode/skills/Mi-Skill/SKILL.md  ❌
   ```

2. **Verificar frontmatter:**
   ```yaml
   ---
   name: mi-skill          ✅
   description: Mi skill   ✅
   ---
   ```

3. **Verificar permisos en opencode.json:**
   ```json
   {
     "permission": {
       "skill": {
         "*": "allow"       ✅
       }
     }
   }
   ```

---

## 14. Ejemplos Prácticos

### 14.1 Skill de Release Management

**Archivo:** `.opencode/skills/git-release/SKILL.md`

```markdown
---
name: git-release
description: Create consistent releases and changelogs from merged PRs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## Qué hago
- Draft release notes from merged PRs
- Propose a version bump (major/minor/patch)
- Provide a copy-pasteable `gh release create` command

## Cuándo usar
Use this when you are preparing a tagged release.
Ask clarifying questions if the target versioning scheme is unclear.

## Instrucciones
1. Get merged PRs since last release: `gh pr list --state merged`
2. Categorize by type: features, fixes, breaking changes
3. Propose version bump based on semver rules
4. Generate changelog in Keep a Changelog format
5. Provide the `gh release create` command

## Ejemplo
Input: User says "create release for v2.0.0"
Output:
- Changelog with categorized PRs
- Version bump recommendation
- Ready-to-run release command

## Restricciones
- DO NOT push tags or create releases without explicit confirmation
- DO NOT modify CHANGELOG.md directly
```

### 14.2 Skill de Code Review

**Archivo:** `.opencode/skills/security-review/SKILL.md`

```markdown
---
name: security-review
description: Review code for security vulnerabilities following OWASP Top 10
metadata:
  audience: developers
  focus: security
---

## Qué hago
- Analizo código en busca de vulnerabilidades de seguridad
- Sigo las directrices OWASP Top 10
- Identifico riesgos de autenticación, autorización, inyección
- Proporciono fixes concretos

## Cuándo usar
- Antes de mergear código sensible
- Al implementar funcionalidades de autenticación
- Al revisar endpoints públicos
- Cuando se sospecha de un problema de seguridad

## Instrucciones
1. Identificar el tipo de aplicación (web, API, mobile)
2. Revisar puntos de entrada de datos
3. Verificar validación de entrada
4. Comprobar manejo de autenticación
5. Analizar acceso a datos
6. Buscar dependencias vulnerables
7. Generar reporte priorizado

## Ejemplo
Input: Revisar endpoint /api/users
Output:
- Lista de vulnerabilidades encontradas
- Severidad de cada una (Critical/High/Medium/Low)
- Código de ejemplo para fix

## Restricciones
- Solo analizo, no modifico código
- NO ejecuto scanners automáticos
- Enfoco en vulnerabilidades manuales
```

### 14.3 Skill de Documentation

**Archivo:** `.opencode/skills/api-docs/SKILL.md`

```markdown
---
name: api-docs
description: Generate OpenAPI/Swagger documentation for REST APIs
metadata:
  format: openapi-3.0
  audience: api-consumers
---

## Qué hago
- Genero documentación OpenAPI 3.0 para APIs REST
- Incluyo schemas, endpoints, autenticación
- Creo ejemplos de requests/responses
- Valido contra especificación OpenAPI

## Cuándo usar
- Al crear nuevos endpoints
- Al modificar contratos existentes
- Para mantener documentación sincronizada

## Instrucciones
1. Analizar código de controladores/routes
2. Extraer métodos HTTP, paths, parámetros
3. Identificar schemas de request/response
4. Generar YAML OpenAPI válido
5. Incluir ejemplos reales

## Ejemplo
Input: Express router con GET /users/:id
Output: Definición completa de endpoint en OpenAPI

## Restricciones
- NO genero clientes SDK
- NO ejecuto tests de integración
- Enfoco solo en documentación
```

### 14.4 Skill de Database Optimization

**Archivo:** `.opencode/skills/db-optimize/SKILL.md`

```markdown
---
name: db-optimize
description: Analyze and optimize database queries for performance
metadata:
  databases: postgresql,mysql,sqlite
  focus: performance
---

## Qué hago
- Analizo queries lentas
- Identifico missing indexes
- Sugiero optimizaciones de schema
- Reviso N+1 queries

## Cuándo usar
- Cuando hay lentitud en queries
- Al diseñar nuevos schemas
- Para revisar queries antes de producción

## Instrucciones
1. Recibir query o schema
2. Analizar plan de ejecución
3. Identificar sequential scans
4. Verificar índices existentes
5. Proponer índices faltantes
6. Sugerir reescritura de queries

## Restricciones
- NO ejecuto queries contra BD de producción
- NO modifico schema directamente
- Solo doy recomendaciones
```

---

## 15. Buenas Prácticas

### 15.1 Nomenclatura

| Hacer | No Hacer |
|-------|----------|
| `code-review` | `code_review` |
| `git-release` | `Git-Release` |
| `api-design` | `api design` |
| `db-optimize` | `dbOptimize` |

### 15.2 Descripciones

| Hacer | No Hacer |
|-------|----------|
| "Review code for security vulnerabilities" | "Helper" |
| "Create consistent releases from PRs" | "Does stuff" |
| "Generate OpenAPI documentation" | "A tool for API docs" |

### 15.3 Contenido

| Hacer | No Hacer |
|-------|----------|
| Estructura clara con secciones | Texto continuo sin estructura |
| Instrucciones paso a pasos | Párrafos largos |
| Ejemplos concretos | Teoría abstracta |
| Restricciones explícitas | Asumir que el agente sabe los límites |

### 15.4 Permisos

| Hacer | No Hacer |
|-------|----------|
| `deny` para skills peligrosos | `allow` para todo |
| `ask` para skills experimentales | `deny` sin razón |
| Patrones específicos | `*` sin consideración |

### 15.5 Organización

| Hacer | No Hacer |
|-------|----------|
| Un skill por carpeta | Múltiples skills en una carpeta |
| Nombres descriptivos | Nombres genéricos (`helper`, `util`) |
| Skills globales para reutilización | Skills específicos como globales |

---

## Referencia Rápida

### Frontmatter

| Campo | Tipo | Obligatorio | Restricción |
|-------|------|-------------|-------------|
| `name` | string | Sí | 1-64 chars, minúsculas, guiones |
| `description` | string | Sí | 1-1024 chars |
| `license` | string | No | — |
| `compatibility` | string | No | — |
| `metadata` | map | No | string → string |

### Nombre Válido

```regex
^[a-z0-9]+(-[a-z0-9]+)*$
```

### Permisos

| Valor | Comportamiento |
|-------|----------------|
| `allow` | Carga inmediata |
| `ask` | Solicita aprobación |
| `deny` | Oculta y rechaza |

### Ubicaciones

| Ruta | Alcance |
|------|---------|
| `.opencode/skills/<name>/SKILL.md` | Proyecto |
| `~/.config/opencode/skills/<name>/SKILL.md` | Global |
| `.claude/skills/<name>/SKILL.md` | Compatible Claude |
| `.agents/skills/<name>/SKILL.md` | Compatible Agentes |

---

*Manual generado a partir de la documentación oficial de OpenCode.*
*Última actualización de la fuente: 26 de junio de 2026.*
