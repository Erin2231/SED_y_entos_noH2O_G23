# Configuración de herramientas

Lo que cada uno configura **una vez** para trabajar sin fricciones.

## 1. Git en tu ordenador (los tres)

```bash
git config --global user.name  "Tu Nombre"
git config --global user.email "el-mismo-email-de-tu-cuenta-de-github"
git config --global init.defaultBranch main
git config --global fetch.prune true
git config --global pull.rebase false
```

**Importante:** si el email no coincide con uno de tu cuenta de GitHub, tus commits no aparecen
a tu nombre y no cuentan en la nota. Compruébalo en GitHub → Settings → Emails.

Si no te manejas con la terminal: **GitHub Desktop** hace lo mismo con botones.

## 2. VS Code

Al abrir la carpeta del repo, VS Code ofrece instalar las extensiones recomendadas
(`.vscode/extensions.json`): acepta. La configuración común está en `.vscode/settings.json`
y el formato en `.editorconfig`.

| Extensión | Para qué |
| --- | --- |
| Git Graph / GitLens | Ver ramas y quién cambió cada línea |
| TerosHDL | VHDL: resaltado, errores, diagramas de la FSM |
| C/C++ y STM32 VS Code Extension | Editar y compilar el firmware fuera de CubeIDE |
| EditorConfig | Respeta `.editorconfig` |
| Markdown All in One | Documentación |

## 3. Vivado

- Todos la **misma versión**: 2026.1 (ver `requirements.md`).
- Añadir fuentes **sin** "Copy sources into project" (ver `expendedora-fpga/vivado/README.md`).
- *Tools → Settings → Text Editor*: tabulador = 4 espacios.
- Opcional: *Text Editor → Current Editor → Custom Editor* = VS Code (`code -g [file name]:[line number]`).

## 4. STM32CubeIDE

- Todos la **misma versión**: CubeIDE 2.2.0 y paquete **STM32Cube FW_F4 V1.28.3** (*Help → Manage
  embedded software packages*). Si no, el `.ioc` se reescribe entero al abrirlo.
- El **workspace fuera del repositorio** (p. ej. `Documentos/cubeide-ws`); el proyecto se importa.
- *Window → Preferences → General → Workspace*: *Text file encoding* = UTF-8,
  *New text file line delimiter* = Unix.
- *C/C++ → Code Style → Formatter*: perfil con espacios en lugar de tabuladores.

## 5. CAD

- Usamos **Fusion 360** con licencia educativa. Cread un *Team Hub* común (o un proyecto compartido)
  para que los tres veáis los diseños; el `.f3d` también se sube a `cad/fuente/`.
- Cada versión que se imprima se exporta a STEP y STL y se sube al repo.

## 6. GitHub (lo hace el administrador)

| Dónde | Qué |
| --- | --- |
| Settings → Collaborators | Invitar a los dos compañeros |
| Settings → General → Pull Requests | Dejar solo *Allow merge commits*; activar *Always suggest updating pull request branches* y *Automatically delete head branches* |
| Settings → Rules → Rulesets | Regla para `main`: *Require a pull request* (1 aprobación), *Block force pushes*, *Restrict deletions* |
| Issues → Labels | `fpga`, `snake`, `cad`, `docs`, `bug` |
| Projects | Tablero Kanban (Por hacer / En curso / Revisión / Hecho) enlazado al repo |
| Releases | Bitstream `.bit` y `.elf` de cada versión que se lleva a la defensa |

Si el repo pasa a **privado**, las reglas de rama necesitan GitHub Pro: es gratis con el
**GitHub Student Developer Pack** (education.github.com, con el correo de la UPM).

Cada uno: botón **Watch → All activity** en el repo, para enterarse de PRs y revisiones.
