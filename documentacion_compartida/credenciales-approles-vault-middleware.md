# Role ID y Secret ID de los AppRoles - Vault Middleware

> Fecha de generación: 19 de febrero de 2026
>
> Vault: `http://vault-middle-des.bmm.com/`
>
> **Importante:** Los `secret-id` son credenciales sensibles. No compartir fuera del equipo autorizado.

---

## AppRoles de Banca

### 1. ms-banca-agente-humano

| Campo | Valor |
|-------|-------|
| **role-id** | `121172fb-b6cd-46b4-acdb-c3e4f08a0188` |
| **secret-id** | `83ee76df-a4f3-30e5-1649-025b1606aedd` |

---

### 2. ms-banca-auditoria

| Campo | Valor |
|-------|-------|
| **role-id** | `daf4bbbb-9ad4-5a9c-39dc-c925958ec4a3` |
| **secret-id** | `34363994-4b1e-6e74-a6cd-ae89bcbf369b` |

---

### 3. ms-banca-autenticacion

| Campo | Valor |
|-------|-------|
| **role-id** | `d1be6033-8652-4510-e918-cd2928623bf3` |
| **secret-id** | `6e520a6b-3daa-aca7-350f-8db15fcfcc97` |

---

### 4. ms-banca-conversacion

| Campo | Valor |
|-------|-------|
| **role-id** | `ad76ab39-410a-80cd-d0c3-0b5b4b1d41c6` |
| **secret-id** | `0db1596a-5f8d-d4f6-1446-519dfa554928` |

---

### 5. ms-banca-localizacion

| Campo | Valor |
|-------|-------|
| **role-id** | `2cafe026-95ba-2bf9-2d78-9942002f2b0c` |
| **secret-id** | `40538726-b9c0-3870-68b5-615371931326` |

---

### 6. ms-banca-notificaciones

| Campo | Valor |
|-------|-------|
| **role-id** | `e3cb1b0a-8a92-34c4-31fd-43565b1f9b60` |
| **secret-id** | `d8cb489e-3ad1-b65b-94eb-e641ddb3240e` |

---

### 7. ms-banca-productos

| Campo | Valor |
|-------|-------|
| **role-id** | `ec26357f-51df-8bf5-af2d-40e688c0c998` |
| **secret-id** | `15f83af6-45df-c007-9379-ff8ebc85973e` |

---

### 8. ms-banca-referidos

| Campo | Valor |
|-------|-------|
| **role-id** | `b3a1ae07-9935-fa68-1747-03575d72170d` |
| **secret-id** | `7f8a921d-fa6a-1331-6f86-b47265b9e02d` |

---

### 9. ms-banca-reportes

| Campo | Valor |
|-------|-------|
| **role-id** | `f945e0cc-e5ca-86b9-50b0-f855482c1af8` |
| **secret-id** | `18623e5e-124a-a308-066f-5c32e36d5f5e` |

---

### 10. ms-banca-retiros

| Campo | Valor |
|-------|-------|
| **role-id** | `164b90e4-7e2f-03d6-907a-34c2d5b9790c` |
| **secret-id** | `ab987a2a-2012-1bd3-dc2a-e65086971056` |

---

### 11. ms-banca-solicitud-producto

| Campo | Valor |
|-------|-------|
| **role-id** | `9e7c6188-57c6-7f27-ec25-3dafede6d70b` |
| **secret-id** | `b79d1854-20bb-1fe6-07e4-24d4c8d3e4af` |

---

### 12. ms-banca-terminos-condiciones

| Campo | Valor |
|-------|-------|
| **role-id** | `a6bf6c1b-c9df-2fb7-11c6-37e12fdf5621` |
| **secret-id** | `26022c91-a546-c353-a90c-84dc9d1b9caa` |

---

## AppRoles de Onboarding

### 13. ms-onboarding-auditoria-trazabilidad

| Campo | Valor |
|-------|-------|
| **role-id** | `17b05f5c-775c-288a-22f6-f5dd00eeee95` |
| **secret-id** | `63ff0750-73d5-2c81-8802-2ff23cc5efe1` |

---

### 14. ms-onboarding-orquestador-bus

| Campo | Valor |
|-------|-------|
| **role-id** | `0b0977ab-903e-67c3-f597-a21c953c6883` |
| **secret-id** | `ae70bcaa-67c1-14c2-23f4-a28b3049b2c4` |

---

### 15. ms-onboarding-registro-usuario

| Campo | Valor |
|-------|-------|
| **role-id** | `f9b496b6-045a-6e0d-701f-0f2c16da1314` |
| **secret-id** | `7e567d3f-94ad-e1a8-0927-63d2aa5351cd` |

---

## AppRoles de Middleware

### 16. ms-middleware-datos-maestros

| Campo | Valor |
|-------|-------|
| **role-id** | `47885174-0300-d669-36d5-0af5f4a4cbc6` |
| **secret-id** | `0f6e9a9d-3606-9e9d-d746-01e672dbd8e6` |

---

## Resumen

| # | AppRole | Políticas | role-id | secret-id |
|---|---------|-----------|---------|-----------|
| 1 | `ms-banca-agente-humano` | `politica-ms-banca-agente-humano` | `121172fb-b6cd-46b4-acdb-c3e4f08a0188` | `83ee76df-a4f3-30e5-1649-025b1606aedd` |
| 2 | `ms-banca-auditoria` | `politica-ms-banca-auditoria`, `politica-certificados` | `daf4bbbb-9ad4-5a9c-39dc-c925958ec4a3` | `34363994-4b1e-6e74-a6cd-ae89bcbf369b` |
| 3 | `ms-banca-autenticacion` | `politica-ms-banca-autenticacion`, `politica-certificados` | `d1be6033-8652-4510-e918-cd2928623bf3` | `6e520a6b-3daa-aca7-350f-8db15fcfcc97` |
| 4 | `ms-banca-conversacion` | `politica-ms-banca-conversacion`, `politica-certificados` | `ad76ab39-410a-80cd-d0c3-0b5b4b1d41c6` | `0db1596a-5f8d-d4f6-1446-519dfa554928` |
| 5 | `ms-banca-localizacion` | `politica-ms-banca-localizacion` | `2cafe026-95ba-2bf9-2d78-9942002f2b0c` | `40538726-b9c0-3870-68b5-615371931326` |
| 6 | `ms-banca-notificaciones` | `politica-ms-banca-notificaciones`, `politica-certificados` | `e3cb1b0a-8a92-34c4-31fd-43565b1f9b60` | `d8cb489e-3ad1-b65b-94eb-e641ddb3240e` |
| 7 | `ms-banca-productos` | `politica-ms-banca-productos`, `politica-certificados` | `ec26357f-51df-8bf5-af2d-40e688c0c998` | `15f83af6-45df-c007-9379-ff8ebc85973e` |
| 8 | `ms-banca-referidos` | `politica-ms-banca-referidos`, `politica-certificados` | `b3a1ae07-9935-fa68-1747-03575d72170d` | `7f8a921d-fa6a-1331-6f86-b47265b9e02d` |
| 9 | `ms-banca-reportes` | `politica-ms-banca-reportes`, `politica-certificados` | `f945e0cc-e5ca-86b9-50b0-f855482c1af8` | `18623e5e-124a-a308-066f-5c32e36d5f5e` |
| 10 | `ms-banca-retiros` | `politica-ms-banca-retiros`, `politica-certificados` | `164b90e4-7e2f-03d6-907a-34c2d5b9790c` | `ab987a2a-2012-1bd3-dc2a-e65086971056` |
| 11 | `ms-banca-solicitud-producto` | `politica-ms-banca-solicitud-producto` | `9e7c6188-57c6-7f27-ec25-3dafede6d70b` | `b79d1854-20bb-1fe6-07e4-24d4c8d3e4af` |
| 12 | `ms-banca-terminos-condiciones` | `politica-ms-banca-terminos-condiciones`, `politica-certificados` | `a6bf6c1b-c9df-2fb7-11c6-37e12fdf5621` | `26022c91-a546-c353-a90c-84dc9d1b9caa` |
| 13 | `ms-onboarding-auditoria-trazabilidad` | `politica-ms-onboarding-auditoria-trazabilidad`, `politica-onboarding-microservicios-host`, `politica-certificados`, `politica-onboarding-redis` | `17b05f5c-775c-288a-22f6-f5dd00eeee95` | `63ff0750-73d5-2c81-8802-2ff23cc5efe1` |
| 14 | `ms-onboarding-orquestador-bus` | `politica-ms-onboarding-orquestador-bus`, `politica-onboarding-microservicios-host`, `politica-certificados`, `politica-onboarding-redis` | `0b0977ab-903e-67c3-f597-a21c953c6883` | `ae70bcaa-67c1-14c2-23f4-a28b3049b2c4` |
| 15 | `ms-onboarding-registro-usuario` | `politica-onboarding-microservicios-host`, `politica-certificados` | `f9b496b6-045a-6e0d-701f-0f2c16da1314` | `7e567d3f-94ad-e1a8-0927-63d2aa5351cd` |
| 16 | `ms-middleware-datos-maestros` | `politica-ms-middleware-datos-maestros`, `politica-certificados` | `47885174-0300-d669-36d5-0af5f4a4cbc6` | `0f6e9a9d-3606-9e9d-d746-01e672dbd8e6` |
