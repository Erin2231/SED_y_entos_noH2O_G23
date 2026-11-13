import math
INK="#222222"; Q="#6b6b6b"; RED="#8b1e1e"; BLU="#2f5d8a"; GRN="#3f6b4f"
F_WOOD="#e9e6e1"; F_PRT="#dfe3e8"; F_COIN="#d9dee5"; F_ELEC="#cfd9d2"; F_DRW="#f4f4f2"; F_PROD="#e6ddd2"; F_GLASS="#eef3f6"
H, W, D = 420, 330, 330      # alto, ancho, fondo (mm) sin la Nexys de arriba
T = 8                        # grosor de tablero (madera 8 mm o impreso)
class Sheet:
    def __init__(s, w, h, title, sub):
        s.w, s.h, s.o = w, h, []
        s.o.append(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' font-family='DejaVu Sans, Arial, sans-serif'>")
        s.o.append("<defs><marker id='ar' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='context-stroke'/></marker>"
                   "<marker id='ab' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='#2f5d8a'/></marker>"
                   "<marker id='ak' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='#1b1b1b'/></marker>"
                   "<marker id='ag' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='#3f6b4f'/></marker>"
                   "<marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='#8b1e1e'/></marker>"
                   "<pattern id='hat' width='6' height='6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><line x1='0' y1='0' x2='0' y2='6' stroke='#a8a29a' stroke-width='1.2'/></pattern></defs>")
        s.o.append(f"<rect width='{w}' height='{h}' fill='white'/>")
        s.txt(30, 42, title, 26, w="bold"); s.txt(30, 68, sub, 14, c=Q)
    def txt(s, x, y, t, sz=12, a="start", c=INK, w="normal"):
        s.o.append(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'>{t}</text>")
    def raw(s, x): s.o.append(x)
    def save(s, fn): open(fn, "w").write("\n".join(s.o + ["</svg>"]))

class View:
    """vista 2D: coordenadas de máquina (h, v) en mm -> px; v hacia arriba"""
    def __init__(s, sh, ox, oy, k, title):
        s.sh, s.ox, s.oy, s.k = sh, ox, oy, k
        sh.txt(ox, oy - H * k - 50, title, 16, w="bold")
    def P(s, h, v): return s.ox + h * s.k, s.oy - v * s.k
    def rect(s, h0, v0, h1, v1, fill="none", st=INK, sw=1.2, dash=None, rx=0):
        x0, y0 = s.P(h0, v1); x1, y1 = s.P(h1, v0)
        d = f" stroke-dasharray='{dash}'" if dash else ""
        s.sh.raw(f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{x1-x0:.1f}' height='{y1-y0:.1f}' rx='{rx}' fill='{fill}' stroke='{st}' stroke-width='{sw}'{d}/>")
    def poly(s, pts, fill="none", st=INK, sw=1.2, close=True, dash=None, mk=None):
        p = " ".join("%.1f,%.1f" % s.P(*q) for q in pts)
        d = f" stroke-dasharray='{dash}'" if dash else ""
        m = f" marker-end='url(#{mk})'" if mk else ""
        tag = "polygon" if close else "polyline"
        s.sh.raw(f"<{tag} points='{p}' fill='{fill}' stroke='{st}' stroke-width='{sw}'{d}{m}/>")
    def circ(s, h, v, r, fill="none", st=INK, sw=1.2):
        x, y = s.P(h, v); s.sh.raw(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r*s.k:.1f}' fill='{fill}' stroke='{st}' stroke-width='{sw}'/>")
    def t(s, h, v, txt, sz=11, a="middle", c=INK, w="normal"):
        x, y = s.P(h, v); s.sh.txt(x, y, txt, sz, a, c, w)
    def lbl(s, h, v, th, tv, txt, sz=11, a="start", c=INK):
        x0, y0 = s.P(h, v); x1, y1 = s.P(th, tv)
        s.sh.raw(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x0:.1f}' y2='{y0:.1f}' stroke='{c}' stroke-width='0.8'/>")
        s.sh.raw(f"<circle cx='{x0:.1f}' cy='{y0:.1f}' r='2' fill='{c}'/>")
        for i, l in enumerate(txt.split("|")):
            s.sh.txt(x1 + (3 if a == "start" else -3), y1 - 3 + i * (sz + 2), l, sz, a, c)
    def dimv(s, h, v0, v1, txt, side=1):
        x, y0 = s.P(h, v0); _, y1 = s.P(h, v1)
        s.sh.raw(f"<line x1='{x:.1f}' y1='{y0:.1f}' x2='{x:.1f}' y2='{y1:.1f}' stroke='{RED}' stroke-width='0.9' marker-start='url(#arr)' marker-end='url(#arr)'/>")
        s.sh.raw(f"<text x='{x+4*side:.1f}' y='{(y0+y1)/2:.1f}' font-size='11' fill='{RED}' text-anchor='{'start' if side>0 else 'end'}'>{txt}</text>")
    def dimh(s, v, h0, h1, txt, off=14):
        x0, y = s.P(h0, v); x1, _ = s.P(h1, v)
        s.sh.raw(f"<line x1='{x0:.1f}' y1='{y:.1f}' x2='{x1:.1f}' y2='{y:.1f}' stroke='{RED}' stroke-width='0.9' marker-start='url(#arr)' marker-end='url(#arr)'/>")
        s.sh.txt((x0 + x1) / 2, y + off, txt, 11, "middle", RED)
    def level(s, v, h0, h1, txt):
        x0, y = s.P(h0, v); x1, _ = s.P(h1, v)
        s.sh.raw(f"<line x1='{x0:.1f}' y1='{y:.1f}' x2='{x1:.1f}' y2='{y:.1f}' stroke='{RED}' stroke-width='0.8'/>")
        s.sh.txt(x1 + 3, y + 4, txt, 10.5, "start", RED)

# ---------- cotas clave (de modelo.py y de la pila calculada) ----------
RAIL = dict(y0=0, y1=158, z_in=352, z_out=326, top=398, low=312)   # carril A en la máquina
B = dict(y0=139.7, y1=185.7, z0=276.0, z1=316.0, piv=284.0)
C = dict(y0=200.0, y1=246.0, z0=183.0, z1=223.0, piv=191.0)          # depósito C = cubilete B (40 de alto), máx. 10 monedas
DEV = dict(y0=T, y1=75, z0=T, z1=65)                                  # cajón devolución
HUC = dict(y0=255, y1=D - T, z0=T, z1=65)                             # hucha (sale por detrás)
PROD_DRW = dict(z1=95)
COL_W = 110                                                           # columna de monedas (interior)
X_DIV = T + COL_W                                                     # tabique columna / productos
LCD = dict(z0=284, z1=320, w=80, d=14)
PAD = dict(z0=200, z1=277, w=70)
BTN = dict(z=176, d=12)
SH1, SH2 = 110, 255                                                   # estantes (cara de arriba)
WIN = dict(z0=105, z1=400)

def corte_monedas(sh, ox, oy, k):
    v = View(sh, ox, oy, k, "1 · Corte lateral por la columna de monedas")
    # carcasa
    v.rect(0, 0, D, T, "url(#hat)"); v.rect(0, H - T, D, H, "url(#hat)")
    v.rect(0, T, T, H - T, F_WOOD)                       # frontal
    v.rect(D - T, T, D, H - T, F_WOOD, dash="5 3")       # trasera en guías
    v.lbl(D - T / 2, 200, D - 15, 160, "trasera|en guías", 10, "end", Q)
    sh.txt(*v.P(D - 2, H / 2 - 14), "", 1)
    # carril A
    v.poly([(0, RAIL["low"] + 30), (RAIL["y1"], RAIL["low"]), (RAIL["y1"] - 8, RAIL["top"] - 26), (0, RAIL["top"])], F_COIN)
    v.poly([(4, RAIL["z_in"]), (152, RAIL["z_out"])], st=BLU, sw=2, close=False)
    for i in range(7):
        y = 20 + i * 19; v.circ(y, RAIL["z_in"] - y * math.tan(math.radians(10)) + 6, 2.2, "#2f5d8a", "none")
    v.lbl(70, 372, 120, 395, "carril A · 150 mm a 10°|7 barreras IR (P1, B1-B5, P2)")
    x, y = v.P(-30, 366); x2, y2 = v.P(6, 362)
    sh.raw(f"<line x1='{x}' y1='{y}' x2='{x2}' y2='{y2}' stroke='{BLU}' stroke-width='1.6' marker-end='url(#ab)'/>")
    v.t(-32, 372, "monedas", 11, "end", BLU)
    # B
    v.rect(B["y0"], B["z0"], B["y1"], B["z1"], F_COIN); v.poly([(B["y0"] + 1, B["piv"] + 3), (B["y1"] - 1, B["piv"] + 3)], st=INK, sw=2.5, close=False)
    v.t((B["y0"] + B["y1"]) / 2, B["z1"] - 13, "B", 12, w="bold"); v.t((B["y0"] + B["y1"]) / 2, B["z1"] - 25, "válido", 9.5, c=Q)
    ax = (B["y0"] + B["y1"]) / 2; az = B["piv"] - 28        # 20 de paso bajo B
    TG = math.tan(math.radians(30))
    v.poly([(128, az - (ax - 128) * TG), (ax, az), (200, az - (200 - ax) * TG)], st=INK, sw=2, close=False)
    # canal de no válidas (34 de ancho, paso 28)
    v.poly([(128, az - (ax - 128) * TG), (128, 137)], st=INK, sw=1.5, close=False)
    v.poly([(100, 262), (100, 118)], st=INK, sw=1.5, close=False)
    v.poly([(140, 250), (114, 236), (114, 112)], st=RED, sw=1.3, close=False, dash="4 3", mk="arr")
    v.lbl(114, 175, 40, 150, "no|válidas", 10, "start", RED)
    # C
    v.rect(C["y0"], C["z0"], C["y1"], C["z1"], F_COIN); v.poly([(C["y0"] + 1, C["piv"] + 3), (C["y1"] - 1, C["piv"] + 3)], st=INK, sw=2.5, close=False)
    v.t((C["y0"] + C["y1"]) / 2, C["z1"] - 13, "C", 12, w="bold"); v.t((C["y0"] + C["y1"]) / 2, C["z1"] - 25, "escrow", 9.5, c=Q)
    v.poly([(ax + 6, az - 22), (ax + 41, az - 24)], st=GRN, sw=1.3, close=False, dash="4 3", mk="ag")
    cx = (C["y0"] + C["y1"]) / 2; cz = C["z0"] - 20          # 20 de paso bajo C
    v.poly([(70, cz - (cx - 70) * TG), (cx, cz), (280, cz - (280 - cx) * TG)], st=INK, sw=2, close=False)
    v.poly([(cx - 20, cz - 22), (cx - 60, cz - 47)], st=RED, sw=1.3, close=False, dash="4 3", mk="arr")
    v.poly([(cx + 14, cz - 16), (cx + 40, cz - 33)], st=GRN, sw=1.3, close=False, dash="4 3", mk="ag")
    v.lbl(cx - 40, cz - 25, 150, 132, "rampas 30°", 10)
    # cajones
    v.rect(75, T, 80, T + 10, "#9aa6b2"); v.rect(250, T, 255, T + 10, "#9aa6b2")   # topes
    v.rect(DEV["y0"] - T, DEV["z0"], DEV["y1"], DEV["z1"], F_DRW, rx=2); v.t(50, 40, "devolución", 10); v.t(50, 28, "y cambio", 10)
    v.rect(HUC["y0"], HUC["z0"], HUC["y1"] + T, HUC["z1"], F_DRW, rx=2); v.t((HUC["y0"] + HUC["y1"]) / 2, 50, "hucha", 11, w="bold"); v.t((HUC["y0"] + HUC["y1"]) / 2, 36, "por detrás", 9.5, c=Q)
    # frontal: pantalla, numpad, botón
    v.rect(T, LCD["z0"], T + LCD["d"], LCD["z1"], F_ELEC); v.lbl(T + 13, (LCD["z0"] + LCD["z1"]) / 2, -40, 320, "LCD 16×2", 10.5, "end")
    v.rect(T, PAD["z0"], T + 6, PAD["z1"], F_ELEC); v.lbl(T + 3, 240, -40, 245, "numpad 3×4", 10.5, "end")
    v.rect(-6, BTN["z"] - 6, T + 18, BTN["z"] + 6, "#9a4a4a", rx=3); v.lbl(-4, BTN["z"], -40, 180, "cancelar", 10.5, "end")
    v.lbl(-2, 40, -40, 70, "cajón a ras|(muesca para el dedo)", 10, "end")
    # placa arriba
    v.rect(200, H, 290, H + 14, "#e3dccb"); v.t(245, H + 4, "placa hija 2", 9)
    x, y = v.P(300, H + 8); x2, y2 = v.P(D + 30, H + 8)
    sh.raw(f"<line x1='{x}' y1='{y}' x2='{x2}' y2='{y2}' stroke='{INK}' stroke-width='1' marker-end='url(#ak)'/>"); v.t(D + 32, H + 4, "USB + 5 V", 10, "start")
    v.poly([(290, H - T), (290, 340)], st=GRN, sw=1, close=False, dash="2 3"); v.t(286, 360, "cables", 9.5, "end", GRN)
    # cotas
    v.dimv(D + 120, 0, H, f"alto {H}", 1); v.dimh(-28, 0, D, f"fondo {D}", 14)
    for z, t in ((352, "352 entrada monedas"), (316, "316 cubilete B"), (223, "223 escrow C"), (65, "65 cajones")):
        v.level(z, D, D + 8, t)
    sh.txt(*v.P(-40, -48), "", 1)
    return v

def corte_productos(sh, ox, oy, k):
    v = View(sh, ox, oy, k, "2 · Corte lateral por los productos")
    v.rect(0, 0, D, T, "url(#hat)"); v.rect(0, H - T, D, H, "url(#hat)")
    v.rect(0, T, T, WIN["z0"], F_WOOD); v.rect(0, WIN["z1"], T, H - T, F_WOOD)
    v.rect(0, WIN["z0"], 3, WIN["z1"], F_GLASS, st=BLU, dash="4 3"); v.lbl(1, 300, -40, 330, "ventana|(metacrilato|opcional)", 10, "end", BLU)
    v.rect(D - T, T, D, H - T, F_WOOD, dash="5 3")
    for zs, nums in ((SH2, "1 · 2"), (SH1, "3 · 4")):
        v.rect(60, zs - 6, D - T, zs, "url(#hat)")
        v.rect(66, zs, 166, zs + 100, F_PROD, rx=3); v.t(116, zs + 46, "producto", 10); v.t(116, zs + 32, nums, 10, c=Q)
        v.rect(175, zs + 30, 205, zs + 52, "#b8c4d0"); v.t(190, zs + 38, "SG90", 8.5)
        v.poly([(175, zs + 41), (168, zs + 41)], st=INK, sw=2.5, close=False)
        x, y = v.P(172, zs + 60); x2, y2 = v.P(140, zs + 60)
        sh.raw(f"<line x1='{x}' y1='{y}' x2='{x2}' y2='{y2}' stroke='{RED}' stroke-width='1.2' marker-end='url(#arr)'/>")
    v.lbl(205, SH2 + 41, 310, SH2 + 128, "empujador o trampilla|(1 SG90 por producto)", 10, "end")
    v.poly([(40, SH2 - 10), (40, PROD_DRW["z1"] + 6)], st=RED, sw=1.3, close=False, dash="4 3", mk="arr")
    v.lbl(40, 180, -10, 160, "caída por|delante", 10, "end")
    v.rect(0, T, 250, PROD_DRW["z1"], F_DRW, rx=2); v.t(125, 50, "cajón de recogida", 11, w="bold"); v.t(125, 36, "apoyado en el suelo, a ras del frontal", 9.5, c=Q)
    v.rect(255, T, D - T, 80, "none", dash="4 3"); v.t(291, 44, "hueco libre", 9.5, c=Q); v.t(291, 31, "(fuente)", 9.5, c=Q)
    v.rect(60, H, 115, H + 14, "#e3dccb"); v.rect(195, H, 315, H + 18, "#b9c9bd"); v.t(255, H + 5, "Nexys", 9.5)
    v.dimv(D + 120, 0, H, f"alto {H}", 1)
    for z, t in ((SH2, f"{SH2} estante 1-2"), (SH1, f"{SH1} estante 3-4"), (95, "95 cajón")):
        v.level(z, D, D + 8, t)
    return v

def frontal(sh, ox, oy, k):
    v = View(sh, ox, oy, k, "3 · Frontal")
    v.rect(0, 0, W, H, F_WOOD, sw=1.6)
    v.rect(X_DIV, WIN["z0"], W - T - 5, WIN["z1"], F_GLASS, st=BLU)
    cx = T + COL_W / 2
    # columna de monedas
    v.rect(20, 357, 23.4, 382, "#333"); v.lbl(22, 375, 60, 395, "ranura monedas", 10)
    v.rect(cx - LCD["w"] / 2, LCD["z0"], cx + LCD["w"] / 2, LCD["z1"], "#3d4a40", rx=2); v.rect(cx - 33, LCD["z0"] + 8, cx + 33, LCD["z1"] - 8, "#8fa596"); v.t(cx, (LCD["z0"] + LCD["z1"]) / 2 - 3, "LCD 16×2", 9.5)
    v.rect(cx - PAD["w"] / 2, PAD["z0"], cx + PAD["w"] / 2, PAD["z1"], "#eceff1", rx=3)
    keys = "123456789*0#"
    for i, ch in enumerate(keys):
        r, c = divmod(i, 3); kx = cx - 22 + c * 22; kz = PAD["z1"] - 13 - r * 18
        v.rect(kx - 8, kz - 6, kx + 8, kz + 8, "white", rx=2); v.t(kx, kz - 2, ch, 9)
    v.circ(cx, BTN["z"], BTN["d"] / 2, "#9a4a4a"); v.t(cx + 14, BTN["z"] - 3, "cancelar", 10, "start")
    v.rect(T + 3, T, T + 107, 65, F_DRW, rx=2); v.rect(cx - 10, 57, cx + 10, 65, "white", rx=3); v.t(cx, 28, "devolución", 10)
    # productos
    for zs, a, b in ((SH2, "1", "2"), (SH1, "3", "4")):
        v.rect(X_DIV + 8, zs - 3, W - T - 13, zs, "#8a8178")
        for i, n in enumerate((a, b)):
            x0 = X_DIV + 18 + i * 95
            v.rect(x0, zs, x0 + 75, zs + 100, F_PROD, rx=3); v.t(x0 + 37, zs + 45, n, 22, w="bold")
    v.rect(X_DIV + 10, T + 2, W - T - 10, PROD_DRW["z1"], F_DRW, rx=2); v.rect((X_DIV + W) / 2 - 15, 82, (X_DIV + W) / 2 + 15, 95, "white", rx=4)
    v.t((X_DIV + W) / 2, 40, "salida de productos (cajón)", 10)
    v.poly([(X_DIV, T), (X_DIV, H - T)], st=INK, sw=0.8, close=False, dash="3 3")
    v.dimh(-16, 0, W, f"ancho {W}"); v.dimh(H + 14, 0, X_DIV, f"monedas {COL_W}", -6); v.dimh(H + 14, X_DIV, W, f"productos {W - X_DIV - T}", -6)
    v.dimv(-16, 0, H, f"{H}", -1)
    return v

def superior(sh, ox, oy, k):
    v = View(sh, ox, oy, k, "4 · Superior (techo)")
    # aquí h = X (ancho), v = Y (fondo), frontal abajo
    sh_v = v
    v.rect(0, 0, W, D, F_WOOD, sw=1.6)
    v.rect(T, T, X_DIV, D - T, "url(#hat)", st="none"); v.t(T + COL_W / 2, 30, "monedas debajo", 9.5, c=Q)
    v.rect(185, 195, 315, 315, "#b9c9bd", st=GRN, sw=1.5); v.t(250, 262, "Nexys 4 DDR", 12, w="bold"); v.t(250, 246, "130 × 120", 10, c=Q)
    v.rect(200, 315, 215, 331, "#555"); v.rect(240, 317, 252, 331, "#555")
    v.t(250, 338, "USB y jack hacia atrás", 10, c=GRN)
    v.rect(140, 60, 305, 115, "#e3dccb", st=INK); v.t(222, 90, "protoboard 165 × 55", 10); v.t(222, 76, "(luego placa soldada)", 9, c=Q)
    v.rect(20, 200, 110, 290, "#e3dccb", st=INK, dash="4 3"); v.t(65, 248, "placa hija 2", 10); v.t(65, 235, "(servos)", 9, c=Q)
    v.rect(140, 140, 175, 147, "#555"); v.t(140, 152, "paso de cables", 9.5, "start")
    v.t(W / 2, -16, "frontal", 11, c=Q)
    v.dimh(-36, 0, W, f"{W}", 14); v.dimv(W + 14, 0, D, f"{D}", 1)
    return v

def iso(sh, ox, oy, k):
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    def P(x, y, z): return ox + (x + y) * c30 * k, oy - (z + (y - x) * s30) * k
    def face(pts, fill, st=INK, sw=1.2, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        sh.raw("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%s'%s/>" % (" ".join("%.1f,%.1f" % P(*p) for p in pts), fill, st, sw, d))
    sh.txt(ox, oy - (H + D * s30) * k - 30, "5 · Isométrica", 16, w="bold")
    face([(0, 0, 0), (W, 0, 0), (W, 0, H), (0, 0, H)], F_WOOD)
    face([(W, 0, 0), (W, D, 0), (W, D, H), (W, 0, H)], "#d9d5cf")
    face([(0, 0, H), (W, 0, H), (W, D, H), (0, D, H)], "#f2f0ec")
    fr = lambda x0, z0, x1, z1, f, **kw: face([(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], f, **kw)
    fr(X_DIV, WIN["z0"], W - T - 5, WIN["z1"], F_GLASS, st=BLU)
    for zs in (SH2, SH1):
        for i in range(2):
            x0 = X_DIV + 18 + i * 95; fr(x0, zs, x0 + 75, zs + 100, F_PROD)
    cx = T + COL_W / 2
    fr(20, 357, 23.4, 382, "#333"); fr(cx - 40, LCD["z0"], cx + 40, LCD["z1"], "#3d4a40"); fr(cx - 35, PAD["z0"], cx + 35, PAD["z1"], "#eceff1")
    fr(cx - 6, BTN["z"] - 6, cx + 6, BTN["z"] + 6, "#9a4a4a")
    fr(T + 3, T, T + 107, 65, F_DRW); fr(X_DIV + 10, T + 2, W - T - 10, 95, F_DRW)
    tp = lambda x0, y0, x1, y1, f, z=H: face([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], f)
    tp(185, 195, 315, 315, "#b9c9bd"); tp(140, 60, 305, 115, "#e3dccb"); tp(20, 200, 110, 290, "#e3dccb")
    x, y = P(250, 255, H); sh.txt(x, y + 4, "Nexys", 10.5, "middle", INK, "bold")

K = 1.0   # misma escala (px por mm) en todas las vistas
sh = Sheet(1414, 2000, "Máquina expendedora · bocetos generales (v2)",
           f"Misma escala en todas las vistas · cotas aproximadas en mm · {W} ancho × {D} fondo × {H} alto (+ Nexys encima) · tableros de {T} mm")
corte_monedas(sh, 190, 560, K)
corte_productos(sh, 880, 560, K)
frontal(sh, 190, 1110, K)
superior(sh, 880, 1060, K)
iso(sh, 120, 1810, K)
notas = ["Notas",
 "· El alto lo fija la pila de monedas: 352 → 316 → 223 → 65.",
 "· Rampas a 30-33° bajo B y bajo C (crestas en Λ).",
 "· No válidas: canal junto al frontal → rampa de C → devolución.",
 "· Productos de hasta 75 × 100 × 100; caen por delante al cajón.",
 "· Cajones a ras, con muesca, sin bisagras ni imanes.",
 "· Hucha por la trasera. Nexys al aire, puertos hacia atrás.",
 "· Carril A y cubilete B: cotas del modelo. Resto aproximado."]
for i, n in enumerate(notas):
    sh.txt(760, 1300 + i * 26, n, 15 if i == 0 else 12.5, c=INK if i == 0 else Q, w="bold" if i == 0 else "normal")
leg = [(F_COIN, "monedas (A, B, C)"), (F_DRW, "cajones"), (F_PROD, "productos"), (F_ELEC, "electrónica"), (F_WOOD, "carcasa"), (F_GLASS, "ventana")]
for i, (c, n) in enumerate(leg):
    y = 1540 + i * 26
    sh.raw(f"<rect x='760' y='{y}' width='22' height='14' fill='{c}' stroke='{INK}' stroke-width='0.8'/>"); sh.txt(790, y + 12, n, 12.5)
sh.save("bocetos.svg")
