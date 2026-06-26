# Instrucciones del agente

## Formato de preguntas

    Usar el snippet de **respuesta rápida**: 
    ||> ícono + letra + texto.

## Modo nota

    Siempre dejar nota en el chat al usuario: 
    ">Rectifica la rama en la que trabajamos."

## Gestión de ramas

### Crear rama

    Cuando se solicite crear una rama:

    1. Preguntar desde qué rama se crea.
    2. Crear la rama con el formato: hu-[ID]-[descripcion-kebab-case] o [descripcion-kebab-case] dependiendo del caso.

### Commit inicial [OBLIGATORIO]

    Luego de crear una rama, siempre realizar un commit inicial vacío:
    ```
    chore: iniciar desarrolcambio de HU [ID/descripcion]
    ```

### Al realizar commit [OBLIGATORIO] 
    Siempre Genera los mensajes de commit siguiendo estrictamente la convención:
        - usa siempre el formato <tipo>[ámbito opcional]: <descripción compacta pero detallada>.
            tipo:
                - `feat:` — nueva funcionalidad
                - `fix:` — corrección de errores
                - `refactor:` — refactorización
                - `docs:` — documentación
                - `chore:` — tareas de mantenimiento.
    Si el código rompe la compatibilidad anterior, incluye obligatoriamente BREAKING CHANGE: al inicio del cuerpo o pie del mensaje.
    Simepre mostrar preview (titulo y descripcion) al usuario para su aprobacion.

## Sincronización con `git-doc-sync`
    Si se crea o modifica un archivo en `Doc_BancaPorWhatsapp`:
    1. Ofrecer sincronizar documentacion.
    2. Si el usuario acepta, ejecuta la skill. 


## Gestion de comentarios de entrega [OBLIGATORIO]
    Cuando el usuario solicite agregar un comentario de ´ENTREGA RELEASE/FEATRUE/FIX/HOTFIX´ a un workitem(WI) el comentario agregado debe de seguir el siguiente formato:

```
    ┌────────────────────────────────────────────────────────────┐
    │  ENTREGA: {RELEASE | FEATURE | FIX | HOTFIX} v{versión}    │
    │  PROYECTO: {nombre_repo}                                   │
    │  FECHA: {YYYY-MM-DD}                                       │
    │  RAMA: {rama_origen}                                       │
    ├────────────────────────────────────────────────────────────┤
    │  DESCRIPCIÓN                                               │
    │  {Breve descripción de lo que se entrega}                  │
    │                                                            │
    │  CAMBIOS                                                   │
    │  • {feat|fix|chore}: {descripción del cambio}              │
    │  • {feat|fix|chore}: {descripción del cambio}              │
    │  • {feat|fix|chore}: {descripción del cambio}              │
    │                                                            │
    │  ENTREGABLES                                               │
    │  • release-notes.md                                        │
    │    → {ruta}/entrega_release/{nombre_repo}/{version}/       │
    │  • CONFIG-ENTORNO-PR                                       │
    │    → {ruta}/entrega_release/{nombre_repo}/{version}/       │
    │                                                            │
    │  ACCIONES REQUERIDAS AL BANCO                              │
    │  • Crear PR de {rama} → des                                │
    │  • Mergear PR a des                                        │
    │  • Taggear v{versión} en des                               │
    │  • Desplegar en DES                                        │
    │  • Configurar variables/colas según CONFIG-ENTORNO-PR      │
    │                                                            │
    │  NOTAS                                                     │
    │  {Notas adicionales si aplica}                             │
    └────────────────────────────────────────────────────────────┘
```
