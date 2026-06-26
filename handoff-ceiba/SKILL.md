---
name: handoff-ceiba
description: >
  Prepara y ejecuta la entrega de releases de CEIBA al banco para el proyecto
  Banca por WhatsApp. Úsala cuando necesites preparar un handoff al banco,
  crear un release branch, generar release notes, CONFIG_ENTORNO_PR,
  feature lista para release, ajustar release o hotfix release.
  NOTA: No debes activarte para desarrollo normal de features, solo
  para preparación de entregas formales al banco.
metadata:
  author: CEIBA DevOps
  version: 1.0.0
---

# Skill: Handoff CEIBA → BANCO

Orquesta la entrega de releases de CEIBA al banco siguiendo el manual de paso entre ambientes.

## Referencias

- Manual completo: `{file:./references/MANUAL_PASO_AMBIENTES.md}` (usar como fuente de verdad)

---

## Menú Principal

Siempre que se active esta skill, muestra el siguiente menú y espera la selección del usuario:

```
╔══════════════════════════════════════════════════════════╗
║          HANDOFF CEIBA → BANCO                          ║
║                                                        ║
║  ¿Qué tipo de entrega necesitas preparar?               ║
║                                                        ║
║  [1] Entregar release desde DEVELOP                     ║
║      → La feature ya está integrada en develop via PR   ║
║      → Crea release/vX.Y.Z desde develop                ║
║                                                        ║
║  [2] Entregar release desde feature/fix/hotfix          ║
║      → El código NO está en develop o ya hay release    ║
║      → El agente determina el flujo según el caso       ║
║                                                        ║
╚══════════════════════════════════════════════════════════╝
```

---

## Opción 1: Entregar release desde DEVELOP

**Cuándo:** La feature ya está integrada a develop mediante PR aprobado. Sigue §3.2 del manual.

### Pasos

#### Paso 1 — Verificar develop
1. `git fetch origin`
2. Verificar que `develop` existe y está actualizada
3. Mostrar último commit (hash, mensaje, autor, fecha)
4. Preguntar al usuario: "¿El pipeline de develop pasó correctamente?"
   - Si responde que no o no sabe → detener, indicar que revise el pipeline primero

#### Paso 2 — Crear/actualizar release/vX.Y.Z
1. Preguntar: "¿Qué versión corresponde a este release?" (formato: vMAJOR.MINOR.PATCH)
2. Validar que el tag no exista ya: `git ls-remote --tags origin vX.Y.Z`
   - Si el tag ya existe → error. Detener.
3. Buscar si release/vX.Y.Z existe:
   ```bash
   git branch -a | grep "release/vX.Y.Z"
   ```
   - **CASO A — No existe:**
     ```bash
     git checkout develop && git pull
     git checkout -b release/vX.Y.Z
     git push origin release/vX.Y.Z
     ```
   - **CASO B — Ya existe (ff-only):**
     ```bash
     git checkout release/vX.Y.Z && git pull origin release/vX.Y.Z
     git merge --ff-only develop
     git push origin release/vX.Y.Z
     ```
   - Si `--ff-only` falla → error. Detener.

#### Paso 3 — Validar mismo commit
```bash
git rev-parse develop
git rev-parse release/vX.Y.Z
```
- Si NO coinciden → error. Detener.

#### Paso 4 — Generar release notes
Ejecutar `git log vTAG_ANTERIOR..vX.Y.Z --oneline --no-merges > release-notes.md`
- TAG_ANTERIOR: tag semver inmediatamente anterior (`git tag --sort=-version:refname | head -5`)
- Si no hay tag anterior, usar `git log --oneline --no-merges`
- Guardar en la raíz del proyecto como `release-notes.md`

#### Paso 5 — Checklist de entrega (§10 del manual)

Mostrar checklist completo. Los items marcados con ⚠️ no los resuelve esta skill — el usuario debe ejecutar las skills correspondientes por separado:

```
CHECKLIST DE ENTREGA — Handoff vX.Y.Z

[✓] Release branch creado o actualizado desde develop
[✓] develop y release/vX.Y.Z apuntan al mismo commit
[ ] Versión actualizada en artefactos
[✓] Release notes generados
[⚠] Pruebas unitarias ejecutadas (100% OK)
     → Ejecuta @ado-pipeline-analyzer para verificar
[⚠] Cobertura ≥ 80% verificada
     → Ejecuta @ado-pipeline-analyzer para verificar
[⚠] DAST ejecutado (0 High/Critical)
     → Ejecuta @ado-pipeline-analyzer para verificar
[⚠] SonarQube Quality Gate passed
     → Ejecuta @ado-pipeline-analyzer para verificar
[⚠] CONFIG_ENTORNO_PR generado
     → Ejecuta @pr-config-audit sobre diff develop..release/vX.Y.Z
[ ] Artefactos listos para entregar al banco
```

Preguntar al usuario: "¿Quieres continuar o revisar algo antes del resumen final?"
- [C] Continuar  [R] Revisar  [A] Abortar

#### Paso 6 — Resumen final
```
═══════════════════════════════════════════════════════════
 RESUMEN FINAL — Handoff vX.Y.Z
═══════════════════════════════════════════════════════════

✅ Handoff preparado.

📦 Artefactos generados por esta skill:
  ├── Rama:        release/vX.Y.Z (push a origin)
  └── release-notes.md

📌 Pendientes (ejecutar skills por separado):
  ├── @pr-config-audit        → CONFIG_ENTORNO_PR_{ID}.md
  └── @ado-pipeline-analyzer  → validar build, tests, cobertura, DAST, SonarQube

👉 El banco debe:
  1. Crear PR de release/vX.Y.Z → des
  2. Mergear el PR a des
  3. Taggear vX.Y.Z en des
  4. Desplegar en DES
```

---

## Opción 2: Entregar release desde feature/fix/hotfix

**Cuándo:** El código aún no está en develop o ya existe un release previo con ajustes solicitados.

Al seleccionar, mostrar sub-menú:

```
╔══════════════════════════════════════════════════════════╗
║  ¿Cuál es el origen del cambio?                          ║
║                                                        ║
║  [a] feature/fix → No está en develop                   ║
║      Crea PR feature → develop                          ║
║      Al aprobarse, usar Opción 1                        ║
║                                                        ║
║  [b] hotfix → Release ya entregado al banco             ║
║      Aplica fix sobre release vivo + back-merge         ║
║                                                        ║
╚══════════════════════════════════════════════════════════╝
```

---

### Opción 2a: feature/fix → develop

#### Pasos

1. **Datos de entrada:**
   - Preguntar: "¿Cuál es el nombre de tu rama?"
   - Preguntar: "¿Qué versión tendrá el release?" (formato: vMAJOR.MINOR.PATCH)
   - Validar que la rama existe: `git fetch origin && git branch -a | grep "rama"`
   - Si no existe → error. Detener.

2. **Informar sobre CONFIG_ENTORNO_PR:**
   - Indicar al usuario: "Si quieres generar el CONFIG_ENTORNO_PR del diff de tu rama, ejecuta `@pr-config-audit` por separado con el diff develop..<rama>"

3. **Crear PR a develop:**
   - Crear PR desde `<rama>` → `develop`
   - Título sugerido: "Release vX.Y.Z — <descripción breve>"
   - Descripción: incluir referencia a release/vX.Y.Z
   - Mostrar link al PR creado

4. **Instrucciones:**
   ```
   📌 Instrucciones para continuar:
     1. Solicita la aprobación del PR #{ID}
     2. Una vez mergeado a develop, ejecuta NUEVAMENTE este agente
        y selecciona la Opción 1 "Entregar release desde DEVELOP"
        usando la versión vX.Y.Z
     3. Opcional: ejecuta @pr-config-audit sobre el diff develop..<rama>
        para adelantar el CONFIG_ENTORNO_PR
   ```

---

### Opción 2b: hotfix post-entrega (§3.2.1 del manual)

#### Pasos

1. **Datos de entrada:**
   - Preguntar: "¿Cuál es la versión del release activo?"
   - Validar: `git fetch origin && git branch -a | grep "release/vX.Y.Z"`
   - Si no existe → error. Detener.
   - Preguntar: "¿Qué ajuste solicitó el banco?" — registrar descripción textual

2. **Aplicar fix sobre release/vX.Y.Z:**
   ```bash
   git checkout release/vX.Y.Z && git pull origin release/vX.Y.Z
   ```
   Mostrar los archivos modificados a medida que se aplican.
   ```bash
   git add .
   git commit -m "fix: <descripción del ajuste>"
   git push origin release/vX.Y.Z
   ```

3. **Back-merge a develop:**
   ```bash
   git checkout develop
   git merge --no-ff release/vX.Y.Z
   git push origin develop
   ```
   Si develop está protegida contra push directo, crear PR de `release/vX.Y.Z → develop`.

4. **Informar sobre CONFIG_ENTORNO_PR:**
   - Indicar: "Si el hotfix incluye cambios de configuración (variables, colas, migraciones), ejecuta `@pr-config-audit` sobre el diff del hotfix para actualizar el CONFIG_ENTORNO_PR."

5. **Resumen:**
   ```
   ✅ Hotfix aplicado y propagado.

   📦 Cambios:
     • release/vX.Y.Z actualizado con el fix
     • develop tiene el fix via back-merge (--no-ff)

   📌 Notas:
     • develop y release/vX.Y.Z están en commits distintos
       (Esto es esperado según §3.2.1 del manual)
     • El banco ya tiene la rama actualizada — el PR release/vX.Y.Z → des
       refleja los cambios automáticamente
     • No requiere nuevo tag ni nueva versión
     • Si hay cambios de config, ejecuta @pr-config-audit
   ```

---

## Reglas obligatorias

1. **Regla de oro:** develop y release/vX.Y.Z deben apuntar al mismo commit antes del handoff. Usar siempre `--ff-only`.
2. **Versionamiento semántico:** vMAJOR.MINOR.PATCH. Validar formato.
3. **release-notes.md se genera desde cero** en cada release — no se actualiza incrementalmente.
4. **El PR a des lo crea el banco, no CEIBA.** El agente solo prepara la rama y artefactos.
5. **No exponer tokens ni contraseñas** en ningún artefacto generado.
6. **Si `--ff-only` falla:** detener y remitir al usuario a §3.2.1 del manual.
7. **El release branch permanece vivo** durante validación del banco. No eliminarlo hasta aprobación.

## Skills complementarias (NO las ejecuta esta skill)

Esta skill NO ejecuta automáticamente estas skills. Solo informa al usuario que puede ejecutarlas por separado si lo necesita:

| Skill | Qué hace | Cuándo ejecutarla |
|-------|----------|-------------------|
| `@pr-config-audit` | Genera CONFIG_ENTORNO_PR_*.md analizando el diff | Opción 1 (paso 5 del checklist), Opción 2a, Opción 2b |
| `@ado-pipeline-analyzer` | Valida build, tests, cobertura, DAST, SonarQube | Opción 1 (paso 5 del checklist) |

## Gotchas

- **develop y release deben coincidir:** Si git merge --ff-only falla, es porque release tiene commits propios. No forzar merge.
- **El tag vX.Y.Z lo crea el banco en des:** CEIBA no crea tags. Solo crea la rama release.
- **Hotfix no cambia versión:** Los ajustes post-entrega no incrementan versión. Se mantiene vX.Y.Z.
- **PR a develop protegida:** Si el push a develop falla, crear PR de release/vX.Y.Z → develop en lugar de push directo.
- **Si la feature branch se llama distinto:** Aceptar cualquier nombre de rama, no solo feature/WA2-xxx.
- **CONFIG_ENTORNO_PR va por separado:** Esta skill no lo genera. El usuario debe ejecutar `@pr-config-audit` manualmente.
