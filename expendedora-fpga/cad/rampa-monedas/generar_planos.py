import math, os, sys
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

INK = "#1f2328"; DIM = "#0b5cad"; BEAM = "#c62828"; COIN = "#c9a227"; WALL = "#d9d9d9"; QUIET = "#57606a"
FONT = "font-family='DejaVu Sans, Arial, sans-serif'"

def svg(w, h, body, title):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}>"
            f"<title>{title}</title>"
            "<defs><marker id='a' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0L10 5L0 10z' fill='{DIM}'/></marker>"
            "<marker id='b' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
            f"<path d='M0 0L10 5L0 10z' fill='{INK}'/></marker></defs>"
            f"<rect width='{w}' height='{h}' fill='white'/>{body}</svg>")

def t(x, y, s, size=13, anchor="start", fill=INK, weight="normal", rot=None):
    r = f" transform='rotate({rot} {x} {y})'" if rot is not None else ""
    return f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' text-anchor='{anchor}' fill='{fill}' font-weight='{weight}'{r}>{s}</text>"

def line(x1, y1, x2, y2, c=INK, w=1.5, dash=None, extra=""):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{c}' stroke-width='{w}'{d} {extra}/>"

def hdim(x1, x2, y, yref, label, above=True):
    """horizontal dimension at y with extension lines from yref"""
    o = line(x1, yref, x1, y + (4 if y > yref else -4), DIM, 0.8) + line(x2, yref, x2, y + (4 if y > yref else -4), DIM, 0.8)
    o += f"<line x1='{x1}' y1='{y}' x2='{x2}' y2='{y}' stroke='{DIM}' stroke-width='1' marker-start='url(#a)' marker-end='url(#a)'/>"
    o += t((x1 + x2) / 2, y - 5 if above else y + 15, label, 12, "middle", DIM)
    return o

def vdim(x, y1, y2, xref, label, left=True):
    o = line(xref, y1, x + (-4 if x < xref else 4), y1, DIM, 0.8) + line(xref, y2, x + (-4 if x < xref else 4), y2, DIM, 0.8)
    o += f"<line x1='{x}' y1='{y1}' x2='{x}' y2='{y2}' stroke='{DIM}' stroke-width='1' marker-start='url(#a)' marker-end='url(#a)'/>"
    ym = (y1 + y2) / 2
    o += t(x - 6 if left else x + 6, ym + 4, label, 12, "end" if left else "start", DIM)
    return o

BEAMS = [("P1", 50, 10.0), ("B1", 60, 19.25), ("B2", 70, 20.5), ("B3", 80, 21.75),
         ("B4", 90, 22.75), ("B5", 100, 23.75), ("P2", 110, 10.0)]

# ---------------- 1. Vista lateral del carril ----------------
def lateral():
    s = 5.0; x0 = 200; yf = 420  # floor
    X = lambda mm: x0 + mm * s
    Y = lambda mm: yf - mm * s
    b = []
    b.append(t(24, 32, "1 · Vista lateral del carril (desde la cara del LED), escala 5:1 en pantalla", 17, weight="bold"))
    b.append(t(24, 54, "Dibujado en horizontal. Montado, todo el carril baja 10° hacia el fondo de la máquina.", 13, fill=QUIET))
    # walls: back wall silhouette (rectangle) 0..150 x -3..35
    b.append(f"<rect x='{X(0)}' y='{Y(35)}' width='{150*s}' height='{38*s}' fill='{WALL}' fill-opacity='0.35' stroke='{INK}' stroke-width='1.5'/>")
    # floor line
    b.append(line(X(0), Y(0), X(150), Y(0), INK, 2.5))
    b.append(t(X(150) - 4, Y(0) - 6, "suelo del carril", 11, "end", QUIET))
    # lid
    b.append(line(X(0), Y(32), X(150), Y(32), INK, 1.5, "6 4"))
    b.append(t(X(150) - 4, Y(32) - 6, "tapa superior (a 32 mm)", 11, "end", QUIET))
    # front panel and slot
    b.append(f"<rect x='{X(-4)}' y='{Y(60)}' width='{4*s}' height='{70*s}' fill='{WALL}' stroke='{INK}' stroke-width='1.5'/>")
    b.append(f"<rect x='{X(-4)-1}' y='{Y(28)}' width='{4*s+2}' height='{25*s}' fill='white' stroke='{INK}' stroke-width='1.5'/>")
    b.append(t(X(-4) - 6, Y(55) + 4, "panel frontal", 11, "end", QUIET))
    b.append(t(X(-4) - 6, Y(55) + 18, "(4 mm)", 11, "end", QUIET))
    b.append(vdim(X(-4) - 34, Y(28), Y(3), X(-4), "25,0", True))
    b.append(t(X(-4) - 40, Y(28) - 10, "ranura (rechaza el 2 €)", 11, "end", DIM))
    b.append(vdim(X(-4) - 34, Y(3), Y(0), X(-4), "3", True))
    # coin entering arrow
    b.append(f"<line x1='{X(-4)}' y1='{Y(15)}' x2='{X(8)}' y2='{Y(15)}' stroke='{INK}' stroke-width='1.5' marker-end='url(#b)'/>")
    b.append(t(X(1), Y(15) - 8, "entra la moneda", 11, "start", INK))
    # coin example: 50c rolling at x center 75
    d = 24.25; cx = 82
    b.append(f"<circle cx='{X(cx)}' cy='{Y(d/2)}' r='{d/2*s}' fill='{COIN}' fill-opacity='0.35' stroke='{COIN}' stroke-width='2'/>")
    b.append(t(X(cx), Y(d/2) + 4, "50c", 12, "middle", INK, "bold"))
    # zones
    for a, c, lab in [(0, 50, "entrada y asentamiento"), (50, 110, "zona de medida"), (110, 150, "salida")]:
        b.append(t((X(a) + X(c)) / 2, Y(-14), lab, 12, "middle", QUIET))
        b.append(line(X(a) + 2, Y(-11), X(c) - 2, Y(-11), QUIET, 1))
    # beams
    for i, (n, x, h) in enumerate(BEAMS):
        cx_, cy_ = X(x), Y(h)
        b.append(f"<circle cx='{cx_}' cy='{cy_}' r='5' fill='white' stroke='{BEAM}' stroke-width='2'/><circle cx='{cx_}' cy='{cy_}' r='1.8' fill='{BEAM}'/>")
        ly = Y(48) + (0 if i % 2 == 0 else 0)
        b.append(line(cx_, cy_ - 6, cx_, Y(40), BEAM, 0.8, "3 3"))
        b.append(t(cx_, Y(46), n, 12, "middle", BEAM, "bold"))
        b.append(t(cx_, Y(42.5), f"{h:.2f}".replace(".", ","), 11, "middle", BEAM))
    b.append(t(X(42), Y(46), "barrera", 11, "end", QUIET))
    b.append(t(X(42), Y(42.5), "altura (mm)", 11, "end", QUIET))
    # dimension chain along bottom
    yd = Y(-22)
    pts = [0, 50, 60, 70, 80, 90, 100, 110, 150]
    for a, c in zip(pts, pts[1:]):
        b.append(hdim(X(a), X(c), yd, Y(0) + 4, str(c - a)))
    b.append(hdim(X(0), X(150), Y(-32), Y(0) + 4, "150 (longitud total del carril)"))
    # walls height
    b.append(vdim(X(150) + 30, Y(32), Y(0), X(150), "32", False))
    # exit arrow
    b.append(f"<line x1='{X(150)}' y1='{Y(5)}' x2='{X(150)+40}' y2='{Y(-8)}' stroke='{INK}' stroke-width='1.5' marker-end='url(#b)'/>")
    b.append(t(X(150) + 10, Y(-12) + 8, "a zona de espera", 11, "start", INK))
    W = int(X(150) + 130); H = int(Y(-32) + 30)
    open(f"{OUT}/1-carril-lateral.svg", "w").write(svg(W, H, "".join(b), "Vista lateral del carril"))

# ---------------- 2. Seccion transversal ----------------
def seccion():
    s = 11.0
    ox, oy = 360, 560  # floor point: back wall inner face meets floor
    ang = 12
    b = []
    b.append(t(24, 32, "2 · Sección transversal por una barrera (B4), escala 11:1 en pantalla", 17, weight="bold"))
    b.append(t(24, 54, "El canal entero va inclinado 12° hacia atrás: la moneda se apoya en la pared con el fototransistor.", 13, fill=QUIET))
    g = []
    P = lambda u, v: (u * s, -v * s)
    def rect(u1, v1, u2, v2, fill, stroke=INK, sw=1.5, op=1):
        x1, y1 = P(u1, v2); return f"<rect x='{x1}' y='{y1}' width='{(u2-u1)*s}' height='{(v2-v1)*s}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}'/>"
    gap = 3.2; wt = 4; h = 22.75
    # back wall with hole, front wall with hole
    g.append(rect(-wt, -3, 0, 32, WALL))
    g.append(rect(gap, -3, gap + wt, 32, WALL))
    g.append(rect(-wt, -3, gap + wt, 0, WALL))
    g.append(rect(-wt, 32, gap + wt, 35, WALL))  # lid
    # holes
    g.append(rect(-wt, h - 1.6, 0, h + 1.6, "white", INK, 1))
    g.append(rect(gap, h - 1.6, gap + wt, h + 1.6, "white", INK, 1))
    # slit insert on back wall inner face
    g.append(rect(-1.2, h + 0.5, 0, h + 1.6, INK, INK, 0.5))
    g.append(rect(-1.2, h - 1.6, 0, h - 0.5, INK, INK, 0.5))
    # coin 50c leaning on back wall
    g.append(rect(0, 0, 2.38, 24.25, COIN, COIN, 2, 0.45))
    # phototransistor (back) and LED (front)
    g.append(rect(-wt - 5.5, h - 1.5, -wt, h + 1.5, "#444", INK, 1))
    g.append(rect(gap + wt, h - 1.5, gap + wt + 5.5, h + 1.5, "#ddd", INK, 1))
    # beam
    x1, y1 = P(-wt, h); x2, y2 = P(gap + wt, h)
    g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{BEAM}' stroke-width='2' stroke-dasharray='5 3'/>")
    body = "".join(g)
    b.append(f"<g transform='translate({ox} {oy}) rotate({-ang})'>{body}</g>")
    # helper to map rotated coords to screen
    def S(u, v):
        x, y = u * s, -v * s
        a = math.radians(-ang)
        return ox + x * math.cos(a) - y * math.sin(a), oy + x * math.sin(a) + y * math.cos(a)
    # vertical reference and angle
    bx, by = S(-wt, 35)
    b.append(line(ox - wt * s * math.cos(math.radians(12)), oy, ox - wt * s * math.cos(math.radians(12)), by - 30, QUIET, 1, "4 3"))
    # labels with leaders
    def lab(u, v, tx, ty, s1, s2=None, anchor="start"):
        x, y = S(u, v)
        o = line(x, y, tx, ty, QUIET, 0.8)
        o += t(tx + (4 if anchor == "start" else -4), ty + 4, s1, 12, anchor)
        if s2: o += t(tx + (4 if anchor == "start" else -4), ty + 19, s2, 11, anchor, QUIET)
        return o
    b.append(lab(-wt - 5.5, h, 190, 250, "Fototransistor", "en la pared trasera", "end"))
    b.append(lab(-1.0, h - 1.2, 190, 340, "Rendija de 1 mm de alto", "pieza sustituible", "end"))
    b.append(lab(gap + wt + 5.5, h, 590, 250, "LED IR 3 mm", "en la pared delantera"))
    b.append(lab(1.6, 6, 590, 470, "Moneda (50c)", "apoyada en la pared trasera"))
    b.append(lab(gap + wt / 2, 34, 590, 140, "Tapa (3 mm)"))
    # dims (in rotated frame, drawn manually)
    def rdim(u1, v1, u2, v2, off_u, off_v, label, tx_off=(0, 0)):
        a1 = S(u1 + off_u, v1 + off_v); a2 = S(u2 + off_u, v2 + off_v)
        e1 = S(u1, v1); e2 = S(u2, v2)
        o = line(*e1, *a1, DIM, 0.7) + line(*e2, *a2, DIM, 0.7)
        o += f"<line x1='{a1[0]:.1f}' y1='{a1[1]:.1f}' x2='{a2[0]:.1f}' y2='{a2[1]:.1f}' stroke='{DIM}' stroke-width='1' marker-start='url(#a)' marker-end='url(#a)'/>"
        mx, my = (a1[0] + a2[0]) / 2 + tx_off[0], (a1[1] + a2[1]) / 2 + tx_off[1]
        o += t(mx, my, label, 12, "middle", DIM)
        return o
    b.append(rdim(gap + wt, 0, gap + wt, h, 9, 0, "22,75", (34, 4)))
    b.append(rdim(gap + wt, 0, gap + wt, 32, 17, 0, "32 interior", (44, 4)))
    b.append(rdim(0, 0, gap, 0, 0, -6, "3,2", (0, 16)))
    b.append(rdim(-wt, 0, 0, 0, 0, -6, "4", (-6, 16)))
    b.append(rdim(gap, 0, gap + wt, 0, 0, -6, "4", (6, 16)))
    # angle text
    b.append(t(ox - wt * s - 20, by - 4, "12° respecto a la vertical", 12, "end", DIM))
    b.append(t(24, 700, "Altura de cada barrera = distancia desde el suelo del canal, medida a lo largo de la pared trasera.", 12, fill=QUIET))
    b.append(t(24, 718, "Como el suelo es perpendicular a la pared, esa altura coincide con el diámetro de la moneda que la corta.", 12, fill=QUIET))
    open(f"{OUT}/2-carril-seccion.svg", "w").write(svg(760, 740, "".join(b), "Sección transversal del canal"))

# ---------------- 3. Detalle de alturas ----------------
def alturas():
    s = 60.0; y0 = 470; base = 18.0
    Y = lambda mm: y0 - (mm - base) * s
    b = []
    b.append(t(24, 32, "3 · Qué barreras corta cada moneda (escala vertical 60:1)", 17, weight="bold"))
    b.append(t(24, 54, "Barra = altura de la moneda (su diámetro). Franja rosa = rendija de 1 mm de cada barrera.", 13, fill=QUIET))
    coins = [("2c", 18.75, "rechazo"), ("10c", 19.75, "acepta"), ("5c", 21.25, "acepta"),
             ("20c", 22.25, "acepta"), ("1 €", 23.25, "acepta"), ("50c", 24.25, "acepta")]
    xl, xr = 150, 720
    for n, x, h in BEAMS[1:6]:
        b.append(f"<rect x='{xl}' y='{Y(h+0.5)}' width='{xr-xl}' height='{s}' fill='{BEAM}' fill-opacity='0.08'/>")
        b.append(line(xl, Y(h), xr, Y(h), BEAM, 1.2, "6 4"))
        b.append(t(xl - 8, Y(h) - 2, n, 13, "end", BEAM, "bold"))
        b.append(t(xl - 8, Y(h) + 13, f"{h:.2f} mm".replace(".", ","), 11, "end", BEAM))
    bw = 60; gapx = (xr - xl - 6 * bw) / 7
    for i, (n, d, res) in enumerate(coins):
        x = xl + gapx + i * (bw + gapx)
        ok = res == "acepta"
        b.append(f"<rect x='{x}' y='{Y(d)}' width='{bw}' height='{Y(base)-Y(d)}' fill='{COIN}' fill-opacity='{0.55 if ok else 0.18}' stroke='{COIN}' stroke-width='1.5'/>")
        b.append(t(x + bw / 2, Y(d) - 8, f"{d:.2f}".replace(".", ","), 12, "middle"))
        b.append(t(x + bw / 2, y0 + 20, n, 14, "middle", INK, "bold"))
        b.append(t(x + bw / 2, y0 + 38, res, 12, "middle", INK if ok else QUIET))
    b.append(line(xl, y0, xr, y0, INK, 1.5))
    b.append(t(xl - 8, y0 + 4, "18 mm", 11, "end", QUIET))
    b.append(t(24, y0 + 66, "Todas las barreras quedan a 0,5 mm de la moneda más cercana por arriba y por abajo: ese es el margen a calibrar.", 12, fill=QUIET))
    b.append(t(24, y0 + 84, "P1 y P2 (a 10 mm) las corta cualquier moneda; abren y cierran la ventana de medida.", 12, fill=QUIET))
    open(f"{OUT}/3-alturas.svg", "w").write(svg(760, y0 + 100, "".join(b), "Detalle de alturas"))

# ---------------- 4. Ubicacion en la maquina ----------------
def maquina():
    s = 0.75
    b = []
    b.append(t(24, 32, "4 · Dónde va el sistema de monedas en la máquina (60 × 40 × 40 cm, escala 1:4 en pantalla aprox.)", 17, weight="bold"))
    b.append(t(24, 54, "Cotas en mm desde el suelo de la máquina y desde la cara exterior del frontal. Son una propuesta de partida.", 13, fill=QUIET))
    # front view
    fx, fy = 70, 600  # bottom-left
    F = lambda x, y: (fx + x * s, fy - y * s)
    def frect(x, y, w, h, fill="none", stroke=INK, sw=1.5, op=1, dash=None):
        X0, Y0 = F(x, y + h); d = f" stroke-dasharray='{dash}'" if dash else ""
        return f"<rect x='{X0:.1f}' y='{Y0:.1f}' width='{w*s:.1f}' height='{h*s:.1f}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}'{d}/>"
    b.append(t(F(200, 600)[0], F(200, 600)[1] - 30, "Vista frontal", 14, "middle", INK, "bold"))
    b.append(frect(0, 0, 400, 600, WALL, INK, 2, 0.25))
    b.append(frect(20, 120, 260, 420, "#e8f1fb", QUIET, 1))
    x, y = F(150, 330); b.append(t(x, y, "escaparate", 12, "middle", QUIET))
    b.append(frect(20, 30, 260, 70, "none", QUIET, 1))
    x, y = F(150, 60); b.append(t(x, y, "recogida de producto", 12, "middle", QUIET))
    b.append(frect(300, 470, 80, 40, "none", QUIET, 1)); x, y = F(340, 486); b.append(t(x, y, "OLED", 11, "middle", QUIET))
    for i in range(4):
        cx, cy = F(340, 455 - i * 22); b.append(f"<circle cx='{cx}' cy='{cy}' r='{6*s*1.2}' fill='none' stroke='{QUIET}'/>")
    x, y = F(300, 425); b.append(t(x - 4, y, "botones", 11, "end", QUIET))
    # coin slot: 3.2 x 25 vertical, bottom at 352
    b.append(frect(338.4, 352, 3.2 * 2.5, 25, BEAM, BEAM, 1.5, 0.9))
    x, y = F(350, 365); b.append(t(x + 4, y + 4, "ranura", 12, "start", BEAM, "bold"))
    b.append(frect(300, 40, 80, 50, "none", BEAM, 1.5)); x, y = F(340, 60); b.append(t(x, y, "devolución", 11, "middle", BEAM))
    # front dims
    a = F(400, 0); c = F(400, 352)
    b.append(vdim(a[0] + 40, c[1], a[1], a[0], "352", False))
    a1 = F(0, -10); a2 = F(340, -10)
    b.append(hdim(F(0, 0)[0], F(340, 0)[0], F(0, 0)[1] + 26, F(0, 0)[1], "340 (eje de la ranura)", False))
    # side section
    sx = 520
    S_ = lambda x, y: (sx + x * s, fy - y * s)
    def srect(x, y, w, h, fill="none", stroke=INK, sw=1.5, op=1, dash=None):
        X0, Y0 = S_(x, y + h); d = f" stroke-dasharray='{dash}'" if dash else ""
        return f"<rect x='{X0:.1f}' y='{Y0:.1f}' width='{w*s:.1f}' height='{h*s:.1f}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}'{d}/>"
    b.append(t(S_(200, 600)[0], S_(200, 600)[1] - 30, "Sección lateral por la columna de mandos", 14, "middle", INK, "bold"))
    b.append(srect(0, 0, 400, 600, WALL, INK, 2, 0.25))
    x, y = S_(0, 600); b.append(t(x, y - 6, "frente", 11, "start", QUIET))
    x, y = S_(400, 600); b.append(t(x, y - 6, "fondo", 11, "end", QUIET))
    # rail: from x=4, top floor at 352 down 10deg, length 150
    x1, y1 = S_(4, 352); dx = 150 * math.cos(math.radians(10)); dy = 150 * math.sin(math.radians(10))
    x2, y2 = S_(4 + dx, 352 - dy)
    b.append(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{BEAM}' stroke-width='5'/>")
    
    # holding cup + servo
    b.append(srect(152, 285, 40, 45, "none", INK, 1.5))
    x, y = S_(196, 312); b.append(t(x + 2, y, "zona de espera", 11, "start", INK))
    x, y = S_(196, 298); b.append(t(x + 2, y + 4, "+ compuerta SG90", 11, "start", INK))
    # hucha
    b.append(srect(200, 150, 180, 110, "none", INK, 1.5)); x, y = S_(290, 205); b.append(t(x, y, "hucha (cajón trasero)", 11, "middle", INK))
    cx, cy = S_(185, 285); hx, hy = S_(240, 262)
    b.append(f"<line x1='{cx:.1f}' y1='{cy:.1f}' x2='{hx:.1f}' y2='{hy:.1f}' stroke='{INK}' stroke-width='1.2' marker-end='url(#b)'/>")
    # return chute
    rx, ry = S_(158, 285); tx, ty = S_(40, 90)
    b.append(f"<line x1='{rx:.1f}' y1='{ry:.1f}' x2='{tx:.1f}' y2='{ty:.1f}' stroke='{INK}' stroke-width='1.2' stroke-dasharray='6 4' marker-end='url(#b)'/>")
    x, y = S_(8, 215); b.append(t(x, y, "rampa de", 11, "start", INK)); b.append(t(x, y + 15, "devolución", 11, "start", INK))
    b.append(srect(0, 40, 80, 50, "none", BEAM, 1.5)); x, y = S_(40, 62); b.append(t(x, y, "bandeja", 11, "middle", BEAM))
    b.append(srect(220, 20, 170, 110, "none", QUIET, 1, None, "5 3")); x, y = S_(305, 80); b.append(t(x, y, "bahía placa Nexys", 11, "middle", QUIET))
    # side dims
    b.append(hdim(S_(0, 0)[0], S_(152, 0)[0], S_(0, 0)[1] + 26, S_(0, 0)[1], "152", False))
    b.append(hdim(S_(0, 0)[0], S_(400, 0)[0], S_(0, 0)[1] + 50, S_(0, 0)[1], "400", False))
    b.append(vdim(S_(400, 0)[0] + 40, S_(0, 600)[1], S_(0, 0)[1], S_(400, 0)[0], "600", False))
    x, y = S_(156, 326); b.append(t(x - 4, y + 18, "fin del carril a 326 del suelo", 11, "end", BEAM))
    x, y = S_(4, 352); b.append(t(x + 2, y - 22, "carril 150 mm a 10°, inicio a 352", 11, "start", BEAM, "bold"))
    open(f"{OUT}/4-ubicacion.svg", "w").write(svg(1040, 700, "".join(b), "Ubicacion en la maquina"))

lateral(); seccion(); alturas(); maquina()
print("ok")
