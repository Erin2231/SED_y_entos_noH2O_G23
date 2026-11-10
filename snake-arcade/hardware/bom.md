# Lista de materiales (BOM) – Mini arcade Snake

Estado: **borrador v0.2** (2026-11-07: sin sensor de moneda; OLED sustituida por LCD 20x4). Precios aproximados, de memoria, sin consultar tiendas: hay que confirmarlos al comprar.

Total estimado sin la placa Discovery: **≈ 70 €** (≈ 74 € con el Bluetooth opcional).

## Núcleo

| # | Componente | Cant. | Uso | Interfaz / pin propuesto | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|---|
| 1 | STM32F411E-DISCO (o STM32F407G-DISC1) | 1 | Microcontrolador | — | ya disponible | Confirmar modelo |
| 2 | Matriz LED WS2812B 16x16 flexible (160x160 mm, paso 10 mm) | 1 | Pantalla del juego | TIM1_CH1 PWM + DMA, PA8 | 15 | Por comprar |
| 3 | Pantalla LCD 20x4 caracteres (HD44780) con adaptador I2C PCF8574, 5 V, módulo ≈ 98x60 mm | 1 | Menús, configuración y récords | I2C1 0x27, PB6/PB9 | 7 | Por comprar |
| 4 | Joystick analógico KY-023 | 1 | Dirección de la serpiente | ADC1 IN1/IN2 (PA1/PA2), SW en PD3 | 2 | Por comprar |
| 5 | Pulsadores arcade 24 mm | 2 | A = OK/START, B = ATRÁS/PAUSA | EXTI, PD1/PD2 | 4 | Por comprar |
| 6 | Zumbador pasivo 5 V | 1 | Efectos y melodías | TIM3_CH3 PWM, PB0 | 1 | Por comprar |
| 7 | Transistor 2N2222 + resistencia 1 kΩ + diodo 1N4148 | 1 | Etapa del zumbador | — | lote pasivos | Por comprar |

## Sensores extra

| # | Componente | Cant. | Uso | Interfaz / pin propuesto | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|---|
| 8 | LDR 5 mm + resistencia 10 kΩ | 1 | Brillo automático de la matriz | ADC1 IN3, PA3 | lote pasivos | Por comprar |
| 9 | Módulo DS3231 (RTC + EEPROM AT24C32) | 1 | Guardar récords con fecha | I2C1 0x68 / 0x57 | 3 | Por comprar |
| — | Acelerómetro de la Discovery | — | Modo "inclinación" | Ya en la placa | 0 | — |

## Alimentación

| # | Componente | Cant. | Uso | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|
| 10 | Fuente 5 V / 4 A con jack 5,5x2,1 (o disparador USB-C PD a 5 V) | 1 | Alimenta matriz + placa | 8 | Por comprar |
| 11 | Jack DC hembra de panel + interruptor de balancín | 1 | Entrada y encendido | 2 | Por comprar |
| 12 | Portafusibles + fusible 3 A | 1 | Protección | 1 | Por comprar |
| 13 | Condensador electrolítico 1000 µF 10 V | 1 | Junto a la entrada de la matriz | lote pasivos | Por comprar |
| 14 | Resistencia 330 Ω | 1 | Serie en la línea de datos de la matriz | lote pasivos | Por comprar |
| 15 | 74HCT125 (o 74AHCT125) | 1 | Adaptar los datos de 3,3 V a 5 V | lote pasivos | Por comprar |

## Montaje y soldadura

| # | Componente | Cant. | Uso | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|
| 16 | Placa de topos (perfboard) ~ 7x9 cm | 1–2 | Shield que encaja en la Discovery | 2 | Por comprar |
| 17 | Tiras de pines hembra/macho 2,54 mm | lote | Conexión shield–Discovery | 1 | Por comprar |
| 18 | Conectores JST-XH (2, 3, 4 y 5 pines) con cables | lote | Periféricos desmontables | 3 | Por comprar |
| 19 | Cable unifilar/ multifilar 22–24 AWG, termorretráctil | lote | Cableado | — | Comprobar si hay |
| 20 | Lote de pasivos (resistencias, condensadores 100 nF) | lote | Varios | 4 | Por comprar |

## Carcasa

| # | Componente | Cant. | Uso | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|
| 21 | Filamento PLA (negro + color) / PETG | ≈ 500 g | Piezas impresas | 8 | Por comprar |
| 22 | Metacrilato opal 3 mm (≈ 170x170 mm) o PLA blanco fino | 1 | Difusor de la pantalla | 2 | Por comprar |
| 23 | Insertos roscados M3 + tornillos M3 (8–12 mm) + separadores M3 | lote | Cierre y fijación de placas | 5 | Por comprar |
| 24 | Tornillos M3 x 10 | 4 | Fijar la LCD | lote | Por comprar |

## Opcional

| # | Componente | Cant. | Uso | Interfaz | Precio aprox. (€) | Estado |
|---|---|---|---|---|---|---|
| 25 | Módulo Bluetooth HC-05 | 1 | Control desde móvil y descarga de récords | USART6, PC6/PC7 | 4 | Si sobra tiempo |
| 26 | Tira WS2812B corta (≈ 10 LEDs) | 1 | Marquesina iluminada | Encadenada a la matriz | 3 | Si sobra tiempo |
| 27 | Segundo joystick KY-023 | 1 | Modo 2 jugadores | ADC | 2 | Si sobra tiempo |

## Notas

- Los pines son provisionales: hay que cruzarlos con el manual de usuario de la Discovery (UM1842 para F411, UM1472 para F407) antes de soldar.
- La matriz a pleno blanco consumiría unos 15 A. El firmware limitará el brillo (≈ 40/255) para quedar por debajo de ~3 A.
- La LCD va a 5 V con pull-ups del adaptador a 5 V; PB6 y PB9 son tolerantes a 5 V, así que se conecta directa al I2C. Si se usa la F407 hay que comprobar lo mismo.
- Masa común entre fuente, matriz y Discovery.
