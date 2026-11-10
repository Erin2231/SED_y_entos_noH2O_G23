# Máquina expendedora en FPGA

Trabajo de VHDL de Sistemas Electrónicos Digitales (UPM ETSIDI), curso 2026-2027.
Placa: Digilent Nexys 4 DDR / Nexys A7 (Artix-7).

Mini máquina expendedora real: reconoce monedas de 10c, 20c, 50c y 1 €, dispensa
el producto con una espiral motorizada y devuelve el dinero si el importe no es exacto.
Todo va dentro de una carcasa impresa en 3D.

## Estado

Fase 0: definición. Ver:

- [Lista de materiales](docs/materiales.md)
- [Dudas abiertas](docs/dudas.md)

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `src/` | Un `.vhd` por entidad, incluido `top.vhd` |
| `tb/` | Un `*_tb.vhd` por entidad y sus `*.wcfg` |
| `constraints/` | Fichero `.xdc` |
| `ip/` | IP de Vivado (solo el `.xci`) |
| `vivado/` | Proyecto `.xpr` (las fuentes se enlazan desde `src/`, no se copian) |
| `scripts/` | Tcl para recrear el proyecto |
| `hardware/` | Esquema, reparto de pines y fotos de la placa soldada |
| `cad/` | Piezas de la carcasa: `fuente/`, `step/` y `stl/` |
| `docs/` | Memoria, diagramas y fichas de cada módulo |

## Equipo

| Rol | Persona |
| --- | --- |
| Arquitecto del sistema | _por decidir_ |
| Programador | _por decidir_ |
| Calidad (testbenches) | _por decidir_ |
