# Mini arcade Snake (SED – Microcontroladores 2026-27)

Máquina recreativa en miniatura que juega a Snake sobre una STM32F4 Discovery. El juego se ve en una matriz LED RGB 16x16 y una pantalla LCD de texto 20x4 muestra los menús, la configuración y los récords. Todo va dentro de una carcasa impresa en 3D.

## Estructura

| Carpeta | Contenido |
|---|---|
| `firmware/` | Proyecto STM32CubeIDE (pendiente) |
| `lib/` | Bibliotecas propias: matriz, LCD, RTC, joystick, zumbador y lógica del juego |
| `hardware/` | Esquema, shield y [lista de materiales](hardware/bom.md) |
| `cad/` | Carcasa: `fuente/`, `step/`, `stl/` (pendiente) y `planos/` con las cotas |
| `docs/` | Diagramas, memoria y [dudas abiertas](docs/dudas.md) |
| `tests/` | Pruebas en PC de la lógica del juego (pendiente) |

## Equipo

| Persona | Responsabilidad |
|---|---|
| _por definir_ | Salida visual (matriz, LCD) y carcasa CAD |
| _por definir_ | Entradas, sonido y shield soldado |
| _por definir_ | Lógica del juego, récords y repositorio |
