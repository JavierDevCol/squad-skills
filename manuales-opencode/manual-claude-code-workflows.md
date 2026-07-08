# Manual de Workflows Claude Code - Análisis Detallado

> **Fuente:** [https://code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows)
> **Fecha de análisis:** 27 de junio de 2026
> **Propósito:** Guía de referencia para la creación y gestión de workflows dinámicos en Claude Code.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [¿Cuándo Usar un Workflow?](#2-cuándo-usar-un-workflow)
3. [Comparativa: Workflows vs Sub-agentes vs Skills vs Agent Teams](#3-comparativa-workflows-vs-sub-agentes-vs-skills-vs-agent-teams)
4. [Workflows Integrados](#4-workflows-integrados)
5. [Crear un Workflow](#5-crear-un-workflow)
6. [Ultracode](#6-ultracode)
7. [Aprobación del Plan](#7-aprobación-del-plan)
8. [Guardar Workflows para Reutilizar](#8-guardar-workflows-para-reutilizar)
9. [Cómo se Ejecuta un Workflow](#9-cómo-se-ejecuta-un-workflow)
10. [Monitorear Ejecuciones](#10-monitorear-ejecuciones)
11. [Gestionar Ejecuciones](#11-gestionar-ejecuciones)
12. [Control de Costos](#12-control-de-costos)
13. [Deshabilitar Workflows](#13-deshabilitar-workflows)
14. [Ejemplos Prácticos](#14-ejemplos-prácticos)
15. [Buenas Prácticas](#15-buenas-prácticas)

---

## 1. Conceptos Fundamentales

### ¿Qué es un Workflow Dinámico?

Un **workflow dinámico** es un script JavaScript que orquesta sub-agentes a escala. Claude escribe el script para la tarea que describes, y un runtime lo ejecuta en segundo plano mientras tu sesión permanece receptiva.

**Características principales:**
- Es un **script JavaScript** (no un prompt)
- Se ejecuta en **segundo plano**
- Orquesta **docenas a cientos de agentes**
- **Reanudable** dentro de la misma sesión
- Los resultados intermedios quedan en **variables del script**
- Solo el **resultado final** llega a la conversación principal

### Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────┐
│                 CONVERSACIÓN PRINCIPAL                   │
│                                                         │
│  1. Describe la tarea (o usa "ultracode")               │
│                          ↓                              │
│  2. Claude escribe un script JavaScript                  │
│                          ↓                              │
│  3. Aprobación del plan (opcional)                       │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              RUNTIME (segundo plano)             │   │
│  │                                                 │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │ Agente1 │ │ Agente2 │ │ Agente3 │  ...      │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘          │   │
│  │       │           │           │                │   │
│  │       └───────────┼───────────┘                │   │
│  │                   ▼                            │   │
│  │          Resultados en variables               │   │
│  │                   │                            │   │
│  │                   ▼                            │   │
│  │          Script procesa y decide               │   │
│  │          siguiente paso                        │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  4. Resultado final en la conversación                  │
└─────────────────────────────────────────────────────────┘
```

---

## 2. ¿Cuándo Usar un Workflow?

### Casos de Uso Ideales

| Caso de Uso | Descripción |
|-------------|-------------|
| **Auditoría de codebase** | Escaneo completo buscando bugs, vulnerabilities, code smells |
| **Migraciones grandes** | 500+ archivos que necesitan cambios consistentes |
| **Investigación cruzada** | Preguntas que requieren múltiples fuentes verificadas |
| **Planes independientes** | Draft desde múltiples ángulos antes de decidir |
| **Revisiones adversariales** | Agentes independientes revisan hallazgos de otros |
| **Tests a gran escala** | Ejecutar y analizar cientos de tests |

### Cuándo NO Usar un Workflow

| Situación | Usar en su lugar |
|-----------|------------------|
| Tarea simple y directa | Conversación principal |
| Necesitas iteración frecuente | Conversación principal |
| Solo necesitas instrucciones | Skills |
| Un par de tareas delegadas | Sub-agentes |
| Sesiones paralelas independientes | Agent Teams |

---

## 3. Comparativa: Workflows vs Sub-agentes vs Skills vs Agent Teams

| Característica | Sub-agentes | Skills | Agent Teams | Workflows |
|----------------|-------------|--------|-------------|-----------|
| **Qué es** | Worker que Claude spawn | Instrucciones que Claude sigue | Agente líder supervisando peers | Script que el runtime ejecuta |
| **Quién decide qué ejecuta** | Claude, turno por turno | Claude, siguiendo el prompt | El líder, turno por turno | El script |
| **Dónde viven resultados intermedios** | Contexto de Claude | Contexto de Claude | Lista compartida de tareas | Variables del script |
| **Qué es reutilizable** | La definición del worker | Las instrucciones | La definición del equipo | La orquestación misma |
| **Escala** | Pocas tareas delegadas por turno | Igual que sub-agentes | Pocos peers de larga duración | Docenas a cientos de agentes por ejecución |
| **Interrupción** | Reinicia el turno | Reinicia el turno | Los teammates siguen ejecutándose | Reanudable en la misma sesión |

### Diferencia Clave

> **Un workflow mueve el plan a código.** Con sub-agentes, skills y agent teams, Claude es el orquestador: decide turno por turno qué spawnar o asignar, y cada resultado cae en una ventana de contexto. Un script de workflow mantiene el loop, el branching y los resultados intermedios, así que el contexto de Claude solo contiene la respuesta final.

---

## 4. Workflows Integrados

### `/deep-research`

| Propiedad | Valor |
|-----------|-------|
| **Comando** | `/deep-research <pregunta>` |
| **Propósito** | Investigar una pregunta en múltiples fuentes |
| **Herramientas requeridas** | WebSearch |
| **Ejecución** | Segundo plano |

**Flujo:**
1. Despacha búsquedas web desde múltiples ángulos
2. Obtiene y verifica las fuentes encontradas
3. Vota en cada afirmación
4. Sintetiza un reporte con citas
5. Filtra afirmaciones que no sobrevivieron la verificación cruzada

**Ejemplo:**
```text
/deep-research What changed in the Node.js permission model between v20 and v22?
```

---

## 5. Crear un Workflow

### 5.1 Pedir a Claude que Escriba uno

**Opción A: Palabra clave `ultracode`**
```text
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

**Opción B: Lenguaje natural**
```text
Use a workflow to migrate all class components to functional components
```

**Opción C: Describir la tarea directamente**
```text
Run a workflow to analyze the security of our authentication module
```

### 5.2 Ultracode como Modo Persistente

```text
/effort ultracode
```

Con ultracode activado:
- Claude planifica un workflow para cada tarea sustancial
- Un solo request puede generar múltiples workflows en cadena
- Se aplica a cada tarea de la sesión
- Dura solo la sesión actual (se reinicia al nueva sesión)

### 5.3 Flujo de Creación

```
1. Describe la tarea
       ↓
2. Claude escribe el script JavaScript
       ↓
3. Revisión del plan (opcional)
       ↓
4. Aprobación
       ↓
5. Ejecución en segundo plano
       ↓
6. Monitoreo via /workflows
       ↓
7. Resultado final
```

---

## 6. Ultracode

### ¿Qué es Ultracode?

Ultracode combina **razonamiento xhigh** con **orquestación automática de workflows**. Con ultracode activado, Claude planifica un workflow para cada tarea sustancial en lugar de esperar a que lo pidas.

### Activar/Desactivar

```text
/effort ultracode    # Activar
/effort high         # Desactivar (volver a nivel normal)
```

### Comportamiento

| Característica | Descripción |
|----------------|-------------|
| **Duración** | Solo la sesión actual |
| **Tokens** | Cada request usa más tokens |
| **Velocidad** | Cada request toma más tiempo |
| **Múltiples workflows** | Un request puede generar varios workflows en cadena |
| **Disponibilidad** | Modelos que soportan `xhigh` effort |

### Cuándo Usar

| Usar Ultracode | No Usar Ultracode |
|----------------|-------------------|
| Tareas complejas que benefician de orquestación | Tareas simples y directas |
| Auditorías y análisis profundos | Cambios rápidos |
| Migraciones a gran escala | Conversación casual |

---

## 7. Aprobación del Plan

### Opciones de Aprobación

| Opción | Descripción |
|--------|-------------|
| **Yes, run it** | Ejecutar el workflow |
| **Yes, and don't ask again for `<name>` en `<path>`** | Ejecutar y no preguntar de nuevo para este workflow en este proyecto |
| **View raw script** | Leer el script antes de decidir |
| **No** | Cancelar |

### Atajos

| Tecla | Acción |
|-------|--------|
| `Ctrl+G` | Abrir script en editor |
| `Tab` | Ajustar prompt antes de ejecutar |

### Modos de Permiso

| Modo | Comportamiento |
|------|----------------|
| `default`, `acceptEdits` | Pregunta en cada ejecución (excepto si seleccionaste "don't ask again") |
| `auto` | Solo pregunta la primera vez. Cualquier "Yes" guarda consentimiento |
| `bypassPermissions`, `claude -p`, Agent SDK | Nunca pregunta, ejecuta inmediatamente |

### Permisos de Sub-agentes

**Importante:** Los sub-agentes que el workflow spawn ejecutan en modo `acceptEdits` y heredan tu allowlist de herramientas, independientemente del modo de tu sesión.

| Herramienta | Comportamiento |
|-------------|----------------|
| Ediciones de archivos | Auto-aprobadas |
| Comandos shell | Pueden pedir permiso si no están en allowlist |
| Web fetches | Pueden pedir permiso si no están en allowlist |
| MCP tools | Pueden pedir permiso si no están en allowlist |

---

## 8. Guardar Workflows para Reutilizar

### Guardar un Workflow

1. Ejecutar `/workflows`
2. Seleccionar la ejecución a guardar
3. Presionar `s`
4. Elegir ubicación:
   - `.claude/workflows/` (proyecto) → compartido con el equipo
   - `~/.claude/workflows/` (personal) → solo tú
5. Presionar Enter

### Ejecutar un Workflow Guardado

```text
/nombre-del-workflow
```

### Pasar Argumentos

```text
> Run /triage-issues on issues 1024, 1025, and 1030
```

El script lee los argumentos como variable global `args`.

### Resolución de Nombres Duplicados

- **Proyecto vs Personal:** El proyecto tiene prioridad
- **Múltiples `.claude/` en monorepo:** Se usa el más cercano al directorio de trabajo

---

## 9. Cómo se Ejecuta un Workflow

### Runtime

| Característica | Descripción |
|----------------|-------------|
| **Ejecución** | Entorno aislado, separado de la conversación |
| **Resultados intermedios** | Variables del script (no contexto de Claude) |
| **Script guardado** | `~/.claude/projects/` bajo el directorio de sesión |
| **Reanudable** | Sí, dentro de la misma sesión |

### Limitaciones

| Límite | Valor | Razón |
|--------|-------|-------|
| **Input mid-run** | No permitido | Solo prompts de permiso pueden pausar |
| **Filesystem/shell directo** | No permitido | Los agentes leen/escriben/ejecutan, el script coordina |
| **Agentes concurrentes** | Máximo 16 | Limitar uso de recursos locales |
| **Agentes totales por run** | 1,000 | Prevenir loops incontrolados |

---

## 10. Monitorear Ejecuciones

### Abrir Vista de Progreso

```text
/workflows
```

### Controles de Navegación

| Tecla | Acción |
|-------|--------|
| `↑` / `↓` | Seleccionar fase o agente |
| `Enter` o `→` | Entrar en fase/agente seleccionado |
| `Esc` | Salir un nivel |
| `j` / `k` | Scroll dentro del detalle del agente |
| `f` | Filtrar lista de agentes por estado |
| `p` | Pausar o reanudar ejecución |
| `x` | Detener agente seleccionado o todo el workflow |
| `r` | Reiniciar agente en ejecución |
| `s` | Guardar script como comando |

### Información Mostrada

Por cada fase:
- Número de agentes
- Total de tokens
- Tiempo transcurrido

Por cada agente:
- Prompt utilizado
- Tool calls recientes
- Resultado

---

## 11. Gestionar Ejecuciones

### Reanudar después de Pausa

1. Ejecutar `/workflows`
2. Seleccionar ejecución pausada
3. Presionar `p`

**Comportamiento:**
- Agentes completados devuelven resultados cacheados
- Los demás ejecutan en vivo
- Funciona solo dentro de la misma sesión

### Guardar para Reutilizar

1. Seleccionar ejecución en `/workflows`
2. Presionar `s`
3. Elegir ubicación
4. El workflow se convierte en un comando `/<nombre>`

---

## 12. Control de Costos

### Consideraciones

| Factor | Impacto |
|--------|---------|
| **Múltiples agentes** | Un workflow puede usar significativamente más tokens |
| **Modelo** | Cada agente usa el modelo de la sesión (a menos que el script especifique otro) |
| **Límites** | Los agentes por run limitan el costo máximo |

### Estrategias de Control

| Estrategia | Descripción |
|------------|-------------|
| **Probar con slice pequeño** | Ejecutar en un directorio en lugar de todo el repo |
| **Verificar modelo** | `/model` antes de ejecución grande |
| **Pedir modelo pequeño** | Para etapas que no necesitan el modelo más potente |
| **Monitorear tokens** | Vista `/workflows` muestra tokens por agente |
| **Detener temprano** | Se puede detener sin perder trabajo completado |

---

## 13. Deshabilitar Workflows

### Opciones de Deshabilitación

| Método | Alcance | Persistencia |
|--------|---------|--------------|
| `/config` → Dynamic workflows toggle | Usuario | Sesiones futuras |
| `~/.claude/settings.json` → `"disableWorkflows": true` | Usuario | Sesiones futuras |
| `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | Variable de entorno | Mientras esté definida |
| Managed settings → `"disableWorkflows": true` | Organización | Organización |
| Claude Code admin settings | Organización | Organización |

### Efecto de Deshabilitar

- Comandos bundled no disponibles
- Palabra clave `ultracode` no activa workflows
- `ultracode` se elimina del menú `/effort`

---

## 14. Ejemplos Prácticos

### 14.1 Auditoría de Seguridad

```text
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

**Resultado esperado:**
- Script que despacha agentes por cada endpoint
- Cada agente verifica autenticación y autorización
- Resultado consolidado con hallazgos priorizados

### 14.2 Migración de Código

```text
ultracode: migrate all class components to functional components with hooks
```

**Resultado esperado:**
- Script que procesa archivos en batches
- Cada agente migra un subconjunto de archivos
- Verificación de que el código compila después de cada batch

### 14.3 Investigación Cruzada

```text
/depth-research What are the best practices for React state management in 2026?
```

**Resultado esperado:**
- Múltiples búsquedas web desde diferentes ángulos
- Verificación cruzada de fuentes
- Reporte con citations y filtrado de afirmaciones no verificadas

### 14.4 Análisis de Rendimiento

```text
use a workflow to analyze the performance of our database queries and suggest optimizations
```

**Resultado esperado:**
- Agentes analizando diferentes módulos
- Identificación de queries lentas
- Sugerencias de índices y optimizaciones

### 14.5 Code Review Adversarial

```text
ultracode: review the authentication module from security, performance, and maintainability perspectives using independent agents
```

**Resultado esperado:**
- 3 agentes independientes revisando desde diferentes ángulos
- Cada agente no ve los hallazgos de los demás
- Síntesis final con perspectivas múltiples

---

## 15. Buenas Prácticas

### 15.1 Cuándo Usar Workflows

| Situación | Decisión |
|-----------|----------|
| Tarea con 3+ sub-tareas independientes | ✅ Workflow |
| Auditoría de codebase completo | ✅ Workflow |
| Migración de 100+ archivos | ✅ Workflow |
| Cambio simple en un archivo | ❌ Conversación |
| Pregunta rápida | ❌ Conversación |
| Necesitas iteración con usuario | ❌ Conversación |

### 15.2 Optimizar Costos

1. **Probar primero en slice pequeño** → Un directorio en lugar de todo el repo
2. **Usar modelo apropiado** → Haiku para investigación, Sonnet para análisis
3. **Monitorear tokens** → Vista `/workflows` en tiempo real
4. **Detener temprano** → Si el enfoque no funciona

### 15.3 Aprobación Inteligente

- **Proyectos personales:** Usar "Yes, and don't ask again" para workflows recurrentes
- **Producción:** Siempre revisar el script antes de ejecutar
- **CI/CD:** Usar `bypassPermissions` solo en entornos controlados

### 15.4 Reutilización

1. **Guardar workflows exitosos** → Se convierten en comandos `/<nombre>`
2. **Documentar propósitos** → Usar nombres descriptivos
3. **Versionar en control de versiones** → `.claude/workflows/` en el repo

### 15.5 Monitoreo

- **Abrir `/workflows`** durante ejecución para ver progreso
- **Drill-down en fases** para verificar que los agentes van bien
- **Detener si algo va mal** → No esperar a que termine

---

## Referencia Rápida

### Comandos

| Comando | Descripción |
|---------|-------------|
| `/deep-research <question>` | Workflow integrado de investigación |
| `/workflows` | Listar y monitorear ejecuciones |
| `/effort ultracode` | Activar modo ultracode |
| `/effort high` | Desactivar ultracode |

### Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `ultracode` | Activar workflow en prompt |
| `Option+W` / `Alt+W` | Descartar keyword ultracode |
| `Ctrl+G` | Abrir script en editor |
| `Tab` | Ajustar prompt antes de ejecutar |
| `Ctrl+B` | Mover tarea a background |

### Límites

| Límite | Valor |
|--------|-------|
| Agentes concurrentes | 16 |
| Agentes totales por run | 1,000 |
| Input mid-run | No permitido |
| Filesystem directo del script | No permitido |

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `CLAUDE_CODE_DISABLE_WORKFLOWS` | Deshabilitar workflows |

### Guardar Ubicaciones

| Ubicación | Alcance | Visibilidad |
|-----------|---------|-------------|
| `.claude/workflows/` | Proyecto | Equipo |
| `~/.claude/workflows/` | Personal | Solo tú |

---

*Manual generado a partir de la documentación oficial de Claude Code.*
*Última actualización de la fuente: 27 de junio de 2026.*
