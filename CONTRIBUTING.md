# Cómo trabajamos en este repositorio

> [!IMPORTANT]
> Los comandos exactos de cada paso están en la **[GUÍA GIT](GUIA_GIT.md)**. Léela antes de tu primer commit.

En la nota cuentan los **commits continuos de los tres**. Por eso cada uno sube
su trabajo con su propia cuenta, poco a poco, y nunca se aplastan los commits
de otro.

## 1. Ramas

- `main` es la versión buena: siempre compila y sintetiza. **Nadie sube directo a `main`.**
- Cada tarea va en su propia rama, que sale de `main` actualizado:

```
<trabajo>/<tipo>-<tema-corto>
```

| Trabajo | Prefijo | Ejemplos |
| --- | --- | --- |
| Expendedora | `fpga/` | `fpga/feat-fsm-monedas`, `fpga/tb-contador`, `fpga/fix-debounce` |
| Snake | `snake/` | `snake/feat-driver-ws2812b`, `snake/fix-lcd-i2c` |
| Carcasa | `cad/` | `cad/feat-frontal-snake` |
| Documentación | `docs/` | `docs/memoria-intro` |

Tipos: `feat` (algo nuevo), `fix` (arreglo), `tb` (testbench o test), `refactor`, `docs`.

## 2. Día a día

```bash
git switch main
git pull                          # trae lo último
git switch -c snake/feat-joystick # rama nueva
# ... trabajas ...
git add snake-arcade/lib/joystick
git commit -m "snake: lee el joystick por ADC con DMA"
git push -u origin snake/feat-joystick
```

Después abre el **pull request** en GitHub (sale un botón amarillo "Compare & pull request").

Si `main` ha avanzado mientras trabajabas:

```bash
git switch main && git pull
git switch snake/feat-joystick
git merge main                    # resuelve conflictos si los hay
git push
```

## 3. Commits

- Pequeños y frecuentes: mejor 5 commits de una tarde que 1 enorme el día antes de entregar.
- Mensaje en presente, empezando por el trabajo:
  - `fpga: añade el detector de flancos de las monedas`
  - `snake: corrige el parpadeo de la matriz`
  - `cad: primera versión del frontal`
  - `docs: acta de la reunión del 12/11`
- Antes de hacer `commit`, mira `git status`: no subas carpetas `Debug/`, `.runs/`, `.Xil/` ni G-code
  (el `.gitignore` ya las tapa, pero comprueba).

## 4. Pull requests

1. Rellena la plantilla (qué cambia, cómo lo has probado).
2. Pide revisión a **al menos un compañero**. El revisor prueba que sintetiza / compila.
3. Para fusionar usa **"Create a merge commit"** (no "Squash"), así quedan todos los commits con su autor.
4. Borra la rama después de fusionar (GitHub ofrece el botón).

## 5. Reglas por trabajo

### Expendedora (Vivado)

- Las fuentes viven en `src/`, `tb/` y `constraints/`. Al añadirlas al proyecto, **desmarca
  "Copy sources into project"**: así Vivado las enlaza y no crea copias dentro de `vivado/`.
- Un fichero por entidad, mismo nombre que la entidad (`fsm_expendedora.vhd`).
- Cada entidad con su testbench en `tb/` (`fsm_expendedora_tb.vhd`).
- Las IP (relojes, etc.) se guardan en `ip/` y solo se sube el `.xci`.
- No toquéis el `.xpr` dos personas a la vez: avisad en el grupo antes de cambiar ajustes del proyecto.
- Ver [`expendedora-fpga/vivado/README.md`](expendedora-fpga/vivado/README.md).

### Snake (STM32CubeIDE)

- El proyecto está en `snake-arcade/firmware/`. Se sube el `.ioc` y también `Drivers/` (HAL y CMSIS)
  para que compile al clonar sin regenerar nada.
- El código propio en el `main.c` va **siempre entre** `/* USER CODE BEGIN */` y `/* USER CODE END */`;
  lo de fuera se borra al regenerar desde el `.ioc`.
- Solo una persona cambia el `.ioc` cada vez (pines, relojes, periféricos). Avisad antes.
- Los drivers propios van en `snake-arcade/lib/<modulo>/` con su `.c`, `.h` y un README corto.
- Ver [`snake-arcade/firmware/README.md`](snake-arcade/firmware/README.md).

### CAD

- Cada pieza en tres formatos: nativo en `cad/fuente/`, `cad/step/` y `cad/stl/`.
- Nombre: `<pieza>_v<versión>.<ext>`, por ejemplo `frontal_v1.step`.
- El programa de CAD es Fusion 360 (ver `requirements.md`).

## 6. Issues y tablero

Usad los issues de GitHub como lista de tareas: una tarea, un issue, asignado a quien la hace.
Todas van al tablero Kanban (pestaña Projects). Reglas en la [GUÍA GIT](GUIA_GIT.md#cómo-usamos-el-tablero).
En el PR escribid `Closes #12` para cerrarlo al fusionar.
