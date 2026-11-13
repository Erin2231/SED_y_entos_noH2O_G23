import cadquery as cq, modelo as M
B = M.cubilete_B().val()
TP, TS, AC = M.trampilla_TP().val(), M.trampilla_TS().val(), M.acople_servo().val()
PZ1 = M.postizo().val(); PZ2 = PZ1.mirror("YZ", cq.Vector(M.B_PIV_X, 0, 0))
ax0, axd = cq.Vector(M.B_PIV_X, 0, M.B_PIV_Z), cq.Vector(0, 1, 0)
inter = lambda a, b: a.intersect(b).Volume()
print("TP∩TS", round(inter(TP, TS), 4), " AC∩TS", round(inter(AC, TS), 4), " AC∩TP", round(inter(AC, TP), 4))
for n, p in (("PZ1", PZ1), ("PZ2", PZ2)):
    print(n, "∩TP", round(inter(p, TP), 4), "∩TS", round(inter(p, TS), 4))
for ang in (0, -40, -20, 20, 40):
    r = lambda s: s.rotate(ax0, ax0 + axd, ang)
    print(f"giro {ang:+}°: cubilete∩TP {inter(B, r(TP)):.4f} ∩TS {inter(B, r(TS)):.4f} ∩AC {inter(B, r(AC)):.4f} ∩PZ {inter(B, r(PZ1))+inter(B, r(PZ2)):.4f}")
# montaje: T-P desplazado +2,6 en Y y bajando desde arriba (sin T-S)
mv = lambda s, v: s.translate(cq.Vector(*v))
peor = max(inter(B, mv(TP, (0, 2.6, dz))) for dz in [i * 1.0 for i in range(0, 45)])
print("T-P bajando con +2,6 en Y, choque con cubilete:", round(peor, 4))
peor = max(inter(B, mv(TP, (0, dy, 0))) for dy in [2.6 - 0.2 * i for i in range(14)])
print("T-P deslizando hacia el agujero ciego:", round(peor, 4))
peor = max(inter(B, mv(TS, (0, 0, dz))) + inter(TP, mv(TS, (0, 0, dz))) for dz in [0.25 * i for i in range(0, 160)])
print("T-S bajando en vertical sobre T-P:", round(peor, 4))
# juego del eje en el agujero del cubilete
d = M.B_EJE_D - M.TR_EJE_D
print("juego radial eje/agujero", d / 2, "poste/agujero ciego", (M.B_PIV_AG_D - M.TR_EJE_D) / 2)
# AC entra desde fuera del soporte, por la ventana del servo, sin servo
peor = max(inter(B, AC.translate(cq.Vector(0, dy, 0))) + inter(TS, AC.translate(cq.Vector(0, dy, 0))) for dy in [0.5 * i for i in range(0, 50)])
print("AC por la ventana del servo:", round(peor, 4))
