"""Hoja A3 apaisada con las tres piezas (CR-1, CR-2, CR-3): vistas por secciones del modelo, cotas, taladros e impresión."""
import math, cadquery as cq, crestas as CR

def _pts(w, ax):
    out = []
    for e in w.Edges():
        k = 1 if e.geomType() == "LINE" else 24
        out.append([tuple(getattr(e.positionAt(i / k), a) for a in ax) for i in range(k + 1)])
    ch = out.pop(0)
    while out:
        l = ch[-1]; best = None
        for i, s in enumerate(out):
            for q in (s, s[::-1]):
                d = (q[0][0] - l[0]) ** 2 + (q[0][1] - l[1]) ** 2
                if best is None or d < best[0]: best = (d, i, q)
        ch += best[2][1:]; out.pop(best[1])
    return ch
def seccion(w, eje, c):
    """eje 'y': plano y=c, puntos (x,z); 'x': plano x=c, puntos (y,z); 'z': plano z=c, puntos (x,y)"""
    big = {"y": cq.Solid.makeBox(600, 0.02, 600, cq.Vector(-100, c - 0.01, -100)),
           "x": cq.Solid.makeBox(0.02, 600, 600, cq.Vector(c - 0.01, -100, -100)),
           "z": cq.Solid.makeBox(600, 600, 0.02, cq.Vector(-100, -100, c - 0.01))}[eje]
    ax = {"y": ("x", "z"), "x": ("y", "z"), "z": ("x", "y")}[eje]
    n = {"y": "y", "x": "x", "z": "z"}[eje]
    sl = w.val().intersect(big); res = []
    for f in sl.Faces():
        if getattr(f.normalAt(), n) < -0.9:
            res.append([_pts(f.outerWire(), ax)] + [_pts(x, ax) for x in f.innerWires()])
    return res

PW, PH = 420.0, 297.0; S = 0.5
INK, Q, RED, BLU = "#222", "#666", "#8b1e1e", "#2f5d8a"
o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{PW}mm' height='{PH}mm' viewBox='0 0 {PW} {PH}' font-family='DejaVu Sans, Arial, sans-serif'>",
     "<defs><pattern id='hm' width='1.6' height='1.6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='1.6' height='1.6' fill='#d3dae3'/><line x1='0' y1='0' x2='0' y2='1.6' stroke='#5b6b80' stroke-width='0.15'/></pattern>"
     f"<marker id='m' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{RED}'/></marker></defs>",
     f"<rect width='{PW}' height='{PH}' fill='white'/><rect x='8' y='8' width='{PW-16}' height='{PH-16}' fill='none' stroke='{INK}' stroke-width='0.5'/>"]
def txt(x, y, t, sz=2.5, a="start", c=INK, w="normal", rot=None):
    tr = f" transform='rotate({rot} {x:.2f} {y:.2f})'" if rot is not None else ""
    o.append(f"<text x='{x:.2f}' y='{y:.2f}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'{tr}>{t}</text>")
def line(x0, y0, x1, y1, c=INK, w=0.2, dash=None, mk=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""; m = f" marker-start='url(#{mk})' marker-end='url(#{mk})'" if mk else ""
    o.append(f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{c}' stroke-width='{w}'{d}{m}/>")
def dib(faces, X, Y, fill="url(#hm)"):
    for f in faces:
        d = " ".join("M" + " L".join(f"{X(a):.2f},{Y(b):.2f}" for a, b in r) + " Z" for r in f)
        o.append(f"<path d='{d}' fill='{fill}' fill-rule='evenodd' stroke='{INK}' stroke-width='0.3' stroke-linejoin='round'/>")
def cota(x0, y0, x1, y1, t, off=(0, -1), rot=None):
    line(x0, y0, x1, y1, RED, 0.15, mk="m"); txt((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], t, 2.2, "middle", RED, rot=rot)
def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".").replace(".", ",")

c1, h1 = CR.cresta("cresta1"); c2, h2 = CR.cresta("cresta2"); ca, h3, zb1 = CR.canal()
tg = CR.tg

def vista_cresta(w, cr, hs, ox, oy, titulo, codigo):
    """alzado (corte por y = 1,5: pared de la U + lengüetas) y sección de la U por el vértice"""
    xs, zs = cr["x0"], cr["vert"][1] - (cr["vert"][0] - cr["x0"]) * tg   # origen: extremo delantero, cara superior
    X = lambda x: ox + (x - cr["x0"]) * S; Y = lambda z: oy - (z - cr["vert"][1]) * S
    txt(ox, oy - 32, f"{codigo} · {titulo}", 3.2, w="bold")
    dib(seccion(w, "y", 1.5), X, Y)
    # perfil del suelo (línea del interior del carril) en discontinua
    xv, zv = cr["vert"]
    line(X(cr["x0"]), Y(zv - (xv - cr["x0"]) * tg), X(xv), Y(zv), BLU, 0.2, "1.2 0.8"); line(X(xv), Y(zv), X(cr["x1"]), Y(zv - (cr["x1"] - xv) * tg), BLU, 0.2, "1.2 0.8")
    # cotas
    L = cr["x1"] - cr["x0"]; zl = min(zv - (xv - cr["x0"]) * tg, zv - (cr["x1"] - xv) * tg)
    bb = w.val().BoundingBox()
    yb = Y(bb.zmin) + 6
    for xx in (cr["x0"], xv, cr["x1"]): line(X(xx), Y(bb.zmin) + 1, X(xx), yb + 1, RED, 0.08, "0.6 0.5")
    cota(X(cr["x0"]), yb, X(xv), yb, f1(xv - cr["x0"])); cota(X(xv), yb, X(cr["x1"]), yb, f1(cr["x1"] - xv))
    cota(X(cr["x0"]), yb + 6, X(cr["x1"]), yb + 6, f1(L))
    # 30°
    xa = cr["x0"]; za = zv - (xv - xa) * tg
    line(X(xa), Y(za), X(xa) + 16, Y(za), RED, 0.12, "1 0.6"); txt(X(xa) + 17, Y(za) - 1.5, "30°", 2.2, "start", RED)
    # alturas de la U
    hv = CR.H_U / CR.c30
    line(X(xv) + 2, Y(zv), X(xv) + 2, Y(zv + hv), RED, 0.15, mk="m"); txt(X(xv) + 3, Y(zv + hv / 2) + 0.8, "15 ⊥", 2.1, "start", RED)
    # lengüetas: cotas en una
    xc, za_ = hs[0]
    txt(X(xc), Y(za_) + 5.5, "Ø3,5", 2.0, "middle", RED)
    for xc, zc in hs: o.append(f"<circle cx='{X(xc):.2f}' cy='{Y(zc):.2f}' r='0.5' fill='{RED}'/>")
    # sección de la U por el vértice (a la derecha)
    sx = X(cr["x1"]) + 18
    U = seccion(w, "x", xv + 10.0)
    YY = lambda y: sx + y * S
    dib(U, YY, Y)
    txt(sx + CR.ANCHO * S / 2, Y(zv + hv) - 4, "sección de la U (a 10 del vértice)", 2.1, "middle", Q)
    cota(YY(0), Y(zv + hv) - 1.5, YY(CR.ANCHO), Y(zv + hv) - 1.5, "46")
    line(YY(CR.ANCHO) + 2, Y(zv - CR.T / CR.c30), YY(CR.ANCHO) + 2, Y(zv + hv), RED, 0.15, mk="m")
    txt(YY(CR.ANCHO) + 3, Y(zv + hv / 2), "pared U", 2.0, "start", RED)
    txt(YY(0), Y(bb.zmin) + 3, "pared de la máquina", 1.9, "start", Q)
    return Y(bb.zmin)

y1 = vista_cresta(c1, CR.CRESTAS["cresta1"], h1, 22, 62, "cresta 1 (bajo B)", "CR-1")
y2 = vista_cresta(c2, CR.CRESTAS["cresta2"], h2, 22, 150, "cresta 2 (bajo C)", "CR-2")

# ---- canal ----
ox, oy = 290, 60
txt(ox - 8, 30, "CR-3 · caja del canal de no válidas", 3.2, w="bold")
X = lambda x: ox + (x - 84) * S; Y = lambda z: oy - (z - 262) * S
dib(seccion(ca, "y", 1.5), X, Y)
for xx, zz in h3: o.append(f"<circle cx='{X(xx):.2f}' cy='{Y(zz):.2f}' r='0.5' fill='{RED}'/>")
txt(X(114), Y(270), "alzado (lado de la pared de la máquina)", 2.1, "middle", Q)
yb = Y(118) + 5
for xx in (97, 100, 128, 131): line(X(xx), Y(118) + 1, X(xx), yb + 1, RED, 0.08, "0.6 0.5")
cota(X(97), yb, X(131), yb, "34"); cota(X(100), yb + 5, X(128), yb + 5, "28 paso")
xr = X(144) + 4
cota(xr, Y(262), xr, Y(118), "144", (-1.2, 0), rot=-90)
cota(xr + 6, Y(zb1), xr + 6, Y(137), f1(zb1 - 137), (-1.2, 0), rot=-90)
for zz in (262, 118): line(X(100), Y(zz), xr + 1, Y(zz), RED, 0.08, "0.6 0.5")
for zz in (zb1, 137): line(X(131), Y(zz), xr + 7, Y(zz), RED, 0.08, "0.6 0.5")
txt(X(90.5), Y(135) + 5, "Ø3,5", 2.0, "middle", RED)
# planta (sección z = 200)
py = Y(118) + 30
Xp = lambda x: ox + (x - 84) * S; Yp = lambda y: py + y * S
dib(seccion(ca, "z", 220), Xp, Yp)
txt(Xp(114), py - 3, "sección z = 220 (planta)", 2.1, "middle", Q)
line(Xp(80), Yp(0), Xp(150), Yp(0), Q, 0.25, "2 1"); txt(Xp(150) + 1, Yp(0) + 0.8, "pared de la máquina", 1.9, "start", Q)
cota(Xp(146) + 4, Yp(0), Xp(146) + 4, Yp(46), "46", (-1.2, 0), rot=-90)
txt(Xp(114), Yp(46) + 5, "orejas simples, como las de las crestas", 1.9, "middle", Q)

# ---- tabla de taladros (pared lateral) e impresión ----
tx, ty = 200, 215
txt(tx, ty, "Taladros Ø3,4 en la pared lateral de la columna (x, z) · M3 + tuerca, como B y C", 2.8, w="bold")
rows = [("CR-1", h1), ("CR-2", h2), ("CR-3", h3)]
for i, (n, hs) in enumerate(rows):
    txt(tx, ty + 6 + i * 4.5, n, 2.4, w="bold"); txt(tx + 14, ty + 6 + i * 4.5, " · ".join(f"({f1(a)}, {f1(b)})" for a, b in hs), 2.4)
nota = ["Coordenadas de la máquina (las del plano del corte 1): x desde la cara exterior del frontal, z desde la cara inferior del suelo.",
        "Todo PLA, paredes de 3 (como los cubiletes). Lengüetas 14 × 13 × 3 con agujero Ø3,5 a 6,5 del borde, en el plano de la pared.",
        "Paredes de la U: 15 sobre el suelo del carril (una de 2 € de canto tiene el centro a 12,9 y no vuelca).",
        "Impresión de las tres: tumbadas sobre la cara de la pared de la máquina (orejas planas en la cama); soporte solo bajo la pared del otro lado.",
                f"La chapa trasera de CR-3 acaba en z {f1(zb1)}, 0,5 por debajo de la cresta 1; la cresta apoya sobre ella al montar."]
for i, t in enumerate(nota): txt(tx, ty + 24 + i * 4.2, t, 2.05, c=Q)
o.append(f"<rect x='{PW-128}' y='{PH-30}' width='120' height='22' fill='none' stroke='{INK}' stroke-width='0.4'/>")
line(PW - 128, PH - 22, PW - 8, PH - 22, INK, 0.25); line(PW - 128, PH - 15, PW - 8, PH - 15, INK, 0.25); line(PW - 58, PH - 22, PW - 58, PH - 8, INK, 0.25)
txt(PW - 125, PH - 24.5, "Máquina expendedora SED · crestas en U y canal", 3.2, w="bold")
txt(PW - 125, PH - 17.5, "Escala 1:2 (A3 apaisado al 100 %)", 2.5); txt(PW - 55, PH - 17.5, "Hoja 1/1 · v1 · 13-11-2026", 2.5)
txt(PW - 125, PH - 10.5, "Cotas en mm · STEP/STL en cad/maquina/crestas", 2.5); txt(PW - 55, PH - 10.5, "UPM ETSIDI · SED 2026-27", 2.5)
o.append("</svg>"); open("crestas.svg", "w").write("\n".join(o)); print(y1, y2)
