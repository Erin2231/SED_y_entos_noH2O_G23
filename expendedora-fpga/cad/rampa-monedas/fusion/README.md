# Script de Fusion 360

`MonedasSED/` es un script de Fusion 360 que crea las piezas del sistema de monedas
(A carril, A-F pared de fototransistores, A-T tapa, A-S portasensor y B cubilete) en un diseño nuevo, un componente por pieza.

## Cómo ejecutarlo
1. Copiad la carpeta `MonedasSED` entera (con `MonedasSED.py` y `MonedasSED.manifest`) a vuestro PC.
2. En Fusion: pestaña **Utilidades** › **Complementos** › **Scripts y complementos** (o tecla Mayús+S).
3. En la pestaña **Scripts**, pulsad **+** › "Script o complemento desde el dispositivo" y elegid la carpeta `MonedasSED`.
4. Seleccionadlo y pulsad **Ejecutar**. Tarda unos segundos.
5. Al final sale un mensaje con el volumen de cada pieza comparado con el modelo de referencia.
   Si alguno sale marcado con ¡¡ o aparece un error, copiad el texto del mensaje.

## Cambiar cotas
Las cotas están en el bloque PARÁMETROS al principio de `MonedasSED.py` (mm y grados).
Editad, guardad y volved a ejecutar: crea un diseño nuevo. `PARED = "derecha"` hace la versión simétrica.
Dentro de Fusion cada operación queda con nombre en la línea de tiempo y se puede editar a mano.

## Comprobación sin Fusion
`probar_geometria.py` reconstruye las mismas operaciones con CadQuery y las compara con `../modelo.py`
(diferencia de volumen 0 en todas las piezas).
