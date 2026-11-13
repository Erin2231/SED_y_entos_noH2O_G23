import json, math
r = json.load(open("corte1.json")); ref = json.load(open("ref.json"))
PW, PH = 297.0, 420.0            # A3 vertical (mm)
S = 0.5                          # escala 1:2
OX, OY = 58.0, 262.0             # origen máquina (frontal, suelo) en la hoja
H, D, T = 420, 330, 8
X = lambda d: OX + d * S
Y = lambda h: OY - h * S
INK = "#222"; Q = "#666"; RED = "#8b1e1e"; BLU = "#2f5d8a"
o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{PW}mm' height='{PH}mm' viewBox='0 0 {PW} {PH}' font-family='DejaVu Sans, Arial, sans-serif'>",
     "<defs>"
     "<pattern id='hm' width='1.6' height='1.6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='1.6' height='1.6' fill='#d3dae3'/><line x1='0' y1='0' x2='0' y2='1.6' stroke='#5b6b80' stroke-width='0.18'/></pattern>"
     "<pattern id='hw' width='2.2' height='2.2' patternUnits='userSpaceOnUse' patternTransform='rotate(-45)'><rect width='2.2' height='2.2' fill='#ebe7e1'/><line x1='0' y1='0' x2='0' y2='2.2' stroke='#a39886' stroke-width='0.18'/></pattern>"
     "<pattern id='hp' width='2' height='2' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='2' height='2' fill='#f3f3f3'/><line x1='0' y1='0' x2='0' y2='2' stroke='#b5b5b5' stroke-width='0.15'/></pattern>"
     f"<marker id='m' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{RED}'/></marker>"
     f"<marker id='mb' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='4' markerHeight='4' orient='auto-start-reverse'><path d='M0,1L10,5L0,9z' fill='{BLU}'/></marker>"
     "</defs>", f"<rect width='{PW}' height='{PH}' fill='white'/>",
     f"<rect x='8' y='8' width='{PW-16}' height='{PH-16}' fill='none' stroke='{INK}' stroke-width='0.5'/>"]
def txt(x, y, t, sz=2.6, a="start", c=INK, w="normal"):
    o.append(f"<text x='{x:.2f}' y='{y:.2f}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'>{t}</text>")
def line(x0, y0, x1, y1, c=INK, w=0.2, dash=None, mk=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""; m = f" marker-start='url(#{mk})' marker-end='url(#{mk})'" if mk else ""
    o.append(f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{c}' stroke-width='{w}'{d}{m}/>")
STY = {"modelo": ("url(#hm)", INK, 0.3, None), "previsto": ("url(#hp)", "#555", 0.25, "1.2 0.6"),
       "carcasa": ("url(#hw)", "#444", 0.25, None), "comprado": ("#53675a", "#222", 0.25, None)}
ORDER = ["suelo", "techo", "frontal", "trasera", "cajón devolución", "hucha", "guía hucha", "canal", "Λ-B", "Λ-C", "C", "C-TP",
         "B", "B-TP", "A", "A-T", "LCD placa", "LCD conectores", "LCD bisel", "numpad", "placa pulsador", "pulsador"]
for n in ORDER:
    grp, faces, yc = r[n]
    fill, st, sw, dash = STY[grp]
    if n == "LCD bisel": fill = "#2e3a31"
    if n == "numpad": fill = "#cfcfcf"
    if n in ("placa pulsador",): fill = "#7a8f6e"
    if n == "pulsador": fill = "#8a3b3b"
    for f in faces:
        d = " ".join("M" + " L".join(f"{X(p[0]):.2f},{Y(p[1]):.2f}" for p in w) + " Z" for w in f)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        o.append(f"<path d='{d}' fill='{fill}' fill-rule='evenodd' stroke='{st}' stroke-width='{sw}'{da} stroke-linejoin='round'/>")
# A-F detrás (contorno)
for f in r["A-F"][1]:
    d = "M" + " L".join(f"{X(p[0]):.2f},{Y(p[1]):.2f}" for p in f[0]) + " Z"
    o.append(f"<path d='{d}' fill='none' stroke='#5b6b80' stroke-width='0.2' stroke-dasharray='0.8 0.5'/>")
# eje de corte y recorrido de monedas
bp, cp = ref["B_PIV"], ref["C_PIV"]
for (x, z) in (bp, cp):
    line(X(x) - 3, Y(z), X(x) + 3, Y(z), "#888", 0.12, "2 0.6 0.4 0.6"); line(X(x), Y(z) - 3, X(x), Y(z) + 3, "#888", 0.12, "2 0.6 0.4 0.6")
txt(X(-30), Y(361), "monedas", 2.4, "end", BLU)
line(X(-28), Y(358), X(2), Y(352), BLU, 0.35, mk=None); o.append(f"<line x1='{X(-28):.2f}' y1='{Y(358):.2f}' x2='{X(2):.2f}' y2='{Y(352):.2f}' stroke='{BLU}' stroke-width='0.35' marker-end='url(#mb)'/>")
def flecha(pts, c=BLU, dash="1.2 0.8"):
    p = " ".join(f"{X(a):.2f},{Y(b):.2f}" for a, b in pts)
    o.append(f"<polyline points='{p}' fill='none' stroke='{c}' stroke-width='0.3' stroke-dasharray='{dash}' marker-end='url(#{'mb' if c == BLU else 'm'})'/>")
flecha([(175, 262), (205, 244)]); flecha([(150, 262), (114, 236), (114, 112)], RED)
flecha([(237, 150), (262, 132), (262, 100)]); flecha([(205, 146), (110, 86), (60, 66)], RED)
# ---------- cotas ----------
def cotav(x, z0, z1, t, side=1):
    line(X(x), Y(z0), X(x), Y(z1), RED, 0.18, mk="m"); txt(X(x) + 1.2 * side, (Y(z0) + Y(z1)) / 2 + 0.9, t, 2.4, "start" if side > 0 else "end", RED)
def cotah(z, x0, x1, t, dy=3.2):
    line(X(x0), Y(z), X(x1), Y(z), RED, 0.18, mk="m"); txt((X(x0) + X(x1)) / 2, Y(z) + dy, t, 2.4, "middle", RED)
def nivel(z, t, x0=D, x1=D + 10):
    line(X(x0), Y(z), X(x1), Y(z), RED, 0.15); txt(X(x1) + 1, Y(z) + 0.9, t, 2.3, "start", RED)
cotah(-22, 0, D, "330"); cotav(D + 80, 0, H, "420")
for z, t in ((398, "398 techo del carril"), (352, "352 suelo del carril en la entrada"), (326, "326 final del carril"), (316, "316 boca de B"),
             (284, "284 eje trampilla B"), (268, "268 vértice Λ-B"), (233, "233 boca de C"), (171, "171 eje trampilla C"),
             (155, "155 vértice Λ-C"), (95, "95 hucha"), (65, "65 cajón devolución")):
    nivel(z, t)
# cotas frontales a la izquierda
for z0, z1, t in ((284, 320, "LCD 284-320"), (200, 277, "numpad 200-277"), (170, 182, "pulsador 176"), (8, 65, "devolución 8-65")):
    line(X(-4), Y(z0), X(-8), Y(z0), RED, 0.15); line(X(-4), Y(z1), X(-8), Y(z1), RED, 0.15)
    line(X(-6), Y(z0), X(-6), Y(z1), RED, 0.18, mk="m"); txt(X(-8), (Y(z0) + Y(z1)) / 2 + 0.9, t, 2.3, "end", RED)

cotav(253, 163, 233, "70", 1)
txt(X(190), Y(196), "32,5°", 2.2, "start", Q); txt(X(140), Y(118), "32,5°", 2.2, "start", Q)
# ---------- globos ----------
G = [(1, (70, 372), (55, 408)), (2, (100, 378), (110, 408)), (3, (140, 340), (160, 352)), (4, (142, 300), (122, 300)),
     (5, (162, 286), (150, 292)), (6, (202, 210), (218, 200)), (7, (230, 174), (275, 182)), (8, (190, 250), (205, 268)),
     (9, (180, 135), (170, 125)), (10, (113, 180), (135, 190)), (11, (50, 40), (45, 80)), (12, (290, 60), (300, 115)),
     (13, (5, 302), (25, 302)), (14, (-0.5, 240), (25, 245)), (15, (10, 176), (30, 176)), (16, (4, 140), (25, 140)),
     (17, (326, 250), (305, 250)), (18, (160, 4), (160, 24)), (19, (200, 416), (230, 430))]
for n, (px, pz), (bx, bz) in G:
    line(X(px), Y(pz), X(bx), Y(bz), INK, 0.15)
    o.append(f"<circle cx='{X(px):.2f}' cy='{Y(pz):.2f}' r='0.45' fill='{INK}'/>")
    o.append(f"<circle cx='{X(bx):.2f}' cy='{Y(bz):.2f}' r='2.3' fill='white' stroke='{INK}' stroke-width='0.25'/>"); txt(X(bx), Y(bz) + 0.9, str(n), 2.5, "middle", w="bold")
# ---------- tabla de piezas ----------
rows = [("1", "A carril de medida", "modelo · PLA", "150 mm a 10°, 7 barreras IR"), ("2", "A-T tapa del canal", "modelo · PLA", "2 × M2×6"),
        ("3", "A-F pared de fototransistores (detrás)", "modelo · PLA", "3 × M2×6 + 5 × A-S"), ("4", "B cubilete de espera", "modelo · PLA", "46 × 46 × 40, SG90 a 16 mm"),
        ("5", "B-TP / B-TS trampilla + B-AC + 2 B-PZ", "modelo · PLA", "giro ±40°"), ("6", "C escrow (20 monedas)", "por diseñar", "como B, 70 de alto, 2º SG90"),
        ("7", "Trampilla de C", "modelo · PLA", "las mismas piezas que B"), ("8", "Λ-B cresta: válidas → C / no válidas → canal", "por diseñar", "115°, 16 bajo el eje"),
        ("9", "Λ-C cresta y rampas: hucha / devolución", "por diseñar", "rampas a 32,5°"), ("10", "Canal de no válidas", "por diseñar", "28 de paso"),
        ("11", "Cajón de devolución y cambio", "por diseñar · PLA", "95 × 57 × ≈90, a ras"), ("12", "Hucha", "por diseñar · PLA", "≈ 67 × 87 × 100, por detrás"),
        ("13", "Pantalla LCD 16×2 HD44780", "comprar", "80 × 36 × 12,5"), ("14", "Teclado de membrana 3×4", "comprar", "70 × 77 × 1, adhesivo"),
        ("15", "Pulsador cancelar", "comprar / tenéis", "Ø12 de panel o táctil + tapa"), ("16", "Frontal (en guías)", "DM 8 mm", "314 × 404"),
        ("17", "Trasera (en guías)", "DM 8 mm", "314 × 404"), ("18", "Suelo", "DM 8 mm", "314 × 330"), ("19", "Techo", "DM 8 mm", "314 × 330")]
ty = 296.0
txt(14, ty - 6, "Lista de piezas del corte", 3.4, w="bold")
cols = (14, 22, 112, 150)
for i, h in enumerate(("n.º", "pieza", "origen", "medidas / notas")):
    txt(cols[i], ty, h, 2.4, c=Q, w="bold")
line(14, ty + 1.2, PW - 14, ty + 1.2, INK, 0.2)
for k, row in enumerate(rows):
    y = ty + 5 + k * 4.1
    for i, c in enumerate(row):
        col = RED if (i == 2 and c.startswith("comprar")) else (Q if i == 2 else INK)
        txt(cols[i], y, c, 2.4, c=col)
# leyenda
ly = 30
for i, (f, d, t) in enumerate((("url(#hm)", None, "pieza diseñada (cotas del modelo)"), ("url(#hp)", "1.2 0.6", "pieza prevista, por diseñar"),
                                ("url(#hw)", None, "carcasa (DM 8 mm o impresa)"), ("#53675a", None, "componente comprado"))):
    da = f" stroke-dasharray='{d}'" if d else ""
    o.append(f"<rect x='{198}' y='{ly + i*5.5 - 2.8}' width='7' height='3.6' fill='{f}' stroke='{INK}' stroke-width='0.2'{da}/>"); txt(207, ly + i * 5.5, t, 2.4)
# cajetín
o.append(f"<rect x='{PW-128}' y='{PH-34}' width='120' height='26' fill='none' stroke='{INK}' stroke-width='0.4'/>")
line(PW - 128, PH - 24, PW - 8, PH - 24, INK, 0.25); line(PW - 128, PH - 16, PW - 8, PH - 16, INK, 0.25); line(PW - 58, PH - 24, PW - 58, PH - 8, INK, 0.25)
txt(PW - 125, PH - 27, "Máquina expendedora SED · Corte 1: columna de monedas", 3.2, w="bold")
txt(PW - 125, PH - 19, "Escala 1:2 (imprimir en A3 al 100 %)", 2.6); txt(PW - 55, PH - 19, "Hoja 1/1 · v1 · 12-11-2026", 2.6)
txt(PW - 125, PH - 11, "Cotas en mm · máquina 330 × 330 × 420", 2.6); txt(PW - 55, PH - 11, "UPM ETSIDI · SED 2026-27", 2.6)
txt(14, 18, "Corte quebrado: carril, B y C por el recorrido de las monedas (a 9,5-12 mm de la pared lateral); carcasa, crestas, cajones y frontal por el centro de la columna (63 mm).", 2.3, c=Q)
txt(14, 22, "A-F (pared de fototransistores) queda detrás del plano y se dibuja en discontinua. Los servos SG90 quedan fuera del plano (lado opuesto a la pared).", 2.3, c=Q)
o.append("</svg>"); open("plano_corte1.svg", "w").write("\n".join(o))
