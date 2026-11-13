"""SED 2026-27 · Máquina expendedora · Sistema de monedas
Script de Fusion 360 que crea las piezas de los planos "planos_carril_cubilete.pdf":
  A   carril de medida (cuña con los LED, suelo, placa frontal y 6 lengüetas M3)
  A-F pared de fototransistores, separada y atornillada al suelo con 3 M2 x 6
  A-T tapa desmontable del canal (con ranura donde encaja el borde de A-F)
  A-S portasensor regulable (imprimir 5)
  B   cubilete de espera sin fondo con soporte de SG90
  B-TP / B-TS  trampilla en dos mitades (junta a 45°) · B-PZ postizo (imprimir 2) · B-AC acople del servo con eje

Uso: Utilidades > Complementos > Scripts y complementos > "+" > añadir esta carpeta > Ejecutar.
Crea un diseño nuevo con un componente por pieza; cada operación queda en la línea de tiempo
con nombre (bocetos + extrusiones; los taladros inclinados como "cuerpos herramienta" + combinar).
Para cambiar cotas: editad los PARÁMETROS de abajo y volved a ejecutar (tarda unos segundos).
Todas las cotas en mm (la API de Fusion trabaja en cm: el script convierte).
"""
import math
import traceback

try:
    import adsk.core
    import adsk.fusion
except ImportError:  # permite probar la geometría fuera de Fusion
    adsk = None

# =====================================================================
# PARÁMETROS (mm y grados) — mismos valores que el PDF
# =====================================================================
PARED = "izquierda"   # "izquierda" (la de los planos) o "derecha" (simetría)

ALFA = 10.0          # pendiente del carril (sale al montar, por la posición de los agujeros)
BETA = 12.0          # inclinación lateral del canal (la da la cuña)
L = 150.0            # longitud del carril
GAP = 3.4            # hueco del canal (sale ~3,2 impreso)
H_INT = 32.0         # altura interior del canal
T_SUELO = 3.0
T_FOTO = 4.0         # pared de fototransistores
Y0 = 8.0             # grosor de la cuña a la altura del suelo
T_TAPA = 3.0
SLOT_H = 25.2        # alto de la ranura (2 € = 25,75 no pasa)
SLOT_V0 = 3.0        # la ranura empieza 3 por encima del suelo
T_PLACA = 4.0        # placa frontal = grosor del panel frontal
PLACA_Y = (0.0, 28.0)
PLACA_E = (-12.0, 46.0)
D_LED = 3.2
D_APER = 2.0
L_APER = 1.5
D_M3 = 3.5
D_M2 = 1.8
T_LENG = 3.0
LENG_W = 14.0
LENG_OUT = 13.0
LENG_X = (20.0, 80.0, 140.0)
BOLS_X = (43.0, 117.0)
BOLS_P = 3.0
RANURA_CABLE_X = 104.0
# pared de fototransistores separada (A-F)
FL_W, FL_T = 9.0, 3.0            # ala inferior de A-F (ancho, grueso)
FL_TORN_X = (15.0, 80.0, 140.0)  # tornillos M2 x 6 del ala al suelo
D_M2_PASO = 2.4
HOLG = 0.15                      # holgura de los encajes
RANURA_P = 1.0                   # profundidad de las ranuras de encaje (suelo y tapa)
HOLG_PLACA = 0.2                 # separación entre A-F y la placa frontal
U_FL = GAP + T_FOTO + FL_W
TAPA_U = (-11.0, GAP + T_FOTO + 2.0)
TAPA_X = (2.0, L)
TAPA_TORN_X = (35.0, 115.0)
TAPA_TORN_U = -6.0
BARRERAS = [  # nombre, x desde R, altura sobre el suelo del canal, tipo
    ("P1", 50.0, 10.00, "fija"),
    ("B1", 60.0, 19.25, "regulable"),
    ("B2", 70.0, 20.50, "regulable"),
    ("B3", 80.0, 21.75, "regulable"),
    ("B4", 90.0, 22.75, "regulable"),
    ("B5", 100.0, 23.75, "regulable"),
    ("P2", 110.0, 10.00, "fija"),
]
VENT_W, VENT_H = 2.5, 5.0
TORN_DV = -8.0
GUIA_AS_P = 0.5      # carril guía de cada A-S en la cara exterior de A-F
GUIA_AS_W = 9.2
GUIA_AS_V0 = -14.0
# portasensor A-S
AS_W, AS_T = 9.0, 3.0
AS_V = (-12.0, 5.0)
AS_RENDIJA = (1.0, 2.5)
AS_RENDIJA_T = 0.6
AS_COLISO = (2.4, 5.0)
# cubilete B
B_INT = 40.0
B_T = 3.0
B_H = 40.0
B_PIV_Z = 8.0
B_PIV_AG_D, B_PIV_AG_P = 4.4, 2.5   # agujero ciego del pivote (el poste Ø4 lo lleva la mitad B-TP)
B_EJE_D = 4.4
SERVO_GAP = 16.0   # 12 -> 16 (2026-11-12) para que quepa el acople
SERVO_T = 3.0
SG90_BODY = (22.8, 12.6)
SG90_EJE_DESDE_EXT = 5.9
SG90_AGUJ_SEP = 27.8
B_LENG_Z = ((0.0, 13.0), (27.0, 40.0))

# trampilla en dos mitades (mismas cotas que modelo.py)
TR_HOLG = 0.7            # holgura con las paredes del cubilete (< 1,67 del 5c)
TR_SOBRE = 3.0           # cara de arriba por encima del eje
TR_T = 2.4               # grosor de la chapa
TR_BAJO = 3.0            # nervios hasta 3 mm por debajo del eje
TR_EJE_D = 4.0
TR_POSTE_L = 3.0
TR_PLANO_D = 0.8
TR_ESPINA_W = 7.0
TR_NERVIO_X = 11.0
TR_NERVIO_W = 6.4
TR_POST = 3.0
TR_POST_HOLG = 0.2
TR_POST_Y = (14.0, 32.0)
TR_JUNTA_HOLG = 0.1
TR_ALOJ_P = 8.0
D_HOLG = 0.3
# acople del brazo simple del SG90, atornillado con 2 x M2x6
AC_T = 5.4
AC_H = 9.0
AC_X = (-4.5, 16.0)
AC_Y0_SEP = 0.6
AC_EJE_DENTRO = 6.0
BRAZO_HUB_D = 7.6
BRAZO_W = 6.2
BRAZO_L = 30.0
BRAZO_T = 1.0
TORN_R = (6.5, 15.0)
TORN_W = 1.7

# volúmenes del modelo de referencia (cm³) para comprobar al final
VOL_ESPERADO = {"A_carril": 72.3, "A-F_pared_foto": 23.8, "A-T_tapa": 8.3, "A-S_portasensor": 0.4, "B_cubilete": 27.1, "B-TP_trampilla_pared": 2.9,
                "B-TS_trampilla_servo": 3.0, "B-PZ_postizo": 0.2, "B-AC_acople_servo": 0.9}

# =====================================================================
# GEOMETRÍA (Python puro). Marco de pieza:
#   X a lo largo del carril, Y hacia el interior de la máquina (cara de montaje en Y=0), Z en la pared.
# Para la pared izquierda se hace simetría Y -> -Y.
# =====================================================================
cb, sb = math.cos(math.radians(BETA)), math.sin(math.radians(BETA))
ca, sa = math.cos(math.radians(ALFA)), math.sin(math.radians(ALFA))
U_HAT = (0.0, cb, -sb)
V_HAT = (0.0, sb, cb)
N_PLACA = (ca, 0.0, sa)
E_UP = (-sa, 0.0, ca)
E_Y = (0.0, 1.0, 0.0)


def add(a, b, k=1.0):
    return tuple(a[i] + k * b[i] for i in range(3))


def neg(v):
    return tuple(-c for c in v)


def P(u, v, x=0.0):
    return (x, Y0 + u * U_HAT[1] + v * V_HAT[1], u * U_HAT[2] + v * V_HAT[2])


def u_at_y0(v):
    return -(Y0 + v * V_HAT[1]) / U_HAT[1]


def salida_led(h):
    y_in = Y0 + h * V_HAT[1]
    s = y_in / U_HAT[1]
    return h * V_HAT[2] + s * (-U_HAT[2])


DATUM = P(0, 0)


def uv_poly(u0, u1, v0, v1, x):
    return [P(u0, v0, x), P(u1, v0, x), P(u1, v1, x), P(u0, v1, x)]


def box_uv(u0, u1, v0, v1, x0, x1):
    c = P((u0 + u1) / 2, (v0 + v1) / 2, (x0 + x1) / 2)
    return ("box", c, U_HAT, V_HAT, u1 - u0, v1 - v0, x1 - x0)


def box_xyz(x0, x1, y0, y1, z0, z1):
    return ("box", ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (1, 0, 0), (0, 1, 0), x1 - x0, y1 - y0, z1 - z0)


def cyl(d, p0, direc, length):
    return ("cyl", p0, direc, d, length)


# Operaciones:
#   ("nuevo", nombre, eje, puntos, c0, c1)              boceto en el plano normal a eje, extruido de c0 a c1 (cuerpo nuevo)
#   ("boceto", nombre, op, eje, puntos, c0, c1)          igual, op = "unir" / "cortar"
#   ("herramientas", nombre, op, [box/cyl...])          cuerpos herramienta + combinar
def semiespacio_placa(offset=0.0):
    big = 400.0
    return ("box", add(DATUM, N_PLACA, offset - big / 2), N_PLACA, E_Y, big, big, big)


def ops_fototransistores():
    t = []
    for (_, x, h, tipo) in BARRERAS:
        if tipo == "fija":
            t.append(cyl(D_APER, P(GAP - 0.01, h, x), U_HAT, 0.62))
            t.append(cyl(D_LED, P(GAP + 0.6, h, x), U_HAT, T_FOTO))
        else:
            t.append(box_uv(GAP - 0.1, GAP + T_FOTO + 0.1, h - VENT_H / 2, h + VENT_H / 2, x - VENT_W / 2, x + VENT_W / 2))
            t.append(box_uv(GAP + T_FOTO - GUIA_AS_P, GAP + T_FOTO + 0.1, h + GUIA_AS_V0, H_INT + RANURA_P + 0.1,
                            x - GUIA_AS_W / 2, x + GUIA_AS_W / 2))
            t.append(cyl(D_M2, P(GAP + T_FOTO - GUIA_AS_P + 0.01, h + TORN_DV, x), neg(U_HAT), T_FOTO - GUIA_AS_P - 0.5))
    return ("herramientas", "Fototransistores: fijos, ventanas, carriles y guías M2 de los A-S", "cortar", t)


def pieza_A():
    ops = []
    vb, vt = -T_SUELO, H_INT
    z_bot = P(u_at_y0(vb), vb)[2]
    z_top = P(u_at_y0(vt), vt)[2]
    perfil = [(-20.0, 0.0, z_bot), P(U_FL, vb, -20.0), P(U_FL, 0, -20.0), P(0, 0, -20.0), P(0, vt, -20.0), (-20.0, 0.0, z_top)]
    ops.append(("nuevo", "Cuerpo: cuña de los LED + suelo", "x", perfil, -20.0, L))
    ops.append(("herramientas", "Recorte por delante de la placa", "cortar", [semiespacio_placa()]))
    ops.append(("boceto", "Ranura del suelo para el pie de A-F", "cortar", "x",
                uv_poly(GAP, GAP + T_FOTO + HOLG, -RANURA_P, 0.01, -30.0), -30.0, L + 5))
    ops.append(("herramientas", "Guías M2 del ala de A-F", "cortar",
                [cyl(D_M2, P(GAP + T_FOTO + FL_W / 2, 0.01, xt), neg(V_HAT), T_SUELO + 2) for xt in FL_TORN_X]))
    o = add(add(DATUM, N_PLACA, -T_PLACA), E_UP, PLACA_E[0])
    o = (o[0], PLACA_Y[0], o[2])
    c = add(add(add(o, E_Y, (PLACA_Y[1] - PLACA_Y[0]) / 2), E_UP, (PLACA_E[1] - PLACA_E[0]) / 2), N_PLACA, T_PLACA / 2)
    ops.append(("herramientas", "Placa frontal", "unir",
                [("box", c, N_PLACA, E_Y, T_PLACA, PLACA_Y[1] - PLACA_Y[0], PLACA_E[1] - PLACA_E[0])]))
    ops.append(("boceto", "Ranura de la placa", "cortar", "x", uv_poly(0, GAP, SLOT_V0, SLOT_V0 + SLOT_H, -30.0), -30.0, 5.0))
    agujeros = []
    for xl in LENG_X:
        for lado in (-1, 1):
            z_edge = z_top if lado > 0 else z_bot
            z0 = z_edge - 2 * lado
            z1 = z_edge + LENG_OUT * lado
            xa, xb = xl - LENG_W / 2, xl + LENG_W / 2
            ext = abs(z1 - z_edge)
            prof = [(xa - ext, 0.0, z0), (xb, 0.0, z0), (xb, 0.0, z1), (xa, 0.0, z1)]
            ops.append(("boceto", f"Lengüeta x={xl:g} {'sup' if lado > 0 else 'inf'}", "unir", "y", prof, 0.0, T_LENG))
            agujeros.append(cyl(D_M3, (xl, -1.0, z_edge + (LENG_OUT - 6.5) * lado), (0, 1, 0), T_LENG + 2))
    ops.append(("herramientas", "Agujeros M3 lengüetas", "cortar", agujeros))
    leds = [salida_led(h) for (_, _, h, _) in BARRERAS]
    zmin, zmax = min(leds) - 3.5, max(leds) + 3.5
    ops.append(("herramientas", "Bolsillo de cables LED + salida", "cortar", [
        box_xyz(BOLS_X[0], BOLS_X[1], -0.01, BOLS_P - 0.01, zmin, zmax),
        box_xyz(RANURA_CABLE_X - 2.5, RANURA_CABLE_X + 2.5, -0.01, BOLS_P - 0.01, z_bot - 4, zmin + 0.01)]))
    t = []
    for (_, x, h, _) in BARRERAS:
        t.append(cyl(D_APER, P(0.01, h, x), neg(U_HAT), L_APER + 0.01))
        t.append(cyl(D_LED, P(-L_APER, h, x), neg(U_HAT), 30))
    ops.append(("herramientas", "Agujeros LED + diafragmas", "cortar", t))
    ops.append(("herramientas", "Guías M2 de la tapa", "cortar",
                [cyl(D_M2, P(TAPA_TORN_U, H_INT + 0.01, xt), neg(V_HAT), 5) for xt in TAPA_TORN_X]))  # M2 x 6
    return ops


def pieza_AF():
    ops = [("nuevo", "Pared (con pie y borde de encaje)", "x", uv_poly(GAP, GAP + T_FOTO, -RANURA_P, H_INT + RANURA_P, -20.0), -20.0, L)]
    ops.append(("boceto", "Ala inferior", "unir", "x", uv_poly(GAP + T_FOTO - 0.5, U_FL, 0, FL_T, -20.0), -20.0, L))
    ops.append(("herramientas", "Recorte junto a la placa frontal", "cortar", [semiespacio_placa(HOLG_PLACA)]))
    ops.append(ops_fototransistores())
    ops.append(("herramientas", "Agujeros M2 pasantes del ala", "cortar",
                [cyl(D_M2_PASO, P(GAP + T_FOTO + FL_W / 2, -1, xt), V_HAT, FL_T + 2) for xt in FL_TORN_X]))
    return ops


def pieza_AT():
    ops = [("nuevo", "Tapa", "x", uv_poly(TAPA_U[0], TAPA_U[1], H_INT, H_INT + T_TAPA, TAPA_X[0]), TAPA_X[0], TAPA_X[1])]
    ops.append(("boceto", "Ranura para el borde de A-F", "cortar", "x",
                uv_poly(GAP - HOLG, GAP + T_FOTO + HOLG, H_INT - 1, H_INT + RANURA_P + HOLG, TAPA_X[0] - 1), TAPA_X[0] - 1, TAPA_X[1] + 1))
    ops.append(("herramientas", "Agujeros M2 pasantes", "cortar",
                [cyl(2.4, P(TAPA_TORN_U, H_INT - 1, xt), V_HAT, T_TAPA + 2) for xt in TAPA_TORN_X]))
    return ops


def pieza_AS():
    w, t = AS_W, AS_T
    prof = [(-w / 2, 0.0, AS_V[0]), (w / 2, 0.0, AS_V[0]), (w / 2, 0.0, AS_V[1]), (-w / 2, 0.0, AS_V[1])]
    ops = [("nuevo", "Portasensor", "y", prof, 0.0, t)]
    ops.append(("herramientas", "Rendija, fototransistor y colisa", "cortar", [
        ("box", (0.0, AS_RENDIJA_T / 2 - 0.01, 0.0), (1, 0, 0), (0, 1, 0), AS_RENDIJA[1], AS_RENDIJA_T + 0.02, AS_RENDIJA[0]),
        cyl(D_LED, (0.0, AS_RENDIJA_T, 0.0), (0, 1, 0), t),
        ("box", (0.0, t / 2, TORN_DV), (1, 0, 0), (0, 1, 0), AS_COLISO[0], t + 1, AS_COLISO[1])]))
    return ops


def pieza_B():
    W = B_INT + 2 * B_T
    piv_x = B_T + B_INT / 2
    sq = lambda a, b: [(a, a, 0.0), (b, a, 0.0), (b, b, 0.0), (a, b, 0.0)]
    ops = [("nuevo", "Caja", "z", sq(0.0, W), 0.0, B_H)]
    ops.append(("boceto", "Hueco interior (sin fondo)", "cortar", "z", sq(B_T, B_T + B_INT), -1.0, B_H + 1))
    ops.append(("herramientas", "Agujero del pivote de la trampilla (lado pared)", "cortar",
                [cyl(B_PIV_AG_D, (piv_x, B_T + 0.01, B_PIV_Z), (0, -1, 0), B_PIV_AG_P + 0.01)]))
    ops.append(("herramientas", "Agujero del eje (lado interior)", "cortar",
                [cyl(B_EJE_D, (piv_x, W - B_T - 1, B_PIV_Z), (0, 1, 0), B_T + 2)]))
    y_pl = W + SERVO_GAP
    x_body0 = piv_x - SG90_EJE_DESDE_EXT
    pz1 = B_PIV_Z + SG90_BODY[1] / 2 + 8
    ops.append(("herramientas", "Soporte SG90", "unir", [
        box_xyz(B_T, W, y_pl, y_pl + SERVO_T, 0.0, pz1),
        box_xyz(B_T, B_T + 3, W - 0.25, W + SERVO_GAP + 0.25, 0.0, pz1),
        box_xyz(W - 3, W, W - 0.25, W + SERVO_GAP + 0.25, 0.0, pz1)]))
    xc = x_body0 + 22.5 / 2
    ops.append(("herramientas", "Hueco y tornillos SG90", "cortar", [
        box_xyz(x_body0 - 0.15, x_body0 - 0.15 + SG90_BODY[0], y_pl - 1, y_pl + SERVO_T + 1,
                B_PIV_Z - SG90_BODY[1] / 2, B_PIV_Z + SG90_BODY[1] / 2)] +
        [cyl(D_M2, (xh, y_pl - 1, B_PIV_Z), (0, 1, 0), SERVO_T + 2) for xh in (xc - SG90_AGUJ_SEP / 2, xc + SG90_AGUJ_SEP / 2)]))
    tabs, holes = [], []
    for (z0, z1) in B_LENG_Z:
        for lado in (-1, 1):
            xe = 0.0 if lado < 0 else W
            x1 = xe + LENG_OUT * lado
            tabs.append(box_xyz(min(xe, x1), max(xe, x1), 0.0, T_LENG, z0, z1))
            if z0 > 0:
                ops.append(("boceto", f"Chaflán 45° lengüeta {'delantera' if lado < 0 else 'trasera'}", "unir", "y",
                            [(xe, 0.0, z0), (x1, 0.0, z0), (xe, 0.0, z0 - LENG_OUT)], 0.0, T_LENG))
            holes.append(cyl(D_M3, (xe + (LENG_OUT - 6.5) * lado, -1.0, (z0 + z1) / 2), (0, 1, 0), T_LENG + 2))
    ops.append(("herramientas", "Lengüetas", "unir", tabs))
    ops.append(("herramientas", "Agujeros M3 lengüetas", "cortar", holes))
    return ops


def _tr_dims():
    return (B_T + TR_HOLG, B_T + B_INT - TR_HOLG, B_T + TR_HOLG, B_T + B_INT - TR_HOLG,
            B_PIV_Z + TR_SOBRE, B_PIV_Z - TR_BAJO)


def ops_trampilla(mitad):
    """mitad "P" (pared, con poste) o "S" (servo, apoya encima en la junta a 45°)."""
    x0, x1, y0, y1, zt, zb = _tr_dims()
    px = B_T + B_INT / 2
    sq = [(x0, y0, 0.0), (x1, y0, 0.0), (x1, y1, 0.0), (x0, y1, 0.0)]
    ops = [("nuevo", "Chapa", "z", sq, zt - TR_T, zt)]
    tools = [box_xyz(px - TR_ESPINA_W / 2, px + TR_ESPINA_W / 2, y0, y1, zb, zt)]
    for sx in (-1, 1):
        xc = px + sx * TR_NERVIO_X
        tools.append(box_xyz(xc - TR_NERVIO_W / 2, xc + TR_NERVIO_W / 2, y0, y1, zb, zt))
    if mitad == "P":
        tools.append(cyl(TR_EJE_D, (px, y0 + 0.01, B_PIV_Z), (0, -1, 0), TR_POSTE_L + 0.01))
    ops.append(("herramientas", "Espina y nervios" + (" + poste Ø4" if mitad == "P" else ""), "unir", tools))
    w = TR_POST + TR_POST_HOLG
    ops.append(("herramientas", "Alojamientos de los postizos", "cortar",
                [box_xyz(px + sx * TR_NERVIO_X - w / 2, px + sx * TR_NERVIO_X + w / 2, TR_POST_Y[0], TR_POST_Y[1], zb - 1, zb + w)
                 for sx in (-1, 1)]))
    if mitad == "S":
        d = TR_EJE_D + D_HOLG
        ops.append(("herramientas", "Alojamiento del eje", "cortar", [cyl(d, (px, y1 - TR_ALOJ_P, B_PIV_Z), (0, 1, 0), TR_ALOJ_P + 1)]))
        zf = B_PIV_Z - TR_EJE_D / 2 + TR_PLANO_D - D_HOLG / 2
        ops.append(("herramientas", "Plano de la D", "unir", [box_xyz(px - 2.5, px + 2.5, y1 - TR_ALOJ_P, y1, zb + 0.5, zf)]))
    k = (y0 + y1) / 2 + (zt + zb) / 2
    off = TR_JUNTA_HOLG * math.sqrt(2)
    z0, z1 = zb - 1, zt + 1
    if mitad == "P":
        pts = [(0.0, k - off - z0, z0), (0.0, k - off - z1, z1), (0.0, y1 + 10, z1), (0.0, y1 + 10, z0)]
    else:
        pts = [(0.0, k + off - z0, z0), (0.0, k + off - z1, z1), (0.0, y0 - 10, z1), (0.0, y0 - 10, z0)]
    ops.append(("boceto", "Junta a 45°", "cortar", "x", pts, x0 - 1, x1 + 1))
    return ops


def ops_postizo():
    zb = B_PIV_Z - TR_BAJO
    xc = B_T + B_INT / 2 + TR_NERVIO_X
    L = TR_POST_Y[1] - TR_POST_Y[0] - 0.4
    ya, za = TR_POST_Y[0] + 0.2, zb + 0.1
    sq = [(xc - TR_POST / 2, ya, 0.0), (xc + TR_POST / 2, ya, 0.0), (xc + TR_POST / 2, ya + L, 0.0), (xc - TR_POST / 2, ya + L, 0.0)]
    return [("nuevo", "Postizo 3 x 3", "z", sq, za, za + TR_POST)]


def ops_acople():
    x0, x1, y0, y1, zt, zb = _tr_dims()
    px = B_T + B_INT / 2
    ya = B_T + B_INT + B_T + AC_Y0_SEP
    pts = [(px + AC_X[0], 0.0, B_PIV_Z - AC_H / 2), (px + AC_X[1], 0.0, B_PIV_Z - AC_H / 2),
           (px + AC_X[1], 0.0, B_PIV_Z + AC_H / 2), (px + AC_X[0], 0.0, B_PIV_Z + AC_H / 2)]
    ops = [("nuevo", "Placa del acople", "y", pts, ya, ya + AC_T)]
    ye0 = y1 - AC_EJE_DENTRO
    ops.append(("herramientas", "Eje Ø4", "unir", [cyl(TR_EJE_D, (px, ye0, B_PIV_Z), (0, 1, 0), ya - ye0 + 0.01)]))
    zf = B_PIV_Z - TR_EJE_D / 2 + TR_PLANO_D
    ops.append(("herramientas", "Plano de la D del eje", "cortar", [box_xyz(px - 3, px + 3, ye0 - 1, ya, B_PIV_Z - 3, zf)]))
    yb = ya + AC_T - BRAZO_T
    ops.append(("herramientas", "Alojamiento del brazo del SG90", "cortar", [
        cyl(BRAZO_HUB_D, (px, yb, B_PIV_Z), (0, 1, 0), BRAZO_T + 1),
        box_xyz(px, px + BRAZO_L, yb, ya + AC_T + 1, B_PIV_Z - BRAZO_W / 2, B_PIV_Z + BRAZO_W / 2)]))
    ops.append(("herramientas", "Ranura guía de los M2", "cortar", [
        box_xyz(px + TORN_R[0], px + TORN_R[1], ya - 1, yb + 0.01, B_PIV_Z - TORN_W / 2, B_PIV_Z + TORN_W / 2)]))
    return ops


def piezas():
    sy = -1.0 if PARED == "izquierda" else 1.0
    return [  # nombre, operaciones, simetría en Y, desplazamiento para verlas separadas (mm)
        ("A_carril", pieza_A(), sy, (0, 0, 0)),
        ("A-F_pared_foto", pieza_AF(), sy, (0, 0, 0)),  # en su sitio, sobre el carril
        ("A-T_tapa", pieza_AT(), sy, (0, 0, 0)),
        ("A-S_portasensor", pieza_AS(), 1.0, (0, 60 * -sy, 0)),
        ("B_cubilete", pieza_B(), sy, (200, 0, 0)),
        # la trampilla y el acople salen ya montados dentro del cubilete
        ("B-TP_trampilla_pared", ops_trampilla("P"), sy, (200, 0, 0)),
        ("B-TS_trampilla_servo", ops_trampilla("S"), sy, (200, 0, 0)),
        ("B-PZ_postizo", ops_postizo(), sy, (200, 0, 0)),
        ("B-AC_acople_servo", ops_acople(), sy, (200, 0, 0)),
    ]


def espejo(p, sy):
    return (p[0], sy * p[1], p[2])


# =====================================================================
# FUSION 360
# =====================================================================
def _pt(p):
    return adsk.core.Point3D.create(p[0] / 10.0, p[1] / 10.0, p[2] / 10.0)


def _vec(v):
    return adsk.core.Vector3D.create(v[0], v[1], v[2])


EJES = "xyz"


class Constructor:
    def __init__(self, comp, sy):
        self.comp, self.sy = comp, sy
        self.cuerpo = None

    def plano(self, eje, c):
        base = {"x": self.comp.yZConstructionPlane, "y": self.comp.xZConstructionPlane, "z": self.comp.xYConstructionPlane}[eje]
        if abs(c) < 1e-9:
            return base
        n = base.geometry.normal
        sgn = [n.x, n.y, n.z][EJES.index(eje)]
        inp = self.comp.constructionPlanes.createInput()
        inp.setByOffset(base, adsk.core.ValueInput.createByReal(c * sgn / 10.0))
        pl = self.comp.constructionPlanes.add(inp)
        pl.isLightBulbOn = False
        return pl

    def boceto(self, nombre, op, eje, pts, c0, c1):
        i = EJES.index(eje)
        # simetría: si el eje es Y, los extremos también cambian de signo
        if eje == "y":
            c0, c1 = c0 * self.sy, c1 * self.sy
        pts = [espejo(p, self.sy) for p in pts]
        pl = self.plano(eje, c0)
        sk = self.comp.sketches.add(pl)
        sk.name = nombre
        sp = []
        for p in pts:
            q = list(p)
            q[i] = c0
            sp.append(sk.modelToSketchSpace(_pt(q)))
        lines = sk.sketchCurves.sketchLines
        first = prev = lines.addByTwoPoints(sp[0], sp[1])
        for q in sp[2:]:
            prev = lines.addByTwoPoints(prev.endSketchPoint, q)
        lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
        prof = sk.profiles.item(0)
        nx = sk.xDirection.crossProduct(sk.yDirection)
        s_sk = [nx.x, nx.y, nx.z][i]
        hacia = 1.0 if c1 > c0 else -1.0
        direc = (adsk.fusion.ExtentDirections.PositiveExtentDirection if hacia * s_sk > 0
                 else adsk.fusion.ExtentDirections.NegativeExtentDirection)
        ops = {"nuevo": adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
               "unir": adsk.fusion.FeatureOperations.JoinFeatureOperation,
               "cortar": adsk.fusion.FeatureOperations.CutFeatureOperation}
        ext = self.comp.features.extrudeFeatures
        inp = ext.createInput(prof, ops[op])
        dist = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(abs(c1 - c0) / 10.0))
        inp.setOneSideExtent(dist, direc)
        if op != "nuevo":
            inp.participantBodies = [self.cuerpo]
        f = ext.add(inp)
        f.name = nombre
        if op == "nuevo":
            self.cuerpo = f.bodies.item(0)
            self.cuerpo.name = self.comp.name

    def herramientas(self, nombre, op, tools):
        tbm = adsk.fusion.TemporaryBRepManager.get()
        temps = []
        for t in tools:
            if t[0] == "box":
                _, c, ld, wd, l, w, h = t
                obb = adsk.core.OrientedBoundingBox3D.create(_pt(espejo(c, self.sy)), _vec(espejo(ld, self.sy)),
                                                              _vec(espejo(wd, self.sy)), l / 10.0, w / 10.0, h / 10.0)
                temps.append(tbm.createBox(obb))
            else:
                _, p0, d, dia, length = t
                p1 = add(p0, d, length)
                temps.append(tbm.createCylinderOrCone(_pt(espejo(p0, self.sy)), dia / 20.0,
                                                      _pt(espejo(p1, self.sy)), dia / 20.0))
        bf = self.comp.features.baseFeatures.add()
        bf.name = nombre + " (herramientas)"
        bf.startEdit()
        for tb in temps:
            self.comp.bRepBodies.add(tb, bf)
        bf.finishEdit()
        coll = adsk.core.ObjectCollection.create()
        for k in range(bf.bodies.count):
            coll.add(bf.bodies.item(k))
        cf = self.comp.features.combineFeatures
        ci = cf.createInput(self.cuerpo, coll)
        ci.operation = (adsk.fusion.FeatureOperations.CutFeatureOperation if op == "cortar"
                        else adsk.fusion.FeatureOperations.JoinFeatureOperation)
        ci.isKeepToolBodies = False
        f = cf.add(ci)
        f.name = nombre

    def ejecutar(self, op):
        self._ejecutar(op)
        # volver a localizar el cuerpo por su nombre (la referencia puede cambiar tras cada operación)
        if self.cuerpo is None or not self.cuerpo.isValid:
            self.cuerpo = self.comp.bRepBodies.itemByName(self.comp.name)
        else:
            self.cuerpo.name = self.comp.name

    def _ejecutar(self, op):
        if op[0] == "nuevo":
            _, nombre, eje, pts, c0, c1 = op
            self.boceto(nombre, "nuevo", eje, pts, c0, c1)
        elif op[0] == "boceto":
            _, nombre, o, eje, pts, c0, c1 = op
            self.boceto(nombre, o, eje, pts, c0, c1)
        else:
            _, nombre, o, tools = op
            self.herramientas(nombre, o, tools)


def run(context):
    ui = None
    paso = "inicio"
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        design.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
        root = design.rootComponent
        informe = []
        occs = []
        for nombre, ops, sy, desp in piezas():
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            occ.component.name = nombre
            c = Constructor(occ.component, sy)
            for op in ops:
                paso = f"{nombre} > {op[1]}"
                c.ejecutar(op)
            c.cuerpo.name = nombre
            vol = c.cuerpo.volume  # cm3
            esp = VOL_ESPERADO.get(nombre)
            ok = esp is None or abs(vol - esp) < 0.05 * esp + 0.1
            informe.append(f"{'OK ' if ok else '¡¡ '} {nombre}: {vol:.1f} cm³ (esperado {esp})")
            occs.append((occ, desp))
        paso = "colocar piezas"
        try:
            for occ, d in occs:
                if any(d):
                    m = adsk.core.Matrix3D.create()
                    m.translation = adsk.core.Vector3D.create(d[0] / 10.0, d[1] / 10.0, d[2] / 10.0)
                    occ.transform2 = m
            if design.snapshots.hasPendingSnapshot:
                design.snapshots.add()
        except Exception:
            informe.append("(no se pudieron separar las piezas: movedlas a mano)")
        app.activeViewport.fit()
        ui.messageBox("Piezas creadas (pared " + PARED + ").\n\n" + "\n".join(informe) +
                      "\n\nSi algún volumen sale con ¡¡, avisad: algo no ha salido como en el modelo.",
                      "Monedas SED")
    except Exception:
        if ui:
            ui.messageBox(f"Error en el paso: {paso}\n\n{traceback.format_exc()}", "Monedas SED")
