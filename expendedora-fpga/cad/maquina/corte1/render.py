import json, math
r = json.load(open("corte1.json")); ref = json.load(open("ref.json"))
PW, PH = 297.0, 420.0
S = 0.5
OX, OY = 34.0, 237.0
H, D, T = 420, 330, 8
X = lambda d: OX + d * S
Y = lambda h: OY - h * S
FX = 222.0                                   # vista frontal: lateral 0 en la hoja
L = lambda u: FX + u * S
INK = "#222"; Q = "#666"; RED = "#8b1e1e"; BLU = "#2f5d8a"
def f1(v): s = f"{v:.1f}".rstrip("0").rstrip("."); return s.replace(".", ",")
o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{PW}mm' height='{PH}mm' viewBox='0 0 {PW} {PH}' font-family='DejaVu Sans, Arial, sans-serif'>",
     "<defs>"
     "<pattern id='hm' width='1.6' height='1.6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='1.6' height='1.6' fill='#d3dae3'/><line x1='0' y1='0' x2='0' y2='1.6' stroke='#5b6b80' stroke-width='0.18'/></pattern>"
     "<pattern id='hw' width='2.2' height='2.2' patternUnits='userSpaceOnUse' patternTransform='rotate(-45)'><rect width='2.2' height='2.2' fill='#ebe7e1'/><line x1='0' y1='0' x2='0' y2='2.2' stroke='#a39886' stroke-width='0.18'/></pattern>"
     "<pattern id='hp' width='2' height='2' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='2' height='2' fill='#f3f3f3'/><line x1='0' y1='0' x2='0' y2='2' stroke='#b5b5b5' stroke-width='0.15'/></pattern>"
     f"<marker id='m' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{RED}'/></marker>"
     f"<marker id='mb' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{BLU}'/></marker>"
     "</defs>", f"<rect width='{PW}' height='{PH}' fill='white'/>",
     f"<rect x='8' y='8' width='{PW-16}' height='{PH-16}' fill='none' stroke='{INK}' stroke-width='0.5'/>"]
def txt(x, y, t, sz=2.4, a="start", c=INK, w="normal", rot=None):
    tr = f" transform='rotate({rot} {x:.2f} {y:.2f})'" if rot is not None else ""
    o.append(f"<text x='{x:.2f}' y='{y:.2f}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'{tr}>{t}</text>")
def line(x0, y0, x1, y1, c=INK, w=0.2, dash=None, mk=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""; m = f" marker-start='url(#{mk})' marker-end='url(#{mk})'" if mk else ""
    o.append(f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{c}' stroke-width='{w}'{d}{m}/>")
def rect(x0, y0, x1, y1, fill="none", st=INK, w=0.25, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    o.append(f"<rect x='{min(x0,x1):.2f}' y='{min(y0,y1):.2f}' width='{abs(x1-x0):.2f}' height='{abs(y1-y0):.2f}' fill='{fill}' stroke='{st}' stroke-width='{w}'{d}/>")
def spread(vals, gap):
    """vals: lista de posiciones (ordenada); devuelve posiciones separadas al menos gap, centradas en lo posible"""
    p = list(vals)
    for _ in range(200):
        moved = False
        for i in range(len(p) - 1):
            if p[i + 1] - p[i] < gap:
                d = (gap - (p[i + 1] - p[i])) / 2; p[i] -= d; p[i + 1] += d; moved = True
        if not moved: break
    return p

# ================= SECCIÓN =================
STY = {"modelo": ("url(#hm)", INK, 0.3, None), "previsto": ("url(#hp)", "#555", 0.25, "1.2 0.6"),
       "carcasa": ("url(#hw)", "#444", 0.25, None), "comprado": ("#53675a", "#222", 0.25, None)}
ORDER = ["suelo", "techo", "frontal", "trasera", "cajón devolución", "hucha", "topes", "canal", "Λ-B", "Λ-C", "C", "C-TP",
         "B", "B-TP", "A", "A-T", "LCD placa", "LCD conectores", "LCD bisel", "numpad", "soporte pulsador", "pulsador", "embellecedor"]
for n in ORDER:
    grp, faces, yc = r[n]; fill, st, sw, dash = STY[grp]
    fill = {"LCD bisel": "#2e3a31", "numpad": "#cfcfcf", "soporte pulsador": "url(#hm)", "pulsador": "#444", "embellecedor": "#8a3b3b"}.get(n, fill)
    for f in faces:
        d = " ".join("M" + " L".join(f"{X(p[0]):.2f},{Y(p[1]):.2f}" for p in w) + " Z" for w in f)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        o.append(f"<path d='{d}' fill='{fill}' fill-rule='evenodd' stroke='{st}' stroke-width='{sw}'{da} stroke-linejoin='round'/>")
for f in r["A-F"][1]:
    d = "M" + " L".join(f"{X(p[0]):.2f},{Y(p[1]):.2f}" for p in f[0]) + " Z"
    o.append(f"<path d='{d}' fill='none' stroke='#5b6b80' stroke-width='0.2' stroke-dasharray='0.8 0.5'/>")
bp, cp = ref["B_PIV"], ref["C_PIV"]
for (x, z) in (bp, cp):
    line(X(x) - 3, Y(z), X(x) + 3, Y(z), "#888", 0.12, "2 0.6 0.4 0.6"); line(X(x), Y(z) - 3, X(x), Y(z) + 3, "#888", 0.12, "2 0.6 0.4 0.6")
def flecha(pts, c=BLU):
    p = " ".join(f"{X(a):.2f},{Y(b):.2f}" for a, b in pts)
    o.append(f"<polyline points='{p}' fill='none' stroke='{c}' stroke-width='0.3' stroke-dasharray='1.2 0.8' marker-end='url(#{'mb' if c == BLU else 'm'})'/>")
flecha([(176, 247), (208, 229)]); flecha([(150, 247), (114, 226), (114, 140)], "#8b1e1e")
flecha([(237, 154), (268, 136), (268, 100)]); flecha([(208, 150), (110, 92), (52, 70)], "#8b1e1e")

# ---- puntos de referencia (coordenadas en tabla) ----
tg = math.tan(math.radians(ref["ANG"]))
LB, LC = ref["LB"], ref["LC"]; (b0, b1), (c0, c1) = ref["LB_X"], ref["LC_X"]
FIN = ref["FIN"]
cf, cb = ref["CAN"]["f"], ref["CAN"]["b"]
PTS = [("p1", "suelo del carril A, entrada", 4.0, 352.0, (-14, 8)),
       ("p2", "suelo del carril A al final", FIN[0], FIN[1], (-10, 8)),
       ("p3", "eje de la trampilla de B", bp[0], bp[1], (12, 6)),
       ("p4", "vértice de Λ-B (cara de arriba)", LB[0], LB[1], (10, -3)),
       ("p5", "extremo delantero de Λ-B", b0, LB[1] - (LB[0] - b0) * tg, (-8, 6)),
       ("p6", "extremo trasero de Λ-B", b1, LB[1] - (b1 - LB[0]) * tg, (8, 8)),
       ("p7", "eje de la trampilla de C", cp[0], cp[1], (14, 4)),
       ("p8", "vértice de Λ-C (cara de arriba)", LC[0], LC[1], (12, -6)),
       ("p9", "extremo delantero de Λ-C", c0, LC[1] - (LC[0] - c0) * tg, (2, 14)),
       ("p10", "extremo trasero de Λ-C", c1, LC[1] - (c1 - LC[0]) * tg, (2, 14))]
for k, desc, x, z, (dx, dz) in PTS:
    o.append(f"<circle cx='{X(x):.2f}' cy='{Y(z):.2f}' r='0.6' fill='{RED}'/>")
    tx, ty = X(x + dx), Y(z + dz); line(X(x), Y(z), tx, ty, RED, 0.12)
    o.append(f"<rect x='{tx-3.2:.2f}' y='{ty-1.7:.2f}' width='6.4' height='3.4' rx='0.6' fill='white' stroke='{RED}' stroke-width='0.2'/>")
    txt(tx, ty + 0.85, k, 2.2, "middle", RED, "bold")

# ---- cotas generales de la sección ----
def cotah(z, x0, x1, t, dy=-1.0, ext=None):
    line(X(x0), Y(z), X(x1), Y(z), RED, 0.18, mk="m"); txt((X(x0) + X(x1)) / 2, Y(z) + dy, t, 2.3, "middle", RED)
def cotav_s(xs, y0, y1, t):
    line(xs, y0, xs, y1, RED, 0.18, mk="m"); txt(xs - 1.0, (y0 + y1) / 2, t, 2.3, "middle", RED, rot=-90)
# 330 abajo, 420 izquierda
line(X(0), Y(0), X(0), Y(-16), RED, 0.12); line(X(D), Y(0), X(D), Y(-16), RED, 0.12)
cotah(-14, 0, D, "330", -1.0)
cotah(-6, 0, 75, "75", -1.0); cotah(-6, 255, D, "75", -1.0)
line(X(75), Y(8), X(75), Y(-8), RED, 0.12); line(X(255), Y(8), X(255), Y(-8), RED, 0.12)
line(X(0), Y(0), X(-26), Y(0), RED, 0.12); line(X(0), Y(H), X(-26), Y(H), RED, 0.12)
cotav_s(X(-24), Y(0), Y(H), "420")
line(X(0), Y(65), X(-12), Y(65), RED, 0.12); line(X(0), Y(67), X(-6), Y(67), RED, 0.12)
cotav_s(X(-10), Y(8), Y(65), "57"); cotav_s(X(-16), Y(0), Y(8), "8")
line(X(-1), Y(8), X(-18), Y(8), RED, 0.12)
# ángulos
def arco(cx, cz, a0, a1, rr, t, tx, tz):
    p0 = (X(cx) + rr * math.cos(math.radians(a0)), Y(cz) - rr * math.sin(math.radians(a0)))
    p1 = (X(cx) + rr * math.cos(math.radians(a1)), Y(cz) - rr * math.sin(math.radians(a1)))
    o.append(f"<path d='M{p0[0]:.2f},{p0[1]:.2f} A{rr},{rr} 0 0 0 {p1[0]:.2f},{p1[1]:.2f}' fill='none' stroke='{RED}' stroke-width='0.15'/>")
    txt(X(tx), Y(tz), t, 2.2, "middle", RED)
x9 = c0; z9 = LC[1] - (LC[0] - c0) * tg
line(X(x9), Y(z9), X(x9 + 40), Y(z9), RED, 0.12, "1 0.6"); arco(x9, z9, 0, 30, 14, "30°", x9 + 34, z9 + 6)
x6 = b1; z6 = LB[1] - (b1 - LB[0]) * tg
line(X(x6), Y(z6), X(x6 - 24), Y(z6), RED, 0.12, "1 0.6"); arco(x6, z6, 150, 180, 9, "30°", x6 - 21, z6 + 4.5)
# ángulo del carril
line(X(4), Y(352), X(60), Y(352), RED, 0.12, "1 0.6"); arco(4, 352, -10, 0, 40, "10°", 88, 345)
# canal: cotas
line(X(cf[0]), Y(cf[3]), X(cf[0]), Y(cf[3] + 12), RED, 0.12); line(X(cb[1]), Y(cb[3]), X(cb[1]), Y(cf[3] + 12), RED, 0.12)
cotah(cf[3] + 10, cf[0], cb[1], "34", -1.0)
line(X(cf[1]), Y(cf[3]), X(cf[1]), Y(cf[3] + 6), RED, 0.12); line(X(cb[0]), Y(cb[3]), X(cb[0]), Y(cf[3] + 6), RED, 0.12)
cotah(cf[3] + 4, cf[1], cb[0], "28 paso", -1.0)
# C: 46 x 70
cotav_s(X(268), Y(183), Y(223), "40")
line(X(262), Y(183), X(270), Y(183), RED, 0.12); line(X(262), Y(223), X(270), Y(223), RED, 0.12)
# paso de 20 bajo cada cubilete (fondo del cubilete - vértice de la cresta)
for xv, z1, z0 in ((ref["LB"][0], 276.0, ref["LB"][1]), (ref["LC"][0], 183.0, ref["LC"][1])):
    line(X(xv) - 2, Y(z1), X(xv) - 2, Y(z0), RED, 0.15, mk="m"); txt(X(xv) - 3.2, (Y(z1) + Y(z0)) / 2 + 0.8, "20", 2.1, "end", RED)

# ---- globos de piezas ----
G = [(1, (70, 372), (50, 408)), (2, (100, 378), (110, 408)), (3, (140, 340), (160, 352)), (4, (142, 300), (122, 300)),
     (5, (178, 279), (196, 292)), (6, (244, 212), (285, 217)), (7, (236, 188), (285, 182)), (8, (190, 238.5), (200, 262)),
     (9, (180, 135), (190, 118)), (10, (98, 200), (82, 210)), (11, (40, 40), (40, 90)), (12, (290, 40), (300, 90)),
     (13, (5, 302), (25, 302)), (14, (-0.5, 240), (25, 245)), (15, (-1.5, 176), (28, 166)), (16, (4, 140), (25, 140)),
     (17, (326, 250), (305, 260)), (18, (160, 4), (160, 24)), (20, (77.5, 13), (95, 30)), (19, (200, 416), (230, 432))]
for n, (px, pz), (bx, bz) in G:
    line(X(px), Y(pz), X(bx), Y(bz), INK, 0.15)
    o.append(f"<circle cx='{X(px):.2f}' cy='{Y(pz):.2f}' r='0.45' fill='{INK}'/>")
    o.append(f"<circle cx='{X(bx):.2f}' cy='{Y(bz):.2f}' r='2.3' fill='white' stroke='{INK}' stroke-width='0.25'/>"); txt(X(bx), Y(bz) + 0.9, str(n), 2.5, "middle", w="bold")
txt(X(D / 2), Y(H) - 3, "SECCIÓN 1-1 (quebrada)  ·  1:2", 3.0, "middle", w="bold")

# ================= VISTA FRONTAL DE LA COLUMNA (pieza 16) =================
txt(L(55), Y(H) - 7, "FRONTAL (16) · 1:2", 3.0, "middle", w="bold"); txt(L(55), Y(H) - 3.5, "zona de la columna, visto desde fuera", 2.0, "middle", Q)
o.append(f"<path d='M{L(0):.2f},{Y(8):.2f} L{L(0):.2f},{Y(412):.2f} L{L(118):.2f},{Y(412):.2f} L{L(118):.2f},{Y(8):.2f} Z' fill='url(#hw)' stroke='#444' stroke-width='0.3'/>")
for zz in (300, 120):
    o.append(f"<path d='M{L(116):.2f},{Y(zz+6):.2f} L{L(118):.2f},{Y(zz+2):.2f} L{L(114):.2f},{Y(zz-2):.2f} L{L(118):.2f},{Y(zz-6):.2f}' fill='none' stroke='#444' stroke-width='0.2'/>")
def hole(u0, u1, z0, z1): rect(L(u0), Y(z0), L(u1), Y(z1), "white", INK, 0.25)
hole(2, 108, 8, 67)          # cajón
hole(0, 28.5, 339.5, 398.5)  # placa A
hole(19.5, 90.5, 290, 314)   # LCD
for u in (17.5, 92.5):
    for z in (286.5, 317.5): o.append(f"<circle cx='{L(u):.2f}' cy='{Y(z):.2f}' r='{1.6*S:.2f}' fill='white' stroke='{INK}' stroke-width='0.2'/>")
o.append(f"<circle cx='{L(55):.2f}' cy='{Y(176):.2f}' r='{6*S:.2f}' fill='white' stroke='{INK}' stroke-width='0.25'/>")
rect(L(20), Y(200), L(90), Y(277), "none", "#777", 0.2, "1.5 0.8"); txt(L(55), Y(240), "teclado 3×4", 2.0, "middle", Q); txt(L(55), Y(236), "(adhesivo)", 2.0, "middle", Q)
# ejes de simetría
line(L(55), Y(160), L(55), Y(330), "#888", 0.12, "3 0.8 0.5 0.8")
# pared lateral y divisor (referencia)
line(L(0), Y(0), L(0), Y(420), "#888", 0.15); line(L(110), Y(70), L(110), Y(400), "#999", 0.12, "1.5 0.8")
txt(L(110) + 0.8, Y(330), "divisor (110-118) detrás", 1.9, "start", Q, rot=-90)
# línea de corte 1-1
line(L(55), Y(412) - 0.5, L(55), Y(412) - 3, RED, 0.45); line(L(55), Y(8) + 0.5, L(55), Y(8) + 3, RED, 0.45)
txt(L(55) + 1.2, Y(412) - 1, "1", 2.4, "start", RED, "bold")
# cotas en Z de la vista frontal (eje entre vistas)
ZA = 213.5
zs = [8, 67, 170, 176, 182, 200, 277, 286.5, 290, 314, 317.5, 339.5, 398.5, 412]
line(ZA, Y(0), ZA, Y(412), RED, 0.12)
lab = spread([Y(z) for z in sorted(zs, reverse=True)], 2.5)
for z, yl in zip(sorted(zs, reverse=True), lab):
    line(ZA, Y(z), L(-1), Y(z), RED, 0.1, "0.6 0.5")
    line(ZA - 0.8, Y(z), ZA + 0.8, Y(z), RED, 0.2)
    line(ZA - 1, Y(z), ZA - 2.2, yl, RED, 0.1); txt(ZA - 2.5, yl + 0.8, f1(z), 2.1, "end", RED)
txt(ZA, Y(0) + 0.8, "0", 2.1, "middle", RED)
# cotas laterales (abajo), desde la pared lateral
us = [0, 2, 17.5, 19.5, 20, 28.5, 55, 90, 90.5, 92.5, 108, 118]
UA = Y(-6)
line(L(0), UA, L(118), UA, RED, 0.12)
labs = spread([L(u) for u in us], 2.6)
for u, xl in zip(us, labs):
    line(L(u), Y(8), L(u), UA, RED, 0.08, "0.6 0.5"); line(L(u), UA - 0.8, L(u), UA + 0.8, RED, 0.2)
    line(L(u), UA + 1, xl, UA + 3, RED, 0.1); txt(xl + 0.8, UA + 3.5, f1(u), 2.1, "end", RED, rot=-90)
txt(L(0) - 1.5, UA + 0.8, "lat", 2.0, "end", Q)
# notas de taladro
txt(L(92.5) + 3, Y(321), "4× Ø3,2", 1.9, "start", RED)
txt(L(55) + 4, Y(171), "Ø12", 1.9, "start", RED)
for uu in (44, 66): o.append(f"<circle cx='{L(uu):.2f}' cy='{Y(176):.2f}' r='{4*S:.2f}' fill='none' stroke='#777' stroke-width='0.15' stroke-dasharray='0.8 0.5'/>")

# ================= TABLAS =================
def table(x, y, title, heads, cols, rows, sz=2.15, lh=3.05):
    txt(x, y - 4.2, title, 2.8, w="bold")
    for i, h in enumerate(heads): txt(x + cols[i], y, h, sz, c=Q, w="bold")
    line(x, y + 1.0, x + cols[-1], y + 1.0, INK, 0.2)
    for k, row in enumerate(rows):
        yy = y + 4.2 + k * lh
        for i, c in enumerate(row): txt(x + cols[i], yy, c, sz)
    return y + 4.2 + len(rows) * lh

# tabla 1: piezas
rows = [("1", "A carril de medida", "modelo", "placa x 0–4 · z 340–398 · lat 0–28", "6 × M3 en la pared (T3)"),
        ("2", "A-T tapa del canal", "modelo", "sobre A", "2 × M2×6"),
        ("3", "A-F pared de fototransistores", "modelo", "detrás de A (lat 11–25)", "3 × M2×6"),
        ("4", "B cubilete de espera", "modelo", "x 139,7–185,7 · z 276–316 · lat 0–46", "4 × M3 en la pared (T3)"),
        ("5", "Trampilla B (TP+TS+AC+2 PZ)", "modelo", "eje p3", "SG90 a 16 mm"),
        ("6", "C escrow (máx. 10 monedas)", "modelo", "x 200–246 · z 183–223 · lat 0–46", "= B, misma pieza; 4 × M3 (T3)"),
        ("7", "Trampilla C", "modelo", "eje p7 (8 sobre el fondo de C)", "mismas piezas que B"),
        ("8", "Λ-B cresta", "por diseñar", "p5–p4–p6 · e 3 · lat 1–109", "alas 40,1 / 43,0"),
        ("9", "Λ-C cresta-rampa", "por diseñar", "p9–p8–p10 · e 3 · lat 1–109", "alas 176,7 / 65,8"),
        ("10", "Canal no válidas (2 chapas)", "por diseñar", "x 97–100 z 118–262 · x 128–131 z 137–235,9", "e 3 · lat 1–109"),
        ("11", "Cajón devolución", "PLA", "x 0–75 · z 8–65 · lat 3–107", "detalle D"),
        ("12", "Hucha (cajón igual)", "PLA", "x 255–330 · z 8–65 · lat 3–107", "detalle D, girado"),
        ("13", "LCD 16×2 (80×36)", "comprar", "z 284–320 · lat 15–95, por dentro", "4 × M3×12 + separador"),
        ("14", "Teclado 3×4 (70×77×1)", "comprar", "z 200–277 · lat 20–90, por fuera", "adhesivo"),
        ("15", "Pulsador 6×6 + PC-E + PC-S", "inventario · PLA", "z 176 · lat 55 · soporte x 8–16,6", "pegado; detalle E"),
        ("16", "Frontal", "DM 8", "314 × 404, entre laterales", "tabla T4"),
        ("17", "Trasera", "DM 8", "314 × 404, entre laterales", "tabla T4"),
        ("18-19", "Suelo / techo", "DM 8", "314 × 330", ""),
        ("20", "Topes de los cajones (×2)", "PLA o DM", "x 75–80 y 250–255 · z 8–18 · lat 3–107", "pegados al suelo")]
yT = 257.0
yend = table(12, yT, "T1 · Piezas y posición",
             ("n.º", "pieza", "origen", "posición", "fijación / nota"), (0, 8, 52, 72, 136, 168), rows)
# tabla 2: puntos
rowsP = [(k, d, f1(x), f1(z)) for k, d, x, z, _ in PTS]
y2 = table(185, yT, "T2 · Puntos (sección)", ("", "", "x", "z"), (0, 7, 84, 94, 100), [(k, d, xx, zz) for k, d, xx, zz in rowsP], 1.95, 3.1)
# tabla 3: taladros en la pared lateral
A_H = [(22.3, 340.8), (30.8, 388.8), (81.4, 330.4), (89.9, 378.4), (140.5, 319.9), (149.0, 368.0)]
B_H = [(133.2, 282.5), (133.2, 309.5), (192.2, 282.5), (192.2, 309.5)]
C_H = [(193.5, 189.5), (193.5, 216.5), (252.5, 189.5), (252.5, 216.5)]
rowsH = [("A", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in A_H[:3])), ("", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in A_H[3:])),
         ("B", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in B_H[:2])), ("", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in B_H[2:])),
         ("C", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in C_H[:2])), ("", " · ".join(f"({f1(x)}, {f1(z)})" for x, z in C_H[2:]))]
y3 = table(185, y2 + 8, "T3 · Taladros Ø3,4 en la pared lateral (x, z)", ("", "centros (x, z)"), (0, 7, 100), rowsH, 1.95, 3.1)
txt(185, y3 + 0.5, "C es la misma pieza que B: mismas orejetas, desplazadas 60,3 en x y −93 en z.", 1.85, c=Q)
txt(185, y3 + 3.5, "Tornillo M3 + tuerca por fuera. Crestas y canal: pegados a pared y divisor.", 1.85, c=Q)

# tabla 4: aberturas en frontal y trasera (coordenadas de la pieza: u = lat, v = z − 8)
rowsO = [("Frontal", "cajón devolución", "106 × 59", "u 2–108 · v 0–59 (desde el canto inferior)"),
         ("", "placa del carril A", "28,5 × 59", "u 0–28,5 · v 331,5–390,5 (desde el canto lateral)"),
         ("", "ventana LCD", "71 × 24", "u 19,5–90,5 · v 282–306"),
         ("", "4 taladros LCD Ø3,2", "75 × 31", "u 17,5 / 92,5 · v 278,5 / 309,5"),
          ("", "pulsador Ø12", "", "u 55 · v 168"),
         ("Trasera", "hucha", "106 × 59", "u 2–108 · v 0–59, u desde la pared lateral (visto desde dentro)")]
y4 = table(12, yend + 8, "T4 · Aberturas en los paneles (u = lat, v = z − 8)",
           ("panel", "abertura", "tamaño", "posición"), (0, 16, 50, 70, 168), rowsO)

# ================= DETALLE D: cajón (devolución = hucha) =================
dx0, s2 = 183.0, 0.5
txt(dx0, y3 + 10, "Detalle D · cajón, 2 iguales (devolución y hucha) · 1:2", 2.6, w="bold")
dy0 = y3 + 17
Lc, Hc, Wc, t, fr = 75, 57, 104, 2.5, 8
ox, oy = dx0 + 5, dy0 + Hc * s2
o.append(f"<path d='M{ox:.2f},{oy:.2f} h{Lc*s2} v{-Hc*s2} h{-t*s2} v{(Hc-t)*s2} h{-(Lc-fr-t)*s2} v{-(Hc-t)*s2} h{-fr*s2} z' fill='url(#hp)' stroke='{INK}' stroke-width='0.25'/>")
rect(ox - 0.01, oy - Hc * s2, ox + fr * s2 + 0.01, oy - (Hc - 8) * s2, "white", INK, 0.2)
line(ox, oy + 2.5, ox + Lc * s2, oy + 2.5, RED, 0.15, mk="m"); txt(ox + Lc * s2 / 2, oy + 2.0, "75", 2.0, "middle", RED)
line(ox - 2.5, oy, ox - 2.5, oy - Hc * s2, RED, 0.15, mk="m"); txt(ox - 3.3, oy - Hc * s2 / 2, "57", 2.0, "middle", RED, rot=-90)
txt(ox + fr * s2 / 2, oy - Hc * s2 - 1, "8", 1.9, "middle", RED); txt(ox + Lc * s2 + 1, oy - Hc * s2 + 2, "2,5", 1.9, "start", RED)
txt(ox + fr * s2 + 1.5, oy - Hc * s2 + 3.5, "muesca 20 × 8", 1.8, "start", Q)
txt(ox + Lc * s2 / 2, oy + 6, "sección (frente a la izq.)", 1.8, "middle", Q)
# planta girada: 104 en horizontal, 75 en vertical (frente abajo)
px0, py0 = ox + Lc * s2 + 9, dy0 - 1
o.append(f"<rect x='{px0:.2f}' y='{py0:.2f}' width='{Wc*s2:.2f}' height='{Lc*s2:.2f}' fill='url(#hp)' stroke='{INK}' stroke-width='0.25'/>")
rect(px0 + t * s2, py0 + t * s2, px0 + (Wc - t) * s2, py0 + (Lc - fr) * s2, "white", INK, 0.2)
rect(px0 + (Wc / 2 - 10) * s2, py0 + (Lc - fr) * s2, px0 + (Wc / 2 + 10) * s2, py0 + Lc * s2, "white", INK, 0.2)
line(px0, py0 + Lc * s2 + 2.5, px0 + Wc * s2, py0 + Lc * s2 + 2.5, RED, 0.15, mk="m"); txt(px0 + Wc * s2 / 2, py0 + Lc * s2 + 2.0, "104", 2.0, "middle", RED)
txt(px0 + Wc * s2 / 2 + 6, py0 + Lc * s2 + 6, "20", 1.8, "start", RED)
txt(px0 + Wc * s2 / 2, py0 - 1.2, "planta (frente abajo)", 1.8, "middle", Q)
txt(dx0, py0 + Lc * s2 + 9.5, "Paredes y fondo 2,5 · frente 8 a ras del panel · holgura 1 por lado en la abertura 106 × 59", 1.75, c=Q)

# ================= leyenda, notas, cajetín =================
ly = y4 + 7
for i, (f, d, tt) in enumerate((("url(#hm)", None, "diseñada (modelo Fusion)"), ("url(#hp)", "1.2 0.6", "prevista, por diseñar"),
                                ("url(#hw)", None, "carcasa DM 8"), ("#53675a", None, "comprada"))):
    da = f" stroke-dasharray='{d}'" if d else ""
    xx = 12 + i * 42
    o.append(f"<rect x='{xx}' y='{ly - 2.8}' width='6' height='3.4' fill='{f}' stroke='{INK}' stroke-width='0.2'{da}/>"); txt(xx + 7.5, ly, tt, 2.1)
txt(12, ly + 6, "Origen: x desde la cara exterior del frontal, z desde la cara inferior del suelo, lat desde la cara interior de la pared lateral de la columna.", 1.95, c=Q); ly += 3
txt(12, ly + 6, "Corte quebrado: A por 9,5 mm de la pared lateral (A-F a 13, en discontinua), B y C por 12, el resto por el centro de la columna (55).", 1.95, c=Q)
txt(12, ly + 9, "Crestas y rampas a 30°; 20 de paso entre el fondo de cada cubilete y el vértice de su cresta. Paso libre ≥ 27 sobre las rampas (moneda de 2 € = Ø25,75).", 1.95, c=Q)
txt(12, ly + 12, "Cotas en mm. Tolerancia general ±0,5 en DM, ±0,2 en impresas. Servos SG90 al otro lado (fuera del plano).", 1.95, c=Q)
# ================= DETALLE E: pulsador cancelar (inventario) =================
ey = ly + 16.5; S1 = 1.0; ex = 78.0
EZ = lambda z: ey + 14 - (z - 176) * S1                 # z 176 en ey+13
EX = lambda x: ex + x * S1
txt(12, ey + 2, "Detalle E · pulsador cancelar · 1:1", 2.6, w="bold")
txt(12, ey + 6, "táctil 6×6 de 5 de alto (inventario)", 1.85, c=Q)
txt(12, ey + 9, "embellecedor PLA Ø11,5 × 11 + collarín Ø16 × 1,5", 1.85, c=Q)
txt(12, ey + 12, "soporte PC-S 26 × 26 × 8,6 pegado al frontal;", 1.85, c=Q)
txt(12, ey + 15, "el táctil va pegado dentro del soporte", 1.85, c=Q)
txt(12, ey + 18, "ver cad/maquina/pulsador/esquema_pulsador", 1.85, c=Q)
o.append(f"<path d='M{EX(0)},{EZ(190)} H{EX(8)} V{EZ(182)} H{EX(0)} Z M{EX(0)},{EZ(170)} H{EX(8)} V{EZ(162)} H{EX(0)} Z' fill='url(#hw)' stroke='#444' stroke-width='0.25'/>")
o.append(f"<path d='M{EX(-3)},{EZ(181.75)} H{EX(8)} V{EZ(184)} H{EX(9.5)} V{EZ(168)} H{EX(8)} V{EZ(170.25)} H{EX(-3)} Z' fill='#8a3b3b' stroke='{INK}' stroke-width='0.2'/>")
rect(EX(9.6), EZ(177.75), EX(11.1), EZ(174.25), "#444", INK, 0.15); rect(EX(11.1), EZ(179), EX(14.6), EZ(173), "#444", INK, 0.15)
o.append(f"<path d='M{EX(8)},{EZ(189)} H{EX(16.6)} V{EZ(163)} H{EX(8)} V{EZ(167.5)} H{EX(10)} V{EZ(172.8)} H{EX(14.6)} V{EZ(179.2)} H{EX(10)} V{EZ(184.5)} H{EX(8)} Z' fill='url(#hm)' stroke='{INK}' stroke-width='0.2'/>")
line(EX(-3), EZ(186.5), EX(0), EZ(186.5), RED, 0.12, mk="m"); txt(EX(-1.5), EZ(186.5) - 0.8, "3", 1.8, "middle", RED)
line(EX(-3), EZ(181.75), EX(-3), EZ(187.5), RED, 0.1); line(EX(-3), EZ(170.25), EX(-3), EZ(159), RED, 0.1); line(EX(8), EZ(162), EX(8), EZ(159), RED, 0.1); line(EX(-3), EZ(160), EX(8), EZ(160), RED, 0.12, mk="m"); txt(EX(2.5), EZ(160) + 2.4, "11", 1.8, "middle", RED)
line(EX(16.6), EZ(163), EX(16.6), EZ(159), RED, 0.1); line(EX(8), EZ(160), EX(16.6), EZ(160), RED, 0.12, mk="m"); txt(EX(12.3), EZ(160) + 2.4, "8,6", 1.8, "middle", RED)
line(EX(-5), EZ(170.25), EX(-5), EZ(181.75), RED, 0.12, mk="m"); txt(EX(-5.8), EZ(176), "Ø11,5", 1.8, "middle", RED, rot=-90)
line(EX(19.5), EZ(163), EX(19.5), EZ(189), RED, 0.12, mk="m"); txt(EX(20.8), EZ(176), "26", 1.8, "middle", RED, rot=90)
line(EX(16.6), EZ(163), EX(20), EZ(163), RED, 0.08); line(EX(16.6), EZ(189), EX(20), EZ(189), RED, 0.08)
txt(EX(4), EZ(190) - 0.8, "frontal", 1.8, "middle", Q)
o.append(f"<rect x='{PW-128}' y='{PH-30}' width='120' height='22' fill='none' stroke='{INK}' stroke-width='0.4'/>")
line(PW - 128, PH - 22, PW - 8, PH - 22, INK, 0.25); line(PW - 128, PH - 15, PW - 8, PH - 15, INK, 0.25); line(PW - 58, PH - 22, PW - 58, PH - 8, INK, 0.25)
txt(PW - 125, PH - 24.5, "Máquina expendedora SED · Corte 1: columna de monedas", 3.2, w="bold")
txt(PW - 125, PH - 17.5, "Escala 1:2 (imprimir A3 al 100 %)", 2.5); txt(PW - 55, PH - 17.5, "Hoja 1/1 · v2 · 12-11-2026", 2.5)
txt(PW - 125, PH - 10.5, "Máquina 330 × 330 × 420 · cotas en mm", 2.5); txt(PW - 55, PH - 10.5, "UPM ETSIDI · SED 2026-27", 2.5)
# barra de escala: comprueba la escala de la impresión
for i in range(5):
    rect(14 + i * 10, 14, 24 + i * 10, 16, INK if i % 2 == 0 else "white", INK, 0.2)
for i, t in ((0, "0"), (5, "100 mm")): txt(14 + i * 10, 20, t, 2.0, "middle")
txt(68, 16.2, "barra de 100 mm reales: mide 50 mm si la escala es 1:2 (A3 al 100 %). En A4 sale ≈ 1:2,8.", 2.0, c=Q)
o.append("</svg>"); open("plano_corte1.svg", "w").write("\n".join(o))
print(yend, y2, y3, y4, ly)
