# Pulsador de cancelar

Táctil 6×6 del inventario + dos piezas impresas en PLA:

| Pieza | Fichero | Impresión |
|---|---|---|
| PC-E embellecedor (Ø11,5 × 11 + collarín Ø16 × 1,5) | `step/PC-E_embellecedor.step`, `stl/...` | collarín sobre la cama |
| PC-S soporte (26 × 26 × 8,6) | `step/PC-S_soporte.step`, `stl/...` | cara de atrás sobre la cama, sin soportes |

- Agujero del frontal: Ø12, en lat 55, z 176 (plano del corte 1, detalle E).
- El embellecedor sobresale 3 mm. Su collarín queda por dentro y no deja que se salga.
- El táctil va pegado en el soporte, con 0,1 mm de juego hasta el collarín. Las patas salen por las ranuras de atrás, donde se sueldan los cables.
- El soporte se pega al frontal. Su hueco Ø17 lo centra sobre el collarín.
- `H_PULS` en `pulsador.py` es el alto total del táctil (5 mm por defecto). Si el tuyo es distinto, cambia el valor y ejecuta `python3 pulsador.py`.
- Esquema de funcionamiento y montaje: `esquema_pulsador.pdf` (lo genera `esquema.py`).
