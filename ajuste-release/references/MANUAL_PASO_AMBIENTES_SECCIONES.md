# Manual de Paso entre Ambientes — Secciones de Referencia

> Extracto de las secciones relevantes para ajustes de releases.
> Manual completo: `MANUAL_PASO_AMBIENTES.md`

---

## §3.2 — Reglas del release

- Versionamiento semántico: `vMAJOR.MINOR.PATCH` (ej. `v2.1.0`)
- Ajustes post-entrega en DES: `vMAJOR.MINOR.PATCH-rc.N` (ej. `v2.1.0-rc.1`)
- Hotfixes: incremento de PATCH (ej. `v2.1.0` → `v2.1.1`)
- El tag `v1.2.3` lo genera el banco al mergear el PR a `des` (punto de handoff)
- Los tags RC (`v1.2.3-rc.N`) los genera el banco al mergear cada RC a `des`
- Cada release debe incluir release notes con el cambio acumulado desde el tag anterior

---

## §3.2.1 — Ajustes solicitados por el banco tras validación en DES

Si el banco solicita cambios tras validar en DES, CEIBA aplica los ajustes directamente sobre el release branch (aún vivo). Cada ajuste se entrega como **Release Candidate (RC)** con versionado diferenciado.

### Convención de versionado RC

| Escenario | Rama | Tag en des | Ejemplo |
|-----------|------|------------|---------|
| Entrega original | `release/vX.Y.Z` | `vX.Y.Z` | `release/v2.2.3` → tag `v2.2.3` |
| Primer ajuste | `release/vX.Y.Z-rc.N` | `vX.Y.Z-rc.N` | `release/v2.2.3-rc.1` → tag `v2.2.3-rc.1` |
| Segundo ajuste | `release/vX.Y.Z-rc.N` | `vX.Y.Z-rc.N` | `release/v2.2.3-rc.2` → tag `v2.2.3-rc.2` |
| Aprobación final | — | `vX.Y.Z` (sin RC) | Tag `v2.2.3` final en des |

### Ciclo de vida de las ramas

- **`release/vX.Y.Z`** — rama base, permanece viva durante todo el ciclo RC. Acumula los fixes.
- **`release/vX.Y.Z-rc.N`** — ramas efímeras. Se crean desde la rama base para el PR a `des`. Se eliminan inmediatamente después de que el banco mergea el PR.

```
release/v2.2.3        ← viva durante todo el ciclo RC
  ├── release/v2.2.3-rc.1  ← efímera: PR → merge → tag → eliminar
  ├── release/v2.2.3-rc.2  ← efímera: PR → merge → tag → eliminar
  └── [banco aprueba] → tag v2.2.3 final → back-merge a develop → eliminar release/v2.2.3
```

### Flujo de ajuste

```bash
# 1. Aplicar fix sobre la rama base (release/vX.Y.Z sigue viva)
git checkout release/v2.2.3
git commit -m "fix: ajuste solicitado por banco en DES"
git push origin release/v2.2.3

# 2. Propagar el fix a develop (back-merge limpio)
git checkout develop
git merge --no-ff release/v2.2.3
git push origin develop

# 3. Crear rama RC efímera para el PR al banco
git checkout -b release/v2.2.3-rc.1 release/v2.2.3
git push origin release/v2.2.3-rc.1

# 4. El banco crea PR release/v2.2.3-rc.1 → des, mergea y taggea v2.2.3-rc.1 en des

# 5. Eliminar rama RC
git push origin --delete release/v2.2.3-rc.1
git branch -d release/v2.2.3-rc.1
```

### Aprobación final

```bash
# El banco crea PR desde release/vX.Y.Z (rama base, no RC) → des
# El banco mergea y taggea el tag final vX.Y.Z (sin sufijo RC) en des

# CEIBA hace back-merge final a develop y elimina la rama base
git checkout develop
git merge --no-ff release/v2.2.3
git push origin develop

git push origin --delete release/v2.2.3
git branch -d release/v2.2.3
```

---

## §5.1 — Hotfix en DES (no ha pasado a PRU)

Cuando el bug se detecta en DES y aún no ha sido promovido a PRU, se aplica el fix directamente sobre la rama release viva y se entrega como RC:

```bash
git checkout release/v2.2.3
git commit -m "fix: corregir [descripción]"
git push origin release/v2.2.3

git checkout develop
git merge --no-ff release/v2.2.3
git push origin develop

git checkout -b release/v2.2.3-rc.1 release/v2.2.3
git push origin release/v2.2.3-rc.1
# El banco mergea PR a des → tag v2.2.3-rc.1 → eliminar RC
```

---

## §5.2 — Hotfix en PRU, PREPRO o PRO

1. Analizar el bug desde el tag del ambiente afectado
2. Verificar que develop también necesita el fix
3. Merge a develop primero
4. Crear nuevo release (`vX.Y.Z+1`)
5. Flujo normal: develop → des → pru → prepro → pro

```bash
git checkout -b hotfix/arreglo-x v2.2.3-pro
# aplicar fix
git commit -m "fix: corregir [descripción]"

git checkout develop
git merge --no-ff hotfix/arreglo-x
git push origin develop

git checkout develop && git pull
git checkout -b release/v2.2.4
git push origin release/v2.2.4

git branch -d hotfix/arreglo-x
git push origin --delete hotfix/arreglo-x
```

---

## §5.3 — Principios para hotfixes

1. Siempre desde el tag del ambiente afectado — no desde `develop`
2. Verificar que develop necesita el fix — antes de crear el nuevo release
3. Merge a develop primero — merge limpio
4. Nuevo release con incremento de PATCH — `v2.2.3` → `v2.2.4`
5. Flujo completo — todos los ambientes
6. No saltar ambientes

---

## §6.1 — Convención de Tags

| Tag | Significado |
|-----|-------------|
| `v1.2.3` | Release final entregado a DES / Producción |
| `v1.2.3-rc.1` | Release candidate 1 — ajuste post-entrega en DES |
| `v1.2.3-rc.2` | Release candidate 2 — segundo ajuste en DES |
| `v1.2.3-pru` | Release promovido a PRU |
| `v1.2.3-prepro` | Release promovido a PREPRO |
| `v1.2.3-pro` | Release promovido a PRODUCCIÓN |
| `v1.2.4` | Hotfix — nuevo release |
