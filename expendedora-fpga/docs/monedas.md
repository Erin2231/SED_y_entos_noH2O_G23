# Reconocimiento y separación de monedas

Estado: **elegida la opción A** (2026-11-11). Planos y montaje en [rampa-monedas.md](rampa-monedas.md), que sustituye a la tabla de barreras de esta ficha (ahora son 7, con dos de presencia).

## Datos de partida

Diámetros aproximados (de memoria: **medidlos con calibre** antes de diseñar).

| Moneda | Diámetro (mm) | ¿La aceptamos? |
| --- | --- | --- |
| 1c | 16,25 | No |
| 2c | 18,75 | No |
| 10c | 19,75 | Sí |
| 5c | 21,25 | Sí (desde el 2026-11-11) |
| 20c | 22,25 | Sí |
| 1 € | 23,25 | Sí |
| 50c | 24,25 | Sí |
| 2 € | 25,75 | No |

El orden por tamaño no es el del valor: el 5c cae entre el 10c y el 20c, y el 1 € entre el 20c y el 50c.
Entre monedas consecutivas solo hay 1 a 1,5 mm. El peso (1 € 7,5 g y 50c 7,8 g, aprox.) y el grosor
están todavía más juntos, así que **el diámetro es la única medida práctica**.

## Opción A (recomendada): medir sin separar

La máquina nunca da cambio, así que no hace falta separar las monedas físicamente: todas acaban
en la misma zona de espera y la compuerta las manda a la hucha o a la bandeja. Basta con **saber**
qué moneda ha pasado.

La moneda rueda de canto por un carril inclinado, apoyada en la pared trasera, y cruza barreras IR
colocadas a distintas alturas sobre el carril. Una barrera se corta solo si la moneda es más alta
que ella.

| Barrera | Altura sobre el carril (mm) | Para qué |
| --- | --- | --- |
| P | 10 | Presencia: ha pasado una moneda |
| B1 | 19,25 | Separa 2c (no corta) de 10c (corta) |
| B2 | 20,5 | Separa 10c de 5c |
| B3 | 21,75 | Separa 5c de 20c |
| B4 | 22,75 | Separa 20c de 1 € |
| B5 | 23,75 | Separa 1 € de 50c |

| Barreras cortadas | Moneda | Acción |
| --- | --- | --- |
| Solo P | 1c o 2c | Devolver |
| P, B1 | 10c | Aceptar |
| P, B1, B2 | 5c | Aceptar |
| P, B1 a B3 | 20c | Aceptar |
| P, B1 a B4 | 1 € | Aceptar |
| P, B1 a B5 | 50c | Aceptar |

El 2 € se rechaza mecánicamente: la ranura de entrada mide unos 25 mm de largo y no cabe.

En VHDL, `detector_monedas` guarda qué barreras se han cortado desde que se corta P hasta que se
libera, y entonces emite `coin_valid` y `coin_value`. Si el código no es válido, emite `coin_reject`.

**Detalles de construcción:**

- Las barreras distan solo entre 1 y 1,25 mm en altura y un LED de 3 mm no cabe en ese hueco, así
  que se **escalonan a lo largo del carril**, unos 10 mm entre una y otra.
- Delante de cada fototransistor va una rendija impresa de 1 mm de alto: lo que mide es la rendija,
  no el LED.
- El margen es de 0,5 mm por cada lado. Haced las rendijas como **piezas sustituibles** (o
  regulables con un tornillo M3) para calibrarlas con monedas reales sin reimprimir el carril.

## Opción B: separar físicamente (más vistosa, más larga)

Es una placa inclinada con agujeros de tamaño creciente. Cada moneda cae por el primer agujero en
el que cabe, y una barrera IR en cada canal la cuenta. Hacen falta 6 agujeros (19,25 · 20,5 ·
21,75 · 22,75 · 23,75 mm, y el final para el 50c), y los de 2c/1c y 5c van a la bandeja de rechazo.

Solo merece la pena si queréis un tubo visible por cada moneda. Ocupa mucho más (ver abajo), la
moneda tiene que deslizar despacio para no saltarse un agujero, y las tolerancias de impresión
(±0,2 mm) se comen casi todo el margen de 0,5 mm.

## ¿Cuánto debe medir el carril?

Velocidad de una moneda que rueda por un carril con inclinación θ: a = (2/3)·g·sin θ.

| Inclinación | Aceleración | Velocidad tras 50 mm | Tiempo en cruzar una barrera (moneda de 24 mm) |
| --- | --- | --- | --- |
| 10° | 1,1 m/s² | 0,34 m/s | unos 70 ms |
| 15° | 1,7 m/s² | 0,41 m/s | unos 60 ms |

Para la FPGA, 60 ms son 6 millones de ciclos de reloj: la velocidad no es problema para medir.
Sí lo es para la mecánica, porque más rápido significa más rebotes. Empezad con 10° a lo largo del
carril y la pared trasera inclinada unos 10 a 15° hacia atrás para que la moneda no se caiga.

| Tramo (opción A) | Longitud aprox. |
| --- | --- |
| Entrada: la moneda cae, rebota y se asienta | 40 a 60 mm |
| Zona de medida: 6 barreras escalonadas cada 10 mm | 60 mm |
| Salida hasta la zona de espera | 20 a 30 mm |
| **Total** | **unos 120 a 150 mm** |

Con la opción B, cada agujero necesita unos 30 a 35 mm, más la entrada: **unos 250 mm**.

## Próximos pasos

- [ ] Medir las monedas con calibre y corregir las tablas
- [ ] Imprimir un carril de prueba de 150 mm con la inclinación regulable (8°, 10°, 12°, 15°)
- [ ] Probar una sola barrera con rendija de 1 mm y un 20c frente a un 1 €
- [ ] Decidir: opción A, opción B o validador CH-926 (plan B)
