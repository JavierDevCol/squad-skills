# Manual de Paso entre Ambientes

| Versión | Fecha       | Autor          | Descripción                     |
|---------|-------------|----------------|---------------------------------|
| 1.0     | 2026-06-11  | DevOps Ceiba   | Versión inicial del manual      |

---

## 1. Propósito

Definir el proceso, responsabilidades y trazabilidad para la promoción de artefactos a través de los 5 ambientes del proyecto Banca por WhatsApp: **DEVELOP → DES → PRU → PREPRO → PRO**.

Los 5 ambientes pertenecen al banco, excepto DEVELOP que es el ambiente propio de CEIBA para pruebas de integración. La gestión se divide en:

| Responsable | Ambientes que gestiona              | Handoff                         |
|-------------|-------------------------------------|----------------------------------|
| **CEIBA**   | DEVELOP (propio)                    | Entrega release en rama `des` + tag |
| **BANCO**   | DES → PRU → PREPRO → PRO            | Promueve entre sus ambientes     |

---

## 2. Arquitectura de Ramas y Ambientes

```
                      ┌─────────────────────────────────────────────────────┐
                      │                RESPONSABILIDAD CEIBA                │
                      │                                                     │
                      │   feature/WA2-xxx  ──┐                              │
                      │                      ├──►  develop  ──►  DEVELOP    │
                      │   feature/WA2-yyy  ──┘                              │
                      │                            │                        │
                      │                            ▼                        │
                      │                     release/x.y.z                    │
                      │                            │                        │
                      └────────────────────────────┼────────────────────────┘
                                                   │   ↑ Handoff (merge a des + tag)
                      ┌────────────────────────────┼────────────────────────┐
                      │       RESPONSABILIDAD BANCO                        │
                      │                            ▼                        │
                      │                      ┌──────────┐                   │
                      │                      │    des   │ ◄────── TAG vX.Y.Z│
                      │                      └────┬─────┘                   │
                      │                           │                        │
                      │                           ▼                        │
                      │                      ┌──────────┐                   │
                      │                      │   pru    │ ◄── TAG vX.Y.Z-pru│
                      │                      └────┬─────┘                   │
                      │                           │                        │
                      │                           ▼                        │
                      │                      ┌──────────┐                   │
                      │                      │  prepro  │ ◄── TAG vX.Y.Z-pp│
                      │                      └────┬─────┘                   │
                      │                           │                        │
                      │                           ▼                        │
                      │                      ┌──────────┐                   │
                      │                      │ main/pro │ ◄── TAG vX.Y.Z-pro│
                      │                      └──────────┘                   │
                      └─────────────────────────────────────────────────────┘
```

### 2.1 Correspondencia Rama ↔ Ambiente

| Rama              | Ambiente | Responsable | Tipo de despliegue       |
|-------------------|----------|-------------|--------------------------|
| `develop`         | DEVELOP  | CEIBA       | Continuo (por merge)     |
| `des`             | DES      | BANCO       | Release versionado       |
| `pru`             | PRU      | BANCO       | Promoción desde DES      |
| `prepro`          | PREPRO   | BANCO       | Promoción desde PRU      |
| `main` / `master` | PRO      | BANCO       | Promoción desde PREPRO   |

---

## 3. Flujo de Trabajo

### 3.1 Desarrollo (CEIBA)

```
1. feature/WA2-xxx ──merge──► develop ──► CI en DEVELOP
2. feature/WA2-yyy ──merge──► develop ──► CI en DEVELOP
```

- Cada merge a `develop` dispara el pipeline y despliega automáticamente a DEVELOP.
- DEVELOP es el ambiente de integración y validación de CEIBA.

### 3.2 Creación de Release y Handoff al Banco (CEIBA)

Cuando la funcionalidad está estabilizada, CEIBA prepara el release y entrega al banco:

```bash
# 1. Verificar si ya existe la rama release
git fetch origin
git branch -a | grep release/v1.2.3

# CASO A — La rama NO existe: crearla desde develop (develop y release quedan en el mismo commit)
git checkout develop
git pull
git checkout -b release/v1.2.3
git push origin release/v1.2.3

# CASO B — La rama YA existe: actualizarla con fast-forward
git checkout release/v1.2.3
git pull origin release/v1.2.3
git merge --ff-only develop   # garantiza que release quede en el mismo commit que develop
git push origin release/v1.2.3

# 2. Validar que develop y release apuntan al mismo commit (obligatorio antes de notificar al banco)
git rev-parse develop
git rev-parse release/v1.2.3
# Si los hashes son distintos → release tiene commits propios → ver §3.2.1

# 3. Ajustes de release (versión, changelog, etc.)

# 4. Notificar al banco y entregar artefactos y release notes
```

> ⚠️ **Regla de oro:** `develop` y `release/vX.Y.Z` deben apuntar al **mismo commit** antes del handoff. Usar siempre `--ff-only` al actualizar una release existente. Si el fast-forward falla, significa que la release tiene commits propios — resolver primero según §3.2.1.

**El banco toma la rama `release/v1.2.3`, crea un PR hacia `des`, lo mergea y genera el tag `v1.2.3` en `des`, y despliega en su ambiente DES para validación.**

**El release branch permanece vivo durante la validación del banco en DES para poder recibir ajustes si es necesario.**

**Reglas del release:**
- Versionamiento semántico: `vMAJOR.MINOR.PATCH` (ej. `v2.1.0`)
- El tag `v1.2.3` lo genera el banco al mergear el PR a `des` (punto de handoff)
- Cada release debe incluir release notes con el cambio acumulado desde el tag anterior
- El archivo `release-notes.md` se genera **desde cero en cada release** sobrescribiendo el anterior, no se actualiza incrementalmente.
  - Al crear `release/vX.Y.Z` el pipeline ejecuta `git log vX.Y.Z-1..HEAD > release-notes.md`
  - Al mergear a `develop` ese archivo queda en el historial, pero el siguiente release lo reemplazará con los nuevos commits

### 3.2.1 Ajustes solicitados por el banco tras validación en DES

Si el banco solicita cambios tras validar en DES, CEIBA aplica los ajustes directamente sobre el release branch (aún vivo). En este caso **es aceptable y esperado** que develop y release queden en commits distintos — release tendrá commits propios que develop aún no tiene:

```bash
git checkout release/v1.2.3
# aplicar ajustes
git commit -m "fix: ajuste solicitado por banco"
git push origin release/v1.2.3

# Propagar el fix a develop para mantener consistencia
# Si develop está protegida, crear un PR desde release/v1.2.3 → develop
git checkout develop
git merge --no-ff release/v1.2.3
git push origin develop   # directo si develop lo permite; PR si está protegida
```

El banco toma la rama actualizada y actualiza el PR hacia `des`.

> ℹ️ Después del back-merge, develop y release volverán a tener commits distintos (develop tendrá el merge commit `--no-ff`). Esto es intencional y no requiere corrección.

### 3.2.2 Eliminación del release branch tras aprobación

Una vez que el banco aprueba la versión en DES, el release branch ya cumplió su propósito y se elimina:

```bash
# Eliminar rama local
git branch -d release/v1.2.3

# Eliminar rama remota
git push origin --delete release/v1.2.3
```

A partir de este punto, la versión sigue su curso en manos del banco (DES → PRU → PREPRO → PRO). CEIBA solo interviene nuevamente si se requiere un hotfix.

### 3.3 Promoción DES → PRU (BANCO)

El banco valida en DES y promueve a PRU. CEIBA registra el avance **cuando el banco confirma**:

```bash
# Cuando el banco confirma la promoción a PRU
git checkout pru
git merge --ff-only v1.2.3     # fast-forward desde el tag de release
git tag -a v1.2.3-pru -m "v1.2.3 promovido a PRU"
git push origin pru v1.2.3-pru
```

### 3.4 Promoción PRU → PREPRO (BANCO)

```bash
# Cuando el banco confirma la promoción a PREPRO
git checkout prepro
git merge --ff-only v1.2.3-pru
git tag -a v1.2.3-prepro -m "v1.2.3 promovido a PREPRO"
git push origin prepro v1.2.3-prepro
```

### 3.5 Promoción PREPRO → PRO (BANCO)

```bash
# Cuando el banco confirma la promoción a PRO
git checkout main
git merge --ff-only v1.2.3-prepro
git tag -a v1.2.3-pro -m "v1.2.3 promovido a PRODUCCIÓN"
git push origin main v1.2.3-pro
```

---

## 4. Matriz de Responsabilidades

| Actividad                                         | CEIBA | BANCO |
|---------------------------------------------------|-------|-------|
| Desarrollo y pruebas unitarias                    | ✅    |       |
| Integración en develop + CI                       | ✅    |       |
| Pruebas en ambiente DEVELOP                       | ✅    |       |
| Estabilización del release branch                 | ✅    |       |
| Merge a `des` + tag vX.Y.Z (handoff)             |       | ✅    |
| Entrega formal de artefacto y release notes       | ✅    |       |
| Despliegue en ambiente DES                        |       | ✅    |
| Validación funcional en DES                       |       | ✅    |
| Promoción DES → PRU                               |       | ✅    |
| Pruebas de integración en PRU                     |       | ✅    |
| Promoción PRU → PREPRO                            |       | ✅    |
| Pruebas de aceptación en PREPRO                   |       | ✅    |
| Promoción PREPRO → PRO                            |       | ✅    |
| Pruebas en PRO / Go-Live                          |       | ✅    |
| Registro de tags post-promoción (en repos CEIBA)  | ✅    |       |

---

## 5. Hotfixes

### 5.1 Hotfix en DES (no ha pasado a PRU)

```bash
git checkout release/v1.2.3
# aplicar fix
git commit -m "fix: corregir [descripción]"
git checkout des
git merge --no-ff release/v1.2.3
git tag -a v1.2.4 -m "Hotfix v1.2.4 para DES"
git merge --no-ff release/v1.2.3 develop
git push origin des develop v1.2.4
```

### 5.2 Hotfix en PRU o superior (bug reportado por el banco)

```bash
# Desde el tag del ambiente donde se reportó
git checkout -b hotfix/arreglo-x v1.2.3-pru
# aplicar fix
git commit -m "fix: corregir [descripción]"

# Merge a main primero (ambiente donde está el bug)
git checkout main
git merge --no-ff hotfix/arreglo-x

# Merge a las ramas inferiores para mantener consistencia
git checkout prepro && git merge --no-ff main
git checkout pru && git merge --no-ff prepro
git checkout des && git merge --no-ff pru
git checkout develop && git merge --no-ff des

# Tags
git tag -a v1.2.4-pro -m "Hotfix v1.2.4 para PRO"
git tag -a v1.2.4-prepro -m "Hotfix v1.2.4 propagado a PREPRO"
git tag -a v1.2.4-pru -m "Hotfix v1.2.4 propagado a PRU"
git tag -a v1.2.4 -m "Hotfix v1.2.4 propagado a DES"

git push origin --all --tags
```

### 5.3 Principios para hotfixes

1. **Siempre desde el tag del ambiente afectado** — no desde `develop`
2. **Propagar hacia arriba y hacia abajo** — mergear a `main`, luego descender a `prepro` → `pru` → `des` → `develop`
3. **Versionar con incremento de PATCH** — `v1.2.3` → `v1.2.4`

---

## 6. Trazabilidad con Tags

### 6.1 Convención de Tags

| Tag                  | Significado                              |
|----------------------|------------------------------------------|
| `v1.2.3`             | Release entregado a DES                  |
| `v1.2.3-pru`         | Release promovido a PRU                  |
| `v1.2.3-prepro`      | Release promovido a PREPRO                  |
| `v1.2.3-pro`         | Release promovido a PRODUCCIÓN           |

### 6.2 Estado actual por ambiente

```bash
# Consultar qué versión está en cada ambiente
git tag | sort -V | tail -20

# Ver el estado de cada rama
git log --oneline --decorate des -5
git log --oneline --decorate pru -5
git log --oneline --decorate prepro -5
git log --oneline --decorate main -5
```

### 6.3 Automatización en Pipeline

Cada pipeline de Azure DevOps debe incluir un paso que registre el tag automáticamente al desplegar:

```yaml
- script: |
    TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "sin-tag")
    echo "Versión desplegada: $TAG en ambiente: $(env)"
  displayName: 'Registrar tag de despliegue'
```

---

## 7. Release Notes

Cada entrega a DES debe incluir un release notes con el siguiente formato:

```markdown
# Release v1.2.3 — YYYY-MM-DD

## Cambios desde v1.2.2
- [WA2-xxx] Nueva funcionalidad de simulación de créditos
- [WA2-yyy] Corrección en flujo de autenticación
- [WA2-zzz] Refactor de servicio de notificaciones

## Commits incluidos
  git log v1.2.2..v1.2.3 --oneline --no-merges

## Artefactos
- Imagen Docker: banca/whatsapp-conversacion:v1.2.3
- Pipeline Build: #12345

## Pruebas realizadas
- [x] Pruebas unitarias (100% pasadas)
- [x] Cobertura ≥ 80%
- [x] Pruebas DAST en DEVELOP (0 High/Critical)
- [x] Análisis SonarQube (Quality Gate passed)
```

---

## 8. Políticas de Ramas Protegidas

| Rama      | Protección                                                |
|-----------|-----------------------------------------------------------|
| `develop` | Requiere PR con al menos 1 approval. No push directo.     |
| `des`     | Merge desde release branch. CEIBA entrega, BANCO despliega. |
| `pru`     | Solo acceso BANCO. CEIBA mergea tags post-promoción.      |
| `prepro`  | Solo acceso BANCO.                                        |
| `main`    | Solo acceso BANCO. Protegida con approvals.               |

---

## 9. Escenarios de Excepción

### 9.1 Rollback

Si un release en DES resulta defectuoso:

```bash
git checkout des
git revert v1.2.3
git tag -a v1.2.2+rollback -m "Rollback: des v1.2.3 → v1.2.2"
git push origin des
```

Si el banco reporta un bug en PRU y decide no promover:

```bash
# El banco detiene la promoción. Se aplica hotfix y se re-taggea.
git checkout -b hotfix/pru-fix v1.2.3-pru
# fix → nuevo tag v1.2.4
```

### 9.2 Release salta un ambiente

Si el banco solicita pasar directamente de DES a PREPRO (saltando PRU):

```bash
git checkout prepro
git merge --ff-only v1.2.3
git tag -a v1.2.3-prepro -m "v1.2.3 promovido directo a PREPRO (saltó PRU)"
```

Incluir en el mensaje del tag la razón: `"Promovido directo a PREPRO por solicitud del banco - [motivo]"`.

---

## 10. Checklist de Entrega

CEIBA antes de cada release a DES:

- [ ] Release branch creado o actualizado desde `develop` (ver §3.2)
- [ ] `develop` y `release/vX.Y.Z` apuntan al **mismo commit** (`git rev-parse develop == git rev-parse release/vX.Y.Z`)
- [ ] Version actualizada en artefactos
- [ ] Release notes generados
- [ ] Pruebas unitarias ejecutadas (100% OK)
- [ ] Cobertura ≥ 80% verificada
- [ ] DAST ejecutado (0 High/Critical)
- [ ] SonarQube Quality Gate passed
- [ ] Merge a `des` completado
- [ ] Tag `v1.2.3` creado y pusheado
- [ ] Release notes enviados al banco
