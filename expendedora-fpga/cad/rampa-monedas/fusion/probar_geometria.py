import sys, cadquery as cq
sys.path.insert(0, "MonedasSED"); sys.path.insert(0, "../cad")
import MonedasSED as F, modelo as M
EJ = "xyz"
def prism(eje, pts, c0, c1):
    i = EJ.index(eje); lo, hi = min(c0, c1), max(c0, c1)
    pl = {"x": "YZ", "y": "XZ", "z": "XY"}[eje]
    # coordenadas 2D en el plano y extrusion generica: construir con makePolygon + extrude vector
    P3 = [cq.Vector(*[(lo if k == i else p[k]) for k in range(3)]) for p in pts]
    w = cq.Wire.makePolygon(P3 + [P3[0]])
    f = cq.Face.makeFromWires(w)
    d = [0, 0, 0]; d[i] = hi - lo
    return cq.Solid.extrudeLinear(f, cq.Vector(*d))
def tool(t, sy):
    if t[0] == "box":
        _, c, ld, wd, l, w, h = t
        c, ld, wd = F.espejo(c, sy), F.espejo(ld, sy), F.espejo(wd, sy)
        X = cq.Vector(*ld).normalized(); Y = cq.Vector(*wd).normalized(); Z = X.cross(Y)
        pl = cq.Plane(origin=cq.Vector(*c), xDir=X, normal=Z)
        return cq.Workplane(pl).box(l, w, h).val()
    _, p0, d, dia, length = t
    return cq.Solid.makeCylinder(dia / 2, length, cq.Vector(*F.espejo(p0, sy)), cq.Vector(*F.espejo(d, sy)))
def construir(ops, sy):
    body = None
    for op in ops:
        if op[0] in ("nuevo", "boceto"):
            if op[0] == "nuevo":
                _, n, eje, pts, c0, c1 = op; o = "nuevo"
            else:
                _, n, o, eje, pts, c0, c1 = op
            if eje == "y": c0, c1 = c0 * sy, c1 * sy
            s = prism(eje, [F.espejo(p, sy) for p in pts], c0, c1)
        else:
            _, n, o, tools = op
            s = None
            for t in tools:
                ti = tool(t, sy); s = ti if s is None else s.fuse(ti)
        if o == "nuevo": body = s
        elif o == "unir": body = body.fuse(s).clean()
        else: body = body.cut(s).clean()
    return body
mir = lambda s: s.mirror("XZ")
ref = {"A_carril": mir(M.cuerpo_A().val()), "A-F_pared_foto": mir(M.pared_AF().val()), "A-T_tapa": mir(M.tapa_AT().val()),
       "A-S_portasensor": M.portasensor_AS().val(), "B_cubilete": mir(M.cubilete_B().val()),
       "B-TP_trampilla_pared": mir(M.trampilla_TP().val()), "B-TS_trampilla_servo": mir(M.trampilla_TS().val()),
       "B-PZ_postizo": mir(M.postizo().val()), "B-AC_acople_servo": mir(M.acople_servo().val())}
for n, ops, sy, d in F.piezas():
    b = construir(ops, sy)
    r = ref[n]
    diff = b.cut(r).Volume() + r.cut(b).Volume()
    print(f"{n}: vol {b.Volume()/1000:.2f} cm3, ref {r.Volume()/1000:.2f}, diferencia {diff:.3f} mm3, valido {b.isValid()}")
