"""Comprueba que las crestas y el canal no chocan con nada (trampillas a 0, ±20 y ±40°). Ejecutar desde esta carpeta."""
import sys; sys.path[:0] = ["../corte1", "../../rampa-monedas"]
import cadquery as cq
import plano1 as PL, crestas as CR
c1, _ = CR.cresta("cresta1"); c2, _ = CR.cresta("cresta2"); ca, _, _ = CR.canal()
for n, w in (("c1", c1), ("c2", c2), ("ca", ca)):
    b = w.val().BoundingBox(); print(n, "y", round(b.ymin, 2), round(b.ymax, 2), "x", round(b.xmin,1), round(b.xmax,1), "z", round(b.zmin,1), round(b.zmax,1))
P = PL.P
def tp(name, piv, ang):
    return P[name].rotate(cq.Vector(piv[0], 0, piv[1]), cq.Vector(piv[0], 1, piv[1]), ang)
otros = {"A": P["A"], "A-F": P["A-F"], "A-T": P["A-T"], "B": P["B"], "C": P["C"], "suelo": PL.K["suelo"], "frontal": PL.K["frontal"],
         "caj_dev": PL.Q["cajón devolución"], "hucha": PL.Q["hucha"], "topes": PL.Q["topes"], "pulsador_sop": PL.E["soporte pulsador"]}
for a in (0, 20, 40, -20, -40):
    otros[f"B-TP{a}"] = tp("B-TP", (PL.B_PIV_D, PL.B_PIV_H), a)
    otros[f"C-TP{a}"] = tp("C-TP", (PL.C_PIV_D, PL.C_PIV_H), a)
mine = {"c1": c1.val(), "c2": c2.val(), "ca": ca.val()}
bad = 0
for n, s in mine.items():
    for m, o in otros.items():
        v = s.intersect(o).Volume()
        if v > 0.01: print("CHOQUE", n, m, round(v, 2)); bad += 1
for a, b in (("c1", "c2"), ("c1", "ca"), ("c2", "ca")):
    v = mine[a].intersect(mine[b]).Volume()
    if v > 0.01: print("CHOQUE", a, b, round(v, 2)); bad += 1
# holgura mínima vertical bajo los cubiletes
print("choques:", bad)
