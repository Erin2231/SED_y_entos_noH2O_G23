"""Plano a escala del corte 1 (columna de monedas). Unidades mm; hoja A4 vertical, escala 1:2."""
import sys, math
sys.path.insert(0, "../../rampa-monedas")
import cadquery as cq, modelo as M
# Corte quebrado (distancia a la pared lateral de la columna): monedas por su recorrido, el resto por el centro de la columna
YCUT = {"A": 9.5, "A-T": 9.5, "A-F": 13.0, "B": 12.0, "B-TP": 12.0, "C": 12.0, "C-TP": 12.0}
H, W, D, T = 420.0, 330.0, 330.0, 8.0
DX, DZ = M.DATUM[0], M.DATUM[2]
def toA(s): return s.translate(cq.Vector(-DX, 0, -DZ)).rotate(cq.Vector(), cq.Vector(0, 1, 0), M.ALFA).translate(cq.Vector(M.T_PLACA, 0, M.H0))
def toB(s, dx=0.0, dz=0.0): return s.translate(cq.Vector(M.B_D0 + dx, 0, M.B_TOP_H - M.B_H + dz))
def box(x0, x1, z0, z1, y0=-5.0, y1=120.0): return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))
def prism(pts, y0=0.0, y1=110.0):
    w = cq.Wire.makePolygon([cq.Vector(x, y0, z) for x, z in pts] + [cq.Vector(pts[0][0], y0, pts[0][1])])
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(0, y1 - y0, 0))
def plate_line(p0, p1, t=3.0, below=True):
    """chapa de grosor t bajo la recta p0-p1 (rampa)"""
    (x0, z0), (x1, z1) = p0, p1; L = math.hypot(x1 - x0, z1 - z0); nx, nz = (z1 - z0) / L, -(x1 - x0) / L
    if nz > 0: nx, nz = -nx, -nz
    return prism([(x0, z0), (x1, z1), (x1 + nx * t, z1 + nz * t), (x0 + nx * t, z0 + nz * t)])

# ---------- piezas del modelo (diseñadas) ----------
P = {}
P["A"] = toA(M.cuerpo_A().val()); P["A-F"] = toA(M.pared_AF().val()); P["A-T"] = toA(M.tapa_AT().val())
P["B"] = toB(M.cubilete_B().val())
P["B-TP"] = toB(M.trampilla_TP().val())
B_PIV_H = M.B_TOP_H - M.B_H + M.B_PIV_Z
B_PIV_D = M.B_D0 + M.B_PIV_X
# ---------- piezas previstas (por diseñar) ----------
# C = cubilete B exacto (misma pieza), desplazado
C_X0, C_H, C_Z0 = 200.0, M.B_H, 183.0
_cdx, _cdz = C_X0 - M.B_D0, C_Z0 - (M.B_TOP_H - M.B_H)
P["C"] = toB(M.cubilete_B().val(), _cdx, _cdz)
P["C-TP"] = toB(M.trampilla_TP().val(), _cdx, _cdz)
Q = {}
C_PIV_H, C_PIV_D = C_Z0 + M.B_PIV_Z, C_X0 + M.B_PIV_X
ANG = 30.0                      # rampas a 30° (crestas de 120°)
tg = math.tan(math.radians(ANG))
TR = 3.0                        # grosor de crestas y rampas
def cresta(xa, za, x_front, x_back, t=TR):
    zf, zb = za - (xa - x_front) * tg, za - (x_back - xa) * tg
    tc = t / math.cos(math.radians(ANG))
    return prism([(x_front, zf), (xa, za), (x_back, zb), (x_back, zb - tc), (xa, za - tc), (x_front, zf - tc)], 1, 109)
LB = (B_PIV_D, B_PIV_H - 28.0)        # Λ-B 12 más baja (Ian): 20 de paso bajo B
LB_X = (128.0, 200.0)
Q["Λ-B"] = cresta(LB[0], LB[1], *LB_X)
LC = (C_PIV_D, 163.0)                  # Λ-C no se mueve; C sube 12 (Ian): 20 de paso bajo C
LC_X = (70.0, 280.0)
Q["Λ-C"] = cresta(LC[0], LC[1], *LC_X)
z_at = lambda x0, z0, x: z0 - abs(x - x0) * tg
CAN = dict(f=(97.0, 100.0, 118.0, 262.0), b=(128.0, 131.0, 137.0, round(z_at(LB[0], LB[1], 128.0), 1)))
Q["canal"] = box(CAN["f"][0], CAN["f"][1], CAN["f"][2], CAN["f"][3], 1, 109).fuse(box(CAN["b"][0], CAN["b"][1], CAN["b"][2], CAN["b"][3], 1, 109))
# cajones iguales (devolución y hucha): frente 8 + caja 67 = 75 de fondo, 57 de alto, 104 de ancho, paredes 2,5
CJ = dict(L=75.0, Hc=57.0, Wc=104.0, t=2.5, fr=8.0)
def cajon(x_frente, sentido):
    x0 = x_frente if sentido > 0 else x_frente - CJ["L"]
    s = box(x0, x0 + CJ["L"], T, T + CJ["Hc"], 3, 3 + CJ["Wc"])
    if sentido > 0: hueco = box(x0 + CJ["fr"], x0 + CJ["L"] - CJ["t"], T + CJ["t"], T + CJ["Hc"] + 5, 3 + CJ["t"], 3 + CJ["Wc"] - CJ["t"])
    else: hueco = box(x0 + CJ["t"], x0 + CJ["L"] - CJ["fr"], T + CJ["t"], T + CJ["Hc"] + 5, 3 + CJ["t"], 3 + CJ["Wc"] - CJ["t"])
    return s.cut(hueco)
Q["cajón devolución"] = cajon(0.0, 1)
Q["hucha"] = cajon(D, -1)
Q["topes"] = box(75.0, 80.0, T, T + 10, 3, 107).fuse(box(250.0, 255.0, T, T + 10, 3, 107))   # topes de los cajones, pegados al suelo
K = {}
K["suelo"] = box(0, D, 0, T); K["techo"] = box(0, D, H - T, H)
front_hole = (300.0, 400.0)   # hueco del frontal para la placa de A (z)
OPEN = dict(z0=T, z1=T + CJ["Hc"] + 2)        # abertura de los cajones en frontal y trasera
K["frontal"] = box(0, T, OPEN["z1"], 339.5).fuse(box(0, T, 398.5, H - T)).cut(box(-1, T + 1, 170, 182)).cut(box(-1, T + 1, 290, 314))
K["trasera"] = box(D - T, D, OPEN["z1"], H - T)
E = {}
E["LCD bisel"] = box(1, T, 290, 314, 15, 86); E["LCD placa"] = box(T, T + 1.6, 284, 320, 11, 91); E["LCD conectores"] = box(T + 1.6, T + 5.5, 286, 318, 13, 89)
E["numpad"] = box(-1, 0, 200, 277, 20, 90)
# pulsador de cancelar: táctil 6x6 (inventario) + embellecedor PC-E + soporte PC-S pegado al frontal (cad/maquina/pulsador)
E["embellecedor"] = box(-3, T, 170.25, 181.75, 49.25, 60.75).fuse(box(T, T + 1.5, 168, 184, 47, 63))
E["pulsador"] = box(T + 1.6, T + 3.1, 174.25, 177.75, 53.25, 56.75).fuse(box(T + 3.1, T + 6.6, 173, 179, 52, 58))
E["soporte pulsador"] = box(T, T + 8.6, 163, 189, 42, 68).cut(box(T - 1, T + 2, 167.5, 184.5, 46.5, 63.5)).cut(box(T + 1.9, T + 6.6, 172.8, 179.2, 51, 59))

def _pts(w):
    n = max(8, 6 * len(w.Edges()))
    out = []
    for e in w.Edges():
        k = 1 if e.geomType() == "LINE" else 16
        ps = [e.positionAt(i / k) for i in range(k + 1)]
        out.append([(p.x, p.z) for p in ps])
    # ordenar aristas encadenándolas
    chain = out.pop(0)
    while out:
        last = chain[-1]; best = None
        for i, seg in enumerate(out):
            for rev in (False, True):
                q = seg[::-1] if rev else seg
                d = (q[0][0] - last[0]) ** 2 + (q[0][1] - last[1]) ** 2
                if best is None or d < best[0]: best = (d, i, q)
        chain += best[2][1:]; out.pop(best[1])
    return chain

def corte(s, yc):
    sl = s.intersect(cq.Solid.makeBox(400, 0.02, 600, cq.Vector(-30, yc - 0.01, -50)))
    res = []
    for f in sl.Faces():
        if f.normalAt().y < -0.9:
            res.append([_pts(f.outerWire())] + [_pts(w) for w in f.innerWires()])
    return res

if __name__ == "__main__":
    import json
    res = {}
    for grp, dd in (("modelo", P), ("previsto", Q), ("carcasa", K), ("comprado", E)):
        for n, sol in dd.items():
            yc = YCUT.get(n, 55.0)
            fs = corte(sol, yc); res[n] = (grp, fs, yc); print(n, grp, len(fs), yc)
    json.dump(res, open("corte1.json", "w"))
    json.dump(dict(B_PIV=(B_PIV_D, B_PIV_H), C_PIV=(C_PIV_D, C_PIV_H), LB=LB, LC=LC, LB_X=LB_X, LC_X=LC_X, C=(C_X0, C_Z0, C_H), FIN=M.FIN_CARRIL, CAN=CAN, CJ=CJ, OPEN=OPEN, ANG=ANG), open("ref.json", "w"))
