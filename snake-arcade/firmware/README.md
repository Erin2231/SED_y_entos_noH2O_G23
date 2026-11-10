# Firmware STM32CubeIDE

Aquí va el proyecto de STM32CubeIDE del Snake.

## Crear el proyecto (solo la primera vez, una persona)

1. *File → New → STM32 Project*, elegir la placa (STM32F411E-DISCO o STM32F407G-DISC1, ver
   [dudas](../docs/dudas.md)).
2. Nombre `snake`, **desmarcar** "Use default location" y elegir esta carpeta (`snake-arcade/firmware`).
3. *Targeted Project Type*: STM32Cube. Generar.
4. Enlazar las bibliotecas propias: botón derecho en el proyecto → *New → Folder → Advanced →
   Link to alternate location* → `PARENT-1-PROJECT_LOC/lib`.
   Después *Properties → C/C++ Build → Settings → MCU GCC Compiler → Include paths* y añadir
   `../../lib/<modulo>` por cada módulo.
5. Subir: `.ioc`, `.project`, `.cproject`, `Core/`, `Drivers/`, `*.ld` y el `.launch`.

## Abrir en otro ordenador

*File → Import → Existing Projects into Workspace* → esta carpeta.
El workspace de CubeIDE debe estar **fuera** del repositorio.
