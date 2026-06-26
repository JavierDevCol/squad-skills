---
name: ado-sprint-tracker
description: >
  Seguimiento de sprints en Azure DevOps con protocolo local-first. Usa esta
  skill cuando el usuario quiera consultar su trabajo del sprint activo, ver
  resumen de trabajo, o sincronizar datos del sprint con ADO. También activa
  cuando mencione: mis HUs, mis bugs, estado del sprint, seguimiento, reporte
  de sprint, generar histórico, consultar trabajo, sprint activo, resumen
  de sprint. Also triggers on: sprint tracking, my work items, sprint report,
  sync sprint data.
---
## LOCAL-FIRST
1. BUSCAR index_[nombre].md EN base_reports_path
2. EXISTE <24H: USAR LOCAL
3. EXISTE >24H O USUARIO PIDE actualizar/sincronizar/fresco: IR ADO
4. DATOS ADO: CREAR/ACTUALIZAR SOLO index_[nombre].md
## ARCHIVO UNICO
RUTA: [base_reports_path]/index_[nombre_sprint].md
## CONSULTAR_TRABAJO
FASE A:
1. BUSCAR index_[nombre].md EN base_reports_path
2. EXISTE <24H: MOSTRAR TABLA LOCAL
3. NO EXISTE O >24H: IR FASE B
FASE B (SOLO SIN LOCAL O PIDE UPDATE):
1. LEER default_sprint DEL PERFIL ACTIVO
2. SI default_sprint NO EXISTE O VIENE VACIO: DETENER Y PEDIR CONFIGURAR PERFIL
3. ado/wit_get_work_items_for_iteration USANDO default_sprint + FILTRAR project_name + user_email
4. CLASIFICAR: HUs 📘, Bugs 🐞, Tasks 🧩
FASE C:
1. GENERAR/ACTUALIZAR index_[default_sprint].md CON TABLA:
   | ID | Tipo | Título | Estado | Asignado | Padre |
2. MOSTRAR: TOTAL ITEMS, DESGLOSE HU/BUG/TASK, RATIO SALUD
3. NOTA FRESCURA: timestamp obtención + "usa sincronizar PARA REFRESCAR"
## GENERAR-HISTORICO
1. ado/work_list_iterations → TODAS ITERACIONES
2. POR CADA SPRINT SIN INDEX LOCAL:
   - ado/wit_get_work_items_for_iteration
   - CREAR index_[sprint_name].md
3. >10 SPRINTS SIN DOCUMENTAR: PEDIR CONFIRMACION ANTES PROCEDER
4. MOSTRAR LISTA DE SPRINTS INDEXADOS
## REGLAS
FILTRAR SIEMPRE POR user_email ACTIVO.
SPRINT A CONSULTAR: USAR SIEMPRE default_sprint DEL PERFIL ACTIVO COMO OVERRIDE OBLIGATORIO.
NO CONSULTAR ado/work_list_team_iterations PARA DECIDIR EL SPRINT.
HISTORICO: ORDEN CRONOLOGICO FECHA INICIO.
base_reports_path NO EXISTE: CREAR ANTES ESCRIBIR.
