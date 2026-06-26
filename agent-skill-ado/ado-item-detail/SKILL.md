---
name: ado-item-detail
description: >
  Extracción y consulta detallada de ítems individuales de Azure DevOps
  (User Stories, Bugs, Tasks). Busca ítems por ID o palabra clave con
  protocolo local-first sobre el index. Usa esta skill cuando el usuario
  pida ver el detalle de un ítem, buscar una tarea, o consultar información
  de un work item. También activa cuando mencione: detalle ítem, detalle HU,
  ver bug, buscar tarea, información de la tarea. Also triggers on: item
  detail, work item info, search task, task detail.
---

Contexto del perfil activo

Esta skill recibe del agente orquestador el contexto ya resuelto:
- project_name — proyecto ADO resuelto desde project_map.workitems
- user_email — email del perfil activo
- base_reports_path — ruta base de reportes

La skill no lee config_consultas.json directamente. Todo el contexto es inyectado por el agente.

Protocolo Local-First

1. BUSCAR index_[nombre].md EN base_reports_path
2. BUSCAR EN LA TABLA POR ID O PALABRA CLAVE EN TITULO
3. ENCONTRADO: MOSTRAR DATOS BASICOS (ID, TIPO, TITULO, ESTADO, ASIGNADO, PADRE)
4. NO ENCONTRADO O USUARIO PIDE DETALLE COMPLETO: IR ADO

Comando: DETALLE_ITEM [ID o Palabra_Clave]

Fase A — Búsqueda en Index Local

1. Busca en index_[nombre].md por [ID] o palabra clave en la columna Título.
2. Si se encuentra:
   - Muestra resumen básico desde la tabla del index
   - Pregunta: "¿Quieres el detalle completo desde ADO? [S]/[N]"
3. Si no se encuentra o usuario quiere detalle completo:
   - Invoca ado/wit_get_work_item con el ID (si es ID)
   - Invoca ado/search_workitem por palabra clave (si es palabra)

Fase B — Extracción desde ADO

1. Invoca ado/wit_get_work_item o ado/search_workitem según corresponda.
2. Extrae:
   - Descripción — limpia de HTML, convierte a Markdown
   - Criterios de Aceptación — lista de checkboxes
   - Estimación — Story Points si aplica
   - Comentarios — fecha, usuario y texto
   - Relaciones — Padre, hijos

Fase C — Resultado

Muestra detalle completo en el chat (NO genera archivos individuales).

Fase D — Actualización del Index

Si el WI no estaba en el index:
- Agrega entrada a index_[nombre].md: ID, Tipo, Título, Estado, Asignado, Padre

Comando: BUSCAR-TAREA [ID o Palabra_Clave]

1. Busca en index_[nombre].md por ID o palabra clave en Título.
2. Encontrado: muestra snippet:
   | ID | Tipo | Título | Estado | Asignado | Padre |
3. No encontrado: invoca ado/search_workitem y muestra resultados.
4. Pregunta si agregar al index los no registrados.

Gotchas

- Descripciones de ADO vienen en HTML. Limpiar antes de mostrar.
- Buscar por palabra clave en Título Y Descripción.
- Si la palabra clave devuelve múltiples resultados, listar opciones y preguntar.
- No crear archivos individuales de detalle. Solo el index.
