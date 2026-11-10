# Preguntas y dudas iniciales

Estado: abierto (2026-11-07). Marcad cada una cuando esté resuelta y apuntad la respuesta debajo.

## Bloqueantes (antes de comprar)

- [ ] **¿Qué Discovery tenéis: STM32F411E-DISCO o STM32F407G-DISC1?** Cambia los pines libres, el acelerómetro (I2C en F411, SPI en F407) y si hay DAC (solo F407) o generador de números aleatorios por hardware (solo F407).
- [ ] **¿Una Discovery por persona o una para el grupo?** Si hay varias, cada uno puede probar su driver en paralelo.
- [ ] **¿Matriz WS2812B 16x16 (RGB) o matrices MAX7219 8x8 (monocolor)?** La WS2812B luce más y usa DMA, pero es más difícil y consume más. MAX7219 es más sencilla por SPI. Propuesta: WS2812B.
- [ ] **¿Presupuesto máximo del grupo?** El BOM ronda los 70 € sin la placa.
- [ ] **¿Dónde compramos y con qué plazo?** AliExpress tarda 2–4 semanas; Amazon o tienda local en días. Condiciona el calendario.

## Con el tutor

- [ ] ¿Aprueba el tema "mini arcade Snake" con los extras propuestos?
- [ ] ¿Cuenta el acelerómetro de la propia placa como sensor, o tiene que ser externo?
- [ ] ¿Es suficiente el ADC como "convertidor A/D o D/A", o quiere también DAC?
- [ ] ¿Fecha de la defensa y de la entrega en Moodle?
- [ ] ¿Se puede usar código de terceros (por ejemplo, una librería para la LCD) si se cita, o todo debe ser propio?

## Fabricación

- [ ] ¿Qué impresora 3D vais a usar y qué tamaño de cama tiene? Decide en cuántas piezas va la carcasa (~220 x 380 x 250 mm).
- [ ] ¿Qué programa de CAD: Fusion 360 (licencia educativa) u Onshape (navegador, colaborativo)?
- [ ] ¿Tenéis soldador, estaño y polímetro, o hay que usar el del laboratorio?

## Resueltas

- [x] Sensor de moneda: descartado (2026-11-07). La partida empieza con START.
- [x] Mini pantalla: LCD de texto 20x4 por I2C en lugar de OLED, por ser más sencilla de programar (2026-11-07).

## Organización

- [ ] ¿Cómo se reparte el trabajo? Propuesta: persona 1 salida visual + CAD; persona 2 entradas y sonido + shield soldado; persona 3 lógica del juego + repo.
- [x] ¿Un repositorio para los dos trabajos o uno para cada uno? Uno para los dos (2026-11-10).
- [x] ¿Quién crea el repo en GitHub y quién lo administra? Ian (@Erin2231), 2026-11-10.
