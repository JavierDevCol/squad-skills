# Propuesta: Agente de Handoff CEIBA → BANCO (Develop → Release → DES)

> Enfoque exclusivo en la responsabilidad de CEIBA: preparación del release y entrega al banco.

---

## 1. Alcance

Este agente cubre **solamente** el tramo que CEIBA gestiona:

```
develop ──► release/vX.Y.Z ──► handoff al BANCO (banco crea PR a des + tag)
```

**Qué NO cubre** (responsabilidad del banco): creación del PR de release → des, merge a des, tagging vX.Y.Z, ni promociones DES→PRU→PREPRO→PRO.

---

## 2. Menú Principal del Agente

Al invocar la skill, el agente presenta un menú con 2 opciones:

```
╔══════════════════════════════════════════════════════════╗
║          HANDOFF CEIBA → BANCO                          ║
║                                                        ║
║  ¿Qué tipo de entrega necesitas preparar?               ║
║                                                        ║
║  [1] Entregar release desde DEVELOP                     ║
║      → La feature ya está integrada en develop via PR   ║
║      → El agente crea release/vX.Y.Z desde develop      ║
║                                                        ║
║  [2] Entregar release desde feature/fix/hotfix          ║
║      → El código NO está en develop o ya hay release    ║
║      → El agente determina el flujo según el caso       ║
║                                                        ║
╚══════════════════════════════════════════════════════════╝
```

---

## 3. Opción 1: Entregar release desde DEVELOP

**Cuándo elegir:** La feature ya fue integrada a develop mediante PR aprobado. El release se construye desde develop siguiendo el manual §3.2.

### Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                    CEIBA (este agente)                          │
│                                                                 │
│  1. Verificar estado de develop (pipeline OK, quality gate OK)  │
│  2. Preguntar versión: "¿vX.Y.Z?"                              │
│  3. Crear o actualizar release/vX.Y.Z desde develop (--ff-only) │
│  4. Validar que develop y release apuntan al mismo commit       │
│  5. Generar release-notes.md (git log desde el tag anterior)    │
│  6. EJECUTAR pr-config-audit → CONFIG_ENTORNO_PR_{ID}.md       │
│  7. Ejecutar checklist de entrega (§10 del manual)              │
│  8. Mostrar resumen final para entregar al banco                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼  (banco toma el control)
                    ┌──────────────────────────────────────────┐
                    │  BANCO: crea PR release/vX.Y.Z → des,   │
                    │  mergea, tag vX.Y.Z, despliega en DES   │
                    └──────────────────────────────────────────┘
```

### Ejemplo completo — Opción 1 desde DEVELOP

```
> handoff

╔══════════════════════════════════════════════════════════╗
║  [1] Entregar release desde DEVELOP                      ║
║  [2] Entregar release desde feature/fix/hotfix            ║
╚══════════════════════════════════════════════════════════╝
Selecciona una opción: 1

¿Qué versión corresponde a este release? (ej: v1.2.3): v1.2.3

═══════════════════════════════════════════════════════════
 Paso 1/5 — Verificar develop
═══════════════════════════════════════════════════════════

✓ git fetch origin
✓ develop actualizado
✓ Último commit: a1b2c3d4 — "feat: simulación de CDTs" (WA2-042)
  Autor: María Pérez  |  Fecha: 2026-06-25 14:30

 ¿El pipeline de develop pasó correctamente? [S/N]: S

═══════════════════════════════════════════════════════════
 Paso 2/5 — Crear release/v1.2.3 desde develop
═══════════════════════════════════════════════════════════

 CASO A — release/v1.2.3 NO existe, creando desde develop

✓ git checkout -b release/v1.2.3 (basado en a1b2c3d4)
✓ git push origin release/v1.2.3

═══════════════════════════════════════════════════════════
 Paso 3/5 — Validar mismo commit
═══════════════════════════════════════════════════════════

✓ develop:       a1b2c3d4
✓ release/v1.2.3: a1b2c3d4
✓ Coinciden — release listo para handoff

═══════════════════════════════════════════════════════════
 Paso 4/5 — Generar artefactos
═══════════════════════════════════════════════════════════

 ✓ release-notes.md generado
   git log v1.2.1..v1.2.3 --oneline --no-merges
   Incluye: WA2-042, WA2-039, WA2-035

 ➜ Ejecutando @pr-config-audit sobre diff develop..release/v1.2.3...
 ✓ CONFIG_ENTORNO_PR_4488.md generado

   Resumen de configuración detectada:
   ┌──────────────────────┬──────────────────────────────────┐
   │ Variables pipeline   │ DOCKER_REGISTRY (nuevo)          │
   │                      │ K8S_REPLICAS: 1→2 (modificado)   │
   ├──────────────────────┼──────────────────────────────────┤
   │ Variables runtime    │ DB_CONNECTION (nueva → Vault)    │
   │                      │ API_TIMEOUT (nueva → VG)         │
   ├──────────────────────┼──────────────────────────────────┤
   │ Colas RabbitMQ       │ queue.simulacion.entrada (nueva) │
   │                      │ queue.simulacion.salida (nueva)  │
   ├──────────────────────┼──────────────────────────────────┤
   │ Migraciones BD       │ V42__crear_tabla_simulacion.sql  │
   └──────────────────────┴──────────────────────────────────┘

═══════════════════════════════════════════════════════════
 Paso 5/5 — Checklist de entrega (§10)
═══════════════════════════════════════════════════════════

 ➜ Consultando último build en develop via @ado-pipeline-analyzer...
 ✓ Build #12345 — Resultado: succeeded
 ✓ Stage "Test": 286/286 tests OK (100%)
 ✓ Stage "SonarQube": Quality Gate passed
 ✓ Stage "DAST": 0 High, 0 Critical
 ✓ Stage "Coverage": 83.2% (≥ 80%)

[✓] Release branch creado desde develop
[✓] develop y release apuntan al mismo commit
[✗] Versión actualizada en artefactos → PENDIENTE
    → Revisa build.gradle: ¿la versión ya se actualizó a 1.2.3?
[✓] Release notes generados
[✓] Pruebas unitarias ejecutadas (100% OK)             ← pipeline
[✓] Cobertura ≥ 80% verificada (83.2%)                 ← pipeline
[✓] DAST ejecutado (0 High/Critical)                   ← pipeline
[✓] SonarQube Quality Gate passed                      ← pipeline
[✓] CONFIG_ENTORNO_PR generado
[✓] Artefactos listos para entregar al banco

 ¿Quieres continuar o revisar algo antes del resumen final?
 [C] Continuar  [R] Revisar  [A] Abortar: C

═══════════════════════════════════════════════════════════
 RESUMEN FINAL — Handoff v1.2.3
═══════════════════════════════════════════════════════════

✅ Handoff preparado. Entregar al banco:

📦 Artefactos entregados:
  ├── Rama:        release/v1.2.3 (push a origin)
  ├── release-notes.md
  └── CONFIG_ENTORNO_PR_4488.md

📋 Release notes (v1.2.3 — 2026-06-25):
  • [WA2-042] Simulación de CDTs
  • [WA2-039] Corrección en flujo de autenticación
  • [WA2-035] Refactor de servicio de notificaciones

🔧 Configuración nueva (ver CONFIG_ENTORNO_PR_4488.md):
  • 3 stages en pipeline, 2 variables runtime nuevas
  • 2 colas RabbitMQ, 1 migración BD (Flyway V42)
  • Revisar Vault: crear secret ms-banca-cdts/des/db-connection

👉 El banco debe:
  1. Crear PR de release/v1.2.3 → des
  2. Mergear el PR a des
  3. Taggear v1.2.3 en des
  4. Desplegar en DES
  5. Crear secrets en Vault según CONFIG_ENTORNO_PR
```

---

## 4. Opción 2: Entregar release desde feature/fix/hotfix

**Cuándo elegir:** El código aún no está en develop o ya existe un release previo con ajustes solicitados.

Al seleccionar esta opción, el agente pregunta para determinar el sub-caso:

```
╔══════════════════════════════════════════════════════════╗
║  ¿Cuál es el origen del cambio?                          ║
║                                                        ║
║  [a] feature/fix → No está en develop                   ║
║      El agente crea PR feature → develop                ║
║      y avisa que al aprobarse use Opción 1              ║
║                                                        ║
║  [b] hotfix → Release ya entregado al banco             ║
║      El banco solicitó ajustes sobre el release vivo    ║
║      El agente aplica fix sobre release + back-merge    ║
║                                                        ║
╚══════════════════════════════════════════════════════════╝
```

### 4a. Sub-caso feature/fix → develop

El cambio está en una rama `feature/WA2-xxx` o `fix/xxx` que aún no se ha integrado a develop.

**Flujo:**

```
rama feature/fix ──► PR → develop ──► (usuario espera aprobación) ──► Opción 1
```

### Ejemplo completo — Opción 2a desde feature/fix

```
> handoff

╔══════════════════════════════════════════════════════════╗
║  [1] Entregar release desde DEVELOP                      ║
║  [2] Entregar release desde feature/fix/hotfix            ║
╚══════════════════════════════════════════════════════════╝
Selecciona una opción: 2

╔══════════════════════════════════════════════════════════╗
║  ¿Cuál es el origen del cambio?                          ║
║                                                        ║
║  [a] feature/fix → No está en develop                   ║
║  [b] hotfix → Release ya entregado al banco             ║
╚══════════════════════════════════════════════════════════╝
Selecciona una opción: a

═══════════════════════════════════════════════════════════
 Feature/Fix — Preparar integración a develop
═══════════════════════════════════════════════════════════

¿Cuál es el nombre de tu rama? (ej: feature/WA2-042): feature/WA2-042
¿Qué versión tendrá el release? (ej: v1.2.3): v1.2.3

✓ git fetch origin
✓ feature/WA2-042 existe en origin
✓ develop actualizado

 ¿Quieres que genere el CONFIG_ENTORNO_PR del diff de tu rama ahora?
 [S] Sí, para ir adelantando  [N] No, lo haré cuando esté en develop: S

 ➜ Ejecutando @pr-config-audit sobre diff develop..feature/WA2-042...
 ✓ CONFIG_ENTORNO_PR_4491.md generado (preview)

   Resumen de configuración detectada:
   ┌──────────────────────┬──────────────────────────────────┐
   │ Variables runtime    │ DB_CONNECTION (nueva → Vault)    │
   │                      │ API_TIMEOUT (nueva → VG)         │
   ├──────────────────────┼──────────────────────────────────┤
   │ Colas RabbitMQ       │ queue.simulacion.entrada (nueva) │
   │                      │ queue.simulacion.salida (nueva)  │
   ├──────────────────────┼──────────────────────────────────┤
   │ Migraciones BD       │ V42__crear_tabla_simulacion.sql  │
   └──────────────────────┴──────────────────────────────────┘

✓ Creando PR de feature/WA2-042 → develop...
✓ PR #4491 creado
  Link: https://dev.azure.com/GestionRequerimientos/BancaPorWhatsappCICD/_git/ms-banca-cdts/pullrequest/4491

  Título: "Release v1.2.3 — Simulación de CDTs"
  Descripción:
    ## Release v1.2.3
    Feature: WA2-042 — Simulación de CDTs
    Release branch: release/v1.2.3 (se creará post-merge)
    
    🔧 Configuración nueva requerida:
    • Vault: ms-banca-cdts/db-connection (runtime)
    • VG ms-banca-cdts-des: API_TIMEOUT
    • Colas: queue.simulacion.entrada, queue.simulacion.salida
    • Flyway: V42__crear_tabla_simulacion.sql
    Ver detalle en: CONFIG_ENTORNO_PR_4491.md (generado, pendiente de merge)

📌 Instrucciones para continuar:
  1. ✓ CONFIG_ENTORNO_PR_4491.md generado (preview)
  2. Solicita la aprobación del PR #4491
  3. Una vez mergeado a develop, ejecuta NUEVAMENTE este agente
     y selecciona la Opción 1 "Entregar release desde DEVELOP"
     usando la versión v1.2.3

⚠️ El CONFIG_ENTORNO_PR se generó con el diff actual. 
   Al mergear a develop pueden aparecer cambios adicionales.
   Se regenerará al ejecutar la Opción 1.
```

### 4b. Sub-caso hotfix → ajustes sobre release existente (§3.2.1)

El release ya fue entregado al banco, está en validación en DES, y el banco solicitó ajustes. El agente aplica el fix directamente sobre el release branch vivo y hace back-merge a develop.

**Flujo:**

```
release/vX.Y.Z (vivo) ──► aplicar fix ──► back-merge a develop
```

### Ejemplo completo — Opción 2b hotfix post-entrega (§3.2.1)

```
> handoff

╔══════════════════════════════════════════════════════════╗
║  [1] Entregar release desde DEVELOP                      ║
║  [2] Entregar release desde feature/fix/hotfix            ║
╚══════════════════════════════════════════════════════════╝
Selecciona una opción: 2

╔══════════════════════════════════════════════════════════╗
║  ¿Cuál es el origen del cambio?                          ║
║                                                        ║
║  [a] feature/fix → No está en develop                   ║
║  [b] hotfix → Release ya entregado al banco             ║
╚══════════════════════════════════════════════════════════╝
Selecciona una opción: b

═══════════════════════════════════════════════════════════
 Hotfix — Ajuste sobre release entregado al banco
═══════════════════════════════════════════════════════════

¿Cuál es la versión del release activo? (ej: v1.2.3): v1.2.3

✓ Verificando que release/v1.2.3 existe...
✓ release/v1.2.3 existe en origin (commit: b2c3d4e5)

¿Qué ajuste solicitó el banco?
 Describe el cambio: Corregir formato de fecha en respuesta de simulación
 El banco reportó que la fecha llega en formato ISO en vez de DD/MM/YYYY

═══════════════════════════════════════════════════════════
 Paso 1/3 — Aplicar fix sobre release/v1.2.3
═══════════════════════════════════════════════════════════

✓ git checkout release/v1.2.3
✓ git pull origin release/v1.2.3

 Aplicando cambios...
 ✓ src/main/java/.../FormateadorFecha.java modificado
 ✓ src/test/java/.../FormateadorFechaTest.java modificado

✓ git add .
✓ git commit -m "fix: corregir formato fecha respuesta simulación (DD/MM/YYYY)"
✓ git push origin release/v1.2.3

═══════════════════════════════════════════════════════════
 Paso 2/3 — Back-merge a develop
═══════════════════════════════════════════════════════════

✓ git checkout develop
✓ git merge --no-ff release/v1.2.3
✓ git push origin develop

✓ develop actualizado con el fix (commit: f5g6h7i8)

═══════════════════════════════════════════════════════════
 Paso 3/3 — CONFIG_ENTORNO_PR del hotfix
═══════════════════════════════════════════════════════════

➜ Ejecutando @pr-config-audit sobre diff release/v1.2.3 (commit anterior..actual)...
✓ No se detectaron cambios de configuración (solo cambio de código)
  (No se actualiza CONFIG_ENTORNO_PR — el cambio no afecta variables, colas ni BD)

═══════════════════════════════════════════════════════════
 Resumen Hotfix v1.2.3
═══════════════════════════════════════════════════════════

✅ Hotfix aplicado y propagado.

📦 Cambios:
  • release/v1.2.3 actualizado con el fix
  • develop tiene el fix via back-merge (--no-ff)

📌 Notas:
  • develop (f5g6h7i8) y release/v1.2.3 (d4e5f6g7) están en commits distintos
    (Esto es esperado según §3.2.1 del manual)
  • El banco ya tiene la rama actualizada — el PR release/v1.2.3 → des
    refleja los cambios automáticamente
  • No requiere nuevo tag ni nueva versión
```

---

## 5. Resumen de la Lógica de Decisión

```
Usuario invoca skill handoff-ceiba
│
├─ ¿Feature ya está en develop?
│  Sí ─────────────────────────────► Opción 1: Entregar desde DEVELOP
│                                      → Crear release branch
│                                      → Release notes
│                                      → pr-config-audit (CONFIG_ENTORNO_PR)
│                                      → Checklist §10
│                                      → Resumen para banco
│
│  No ──── ¿Qué tipo de rama?
│         │
│         ├─ feature/fix ──────────► Opción 2a: Crear PR → develop
│         │                            → Indicar que después use Opción 1
│         │
│         └─ hotfix ───────────────► Opción 2b: Aplicar fix sobre release vivo
│                                      → git commit en release/vX.Y.Z
│                                      → push
│                                      → back-merge a develop (§3.2.1)
│                                      → CONFIG_ENTORNO_PR del hotfix
```

---

## 6. Skill Propuesta

```markdown
---
name: handoff-ceiba
description: >
  Prepara y ejecuta la entrega de releases de CEIBA al banco para el proyecto
  Banca por WhatsApp. Úsala cuando necesites preparar un handoff al banco,
  crear un release branch, generar release notes, auditar configs con
  CONFIG_ENTORNO_PR, o aplicar ajustes post-entrega.
  También cuando te pidan "preparar handoff", "crear release", "entregar al banco",
  "pasar a des", "generar release notes", "CONFIG_ENTORNO_PR",
  "feature lista para release", "ajustar release" o "hotfix release".
  NOTA: No debes activarte para desarrollo normal de features, solo
  para preparación de entregas formales al banco.
---
```

### Frontmatter YAML

```yaml
name: handoff-ceiba
description: >
  Prepara y ejecuta la entrega de releases de CEIBA al banco para el proyecto
  Banca por WhatsApp. Úsala cuando necesites preparar un handoff al banco,
  crear un release branch, generar release notes, auditar configs con
  CONFIG_ENTORNO_PR, o aplicar ajustes post-entrega.
  También cuando te pidan "preparar handoff", "crear release", "entregar al banco",
  "pasar a des", "generar release notes", "CONFIG_ENTORNO_PR",
  "feature lista para release", "ajustar release" o "hotfix release".
  NOTA: No debes activarte para desarrollo normal de features, solo
  para preparación de entregas formales al banco.
metadata:
  author: CEIBA DevOps
  version: 1.0.0
```

---

## 7. Integración con Skills Existentes

```
┌──────────────────────────────────────────────────────────────────┐
│                   SKILL handoff-ceiba                             │
│                                                                  │
│  Prompt base: MANUAL_PASO_AMBIENTES.md §3.2 + §3.2.1 + §7 + §10 │
│  + lógica de menú con 2 opciones + 2 sub-casos                   │
└──────────────────┬───────────────────────────────────────────────┘
                   │  skill tool
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                     SKILLS QUE DELEGA                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ @pr-config-audit                                         │     │
│  │ Analiza diff develop..release/vX.Y.Z y genera:           │     │
│  │ CONFIG_ENTORNO_PR_{ID}.md                                │     │
│  │ - Variables nuevas (VG vs Vault)                         │     │
│  │ - Colas RabbitMQ nuevas/modificadas                      │     │
│  │ - Redis, migraciones BD                                  │     │
│  │ - Secretos hardcodeados                                  │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ @ado-pipeline-analyzer (OPCIONAL)                        │     │
│  │ Valida automáticamente los items del checklist §10:      │     │
│  │ - Build más reciente en develop/release ¿pasó?           │     │
│  │ - Stages: test, SonarQube, DAST, cobertura               │     │
│  │ - Resuelve los [?] del checklist sin preguntar al user   │     │
│  └─────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Documentos Generados por el Handoff

| Artefacto | Opción | Contenido | Generado por |
|-----------|--------|-----------|-------------|
| `release/vX.Y.Z` | 1, 2b | Rama de release en origin | Git |
| `release-notes.md` | 1 | Changelog desde el tag anterior | `git log` |
| `CONFIG_ENTORNO_PR_{ID}.md` | 1, 2a, 2b | Variables, colas, Redis, migraciones nuevas/detectadas | `pr-config-audit` |
| PR `feature → develop` | 2a | Pull request para integrar a develop | Git / ADO |

---

## 9. Checklist de Entrega (§10)

El agente ejecuta y reporta cada item solo en **Opción 1** (desde develop).

### Sin `ado-pipeline-analyzer`

Los items del pipeline se marcan como `[?]` y el agente pregunta al usuario:

```
[✓] Release branch creado o actualizado desde develop
[✓] develop y release/vX.Y.Z apuntan al mismo commit
[✗] Versión actualizada en artefactos
[✓] Release notes generados
[?] Pruebas unitarias ejecutadas (100% OK)
     → "¿El pipeline de develop pasó con 100% de tests?"
[?] Cobertura ≥ 80% verificada
     → "¿La cobertura está ≥ 80%?"
[?] DAST ejecutado (0 High/Critical)
     → "¿El DAST reporta 0 High/Critical?"
[?] SonarQube Quality Gate passed
     → "¿El Quality Gate de SonarQube pasó?"
[✓] CONFIG_ENTORNO_PR generado
[✓] Artefactos listos para entregar al banco
```

### Con `ado-pipeline-analyzer`

El agente invoca la skill automáticamente para consultar el último build en develop y validar los items sin intervención del usuario:

```
➜ Consultando último build en develop...
  ✓ ado-pipeline-analyzer: Build #12345 — Resultado: succeeded
  ✓ Stage "Test": 286/286 tests OK (100%)
  ✓ Stage "SonarQube": Quality Gate passed
  ✓ Stage "DAST": 0 High, 0 Critical
  ✓ Stage "Coverage": 83.2% (≥ 80%)

[✓] Release branch creado o actualizado desde develop
[✓] develop y release/vX.Y.Z apuntan al mismo commit
[✗] Versión actualizada en artefactos → PENDIENTE
[✓] Release notes generados
[✓] Pruebas unitarias ejecutadas (100% OK)     ← validado por pipeline
[✓] Cobertura ≥ 80% verificada (83.2%)         ← validado por pipeline
[✓] DAST ejecutado (0 High/Critical)            ← validado por pipeline
[✓] SonarQube Quality Gate passed               ← validado por pipeline
[✓] CONFIG_ENTORNO_PR generado
[✓] Artefactos listos para entregar al banco
```

---

## 10. Archivos a Crear

```
opencode de este proyecto /
├── .opencode/
│   └── skills/
│       └── handoff-ceiba/
│           ├── SKILL.md                   # Skill principal con menú + lógica
│           └── references/
│               └── MANUAL_PASO_AMBIENTES.md  # Copia de referencia del manual
```

### Dependencias

| Recurso | ¿Obligatorio? | Propósito |
|---------|--------------|-----------|
| `pr-config-audit` skill | Sí | Generar CONFIG_ENTORNO_PR_*.md |
| `MANUAL_PASO_AMBIENTES.md` | Sí | Fuente de verdad del proceso |
| `ado-pipeline-analyzer` skill | No | Validar automáticamente los items del checklist §10 (tests, cobertura, DAST, SonarQube) consultando el último build en develop. Sin ella, el agente pregunta al usuario manualmente. |

---

## 11. Resumen de Beneficios

- **Enfoque acotado**: solo la responsabilidad de CEIBA, sin mezclar lógica del banco
- **Menú guiado**: 2 opciones claras que cubren los 3 escenarios reales (desde develop, desde feature, hotfix post-entrega)
- **Reuso máximo**: aprovecha `pr-config-audit` y `ado-pipeline-analyzer` que ya existen
- **Checklist automático**: el §10 se verifica en cada handoff, con validación real del pipeline si `ado-pipeline-analyzer` está disponible
- **Consistencia**: siempre `--ff-only`, tags con convención, mismo proceso
- **Trazabilidad**: todo queda documentado (CONFIG_ENTORNO_PR, release-notes, rama release)
