# CONFIG-ENTORNO-PR_4895 — ms-banca-simulacion-productos

> **Tipo de entrega:** Delta de funcionalidad — solo cambios del PR
> **Fecha:** 2026-06-25

## 1. Resumen

PR #4895 agrega el servicio de simulación de créditos al microservicio `ms-banca-simulacion-productos`.
El cambio introduce dos nuevos flujos de mensajería RabbitMQ (simulación de crédito y consulta de montos de simulación), una tabla de BD con datos semilla de montos por tipo de crédito (Flyway), nuevas rutas Vault para configuración del servicio de crédito y el bus de servicios BMM, y un nuevo componente de repositorio JPA para consulta de montos.

- **Repositorio:** https://dev.azure.com/GestionRequerimientos/BancaPorWhatsappCICD/_git/ms-banca-simulacion-productos
- **PR / Rama:** PR #4895 — `feature/WA2-003-simulacion-creditos-core` → `develop`
- **Historia de usuario:** WA2-003
- **Ambientes:** DES (develop) — único alcance de este PR

---

## 2. Variables de entorno

**Alcance:** Solo delta introducido por este PR. Variables preexistentes no se listan salvo que hayan sido modificadas.

| Nombre | Ámbito | Secreta | Obligatoria | Dónde se usa | Origen / Destino | Acción |
|--------|--------|---------|-------------|--------------|------------------|--------|
| `DB_HOST` | Runtime | No | Sí | `application.yaml` → `spring.datasource.jdbcUrl` | Vault: `dev/ms-banca-simulacion-productos/configuracion-data-base` | ➕ Crear path Vault (DES) |
| `DB_PORT` | Runtime | No | Sí | `application.yaml` → `spring.datasource.jdbcUrl` | Vault: `dev/ms-banca-simulacion-productos/configuracion-data-base` | ➕ Crear path Vault (DES) |
| `DB_NAME` | Runtime | No | Sí | `application.yaml` → `spring.datasource.jdbcUrl` | Vault: `dev/ms-banca-simulacion-productos/configuracion-data-base` | ➕ Crear path Vault (DES) |
| `DB_USERNAME` | Runtime | No | Sí | `application.yaml` → `spring.datasource.username` | Vault: `dev/ms-banca-simulacion-productos/configuracion-data-base` | ➕ Crear path Vault (DES) |
| `DB_PASSWORD` | Runtime | **Sí** | Sí | `application.yaml` → `spring.datasource.password` | Vault: `dev/ms-banca-simulacion-productos/configuracion-data-base` | ➕ Crear path Vault (DES) |
| `credito.rutaServicioSimulacionCredito` | Runtime | No | Sí | `PropiedadesConfiguracionServicioCredito.java`, `application-test.yaml:20` | Vault: `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | ➕ Crear ⚠️ Pendiente BMM |
| `credito.puertoServicioSimulacionCredito` | Runtime | No | Sí | `PropiedadesConfiguracionServicioCredito.java`, `application-test.yaml:21` | Vault: `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | ➕ Crear ⚠️ Pendiente BMM |
| `credito.contentType` | Runtime | No | Sí | `PropiedadesConfiguracionServicioCredito.java` | Vault: `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | ➕ Crear — valor: `application/json` |
| `credito.nombreUsuario` | Runtime | **Sí** | Sí | `PropiedadesConfiguracionServicioCredito.java` | Vault: `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | ➕ Crear ⚠️ Pendiente BMM |
| `credito.contrasenia` | Runtime | **Sí** | Sí | `PropiedadesConfiguracionServicioCredito.java` | Vault: `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | ➕ Crear ⚠️ Pendiente BMM |
| `puertoGenerateTokenCredito` | Runtime | No | Sí | `PropiedadesConfiguracionBmmBusServicios.java` (campo nuevo) | Vault: `dev/ms-banca-simulacion-productos/credito/config-bus-servicio-bmm` | ➕ Crear ⚠️ Pendiente BMM |
| `puertoSessionTokenCredito` | Runtime | No | Sí | `PropiedadesConfiguracionBmmBusServicios.java` (campo nuevo) | Vault: `dev/ms-banca-simulacion-productos/credito/config-bus-servicio-bmm` | ➕ Crear ⚠️ Pendiente BMM |
| `rabbitmq.queue.consulta-credito.*` | Runtime | No | Sí | `PropiedadesRabbitMQ.java`, `application.yaml` | Vault / config existente de RabbitMQ | ✏️ Actualizar (nuevos campos) |
| `rabbitmq.queue.consulta-montos.*` | Runtime | No | Sí | `PropiedadesRabbitMQ.java`, `application.yaml` | Vault / config existente de RabbitMQ | ✏️ Actualizar (nuevos campos) |

> ⚠️ **Variables pendientes (solicitar al banco BMM):**
> `credito.rutaServicioSimulacionCredito`, `credito.puertoServicioSimulacionCredito`,
> `credito.nombreUsuario`, `credito.contrasenia`,
> `puertoGenerateTokenCredito`, `puertoSessionTokenCredito`

---

## 3. Acciones por plataforma

### 3.1 Variable Groups ADO

Sin cambios requeridos en este PR.

| Variable Group | Ambiente | Observación |
|----------------|----------|-------------|
| `ms-banca-simulacion-productos-develop` | DES | Las variables `DB_*` ya existen. El cambio de pipeline (`authenticateFeed: true` + `AZURE_TOKEN`) usa `$(System.AccessToken)`, variable built-in — no requiere nueva entrada en el VG. |

---

### 3.2 Vault corporativo

> **Nota:** Los paths de QA (`pru`), PRE-PRO (`pre-prod`) y PRO (`pro`) fueron cubiertos por PR #4912.
> Este PR solo requiere acciones en el ambiente **DES (`dev`)**.

| Path Vault | Ambiente | Variable | ¿Secreta? | Acción |
|------------|----------|----------|-----------|--------|
| `dev/ms-banca-simulacion-productos/configuracion-data-base` | DES | `DB_HOST` | No | ➕ Crear path y clave |
| `dev/ms-banca-simulacion-productos/configuracion-data-base` | DES | `DB_PORT` | No | ➕ Crear clave |
| `dev/ms-banca-simulacion-productos/configuracion-data-base` | DES | `DB_NAME` | No | ➕ Crear clave |
| `dev/ms-banca-simulacion-productos/configuracion-data-base` | DES | `DB_USERNAME` | No | ➕ Crear clave |
| `dev/ms-banca-simulacion-productos/configuracion-data-base` | DES | `DB_PASSWORD` | **Sí** | ➕ Crear clave |
| `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | DES | `credito.rutaServicioSimulacionCredito` | No | ➕ Crear path y clave — ⚠️ valor: **Pendiente BMM** |
| `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | DES | `credito.puertoServicioSimulacionCredito` | No | ➕ Crear clave — ⚠️ valor: **Pendiente BMM** |
| `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | DES | `credito.contentType` | No | ➕ Crear clave — valor: `application/json` |
| `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | DES | `credito.nombreUsuario` | **Sí** | ➕ Crear clave — ⚠️ valor: **Pendiente BMM** |
| `dev/ms-banca-simulacion-productos/credito/configuracion-servicio` | DES | `credito.contrasenia` | **Sí** | ➕ Crear clave — ⚠️ valor: **Pendiente BMM** |
| `dev/ms-banca-simulacion-productos/credito/config-bus-servicio-bmm` | DES | `puertoGenerateTokenCredito` | No | ➕ Crear path y clave — ⚠️ valor: **Pendiente BMM** |
| `dev/ms-banca-simulacion-productos/credito/config-bus-servicio-bmm` | DES | `puertoSessionTokenCredito` | No | ➕ Crear clave — ⚠️ valor: **Pendiente BMM** |

---

### 3.3 Archivos de configuración

Cambios en archivos de configuración incluidos en el PR (ya mergeados a `develop`):

| Archivo | Tipo de cambio | Detalle |
|---------|----------------|---------|
| `microservicio/src/main/resources/application.yaml` | ✏️ Modificado | Agrega datasource PostgreSQL (`${DB_*}`), Flyway, dos nuevas secciones de colas RabbitMQ (`consulta-credito`, `consulta-montos`). Cambia `server.servlet.context-path` de `/cdts` a `/simulacion-productos`. |
| `microservicio/src/main/resources/application-local.yaml` | ✏️ Modificado | Agrega datasource con defaults locales `${DB_HOST:localhost}:${DB_PORT:5432}`. Añade rutas Vault `dev/ms-banca-simulacion-productos/configuracion-data-base`, `credito/configuracion-servicio`, `credito/config-bus-servicio-bmm`. |
| `microservicio/src/main/resources/application-develop.yml` | ✏️ Modificado | Actualiza rutas Vault de `ms-banca-cdts` a `ms-banca-simulacion-productos`. Añade las tres rutas Vault nuevas. |
| `microservicio/src/main/resources/application-pru.yaml` | ✏️ Modificado | Rutas Vault actualizadas al nombre del nuevo MS. Añade `configuracion-redis`, `credito/configuracion-servicio`, `credito/config-bus-servicio-bmm` (sin `configuracion-data-base`, cubierto por PR #4912). |
| `microservicio/src/main/resources/application-prepro.yaml` | ✏️ Modificado | Igual que `pru` con prefijo `pre-prod`. |
| `microservicio/src/main/resources/application-pro.yaml` | ✏️ Modificado | Igual que `pru` con prefijo `pro`. |
| `microservicio/gradle.properties` | ✏️ Modificado | `libBancaTransversalesVersion`: `1.0.8` → `1.0.11` |
| `microservicio/settings.gradle` | ✏️ Modificado | `rootProject.name`: `ms_banca_cdts` → `ms_banca_simulacion_productos` |
| `microservicio/infraestructura/build.gradle` | ✏️ Modificado | Dependencia Flyway: `testImplementation` → `implementation` (Flyway activo en runtime) |
| `azure-pipelines.yml` | ✏️ Modificado | Paso `cyclonedxBom`: agrega `authenticateFeed: true` y `AZURE_TOKEN: $(System.AccessToken)` para resolver librería privada. |

---

### 3.4 Colas RabbitMQ

> **Ambiente:** DES (develop)
> Las colas deben crearse manualmente en el broker RabbitMQ del entorno DES antes del primer despliegue, o se pueden dejar que la app las declare automáticamente al arrancar (según configuración del broker).

| Cola | Tipo | Routing Key | DLX | DLK | Durable | Consumidores | Acción | Dónde se declara |
|------|------|-------------|-----|-----|---------|-------------|--------|------------------|
| `queue.whatsapp.simulacion.credito` | Queue (quorum) | `simulacion.credito.to.process` | `exchange.dead.letter` | `dead.letter` | Sí | `ConsumidorSimulacionCreditoRabbitMQ` | Automático | `ConfiguracionRabbitMQ.java` — bean `colaSimulacionCredito()` |
| `queue.whatsapp.consulta-montos-simulacion-credito` | Queue (quorum) | `montos.simulacion.to.process` | `exchange.dead.letter` | `dead.letter` | Sí | `ConsumidorConsultaMontosSimulacionRabbitMQ` | Automático | `ConfiguracionRabbitMQ.java` — bean `colaConsultaMontos()` |

**Argumentos comunes a ambas colas:**
```
x-queue-type: quorum
x-delivery-limit: 5
x-dead-letter-exchange: exchange.dead.letter
x-dead-letter-routing-key: dead.letter
```

**Colas existentes sin cambio estructural (referencia):**

| Cola | Routing Key | Observación |
|------|-------------|-------------|
| `queue.whatsapp.simulacion.cdt` | `simulacion.cdt.to.process` | Preexistente, sin cambio |
| `queue.whatsapp.respuesta.servicio` | `whatsapp.respuesta.servicio` | Destino de respuestas de los 3 consumidores |
| `queue.errores.servicio-externo` | `errores.servicio-externo.to.process` | Preexistente, sin cambio |

---

### 3.5 Redis

Sin cambios en Redis en este PR. El path `configuracion-redis` ya existía en todos los ambientes.

---

### 3.6 Migraciones BD

> La migración se ejecuta **automáticamente** al iniciar la aplicación mediante Flyway.
> No requiere ejecución manual salvo que Flyway esté deshabilitado en el entorno.

| Archivo | Herramienta | Descripción | Schema / BD | Tablas afectadas | Rollback | Ambientes | Acción |
|---------|-------------|-------------|-------------|------------------|----------|-----------|--------|
| `V1.0__crear_tabla_simulacion_creditos_montos.sql` | Flyway | Crea schema `banca_whatsapp` (si no existe) y tabla `simulacion_creditos_montos` con 25 filas de datos semilla (tipos NUEVO, RENOVACION, AMPLIACION con rangos de monto y plazo) | `banca_whatsapp` | `simulacion_creditos_montos` (nueva) | `DROP TABLE banca_whatsapp.simulacion_creditos_montos;` | TODOS | ▶️ Auto en startup |

**Configuración Flyway aplicada:**
```yaml
spring.flyway.schemas: banca_whatsapp
spring.flyway.locations: classpath:db/migration
spring.flyway.default-schema: banca_whatsapp
spring.flyway.table: flyway_schema_history_simulacion_productos
spring.flyway.baseline-on-migrate: true
spring.flyway.validate-on-migrate: true
spring.flyway.baseline-version: 0
```

> **Nota:** La migración `V1.0__schema.sql` fue eliminada en este PR y reemplazada por `V1.0__crear_tabla_simulacion_creditos_montos.sql`. Si existe un historial Flyway anterior en la BD, verificar que no haya conflicto de versión `1.0`.

---

## 4. Observaciones

1. **Secretos hardcodeados:** No se detectaron secretos reales en texto plano. Los archivos de test contienen `usuario-test` / `contrasenia-test` (datos ficticios). El archivo `application-local.yaml` contiene `spring.rabbitmq.password: root` (credencial default local de RabbitMQ — bajo riesgo, solo afecta entorno local).

2. **Valores fijos de negocio en código:** La clase `AsistenteServicioSimulacionCredito.java` contiene constantes hardcodeadas (`PRODUCT_UID_FIJO = "121"`, `NUMBER_ID_FIJO = 999999L`, `PERIOD_FEES_FIJO = "30"`, `VALUE_TOTAL_TERM = "365"`). Si estos valores varían por ambiente o pueden cambiar, considerar externalizarlos a Vault.

3. **MS renombrado:** Este microservicio era previamente `ms-banca-cdts`. El PR actualiza `settings.gradle` (`ms_banca_cdts` → `ms_banca_simulacion_productos`) y `context-path` (`/cdts` → `/simulacion-productos`). Verificar que los clientes que consumían el MS anterior hayan sido actualizados.

4. **Vault QA/PRE/PRO:** Los paths de Vault para los ambientes superiores (`pru`, `pre-prod`, `pro`) fueron gestionados en el PR #4912. Validar que ese PR esté mergeado antes de promover a QA.

5. **Versión de librería:** `libBancaTransversalesVersion` sube de `1.0.8` a `1.0.11`. Verificar compatibilidad y que el feed de Artifacts tenga la nueva versión disponible (el cambio en el pipeline agrega `authenticateFeed: true` precisamente para esto).

---

*Documento generado con pr-config-audit skill — 2026-06-25*
