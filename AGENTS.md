# Instrucciones del agente

## Formato de preguntas

Usar el snippet de **respuesta rápida**: ícono + letra + texto.

## Modo nota

> Rectifica la rama en la que trabajamos.

## Gestión de ramas

### Crear rama

Cuando se solicite crear una rama:

1. Preguntar desde qué rama se crea.
2. Crear la rama con el formato:
   ```
   hu-[ID]-[descripcion-kebab-case]
   ```

### Commit inicial

Luego de crear la rama, realizar un commit inicial vacío:
```
chore: iniciar desarrollo de HU [ID]
```

### Tipos de commit
/
Usar:
- `feat:` — nueva funcionalidad
- `fix:` — corrección de errores
- `refactor:` — refactorización
- `docs:` — documentación
- `chore:` — tareas de mantenimiento

## Sincronización con `git-doc-sync`
Si se crea o modifica un archivo en `Doc_BancaPorWhatsapp`:

1. Ofrecer sincronizar documentacion.
2. Si el usuario acepta, ejecuta la skill. 
