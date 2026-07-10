# Manual de Paso entre Ambientes — Secciones de Referencia (Bugfix)

> Extracto de las secciones relevantes para bugfixes en desarrollo.
> Manual completo: `MANUAL_PASO_AMBIENTES.md`

---

## §3.1 — Desarrollo (CEIBA)

```
1. feature/WA2-xxx ──merge──► develop ──► CI en DEVELOP
2. feature/WA2-yyy ──merge──► develop ──► CI en DEVELOP
```

- Cada merge a `develop` dispara el pipeline y despliega automáticamente a DEVELOP.
- DEVELOP es el ambiente de integración y validación de CEIBA.

---

## §3.2 — Reglas del release

- Versionamiento semántico: `vMAJOR.MINOR.PATCH` (ej. `v2.1.0`)
- Ajustes post-entrega en DES: `vMAJOR.MINOR.PATCH-rc.N` (ej. `v2.1.0-rc.1`)
- Hotfixes: incremento de PATCH (ej. `v2.1.0` → `v2.1.1`)

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
```

> **Nota:** Este flujo lo gestiona `fix-release`, no `fix-develop`.

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
```

> **Nota:** Este flujo lo gestiona `fix-release`, no `fix-develop`.

---

## §5.3 — Principios para hotfixes

1. Siempre desde el tag del ambiente afectado — no desde `develop`
2. Verificar que develop necesita el fix — antes de crear el nuevo release
3. Merge a develop primero — merge limpio
4. Nuevo release con incremento de PATCH — `v2.2.3` → `v2.2.4`
5. Flujo completo — todos los ambientes
6. No saltar ambientes

---

## §8 — Políticas de Ramas Protegidas

| Rama | Protección |
|------|------------|
| `develop` | Requiere PR con al menos 1 approval. No push directo. |

---

## Matriz de decisión: ¿Qué skill usar?

| Escenario | Entorno | Skill |
|-----------|---------|-------|
| Bug en DEVELOP (post-merge) | CEIBA | `fix-develop` Opción 1 |
| Bug en feature branch | CEIBA | `fix-develop` Opción 2 |
| Bug en DES (pre-entrega) | CEIBA | `fix-develop` Opción 3 |
| Bug en DES (post-entrega, RC) | CEIBA → BANCO | `fix-release` Opción 1 |
| Bug en PRU/PREPRO/PRO | BANCO reporta | `fix-release` Opción 2 |
| Entrega formal | CEIBA → BANCO | `handoff-ceiba` |
