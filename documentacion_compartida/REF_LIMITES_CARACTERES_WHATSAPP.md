# Límites de caracteres — WhatsApp Business API

Referencia rápida para escribir plantillas y mensajes dinámicos en el flujo de ms-banca-conversacion.

## TEXT (mensaje de texto libre)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Body** | 4096 caracteres | Soporta `*negritas*` y `_cursivas_` |

## BOTONES (Buttons — WhatsApp UI nativo)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Título del botón** | 20 caracteres | Máximo 3 botones por mensaje |

## LISTA (Interactive List)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Botón "Ver opciones"** | 20 caracteres | El label del botón que abre la lista |
| **Título de sección** | 24 caracteres | `Seccion.titulo` |
| **Título de fila (opción)** | 24 caracteres | `Fila.titulo` |
| **Descripción de fila** | 72 caracteres | `Fila.descripcion` |
| **Descripción del mensaje de lista** | 1024 caracteres | El cuerpo (body) que se muestra antes de la lista |
| **Número de filas** | 10 máx TOTAL | Sumatoria de todas las secciones combinadas |
| **Número de secciones** | 10 máx | |

## BOTONES INTERACTIVOS (Interactive Buttons / Reply Buttons)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Título del botón** | 20 caracteres | Máximo 3 botones en total por mensaje |
| **Cuerpo del mensaje** | 1024 caracteres | Soporta `*negritas*` |
| **Pie de página** | 60 caracteres | Opcional |

## BOTONES DE LLAMADA A LA ACCIÓN (CTA - Enlaces y Teléfonos)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Título del botón** | 20 caracteres | Texto visible (25 caracteres si es dentro de una Plantilla aprobada) |
| **URL (Hipervínculo)** | 2000 caracteres | Longitud máxima del enlace (payload) |
| **Número de teléfono** | 20 caracteres | Formato internacional sugerido (ej. +573001234567) |

## NOTIFICACIONES (Templates)

| Campo | Límite | Notas |
|-------|--------|-------|
| **Body** | 550 caracteres | Límite crítico para plantillas (Utility, Marketing). Máximo 10 emojis. |
| **Componente de botón (URL/Texto)** | 25 caracteres | Título del botón (CTA o Quick Reply en plantillas) |
| **Componente de botón (URL)** | 2000 caracteres | Valor máximo de la URL dinámica / Payload |
| **Componente texto dinámico** | 256 caracteres | Cada `{n}` reemplazable en el cuerpo |
| **Número de componentes** | 10 botones máx | Limite total de botones dentro de la plantilla |

## Fuentes

- [WhatsApp Cloud API Messages Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages)
- [WhatsApp Business Platform Limits](https://developers.facebook.com/docs/whatsapp/cloud-api/guides#message-length)