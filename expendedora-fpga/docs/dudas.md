# Dudas abiertas

Marcad cada una al resolverla y escribid la respuesta debajo.

## Para el tutor (antes de comprar)

- [ ] ¿Aceptan la expendedora ampliada (monedas reales, motores, OLED, carcasa) como trabajo de dificultad alta?
- [ ] ¿Podemos sacar la Nexys del laboratorio, o al menos montarla en la carcasa el día de la defensa?
- [ ] ¿Se puede conectar hardware externo a los Pmod con una fuente de 5 V propia?
- [ ] ¿Cuenta como "entradas y salidas manuales" usar pulsadores externos y los 7 segmentos de la placa vistos por una ventana?
- [ ] El enunciado fija el precio en 1 €. ¿Podemos tener varios productos con precios distintos?
- [ ] ¿Fecha y lugar de la defensa en enero? ¿Hay enchufe para la fuente de los motores?
- [ ] ¿Cuántos turnos de laboratorio podemos reservar por semana?

## Para el equipo

- [ ] ¿Quién hace de arquitecto, programador y responsable de calidad?
- [x] ¿Tenemos impresora 3D? ¿Qué tamaño de cama tiene?
  Bambu Lab A1, cama 256 × 256 mm, PLA. Las paredes de 60 × 40 cm se imprimen por trozos.
- [ ] ¿Qué presupuesto máximo tenemos entre los tres?
- [ ] ¿Qué producto vamos a vender? (fija el tamaño de la espiral; mejor algo pequeño y regular, como caramelos en caja o chicles)
- [x] ¿Cuántos productos: 2 o 3?
  4 productos: 2 estantes con 2 productos cada uno.
- [x] ¿Qué programa de CAD usamos: Fusion 360 u Onshape?
  Fusion 360 (licencia educativa), con scripts en cad/.
- [x] ¿Quién crea el repositorio de GitHub y con qué nombre? Ian, `SED_y_entos_noH2O_G23`, compartido con el Snake (2026-11-10).
- [x] ¿Rampa de monedas propia (más nota, más riesgo) o directamente el validador CH-926?
  Rampa propia con 7 barreras IR.

## Decisiones tomadas

| Fecha | Decisión | Motivo |
| --- | --- | --- |
| 2026-11-07 | Diseño inicial: FSM de Moore de 9 estados, dispensar antes de cobrar | Así "devolver todo" es real y un atasco no se queda con el dinero |
| 2026-11-11 | Reconocer monedas con rampa de barreras IR (opción A) | Más VHDL propio; CH-926 queda como plan B |
| 2026-11-11 | Aceptar también el 5c | No cambia los sensores, solo la tabla del detector |
| 2026-11-11 | Máquina de unos 60 × 40 × 40 cm | Tamaño de la maqueta |
| 2026-11-11 | Depósito de garantía (escrow) entre el cubilete y la hucha, con su propio SG90 | Al cancelar o resetear se devuelve el dinero; a la hucha solo va al completar la compra |
| 2026-11-11 | Cambio: el sobrante queda como saldo para la siguiente compra; cancelar devuelve todo el depósito | La máquina no tiene dispensador de cambio |
| 2026-11-11 | Salida de producto con empujador o trampilla movidos por SG90 (4) | Hay 6 SG90: 2 para monedas y 4 para productos; sin compras y 1 pin por producto |
| 2026-11-11 | Pantalla LCD externa en el frontal; la Nexys va en la base con el USB hacia fuera | La placa queda oculta y se programa sin abrir |
| 2026-11-11 | Carcasa: paredes laterales y techo rígidos; frontal y trasera en guías, extraíbles | Acceso fácil a productos (delante) y cableado (detrás) |
| 2026-11-11 | Sin sensor de caída de producto | Simplificar; se puede añadir después |
| 2026-11-11 | Electrónica: primero en protoboard, después en placa de prototipos soldada | Probar cada bloque antes de soldar |
| 2026-11-11 | Precios y cantidades máximas fijados en el bitstream; no se guarda el saldo al apagar | Plug and play |
| 2026-11-11 | Lógica: producto agotado, tiempo de espera de 30 s, detección de atasco y antirrebotes; sonido más adelante | Robustez en la demo |

### Decisión 2026-11-11 (noche): saldo y depósito
- Se rechaza cualquier moneda que haga que el saldo supere el precio más caro (**2,80 €**). Saldo máximo = 2,80 €.
- «Cancelar» devuelve solo las monedas que siguen en el depósito C. El saldo que sobra tras una compra se puede gastar, pero no se devuelve.
- Peor caso para el depósito: 2,80 € en monedas de 5 c = 56 monedas. Decisión (Ian, 12-11): C es exactamente el mismo cubilete que B (40 de alto), así que el depósito admite como máximo **10 monedas**; la FSM rechaza (devuelve) la moneda 11.

### Decisión 2026-11-12: máquina completa (bocetos en cad/maquina/bocetos_v1.png)
- Medidas aprox.: 330 ancho × 330 fondo × 420 alto (+ Nexys encima), fijadas por Ian el 2026-11-12 (bocetos_v2); el alto lo fija la pila carril → B → C → cajones. Se pueden ampliar si hace falta.
- Ancho = columna de monedas (110: cubiletes + servo + cable, numpad, LCD) + 2 productos (~205).
- Selección con numpad genérico 3×4 por número de producto + botón cancelar (JB: 8 pines; total 27 de 32).
- Productos: ventana para metacrilato opcional; salida a un cajón apoyado en el suelo. Hucha por la trasera.
- Nexys al aire sobre el techo, puertos hacia atrás, con espacio para placas hijas (la placa no es nuestra: fácil de sacar).
- Cajones a ras de la cara, con muesca para el dedo, sin bisagras ni imanes.
- Carcasa: impresa, o madera si las piezas son simples.
