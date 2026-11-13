# Carril de monedas (pieza A) y cubilete de espera (pieza B)

- `planos/planos_carril_cubilete.pdf`: 7 hojas A4 apaisado con cotas (portada e índice, situación, A, secciones, placa/tapa/portasensor, B, impresión y montaje).
- `step/`: modelos para importar en Fusion 360 (versión para la pared IZQUIERDA, la de los planos).
- `stl/`: para laminar directamente en Bambu Studio (PLA, sin soportes).
- `modelo.py`: modelo paramétrico (CadQuery). Cambiad las cotas arriba del fichero y ejecutad `python3 modelo.py out`.
- `planos.py` + `vistas.py` + `pdf.js`: regeneran las hojas SVG y el PDF a partir del modelo.

Piezas: A carril de medida (cuña con los LED, suelo, placa frontal y 6 lengüetas M3) · A-F pared de fototransistores, separada (3× M2 × 6 al suelo, encaja en ranuras del suelo y de la tapa) · A-T tapa (2× M2 × 6) · A-S portasensor regulable (×5) · B cubilete sin fondo con soporte SG90 y 4 lengüetas M3 · B-TP y B-TS trampilla en dos mitades · B-PZ postizo (×2) · B-AC acople del servo con eje.

## Cambios respecto al PDF (planos_carril_cubilete.pdf, versión del 2026-11-11)
- La pared de fototransistores es ahora una pieza aparte (A-F). Corte de referencia: `planos/corte_B3_piezas_separadas.png`.
- El suelo del carril llega 9 mm más allá de la pared (apoyo del ala de A-F) y lleva una ranura de 1 mm para su pie.
- La tapa A-T es 2 mm más ancha y lleva una ranura de 1 mm donde encaja el borde superior de A-F.
- A-F lleva en la cara exterior un carril guía de 9,2 × 0,5 por cada portasensor B1-B5: el A-S solo desliza arriba/abajo y no gira al apretar el tornillo (guía M2 de 3 mm desde el fondo del carril).
- Cubilete B: el pivote de la trampilla es un agujero ciego Ø4,4 × 2,5 en la pared del lado de montaje (0,5 de piel); el poste Ø4 lo lleva la mitad B-TP.
- Tornillos: todos los M2 son M2 × 6 autorroscantes (tapa, ala de A-F y portasensores). Guías de la tapa de 5 de fondo.
- Corregido: la ranura de la placa frontal mide 25,2 de alto (en el dibujo de la hoja 5 aparece más larga).

## Trampilla en dos mitades (2026-11-12)
Esquema: `planos/trampilla_montaje.png`. Comprobación: `python3 chk_trampilla.py` (sin choques a 0°, ±20° y ±40°, y montaje paso a paso sin choques).
- 38,6 × 38,6 (0,7 de holgura con el cubilete), chapa de 2,4, cara de arriba 3 mm por encima del eje, espina central y dos nervios a ±11 mm.
- Junta a 45° en el centro: B-TS apoya encima de B-TP, así no se cae antes de pegar y las dos se imprimen sin soportes.
- Dos postizos 3 × 3 × 17,6 pegados por debajo en los nervios, cruzando la junta (9 mm en cada mitad).
- El eje del lado del servo es parte del acople B-AC: entra desde fuera por la ventana del SG90 y el agujero Ø4,4 hasta un alojamiento en D de 8 mm en B-TS (entra 6, quedan 2 de ajuste). El brazo simple del SG90 va horizontal (+X) con la trampilla horizontal, apoyado en un rebaje de 1 mm y atornillado con 2 M2×6 (agrandad a Ø2 dos agujeros del brazo; ranura guía de 1,7 en el acople, vale cualquier separación de agujeros).
- Soporte del servo 4 mm más separado (SERVO_GAP 12 → 16): en el prototipo, el brazo quedaba a 1 mm de la pared y el acople no cabía.
- Montaje: B-TP (poste al agujero ciego) → B-TS desde arriba → B-AC por la ventana → postizos con cianocrilato → brazo atornillado al acople por la ventana → servo por la ventana y atornillado.
Por debajo del soporte del servo dejad unos 6 mm libres: el acople baja hasta ahí a 40°.

## Orientación de impresión
- A: tumbada, con la cara de montaje (la que toca la pared) sobre la cama.
- A-F: plana, con la cara del canal (la de las rendijas) sobre la cama.
- A-T: plana, con la cara de la ranura sobre la cama. A-S: rendija sobre la cama. B: de pie, borde abierto abajo.
- B-TP y B-TS: cara de arriba (donde caen las monedas) sobre la cama. B-AC: de pie sobre la cara del brazo, eje hacia arriba, 4 perímetros. B-PZ: tumbados.
- Activad la compensación de pata de elefante en Bambu Studio (A-S tiene la rendija de 1 mm en las primeras capas).
- Agujeros horizontales que pueden salir justos: Ø2,4 del ala de A-F, Ø4,4 del pivote y del eje en B, alojamiento en D de B-TS. Repasad con broca a mano si rozan.
- Comprobación de encajes: `python3 comprobar.py`.
