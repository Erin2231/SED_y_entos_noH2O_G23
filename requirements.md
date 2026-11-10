# Requisitos

Versiones que usamos los tres. Son las del PC de Ian (comprobadas el 2026-11-11).
**Instalad exactamente estas** para que los proyectos se abran sin convertirse ni reescribirse.

| Herramienta | Versión | Para qué | Notas |
| --- | --- | --- | --- |
| AMD Vivado (Design Suite) | **2026.1** | Expendedora FPGA | Instalación en `C:\AMDDesignTools\2026.1`. Con el soporte de placas Digilent (Nexys A7 / Nexys 4 DDR). |
| STM32CubeIDE | **2.2.0** | Snake STM32 | Instalación en `C:\ST\STM32CubeIDE_2.2.0`. |
| Paquete STM32Cube FW_F4 | **V1.28.3** | HAL y CMSIS del STM32F4 | En CubeIDE: *Help → Manage embedded software packages*. Si tenéis otra versión, el `.ioc` pide migrar: **decid que no**. |
| Autodesk Fusion 360 | **la actual** (se actualiza sola) | Carcasas 3D | Licencia educativa gratuita. Formato nativo `.f3d`; se exporta a STEP y STL. |
| Git | 2.4x o posterior | Control de versiones | Git for Windows, con Git Bash. |
| VS Code | la actual | Editar VHDL, C y documentación | Instalad las extensiones que recomienda el repo. |

## Placas

| Placa | Trabajo |
| --- | --- |
| Digilent Nexys A7-100T / Nexys 4 DDR | Expendedora |
| STM32F4 Discovery (F411E-DISCO o F407G-DISC1, por confirmar) | Snake |

## Si cambiamos de versión

Solo se cambia de versión si estamos los tres de acuerdo, y en una rama aparte
(`fpga/chore-vivado-20xx` o `snake/chore-cubeide-x.y`). Se apunta aquí la nueva versión en el mismo PR.
