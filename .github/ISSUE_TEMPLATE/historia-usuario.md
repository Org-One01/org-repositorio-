---
name: Historia de Usuario
about: Plantilla para crear una nueva historia de usuario
title: '[HU-002] - Registrar nueva tarea con fecha límite'
labels: 'historia de usuario, sprint 1'
assignees: 'estudiante-dev'
---

## Descripción de la Historia
**Como** estudiante universitario,
**Quiero** registrar una nueva tarea con su título, descripción y fecha límite,
**Para** poder organizar mis entregas académicas y no olvidar ninguna fecha.

## Criterios de Aceptación
- [ ] El sistema debe mostrar un formulario con los campos: Título (obligatorio), Descripción (opcional) y Fecha límite (obligatorio).
- [ ] Al hacer clic en "Guardar", la tarea debe aparecer inmediatamente en la lista principal.
- [ ] El campo "Título" no debe permitir más de 50 caracteres.
- [ ] El campo "Fecha límite" debe validar que la fecha seleccionada no sea anterior al día de hoy.
- [ ] Si el formulario está incompleto, debe mostrar un mensaje de error claro al usuario.

## Tareas Técnicas (Checklist para el desarrollador)
- [ ] Crear el formulario HTML con sus respectivos `id` y `class`.
- [ ] Estilizar el formulario para que sea responsive (CSS).
- [ ] Capturar los datos del formulario con JavaScript (`document.getElementById` o `querySelector`).
- [ ] Implementar la validación de la fecha (que no sea en el pasado).
- [ ] Crear la función que agrega el objeto tarea a un array global.
- [ ] Renderizar la nueva tarea en el DOM (actualizar la lista visualmente).
- [ ] Limpiar los campos del formulario después de guardar exitosamente.
- [ ] Escribir pruebas unitarias para la función de validación de fechas.

## Estimación
**Puntos de historia:** 3