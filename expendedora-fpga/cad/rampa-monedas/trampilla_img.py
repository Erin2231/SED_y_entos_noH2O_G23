import numpy as np, cadquery as cq, modelo as M, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
B = M.cubilete_B().val(); TP = M.trampilla_TP().val(); TS = M.trampilla_TS().val(); AC = M.acople_servo().val()
PZ1 = M.postizo().val(); PZ2 = PZ1.mirror("YZ", cq.Vector(M.B_PIV_X, 0, 0))
COL = {"TP": "#3b7dd8", "TS": "#e8893a", "AC": "#3aa55d", "PZ": "#9a5bd0", "B": "#b5b5b5"}
NOM = {"TP": "B-TP mitad pared", "TS": "B-TS mitad servo", "AC": "B-AC acople + eje", "PZ": "B-PZ postizo", "B": "cubilete B"}
def seccion(ax, s, x, col, a=1.0):
    sl = s.intersect(cq.Solid.makeBox(0.02, 400, 400, pnt=cq.Vector(x - 0.01, -200, -200)))
    for f in sl.Faces():
        if f.normalAt().x > 0.9:
            v, t = f.tessellate(0.02)
            for tri in t:
                ax.fill([v[i].y for i in tri], [v[i].z for i in tri], color=col, alpha=a, lw=0.3, ec=col)
fig = plt.figure(figsize=(15, 10.5), dpi=150)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15])
for k, (x, tit) in enumerate(((M.B_PIV_X, "Corte por el eje"), (M.B_PIV_X + M.TR_NERVIO_X, "Corte por un nervio"))):
    ax = fig.add_subplot(gs[0, k])
    for s, c in ((B, "B"), (TP, "TP"), (TS, "TS"), (AC, "AC"), (PZ1, "PZ")):
        seccion(ax, s, x, COL[c], 0.45 if c == "B" else 0.95)
    ax.set_aspect("equal"); ax.set_xlim(-2, 68); ax.set_ylim(-1, 26)
    ax.set_title(tit, fontsize=13, fontweight="bold"); ax.set_xlabel("pared de la máquina  ←  Y (mm)  →  servo")
    ax.axhline(M.B_PIV_Z, color="k", lw=0.6, ls=(0, (6, 3)))
    if k == 0:
        ax.annotate("poste Ø4 en\nagujero ciego Ø4,4", (2, 8), (0, 18), fontsize=9, arrowprops=dict(arrowstyle="->"))
        ax.annotate("junta a 45°\n(T-S apoya encima)", (23, 8), (14, 18), fontsize=9, arrowprops=dict(arrowstyle="->"))
        ax.annotate("eje en D: entra 6 mm\nen T-S (2 mm de ajuste)", (40, 7), (36, 18), fontsize=9, arrowprops=dict(arrowstyle="->"))
        ax.annotate("acople: aquí se\natornilla el brazo", (51, 10), (50, 20), fontsize=9, arrowprops=dict(arrowstyle="->"))
    else:
        ax.annotate("postizo 3×3 cruzando la junta\n(9 mm en cada mitad)", (23, 6.5), (16, 18), fontsize=9, arrowprops=dict(arrowstyle="->"))
        ax.annotate("soporte del SG90", (63.5, 15), (50, 22), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax = fig.add_subplot(gs[1, 0], projection="3d")
L = np.array([0.3, -0.5, 0.8]); L /= np.linalg.norm(L)
def draw(s, col, off=(0, 0, 0)):
    v, t = s.tessellate(0.05, 0.2)
    v = np.array([(p.x + off[0], p.y + off[1], p.z + off[2]) for p in v]); tr = v[np.array(t)]
    n = np.cross(tr[:, 1] - tr[:, 0], tr[:, 2] - tr[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-9
    sh = 0.4 + 0.6 * np.abs(n @ L); c = np.array(matplotlib.colors.to_rgb(col))
    ax.add_collection3d(Poly3DCollection(tr, facecolors=np.clip(c * sh[:, None], 0, 1), edgecolors="none"))
ex = {"TP": (0, -10, 0), "TS": (0, 8, 18), "AC": (0, 30, 0), "PZ": (0, 0, -14)}
draw(TP, COL["TP"], ex["TP"]); draw(TS, COL["TS"], ex["TS"]); draw(AC, COL["AC"], ex["AC"])
draw(PZ1, COL["PZ"], ex["PZ"]); draw(PZ2, COL["PZ"], ex["PZ"])
ax.set_xlim(0, 46); ax.set_ylim(-14, 86); ax.set_zlim(-12, 32); ax.set_box_aspect((46, 100, 44))
ax.view_init(-25, -60); ax.set_axis_off(); ax.set_title("Despiece visto desde abajo", fontsize=13, fontweight="bold")
ax2 = fig.add_subplot(gs[1, 1]); ax2.axis("off")
pasos = [("Montaje (en el banco, antes de atornillar B a la máquina)", "k", True),
         ("1. B-TP: por arriba, empujar hacia la pared hasta que el poste entre en el agujero ciego.", COL["TP"], False),
         ("2. B-TS: bajarla en vertical por arriba; apoya encima de B-TP en la junta a 45°.", COL["TS"], False),
         ("3. B-AC: desde fuera, por la ventana del servo, meter el eje por el agujero Ø4,4\n    hasta el alojamiento en D de B-TS (con la trampilla horizontal y el brazo hacia +X).", COL["AC"], False),
         ("4. 2 × B-PZ: por debajo del cubilete, con una gota de cianocrilato, en los dos nervios.", COL["PZ"], False),
         ("5. Brazo simple del SG90: agrandar 2 agujeros a Ø2, meterlo por arriba en el\n    hueco, apoyarlo en el rebaje del acople y atornillarlo con 2 M2×6 por la ventana.\n6. Servo por la ventana (su eje entra en el brazo) y sus 2 tornillos.", "#444", False),
         ("", "k", False),
         ("Impresión (A1, PLA, 0,2 mm, sin soportes)", "k", True),
         ("• B-TP y B-TS: cara de arriba (donde caen las monedas) sobre la cama.", "#333", False),
         ("• B-AC: de pie sobre la cara del brazo, con el eje hacia arriba. 4 perímetros.", "#333", False),
         ("• B-PZ (2): tumbados. Si entran justos, lijad; si bailan, la cola lo rellena.", "#333", False),
         ("", "k", False),
         ("Cambia en el cubilete: agujero ciego Ø3,4 → Ø4,4 y soporte del servo 4 mm más separado.", "#b00", True)]
y = 0.97
for t, c, b in pasos:
    ax2.text(0, y, t, color=c, fontsize=10.5, fontweight="bold" if b else "normal", va="top", transform=ax2.transAxes)
    y -= 0.075 if "\n" not in t else 0.11
for i, k in enumerate(("TP", "TS", "AC", "PZ", "B")):
    fig.patches.append(matplotlib.patches.Rectangle((0.06 + i * 0.17, 0.945), 0.015, 0.012, color=COL[k], transform=fig.transFigure))
    fig.text(0.08 + i * 0.17, 0.946, NOM[k], fontsize=10)
fig.suptitle("Trampilla del cubilete B en dos mitades", fontsize=16, fontweight="bold", y=0.995)
plt.subplots_adjust(left=0.04, right=0.98, top=0.9, bottom=0.02, hspace=0.12, wspace=0.08)
plt.savefig("out/trampilla_montaje.png")
