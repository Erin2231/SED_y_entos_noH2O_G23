"""Crestas en U (tipo pista Hot Wheels) y caja del canal de no válidas. PLA.
Ejes de la máquina (mm): x = fondo desde la cara exterior del frontal, y = lateral desde la cara interior
de la pared lateral de la columna (y = 0 es esa pared), z = altura desde la cara inferior del suelo.
Mismas cotas que el plano del corte 1 (cad/maquina/corte1). Se fijan como el cubilete B y el carril A:
lengüetas de 3 mm con agujero Ø3,5 para M3, apoyadas en la pared lateral (y = 0)."""
import math, cadquery as cq

# ---- parámetros comunes (iguales que en rampa-monedas/modelo.py) ----
T = 3.0              # grosor de pared, suelo y lengüetas (= B_T, T_LENG)
D_M3 = 3.5           # agujero M3
LENG_W, LENG_OUT, LENG_AG = 14.0, 13.0, 6.5   # ancho, cuánto sobresale, agujero a 6,5 del borde libre
ANCHO = 46.0         # ancho lateral de crestas y canal (= cubiletes B y C)
H_U = 15.0           # altura de las paredes de la U sobre el suelo del carril (2 € de canto: centro a 12,9)
ANG = 30.0
tg, c30 = math.tan(math.radians(ANG)), math.cos(math.radians(ANG))

# ---- posiciones (plano corte 1, tabla T2) ----
CRESTAS = {
    "cresta1": dict(vert=(162.721, 255.953), x0=128.0, x1=200.0),   # Λ-B, bajo el cubilete B
    "cresta2": dict(vert=(223.0, 163.0), x0=70.0, x1=280.0),         # Λ-C, bajo el cubilete C
}
CAN_F = (97.0, 100.0, 118.0, 262.0)     # chapa delantera del canal: x0, x1, z0, z1

def z_sup(cr, x):
    """cara de arriba del suelo del carril"""
    xv, zv = cr["vert"]; return zv - abs(x - xv) * tg

def _prisma(pts, y0, y1):
    w = cq.Workplane("XZ", origin=(0, y0, 0)).polyline(pts).close().extrude(-(y1 - y0))
    return w

def _perfil(cr, dz_top, dz_bot):
    """polígono entre la recta desplazada dz_top y dz_bot (en vertical) del perfil Λ"""
    x0, x1 = cr["x0"], cr["x1"]; xv, _ = cr["vert"]
    top = [(x, z_sup(cr, x) + dz_top) for x in (x0, xv, x1)]
    bot = [(x, z_sup(cr, x) + dz_bot) for x in (x1, xv, x0)]
    return top + bot

def cresta(nombre):
    cr = CRESTAS[nombre]
    tv = T / c30; hv = H_U / c30                                  # grosores perpendiculares 3 y 15
    s = _prisma(_perfil(cr, 0.0, -tv), 0.0, ANCHO)                # suelo del carril
    for y0 in (0.0, ANCHO - T):                                   # paredes de la U
        s = s.union(_prisma(_perfil(cr, hv, -tv), y0, y0 + T))
    # 3 lengüetas hacia abajo, en el plano de la pared lateral (y 0..3): vértice + una en cada rampa
    xv = cr["vert"][0]
    xs = (xv, (cr["x0"] + xv) / 2, (xv + cr["x1"]) / 2)
    agujeros = []
    for xc in xs:
        xa, xb = xc - LENG_W / 2, xc + LENG_W / 2
        zlow = min(z_sup(cr, xa), z_sup(cr, xb)) - tv          # punto más bajo de la cara inferior en el ancho
        zb = zlow - LENG_OUT
        pts = [(xa, z_sup(cr, xa) - tv / 2), (xb, z_sup(cr, xb) - tv / 2), (xb, zb), (xa, zb)]
        if xa < xv < xb: pts.insert(1, (xv, z_sup(cr, xv) - tv / 2))
        s = s.union(_prisma(pts, 0.0, T))
        za = zb + LENG_AG
        s = s.cut(cq.Workplane("XZ", origin=(xc, -1, za)).circle(D_M3 / 2).extrude(-(T + 2)))
        agujeros.append((round(xc, 1), round(za, 1)))
    return s, agujeros

def canal():
    """caja de 3 lados: chapa delantera, trasera y pared del fondo (lat 43-46); la 4ª es la pared de la máquina"""
    cr = CRESTAS["cresta1"]
    xf0, xf1, zf0, zf1 = CAN_F
    xb0, xb1 = cr["x0"], cr["x0"] + T
    zb0 = 137.0
    zb1 = round(min(z_sup(cr, xb0), z_sup(cr, xb1)) - T / c30 - 0.5, 1)   # 0,5 por debajo de la cresta 1
    caja = cq.Workplane("XY").box(xf1 - xf0, ANCHO, zf1 - zf0, centered=False).translate((xf0, 0, zf0))
    caja = caja.union(cq.Workplane("XY").box(xb1 - xb0, ANCHO, zb1 - zb0, centered=False).translate((xb0, 0, zb0)))
    caja = caja.union(_prisma([(xf0, zf0), (xf0, zf1), (xb0, zb1), (xb1, zb1), (xb1, zb0)], ANCHO - T, ANCHO))
    agujeros = []
    for (xe, lado, zs) in ((xf0, -1, (135.0, 245.0)), (xb1, 1, (150.0, 215.0))):
        for zc in zs:
            xo = xe + LENG_OUT * lado
            x_in = xe - T * lado if lado < 0 else xe - T             # la lengüeta pisa la chapa
            xlo, xhi = min(xo, xe + (T if lado < 0 else -T)), max(xo, xe + (T if lado < 0 else -T))
            tab = cq.Workplane("XY").box(xhi - xlo, T, LENG_W, centered=False).translate((xlo, 0, zc - LENG_W / 2))
            caja = caja.union(tab)          # oreja simple, igual que las de las crestas
            xh = xe + (LENG_OUT - LENG_AG) * lado
            caja = caja.cut(cq.Workplane("XZ", origin=(xh, -1, zc)).circle(D_M3 / 2).extrude(-(T + 2)))
            agujeros.append((xh, zc))
    return caja, agujeros, zb1

if __name__ == "__main__":
    import os
    os.makedirs("step", exist_ok=True); os.makedirs("stl", exist_ok=True)
    piezas = {}
    c1, h1 = cresta("cresta1"); c2, h2 = cresta("cresta2"); ca, h3, zb1 = canal()
    for n, (w, h) in {"CR-1_cresta1": (c1, h1), "CR-2_cresta2": (c2, h2), "CR-3_canal": (ca, h3)}.items():
        v = w.val(); bb = v.BoundingBox()
        print(f"{n}: valido {v.isValid()} vol {v.Volume()/1000:.1f} cm3 bbox {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  taladros (x,z) {h}")
        cq.exporters.export(w, f"step/{n}.step"); cq.exporters.export(w, f"stl/{n}.stl", tolerance=0.02, angularTolerance=0.1)
        piezas[n] = w
    print("chapa trasera del canal hasta z", zb1)
