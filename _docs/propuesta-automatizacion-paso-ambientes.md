# Propuesta: Agente Automatizador de Paso entre Ambientes

> Basado en `MANUAL_PASO_AMBIENTES.md` y las skills existentes del ecosistema BMM.

---

## 1. Problema

El manual de paso entre ambientes (DEVELOP → DES → PRU → PREPRO → PRO) define ~20 comandos Git manuales que deben ejecutarse secuencialmente. Hoy se hace a mano, con riesgo de:

- Saltarse pasos
- Versión incorrecta de tag
- Fast-forward fallido por no validar precondiciones
- Errores de convención en nombres de tags
- Falta de trazabilidad

---

## 2. Solución Propuesta

Crear un **Agente "release-promoter"** que automatice todo el ciclo de promoción.

### Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                     AGENTE PRIMARIO                          │
│                   release-promoter.agent.md                  │
│                                                              │
│  ├── Conoce MANUAL_PASO_AMBIENTES.md como prompt             │
│  ├── Sabe la correspondencia rama ↔ ambiente                 │
│  ├── Ejecuta git commands (merge --ff-only + tags)           │
│  └── Delega a subagentes según la tarea                      │
└──────────────────────┬───────────────────────────────────────┘
                       │  task tool
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  SUBAGENTES / SKILLS EXISTENTES                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ @ado-repo-   │  │ @ado-pr-     │  │ @ado-pipeline-   │   │
│  │ browser      │  │ creator      │  │ analyzer         │   │
│  │ (listar ramas│  │ (crear PR    │  │ (chequear estado │   │
│  │  y tags)     │  │  handoff)    │  │  del pipeline)   │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ @pr-config-  │  │ @bmm-manual- │  │ @ado-sprint-     │   │
│  │ audit        │  │ tecnico      │  │ tracker          │   │
│  │ (auditar     │  │ (generar     │  │ (consultar       │   │
│  │  config del  │  │  manual      │  │  trabajo del     │   │
│  │  PR/diff)    │  │  técnico)    │  │  sprint)         │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Ciclo de Promoción Automatizable

Cada etapa del manual se traduce a comandos que el agente ejecuta:

| Etapa | Acción del agente | Precondición | Skills involucradas |
|-------|-------------------|-------------|---------------------|
| **3.1** Desarrollo CEIBA | Monitorear merges a `develop` | PR aprobado | `ado-pr-reviewer` |
| **3.2** Crear release | Crear/actualizar `release/vX.Y.Z` desde `develop` con `--ff-only` | develop estable | `ado-repo-browser` |
| **3.2.1** Ajustes post-validación | Aplicar fix en release, back-merge a develop | Bug reportado | Git directo |
| **3.2.2** Eliminar release branch | `git branch -d` + `git push --delete` | Aprobación en DES | `ado-repo-browser` |
| **3.3** DES → PRU | `git checkout pru && git merge --ff-only vX.Y.Z && git tag vX.Y.Z-pru` | Tag vX.Y.Z existe | Git directo |
| **3.4** PRU → PREPRO | `git checkout prepro && git merge --ff-only vX.Y.Z-pru && git tag vX.Y.Z-prepro` | Tag -pru existe | Git directo |
| **3.5** PREPRO → PRO | `git checkout main && git merge --ff-only vX.Y.Z-prepro && git tag vX.Y.Z-pro` | Tag -prepro existe | Git directo |
| **5.1** Hotfix en DES | Aplicar fix en release, merge a des + develop, tag vX.Y+1 | Bug en DES | Git directo |
| **5.2** Hotfix en PRU+ | Desde tag, hotfix branch, merge top-down, re-tag | Bug en PRU/PRO | Git directo |

---

## 4. Comandos del Agente (Interface de Usuario)

```
> release crear v1.2.3
  → Crea release/v1.2.3 desde develop, valida ff-only

> release promover v1.2.3 --to pru
  → Ejecuta §3.3: merge ff-only + tag v1.2.3-pru

> release promover v1.2.3 --to prepro
  → Ejecuta §3.4: merge ff-only + tag v1.2.3-prepro

> release promover v1.2.3 --to pro
  → Ejecuta §3.5: merge ff-only + tag v1.2.3-pro

> release hotfix v1.2.4 --env des --fix "corregir X"
  → Ejecuta §5.1

> release hotfix v1.2.4 --env pru --fix "corregir Y"
  → Ejecuta §5.2

> release estado
  → Muestra qué versión está en cada ambiente (usa tags)

> release rollback v1.2.3 --env des
  → Ejecuta §9.1: git revert + tag rollback

> release audit v1.2.3
  → Delega a pr-config-audit para auditar el diff del release
```

---

## 5. Skill Propuesta: `release-promoter`

```markdown
---
name: release-promoter
description: >
  Automatiza la promoción de releases entre ambientes (DEVELOP → DES → PRU → PREPRO → PRO)
  siguiendo el manual de paso entre ambientes de BMM. Úsala cuando necesites crear un release,
  promover entre ambientes, aplicar hotfixes, auditar configuración de un PR de release,
  generar release notes o consultar el estado actual de cada ambiente.
  También cuando te pidan "pasar a des", "promover a pru", "aplicar hotfix", "crear tag",
  "release notes" o "qué versión está en cada ambiente".
---
```

### Prompt base del agente

El agente debe tener en su system prompt el contenido completo del `MANUAL_PASO_AMBIENTES.md` como fuente de verdad.

### Permisos

```yaml
permission:
  bash:
    "git *": allow
    "git push origin --delete *": ask
    "git push origin --tags": ask
  skill:
    "pr-config-audit": allow
    "bmm-manual-tecnico": allow
    "ado-*": allow
```

---

## 6. Casos de Uso Detallados

### 6.1 Creación de Release (CEO → banco)

1. Usuario: `release crear v1.2.3`
2. Agente verifica que `develop` y `release/v1.2.3` no existen o están en mismo commit
3. Ejecuta `git fetch`, crea/actualiza rama, valida `--ff-only`
4. Delega a `bmm-manual-tecnico` si se necesita el manual técnico
5. Delega a `pr-config-audit` para auditar el diff del release contra `des`
6. Informa al usuario resumen: `release/v1.2.3 creada → lista para handoff`

### 6.2 Promoción con confirmación

1. Usuario: `release promover v1.2.3 --to pru`
2. Agente valida: tag `v1.2.3` existe, `pru` existe
3. Muestra preview: `merge ff-only v1.2.3 → pru → tag v1.2.3-pru`
4. Pide confirmación (previene accidentes)
5. Ejecuta los comandos
6. Si falla `--ff-only`, se detiene y explica por qué

### 6.3 Hotfind en PRU

1. Usuario: `release hotfix v1.2.4 --env pru --fix "corregir timeout"`
2. Agente lee §5.2 del manual
3. Crea `hotfix/arreglo-timeout` desde `v1.2.3-pru`
4. Aplica fix, mergea a `main`, luego cascada a `prepro` → `pru` → `des` → `develop`
5. Crea tags: `v1.2.4-pro`, `v1.2.4-prepro`, `v1.2.4-pru`, `v1.2.4`

---

## 7. Trazabilidad

Tras cada operación, el agente registra en un archivo `RELEASE_HISTORIAL.md`:

```markdown
| Fecha       | Versión | Acción      | De          | A         | Ejecutor |
|-------------|---------|-------------|-------------|-----------|----------|
| 2026-06-25  | v1.2.3  | Create      | develop     | release/  | agente   |
| 2026-06-26  | v1.2.3  | Promote     | DES         | PRU       | agente   |
| 2026-06-27  | v1.2.4  | Hotfix      | v1.2.3-pru  | PRO       | agente   |
```

---

## 8. Implementación

### Archivos a crear

```
.opencode/agents/release-promoter.agent.md     # Agente orquestador
.opencode/skills/release-promoter/SKILL.md     # Skill con instrucciones detalladas
```

### Dependencias

- Acceso al repositorio Git del proyecto (las skills ADO ya lo proveen)
- Las skills ya existentes: `agent-skill-ado/*`, `pr-config-audit`, `bmm-manual-tecnico`
- `MANUAL_PASO_AMBIENTES.md` como recurso referenciable

### Beneficios

- **Ejecución consistente**: mismos comandos siempre, sin errores humanos
- **Validación automática**: precondiciones antes de cada paso
- **Trazabilidad**: registro automático de cada promoción
- **Rapidez**: de minutos a segundos por operación
- **Integración**: reusa las skills ADO ya construidas para consultar estado, PRs, etc.

---

## 9. Optimización Futura

Una vez validado el agente, se podría extender para:

- **Pipeline integrado**: que el agente monitoree el pipeline de Azure DevOps y promueva automáticamente cuando el Quality Gate pase
- **Notificaciones**: que avise al banco cuando el release esté listo
- **Dashboard**: generación de reporte visual del estado de cada ambiente
- **Rollback automático**: revertir a versión anterior si el health check falla post-promoción
