# Contexto del proyecto (traspaso)

Resumen para quien se incorpora a los trabajos de SED del grupo 23. Recoge el objetivo, en qué punto
está cada cosa, qué está decidido, qué falta por decidir y dónde está cada fichero. Se puede leer tal
cual o dárselo como contexto a un asistente.

Estado a **13-11-2026**. Si algo de aquí contradice a un fichero más nuevo, manda el fichero.

> **Aviso: borradores.** Las listas de materiales (`expendedora-fpga/docs/materiales.md`,
> `snake-arcade/hardware/bom.md`, `snake-arcade/hardware/lista_materiales.txt`) y las cotas de la
> carcasa del Snake (`snake-arcade/cad/planos/maquina_cotas_v0.2`) son **ejemplos muy iniciales** y
> van a cambiar. No construyáis encima sin revisarlas. Lo mismo para cualquier cota que no esté en
> la lista de "Decisiones confirmadas".

---

## 1. Objetivo

Sistemas Electrónicos Digitales, UPM ETSIDI, curso 2026-27. Grupo de 3. Dos trabajos, defensa en
**enero de 2027** (fecha por fijar). La documentación en GitHub y los commits de cada uno puntúan.

| Trabajo | Placa | Qué es |
| --- | --- | --- |
| Expendedora | Nexys 4 DDR / Nexys A7 (VHDL, Vivado) | Máquina expendedora real (enunciado 3 de VHDL ampliado): reconoce monedas reales, dispensa 4 productos, devuelve el dinero. Maqueta de 330 × 330 × 420 mm |
| Snake | STM32F4 Discovery (C, STM32CubeIDE) | Mini arcade de Snake con matriz LED 16×16 y LCD 20×4 para menús y récords |

Las dos van dentro de una maqueta impresa en 3D (Bambu Lab A1, cama 256 × 256, PLA) que esconde la
placa y los cables. CAD en **Fusion 360**.

## 2. Estado actual

| Bloque | Estado |
| --- | --- |
| Repositorio | Creado, estructura y normas en `main`. Faltan los usuarios de GitHub de los compañeros |
| Expendedora: diseño del sistema | FSM y bloques definidos (`expendedora-fpga/docs/img/bloques/`). **VHDL sin empezar** (`src/` vacío) |
| Expendedora: mecánica de monedas | Modelado y en prototipo: carril A, cubilete B, trampilla, acople del servo, crestas y canal. El cubilete se está reimprimiendo (la primera impresión falló) |
| Expendedora: carcasa | Bocetos v2 y plano del corte 1 (sección de la columna de monedas) a escala 1:2 en A3 |
| Expendedora: electrónica | Sin montar. Faltan LED IR y fototransistores (no hay en el inventario) |
| Snake | Solo diseño (BOM borrador, cotas v0.2 borrador, dudas). Sin firmware ni CAD |
| Tutor | **No ha validado todavía ninguno de los dos temas** |

## 3. Decisiones confirmadas

### Expendedora: funcionamiento

- FSM de Moore de 9 estados; se **dispensa antes de cobrar**, así un atasco no se queda con el dinero.
- Monedas: rampa propia con **7 barreras IR** (P1, B1-B5, P2) que miden el diámetro (opción A). El
  validador CH-926 queda como plan B. Se aceptan 5c, 10c, 20c, 50c y 1 €; 1c y 2c se rechazan por
  sensor, el 2 € no cabe por la ranura (25 mm).
- Carril de 150 mm, pendiente 10°, inclinación lateral 12°. Código termómetro en `detector_monedas`.
- Depósito de garantía **C** (escrow) entre el cubilete B y la hucha, con su propio SG90. Cancelar o
  Reset devuelven lo que hay en C. A la hucha solo va al completar la compra.
- Precio máximo **2,80 €**: se rechaza la moneda que haría pasar el saldo de 2,80. El saldo sobrante
  tras comprar se puede gastar pero no se devuelve. C admite como máximo **10 monedas**; la 11ª se devuelve.
- Trampillas con SG90 de 3 posiciones (retener / hucha / devolución) sobre una cresta en Λ.
- 4 productos (2 estantes × 2), salida con SG90 (empujador o trampilla). Sin sensor de caída.
- Selección con **teclado de membrana 3×4** + pulsador de cancelar (táctil 6×6 con embellecedor impreso).
- Pantalla **LCD 16×2 HD44780**. Fuente única de 5 V (3-4 A).
- Precios fijos en el bitstream; no se guarda el saldo al apagar.

### Expendedora: mecánica y carcasa

- Medidas de la máquina: **330 ancho × 330 fondo × 420 alto** (fijadas por Ian el 12-11).
- Nexys **al aire sobre el techo**, puertos hacia atrás (ya no va en la base). La placa es del
  laboratorio: tiene que poder sacarse fácil.
- Cajones de devolución, productos y hucha a ras, sin bisagras ni imanes. Hucha por detrás.
  Devolución y hucha iguales: 75 fondo × 57 alto × 104 ancho.
- Ventana de productos con metacrilato opcional. Carcasa impresa, o tablero DM si las piezas son simples.
- Carril A: placa frontal, tapa A-T desmontable, portasensores A-S regulables (×5), pared de
  fototransistores A-F separada (por el voladizo). LEDs en el lado de la pared, fototransistores
  hacia el interior. Todos los tornillos pequeños M2 × 6 autorroscantes.
- Cubilete B sin fondo con soporte SG90; **C es exactamente la misma pieza que B**.
- Trampilla en dos mitades (B-TP + B-TS, junta a 45°, 2 postizos) y acople B-AC atornillado al
  brazo del servo. SERVO_GAP = 16. **No tocar** cubilete, mitades ni postizos: aprobado así.
- Crestas en U (CR-1 bajo B, CR-2 bajo C) y caja del canal de no válidas (CR-3, 3 lados; el 4º es la
  pared de la máquina). 46 de ancho, paredes de la U de 15, rampas a 30°, fijadas con lengüetas
  iguales a las del cubilete (M3 + tuerca a la pared lateral).
- 20 mm de paso entre el fondo de cada cubilete y el vértice de su cresta.

### Snake

- Sin sensor de moneda: la partida empieza con START.
- LCD de texto 20×4 por I2C (PCF8574) en vez de OLED, por sencillez.
- Propuesta (sin cerrar): matriz WS2812B 16×16, DS3231 para récords, joystick KY-023, 2 botones,
  zumbador pasivo, solo 5 V externos.

### Repositorio y forma de trabajar

- Un único repo para los dos trabajos (este). Nada directo a `main`: rama + PR + 1 revisión,
  fusionar con *merge commit* (no squash), porque cuentan los commits de cada uno.
- Ramas `<trabajo>/<tipo>-<tema>`, por ejemplo `fpga/feat-detector-monedas`. Ver `CONTRIBUTING.md`
  y `GUIA_GIT.md`.
- Versiones exactas en `requirements.md` (Vivado 2026.1, STM32CubeIDE 2.2.0, FW_F4 V1.28.3).
- Commits y PRs **solo a nombre del grupo**: sin coautores externos ni firmas de herramientas.
- Primero se usa el material del inventario (`docs/inventario/`). La lista de compra está vacía a
  propósito: no se añade nada sin acordarlo.
- Documentar cada avance: README del módulo, decisión en `dudas.md`, esquema o pines en `hardware/`,
  foto o captura, y BOM o cotas actualizados.

## 4. Dudas abiertas

**Para el tutor** (ver `expendedora-fpga/docs/dudas.md` y `snake-arcade/docs/dudas.md`): aprobación
de los dos temas, sacar la Nexys del laboratorio, hardware externo con fuente de 5 V propia,
productos con precios distintos (el enunciado dice 1 €), fecha y lugar de la defensa, código de
terceros en el Snake.

**Del diseño:**

- Reparto de roles en los dos trabajos.
- Presupuesto del grupo y qué producto se vende (fija el tamaño del dispensador).
- Comprar LED IR + fototransistores (propuesta: Vishay VSLB3940 + TEFT4300, ver
  `expendedora-fpga/cad/maquina/corte1/compras.md`) y tornillos M2 × 6.
- Medir las monedas con calibre y corregir las alturas de las barreras.
- "Pared izquierda" del carril = la izquierda mirando la máquina de frente (supuesto sin confirmar;
  los STEP son para esa pared y los scripts de Fusion tienen `PARED = "derecha"` para la simétrica).
- Alto real del táctil del pulsador de cancelar (`H_PULS` en `pulsador.py`, 5 mm por defecto).
- Por dónde pasa el cable plano del teclado (se quitó la ranura 20 × 3 que había).
- CR-3: comprobar que el script de Fusion lo crea como **un solo cuerpo** con los 4 agujeros (se
  corrigió el 13-11 y falta confirmarlo en Fusion).
- Snake: qué Discovery es (F411E o F407G), WS2812B o MAX7219, dónde se compra.

**Ficheros desactualizados (cuidado):**

- `expendedora-fpga/cad/rampa-monedas/planos/planos_carril_cubilete.pdf` es del 11-11 y no recoge
  A-F, la trampilla en dos mitades ni la ranura corregida. Los cambios están en el README de esa carpeta;
  manda `modelo.py`.
- `expendedora-fpga/docs/rampa-monedas.md` y `monedas.md` hablan aún de una máquina de 60 × 40 × 40 y
  de la Nexys en la base: eso ya no vale (ver medidas arriba).
- `expendedora-fpga/docs/materiales.md` propone OLED, 28BYJ-48 y 4 botones: sustituido por LCD,
  SG90 y teclado 3×4. Es borrador.
- `plano_corte1_v1.*` y `render_v1.py` son la versión anterior del plano, se guardan solo como historial.

## 5. Índice de ficheros

### Documentos principales

| Fichero | Qué es |
| --- | --- |
| `README.md`, `GUIA_GIT.md`, `CONTRIBUTING.md` | Portada del repo y normas de trabajo |
| `requirements.md`, `docs/configuracion.md` | Versiones de programas y configuración de Git, VS Code, Vivado, CubeIDE |
| `docs/inventario/inventario.md` | Material que ya tenemos (borrador sacado de una foto) |
| `docs/inventario/lista_compra.md` | Vacía a propósito |
| `expendedora-fpga/README.md` | Portada del trabajo FPGA |
| `expendedora-fpga/docs/dudas.md` | Dudas abiertas y **tabla de decisiones** con fecha y motivo |
| `expendedora-fpga/docs/monedas.md` | Por qué se mide el diámetro, opciones A/B, tabla de barreras |
| `expendedora-fpga/docs/rampa-monedas.md` | Rampa de monedas: alturas, ángulos, compuerta, calibración, VHDL del detector |
| `expendedora-fpga/docs/materiales.md` | Lista de materiales (**borrador**) |
| `snake-arcade/README.md`, `snake-arcade/docs/dudas.md` | Portada y dudas del Snake |
| `snake-arcade/hardware/bom.md`, `lista_materiales.txt` | BOM del Snake (**borrador**) |

### Croquis y planos

| Fichero | Qué es |
| --- | --- |
| `expendedora-fpga/cad/maquina/bocetos_v2.png` / `.svg` | Bocetos de la máquina completa (versión vigente) |
| `expendedora-fpga/cad/maquina/bocetos_v1.png` / `.svg` | Bocetos anteriores |
| `expendedora-fpga/cad/maquina/corte1/plano_corte1.pdf` | **Plano principal**: corte 1 (columna de monedas), 1:2 en A3, con tablas de piezas, puntos y taladros |
| `expendedora-fpga/cad/maquina/corte1/compras.md` | Piezas del corte 1 que habría que comprar, con referencias (no es la lista de compra) |
| `expendedora-fpga/cad/maquina/crestas/crestas.pdf` | Hoja con cotas de CR-1, CR-2 y CR-3 |
| `expendedora-fpga/cad/maquina/pulsador/esquema_pulsador.pdf` | Montaje del pulsador de cancelar |
| `expendedora-fpga/cad/rampa-monedas/planos/planos_carril_cubilete.pdf` | 7 hojas A4 del carril A y cubilete B (versión 11-11, ver aviso arriba) |
| `expendedora-fpga/cad/rampa-monedas/planos/trampilla_montaje.png` | Montaje de la trampilla en dos mitades |
| `expendedora-fpga/cad/rampa-monedas/planos/corte_B3_piezas_separadas.png` | Corte con la pared A-F separada |
| `expendedora-fpga/docs/img/bloques/` | Diagramas de bloques de hardware y VHDL |
| `expendedora-fpga/docs/img/monedas/`, `docs/img/cad/` | Figuras de la rampa, ángulos, compuerta y montaje de sensores |
| `snake-arcade/cad/planos/maquina_cotas_v0.2.png` | Cotas de la carcasa del Snake (**borrador**) |

### Piezas 3D (STEP para Fusion, STL para Bambu Studio)

| Carpeta | Piezas |
| --- | --- |
| `expendedora-fpga/cad/rampa-monedas/step/` y `stl/` | A carril, A-F pared de fototransistores, A-T tapa, A-S portasensor, B cubilete (también vale para C), B-TP y B-TS trampilla, B-PZ postizo, B-AC acople del servo |
| `expendedora-fpga/cad/maquina/crestas/step/` y `stl/` | CR-1 cresta 1, CR-2 cresta 2, CR-3 caja del canal |
| `expendedora-fpga/cad/maquina/pulsador/step/` y `stl/` | PC-E embellecedor, PC-S soporte |

Orientación de impresión y montaje: en el README de cada carpeta.

### Scripts de Fusion 360

| Carpeta | Qué hace |
| --- | --- |
| `expendedora-fpga/cad/rampa-monedas/fusion/MonedasSED/` | Crea A, A-F, A-T, A-S, B y la trampilla en un diseño nuevo. Probado en Fusion |
| `expendedora-fpga/cad/maquina/crestas/fusion/CrestasSED/` | Crea CR-1, CR-2 y CR-3 en su sitio de la máquina |

Uso: Utilidades › Complementos › Scripts y complementos › "+" › elegir la carpeta (con su
`.manifest`) › Ejecutar. Las cotas están en el bloque PARÁMETROS al principio del `.py`.

### Modelos paramétricos y comprobaciones (Python + CadQuery)

| Fichero | Qué hace |
| --- | --- |
| `expendedora-fpga/cad/rampa-monedas/modelo.py` | **Modelo de referencia** del carril y el cubilete: cambiar cotas aquí. `python3 modelo.py out` exporta |
| `.../rampa-monedas/comprobar.py`, `chk_trampilla.py` | Encajes y choques de la trampilla a 0°, ±20° y ±40° |
| `.../rampa-monedas/planos.py`, `vistas.py`, `pdf.js` | Regeneran las hojas SVG y el PDF de A y B |
| `.../rampa-monedas/fusion/probar_geometria.py` | Compara el script de Fusion con `modelo.py` (diferencia 0) |
| `expendedora-fpga/cad/maquina/crestas/crestas.py`, `comprobar.py`, `hoja.py` | Crestas y canal, choques con todo el corte 1, hoja con cotas |
| `expendedora-fpga/cad/maquina/pulsador/pulsador.py`, `esquema.py` | Pulsador de cancelar y su esquema |
| `expendedora-fpga/cad/maquina/corte1/render.py`, `plano1.py` | Generan el plano del corte 1 |
| `expendedora-fpga/cad/maquina/bocetos_gen.py` | Genera los bocetos |
| `expendedora-fpga/docs/img/bloques/gen.py` | Genera los diagramas de bloques |

## 6. Próximos pasos razonables

1. Llevar los dos temas al tutor y apuntar las respuestas en los `dudas.md`.
2. Repartir roles y anotarlos en los README.
3. Expendedora: reimprimir B, probar una barrera IR con un 20c y un 1 €, medir monedas.
4. Expendedora: empezar el VHDL por `detector_monedas` y `pwm_servo`, cada uno con su testbench.
5. Revisar las listas de materiales borrador y decidir qué se compra.
6. Snake: confirmar la Discovery y crear el proyecto de CubeIDE.
