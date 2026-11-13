import modelo as m, cadquery as cq, math
A=m.cuerpo_A().val(); F=m.pared_AF().val(); T=m.tapa_AT().val(); B=m.cubilete_B().val()
print("== solapes entre piezas montadas (mm3)")
print(" A-F", round(A.intersect(F).Volume(),3), " A-T", round(A.intersect(T).Volume(),3), " F-T", round(F.intersect(T).Volume(),3))
print("== portasensores A-S en su carril, posiciones extremas (-1,3 / 0 / +1,3)")
u0 = m.GAP + m.T_FOTO - m.GUIA_AS_P
worst = 0; vecinos = []
for (n, x, h, t) in m.BARRERAS:
    if t != "regulable": continue
    for d in (-1.3, 0, 1.3):
        s = m.prism_uv(u0 + 0.001, u0 + m.AS_T, h + d + m.AS_V[0], h + d + m.AS_V[1], x - m.AS_W / 2, x + m.AS_W / 2).val()
        for nm, other in (("A-F", F), ("A", A), ("A-T", T)):
            v = s.intersect(other).Volume()
            if v > 1e-3: print("  CHOQUE", n, d, nm, round(v, 3))
        worst = max(worst, h + d + m.AS_V[1])
    vecinos.append(x)
print("  A-S mas alto llega a v =", round(worst + 0, 2), "(tapa empieza en v =", m.H_INT, ")")
print("  hueco entre A-S vecinos:", min(b - a for a, b in zip(vecinos, vecinos[1:])) - m.AS_W, "mm")
print("  A-S mas bajo empieza en v =", round(min(h - 1.3 + m.AS_V[0] for (_, _, h, t) in m.BARRERAS if t == 'regulable'), 2), "(ala hasta v =", m.FL_T, ")")
print("  carril guia de", m.GUIA_AS_V0, "a la parte de arriba; A-S ocupa de", m.AS_V[0]-1.3, "a", m.AS_V[1]+1.3)
print("  ventana +-", m.VENT_H/2, " rendija +-", m.AS_RENDIJA[0]/2, "+ recorrido 1,3 ->", m.AS_RENDIJA[0]/2+1.3)
print("  colisa", m.AS_COLISO, "-> recorrido con M2 (2,1) +-", round((m.AS_COLISO[1]-2.1)/2,2))
print("  tornillo M2x6: 3 en A-S + 3 en pared; guia", m.T_FOTO - m.GUIA_AS_P - 0.5, "mm; piel hasta canal 0,5")
print("== agujeros LED: largo desde el fondo del bolsillo (y=3) hasta el diafragma")
for (n, x, h, t) in m.BARRERAS:
    u_floor = (m.BOLS_P - m.Y0 - h * m.sb) / m.cb
    print(f"  {n}: {(-m.L_APER - u_floor):.2f} mm (LED 3 mm: cuerpo ~4,6-5,3 desde la pestaña)")
print("== cubilete: hueco SG90 x", m.SG90_BODY, "frente a cuerpo real ~22,2-22,5 x 11,8-12,2")
x_body0 = m.B_PIV_X - m.SG90_EJE_DESDE_EXT
xc = x_body0 + 22.5 / 2
print("  agujeros SG90 en x =", round(xc - 13.9, 2), round(xc + 13.9, 2), "; orejas de", round(xc - 16.1, 2), "a", round(xc + 16.1, 2), "; placa de", m.B_T, "a", m.B_INT + 2 * m.B_T)
