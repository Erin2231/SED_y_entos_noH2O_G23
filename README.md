# SED 2026-27 · Grupo 23

> [!IMPORTANT]
> ## 📌 Antes de tocar nada: lee la [GUÍA GIT](GUIA_GIT.md)
> Cómo descargar, crear tu rama, hacer commit, subir y abrir el pull request, **comando a comando**.
> Nadie sube directo a `main`: todo va por rama + pull request + revisión de un compañero.
>
> 1. [GUIA_GIT.md](GUIA_GIT.md): el flujo de trabajo paso a paso
> 2. [requirements.md](requirements.md): versiones exactas de Vivado, CubeIDE y Fusion 360
> 3. [docs/configuracion.md](docs/configuracion.md): configurar Git, VS Code, Vivado y CubeIDE
> 4. [CONTRIBUTING.md](CONTRIBUTING.md): normas de ramas, commits y PR

Trabajos de **Sistemas Electrónicos Digitales** (UPM ETSIDI), curso 2026-2027.
Los dos montajes van dentro de una maqueta impresa en 3D.

| Trabajo | Placa | Carpeta |
| --- | --- | --- |
| Máquina expendedora en VHDL | Digilent Nexys 4 DDR / Nexys A7 (Artix-7) | [`expendedora-fpga/`](expendedora-fpga/) |
| Mini arcade Snake en C | STM32F4 Discovery | [`snake-arcade/`](snake-arcade/) |

## Estructura

```
.
├── expendedora-fpga/      Trabajo FPGA (Vivado)
│   ├── src/               Un .vhd por entidad, incluido top.vhd
│   ├── tb/                Testbenches *_tb.vhd y sus .wcfg
│   ├── constraints/       Fichero .xdc
│   ├── ip/                IP de Vivado (solo el .xci)
│   ├── vivado/            Proyecto .xpr (enlaza las fuentes de src/)
│   ├── scripts/           Tcl para recrear el proyecto
│   ├── hardware/          Esquemas, pines, fotos
│   ├── cad/               Carcasa: fuente/, step/, stl/
│   └── docs/              Materiales, dudas, diagramas
├── snake-arcade/          Trabajo microcontroladores (STM32CubeIDE)
│   ├── firmware/          Proyecto STM32CubeIDE (Core/, Drivers/, .ioc)
│   ├── lib/               Bibliotecas propias (matriz, LCD, RTC, joystick...)
│   ├── tests/             Pruebas en PC de la lógica del juego
│   ├── hardware/          Esquema, shield, lista de materiales
│   ├── cad/               Carcasa: fuente/, step/, stl/, planos/
│   └── docs/              Diagramas y dudas
├── docs/                  Común: actas de reunión y memoria final
└── .github/               Plantillas de PR e issues
```

## Empezar

```bash
git clone https://github.com/Erin2231/SED_y_entos_noH2O_G23.git
cd SED_y_entos_noH2O_G23
```

Primero configura tus herramientas con **[docs/configuracion.md](docs/configuracion.md)**.
El día a día con Git, comando a comando: **[GUIA_GIT.md](GUIA_GIT.md)**.
Antes de tu primer cambio lee **[CONTRIBUTING.md](CONTRIBUTING.md)**: cómo nombrar
ramas, cómo escribir commits y cómo abrir un pull request.

Herramientas y versiones exactas: **[requirements.md](requirements.md)**
(Vivado 2026.1, STM32CubeIDE 2.2.0 con FW_F4 V1.28.3, Fusion 360).

## Equipo

| Persona | GitHub | Expendedora | Snake |
| --- | --- | --- | --- |
| Ian | @Erin2231 | _por decidir_ | _por decidir_ |
| _compañero 2_ | _@usuario_ | _por decidir_ | _por decidir_ |
| _compañero 3_ | _@usuario_ | _por decidir_ | _por decidir_ |
