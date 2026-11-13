# Crestas en U y caja del canal

Tres piezas de PLA con paredes de 3 mm, fijadas con lengüetas iguales a las de los cubiletes (14 × 13 × 3, agujero Ø3,5 para M3 + tuerca a la pared lateral de la columna):

| Pieza | Qué es | Lengüetas | Impresión |
|---|---|---|---|
| CR-1 | Cresta 1 (bajo B): carril en U de 46 de ancho, rampas a 30°, 72 de largo | 3, por debajo (vértice + una por rampa) | tumbada sobre la cara de la pared de la máquina, con soporte solo bajo la pared de la U de enfrente |
| CR-2 | Cresta 2 (bajo C): igual, 210 de largo (153 delante, 57 detrás) | 3, por debajo | igual que CR-1 |
| CR-3 | Caja de 3 lados del canal de no válidas (el 4º lado es la pared de la máquina) | 4 orejas simples, dos por chapa | igual que CR-1 (soporte solo bajo la pared del fondo) |

- Paredes de la U: 15 mm sobre el suelo del carril. Una moneda de 2 € de canto tiene el centro a 12,9 mm, así que no vuelca por encima.
- `crestas.py` genera los STEP y STL. `comprobar.py` revisa que no choquen con nada del corte 1, incluidas las trampillas a 0, ±20 y ±40°. `hoja.py` dibuja `crestas.pdf`.
- Las coordenadas de los taladros en la pared lateral están en la hoja y en la salida de `crestas.py`.

## Script de Fusion 360

`fusion/CrestasSED/` (con `CrestasSED.manifest`) funciona igual que MonedasSED: Utilidades > Complementos > Scripts y complementos > "+" > añadir la carpeta > Ejecutar. Crea las 3 piezas ya colocadas en su sitio de la máquina. `PARED = "izquierda"` por defecto, como MonedasSED.

`fusion/probar_geometria.py` reconstruye las operaciones del script y las compara con `crestas.py`: la diferencia sale 0 mm³ en las tres piezas.
