---
name: ado-task-creator
description: >
  Creación de tareas hijas en Azure DevOps en dos fases: diseño local desde un
  archivo de contexto técnico, y sincronización batch con ADO. Analiza documentos
  para proponer subtareas, valida contra la HU padre, y crea work items vinculados.
  Usa esta skill cuando el usuario quiera agregar tareas a una User Story, crear
  tareas desde un documento técnico, planificar subtareas, o desglosar una HU en
  trabajo ejecutable. También activa cuando mencione: agregar tareas, crear
  subtareas, desglosar HU, agg-tarea, plan de trabajo, crear tareas desde archivo.
  Also triggers on: create child tasks, batch task creation, break down user story.
---

# ADO Task Creator

Creación de tareas hijas en Azure DevOps con flujo de dos fases: diseño local (cero consumo ADO) y sincronización batch.

## Contexto del perfil activo

Esta skill recibe del agente orquestador el contexto ya resuelto:
- `project_name` — proyecto ADO resuelto desde `project_map.workitems`
- `user_email` — email del perfil activo
- `base_reports_path` — ruta base de reportes
- `config_extras` — para reglas dinámicas de estimación, formato, etc.

La skill **no lee `config_consultas.json` directamente**. Todo el contexto es inyectado por el agente.

## Comando: AGG-TAREA [HU_ID] [archivo_contexto]

### Fase 1 — Diseño y Simulación Local (Cero Consumo ADO)

**A. Análisis de Contexto:**
1. Lee el `[archivo_contexto]` con `read/readFile`.
2. Identifica los pasos técnicos, componentes o acciones discretas que constituyen subtareas.

**B. Validación de Identidad:**
1. Busca en `index_[nombre].md` si el `HU_ID` existe y es de tipo `User Story`.
2. Si no está en el index, consulta `ado/wit_get_work_item` para validar la HU padre.

**C. Propuesta de Plan de Trabajo:**
Presenta en el chat una tabla con las tareas detectadas:

| # | Título | Descripción sugerida | Estimación |
|---|--------|---------------------|------------|
| 1 | [Título] | [Descripción] | [Horas/Puntos según config_extras] |

**D. Interacción por Ambigüedad:**
Si un punto del documento es vago, el agente se detiene.

### Fase 2 — Confirmación y Creación en Lote (Batch Sync)

Tras validar todos los puntos, presenta el resumen y pregunta:
> **[S]** Sí, crear todas | **[E]** Editar lista | **[A]** Abortar

**Si el usuario elige [S]:**
1. Invoca `ado/wit_create_work_item` para cada tarea con:
   - `System.Title` — Título de la tarea
   - `System.Description` — Descripción
   - Relación `Parent` → `HU_ID`
   - `System.AssignedTo` → `user_email` del perfil activo
   - Campos adicionales según `config_extras`
2. Recoge los IDs reales devueltos por ADO.

### Fase 3 — Registro en Index

1. Agrega cada tarea creada al `index_[nombre].md` con:
   | ID | Tipo | Título | Estado | Asignado | Padre |
   - Tipo: siempre `Task`
   - Padre: `[HU_ID]`
2. No crear archivos individuales de detalle.

## Gotchas

- **NUNCA crees tareas en ADO sin confirmación explícita [S].**
- Si una tarea falla en batch, continúa con las siguientes y reporta errores al final.
- Verifica que `HU_ID` sea `User Story`. Si es Bug, informa pero permite continuar.
- Siempre incluir el `Padre: [HU_ID]` en la entrada del index para las tasks hijas.
