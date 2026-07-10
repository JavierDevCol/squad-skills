Aquí están todas las 90 tools del MCP ADO agrupadas por categoría:

---
🔐 Advanced Security (advsec)

┌──────────────────────────┬────────────────────────────────────────────────────────────────────────────────
│           Tool           │                                             Descripción                                             │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ advsec_get_alerts        │ Obtiene alertas de seguridad avanzada de un repositorio (dependencias, secretos, código, licencias) │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ advsec_get_alert_details │ Obtiene detalles de una alerta específica de seguridad avanzada                                     │
└──────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┘

---
🏢 Core / Organización (core)

┌─────────────────────────┬────────────────────────────────────────────────────────────┐
│          Tool           │                        Descripción                         │
├─────────────────────────┼────────────────────────────────────────────────────────────┤
│ core_list_projects      │ Lista los proyectos de la organización en Azure DevOps     │
├─────────────────────────┼────────────────────────────────────────────────────────────┤
│ core_list_project_teams │ Lista los equipos de un proyecto                           │
├─────────────────────────┼────────────────────────────────────────────────────────────┤
│ core_get_identity_ids   │ Obtiene IDs de identidad (por nombre, email, display name) │
└─────────────────────────┴────────────────────────────────────────────────────────────┘

---
🚀 Pipelines / Builds (pipelines)

┌──────────────────────────────────────────┬─────────────────────────────────────────────────────────────────┐
│                   Tool                   │                           Descripción                           │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_create_pipeline                │ Crea una definición de pipeline con configuración YAML          │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_run_pipeline                   │ Inicia una nueva ejecución de un pipeline                       │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_run                        │ Obtiene una ejecución específica de un pipeline                 │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_list_runs                      │ Lista hasta 10.000 ejecuciones de un pipeline                   │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────
│ pipelines_get_builds                     │ Lista builds de un proyecto con múltiples filtros               │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_build_status               │ Obtiene el estado de un build específico                        │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────
│ pipelines_get_build_log                  │ Obtiene los logs de un build                                    │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_build_log_by_id            │ Obtiene un log específico de un build por su ID                 │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_build_changes              │ Obtiene los cambios asociados a un build                        │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_build_definitions          │ Lista definiciones de build de un proyecto                      │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_get_build_definition_revisions │ Lista las revisiones de una definición de build                 │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_update_build_stage             │ Actualiza el estado de una stage de un build (Cancel/Retry/Run) │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_list_artifacts                 │ Lista los artefactos de un build                                │
├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ pipelines_download_artifact              │ Descarga un artefacto de pipeline                               │
└──────────────────────────────────────────┴─────────────────────────────────────────────────────────────────┘

---
🌿 Repositorios / Git (repo)

┌───────────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
│             Tool              │                               Descripción                               │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_list_repos_by_project    │ Lista repositorios de un proyecto                                       │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_get_repo_by_name_or_id   │ Obtiene un repositorio por nombre o ID                                  │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_list_directory           │ Lista archivos y carpetas dentro de un directorio del repo              │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_get_file_content         │ Obtiene el contenido de un archivo en una rama, tag o commit específico │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_create_branch            │ Crea una nueva rama en el repositorio                                   │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_get_branch_by_name       │ Obtiene una rama por su nombre                                          │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_list_branches_by_repo    │ Lista todas las ramas de un repositorio                                 │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_list_my_branches_by_repo │ Lista las ramas propias del usuario autenticado                         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ repo_search_commits           │ Busca commits con filtros por texto, fecha, autor, rama, etc.           │
└───────────────────────────────┴─────────────────────────────────────────────────────────────────────────┘

---
🔀 Pull Requests (repo — PR)

┌────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
│                    Tool                    │                            Descripción                            │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_create_pull_request                   │ Crea un nuevo pull request                                        │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_get_pull_request_by_id                │ Obtiene un PR por su ID                                           │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_list_pull_requests_by_repo_or_project │ Lista PRs de un repositorio o proyecto con filtros                │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_list_pull_requests_by_commits         │ Lista PRs que contienen commits específicos                       │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_get_pull_request_changes              │ Obtiene el diff de archivos cambiados en un PR                    │
├────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ repo_update_pull_request                   │ Actualiza un PR (título, descripción, estado, autocomplete, etc.) │
├────────────────────────────────────────────┼──────────────────────────────────────────────────────────────
───────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ repo_create_pull_request_thread        │ Crea un nuevo hilo de comentario en un PR                      │
├────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ repo_list_pull_request_threads         │ Lista los hilos de comentarios de un PR                        │
├────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ repo_list_pull_request_thread_comments │ Lista los comentarios de un hilo específico                    │
├────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ repo_reply_to_comment                  │ Responde a un comentario en un hilo de PR                      │
├────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ repo_update_pull_request_thread        │ Actualiza el estado de un hilo (Active / Fixed / Closed, etc.) │
└────────────────────────────────────────┴────────────────────────────────────────────────────────────────┘

---
🔍 Búsqueda Global (search)

┌─────────────────┬────────────────────────────────────────────────────────────────────────┐
│      Tool       │                              Descripción                               │
├─────────────────┼────────────────────────────────────────────────────────────────────────┤
│ search_code     │ Busca texto en repositorios de código                                  │
├─────────────────┼────────────────────────────────────────────────────────────────────────┤
│ search_wiki     │ Busca texto en páginas de wiki                                         │
├─────────────────┼────────────────────────────────────────────────────────────────────────┤
│ search_workitem │ Busca work items por texto con filtros de estado, tipo, asignado, etc. │
└─────────────────┴────────────────────────────────────────────────────────────────────────┘

---
🧪 Planes de Prueba (testplan)

┌──────────────────────────────────────────┬────────────────────────────────────────────────────────────────────┐
│                   Tool                   │                            Descripción                             │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_create_test_plan                │ Crea un nuevo plan de pruebas                                      │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_list_test_plans                 │ Lista los planes de prueba de un proyecto                          │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_create_test_suite               │ Crea una suite de pruebas dentro de un plan                        │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_list_test_suites                │ Lista las suites de un plan de pruebas                             │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_create_test_case                │ Crea un nuevo caso de prueba (work item)                           │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_list_test_cases                 │ Lista los casos de prueba de una suite                             │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_add_test_cases_to_suite         │ Agrega casos de prueba existentes a una suite                      │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_update_test_case_steps          │ Actualiza los pasos de un caso de prueba existente                 │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ testplan_show_test_results_from_build_id │ Obtiene resultados de pruebas de un build (con filtro por outcome) │
└──────────────────────────────────────────┴────────────────────────────────────────────────────────────────────┘

---
📖 Wiki (wiki)

┌────────────────────────────┬─────────────────────────────────────────────────────────┐
│            Tool            │                       Descripción                       │
├────────────────────────────┼─────────────────────────────────────────────────────────┤
│ wiki_list_wikis            │ Lista todos los wikis de la organización o proyecto     │
_create_or_update_page │ Crea o actualiza una página wiki con contenido Markdown │
└────────────────────────────┴─────────────────────────────────────────────────────────┘

---
📋 Work Items (wit)

┌────────────────────────────────────┬───────────────────────────────────────────────────────────────────────┐
│                Tool                │                              Descripción                              │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_create_work_item               │ Crea un nuevo work item (Bug, Task, HU, etc.)                         │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_work_item                  │ Obtiene un work item por ID                                           │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_work_items_batch_by_ids    │ Obtiene múltiples work items por IDs en batch                         │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_update_work_item               │ Actualiza campos de un work item por ID                               │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_update_work_items_batch        │ Actualiza múltiples work items en batch                               │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_my_work_items                  │ Lista work items asignados al usuario autenticado                     │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_query_by_wiql                  │ Ejecuta una consulta WIQL y retorna work items                        │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_query                      │ Obtiene una query guardada por ID o ruta                              │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_query_results_by_id        │ Ejecuta una query guardada y retorna sus resultados                   │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_work_item_type             │ Obtiene la definición de un tipo de work item                         │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_work_items_for_iteration   │ Lista work items de una iteración específica                          │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_get_work_item_attachment       │ Descarga un adjunto de un work item (imágenes, archivos)              │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_add_work_item_comment          │ Agrega un comentario a un work item                                   │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_update_work_item_comment       │ Actualiza un comentario existente en un work item                     │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_list_work_item_comments        │ Lista los comentarios de un work item                                 │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_list_work_item_revisions       │ Lista el historial de revisiones de un work item                      │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_add_child_work_items           │ Crea work items hijos bajo un padre específico                        │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_work_items_link                │ Vincula work items entre sí en batch                                  │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_work_item_unlink               │ Elimina vínculos de un work item                                      │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_add_artifact_link              │ Agrega links de artefactos (repos, branches, commits, builds) a un WI │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_link_work_item_to_pull_request │ Vincula un work item a un pull request                                │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_list_backlogs                  │ Lista los backlogs disponibles de un equipo                           │
├────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ wit_list_backlog_work_items        │ Lista work items de una categoría de backlog específica               │
└────────────────────────────────────┴───────────────────────────────────────────────────────────────────────┘

---
📅 Iteraciones y Capacidad (work)

┌───────────────────────────────┬─────────────────────────────────────────────────────────────────────┐
│             Tool              │                             Descripción                             │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_list_iterations          │ Lista todas las iteraciones de un proyecto                          │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_list_team_iterations     │ Lista las iteraciones de un equipo (con filtro de timeframe)        │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_create_iterations        │ Crea nuevas iteraciones en un proyecto                              │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_assign_iterations        │ Asigna iteraciones existentes a un equipo                           │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_get_team_settings        │ Obtiene la configuración del equipo (iteración default, área, etc.) │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_get_team_capacity        │ Obtiene la capacidad de un equipo para una iteración                │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_get_iteration_capacities │ Obtiene la capacidad de todos los equipos en una iteración          │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
│ work_update_team_capacity     │ Actualiza la capacidad de un miembro del equipo en una iteración    │
└───────────────────────────────┴─────────────────────────────────────────────────────────────────────┘

---
Total: 90 tools distribuidas en 9 categorías.