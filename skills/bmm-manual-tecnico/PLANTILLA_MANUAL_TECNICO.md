# MANUAL TÉCNICO Y FUNCIONAL
## [Nombre del microservicio]
### [Título de la Historia de Usuario]

---

| Campo | Valor |
|-------|-------|
| **Número del requerimiento/solicitud** | [Número del requerimiento] |
| **Número del paso** | [Número del paso] |
| **Historia de usuario** | [HU-XXX.X] – [Título de la HU] |
| **Pull Requests** | [PR XXXX], [PR XXXX], [PR XXXX] |
| **Nombre del desarrollador / Equipo** | [Nombre del desarrollador o equipo] |
| **Fecha de creación** | [dd/mm/yyyy] |

---

## TABLA DE CONTENIDO

1. Descripción del Requerimiento
2. Solución al Requerimiento
   - 2.1. Versionamiento
   - 2.2. Arquitectura y Tecnologías
3. Manual Técnico
   - 3.1. Prerrequisitos de Infraestructura
   - 3.2. Configuración de Secrets en HashiCorp Vault
   - 3.3. Library Variables en Azure DevOps
   - 3.4. Secure Files Requeridos
   - 3.5. Proceso de Despliegue (Pipeline CI/CD)
   - 3.6. Verificación del Despliegue
   - 3.7. Parametrización por Ambiente
4. Descripción Funcional Detallada
5. Interacciones con Otras Funcionalidades del Sistema
6. Modelo Lógico
7. Cadena de Llamadas
8. Desarrollos de Interfaces al Core Bancario
9. Pruebas al Desarrollo
10. Anexos
11. Control de Versiones del Documento

---

## PRESENTACIÓN DEL REQUERIMIENTO Y LA SOLUCIÓN

### 1. Descripción del Requerimiento

[Describe en 2-3 párrafos QUÉ se solicitó: contexto de negocio, objetivo, Historia de Usuario de referencia. No describas cómo se implementó.]

> **Historia de usuario de referencia:** [HU-XXX.X] – [Título de la HU]

---

### 2. Solución al Requerimiento

[Describe CÓMO se resolvió el requerimiento: patrón arquitectónico usado y componentes principales entregados.]

**Componentes entregados:**

- [Componente 1: descripción breve]
- [Componente 2: descripción breve]
- [Componente N: descripción breve]

---

#### 2.1. Versionamiento

| PR # | Commit | Descripción |
|------|--------|-------------|
| PR XXXX | xxxxxxx | [Descripción del PR] |
| PR XXXX | xxxxxxx | [Descripción del PR] |
| PR XXXX | xxxxxxx | [Descripción del PR] |

---

#### 2.2. Arquitectura y Tecnologías

**Patrón:** [ej: Clean Architecture / Hexagonal – Ports & Adapters]

**Capas del microservicio:**

| Capa | Módulo Gradle | Responsabilidad |
|------|---------------|-----------------|
| Dominio | `microservicio/dominio` | [Entidades, puertos, servicios de dominio. Sin dependencias externas.] |
| Aplicación | `microservicio/aplicacion` | [Comandos, manejadores, DTOs, mapeadores. Orquesta casos de uso.] |
| Infraestructura | `microservicio/infraestructura` | [Adaptadores, consumidores, publicadores, configuraciones.] |

**Tecnologías principales:**

| Componente | Tecnología / Versión |
|------------|----------------------|
| Lenguaje / Runtime | [Java XX – Amazon Corretto XX] |
| Framework | [Spring Boot X.X.X – Spring Cloud Vault] |
| Servidor web | [Undertow / Tomcat] |
| Mensajería | [RabbitMQ AMQP con Dead Letter Exchange] |
| Caché / Sesiones | [Redis – cliente Lettuce – TTL XX horas] |
| Base de datos | [PostgreSQL con Flyway X.X.X] |
| Seguridad secretos | HashiCorp Vault – autenticación AppRole |
| Cifrado mensajes | [JWE/RSA / N/A] |
| Orquestación | Kubernetes en AWS EKS |
| Registry de imágenes | AWS ECR |
| CI/CD | Azure DevOps Pipelines |
| Calidad de código | SonarQube, Gitleaks, Dependency Track, JaCoCo, PIT |
| Librería transversal | [libBancaTransversales vX.X.X / N/A] |

**Flujo de datos de alto nivel:**

```
[Sistema de origen] → [Cola/Endpoint de entrada]
    → [Consumidor / Controlador]
    → [Manejador del caso de uso]
    → [Servicio de dominio]
    → [Adaptador al sistema externo] → [Sistema externo]
    ← [Respuesta del sistema externo]
    → [Mapeador] → [DTO de respuesta]
    → [Cola/Endpoint de salida] → [Sistema de destino]

En caso de error:
    → [Publicador de errores] → [Cola de errores]
```

---

## MANUAL TÉCNICO Y FUNCIONAL

### 3. Manual Técnico

#### 3.1. Prerrequisitos de Infraestructura

| Componente | Requisito |
|------------|-----------|
| AWS EKS | Cluster Kubernetes activo. El agente debe poder ejecutar `kubectl` y `aws eks update-kubeconfig`. |
| AWS ECR | Repositorio de imágenes Docker disponible. |
| HashiCorp Vault | Instancia disponible con los secrets del microservicio creados (ver sección 3.2). |
| RabbitMQ | Broker disponible con colas y exchanges configurados (ver sección 6.2). |
| Redis | [Propósito específico del caché en este microservicio] |
| PostgreSQL | Base de datos disponible. Flyway aplicará el schema automáticamente al arrancar. |
| Agente Azure DevOps | Configurado con acceso a red interna, AWS CLI y kubectl. Pool: `$(AZDO_AGENTPOOL_BUILD)`. |
| Secure Files | Certificados cargados en Azure DevOps Library (ver sección 3.4). |

---

#### 3.2. Configuración de Secrets en HashiCorp Vault

**Rutas de secrets por ambiente:**

| Ambiente | Perfil Spring | Rutas de Secrets en Vault |
|----------|---------------|---------------------------|
| Desarrollo | `develop` | `vault://dev/[microservicio]/[secret-1]`<br>`vault://dev/[microservicio]/[secret-N]`<br>`vault://dev/certificados` |
| Pruebas | `pru` | `vault://pru/[microservicio]/[secret-1]`<br>`vault://pru/[microservicio]/[secret-N]`<br>`vault://pru/certificados` |
| Pre-producción | `prepro` | `vault://pre-prod/[microservicio]/[secret-1]`<br>`vault://pre-prod/[microservicio]/[secret-N]`<br>`vault://pre-prod/certificados` |
| Producción | `pro` | `vault://pro/[microservicio]/[secret-1]`<br>`vault://pro/[microservicio]/[secret-N]`<br>`vault://pro/certificados` |

---

**Secret 1: [nombre-secret-1]**

| Atributo | Valor |
|----------|-------|
| **Ruta en Vault** | `{env}/[microservicio]/[nombre-secret-1]` |
| **Descripción** | [Para qué sirve este secret] |

```json
{
  "[clave_1]": "<[descripción del valor 1]>",
  "[clave_2]": "<[descripción del valor 2]>",
  "[clave_N]": "<[descripción del valor N]>"
}
```

**Secret 2: [nombre-secret-2]**

| Atributo | Valor |
|----------|-------|
| **Ruta en Vault** | `{env}/[microservicio]/[nombre-secret-2]` |
| **Descripción** | [Para qué sirve este secret] |

```json
{
  "[clave_1]": "<[descripción del valor 1]>",
  "[clave_N]": "<[descripción del valor N]>"
}
```

> Agregar un bloque por cada secret adicional del microservicio.

**Prefijos de ruta por ambiente:**

| Ambiente | Prefijo `{env}` | Ejemplo de ruta completa |
|----------|-----------------|--------------------------|
| Desarrollo | `dev` | `dev/[microservicio]/[nombre-secret]` |
| Pruebas | `pru` | `pru/[microservicio]/[nombre-secret]` |
| Pre-producción | `pre-prod` | `pre-prod/[microservicio]/[nombre-secret]` |
| Producción | `pro` | `pro/[microservicio]/[nombre-secret]` |

**Crear rol AppRole en Vault (ejecutar por ambiente):**

```bash
set VAULT_ADDR=https://vault-middle-{env}.bmm.com/
set VAULT_TOKEN=<token_admin>

vault auth enable approle

vault write auth/approle/role/[microservicio] ^
    token_policies="politica-[microservicio],politica-certificados" ^
    token_ttl=1h token_max_ttl=4h

# Guardar en Library ADO → VAULT_ROLE_ID
vault read auth/approle/role/[microservicio]/role-id

# Guardar en Library ADO → VAULT_SECRET_ID
vault write -f auth/approle/role/[microservicio]/secret-id
```

---

#### 3.3. Library Variables en Azure DevOps

> Nombre del grupo: **`[microservicio]-{env}`**

| Variable | Descripción | Ejemplo | Secreto |
|----------|-------------|---------|---------|
| `AZDO_AGENTPOOL_BUILD` | Pool de agentes de build | `bmm-agents-linux` | No |
| `AWS_ACCOUNT_ID` | ID de cuenta AWS | `123456789012` | **Sí** |
| `AWS_REGION` | Región AWS | `us-east-1` | No |
| `DOCKER_REPO_NAME` | Nombre del repositorio ECR | `[microservicio]` | No |
| `EKS_CLUSTER_NAME` | Nombre del cluster EKS | `bmm-kubernetes-{env}` | No |
| `K8S_NAMESPACE` | Namespace de Kubernetes | `banca-whatsapp` | No |
| `K8S_DEPLOY_NAME` | Nombre del Deployment en K8s | `[microservicio]` | No |
| `K8S_REPLICAS` | Número de réplicas del pod | `1` | No |
| `K8S_CONTAINER_PORT` | Puerto interno del contenedor | `[puerto]` | No |
| `K8S_EXPOSE_PORT` | Puerto expuesto por el Service | `[puerto]` | No |
| `K8S_SVC_TYPE` | Tipo de Service K8s | `ClusterIP` | No |
| `VAULT_HOST` | Host de Vault (sin https://) | `vault-middle-des.bmm.com` | No |
| `VAULT_ROLE_ID` | AppRole role-id del microservicio | *(obtenido de Vault)* | **Sí** |
| `VAULT_SECRET_ID` | AppRole secret-id del microservicio | *(obtenido de Vault)* | **Sí** |
| `IP_NAT` | IP NAT para hostAliases del pod | `10.x.x.x` | No |
| `HOST_NAT` | Hostname NAT para hostAliases | `core-bancario.interno` | No |
| `SONARQ_SONARQUBE` | Service Connection SonarQube *(solo develop)* | `SonarQube-BMM` | No |
| `SONARQ_CLI_PROJECT_KEY` | Clave del proyecto en SonarQube | `[microservicio]` | No |
| `SONARQ_CLI_PROJECT_NAME` | Nombre del proyecto en SonarQube | `[microservicio]` | No |
| `SONARQ_CLI_SOURCES` | Directorio fuente para análisis Sonar | `microservicio` | No |
| `SONARQ_EXCLUSIONS` | Exclusiones del análisis Sonar | `**/test/**,**/build/**` | No |
| `DTRACK_SC` | Service Connection Dependency Track | `DTrack-BMM` | No |
| `DTRACK_PROJ_NAME` | Proyecto en Dependency Track | `[microservicio]` | No |
| `DTRACK_GROUP_NAME` | Grupo del proyecto en Dependency Track | `co.com.bmm` | No |
| `LIB_BANCA_TRANSVERSALES_USERNAME` | Usuario Azure Artifacts | *(usuario)* | **Sí** |
| `LIB_BANCA_TRANSVERSALES_PASSWORD` | PAT Azure Artifacts | *(pat)* | **Sí** |
| `GITLEAKS_VERSION` | Versión de Gitleaks *(solo develop)* | `8.28.0` | No |

---

#### 3.4. Secure Files Requeridos

| Archivo | Descripción | Stage |
|---------|-------------|-------|
| `ca-vault.pem` | Certificado CA que firmó el cert de Vault. Se importa al truststore Java del contenedor para validar la conexión HTTPS con Vault. | `Push_Docker` |
| `servidor-vault.pem` | Certificado TLS del servidor Vault. Se crea como Secret TLS en Kubernetes para el Ingress. | `Deploy` |
| `servidor-vault.key` | Clave privada del certificado del servidor Vault. | `Deploy` |

---

#### 3.5. Proceso de Despliegue (Pipeline CI/CD)

| Stage | Nombre | Descripción | Pasos principales |
|-------|--------|-------------|-------------------|
| 1 | **Build – Compilar** | Compila, ejecuta análisis de calidad y empaqueta el JAR. | 1. Verificar Java/Gradle<br>2. Instalar Gitleaks *(solo develop)*<br>3. Generar BOM CycloneDX<br>4. `gradle test` + `jacocoTestReport`<br>5. Publicar JUnit y cobertura<br>6. Upload BOM a Dependency Track<br>7. PIT Mutation Testing<br>8. SonarQube (prepare → analyze → publish → break on failure)<br>9. `gradle clean build` → JAR<br>10. Publicar artefacto `code` |
| 2 | **Push_Docker – Push a ECR** | Construye imagen Docker y la sube a ECR. | 1. Descargar artefacto `code`<br>2. Descargar `ca-vault.pem`<br>3. `docker build --build-arg CA_CERT_PATH=certs/ca-vault.pem`<br>4. ECR Push tag=`$(Build.BuildNumber)` |
| 3 | **Deploy – Desplegar en EKS** | Aplica el manifiesto K8s en el cluster EKS. | 1. Descargar artefacto<br>2. Replace tokens `#{...}#` en `deployment.yaml`<br>3. Descargar `servidor-vault.pem` y `.key`<br>4. `kubectl create secret tls tls-secret`<br>5. `aws eks update-kubeconfig`<br>6. `kubectl apply -f deployment.yaml`<br>7. `kubectl get pods` |

**Estrategia de ramas y mapeo a ambientes:**

| Rama | Patrón | Ambiente destino | Perfil Spring | Permanente |
|------|--------|-----------------|---------------|-----------|
| `develop` | `develop` | develop | develop | Sí |
| `release/x.x.x` | `release/*` | **des** | des | **No – se elimina tras aprobación** |
| `des` | `des` | des | des | Sí |
| `pru` | `pru` | pru | pru | Sí |
| `prepro` | `prepro` | prepro | prepro | Sí |
| `main` / `master` | `main` o `master` | pro | pro | Sí |

**Ciclo de vida de `release/x.x.x`:**

```
PASO 1 – Creación: se crea release/x.x.x desde develop cuando está lista para des.
PASO 2 – Despliegue: el pipeline despliega en des para validación funcional.
PASO 3 – Correcciones: bugs/mejoras de des se commiten SOBRE release/ (NO develop).
          Cada commit redespliega automáticamente en des.
PASO 4 – Aprobación: des aprueba → release/ se elimina → se promueve: des → pru → prepro → pro.

IMPORTANTE: nunca volver a develop para fixes del ciclo de validación en des.
```

---

#### 3.6. Verificación del Despliegue

```bash
# Conectar al cluster
aws eks update-kubeconfig --name bmm-kubernetes-{env} --region us-east-1

# Verificar pod Running
kubectl get pods -n {K8S_NAMESPACE} | grep [microservicio]

# Ver logs (buscar "Started Application")
kubectl logs -n {K8S_NAMESPACE} deployment/[microservicio] --tail=50

# Health check
kubectl port-forward -n {K8S_NAMESPACE} deployment/[microservicio] [puerto]:[puerto]
curl http://localhost:[puerto]/[context-path]/actuator/health
# Esperado: {"status":"UP"}
```

---

#### 3.7. Parametrización por Ambiente

| Parámetro | develop | **des *(via release/)*** | pru | prepro | pro |
|-----------|---------|--------------------------|-----|--------|-----|
| Rama de origen | `develop` | `release/x.x.x` | `des` | `pru` | `prepro` |
| Perfil Spring | `develop` | `des` | `pru` | `prepro` | `pro` |
| Vault path prefix | `dev/` | `dev/` | `pru/` | `pre-prod/` | `pro/` |
| `VAULT_HOST` | [vault-develop] | [vault-des] | [vault-pru] | [vault-prepro] | [vault-pro] |
| `K8S_NAMESPACE` | [namespace-dev] | [namespace-des] | [namespace-pru] | [namespace-pre] | [namespace-pro] |
| `EKS_CLUSTER_NAME` | `bmm-kubernetes-develop` | `bmm-kubernetes-des` | `bmm-kubernetes-pru` | `bmm-kubernetes-prepro` | `bmm-kubernetes-pro` |
| `K8S_REPLICAS` | `1` | `1` | `1` | `2` | `2` |
| SonarQube | ✅ Sí | ❌ No | ❌ No | ❌ No | ❌ No |
| Gitleaks | ✅ Sí | ❌ No | ❌ No | ❌ No | ❌ No |
| PIT Mutation | ✅ Sí | ❌ No | ❌ No | ❌ No | ❌ No |
| `logging.level` | `INFO` | `DEBUG` | `DEBUG` | `INFO` | `INFO` |
| Library ADO group | `[ms]-develop` | `[ms]-des` | `[ms]-pru` | `[ms]-prepro` | `[ms]-pro` |

---

## 4. Descripción Funcional Detallada

### 4.1. Funcionalidad: [Título de la HU]

[Descripción general de la funcionalidad. Si el microservicio es completamente asíncrono (sin REST), aclararlo aquí.]

#### 4.1.1. Campos de Entrada

> **Origen:** [Cola RabbitMQ / Endpoint REST] — `[nombre de la cola o path]`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| [campo] | [Tipo] | Sí / No | [Descripción] |
| [campo] | [Tipo] | Sí / No | [Descripción] |
| [campo] | [Tipo] | Sí / No | [Descripción] |

#### 4.1.2. Campos de Salida

> **Destino:** [Cola RabbitMQ / Respuesta HTTP] — `[nombre de la cola o código HTTP]`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| [campo] | [Tipo] | [Descripción] |
| [campo] | [Tipo] | [Descripción] |
| [campo] | [Tipo] | [Descripción] |

#### 4.1.3. Acciones y Eventos

**[Evento 1: ej. Recepción del mensaje]**
[Descripción detallada de este evento y las clases involucradas.]

**[Evento 2: ej. Mapeo al comando de aplicación]**
[Descripción detallada.]

**[Evento N: ej. Publicación de la respuesta]**
[Descripción detallada.]

**Manejo de errores**
[Si ocurre una excepción, describe qué hace el microservicio: reintento, publicación en cola de errores, etc.]

#### 4.1.4. Restricciones

- [Restricción 1]
- [Restricción 2]
- [Restricción N]

---

## 5. Interacciones con Otras Funcionalidades del Sistema

| Integración / Sistema | Tipo y Conexión | Descripción |
|-----------------------|-----------------|-------------|
| [Sistema o microservicio 1] | [Tipo: RabbitMQ / REST / JDBC]<br>[Host:Port / URL] | [Descripción de la integración] |
| [Sistema o microservicio N] | [Tipo y conexión] | [Descripción] |
| HashiCorp Vault | HTTPS – Puerto 443 / AppRole<br>Host: `${VAULT_HOST}` | Almacén centralizado de secretos. Se consulta al arrancar la aplicación. |
| RabbitMQ | AMQP<br>Host: `${rabbit.host}:${rabbit.puerto}` | Broker de mensajes para colas de entrada, salida y dead letter. |
| Redis | Redis Lettuce<br>Host: `${redis_host}:${redis_port}` | [Propósito específico del caché en este microservicio] |
| PostgreSQL | JDBC / Flyway | Base de datos relacional. Flyway aplica migraciones automáticamente. |
| Azure DevOps | CI/CD Pipeline / `azure-pipelines.yml` | Build, análisis de calidad, empaquetado Docker y despliegue en EKS. |
| AWS ECR | Docker Registry / `${AWS_REGION}` | Almacena imágenes Docker etiquetadas con el número de build. |
| AWS EKS | Kubernetes / `$(EKS_CLUSTER_NAME)` | Plataforma de orquestación donde se despliega el microservicio. |

---

## MODELO LÓGICO

### 6. Descripción de Tablas

#### Tabla: `[nombre_tabla]`

> **Descripción:** [Para qué sirve esta tabla]

```sql
CREATE TABLE [nombre_tabla] (
    [campo_1]  [tipo]  PRIMARY KEY NOT NULL,
    [campo_2]  [tipo]  NOT NULL,
    [campo_N]  [tipo]  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

| Campo | Tipo | Longitud | Requerido | Descripción |
|-------|------|----------|-----------|-------------|
| [campo] | [tipo] | [-] | Sí / No | [Descripción] |
| [campo] | [tipo] | [-] | Sí / No | [Descripción] |

**Índices:**

| Nombre | Campo(s) | Tipo |
|--------|----------|------|
| [nombre_pk] | [campo] | P (Primary Key) |

> Agregar una sección por cada tabla adicional del microservicio.

---

### 6.1. Configuración de Colas RabbitMQ

| Nombre de Cola | Routing Key | Durable | DLX / DLK | Propósito |
|----------------|-------------|---------|-----------|-----------|
| `[queue.entrada]` | `[rk.entrada]` | Sí | `exchange.dead.letter / dead.letter` | **ENTRADA** – [Descripción] |
| `[queue.salida]` | `[rk.salida]` | Sí | `exchange.dead.letter / dead.letter` | **SALIDA** – [Descripción] |
| `queue.errores.servicio-externo` | `errores.servicio-externo.to.process` | Sí | – | **ERRORES** – Eventos de error para trazabilidad. |

---

## 7. Cadena de Llamadas de Procedimientos y Funciones

```
[ClaseEntrada] (consumidor / controlador)
  └─ [MapeadorEntrada].metodo(parametro)
      └─ [Manejador].metodo(comando)
          └─ [ServicioDominio].metodo(entidad)
              ├─ [AdaptadorSalida].metodo() → [Sistema externo]
              │   └─ [RespuestaExterna]
              └─ [MapeadorSalida].metodo(RespuestaExterna)
                  └─ [DTOFinal]
                      └─ [Publicar en cola de salida]

En caso de excepción:
  └─ [PublicadorErrores].metodo(EventoError)
      └─ [Sanitizador].metodo(payload)
          └─ [Publicar en queue.errores.servicio-externo]
```

---

## 8. Desarrollos de Interfaces al Core Bancario

[Describe la integración con el Core Bancario. Si no aplica: "Este microservicio no realiza integración directa con el Core Bancario."]

### 8.1. Actas de Reuniones con Seguridad de la Información

> Solicitar consecutivo del acta FM-005 a: **solicitudes.tecnologicas@bmm.com.co**

Consecutivo(s) FM-005: [número del acta]

### 8.2. Cumplimiento PT-007 – Desarrollo de Interfaces desde o hacia el CORE

| PT-007 | Descripción | Cumple | Evidencia / Comentario |
|--------|-------------|--------|------------------------|
| 7.10.2.6 | La Gerencia de Riesgos No Financieros y Tecnología Informática definirán y revisarán los lineamientos para el desarrollo de software. | Sí | Pipeline con SonarQube, PIT y JaCoCo configurados. |
| 7.10.2.7 | Vincular seguridad de la información en el proceso del diseño del desarrollo de interfaces al Core. | Sí | Peer review incluido. Acta FM-005. |
| 7.10.2.8 | Establecer controles en las interfaces al Core de acuerdo con la sensibilidad de los datos. | Sí | [Evidencia: ej. Encriptación JWE/RSA. SanitizadorDatos en logs.] |
| 7.10.2.9 | Usar controles de cifrado si la información es de tipo confidencial. | Sí | [Evidencia: ej. JWE/RSA. Certificados vía Vault.] |
| 7.10.2.10 | Establecer controles de entrada, procesamiento y salida para garantizar autenticidad e integridad. | Sí | [Evidencia: ej. ValidadorArgumento en dominio. Fail-fast en propiedades.] |
| 7.10.2.11 | Verificar exactitud, suficiencia y validez de los datos de transacciones. | Sí | Tests unitarios y de mutación cubren las validaciones de negocio. |
| 7.10.2.12 | Realizar pruebas en los diferentes ambientes antes de producción. | Sí | Pipeline: develop → des → pru → prepro → pro. |
| 7.10.2.13 | Los desarrollos deben evitar el uso de configuraciones por defecto. | Sí | Todos los valores provienen de Vault o variables de entorno. |
| 7.10.2.14 | No está permitido quemar usuarios y/o perfiles en el código fuente. | Sí | Gitleaks escanea automáticamente. Vault gestiona todas las credenciales. |
| 7.10.2.15 | La depuración de privilegios deberá iniciarse desde ambiente de pruebas. | Sí | AppRole con permisos mínimos por ambiente. |
| 7.10.2.16 | No está autorizado almacenar sentencias SQL en BD. | Sí | Sin stored procedures. Solo Flyway para DDL. |
| 7.10.2.17 | Los desarrollos con parámetros frecuentes deberán tener paneles de mantenimiento. | N/A | Parámetros gestionados vía Vault y Azure DevOps Library. |
| 7.10.2.19 | Todo desarrollo que contenga el PAN debe ocultarlo/ofuscarlo. | N/A | [Indicar si aplica o no para este microservicio] |

---

## 9. Pruebas al Desarrollo

| Tipo de Prueba | Herramienta | Cobertura objetivo | Descripción |
|----------------|-------------|-------------------|-------------|
| Unitarias | JUnit 5 + Mockito | >80% líneas | Pruebas aisladas de cada clase de dominio y aplicación. |
| Integración | Spring Boot Test + H2 | >70% integradas | Pruebas de adaptadores con infraestructura en memoria. |
| Arquitectura | ArchUnit | 100% | Validan que las capas no tengan dependencias cruzadas indebidas. |
| Cobertura de código | JaCoCo + SonarQube | >80% | Reportes XML enviados a SonarQube. Quality gate debe pasar. |
| Mutación | PIT Mutation Testing | >70% mutantes | Validan la efectividad de las pruebas unitarias. |
| Análisis de secretos | Gitleaks v8.28.0 | 100% commits | Detecta credenciales expuestas en el historial de commits. |
| Análisis de dependencias | Dependency Track / OWASP | 100% deps | CVEs en dependencias vía BOM CycloneDX. |
| Código estático | SonarQube | Quality Gate OK | Code smells, bugs, vulnerabilidades y cobertura. |

**Checklist de verificación post-despliegue:**

- [ ] Pod en estado `Running` en el namespace correspondiente.
- [ ] Endpoint `GET /[context-path]/actuator/health` responde `{"status":"UP"}`.
- [ ] Logs del pod confirman conexión exitosa con Vault y carga de todos los secrets.
- [ ] [Verificación funcional específica del microservicio]
- [ ] [Verificación de caché / Redis si aplica]
- [ ] Verificar en PostgreSQL que Flyway aplicó las migraciones y las tablas existen.

---

## 10. Anexos

| Artefacto | Descripción / Ubicación |
|-----------|------------------------|
| `azure-pipelines.yml` | Pipeline CI/CD. Repositorio `[microservicio]`, rama `develop`. |
| `deployment.yaml` | Manifiesto Kubernetes (Deployment + Service + Ingress ALB). Raíz del repositorio. |
| `Dockerfile` | Imagen Docker (`amazoncorretto:21-alpine`). Raíz del repositorio. |
| Migraciones Flyway | `microservicio/src/main/resources/db/migration/DDL/` |
| BOM CycloneDX | `microservicio/build/reports/bom.xml` *(generado por el pipeline)* |
| Reportes JaCoCo | `microservicio/dominio\|infraestructura/build/reports/jacoco/` |
| Reportes PIT | `microservicio/dominio\|infraestructura/build/reports/pitest/` |
| Repositorio ADO | `https://dev.azure.com/GestionRequerimientos/BancaPorWhatsappCICD/_git/[microservicio]` |
| [Documento adicional] | [Ruta o descripción del documento adicional si aplica] |

---

## 11. Control de Versiones del Documento

| Versión | Fecha | Descripción | Autor |
|---------|-------|-------------|-------|
| 1.0 | 01/01/2015 | Creación del documento plantilla | BMM |
| 2.0 | 18/01/2023 | Modificación de plantilla, ampliación de PT-007, versionamiento y arquitectura | Dirección de Aplicaciones |
| 3.0 | 26/01/2023 | Modificación en el formato, versionamiento y parametrización | Dirección de Aplicaciones |
| **[4.0]** | **[dd/mm/yyyy]** | **[Descripción del cambio] – HU [XXX.X]: [Título de la HU]** | **[Desarrollador / Equipo]** |
