---
name: sed-g23
description: Normas del repo SED Grupo 23 (expendedora VHDL y Snake STM32). Usar en cualquier tarea de este repo: código, CAD, docs, ramas, commits o PR.
---

# SED Grupo 23: normas de trabajo

Repo: `Erin2231/SED_y_entos_noH2O_G23`. Clon local en Windows: `C:\proyectos\SED_y_entos_noH2O_G23`.
Contexto completo y decisiones: `CONTEXTO.md` (proyecto "trabajoSED") y los `docs/dudas.md` de cada trabajo.
Si algo de esta skill contradice a un fichero más nuevo del repo, manda el fichero.

## Quién hace qué

- Claude prepara y edita ficheros. **Ian hace siempre `git add`, `commit`, `push` y el PR** con su cuenta.
- Cada vez que haya algo listo para subir, dar los comandos exactos para **Git Bash** (no PowerShell), con la rama y el mensaje ya escritos.
- Commits y PR **sin firmas de herramientas ni `Co-Authored-By`**. Cuentan los commits de cada alumno.
- No añadir nada a `docs/inventario/lista_compra.md` sin que el grupo lo acuerde.

## Ramas

`<trabajo>/<tipo>-<tema-corto>`, siempre desde `main` actualizado. Nunca commit directo a `main`.

| Trabajo | Prefijo |
| --- | --- |
| Expendedora | `fpga/` |
| Snake | `snake/` |
| Carcasa | `cad/` |
| Documentación | `docs/` |

Tipos: `feat`, `fix`, `tb`, `refactor`, `docs`, `chore`.

## Commits

- En español, presente, empezando por el trabajo: `fpga: añade el antirrebote del pulsador`.
- Pequeños: un módulo o un cambio con sentido por commit.
- Antes de commit, `git status`: nada de `Debug/`, `.runs/`, `.Xil/`, `.bit` ni G-code.

## Plantilla de comandos para Ian

```bash
cd /c/proyectos/SED_y_entos_noH2O_G23
git switch main
git pull
git switch -c fpga/feat-<tema>
git status
git add <rutas concretas>
git commit -m "fpga: <qué hace>"
git push -u origin fpga/feat-<tema>
```

Después en GitHub: *Compare & pull request*, plantilla rellena con `Closes #n`, un compañero como revisor,
tarjeta a **Revisión**. Fusionar con **Create a merge commit** (nunca squash) y borrar la rama.

## Expendedora (VHDL, Vivado 2026.1, Nexys A7 / Nexys 4 DDR)

- Fuentes en `expendedora-fpga/src/`, testbenches en `tb/`, `.xdc` en `constraints/`, IP en `ip/` (solo `.xci`).
- Un fichero por entidad, mismo nombre que la entidad. Cada entidad con su `<entidad>_tb.vhd`.
- Usar `ieee.numeric_std`. Entradas externas (botones, teclado, sensores) pasan por sincronizador.
- En Vivado, añadir fuentes **sin** "Copy sources into project".
- No tocar el `.xpr` sin avisar al grupo.
- Decisiones fijas: FSM de Moore de 9 estados, dispensa antes de cobrar, precio máximo 2,80 euros,
  máximo 10 monedas en C, teclado 3x4 + pulsador cancelar, LCD 16x2 HD44780, servos SG90.

## Snake (C, STM32CubeIDE 2.2.0, FW_F4 V1.28.3)

- Proyecto en `snake-arcade/firmware/`. Se suben `.ioc` y `Drivers/`.
- Código propio en `main.c` solo entre `/* USER CODE BEGIN */` y `/* USER CODE END */`.
- Drivers propios en `snake-arcade/lib/<modulo>/` con `.c`, `.h` y README corto.
- Si el `.ioc` pide migrar a otra versión del paquete: decir que no.

## CAD (Fusion 360)

- Cada pieza en `cad/fuente/` (`.f3d`), `cad/step/` y `cad/stl/`. Nombre `<pieza>_v<n>.<ext>`.
- **No tocar** cubilete B/C, mitades de trampilla ni postizos: aprobados.
- Las cotas se cambian en el modelo paramétrico (`modelo.py`, `crestas.py`), no a mano en el STEP.

## Documentar cada avance

README del módulo, decisión con fecha en `dudas.md`, pines o esquema en `hardware/`, captura o foto.

## Estilo de código y respuestas

- Código primero; explicación después solo si no es obvia.
- La solución más simple que funcione. Sin abstracciones de un solo uso ni funciones especulativas.
- Leer el fichero antes de modificarlo.
- Revisiones: el fallo, el arreglo y nada más. Si la causa no está clara, decirlo.
- Sin rayas largas, comillas tipográficas ni símbolos decorativos. Código copiable tal cual.

## Antes de la entrega

Rellenar en los README: usuarios de GitHub de los compañeros, reparto de roles y modelo de Discovery.
