"""Pulsador de cancelar: soporte (pegado al frontal por dentro) + embellecedor (en el agujero Ø12 del frontal).
El pulsador es un táctil 6x6 del inventario, pegado dentro del soporte.
Ejes locales (mm): x hacia dentro de la máquina, 0 = cara interior del frontal (el frontal va de x -8 a 0);
y = lateral, z = vertical, origen en el eje del pulsador (en la máquina: lat 55, z 176)."""
import cadquery as cq

# ---- parámetros ----
T_PANEL = 8.0        # grosor del frontal (DM)
AG_PANEL = 12.0      # agujero del frontal
H_PULS = 5.0         # ALTO TOTAL del táctil 6x6 (cuerpo + botón). Mide el tuyo y cambia este valor
CUERPO = 6.0         # lado del cuerpo del táctil
CUERPO_H = 3.5       # alto del cuerpo (sin el botón)
PATA_Y = 6.5         # separación entre filas de patas (las patas salen por los lados "y")
HOLG_CUERPO = 0.2    # holgura por lado en el alojamiento

EMB_D, EMB_SALE = 11.5, 3.0          # embellecedor: diámetro y cuánto sobresale por fuera del frontal
COL_D, COL_T = 16.0, 1.5             # collarín (por dentro): no deja que el embellecedor se salga
CHAF = 1.0                           # chaflán del borde exterior
JUEGO = 0.1                          # holgura entre el collarín y el botón del táctil en reposo

SOP_W = 26.0                         # soporte: cuadrado de 26 x 26
CAV_D, CAV_P = 17.0, COL_T + 0.5     # hueco del collarín (centra el soporte sobre el embellecedor)
FONDO = 2.0                          # pared de atrás del soporte

X_BOTON = COL_T + JUEGO                       # punta del botón del táctil en reposo
X_CUERPO = X_BOTON + (H_PULS - CUERPO_H)      # cara delantera del cuerpo
X_ALOJ = X_BOTON + H_PULS                     # fondo del alojamiento = cara trasera del cuerpo
SOP_L = X_ALOJ + FONDO                        # fondo total del soporte

def embellecedor():
    L = T_PANEL + EMB_SALE
    vastago = cq.Workplane("YZ").workplane(offset=-L).circle(EMB_D / 2).extrude(L).faces("<X").chamfer(CHAF)
    col = cq.Workplane("YZ").circle(COL_D / 2).extrude(COL_T)
    return vastago.union(col)

def soporte():
    s = cq.Workplane("YZ").rect(SOP_W, SOP_W).extrude(SOP_L).edges("|X").fillet(2.0)
    s = s.cut(cq.Workplane("YZ").circle(CAV_D / 2).extrude(CAV_P))
    a = CUERPO + 2 * HOLG_CUERPO
    s = s.cut(cq.Workplane("YZ").workplane(offset=CAV_P - 0.01).rect(a + 1.6, a).extrude(X_ALOJ - CAV_P + 0.01))   # +1,6 en y: patas
    for sy in (-1, 1):   # ranuras para las patas (salen por detrás, ahí se sueldan los cables)
        s = s.cut(cq.Workplane("YZ").workplane(offset=X_ALOJ - 0.01).center(sy * PATA_Y / 2, 0).rect(1.4, a).extrude(FONDO + 0.02))
    # muesca para los cables en el borde de atrás (hacia abajo)
    s = s.cut(cq.Workplane("YZ").workplane(offset=SOP_L - 1.2).center(0, -SOP_W / 4 - 2).rect(8, SOP_W / 2 + 4).extrude(1.3))
    return s

def tactil(pulsado=False):
    d = 0.25 if pulsado else 0.0
    c = cq.Workplane("YZ").workplane(offset=X_CUERPO).rect(CUERPO, CUERPO).extrude(CUERPO_H)
    b = cq.Workplane("YZ").workplane(offset=X_BOTON + d).circle(1.75).extrude(X_CUERPO - X_BOTON - d)
    p = cq.Workplane("YZ")
    for sy in (-1, 1):
        for sz in (-1, 1):
            c = c.union(cq.Workplane("YZ").workplane(offset=X_ALOJ - 0.5).center(sy * PATA_Y / 2, sz * 2.25).rect(0.6, 0.6).extrude(4.0))
    return c.union(b)

def panel():
    return cq.Workplane("YZ").workplane(offset=-T_PANEL).rect(60, 60).extrude(T_PANEL).cut(
        cq.Workplane("YZ").workplane(offset=-T_PANEL - 1).circle(AG_PANEL / 2).extrude(T_PANEL + 2))

if __name__ == "__main__":
    import os
    os.makedirs("step", exist_ok=True); os.makedirs("stl", exist_ok=True)
    E, S = embellecedor(), soporte()
    for n, w in (("PC-E_embellecedor", E), ("PC-S_soporte", S)):
        cq.exporters.export(w, f"step/{n}.step"); cq.exporters.export(w, f"stl/{n}.stl", tolerance=0.02, angularTolerance=0.1)
        print(n, "vol cm3", round(w.val().Volume() / 1000, 2), "bbox", [round(v, 2) for v in (w.val().BoundingBox().xmin, w.val().BoundingBox().xmax)])
    # comprobaciones: solapes en reposo y pulsado (el embellecedor entra 0,25 = recorrido del táctil)
    Pn = panel()
    for pul in (False, True):
        Ed = E.translate((0.25 + JUEGO, 0, 0)) if pul else E
        Tt = tactil(pul)
        for a, b, n in ((Ed, Pn, "emb-panel"), (Ed, S, "emb-soporte"), (Tt, S, "tactil-soporte"), (S, Pn, "soporte-panel")):
            v = a.intersect(b).val().Volume() if a.intersect(b).vals() else 0
            print("pulsado" if pul else "reposo ", n, round(v, 4))
        v = Ed.intersect(Tt).vals()
        print("   contacto emb-botón:", "sí" if pul else f"juego {JUEGO} mm")
    print("SOP_L", SOP_L, "X_BOTON", X_BOTON, "X_ALOJ", X_ALOJ)
