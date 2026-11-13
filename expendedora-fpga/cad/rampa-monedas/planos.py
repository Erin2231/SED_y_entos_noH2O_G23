"""Genera los planos (SVG por hoja, A4 apaisado, unidades en mm) a partir de modelo.py."""
import math, os, sys, datetime
import numpy as np
import cadquery as cq
import modelo as m
import vistas as V

OUT = sys.argv[1] if len(sys.argv) > 1 else "planos"
os.makedirs(OUT, exist_ok=True)
FECHA = "2026-11-11"
INK = "#111"; HID = "#9aa0a6"; DIM = "#0b5cad"; RED = "#c62828"; QUIET = "#555"; FILL = "#e9eef5"
NHOJAS = 7

# ---------------- piezas (espejadas: pared de montaje a la IZQUIERDA vista desde el frente) ----------------
MIR = cq.Matrix([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0]])


def mir(wp):
    return cq.Workplane(obj=wp.val().mirror("XZ"))


A = mir(m.cuerpo_A()); AT = mir(m.tapa_AT()); AS = m.portasensor_AS(); B = mir(m.cubilete_B())


def mp(p):
    return (p[0], -p[1], p[2])


def PA(u, v, x=0.0):
    return mp(m.P(u, v, x))


# ---------------- primitivas SVG ----------------
class Hoja:
    def __init__(self, n, titulo, pieza, escala):
        self.n, self.titulo, self.pieza, self.escala = n, titulo, pieza, escala
        self.b = []

    def add(self, s):
        self.b.append(s)

    def text(self, x, y, s, size=2.6, anchor="start", fill=INK, weight="normal", rot=None, italic=False):
        r = f" transform='rotate({rot:.2f} {x:.2f} {y:.2f})'" if rot is not None else ""
        st = " font-style='italic'" if italic else ""
        self.add(f"<text x='{x:.2f}' y='{y:.2f}' font-size='{size}' text-anchor='{anchor}' fill='{fill}' font-weight='{weight}'{st}{r}>{s}</text>")

    def line(self, x1, y1, x2, y2, c=INK, w=0.3, dash=None, cap="round"):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<line x1='{x1:.3f}' y1='{y1:.3f}' x2='{x2:.3f}' y2='{y2:.3f}' stroke='{c}' stroke-width='{w}' stroke-linecap='{cap}'{d}/>")

    def rect(self, x, y, w, h, c=INK, sw=0.3, fill="none"):
        self.add(f"<rect x='{x:.2f}' y='{y:.2f}' width='{w:.2f}' height='{h:.2f}' fill='{fill}' stroke='{c}' stroke-width='{sw}'/>")

    def para(self, x, y, lines, size=2.7, lh=4.2, fill=INK, width=None):
        for i, l in enumerate(lines):
            w = "bold" if l.startswith("**") else "normal"
            self.text(x, y + i * lh, l.strip("*"), size, fill=fill, weight=w)
        return y + len(lines) * lh

    def svg(self):
        self.cajetin()
        return ("<svg xmlns='http://www.w3.org/2000/svg' width='297mm' height='210mm' viewBox='0 0 297 210' "
                "font-family='DejaVu Sans, Arial, sans-serif'>"
                "<defs><marker id='ar' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='2.6' markerHeight='2.6' markerUnits='userSpaceOnUse' orient='auto-start-reverse'>"
                f"<path d='M0 1.5L10 5L0 8.5z' fill='{DIM}'/></marker>"
                "<marker id='ak' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='2.4' markerHeight='2.4' markerUnits='userSpaceOnUse' orient='auto-start-reverse'>"
                f"<path d='M0 1.5L10 5L0 8.5z' fill='{INK}'/></marker></defs>"
                "<rect width='297' height='210' fill='white'/>"
                f"<rect x='6' y='6' width='285' height='198' fill='none' stroke='{INK}' stroke-width='0.5'/>"
                + "".join(self.b) + "</svg>")

    def cajetin(self):
        x0, y0, w, h = 191, 180, 100, 24
        self.rect(x0, y0, w, h, INK, 0.4, "white")
        self.line(x0, y0 + 8, x0 + w, y0 + 8, INK, 0.25)
        self.line(x0, y0 + 16, x0 + w, y0 + 16, INK, 0.25)
        self.line(x0 + 62, y0 + 8, x0 + 62, y0 + 24, INK, 0.25)
        self.text(x0 + 2, y0 + 5.6, self.titulo, 3.2, weight="bold")
        self.text(x0 + 2, y0 + 13.2, self.pieza, 2.6)
        self.text(x0 + 2, y0 + 21.2, "SED 2026-27 · Máquina expendedora", 2.4, fill=QUIET)
        self.text(x0 + 64, y0 + 13.2, f"Escala {self.escala}", 2.6)
        self.text(x0 + 64, y0 + 21.2, f"Hoja {self.n}/{NHOJAS} · {FECHA}", 2.4, fill=QUIET)
        self.text(x0 + w - 2, y0 + 5.6, "cotas en mm", 2.2, "end", QUIET)


# ---------------- vistas ----------------
class Vista:
    def __init__(self, hoja, shape, ver, xdir, ox, oy, s, hidden=True, w=0.32):
        self.h, self.ver, self.xdir, self.ox, self.oy, self.s = hoja, ver, xdir, ox, oy, s
        if shape is not None:
            vis, hid = V.proyectar(shape, ver, xdir)
            if hidden:
                for e in hid:
                    hoja.add(self._pl(e, HID, 0.16, "0.9 0.6"))
            for e in vis:
                hoja.add(self._pl(e, INK, w))

    def _pl(self, pts, c, w, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        p = " ".join(f"{self.ox + self.s * x:.3f},{self.oy - self.s * y:.3f}" for x, y in pts)
        return f"<polyline points='{p}' fill='none' stroke='{c}' stroke-width='{w}' stroke-linejoin='round' stroke-linecap='round'{d}/>"

    def pt(self, p3):
        x, y = V.p2(p3, self.ver, self.xdir)
        return self.ox + self.s * x, self.oy - self.s * y

    def poly(self, pts2d, fill=FILL, c=INK, w=0.3):
        p = " ".join(f"{self.ox + self.s * x:.3f},{self.oy - self.s * y:.3f}" for x, y in pts2d)
        self.h.add(f"<polygon points='{p}' fill='{fill}' stroke='{c}' stroke-width='{w}'/>")


def cota(h, a, b, off, txt=None, ang=None, size=2.5, ext=1.5, gap=0.8, inside=True, tpos=0.5):
    """Cota lineal entre puntos de pagina a y b. off: desplazamiento perpendicular (mm, signo = lado).
    ang: None = alineada; 'h' = horizontal; 'v' = vertical."""
    a, b = np.array(a, float), np.array(b, float)
    if ang == 'h':
        d = np.array([1.0, 0.0]); n = np.array([0.0, -1.0])
    elif ang == 'v':
        d = np.array([0.0, -1.0]); n = np.array([-1.0, 0.0])
    else:
        d = (b - a) / np.linalg.norm(b - a); n = np.array([d[1], -d[0]])
    base = a if off >= 0 else a
    # posiciones de la linea de cota
    la = a + n * (off + ((b - a) @ n if False else 0))
    # proyectar a y b sobre la recta de cota: punto = p + n * (k - p.n) con k fijo
    k = max(a @ n, b @ n) + off if off >= 0 else min(a @ n, b @ n) + off
    pa = a + n * (k - a @ n); pb = b + n * (k - b @ n)
    for p, q in ((a, pa), (b, pb)):
        v = q - p; L = np.linalg.norm(v)
        if L > 1e-6:
            u = v / L; s0 = p + u * gap; s1 = q + u * ext
            h.line(*s0, *s1, DIM, 0.15)
    if txt is None:
        txt = fmt(np.linalg.norm(pb - pa) / 1.0)
    h.add(f"<line x1='{pa[0]:.3f}' y1='{pa[1]:.3f}' x2='{pb[0]:.3f}' y2='{pb[1]:.3f}' stroke='{DIM}' stroke-width='0.18' marker-start='url(#ar)' marker-end='url(#ar)'/>")
    mid = pa + (pb - pa) * tpos
    angd = math.degrees(math.atan2(pb[1] - pa[1], pb[0] - pa[0]))
    if angd > 90 or angd <= -90:
        angd += 180
    off_t = -n * 0.0
    tx = mid + np.array([math.sin(math.radians(angd)), -math.cos(math.radians(angd))]) * 0.9
    h.text(tx[0], tx[1], txt, size, "middle", DIM, rot=angd if abs(angd) > 0.01 else None)


def fmt(v, nd=1):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".") if nd else f"{v:.0f}"
    return s.replace(".", ",")


def nota(h, p, t, dx, dy, size=2.4, anchor="start", c=INK):
    x, y = p
    tx, ty = x + dx, y + dy
    h.line(x, y, tx, ty, QUIET, 0.15)
    h.add(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='0.45' fill='{QUIET}'/>")
    h.line(tx, ty, tx + (8 if anchor == 'start' else -8), ty, QUIET, 0.15)
    h.text(tx + (9 if anchor == 'start' else -9), ty + 0.9, t, size, anchor, c)


def etiqueta(h, x, y, t, size=3.0):
    h.text(x, y, t, size, "middle", INK, "bold")


def arco(h, c, r, a0, a1, txt, tr=None, size=2.5):
    """angulos en grados en pantalla (0 = derecha, positivo = antihorario visual)"""
    x0, y0 = c[0] + r * math.cos(math.radians(a0)), c[1] - r * math.sin(math.radians(a0))
    x1, y1 = c[0] + r * math.cos(math.radians(a1)), c[1] - r * math.sin(math.radians(a1))
    sweep = 0 if a1 > a0 else 1
    h.add(f"<path d='M{x0:.2f} {y0:.2f}A{r} {r} 0 0 {sweep} {x1:.2f} {y1:.2f}' fill='none' stroke='{DIM}' stroke-width='0.18' marker-start='url(#ar)' marker-end='url(#ar)'/>")
    am = (a0 + a1) / 2; rr = tr or r + 3
    h.text(c[0] + rr * math.cos(math.radians(am)), c[1] - rr * math.sin(math.radians(am)) + 0.9, txt, size, "middle", DIM)


def seccion_face(shape, x, zlim=None):
    """Cara de seccion en el plano X = x (devuelve lista de anillos 3D)."""
    big = cq.Workplane("XY").box(0.02, 400, 400).translate((x, 0, 0))
    if zlim:
        big = cq.Workplane("XY").box(0.02, 400, zlim[1] - zlim[0]).translate((x, 0, (zlim[0] + zlim[1]) / 2))
    sl = shape.intersect(big)
    faces = sl.faces(">X").vals()
    from OCP.BRepTools import BRepTools_WireExplorer
    from OCP.TopAbs import TopAbs_REVERSED
    rings = []
    for f in faces:
        for w in [f.outerWire()] + f.innerWires():
            pts = []
            ex = BRepTools_WireExplorer(w.wrapped)
            while ex.More():
                e = cq.Edge(ex.Current())
                n = 2 if e.geomType() == "LINE" else 24
                seg = [e.positionAt(t, mode="parameter").toTuple() for t in np.linspace(e._bounds()[0], e._bounds()[1], n)]
                if ex.Current().Orientation() == TopAbs_REVERSED:
                    seg = seg[::-1]
                pts += seg
                ex.Next()
            rings.append(pts)
    return rings


def dibuja_seccion(vista, rings, hatch=True):
    pts_all = []
    d = ""
    for r in rings:
        pp = [vista.pt(p) for p in r]
        d += "M" + " L".join(f"{x:.3f} {y:.3f}" for x, y in pp) + "Z "
    vista.h.add(f"<path d='{d}' fill='{FILL}' fill-rule='evenodd' stroke='{INK}' stroke-width='0.35'/>")


# =====================================================================
hojas = []

# ---------------- Hoja 1: portada e indice ----------------
h = Hoja(1, "Sistema de monedas", "Portada e índice", "—")
h.text(20, 34, "Sistema de monedas de la máquina expendedora", 8, weight="bold")
h.text(20, 44, "Planos para modelar en CAD: carril de medida (pieza A) y cubilete de espera (pieza B)", 4, fill=QUIET)
y = 62
h.text(20, y, "Índice", 4.5, weight="bold"); y += 8
idx = [("1", "Portada e índice"), ("2", "Qué es, dónde va y lista de piezas (dibujo de situación)"),
       ("3", "Pieza A · Carril de medida: vistas generales"), ("4", "Pieza A · Secciones por las barreras y tabla de alturas"),
       ("5", "Pieza A · Placa frontal y ranura · Pieza A-T (tapa) · Pieza A-S (portasensor)"),
       ("6", "Pieza B · Cubilete de espera (sin fondo)"), ("7", "Impresión en Bambu Lab A1, montaje y comprobaciones")]
for n, t in idx:
    h.text(24, y, f"Hoja {n}", 3.4, weight="bold"); h.text(46, y, t, 3.4); y += 6.5
y += 6
h.text(20, y, "Criterios generales", 4.5, weight="bold"); y += 7
y = h.para(20, y, [
    "· Cotas en mm. Ángulos en grados. Material: PLA. Impresora: Bambu Lab A1, boquilla 0,4 mm.",
    "· Las medidas de agujeros y huecos ya están compensadas para impresión (salen un poco más pequeñas):",
    "   canal 3,4 (sale ~3,2) · ranura 25,2 (sale ~25,0) · LED 3 mm → Ø3,2 · M3 pasante → Ø3,5 · M2 autorroscante → Ø1,8.",
    "· Pared de montaje: la de la IZQUIERDA del canal mirando la máquina de frente. LEDs del lado de la pared,",
    "   fototransistores hacia el interior. Si se monta en la pared derecha, basta con hacer simetría en el CAD.",
    "· El canal se dibuja recto; los dos ángulos salen solos al montar: 12° por la cuña (\"medio trapecio\")",
    "   y 10° por la posición de los agujeros en la pared lateral (hoja 7).",
    "· Diámetros de monedas de memoria: medidlos con calibre y ajustad la tabla de alturas (hoja 4) antes de imprimir.",
], 3.0, 5.0)
h.text(20, 196, "Generado a partir del modelo paramétrico cad/rampa-monedas/modelo.py (mismas cotas que los STEP adjuntos).", 2.5, fill=QUIET)
hojas.append(h)

# ---------------- Hoja 2: situacion ----------------
h = Hoja(2, "Situación en la máquina", "Conjunto A + B", "sin escala")
h.text(12, 16, "Qué es y dónde va", 5, weight="bold")
txt = [
    "La moneda entra por la ranura de la placa frontal (pieza A), rueda por el canal",
    "inclinado 10° y cruza 7 barreras de infrarrojos. Al salir cae en el cubilete (pieza B),",
    "cuyo fondo es una trampilla con servo: la retiene, la cobra (hucha, detrás) o la",
    "devuelve (bandeja, delante). La trampilla y las rampas de debajo son la siguiente pieza.",
    "",
    "**Piezas de esta entrega",
    "A    Carril de medida con placa frontal y 6 lengüetas M3",
    "A-T Tapa desmontable del canal (2 tornillos M2)",
    "A-S Portasensor regulable con rendija de 1 mm (×5)",
    "B    Cubilete de espera sin fondo, soporte de SG90 y 4 lengüetas M3",
    "",
    "**Posición (desde la cara exterior del frontal y el suelo)",
    f"Entrada del canal (punto de referencia R): altura {fmt(m.H0, 0)}",
    f"Final del suelo del canal: fondo {fmt(m.FIN_CARRIL[0])}, altura {fmt(m.FIN_CARRIL[1])}",
    f"Cubilete: de fondo {fmt(m.B_D0)} a {fmt(m.B_D0 + 46)}, borde superior a {fmt(m.B_TOP_H)}",
    "Las coordenadas de cada agujero de la pared están en la hoja 7.",
]
h.para(12, 26, txt, 2.9, 4.6)
# dibujo isometrico de situacion
mov_A = A.val().rotate((0, 0, 0), (0, 1, 0), m.ALFA).translate(cq.Vector(m.T_PLACA, 0, m.H0) - cq.Vector(0, 0, 0))
# el DATUM espejado es (0,-8,0); tras rotar sigue en (0,-8,0) -> a (T_PLACA, -8, H0)
mov_T = AT.val().rotate((0, 0, 0), (0, 1, 0), m.ALFA).translate(cq.Vector(m.T_PLACA, 0, m.H0))
mov_B = B.val().translate(cq.Vector(m.B_D0, 0, m.B_TOP_H - m.B_H))
pared = cq.Workplane("XY").box(230, 4, 150, centered=False).translate((0, 0, 255)).val()
panel = (cq.Workplane("XY").box(4, 70, 150, centered=False).translate((0, -66, 255))
         .cut(cq.Workplane("XY").box(6, 28.4, 58.4, centered=False).translate((-1, -28.2, m.H0 - 12.2)))).val()
asm = cq.Workplane(obj=cq.Compound.makeCompound([mov_A, mov_T, mov_B, pared, panel]))
iso_ver, iso_x = (-1.0, -1.25, 0.9), (1, -0.8, 0)
vi = Vista(h, asm, iso_ver, iso_x, 0, 0, 1.0, hidden=False, w=0.25)
# reencuadrar: calcular bbox de proyeccion
pts = []
for sh in [mov_A, mov_B, pared, panel]:
    bb = sh.BoundingBox()
    for X in (bb.xmin, bb.xmax):
        for Y in (bb.ymin, bb.ymax):
            for Z in (bb.zmin, bb.zmax):
                pts.append(V.p2((X, Y, Z), iso_ver, iso_x))
pts = np.array(pts)
sc = min(150 / (pts[:, 0].max() - pts[:, 0].min()), 150 / (pts[:, 1].max() - pts[:, 1].min()))
h.b = h.b[:len(h.b) - 0]  # (se redibuja abajo con escala buena)
# borrar el dibujo provisional
h.b = [s for s in h.b if not s.startswith("<polyline")]
ox = 130 - sc * pts[:, 0].min(); oy = 18 + sc * pts[:, 1].max()
vi = Vista(h, asm, iso_ver, iso_x, ox, oy, sc, hidden=False, w=0.25)
nota(h, vi.pt((2, -10, m.H0 + 15)), "placa frontal con ranura (A)", -10, 45, anchor="end")
nota(h, vi.pt((60, -20, m.H0 + 10)), "carril A + tapa A-T", 6, -14)
nota(h, vi.pt((m.B_D0, -23, m.B_TOP_H - 20)), "cubilete B", 22, 32)
nota(h, vi.pt((200, 2, 380)), "pared lateral izquierda", 6, -6)
nota(h, vi.pt((2, -55, 300)), "panel frontal", -10, 12, anchor="end")
nota(h, vi.pt((m.B_D0 + 23, -52, m.B_TOP_H - 33)), "soporte SG90", 14, 6)
h.text(12, 172, "Vista isométrica desde el interior de la máquina, por delante y por encima.", 2.6, fill=QUIET)
h.text(12, 177, "Simplificado: pared y panel recortados; sin trampilla ni rampas.", 2.6, fill=QUIET)
hojas.append(h)

# ---------------- Hoja 3: pieza A vistas generales ----------------
h = Hoja(3, "Pieza A · Carril de medida", "Vistas generales", "1:1")
s = 1.0
# vista desde el interior (arriba)
v1 = Vista(h, A, (0, -1, 0), (1, 0, 0), 40, 80, s)
etiqueta(h, 40 + 75, 13, "VISTA DESDE EL INTERIOR (lado fototransistores)")
# vista desde la pared (abajo)
v2 = Vista(h, A, (0, 1, 0), (-1, 0, 0), 205, 160, s)
etiqueta(h, 205 - 75, 106, "VISTA DESDE LA PARED (cara de montaje)")
# cotas v1
zt = m.yz(m.u_at_y0(m.H_INT), m.H_INT)[1]; zb = m.yz(m.u_at_y0(-m.T_SUELO), -m.T_SUELO)[1]
xe = m.L
cota(h, v1.pt(PA(0, 0, 0)), v1.pt(PA(0, 0, xe)), 0, "150 (longitud del carril, desde R)", 'h') if False else None
pR = v1.pt(PA(0, 0, 0)); pE = v1.pt((m.L, 0, 0))
cota(h, (pR[0], v1.pt((0, 0, zb - m.LENG_OUT))[1]), (pE[0], v1.pt((0, 0, zb - m.LENG_OUT))[1]), -6, "150 (desde R hasta el final)", 'h')
for xl in m.LENG_X:
    pass
base_y = v1.pt((0, 0, zt + m.LENG_OUT))[1]
prev = pR[0]
for i, xl in enumerate(m.LENG_X):
    cota(h, (prev, base_y), (v1.pt((xl, 0, 0))[0], base_y), -(5 if i == 0 else 5), fmt(xl - (0 if i == 0 else m.LENG_X[i - 1])), 'h')
    prev = v1.pt((xl, 0, 0))[0]
h.text(pR[0] - 12, base_y - 4, "lengüetas:", 2.3, "start", DIM)
# R mark
h.add(f"<circle cx='{pR[0]:.2f}' cy='{pR[1]:.2f}' r='1.1' fill='none' stroke='{RED}' stroke-width='0.3'/>")
h.text(pR[0] + 1.8, pR[1] + 3.6, "R", 2.6, fill=RED, weight="bold")
# barreras: marcas en v1
for (n, x, hh, t) in m.BARRERAS:
    p = v1.pt(PA(m.GAP + m.T_FOTO, hh, x))
    h.text(p[0], v1.pt((0, 0, zb))[1] + 4.5, n, 2.2, "middle", RED, "bold")
# lengueta detalle
pl = v1.pt((m.LENG_X[2] - 7, 0, zt + m.LENG_OUT)); pr_ = v1.pt((m.LENG_X[2] + 7, 0, zt + m.LENG_OUT))
cota(h, pl, pr_, 4, "14", 'h')
pz0 = v1.pt((m.LENG_X[2] + 7, 0, zt)); pz1 = v1.pt((m.LENG_X[2] + 7, 0, zt + m.LENG_OUT))
cota(h, pz0, pz1, -5, "13", 'v')
nota(h, v1.pt((m.LENG_X[2], 0, zt + m.LENG_OUT - 6.5)), "6× Ø3,5 pasante (M3), a 6,5 del borde", 10, -2)
nota(h, v1.pt((m.LENG_X[1] - 7 - 6, 0, zt + 6)), "chaflán 45° (sin soportes)", -16, 4, anchor="end")
# altura total de la cara de montaje
cota(h, v1.pt((m.L, 0, zb)), v1.pt((m.L, 0, zt)), 10, fmt(zt - zb), 'v')
h.text(v1.pt((m.L, 0, 0))[0] + 13, v1.pt((m.L, 0, 16))[1], "cara de", 2.2, "start", DIM)
h.text(v1.pt((m.L, 0, 0))[0] + 13, v1.pt((m.L, 0, 16))[1] + 3, "montaje", 2.2, "start", DIM)
# v2 cotas: bolsillo
b0 = v2.pt((m.BOLS_X[0], 0, 0)); b1 = v2.pt((m.BOLS_X[1], 0, 0))
leds = [m.salida_led(hh) for (_, _, hh, _) in m.BARRERAS]
zmin = min(leds) - 3.5; zmax = max(leds) + 3.5
yb = v2.pt((0, 0, zb - m.LENG_OUT))[1]
cota(h, (b0[0], v2.pt((0, 0, zmin))[1]), (b1[0], v2.pt((0, 0, zmin))[1]), -(yb - v2.pt((0, 0, zmin))[1]) - 6, f"{fmt(m.BOLS_X[1]-m.BOLS_X[0])} (bolsillo, de x={fmt(m.BOLS_X[0])} a {fmt(m.BOLS_X[1])})", 'h')
cota(h, v2.pt((m.BOLS_X[0], 0, zmin)), v2.pt((m.BOLS_X[0], 0, zmax)), -6, fmt(zmax - zmin), 'v')
nota(h, v2.pt((80, 0, (zmin + zmax) / 2)), f"bolsillo de cableado, {fmt(m.BOLS_P)} de profundidad", 60, -12)
nota(h, v2.pt((m.RANURA_CABLE_X, 0, zb + 2)), "salida de cables 5 de ancho", -40, 14, anchor="end")
nota(h, v2.pt((m.BARRERAS[3][1], 0, m.salida_led(m.BARRERAS[3][2]))), "7× agujero LED Ø3,2 (eje ⟂ al canal, ver hoja 4)", -30, 18, anchor="end")
h.text(14, 190, "R = punto de referencia: suelo del canal junto a la pared de LEDs, en la cara trasera de la placa frontal.", 2.4, fill=QUIET)
h.text(14, 194.5, "X se mide desde R a lo largo del carril. Líneas grises a trazos = aristas ocultas.", 2.4, fill=QUIET)
hojas.append(h)

# ---------------- Hoja 4: secciones ----------------
h = Hoja(4, "Pieza A · Secciones", "Secciones por B3 y por P1", "3:1")
s = 3.0
ver_s, x_s = (-1, 0, 0), (0, -1, 0)   # mirando hacia el fondo; interior a la derecha
zt4 = m.yz(m.u_at_y0(m.H_INT), m.H_INT)[1]; zb4 = m.yz(m.u_at_y0(-m.T_SUELO), -m.T_SUELO)[1]
vs = Vista(h, None, ver_s, x_s, 62, 138, s)
dibuja_seccion(vs, seccion_face(A, 80.0, (zb4, zt4)))
dibuja_seccion(vs, seccion_face(AT, 80.0))
etiqueta(h, 62, 14, "SECCIÓN B-B (x = 80, barrera B3)")
# cotas seccion
def S(u, v):
    return vs.pt(PA(u, v, 80))
cota(h, S(0, 0), S(m.GAP, 0), -10, "3,4")
cota(h, S(m.GAP, 0), S(m.GAP + m.T_FOTO, 0), -10, "4")
cota(h, S(m.GAP + m.T_FOTO, -m.T_SUELO), S(m.GAP + m.T_FOTO, 0), -6, "3")
cota(h, S(m.GAP + m.T_FOTO, 0), S(m.GAP + m.T_FOTO, m.H_INT), -14, "32")
cota(h, S(m.GAP + m.T_FOTO, m.H_INT), S(m.GAP + m.T_FOTO, m.H_INT + m.T_TAPA), -6, "3")
cota(h, S(m.GAP + m.T_FOTO, 0), S(m.GAP + m.T_FOTO, 21.75), -24, "21,75 (altura B3)")
pY0 = vs.pt(mp((80, 0, 0))); pY8 = vs.pt(mp((80, m.Y0, 0)))
cota(h, (pY0[0], vs.pt(mp((80, 0, -6)))[1]), (pY8[0], vs.pt(mp((80, 0, -6)))[1]), 14, "8 (cuña a la altura del suelo)", 'h')
# angulo
c0 = S(0, 0)
top = S(0, 30)
h.line(c0[0], c0[1], c0[0], c0[1] - 95, QUIET, 0.15, "1.2 0.8")
arco(h, c0, 80, 90, 90 - m.BETA, "12°", 85)
# cara de montaje
pm0 = vs.pt(mp((80, 0, -10))); pm1 = vs.pt(mp((80, 0, 40)))
h.line(pm0[0], pm0[1], pm1[0], pm1[1], RED, 0.25, "2 1")
h.text(pm1[0] - 1, pm1[1] - 1, "cara de montaje (vertical)", 2.4, "end", RED)
nota(h, S(-1.5, 21.75), "LED IR Ø3,2 + diafragma Ø2 × 1,5", -18, -26, anchor="end")
nota(h, S(m.GAP + m.T_FOTO, 21.75 + 2.5), "ventana 2,5 × 5", 12, -30)
nota(h, S(m.GAP + m.T_FOTO, 21.75 - 8), "guía M2 Ø1,8 × 3,5", 32, 4)
nota(h, S(m.TAPA_U[0] + 2, m.H_INT + 1.5), "tapa A-T", 30, -6)
nota(h, S(-6, 4), "cuña maciza (medio trapecio)", -14, 16, anchor="end")
# seccion P1 (pequena, 2:1)
s2 = 2.0
vs2 = Vista(h, None, ver_s, x_s, 205, 92, s2)
dibuja_seccion(vs2, seccion_face(A, 50.0))
etiqueta(h, 228, 19, "SECCIÓN A-A (x = 50, P1) 2:1")
h.text(228, 107, "LED Ø3,2 · fototransistor fijo Ø3,2 + diafragma Ø2 × 0,6", 2.2, "middle", QUIET)
def S2(u, v):
    return vs2.pt(PA(u, v, 50))
cota(h, S2(m.GAP + m.T_FOTO, 0), S2(m.GAP + m.T_FOTO, 10), -6, "10")
# tabla de barreras
tx, ty = 150, 116
h.text(tx, ty, "Barreras (alturas medidas sobre la pared, desde el suelo del canal)", 2.8, weight="bold")
cols = [0, 14, 34, 58, 86, 116]
hdr = ["", "x desde R", "altura", "LED (pared)", "fototransistor", "z cara montaje"]
ty += 5
for c, t in zip(cols, hdr):
    h.text(tx + c, ty, t, 2.3, fill=QUIET, weight="bold")
for (n, x, hh, t) in m.BARRERAS:
    ty += 4.6
    vals = [n, fmt(x), f"{hh:.2f}".replace(".", ","), "Ø3,2 + Ø2", "fijo Ø3,2" if t == "fija" else "A-S regulable", fmt(m.salida_led(hh), 2)]
    for c, vv in zip(cols, vals):
        h.text(tx + c, ty, vv, 2.4, weight="bold" if c == 0 else "normal", fill=RED if c == 0 else INK)
h.line(tx, ty + 2, tx + 135, ty + 2, QUIET, 0.15)
h.para(tx, ty + 7, [
    "Los ejes de LED y fototransistor son perpendiculares a las paredes del canal (12° respecto a",
    "la horizontal de la cara de montaje). En el CAD: boceto en el plano de la sección y taladro",
    "\"perpendicular a cara\" desde la pared del canal.",
    "P1 y P2 abren y cierran la medida: las corta cualquier moneda.",
], 2.4, 3.8, QUIET)
hojas.append(h)

# ---------------- Hoja 5: placa frontal, tapa, portasensor ----------------
h = Hoja(5, "Pieza A · Placa · A-T · A-S", "Placa frontal, tapa y portasensor", "2:1 / 4:1")
s = 2.0
_c = mp(m.add(m.DATUM, m.N_PLACA, -m.T_PLACA / 2))
_slab = cq.Workplane("XY").box(m.T_PLACA - 0.02, 300, 300).rotate((0, 0, 0), (0, 1, 0), -m.ALFA).translate(_c)
PLACA = A.intersect(_slab)
vf = Vista(h, PLACA, (-m.ca, 0, -m.sa), (0, -1, 0), 42, 120, s, hidden=False)
etiqueta(h, 62, 14, "PLACA FRONTAL (vista de frente) 2:1")
def F(e, y):  # punto en el plano frontal de la placa: e = altura sobre R (vertical maquina), y = distancia a la pared
    o = m.add(m.DATUM, m.N_PLACA, -m.T_PLACA)
    p = m.add(o, m.E_UP, e)
    return mp((p[0], y, p[2]))
cota(h, vf.pt(F(m.PLACA_E[0], 0)), vf.pt(F(m.PLACA_E[0], 28)), 8, "28", 'h')
cota(h, vf.pt(F(m.PLACA_E[0], 28)), vf.pt(F(m.PLACA_E[1], 28)), -8, fmt(m.PLACA_E[1] - m.PLACA_E[0]), 'v')
cota(h, vf.pt(F(m.PLACA_E[0], 0)), vf.pt(F(0, 0)), 8, "12", 'v')
h.text(vf.pt(F(0, 0))[0] - 2, vf.pt(F(0, 0))[1] + 1, "R", 2.6, "end", RED, "bold")
nota(h, vf.pt(F(m.SLOT_V0 + 12, m.Y0 + 3)), "ranura 3,4 × 25,2 (girada 12°)", 14, -44)
nota(h, vf.pt(F(m.PLACA_E[1] - 3, 4)), "placa de 4 (= panel frontal)", 8, -10)
h.para(14, 168, [
    "La placa encaja a ras en un hueco del panel frontal de 28,4 × 58,4.",
    "La ranura empieza 3 por encima del suelo del canal: la moneda cae 3 mm y rueda.",
    "La placa está a 80° del suelo del canal (90° − 10°): montada queda vertical.",
], 2.4, 3.8, QUIET)
# tapa A-T: vista superior y seccion
s = 1.0
vt = Vista(h, AT, (0, 0, 1), (1, 0, 0), 112, 52, s)
etiqueta(h, 190, 34, "A-T · TAPA (planta 1:1)")
t0 = vt.pt(PA(m.TAPA_U[0], m.H_INT + m.T_TAPA, m.TAPA_X[0])); t1 = vt.pt(PA(m.TAPA_U[0], m.H_INT + m.T_TAPA, m.TAPA_X[1]))
cota(h, t0, t1, 7, fmt(m.TAPA_X[1] - m.TAPA_X[0]), 'h')
pa_ = vt.pt(PA(m.TAPA_U[0], m.H_INT + m.T_TAPA, m.TAPA_X[1])); pb_ = vt.pt(PA(m.TAPA_U[1], m.H_INT + m.T_TAPA, m.TAPA_X[1]))
cota(h, pa_, pb_, -6, fmt(m.TAPA_U[1] - m.TAPA_U[0]), 'v')
for xt in m.TAPA_TORN_X:
    pass
cota(h, vt.pt(PA(m.TAPA_TORN_U, m.H_INT + 3, m.TAPA_X[0])), vt.pt(PA(m.TAPA_TORN_U, m.H_INT + 3, m.TAPA_TORN_X[0])), -9, fmt(m.TAPA_TORN_X[0] - m.TAPA_X[0]), 'h')
cota(h, vt.pt(PA(m.TAPA_TORN_U, m.H_INT + 3, m.TAPA_TORN_X[0])), vt.pt(PA(m.TAPA_TORN_U, m.H_INT + 3, m.TAPA_TORN_X[1])), -9, fmt(m.TAPA_TORN_X[1] - m.TAPA_TORN_X[0]), 'h')
nota(h, vt.pt(PA(m.TAPA_TORN_U, m.H_INT + 3, m.TAPA_TORN_X[1])), "2× Ø2,4 pasante (M2 × 10)", 6, 10)
h.para(112, 78, [
    "Placa de 3 de grosor. Se apoya sobre la cuña y la pared de fototransistores,",
    f"perpendicular a las paredes del canal. Tornillos a {fmt(-m.TAPA_U[0] + m.TAPA_TORN_U)} del borde del lado de la pared.",
], 2.4, 3.8, QUIET)
# portasensor A-S: alzado (cara exterior) y perfil, 4:1
s = 4.0
va = Vista(h, AS, (0, 1, 0), (-1, 0, 0), 185, 130, s)
vb_ = Vista(h, AS, (1, 0, 0), (0, 1, 0), 232, 130, s)
etiqueta(h, 205, 97, "A-S · PORTASENSOR ×5 (4:1)")
h.text(185, 104, "cara interior (rendija)", 2.2, "middle", QUIET)
h.text(239, 104, "perfil", 2.2, "middle", QUIET)
cota(h, va.pt((-m.AS_W / 2, 0, m.AS_V[0])), va.pt((m.AS_W / 2, 0, m.AS_V[0])), 6, "9", 'h')
cota(h, va.pt((m.AS_W / 2, 0, m.AS_V[0])), va.pt((m.AS_W / 2, 0, m.AS_V[1])), 6, "17", 'v')
cota(h, va.pt((-m.AS_W / 2, 0, 0)), va.pt((-m.AS_W / 2, 0, m.AS_V[1])), -6, "5", 'v')
cota(h, va.pt((-m.AS_W / 2, 0, m.TORN_DV)), va.pt((-m.AS_W / 2, 0, 0)), -6, "8", 'v')
nota(h, va.pt((0, 0, 0)), "rendija 1 × 2,5 (0,6 de grosor)", -30, -10, anchor="end")
nota(h, va.pt((0, 0, m.TORN_DV)), "colisa 2,4 × 5 (M2): ±1,3 de ajuste", -30, 6, anchor="end")
cota(h, vb_.pt((0, 0, m.AS_V[0])), vb_.pt((0, m.AS_T, m.AS_V[0])), 6, "3", 'h')
nota(h, vb_.pt((0, 2, 0)), "Ø3,2 fototransistor", 10, -18)
h.text(112, 186, "Imprimir con la cara de la rendija sobre la cama.", 2.3, fill=QUIET)
hojas.append(h)

# ---------------- Hoja 6: pieza B ----------------
h = Hoja(6, "Pieza B · Cubilete", "Cubilete de espera sin fondo", "1:1")
s = 1.0
W = m.B_INT + 2 * m.B_T
vbf = Vista(h, B, (0, -1, 0), (1, 0, 0), 62, 70, s)          # desde el interior
etiqueta(h, 85, 16, "VISTA DESDE EL INTERIOR")
vbp = Vista(h, B, (0, 0, 1), (1, 0, 0), 62, 112, s)           # planta
etiqueta(h, 85, 100, "PLANTA (desde arriba)")
vbs = Vista(h, B, (-1, 0, 0), (0, -1, 0), 185, 70, s)        # de frente
etiqueta(h, 215, 16, "VISTA DE FRENTE")
iso_b = Vista(h, B, (-1, -1.1, 0.9), (1, -1, 0), 195, 150, 0.85, hidden=False, w=0.25)
# cotas interior
cota(h, vbf.pt((0, 0, 0)), vbf.pt((W, 0, 0)), 8, fmt(W), 'h')
cota(h, vbf.pt((-m.LENG_OUT, 0, 0)), vbf.pt((0, 0, 0)), 8, "13", 'h')
cota(h, vbf.pt((W, 0, 0)), vbf.pt((W, 0, m.B_H)), -24, "40", 'v')
cota(h, vbf.pt((m.B_PIV_X, 0, 0)), vbf.pt((m.B_PIV_X, 0, m.B_PIV_Z)), 0.01, "8", 'v')
cota(h, vbf.pt((0, 0, m.B_PIV_Z)), vbf.pt((m.B_PIV_X, 0, m.B_PIV_Z)), -0.01 - 12, "23 (eje trampilla)", 'h')
nota(h, vbf.pt((m.B_PIV_X, -m.B_T, m.B_PIV_Z)), "eje del servo = eje de la trampilla", 52, -18)
nota(h, vbf.pt((m.B_PIV_X - m.SG90_EJE_DESDE_EXT + 2, -W - m.SERVO_GAP, m.B_PIV_Z + 6)), "hueco SG90 22,8 × 12,6", -12, -14, anchor="end")
nota(h, vbf.pt((m.B_PIV_X - m.SG90_EJE_DESDE_EXT + 11.25 - 13.9, -W - m.SERVO_GAP, m.B_PIV_Z)), "2× Ø1,8 a 27,8 (tornillos del SG90)", -8, 16, anchor="end")
cota(h, vbf.pt((-m.LENG_OUT, 0, 27)), vbf.pt((-m.LENG_OUT, 0, 40)), -5, "13", 'v')
nota(h, vbf.pt((W + m.LENG_OUT - 6.5, 0, 33.5)), "4× Ø3,5 pasante (M3)", 6, -8)
# planta
cota(h, vbp.pt((0, 0, 40)), vbp.pt((0, -W, 40)), 8, fmt(W), 'v')
cota(h, vbp.pt((W, -W, 40)), vbp.pt((W, -W - m.SERVO_GAP, 40)), -8, "12", 'v')
cota(h, vbp.pt((W, -W - m.SERVO_GAP, 40)), vbp.pt((W, -W - m.SERVO_GAP - m.SERVO_T, 40)), -8, "3", 'v')
cota(h, vbp.pt((m.B_T, -m.B_T, 40)), vbp.pt((W - m.B_T, -m.B_T, 40)), -0.01 - 14, "40 interior", 'h')
nota(h, vbp.pt((0, 0, 40)), "cara de montaje (pared lateral)", -4, -8, anchor="end")
# frente
nota(h, vbs.pt((m.B_PIV_X, -m.B_T - 1.5, m.B_PIV_Z)), "pivote Ø3 × 3 (lado pared)", -6, -30, anchor="end")
nota(h, vbs.pt((m.B_PIV_X, -W + 1.5, m.B_PIV_Z)), "agujero del eje Ø4,4", 6, -38)
cota(h, vbs.pt((0, -W, 0)), vbs.pt((0, -W - m.SERVO_GAP - m.SERVO_T, 0)), 8, "15", 'h')
cota(h, vbs.pt((0, -W - m.SERVO_GAP, 0)), vbs.pt((0, -W - m.SERVO_GAP, m.B_PIV_Z + m.SG90_BODY[1] / 2 + 8)), -6, fmt(m.B_PIV_Z + m.SG90_BODY[1] / 2 + 8), 'v')
h.para(14, 186, [
    "Las medidas del SG90 son las típicas (cuerpo 22,5 × 12,2, agujeros a 27,8, eje a 5,9 de un extremo): comprobadlas con vuestro servo.",
    "Trampilla (siguiente pieza): 38,4 × 38,4 × 2, gira sobre el pivote Ø3 y la mueve un eje Ø4 unido al brazo del servo.",
], 2.4, 3.8, QUIET)
hojas.append(h)

# ---------------- Hoja 7: impresion y montaje ----------------
h = Hoja(7, "Impresión y montaje", "Bambu Lab A1 · PLA", "—")
h.text(12, 16, "Impresión", 5, weight="bold")
h.para(12, 25, [
    "**Ajustes comunes (PLA, boquilla 0,4)",
    "Capa 0,2 · 3 perímetros · relleno 15 % giroide · sin soportes en ninguna pieza.",
    "",
    "**Orientación",
    "A   De pie, con la cara frontal de la placa sobre la cama (el carril sube 150).",
    "     Así el canal y las paredes salen verticales y la ranura queda limpia.",
    "     Usad borde (brim) de 5 mm: la base es pequeña para la altura.",
    "A-T Plana, cara superior hacia arriba.",
    "A-S Plana, con la cara de la rendija sobre la cama (la rendija sale en las 3 primeras capas).",
    "B   De pie, con el borde abierto sobre la cama. Las lengüetas altas llevan chaflán a 45°.",
    "",
    "**Antes de la pieza grande, imprimid una probeta",
    "Un trozo de canal de 30 de largo con la ranura: comprobad que pasa el 50c (24,25)",
    "y no el 2 € (25,75), y que el hueco mide 3,2 ± 0,1. Si no, ajustad GAP y SLOT_H.",
], 2.8, 4.6)
h.text(155, 16, "Montaje", 5, weight="bold")
h.para(155, 25, [
    "1. LEDs desde la cara de montaje, hasta el tope del diafragma.",
    "    Cables por el bolsillo y salida inferior; fijad con una gota de cola.",
    "2. Fototransistores P1 y P2 desde el interior, a tope.",
    "3. Portasensores A-S en B1 a B5 con M2 × 6, sin apretar.",
    "4. Atornillad A a la pared con 6 M3. En pared de PLA: insertos de",
    "    latón M3 (agujero Ø4,0 × 5) o tuerca por el otro lado.",
    "5. Calibrad B1 a B5 con monedas reales (rampa-monedas.md) y apretad.",
    "6. Tapa A-T con 2 M2 × 10.",
    "7. Cubilete B con 4 M3, debajo del final del carril.",
], 2.8, 4.6)
# tabla de agujeros en la pared
h.text(155, 78, "Agujeros en la pared lateral (centro de cada lengüeta)", 3.2, weight="bold")
h.text(155, 83, "fondo = desde la cara exterior del frontal · altura = desde el suelo de la máquina", 2.3, fill=QUIET)
rows = []
zt = m.yz(m.u_at_y0(m.H_INT), m.H_INT)[1]; zb = m.yz(m.u_at_y0(-m.T_SUELO), -m.T_SUELO)[1]
for xl in m.LENG_X:
    for lado, zc in (("sup", zt + m.LENG_OUT - 6.5), ("inf", zb - m.LENG_OUT + 6.5)):
        d, hh, _ = m.maquina_A((xl, 0, zc))
        rows.append((f"A {lado} x={fmt(xl)}", d, hh))
for (z0, z1) in m.B_LENG_Z:
    for lado, xc in (("del.", -m.LENG_OUT + 6.5), ("tras.", W + m.LENG_OUT - 6.5)):
        d, hh, _ = m.maquina_B((xc, 0, (z0 + z1) / 2))
        rows.append((f"B {lado} z={fmt((z0 + z1) / 2)}", d, hh))
ty = 90
h.text(155, ty, "agujero", 2.4, fill=QUIET, weight="bold"); h.text(205, ty, "fondo", 2.4, fill=QUIET, weight="bold"); h.text(228, ty, "altura", 2.4, fill=QUIET, weight="bold")
for r in rows:
    ty += 4.2
    h.text(155, ty, r[0], 2.4); h.text(205, ty, fmt(r[1]), 2.4); h.text(228, ty, fmt(r[2]), 2.4)
h.text(155, ty + 6, f"Supone R a {fmt(m.H0, 0)} del suelo y placa de {fmt(m.T_PLACA, 0)} a ras del frontal.", 2.3, fill=QUIET)
h.text(155, ty + 10, "Los 6 agujeros de A quedan sobre líneas inclinadas 10°: así sale la pendiente.", 2.3, fill=QUIET)
h.text(12, 105, "Comprobaciones después de montar", 4, weight="bold")
h.para(12, 113, [
    "· Con un nivel de burbuja o el móvil: suelo del canal a 10° ± 1° y cara de los",
    "  fototransistores a 12° ± 1° de la vertical.",
    "· Cada moneda rueda de la ranura al cubilete sin pararse ni saltar (20 pasadas).",
    "· Ninguna moneda roza la tapa (si roza, revisad el grosor de la primera capa).",
    "· El final del carril queda dentro del cubilete visto desde arriba.",
    "· Con la tapa puesta, en la oscuridad del interior, cada fototransistor da",
    "  señal clara tapado / destapado (polímetro).",
], 2.8, 4.6)
hojas.append(h)

for hh in hojas:
    open(f"{OUT}/hoja{hh.n}.svg", "w").write(hh.svg())
print("hojas", len(hojas))
