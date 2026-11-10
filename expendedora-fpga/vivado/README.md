# Proyecto Vivado

Aquí va el `.xpr` de la expendedora. Las fuentes **no se copian aquí**: se enlazan desde
`../src`, `../tb` y `../constraints`.

## Crear el proyecto (solo la primera vez, una persona)

1. Vivado → *Create Project* → ubicación: esta carpeta, nombre `expendedora`,
   **desmarcar** "Create project subdirectory".
2. Placa: Nexys A7-100T (o Nexys 4 DDR, la que tengáis en el laboratorio).
3. Añadir fuentes de `../src`, simulación de `../tb` y restricciones de `../constraints`
   **sin marcar "Copy sources into project"**.
4. Guardar una copia recreable: en la consola Tcl
   `write_project_tcl -force ../scripts/recrear_proyecto.tcl`
   y subirla.

## Si el proyecto se rompe o no abre

Borra todo lo de esta carpeta menos este README y, desde la consola Tcl de Vivado:

```tcl
cd <ruta-del-repo>/expendedora-fpga/vivado
source ../scripts/recrear_proyecto.tcl
```

Lo que Vivado genera (`.runs/`, `.cache/`, `.sim/`...) está en el `.gitignore`.
