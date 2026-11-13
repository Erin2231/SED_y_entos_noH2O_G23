# Inventario: material que ya tenemos

Estado: borrador (2026-11-11), sacado de una foto. Las cantidades son las del etiquetado: contad
las piezas y medid lo que se indica antes de diseñar encima. La lista de compra está vacía por
ahora ([lista_compra.md](lista_compra.md)).

## Placas, máquinas y programas

| Material | Para qué |
| --- | --- |
| Nexys 4 DDR | Expendedora (VHDL) |
| STM32 Discovery (confirmar si es F411E o F407G) | Snake |
| Impresora Bambu Lab A1 (cama 256 × 256 mm) + PLA | Carcasas y piezas mecánicas de los dos trabajos |
| Fusion 360, Vivado, STM32CubeIDE | CAD, FPGA y micro |

## Componentes

| Material | Cantidad | Uso previsto |
| --- | --- | --- |
| Servo SG90 azul (180°, 9 g) | 6 | Expendedora: compuerta de monedas (pieza B del carril ya lleva soporte SG90). Quedan 5 libres |
| Servo Feetech FT1117M (mini, piñones metálicos, ~3,5 kg·cm, ~120°) | 1 | Repuesto fuerte. Si tiene 4 cables (cable verde = versión FB), da la posición real del eje en una salida analógica: se podría leer con el XADC de la Nexys (Pmod JXADC). Opcional |
| Imanes de neodimio (discos; medid diámetro y grosor) | ~20 | Cierres: cajón de la hucha, puertas de mantenimiento, tapa del carril, bahía de la Nexys. Hueco impreso = diámetro + 0,2 mm, pegado con cianoacrilato |
| Pulsadores táctiles 6×6 (alturas 4,3 a 12 mm) y 7×7 con enclavamiento | 100 | Botones de las dos máquinas con capuchón impreso (los de 11-12 mm sobresalen del panel). Los 7×7 con enclavamiento sirven de interruptor de señal, no de alimentación |
| Protoboard MB-102 | 1 | Probar cada bloque antes de soldarlo |
| Tornillos de rosca chapa (autorroscantes) | 360 | Uniones de la carcasa directamente en el PLA, sin insertos. Medidas abajo |

### Tornillos (rosca chapa)

| Medida | Cant. | Agujero guía en PLA |
| --- | --- | --- |
| M3 × 16 / × 20 / × 30 | 60 / 60 / 30 | 2,5 mm |
| M3,5 × 16 / × 20 / × 25 | 50 / 50 / 30 | 2,9 mm |
| M4 × 20 / × 30 / × 40 | 30 / 30 / 20 | 3,3 mm |

El más corto mide 16 mm: los resaltes (bosses) del CAD tienen que tener al menos 14 mm de rosca
útil. Para piezas finas (tapas, portasensores del carril) hacen falta tornillos M2 cortos, que no
están en la caja; cada SG90 trae 2 o 3 tornillitos M2, que pueden servir para las primeras pruebas.

### Kit "electronic components kit"

| Familia | Valores | Cantidad |
| --- | --- | --- |
| LED visibles 3 o 5 mm | azul, amarillo, verde, rojo, blanco | 20 de cada |
| Resistencias 1/4 W | 10 Ω a 1 MΩ (incluye 220 Ω, 330 Ω, 1 kΩ, 4,7 kΩ, 10 kΩ) | 20 de cada valor |
| Diodos | 1N4148, 1N4007, 1N5819, 1N5399, 1N5408, 1N5822, FR107, FR207 | 5-25 de cada |
| Transistores | 2N2222, 2N3904, 2N3906, S8050, S8550, BC/C1815, A1015, 2N5551, etc. | 10 de cada |
| Electrolíticos 50 V | 0,22 µF a 470 µF | 10 de cada |
| Cerámicos | 2 pF a 100 nF | 10 de cada |

**Ojo:** los LED del kit son visibles, no infrarrojos, y no hay fototransistores, así que no sirven
para las barreras del carril de monedas. Tampoco hay MOSFET, optoacopladores, circuitos integrados,
LDR, zumbador ni condensadores de más de 470 µF (para 1000 µF se pueden poner dos de 470 µF en paralelo).
