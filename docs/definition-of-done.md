# Definition of Done (DoD) - TaskFlow

Para que una Historia de Usuario o Tarea se considere **"Terminada"**, debe cumplir con TODOS los siguientes puntos:

## 1. Código
- [ ] El código compila y se ejecuta sin errores en la consola.
- [ ] Se sigue la guía de estilo acordada (ej. camelCase, nombres descriptivos).
- [ ] No hay código comentado ni `console.log()` de depuración olvidados.
- [ ] La funcionalidad cumple con todos los Criterios de Aceptación de la Historia de Usuario.

## 2. Control de Versiones
- [ ] Los cambios están en una rama con un nombre descriptivo (ej. `feature/agregar-tarea`).
- [ ] Se ha creado un Pull Request (PR) hacia la rama `develop` o `main`.
- [ ] El PR ha sido revisado y aprobado por al menos otro miembro del equipo (Code Review).

## 3. Pruebas
- [ ] Se han realizado pruebas manuales para verificar que no se rompió nada (pruebas de regresión).
- [ ] (Opcional pero recomendado) Se han escrito pruebas unitarias para la lógica principal.

## 4. Documentación
- [ ] El `README.md` o la documentación técnica se ha actualizado si es necesario.
- [ ] La tarjeta en el tablero Kanban se ha movido a la columna "Done".