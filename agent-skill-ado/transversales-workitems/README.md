# Skill: `transversales-workitems`

Gestión de **work items de la célula de temas transversales** de BancaPorWhatsapp (BMM)
en Azure DevOps, conectada en vivo por **MCP**, haciendo cumplir el **protocolo de
incidentes** acordado con el cliente.

Cualquier miembro de la célula puede usar esta skill para **crear**, **actualizar** o
**verificar** que un work item esté alineado al protocolo, sin tener que memorizar las reglas.

---

## ¿Qué hace?

| Modo          | Para qué sirve                                                                                  |
| ------------- | ----------------------------------------------------------------------------------------------- |
| **crear**     | Registra un WI (Bug/Incidente, Task, User Story, Issue) como hijo del **Feature 128821**, recolectando y validando todos los campos del protocolo. Soporta incidentes **nuevos** e incidentes **ya resueltos** (registro retroactivo: queda en estado Resolved/Closed con su sección de Resolución). |
| **actualizar** `<id>` | Modifica un WI existente y, si hace falta, lo enlaza al Feature 128821.                  |
| **verificar** `<id>`  | Audita un WI contra el protocolo y devuelve un reporte ✅/❌ punto por punto.           |

Todos los work items se crean en:

- **Organización:** `GestionRequerimientos`
- **Proyecto:** `FINTIA`
- **Feature padre:** `128821` ([abrir en Azure DevOps](https://dev.azure.com/GestionRequerimientos/FINTIA/_backlogs/backlog/FINTIA%20Team/Epics?workitem=128821))

---

## Requisito MANDATORIO: configurar el MCP de Azure DevOps apuntando a `FINTIA`

Esta skill **no funciona sin** un servidor MCP de Azure DevOps conectado **y apuntando al
proyecto `FINTIA`**.

> 🧭 **Por qué `FINTIA` sí o sí.** En la organización `GestionRequerimientos`, el cliente
> concentra **todos los work items (incidentes, tickets, boards) en un único proyecto: `FINTIA`**.
> El resto de proyectos (p. ej. `BancaPorWhatsappCICD`) son para **soluciones de software**:
> repositorios, pipelines, etc. Por eso el MCP de esta skill **debe** apuntar a `FINTIA`;
> si apunta a otro proyecto, los work items quedarían registrados en el lugar equivocado.

En este repo conviven **dos** servidores MCP de Azure DevOps en `.mcp.json` (raíz del workspace):

| Servidor MCP                | Proyecto (`DEFAULT_PROJECT`) | Para qué                                   | ¿Lo usa esta skill? |
| --------------------------- | ---------------------------- | ------------------------------------------ | ------------------- |
| `bmm-devops-mcp`            | `BancaPorWhatsappCICD`       | Software: repos, pipelines, código         | ❌ No                |
| **`bmm-dashboard-devops-mcp`** | **`FINTIA`**              | **Boards / work items (incidentes)**       | ✅ **Sí**            |

### Cómo está cableada la configuración (PAT personalizado por miembro)

Para **no commitear tokens**, el PAT se separa en dos archivos:

- **`.mcp.json`** (raíz del workspace, **sí se comparte**): declara el servidor, pero el PAT
  es una **variable** `${AZURE_DEVOPS_PAT}` — no un token literal:

  ```jsonc
  // .mcp.json — compartido por el repo (sin secretos)
  {
    "mcpServers": {
      "bmm-dashboard-devops-mcp": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@tiberriver256/mcp-server-azure-devops"],
        "env": {
          "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/GestionRequerimientos",
          "AZURE_DEVOPS_PAT": "${AZURE_DEVOPS_PAT}",
          "AZURE_DEVOPS_DEFAULT_PROJECT": "FINTIA",
          "AZURE_DEVOPS_AUTH_METHOD": "pat"
        }
      }
    }
  }
  ```

- **`.claude/settings.local.json`** (personal de cada quien, **NO se commitea** —
  está en `.gitignore`): aquí cada miembro pone **su propio PAT** y habilita el servidor:

  ```jsonc
  // .claude/settings.local.json — LOCAL, nunca se commitea
  {
    "enabledMcpjsonServers": ["bmm-dashboard-devops-mcp"],
    "env": {
      "AZURE_DEVOPS_PAT": "<TU_PAT_PERSONAL_AQUI>"
    }
  }
  ```

  El valor de `env.AZURE_DEVOPS_PAT` se inyecta en la sesión y `.mcp.json` lo resuelve en
  `${AZURE_DEVOPS_PAT}`. Así el `.mcp.json` queda limpio y cada quien usa su token.

### Pasos para cada miembro de la célula

1. **Generar un PAT propio** en Azure DevOps (org `GestionRequerimientos`) con permisos de
   **Work Items: Read & Write**.
2. Abrir (o crear) tu **`.claude/settings.local.json`** y:
   - poner tu PAT en `env.AZURE_DEVOPS_PAT`;
   - incluir `"bmm-dashboard-devops-mcp"` en `enabledMcpjsonServers`.
   > **Cada quien usa su propio token** — no se comparte ni se commitea.
3. Reiniciar Claude Code / recargar el MCP y verificar la conexión (p. ej. leer el WI 128821).
4. Listo: invocar la skill (ver abajo).

> ⚠️ **Seguridad.** El `AZURE_DEVOPS_PAT` es una credencial personal: vive solo en
> `settings.local.json` (ignorado por git), nunca en `.mcp.json` ni en el chat. Si un token
> estuvo expuesto en texto plano en `.mcp.json`, **rótalo** en Azure DevOps.

---

## Cómo se usa

Invocar por nombre o por frase natural. Ejemplos:

- `/transversales-workitems crear` — y luego describir el incidente.
- "Registra un incidente transversal: error al generar certificados en Portal Clientes…"
- "Verifica el work item 130045 contra el protocolo."
- "Actualiza el WI 130045: súbelo a P1 y enlázalo al Feature transversal."

La skill te pedirá los datos que falten (nunca inventa). Para un **Bug/Incidente** suele pedir:
título, las 3 preguntas de diagnóstico, sistema afectado, ambiente, prioridad (P1–P4),
usuarios afectados, fecha/hora de detección, evidencias, datos del solicitante y responsable.

---

## Estructura de la skill

```
transversales-workitems/
  SKILL.md                       # lógica: modos crear/actualizar/verificar + reglas
  README.md                      # este archivo
  references/
    mapeo-campos.md              # protocolo → campos de Azure DevOps + plantilla HTML + ejemplos MCP
    checklist-protocolo.md       # checklist de cumplimiento + matriz de prioridades + formato de reporte
```

## Fuente de verdad del protocolo

El protocolo completo vive en
[`Doc_BancaPorWhatsapp/docs/procedimientos/protocolo-icidentes.md`](../../../Doc_BancaPorWhatsapp/docs/procedimientos/protocolo-icidentes.md).
Si el cliente actualiza el protocolo, se edita **ese documento** y, si cambian campos o reglas,
se ajustan los `references/` de esta skill.
