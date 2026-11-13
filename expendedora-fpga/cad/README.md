# CAD de la carcasa

Las piezas ya modeladas van por módulos, cada uno con su README:

| Carpeta | Contenido |
| --- | --- |
| `rampa-monedas/` | Carril de monedas A, cubilete B, trampilla y acople del servo: modelo, planos, STEP, STL y script de Fusion |
| `maquina/` | Bocetos, plano del corte 1, crestas en U y canal (`crestas/`), pulsador de cancelar (`pulsador/`) |

Para piezas nuevas hechas a mano en Fusion, cada pieza se sube en tres formatos:

| Carpeta | Contenido |
| --- | --- |
| `fuente/` | Fichero nativo de Fusion 360 (`.f3d`: *File → Export → .f3d*) |
| `step/` | Exportación `.step` (la abre cualquier programa) |
| `stl/` | Exportación `.stl` lista para laminar (*botón derecho en el cuerpo → Save as Mesh*) |

Nombre: `<pieza>_v<versión>.<ext>`, por ejemplo `frontal_v1.stl`.
Los G-code no se suben porque dependen de cada impresora.
