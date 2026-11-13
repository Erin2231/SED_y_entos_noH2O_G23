"""Esquema de funcionamiento y montaje del pulsador de cancelar -> esquema_pulsador.svg/png"""
import math, cadquery as cq
import pulsador as PZ

def _pts(w):
    out = []
    for e in w.Edges():
        k = 1 if e.geomType() == "LINE" else 24
        out.append([(e.positionAt(i / k).x, e.positionAt(i / k).y) for i in range(k + 1)])
    chain = out.pop(0)
    while out:
        last = chain[-1]; best = None
        for i, seg in enumerate(out):
            for q in (seg, seg[::-1]):
                d = (q[0][0] - last[0]) ** 2 + (q[0][1] - last[1]) ** 2
                if best is None or d < best[0]: best = (d, i, q)
        chain += best[2][1:]; out.pop(best[1])
    return chain
def corte(w, zc=2.25):
    sl = w.val().intersect(cq.Solid.makeBox(100, 100, 0.02, cq.Vector(-50, -50, zc - 0.01)))
    return [[_pts(f.outerWire())] + [_pts(x) for x in f.innerWires()] for f in sl.Faces() if f.normalAt().z < -0.9]

PW, PH = 297.0, 210.0      # A4 apaisado
INK, Q, RED, BLU = "#222", "#666", "#8b1e1e", "#2f5d8a"
o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{PW}mm' height='{PH}mm' viewBox='0 0 {PW} {PH}' font-family='DejaVu Sans, Arial, sans-serif'>",
     "<defs><pattern id='hw' width='2' height='2' patternUnits='userSpaceOnUse' patternTransform='rotate(-45)'><rect width='2' height='2' fill='#ebe7e1'/><line x1='0' y1='0' x2='0' y2='2' stroke='#a39886' stroke-width='0.15'/></pattern>"
     "<pattern id='hp' width='1.4' height='1.4' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='1.4' height='1.4' fill='#d3dae3'/><line x1='0' y1='0' x2='0' y2='1.4' stroke='#5b6b80' stroke-width='0.12'/></pattern>"
     f"<marker id='m' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{RED}'/></marker>"
     f"<marker id='mb' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{BLU}'/></marker></defs>",
     f"<rect width='{PW}' height='{PH}' fill='white'/><rect x='6' y='6' width='{PW-12}' height='{PH-12}' fill='none' stroke='{INK}' stroke-width='0.4'/>"]
def txt(x, y, t, sz=2.6, a="start", c=INK, w="normal", rot=None):
    tr = f" transform='rotate({rot} {x:.2f} {y:.2f})'" if rot is not None else ""
    o.append(f"<text x='{x:.2f}' y='{y:.2f}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'{tr}>{t}</text>")
def line(x0, y0, x1, y1, c=INK, w=0.2, dash=None, mk=None, me=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    m = (f" marker-start='url(#{mk})' marker-end='url(#{mk})'" if mk else "") + (f" marker-end='url(#{me})'" if me else "")
    o.append(f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{c}' stroke-width='{w}'{d}{m}/>")

E, S, Pn = PZ.embellecedor(), PZ.soporte(), PZ.panel()
STY = {"panel": ("url(#hw)", "#444"), "emb": ("#8a3b3b", INK), "sop": ("url(#hp)", INK), "tac": ("#3c3c3c", INK)}
def dibuja(ox, oy, k, piezas, recorte=(-14, 14)):
    X = lambda x: ox + x * k; Y = lambda y: oy - y * k
    for nombre, w, dx in piezas:
        f, st = STY[nombre]
        for face in corte(w.translate((dx, 0, 0))):
            pts = [[(x, y) for x, y in ring] for ring in face]
            if nombre == "panel": pts = [[(x, max(min(y, recorte[1]), recorte[0])) for x, y in ring] for ring in pts]
            d = " ".join("M" + " L".join(f"{X(x):.2f},{Y(y):.2f}" for x, y in ring) + " Z" for ring in pts)
            o.append(f"<path d='{d}' fill='{f}' fill-rule='evenodd' stroke='{st}' stroke-width='0.25' stroke-linejoin='round'/>")
    return X, Y

# ---------- 1 · montado, en reposo (3:1) ----------
k = 3.0
txt(14, 16, "Pulsador de cancelar · soporte PC-S + embellecedor PC-E + táctil 6×6", 4.2, w="bold")
txt(14, 22, "Sección horizontal por una fila de patas · escala 3:1 · cotas en mm", 2.6, c=Q)
X, Y = dibuja(75, 77, k, [("panel", Pn, 0), ("emb", E, 0), ("sop", S, 0), ("tac", PZ.tactil(), 0)])
txt(X(-4), Y(-14) + 4, "frontal (DM 8)", 2.4, "middle", Q)
txt(X(-16), Y(0) + 1, "FUERA", 2.6, "end", Q); txt(X(16), Y(0) + 1, "DENTRO", 2.6, "start", Q)
def etiqueta(px, py, tx, ty, t, a="start"):
    o.append(f"<circle cx='{px:.2f}' cy='{py:.2f}' r='0.5' fill='{INK}'/>"); line(px, py, tx, ty, INK, 0.15); txt(tx + (1 if a == "start" else -1), ty + 0.9, t, 2.4, a)
etiqueta(X(-9), Y(-3), X(-15), Y(-11), "PC-E embellecedor", "end")
etiqueta(X(0.8), Y(-7.5), X(4), Y(-17), "collarín Ø16 (no deja que se salga)")
etiqueta(X(6), Y(-10), X(16), Y(-12), "PC-S soporte, pegado al frontal")
etiqueta(X(4.5), Y(1.5), X(16), Y(9), "táctil 6×6, pegado en el soporte")
etiqueta(X(9.5), Y(3.25), X(16), Y(5), "patas: aquí se sueldan los cables")
def cota_h(x0, x1, y, t, dy=-1):
    line(X(x0), y, X(x1), y, RED, 0.15, mk="m"); txt((X(x0) + X(x1)) / 2, y + dy, t, 2.2, "middle", RED)
yb = Y(14) - 3.5
for xx in (-11, -8, 0, PZ.SOP_L): line(X(xx), Y(6), X(xx), yb - 1, RED, 0.08, "0.6 0.5")
cota_h(-11, -8, yb, "3"); cota_h(-8, 0, yb, "8"); cota_h(0, PZ.SOP_L, yb, f"{PZ.SOP_L:.1f}".replace('.', ','))
line(X(-12.5), Y(5.75), X(-12.5), Y(-5.75), RED, 0.15, mk="m"); txt(X(-12.5) - 1, Y(0), "Ø11,5", 2.2, "middle", RED, rot=-90)
txt(X(1.6), Y(13) - 10, "", 2)

# ---------- 2 · cómo funciona ----------
bx = 190
txt(bx, 34, "Cómo funciona", 3.4, w="bold")
L = ["• El embellecedor pasa por el agujero Ø12 del frontal y sobresale 3 mm.",
     "• Por dentro, su collarín Ø16 apoya en el frontal: no se puede sacar",
     "   tirando desde fuera.",
     f"• Detrás del collarín está el botón del táctil, con {PZ.JUEGO:.1f} mm de juego".replace('.', ',', 1),
     "   (el embellecedor no baila y el táctil no queda pulsado).",
     "• Al apretar, el embellecedor entra ~0,35 mm, empuja el botón",
     "   (recorrido 0,25) y el táctil hace clic: cierra el contacto.",
     "• Al soltar, el muelle del táctil devuelve el embellecedor.",
     "• El hueco Ø17 del soporte deja moverse al collarín y además",
     "   centra el soporte respecto al embellecedor al pegarlo.",
     "• Conexión: 2 patas de un mismo lado (contacto NA) → JB pin 8",
     "   (cancelar) y GND, con la resistencia de pull-up de la FPGA."]
for i, t in enumerate(L): txt(bx, 41 + i * 4.1, t, 2.3)

# ---------- 3 · montaje paso a paso (2:1) ----------
txt(14, 130, "Montaje", 3.4, w="bold")
k2 = 1.6
pasos = [("1", "Mide tu táctil (alto total).", "Si no es 5 mm, cambia H_PULS", "en pulsador.py y reexporta."),
         ("2", "Pega el táctil en el soporte,", "patas por las ranuras. Suelda", "2 cables y sácalos por la muesca."),
         ("3", "Mete el embellecedor por el", "agujero desde DENTRO del frontal", "(el collarín queda por dentro)."),
         ("4", "Pon cola en la cara del soporte,", "encájalo sobre el collarín y", "aprieta 1 min. Prueba el clic."),
        ]
for i, (n, a, b, c) in enumerate(pasos):
    cx = 20 + i * 68; cy = 152
    o.append(f"<circle cx='{cx}' cy='{cy - 14}' r='3' fill='white' stroke='{INK}' stroke-width='0.3'/>"); txt(cx, cy - 13, n, 3, "middle", w="bold")
    ox = cx + 22
    if n == "1":
        dibuja(ox - PZ.X_BOTON * 3, cy, 3, [("tac", PZ.tactil(), 0)])
        line(ox, cy + 12, ox + PZ.H_PULS * 3, cy + 12, RED, 0.15, mk="m"); txt(ox + PZ.H_PULS * 1.5, cy + 16, "alto total (5)", 2.1, "middle", RED)
        for xx in (ox, ox + PZ.H_PULS * 3): line(xx, cy - 4, xx, cy + 13, RED, 0.08, "0.6 0.5")
    elif n == "2":
        dibuja(ox - 6, cy, k2, [("sop", S, 0), ("tac", PZ.tactil(), 0)])
        line(ox - 24, cy, ox - 12, cy, BLU, 0.35, me="mb"); txt(ox - 24, cy - 2, "táctil", 2.0, "start", BLU)
    elif n == "3":
        dibuja(ox - 4, cy, k2, [("panel", Pn, 0), ("emb", E, 9)], (-12, 12))
        line(ox + 26, cy, ox + 15, cy, BLU, 0.35, me="mb")
    else:
        dibuja(ox - 4, cy, k2, [("panel", Pn, 0), ("emb", E, 0), ("sop", S, 7), ("tac", PZ.tactil(), 7)], (-12, 12))
        line(ox + 34, cy - 14, ox + 12, cy - 14, BLU, 0.35, me="mb")
    for j, t in enumerate((a, b, c)): txt(cx - 3, cy + 27 + j * 4, t, 2.3)
txt(14, 198, f"Imprimir: PC-E con el collarín sobre la cama; PC-S con la cara de atrás sobre la cama (sin soportes). Cola: cianoacrilato o epoxi. Posición en la máquina: lat 55, z 176 (plano corte 1, detalle E).", 2.2, c=Q)
o.append("</svg>")
open("esquema_pulsador.svg", "w").write("\n".join(o))
