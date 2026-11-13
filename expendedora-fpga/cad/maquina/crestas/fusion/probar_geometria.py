"""Construye las operaciones del script de Fusion con CadQuery y las compara con crestas.py (diferencia en mm3)."""
import sys, cadquery as cq
sys.path[:0] = ["CrestasSED", ".."]
import CrestasSED as F, crestas as CR
EJ = "xyz"
def prism(eje, pts, c0, c1):
    i = EJ.index(eje); lo, hi = min(c0, c1), max(c0, c1)
    P3 = [cq.Vector(*[(lo if k == i else p[k]) for k in range(3)]) for p in pts]
    f = cq.Face.makeFromWires(cq.Wire.makePolygon(P3 + [P3[0]]))
    d = [0, 0, 0]; d[i] = hi - lo
    return cq.Solid.extrudeLinear(f, cq.Vector(*d))
def tool(t, sy):
    _, p0, d, dia, length = t
    return cq.Solid.makeCylinder(dia / 2, length, cq.Vector(*F.espejo(p0, sy)), cq.Vector(*F.espejo(d, sy)))
def construir(ops, sy):
    body = None
    for op in ops:
        if op[0] in ("nuevo", "boceto"):
            if op[0] == "nuevo": _, n, eje, pts, c0, c1 = op; o = "nuevo"
            else: _, n, o, eje, pts, c0, c1 = op
            if eje == "y": c0, c1 = c0 * sy, c1 * sy
            s = prism(eje, [F.espejo(p, sy) for p in pts], c0, c1)
        else:
            _, n, o, tools = op; s = None
            for t in tools:
                ti = tool(t, sy); s = ti if s is None else s.fuse(ti)
        body = s if o == "nuevo" else (body.fuse(s).clean() if o == "unir" else body.cut(s).clean())
    return body
ref = {"CR-1_cresta1": CR.cresta("cresta1")[0].val(), "CR-2_cresta2": CR.cresta("cresta2")[0].val(), "CR-3_canal": CR.canal()[0].val()}
for n, ops, sy, d in F.piezas():
    b = construir(ops, sy); r = ref[n].mirror("XZ") if sy < 0 else ref[n]
    diff = b.cut(r).Volume() + r.cut(b).Volume()
    print(f"{n}: vol {b.Volume()/1000:.2f} cm3 (esperado {F.VOL_ESPERADO[n]}), ref {r.Volume()/1000:.2f}, diferencia {diff:.3f} mm3, valido {b.isValid()}")
# Cada "unir" debe tocar el cuerpo acumulado (si no, Fusion crea un cuerpo aparte)
for n, ops, sy, d in F.piezas():
    body = None
    for op in ops:
        if op[0] == "herramientas": continue
        if op[0] == "nuevo": _, nm, eje, pts, c0, c1 = op; o = "nuevo"
        else: _, nm, o, eje, pts, c0, c1 = op
        if eje == "y": c0, c1 = c0 * sy, c1 * sy
        s = prism(eje, [F.espejo(p, sy) for p in pts], c0, c1)
        if o == "unir" and body.intersect(s).Volume() < 1e-3:
            print(f"  ¡¡ {n} > {nm}: no toca el cuerpo, Fusion lo dejaría aparte")
        body = s if o == "nuevo" else body.fuse(s)
    print(f"  {n}: todas las uniones tocan el cuerpo" if True else "")
