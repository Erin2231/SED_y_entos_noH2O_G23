"""Planos 5 (angulos) y 6 (compuerta y rampas). Reutiliza los helpers de generar_planos.py."""
import math, os, sys, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location("gp", os.path.join(here, "generar_planos.py"))
sys.argv = [sys.argv[0], OUT]
gp = importlib.util.module_from_spec(spec); spec.loader.exec_module(gp)
from math import radians, sin, cos
INK, DIM, BEAM, COIN, WALL, QUIET = gp.INK, gp.DIM, gp.BEAM, gp.COIN, gp.WALL, gp.QUIET
t, line, svg = gp.t, gp.line, gp.svg

def arc(cx, cy, r, a0, a1, color=DIM):
    # angles in degrees, screen coords, measured counterclockwise from +x (y up visually)
    x0, y0 = cx + r * cos(radians(a0)), cy - r * sin(radians(a0))
    x1, y1 = cx + r * cos(radians(a1)), cy - r * sin(radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    return f"<path d='M{x0:.1f} {y0:.1f}A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}' fill='none' stroke='{color}' stroke-width='1.2'/>"

def poly(pts, fill="none", stroke=INK, sw=1.5, op=1, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f"<polygon points='{p}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}'{d}/>"

# ---------------- 5. Angulos ----------------
def angulos():
    b = []
    b.append(t(24, 32, "5 · Los dos ángulos del carril", 17, weight="bold"))
    b.append(t(24, 54, "α hace rodar la moneda hacia el fondo. β la deja apoyada en la pared de los sensores.", 13, fill=QUIET))
    # left: side view, alpha = 10
    a = 10; L = 300; x0, y0 = 60, 160
    x1, y1 = x0 + L * cos(radians(a)), y0 + L * sin(radians(a))
    b.append(t(200, 100, "Vista lateral (de frente a fondo)", 14, "middle", INK, "bold"))
    b.append(line(x0, y0, x1, y1, INK, 4))
    b.append(line(x0, y0, x1 + 20, y0, QUIET, 1, "5 4"))
    b.append(arc(x0, y0, 120, -a, 0))
    b.append(t(x0 + 130, y0 + 16, "α = 10°", 14, "start", DIM, "bold"))
    r = 40; cx = x0 + 150 * cos(radians(a)) - r * sin(radians(a)); cy = y0 + 150 * sin(radians(a)) - r * cos(radians(a))
    b.append(f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r}' fill='{COIN}' fill-opacity='0.35' stroke='{COIN}' stroke-width='2'/>")
    b.append(f"<line x1='{cx+50:.1f}' y1='{cy-10:.1f}' x2='{cx+110:.1f}' y2='{cy:.1f}' stroke='{INK}' stroke-width='1.5' marker-end='url(#b)'/>")
    b.append(t(x0, y1 + 30, "frente", 12, "start", QUIET)); b.append(t(x1, y1 + 30, "fondo", 12, "end", QUIET))
    b.append(t(x0, y1 + 56, "Margen de prueba: 8° a 12°", 12, "start", INK))
    b.append(t(x0, y1 + 74, "Por debajo de unos 5° el roce con la pared la para.", 12, "start", QUIET))
    b.append(t(x0, y1 + 92, "Por encima de 15° rebota y llega demasiado rápida al vaso.", 12, "start", QUIET))
    # right: cross-section, beta = 12
    bt = 12; px, py = 560, 300; H = 190
    b.append(t(560, 100, "Sección (mirando desde el frente)", 14, "middle", INK, "bold"))
    wx, wy = px - H * sin(radians(bt)), py - H * cos(radians(bt))
    b.append(line(px, py, wx, wy, INK, 4))  # back wall (sensors)
    fx0, fy0 = px + 16 * cos(radians(bt)), py + 16 * sin(radians(bt))
    b.append(line(fx0, fy0, fx0 - H * sin(radians(bt)), fy0 - H * cos(radians(bt)), INK, 2, "6 4"))  # front wall
    b.append(line(px - 6 * cos(radians(bt)), py - 6 * sin(radians(bt)), fx0 + 6 * cos(radians(bt)), fy0 + 6 * sin(radians(bt)), INK, 4))  # floor
    cpx, cpy = px + 6 * cos(radians(bt)), py + 6 * sin(radians(bt))
    b.append(line(cpx, cpy, cpx - 150 * sin(radians(bt)), cpy - 150 * cos(radians(bt)), COIN, 9))
    b.append(line(px, py, px, py - H - 10, QUIET, 1, "5 4"))
    b.append(arc(px, py, 150, 90, 90 + bt))
    b.append(t(px - 40, py - 160, "β = 12°", 14, "end", DIM, "bold"))
    b.append(t(wx - 8, wy + 40, "pared trasera", 12, "end", INK))
    b.append(t(wx - 8, wy + 56, "(fototransistores)", 12, "end", QUIET))
    b.append(t(fx0 + 30, fy0 - 120, "pared delantera", 12, "start", INK))
    b.append(t(fx0 + 30, fy0 - 104, "(LEDs)", 12, "start", QUIET))
    b.append(t(cpx + 26, cpy - 30, "moneda", 12, "start", COIN, "bold"))
    b.append(t(440, py + 46, "Margen de prueba: 10° a 15°", 12, "start", INK))
    b.append(t(440, py + 64, "Más β = más roce con la pared;", 12, "start", QUIET))
    b.append(t(440, py + 82, "por eso α debe crecer si sube β.", 12, "start", QUIET))
    b.append(t(24, 430, "Condición para que no se pare: sen α > μ · sen β (μ ≈ 0,35 entre PLA y metal, estimado).", 13, fill=INK))
    b.append(t(24, 450, "Con β = 12° basta α > 4,2°; con α = 10° hay más del doble de margen.", 13, fill=QUIET))
    open(f"{OUT}/5-angulos.svg", "w").write(svg(760, 470, "".join(b), "Angulos del carril"))

# ---------------- 6. Compuerta y rampas ----------------
def compuerta():
    s = 4.0; ox, oy = 140, 770  # machine coords: x depth from front (mm), y height (mm); window x 100..270, y 190..340
    X = lambda x: ox + (x - 100) * s
    Y = lambda y: oy - (y - 190) * s
    P = lambda x, y: (X(x), Y(y))
    b = []
    b.append(t(24, 32, "6 · Compuerta de 3 posiciones y separación hucha / devolución", 17, weight="bold"))
    b.append(t(24, 54, "Sección lateral (frente a la izquierda, fondo a la derecha). Cotas en mm desde el suelo de la máquina.", 13, fill=QUIET))
    # rail end
    re_x, re_y = 154, 326
    b.append(line(X(110), Y(re_y + 44 * math.tan(radians(10))), X(re_x), Y(re_y), BEAM, 5))
    b.append(t(X(112), Y(re_y) + 34, "llega del carril", 12, "start", BEAM, "bold"))
    # cup walls
    cx0, cx1, piv_y = 154, 194, 282
    b.append(line(X(cx0), Y(320), X(cx0), Y(piv_y + 2), INK, 3))
    b.append(line(X(cx1), Y(334), X(cx1), Y(piv_y + 2), INK, 3))
    b.append(t(X(174), Y(312), "vaso de espera", 12, "middle", INK, "bold"))
    b.append(t(X(174), Y(306), "40 × 40 × 40", 11, "middle", QUIET))
    # flap positions
    pv = (174, piv_y); half = 19
    def flap(ang, col, dash=None, w=4):
        dx, dy = half * cos(radians(ang)), half * sin(radians(ang))
        return line(X(pv[0] - dx), Y(pv[1] - dy), X(pv[0] + dx), Y(pv[1] + dy), col, w, dash)
    b.append(flap(0, INK, None, 5))
    b.append(flap(40, "#2e7d32", "6 4", 3))   # fondo arriba: resbala al frente
    b.append(flap(-40, DIM, "6 4", 3))       # frente arriba: resbala al fondo
    b.append(f"<circle cx='{X(pv[0])}' cy='{Y(pv[1])}' r='5' fill='white' stroke='{INK}' stroke-width='2'/>")
    b.append(t(X(cx0) - 10, Y(pv[1]) + 4, "eje del servo SG90", 11, "end", INK))
    # divider ridge (inverted V) under pivot
    ridge = (174, 266)
    fl = (122, 266 - 52 * math.tan(radians(33)))   # front floor end
    bl = (226, 266 - 52 * math.tan(radians(33)))   # back floor end
    b.append(line(*P(*ridge), *P(*fl), INK, 3))
    b.append(line(*P(*ridge), *P(*bl), INK, 3))
    b.append(t(X(174), Y(266) + 44, "cresta separadora", 11, "middle", INK, "bold"))
    b.append(t(X(174), Y(266) + 60, "justo bajo el eje", 11, "middle", QUIET))
    # chute walls continuing
    b.append(f"<line x1='{X(fl[0]):.1f}' y1='{Y(fl[1]):.1f}' x2='{X(104):.1f}' y2='{Y(fl[1]-18*math.tan(radians(33))):.1f}' stroke='#2e7d32' stroke-width='2' marker-end='url(#b)'/>")
    b.append(t(X(104), Y(fl[1] - 18 * math.tan(radians(33))) + 22, "a la bandeja", 12, "start", "#2e7d32", "bold"))
    b.append(t(X(104), Y(fl[1] - 18 * math.tan(radians(33))) + 38, "(rampa ≥ 30°)", 11, "start", QUIET))
    b.append(f"<line x1='{X(bl[0]):.1f}' y1='{Y(bl[1]):.1f}' x2='{X(244):.1f}' y2='{Y(bl[1]-18*math.tan(radians(33))):.1f}' stroke='{DIM}' stroke-width='2' marker-end='url(#a)'/>")
    b.append(t(X(244), Y(bl[1] - 18 * math.tan(radians(33))) + 22, "a la hucha", 12, "end", DIM, "bold"))
    # angle annotations
    b.append(arc(X(ridge[0]), Y(ridge[1]), 70, 180, 180 + 33))
    b.append(t(X(ridge[0]) - 80, Y(ridge[1]) + 4, "33°", 12, "end", DIM))
    b.append(arc(X(pv[0]), Y(pv[1]), 60, 0, 40))
    b.append(t(X(pv[0]) + 64, Y(pv[1]) - 26, "40°", 12, "start", DIM))
    # legend
    lx, ly = 60, 830
    items = [(INK, None, "RETENER: 1,5 ms, 0° (horizontal)"), ("#2e7d32", "6 4", "DEVOLVER: 40° con el fondo arriba"), (DIM, "6 4", "COBRAR: 40° con el frente arriba")]
    for i, (c, d, txt) in enumerate(items):
        b.append(line(lx, ly + i * 24, lx + 30, ly + i * 24, c, 4 if d is None else 3, d))
        b.append(t(lx + 40, ly + i * 24 + 4, txt, 12, "start", INK))
    # dims
    b.append(gp.hdim(X(cx0), X(cx1), Y(342), Y(334), "40"))
    b.append(gp.vdim(X(cx1) + 50, Y(piv_y), Y(ridge[1]), X(cx1), "16", False))
    b.append(t(X(cx1) + 58, Y(piv_y) + 52, "hueco eje–cresta", 11, "start", QUIET))
    b.append(t(24, 920, "La compuerta es el fondo del vaso y gira sobre su centro. Al inclinarse, las monedas resbalan por el borde bajo", 12, fill=QUIET))
    b.append(t(24, 938, "y caen a un lado u otro de la cresta: es imposible que una moneda de la devolución acabe en la hucha.", 12, fill=QUIET))
    open(f"{OUT}/6-compuerta.svg", "w").write(svg(760, 960, "".join(b), "Compuerta y rampas"))

angulos(); compuerta(); print("ok2")
