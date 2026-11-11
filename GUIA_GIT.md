# Guía Git: del cambio en tu PC a `main`

> **Obligatorio para los tres.** Incluye cómo usar el **tablero Kanban** (paso 2 y [reglas del tablero](#cómo-usamos-el-tablero)). Si dudas en cualquier paso, vuelve aquí antes de improvisar con Git.
En Windows usa **Git Bash**. Cambia los ejemplos (`snake/feat-lcd`, rutas, mensajes) por lo tuyo.

```mermaid
flowchart TD
  A["0 · Solo la primera vez: configurar Git y clonar"] --> B["1 · git switch main · git pull"]
  B --> T["2 · Tablero: coger o crear la tarea, asignártela y moverla a In Progress"]
  T --> C["3 · git switch -c snake/feat-lcd"]
  C --> D["4 · Crear, editar, borrar archivos"]
  D --> E["5 · git status · git diff"]
  E --> F["6 · git add · git commit"]
  F -->|sigo trabajando| D
  F --> G["7 · git push"]
  G --> H["8 · Pull request con Closes #n · tarjeta a Revisión"]
  H --> I{"9 · Revisa un compañero"}
  I -->|pide cambios| D
  I -->|aprueba| J["10 · Merge pull request"]
  J --> K(["Confirmado en main · tarjeta a Done sola"])
  K --> L["11 · Volver a main y borrar la rama"]
  L --> B
```

## 0. Solo la primera vez

Acepta la invitación de colaborador (correo o https://github.com/Erin2231/SED_y_entos_noH2O_G23/invitations).

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email_de_github"   # debe ser un email de tu cuenta de GitHub
git config --global init.defaultBranch main
git config --global fetch.prune true
git config --global pull.rebase false
git config --global core.autocrlf true

mkdir -p /c/proyectos && cd /c/proyectos               # fuera de OneDrive
git clone https://github.com/Erin2231/SED_y_entos_noH2O_G23.git
cd SED_y_entos_noH2O_G23
```

El primer `git push` abre una ventana para iniciar sesión en GitHub: *Sign in with your browser*.

## 1. Al empezar cada sesión (descargar lo último)

```bash
cd /c/proyectos/SED_y_entos_noH2O_G23
git switch main
git pull
```

## 2. Coger la tarea en el tablero (Kanban)

Toda tarea vive en el tablero del repo (pestaña **Projects** → *SED G23*). Antes de escribir una línea:

1. Busca la tarea en **Todo**. Si no existe, créala: botón **New issue** con la plantilla *Tarea*,
   etiqueta (`fpga`, `snake`, `cad`, `docs`). Aparece sola en el tablero.
2. Ábrela y en **Assignees** ponte a ti. Una tarea, una persona.
3. Arrastra la tarjeta a **In Progress**.
4. Apunta su número (por ejemplo `#12`): lo usarás en el pull request.

## 3. Crear tu rama

```bash
git switch -c snake/feat-lcd            # nueva
git switch snake/feat-lcd && git merge main   # retomar una existente
git fetch && git switch fpga/feat-fsm-monedas # probar la rama de un compañero
```

## 4. Trabajar

Guarda los archivos en su carpeta. Vivado: sin "Copy sources into project". CubeIDE: código entre
`USER CODE BEGIN/END`. Fusion: exporta `.f3d`, `.step` y `.stl` a `cad/fuente|step|stl`.

```bash
git rm ruta/archivo_viejo.vhd
git mv ruta/nombre_viejo.c ruta/nombre_nuevo.c
```

## 5. Revisar

```bash
git status
git diff
```

## 6. Guardar un commit

```bash
git add snake-arcade/lib/lcd_i2c     # o git add -A
git commit -m "snake: inicializa la LCD por I2C"
```

## 7. Subir

```bash
git push -u origin snake/feat-lcd    # primera vez
git push                             # siguientes
```

## 8. Pull request (GitHub web)

*Compare & pull request* → rellenar plantilla → en la descripción escribe **`Closes #12`** (el número de tu tarea)
→ *Reviewers*: un compañero → *Create pull request*.

En el tablero, arrastra tu tarjeta a **Revisión**: así el compañero sabe que le toca.

## 9. Revisión

Revisor: `git fetch && git switch snake/feat-lcd && git pull`, prueba, y en el PR
*Files changed → Review changes → Approve → Submit review*.
Si piden cambios: pasos 5 a 7 en la misma rama. El PR y la tarjeta se actualizan solos.

## 10. Fusionar

*Merge pull request → Confirm merge → Delete branch*. Ya está confirmado en `main`, el issue se cierra
(gracias al `Closes #12`) y la tarjeta pasa sola a **Done**.

## 11. Limpiar

```bash
git switch main
git pull
git branch -d snake/feat-lcd
git log --oneline -5
```

## Cómo usamos el tablero

| Columna | Qué significa | Quién la mueve |
| --- | --- | --- |
| **Todo** | Tareas pendientes, sin empezar | Entran solas al crear el issue |
| **In Progress** | Alguien está con ella (mira *Assignees*) | Tú, al empezar (paso 2) |
| **Revisión** | Hay un PR esperando revisión | Tú, al abrir el PR (paso 8) |
| **Done** | Fusionada en `main` | Sola, al fusionar el PR |

Reglas:

- **Nada sin tarjeta.** Si vas a trabajar en algo, que esté en el tablero y asignado a ti.
- **Máximo 2 tarjetas en In Progress por persona.** Termina antes de empezar otra.
- **Revisa el tablero al empezar cada sesión** (paso 1): si hay algo en *Revisión* que no es tuyo, revísalo primero.
- Una tarea grande (por ejemplo "driver de la matriz") se parte en issues pequeños de 1-3 días.

## Problemas frecuentes

| Problema | Solución |
| --- | --- |
| Conflicto | Edita el archivo (VS Code: *Accept current/incoming/both*), `git add archivo`, `git commit`, `git push`. En `.xpr`, `.ioc`, `.f3d` elegid una versión entera. |
| Deshacer cambios no guardados | `git restore archivo` · sacar del add: `git restore --staged archivo` |
| `push` *rejected* | `git pull` y `git push` |
| Commits en `main` sin querer | `git switch -c rama-nueva` · `git switch main` · `git reset --hard origin/main` · `git switch rama-nueva` |
