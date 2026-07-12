# ms-banca-conversacion — CONFIG-ENTORNO-PR #4898

> **Tipo de entrega:** Funcionalidad en MS existente (delta del PR)
> **Fecha:** 2026-06-25

## 1. Resumen

Implementación del flujo conversacional completo de simulación de crédito (WA2-003) en el bot de WhatsApp de Banco Mundo Mujer. Permite simular crédito nuevo, renovación o ampliación ingresando monto, cuotas y fecha de primer pago, obteniendo valores proyectados desde el Core Bancario.

- **Repositorio:** https://dev.azure.com/GestionRequerimientos/BancaPorWhatsappCICD/_git/ms-banca-conversacion
- **PR / Rama:** PR #4898 — `feature-simulacion-creditos` → `develop` (mergeado 2026-06-24)
- **Work items:** #131120, #131121, #131122
- **Autor:** Carlos Felipe Velandia Leon (cvelandia@bmm.com.co)
- **Ambientes:** DES / QA / PROD

---

## 2. Variables de entorno

> **Alcance delta:** No se introducen variables de entorno nuevas en este PR.
> Todas las propiedades nuevas de RabbitMQ están hardcodeadas en `application.yaml`
> con valores por defecto en las anotaciones `@Value`. No se requieren cambios en Vault ni en Variable Groups ADO.

| Nombre | Ámbito | Secreta | Obligatoria | Dónde se usa | Origen / Destino | Acción |
|--------|--------|---------|-------------|--------------|------------------|--------|
| — | — | — | — | — | — | Sin cambios |

---

## 3. Acciones por plataforma

### 3.1 Variable Groups ADO

> Sin cambios. Este PR no introduce variables de pipeline nuevas.

| Variable Group | Ambiente | Variable | Acción |
|----------------|----------|----------|--------|
| — | — | — | Sin cambios |

---

### 3.2 Vault corporativo

> Sin cambios. Este PR no introduce secretos nuevos.

| Path | Ambiente | Variable | Acción |
|------|----------|----------|--------|
| — | — | — | Sin cambios |

---

### 3.3 Archivos de configuración

Los cambios de configuración están commiteados directamente en `application.yaml` dentro del repositorio.

| Archivo | Cambio | Detalle |
|---------|--------|---------|
| `microservicio/src/main/resources/application.yaml` | ➕ Nuevo exchange | `rabbitmq.exchange.whatsapp.consulta-montos-credito.name: exchange.whatsapp.consulta.montos.credito` |
| `microservicio/src/main/resources/application.yaml` | ➕ Nuevo exchange | `rabbitmq.exchange.whatsapp.simulacion-credito.name: exchange.whatsapp.simulacion.credito` |
| `microservicio/src/main/resources/application.yaml` | ➕ Nueva queue | `rabbitmq.queue.whatsapp.consulta-montos-credito.name: queue.whatsapp.consulta-montos-simulacion-credito` |
| `microservicio/src/main/resources/application.yaml` | ➕ Nueva queue | `rabbitmq.queue.whatsapp.simulacion-credito.name: queue.whatsapp.simulacion.credito` |

---

### 3.4 Colas RabbitMQ

> **Mecanismo de creación:** Automático. El MS usa `RabbitAdmin` con `setAutoStartup(true)`.
> Spring AMQP declara todos los beans `Queue`, `Exchange` y `Binding` en RabbitMQ
> en el primer arranque de la aplicación. **No se requiere creación manual.**

| Cola / Exchange / Binding | Tipo | Routing key | Durable | Argumentos | Acción |
|---------------------------|------|-------------|---------|------------|--------|
| `exchange.whatsapp.consulta.montos.credito` | Exchange (Topic) | — | `true` | auto-delete: false | ➕ Auto-creado al arrancar |
| `exchange.whatsapp.simulacion.credito` | Exchange (Topic) | — | `true` | auto-delete: false | ➕ Auto-creado al arrancar |
| `queue.whatsapp.consulta-montos-simulacion-credito` | Queue (quorum) | `montos.simulacion.to.process` | `true` | x-dead-letter-exchange: `exchange.dead.letter`<br>x-dead-letter-routing-key: `dead.letter`<br>x-delivery-limit: `5` | ➕ Auto-creado al arrancar |
| `queue.whatsapp.simulacion.credito` | Queue (quorum) | `simulacion.credito.to.process` | `true` | x-dead-letter-exchange: `exchange.dead.letter`<br>x-dead-letter-routing-key: `dead.letter`<br>x-delivery-limit: `5` | ➕ Auto-creado al arrancar |
| Binding: `queue.whatsapp.consulta-montos-simulacion-credito` → `exchange.whatsapp.consulta.montos.credito` | Binding | `montos.simulacion.to.process` | — | — | ➕ Auto-creado al arrancar |
| Binding: `queue.whatsapp.simulacion.credito` → `exchange.whatsapp.simulacion.credito` | Binding | `simulacion.credito.to.process` | — | — | ➕ Auto-creado al arrancar |

**Declarado en:**
- `RabbitConfig.java`: beans `consultaMontosCreditoExchange()`, `consultaMontosCreditoQueue()`, `bindingConsultaMontosCredoQueue()`
- `RabbitConfig.java`: beans `simulacionCreditoExchange()`, `simulacionCreditoQueue()`, `bindingSimulacionCreditoQueue()`
- `ProductorParaConsultaMontosCredito.java`: productor que publica en `exchange.whatsapp.consulta.montos.credito`
- `ProductorParaSimulacionCredito.java`: productor que publica en `exchange.whatsapp.simulacion.credito`

> ⚠️ **Nota:** Estas son colas **productoras** desde el punto de vista de `ms-banca-conversacion`.
> El MS consumidor de estas colas (presumiblemente `ms-banca-simulacion-productos`) debe tener
> sus propias declaraciones o configuraciones para procesarlas.

---

### 3.5 Redis

> Reutiliza la conexión Redis existente (`redis_host` / `redis_port`). No requiere cambios de infraestructura.

| Tipo | Clave / patrón | TTL | Serialización | Acción | Dónde se usa |
|------|----------------|-----|---------------|--------|--------------|
| Cache (String JSON) | `simulacion_credito:{idInteraccion}` | 86400 s (24 h) | JSON (ObjectMapper) | Solo documentar — usa infra existente | `AdaptadorCacheSimulacionCredito.java` |

**Propósito:** Almacena `DtoDatosSimulacionCredito` (rangos de monto consultados al Core) durante la sesión de simulación. La "Nueva simulación" reutiliza estos datos cacheados para evitar repetir la consulta al Core Bancario.

---

### 3.6 Migraciones BD

> **Mecanismo:** Flyway con `baseline-on-migrate: true`. La migración se ejecuta
> **automáticamente** en el arranque del MS si no ha sido aplicada aún.

| Archivo | Herramienta | Schema | Descripción | Tablas afectadas | Rollback | Ambientes | Acción |
|---------|-------------|--------|-------------|------------------|----------|-----------|--------|
| `V92__simulacion_credito_menu.sql` | Flyway | `banca_whatsapp` | Agrega opción "Simular crédito" al menú de créditos e inserta 13 plantillas de mensaje + opciones para el flujo completo de simulación | `plantillas_mensajes`<br>`opciones_plantillas` | Manual: eliminar filas insertadas y revertir UPDATE de orden en `opciones_plantillas` | DES → QA → PROD | ▶️ Auto-ejecutado al arrancar |

**Detalle de cambios SQL:**
- `UPDATE` opciones_plantillas: mueve "Volver" de orden 3 → 4 en menú `CREDITO_SOLICITUD_HIPERVINCULO`
- `INSERT` opciones_plantillas: agrega opción "Simular crédito" (orden 3, id_respuesta: `SIMULAR`)
- `INSERT` plantillas_mensajes (13 registros):
  - `CREDITOS_SIMULACION_DISCLAIMER`
  - `CREDITOS_SIMULACION_TIPO_CREDITO`
  - `CREDITOS_SIMULACION_SOLICITAR_MONTO_NUEVO`
  - `CREDITOS_SIMULACION_SOLICITAR_MONTO_RENOVACION`
  - `CREDITOS_SIMULACION_ERROR_MONTO_INVALIDO`
  - `CREDITOS_SIMULACION_SOLICITAR_PLAZO`
  - `CREDITOS_SIMULACION_ERROR_PLAZO_INVALIDO`
  - `CREDITOS_SIMULACION_SOLICITAR_FECHA_PRIMER_PAGO`
  - `CREDITOS_SIMULACION_ERROR_FECHA_INVALIDA`
  - `CREDITOS_SIMULACION_PROCESANDO`
  - `CREDITOS_SIMULACION_RESULTADO`
  - `CREDITOS_SIMULACION_OPCIONES_POST_RESULTADO`

---

## 4. Observaciones

1. **Sin acciones manuales de infraestructura requeridas.** Todo se auto-provisiona en arranque: RabbitMQ vía `RabbitAdmin` y BD vía Flyway.

2. **Coordinación con MS consumidor.** Las colas `queue.whatsapp.consulta-montos-simulacion-credito` y `queue.whatsapp.simulacion.credito` son publicadas por este MS y consumidas por otro (probablemente `ms-banca-simulacion-productos`). Verificar que ese MS también esté desplegado y configurado antes de activar el flujo en producción.

3. **Verificar orden de despliegue.** Para evitar errores en la primera sesión de usuario, desplegar `ms-banca-conversacion` antes de que haya tráfico en el nuevo flujo, de modo que Flyway V92 se ejecute y las colas queden declaradas.

4. **Sin secretos hardcodeados detectados.** Revisión del diff no arroja credenciales ni tokens expuestos en el código.

---

*Documento generado con pr-config-audit skill — 2026-06-25*
