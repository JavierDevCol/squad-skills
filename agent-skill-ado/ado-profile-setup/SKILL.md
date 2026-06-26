---
name: ado-profile-setup
description: >
  Crea un nuevo perfil en config_consultas.json. Activa esta skill cuando
  config_consultas.json no exista, el perfil activo este incompleto o invalido,
  o el usuario quiera agregar un nuevo perfil.
  Triggers on: configurar perfil, nuevo perfil, setup agente,
  inicializar, config no existe, >nuevo-perfil.
---
PEDIR NOMBRE PERFIL → NOMBRE
PEDIR EMAIL ADO → EMAIL
PEDIR PROYECTO WORK ITEMS ADO → PROJ_WI
PEDIR Sprint por defecto para consultas → DEFAULT_SPRINT
PEDIR PROYECTO REPOS/PRs ADO → PROJ_REPOS ([=] → copiar PROJ_WI)
PEDIR RUTA ABSOLUTA REPORTES → RUTA
LEER config_consultas.json raiz workspace
NO EXISTE: CREAR JSON PLANTILLA
EXISTE JSON VALIDO: INSERTAR NOMBRE, ACTIVAR NOMBRE, NO MODIFICAR RESTO
EXISTE JSON INVALIDO: PREGUNTAR SOBRESCRIBIR, NO → CANCELAR
ESCRIBIR config_consultas.json 2 ESPACIOS INDENTACION SUSTITUIR VARIABLES:
```json
{
  "perfil_activo": "NOMBRE",
  "perfiles": {
    "NOMBRE": {
      "user_email": "EMAIL",
      "project_map": {
        "workitems": "PROJ_WI",
        "repos": "PROJ_REPOS",
        "pipelines": "PROJ_REPOS",
        "wiki": "PROJ_WI",
        "testplans": "PROJ_WI",
        "default": "PROJ_WI"
      },
      "base_reports_path": "RUTA",
      "default_sprint": "DEFAULT_SPRINT",
      "config_extras": {
        "formato_fecha": "ISO-8601",
        "idioma_reportes": "es"
      }
    }
  }
}
```
CONFIRMAR USUARIO: NOMBRE ACTIVADO, RESUMEN 5 VALORES
