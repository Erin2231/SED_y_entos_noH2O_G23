# Bibliotecas propias

Un módulo por carpeta, con su `.c`, su `.h` y un README de 5 líneas (qué hace, pines, ejemplo).

| Módulo | Qué hace | Periférico |
| --- | --- | --- |
| `ws2812b/` | Matriz LED RGB 16x16 | TIM1 PWM + DMA |
| `lcd_i2c/` | LCD 20x4 HD44780 con PCF8574 | I2C1 |
| `ds3231/` | Reloj RTC y EEPROM de récords | I2C1 |
| `joystick/` | Joystick KY-023 | ADC1 + DMA |
| `buzzer/` | Efectos y melodías | TIM3 PWM |
| `snake_juego/` | Lógica del juego, **sin HAL** (se prueba en PC desde `../tests`) | — |

Si usáis código de terceros, ponedlo en `lib/terceros/<nombre>/` con su licencia y citadlo
en la memoria.
