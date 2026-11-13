"""Modelo parametrico del sistema de monedas (pieza A: carril, A-T: tapa, A-S: portasensor, B: cubilete).

Sistema de referencia de la pieza A ("marco pieza"):
  X: a lo largo del carril (del frente hacia el fondo). Montado, baja 10 grados.
  Y: perpendicular a la pared lateral de montaje, hacia el interior de la maquina. Cara de montaje en Y = 0.
  Z: en el plano de la pared, perpendicular a X.
Marco del canal (seccion): u = de la pared de LEDs a la de fototransistores, v = a lo largo de la pared (altura de la moneda).
El canal esta girado BETA alrededor de X: la cuna (medio trapecio) hace que la cara de montaje quede vertical.
Todas las cotas en mm.
"""
import math
import cadquery as cq

# ---------------- parametros ----------------
ALFA = 10.0          # pendiente del carril (grados)
BETA = 12.0          # inclinacion lateral del canal (grados)
L = 150.0            # longitud del carril
GAP = 3.4            # hueco del canal en CAD (sale ~3,2 impreso)
H_INT = 32.0         # altura interior del canal
T_SUELO = 3.0        # grosor del suelo
T_FOTO = 4.0         # grosor de la pared de fototransistores
Y0 = 8.0             # grosor de la cuna (pared de LEDs) a la altura del suelo, medido en Y
T_TAPA = 3.0
SLOT_H = 25.2        # alto de la ranura en CAD (sale ~25,0; el 2 euros, 25,75, no pasa)
SLOT_V0 = 3.0        # la ranura empieza 3 mm por encima del suelo
T_PLACA = 4.0        # grosor de la placa frontal (= grosor del panel frontal)
PLACA_Y = (0.0, 28.0)      # ancho de la placa frontal (en Y)
PLACA_E = (-12.0, 46.0)    # alto de la placa frontal (vertical de la maquina, desde el punto de referencia)
D_LED = 3.2          # agujero para LED de 3 mm
D_APER = 2.0         # diafragma delante del LED
L_APER = 1.5
D_M3 = 3.5           # agujero pasante M3 en lenguetas
D_M2 = 1.8           # agujero guia para tornillo M2 autorroscante
T_LENG = 3.0         # grosor de las lenguetas
LENG_W = 14.0        # ancho de lengueta
LENG_OUT = 13.0      # cuanto sobresale la lengueta
LENG_X = (20.0, 80.0, 140.0)  # posiciones de las 6 lenguetas (3 arriba, 3 abajo)
BOLS_X = (43.0, 117.0)        # bolsillo de cableado de LEDs en la cara de montaje
BOLS_P = 3.0                  # profundidad del bolsillo
RANURA_CABLE_X = 104.0        # salida de cables del bolsillo hacia abajo
# pared de fototransistores separada (pieza A-F), atornillada al suelo y encajada en la tapa
FL_W, FL_T = 9.0, 3.0          # ala inferior de la pared A-F (ancho en u, grueso en v)
FL_TORN_X = (15.0, 80.0, 140.0)  # tornillos M2 x 6 del ala al suelo
D_M2_PASO = 2.4                # agujero pasante M2
HOLG = 0.15                    # holgura de encajes
RANURA_P = 1.0                 # profundidad de las ranuras de encaje (suelo y tapa)
HOLG_PLACA = 0.2               # separacion entre la pared A-F y la placa frontal
U_FL = GAP + T_FOTO + FL_W     # hasta donde llega el suelo del carril
TAPA_U = (-11.0, GAP + T_FOTO + 2.0)  # ancho de la tapa en u (2 de labio por fuera de la ranura)
TAPA_X = (2.0, L)
TAPA_TORN_X = (35.0, 115.0)
TAPA_TORN_U = -6.0

BARRERAS = [  # nombre, x, altura (v), tipo
    ("P1", 50.0, 10.00, "fija"),
    ("B1", 60.0, 19.25, "regulable"),
    ("B2", 70.0, 20.50, "regulable"),
    ("B3", 80.0, 21.75, "regulable"),
    ("B4", 90.0, 22.75, "regulable"),
    ("B5", 100.0, 23.75, "regulable"),
    ("P2", 110.0, 10.00, "fija"),
]
VENT_W, VENT_H = 2.5, 5.0     # ventana en la pared de fototransistores (para regulables)
TORN_DV = -8.0                # tornillo del portasensor: 8 mm por debajo de la barrera
GUIA_AS_P = 0.5               # carril guia de cada A-S en la cara exterior de A-F (profundidad)
GUIA_AS_W = 9.2               # ancho del carril guia (A-S de 9 + 0,2)
GUIA_AS_V0 = -14.0            # el carril empieza 14 mm por debajo de la barrera y sale por arriba

# portasensor A-S
AS_W, AS_T = 9.0, 3.0
AS_V = (-12.0, 5.0)           # extension en v respecto a la altura de la barrera
AS_RENDIJA = (1.0, 2.5)       # alto x ancho de la rendija
AS_RENDIJA_T = 0.6
AS_COLISO = (2.4, 5.0)        # colisa del tornillo M2 (ancho x largo)

cb, sb = math.cos(math.radians(BETA)), math.sin(math.radians(BETA))
U_HAT = (0.0, cb, -sb)   # en (X, Y, Z)
V_HAT = (0.0, sb, cb)
ORIG = (0.0, Y0, 0.0)


def P(u, v, x=0.0):
    return (x, ORIG[1] + u * U_HAT[1] + v * V_HAT[1], ORIG[2] + u * U_HAT[2] + v * V_HAT[2])


def yz(u, v):
    p = P(u, v)
    return (p[1], p[2])


def u_at_y0(v):
    """u donde la linea v=cte corta la cara de montaje Y=0"""
    return -(ORIG[1] + v * V_HAT[1]) / U_HAT[1]


def prism_uv(u0, u1, v0, v1, x0, x1):
    pts = [yz(u0, v0), yz(u1, v0), yz(u1, v1), yz(u0, v1)]
    return cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(pts).close().extrude(x1 - x0)


def cyl(d, p0, direction, length):
    return cq.Workplane(obj=cq.Solid.makeCylinder(d / 2, length, cq.Vector(*p0), cq.Vector(*direction)))


def neg(vv):
    return tuple(-c for c in vv)


def add(a, b, k=1.0):
    return tuple(a[i] + k * b[i] for i in range(3))


# ---------------- placa frontal ----------------
ca, sa = math.cos(math.radians(ALFA)), math.sin(math.radians(ALFA))
N_PLACA = (ca, 0.0, sa)       # normal de la placa (vertical de la maquina) en marco pieza
E_UP = (-sa, 0.0, ca)         # vertical de la maquina en marco pieza
E_Y = (0.0, 1.0, 0.0)
DATUM = P(0, 0)               # punto de referencia: suelo del canal junto a la pared de LEDs


def placa_solid():
    o = add(DATUM, N_PLACA, -T_PLACA)
    o = add(o, E_UP, PLACA_E[0])
    o = (o[0], PLACA_Y[0], o[2])
    plane = cq.Plane(origin=o, xDir=E_Y, normal=N_PLACA)
    return cq.Workplane(plane).rect(PLACA_Y[1] - PLACA_Y[0], PLACA_E[1] - PLACA_E[0], centered=False).extrude(T_PLACA)


def semiespacio_placa(offset=0.0):
    """Todo lo que queda por delante del plano trasero de la placa (desplazado offset hacia el fondo)."""
    big = 400
    o = add(DATUM, N_PLACA, offset)
    return cq.Workplane(cq.Plane(origin=o, xDir=E_Y, normal=neg(N_PLACA))).rect(big, big).extrude(big)


def cuerpo_A():
    """Carril A: cuña (pared de LEDs) + suelo + placa frontal + lengüetas. La pared de fototransistores es la pieza A-F."""
    vb, vt = -T_SUELO, H_INT
    z_bot = yz(u_at_y0(vb), vb)[1]
    z_top = yz(u_at_y0(vt), vt)[1]
    pts = [(0.0, z_bot), yz(U_FL, vb), yz(U_FL, 0), yz(0, 0), yz(0, vt), (0.0, z_top)]
    body = cq.Workplane("YZ", origin=(-20, 0, 0)).polyline(pts).close().extrude(L + 20)
    body = body.cut(semiespacio_placa())
    # ranura del suelo donde encaja el pie de la pared A-F
    body = body.cut(prism_uv(GAP, GAP + T_FOTO + HOLG, -RANURA_P, 0.01, -30, L + 5))
    # guias M2 del ala de A-F (atraviesan el suelo)
    for xt in FL_TORN_X:
        body = body.cut(cyl(D_M2, P(GAP + T_FOTO + FL_W / 2, 0.01, xt), neg(V_HAT), T_SUELO + 2))
    body = body.union(placa_solid())
    # ranura en la placa
    body = body.cut(prism_uv(0, GAP, SLOT_V0, SLOT_V0 + SLOT_H, -30, 5))
    for xl in LENG_X:
        for lado in (-1, 1):
            z_edge = z_top if lado > 0 else z_bot
            z0 = z_edge - 2 * lado
            z1 = z_edge + LENG_OUT * lado
            xa, xb = xl - LENG_W / 2, xl + LENG_W / 2
            ext = abs(z1 - z_edge)
            prof = [(xa - ext, z0), (xb, z0), (xb, z1), (xa, z1)]
            tab = cq.Workplane("XZ").polyline(prof).close().extrude(-T_LENG)
            hole = cyl(D_M3, (xl, -1, z_edge + (LENG_OUT - 6.5) * lado), (0, 1, 0), T_LENG + 2)
            body = body.union(tab).cut(hole)
    leds = [salida_led(h) for (_, x, h, _) in BARRERAS]
    zmin = min(z for z in leds) - 3.5
    zmax = max(z for z in leds) + 3.5
    body = body.cut(cq.Workplane("XY").box(BOLS_X[1] - BOLS_X[0], BOLS_P, zmax - zmin, centered=False).translate((BOLS_X[0], -0.01, zmin)))
    body = body.cut(cq.Workplane("XY").box(5, BOLS_P, zmin - z_bot + 4, centered=False).translate((RANURA_CABLE_X - 2.5, -0.01, z_bot - 4)))
    for (_, x, h, _) in BARRERAS:
        p0 = P(0.01, h, x)
        body = body.cut(cyl(D_APER, p0, neg(U_HAT), L_APER + 0.01))
        body = body.cut(cyl(D_LED, P(-L_APER, h, x), neg(U_HAT), 30))
    for xt in TAPA_TORN_X:
        body = body.cut(cyl(D_M2, P(TAPA_TORN_U, H_INT + 0.01, xt), neg(V_HAT), 5))  # M2 x 6: 3 en la tapa + 3 en la cuña
    return body


def pared_AF():
    """Pared de fototransistores (A-F), en el marco de la pieza A (posicion montada)."""
    w = prism_uv(GAP, GAP + T_FOTO, -RANURA_P, H_INT + RANURA_P, -20, L)
    w = w.union(prism_uv(GAP + T_FOTO - 0.5, GAP + T_FOTO + FL_W, 0, FL_T, -20, L))
    w = w.cut(semiespacio_placa(HOLG_PLACA))
    for (_, x, h, tipo) in BARRERAS:
        if tipo == "fija":
            w = w.cut(cyl(D_APER, P(GAP - 0.01, h, x), U_HAT, 0.62))
            w = w.cut(cyl(D_LED, P(GAP + 0.6, h, x), U_HAT, T_FOTO))
        else:
            w = w.cut(prism_uv(GAP - 0.1, GAP + T_FOTO + 0.1, h - VENT_H / 2, h + VENT_H / 2, x - VENT_W / 2, x + VENT_W / 2))
            # carril guia: el A-S solo desliza arriba/abajo, no gira al apretar
            w = w.cut(prism_uv(GAP + T_FOTO - GUIA_AS_P, GAP + T_FOTO + 0.1, h + GUIA_AS_V0, H_INT + RANURA_P + 0.1, x - GUIA_AS_W / 2, x + GUIA_AS_W / 2))
            # guia M2 desde el fondo del carril, deja 0,5 hasta el canal
            w = w.cut(cyl(D_M2, P(GAP + T_FOTO - GUIA_AS_P + 0.01, h + TORN_DV, x), neg(U_HAT), T_FOTO - GUIA_AS_P - 0.5))
    for xt in FL_TORN_X:
        w = w.cut(cyl(D_M2_PASO, P(GAP + T_FOTO + FL_W / 2, -1, xt), V_HAT, FL_T + 2))
    return w


def salida_led(h):
    """Z donde el eje del LED de altura h sale por la cara de montaje"""
    y_in = ORIG[1] + h * V_HAT[1]
    s = y_in / U_HAT[1]
    return ORIG[2] + h * V_HAT[2] + s * (-U_HAT[2])


def tapa_AT():
    t = prism_uv(TAPA_U[0], TAPA_U[1], H_INT, H_INT + T_TAPA, TAPA_X[0], TAPA_X[1])
    # ranura donde encaja el borde superior de la pared A-F
    t = t.cut(prism_uv(GAP - HOLG, GAP + T_FOTO + HOLG, H_INT - 1, H_INT + RANURA_P + HOLG, TAPA_X[0] - 1, TAPA_X[1] + 1))
    for xt in TAPA_TORN_X:
        t = t.cut(cyl(2.4, P(TAPA_TORN_U, H_INT - 1, xt), V_HAT, T_TAPA + 2))
    return t


def portasensor_AS():
    """Pieza suelta, en su propio marco: X = ancho, Y = grosor (cara interior en Y=0), Z = a lo largo de la pared"""
    w, t = AS_W, AS_T
    b = cq.Workplane("XY").box(w, t, AS_V[1] - AS_V[0], centered=False).translate((-w / 2, 0, AS_V[0]))
    b = b.cut(cq.Workplane("XY").box(AS_RENDIJA[1], AS_RENDIJA_T + 0.02, AS_RENDIJA[0]).translate((0, AS_RENDIJA_T / 2 - 0.01, 0)))
    b = b.cut(cyl(D_LED, (0, AS_RENDIJA_T, 0), (0, 1, 0), t))
    b = b.cut(cq.Workplane("XY").box(AS_COLISO[0], t + 1, AS_COLISO[1]).translate((0, t / 2, TORN_DV)))
    return b


# ---------------- pieza B: cubilete ----------------
B_INT = 40.0
B_T = 3.0
B_H = 40.0
B_PIV_Z = 8.0
B_PIV_X = B_T + B_INT / 2
B_PIV_AG_D, B_PIV_AG_P = 4.4, 2.5   # agujero ciego del pivote de la trampilla (el poste Ø4 lo lleva la mitad T-P)
B_EJE_D = 4.4
SERVO_GAP = 16.0          # de la cara exterior del cubilete a la placa del soporte (12 -> 16 el 2026-11-12 para que quepa el acople)
SERVO_T = 3.0
SG90_BODY = (22.8, 12.6)  # hueco para el cuerpo (largo x alto), con holgura
SG90_EJE_DESDE_EXT = 5.9  # eje del servo medido desde un extremo del cuerpo
SG90_AGUJ_SEP = 27.8
B_LENG_Z = ((0.0, 13.0), (27.0, 40.0))


def cubilete_B():
    W = B_INT + 2 * B_T
    c = cq.Workplane("XY").box(W, W, B_H, centered=False)
    c = c.cut(cq.Workplane("XY").box(B_INT, B_INT, B_H + 2, centered=False).translate((B_T, B_T, -1)))
    # agujero ciego del pivote (lado pared): deja 0,5 de piel hacia la pared de la maquina
    c = c.cut(cyl(B_PIV_AG_D, (B_PIV_X, B_T + 0.01, B_PIV_Z), (0, -1, 0), B_PIV_AG_P + 0.01))
    # agujero del eje del lado interior
    c = c.cut(cyl(B_EJE_D, (B_PIV_X, W - B_T - 1, B_PIV_Z), (0, 1, 0), B_T + 2))
    # soporte del servo
    y_pl = W + SERVO_GAP
    x_body0 = B_PIV_X - SG90_EJE_DESDE_EXT
    pl_x = (B_T, W)
    pl_z = (0.0, B_PIV_Z + SG90_BODY[1] / 2 + 8)
    plate = cq.Workplane("XY").box(pl_x[1] - pl_x[0], SERVO_T, pl_z[1] - pl_z[0], centered=False).translate((pl_x[0], y_pl, pl_z[0]))
    for xr in (pl_x[0], pl_x[1] - 3):
        plate = plate.union(cq.Workplane("XY").box(3, SERVO_GAP + 0.5, pl_z[1] - pl_z[0], centered=False).translate((xr, W - 0.25, pl_z[0])))
    plate = plate.cut(cq.Workplane("XY").box(SG90_BODY[0], SERVO_T + 2, SG90_BODY[1], centered=False)
                      .translate((x_body0 - 0.15, y_pl - 1, B_PIV_Z - SG90_BODY[1] / 2)))
    xc = x_body0 + 22.5 / 2
    for xh in (xc - SG90_AGUJ_SEP / 2, xc + SG90_AGUJ_SEP / 2):
        plate = plate.cut(cyl(D_M2, (xh, y_pl - 1, B_PIV_Z), (0, 1, 0), SERVO_T + 2))
    c = c.union(plate)
    # lenguetas en la cara de montaje (Y=0), hacia delante y hacia atras, chaflan 45 por debajo
    for (z0, z1) in B_LENG_Z:
        for lado in (-1, 1):
            xe = 0.0 if lado < 0 else W
            x1 = xe + LENG_OUT * lado
            xlo, xhi = min(xe, x1), max(xe, x1)
            tab = cq.Workplane("XY").box(xhi - xlo, T_LENG, z1 - z0, centered=False).translate((xlo, 0, z0))
            if z0 > 0:
                ch = cq.Workplane("XZ").polyline([(xe, z0), (x1, z0), (xe, z0 - LENG_OUT)]).close().extrude(-T_LENG)
                tab = tab.union(ch)
            tab = tab.cut(cyl(D_M3, (xe + (LENG_OUT - 6.5) * lado, -1, (z0 + z1) / 2), (0, 1, 0), T_LENG + 2))
            c = c.union(tab)
    return c


# ---------------- trampilla de B en dos mitades + acople con eje ----------------
# Marco del cubilete: eje de giro paralelo a Y, en X = B_PIV_X, Z = B_PIV_Z.
# T-P (lado pared): poste Ø4 que entra en el agujero ciego. Se mete la primera.
# T-S (lado servo): se baja desde arriba y apoya sobre T-P en una junta a 45° (escalón inclinado,
#   se imprime sin soportes). Lleva un alojamiento en D para el eje.
# AC (acople): eje en D que entra desde fuera por el agujero Ø4,4 + alojamiento para el brazo del SG90.
# PZ (postizo) x2: barras de 3 x 3 pegadas desde abajo en los nervios, cruzando la junta.
TR_HOLG = 0.7            # holgura trampilla-pared del cubilete (< 1,67 del 5c)
TR_SOBRE = 3.0           # cara de arriba de la trampilla por encima del eje
TR_T = 2.4               # grosor de la chapa
TR_BAJO = 3.0            # nervios hasta 3 mm por debajo del eje
TR_EJE_D = 4.0           # poste y eje Ø4
TR_POSTE_L = 3.0         # poste: 0,7 de holgura + 2,3 dentro del agujero ciego (2,5)
TR_PLANO_D = 0.8         # plano de la D (abajo, en la cara que queda arriba al imprimir)
TR_ESPINA_W = 7.0
TR_NERVIO_X = 11.0       # nervios con alojamiento para los postizos, a +-11 del eje
TR_NERVIO_W = 6.4
TR_POST = 3.0            # postizo de 3 x 3
TR_POST_HOLG = 0.2
TR_POST_Y = (14.0, 32.0) # alojamiento (cruza la junta)
TR_JUNTA_HOLG = 0.1      # holgura a cada lado de la junta (perpendicular)
TR_ALOJ_P = 8.0          # profundidad del alojamiento del eje en T-S
D_HOLG = 0.3             # holgura de la D
# acople al brazo simple del SG90, atornillado (2 x M2x6 por los agujeros del brazo, agrandados a Ø2).
# Medido en el prototipo con SERVO_GAP = 12: cara del brazo a 1 mm de la pared -> con 16 queda a 5 mm.
# Pasa por la ventana del servo con el eje: por eso el brazo va horizontal (+X).
AC_T = 5.4               # grueso total; 4,4 bajo el brazo para que el M2x6 no asome
AC_H = 9.0               # alto (Z), centrado en el eje
AC_X = (-4.5, 16.0)      # respecto al eje; cabe por la ventana del soporte del servo
AC_Y0_SEP = 0.6          # separación entre la cara exterior del cubilete y el acople
AC_EJE_DENTRO = 6.0      # cuánto entra el eje en T-S (quedan 2 mm de ajuste)
BRAZO_HUB_D = 7.6        # rebaje del buje del brazo
BRAZO_W = 6.2            # rebaje del brazo (recto; el brazo real se estrecha hacia la punta)
BRAZO_L = 30.0           # rebaje abierto por el extremo: vale cualquier largo de brazo
BRAZO_T = 1.0            # profundidad del rebaje
TORN_R = (6.5, 15.0)     # ranura guía para los M2 (agujero guía 1,7), del centro hacia la punta
TORN_W = 1.7

def _bx(a0, a1, b0, b1, c0, c1):
    return cq.Workplane("XY").box(a1 - a0, b1 - b0, c1 - c0, centered=False).translate((a0, b0, c0))


def _tr_dims():
    x0, x1 = B_T + TR_HOLG, B_T + B_INT - TR_HOLG
    y0, y1 = B_T + TR_HOLG, B_T + B_INT - TR_HOLG
    return x0, x1, y0, y1, B_PIV_Z + TR_SOBRE, B_PIV_Z - TR_BAJO


def _d_solido(d, y0, y1, plano):
    """cilindro de eje Y con la parte de abajo cortada (forma de D)"""
    c = cyl(d, (B_PIV_X, y0, B_PIV_Z), (0, 1, 0), y1 - y0)
    zf = B_PIV_Z - TR_EJE_D / 2 + plano
    return c.cut(_bx(B_PIV_X - d, B_PIV_X + d, y0 - 1, y1 + 1, B_PIV_Z - d, zf))


def trampilla_entera():
    x0, x1, y0, y1, zt, zb = _tr_dims()
    t = _bx(x0, x1, y0, y1, zt - TR_T, zt)
    t = t.union(_bx(B_PIV_X - TR_ESPINA_W / 2, B_PIV_X + TR_ESPINA_W / 2, y0, y1, zb, zt))
    for sx in (-1, 1):
        xc = B_PIV_X + sx * TR_NERVIO_X
        t = t.union(_bx(xc - TR_NERVIO_W / 2, xc + TR_NERVIO_W / 2, y0, y1, zb, zt))
    t = t.union(cyl(TR_EJE_D, (B_PIV_X, y0 + 0.01, B_PIV_Z), (0, -1, 0), TR_POSTE_L + 0.01))
    w = TR_POST + TR_POST_HOLG
    for sx in (-1, 1):
        xc = B_PIV_X + sx * TR_NERVIO_X
        t = t.cut(_bx(xc - w / 2, xc + w / 2, TR_POST_Y[0], TR_POST_Y[1], zb - 1, zb + w))
    # alojamiento en D del eje (lado servo)
    t = t.cut(_d_solido(TR_EJE_D + D_HOLG, y1 - TR_ALOJ_P, y1 + 1, TR_PLANO_D - D_HOLG / 2))
    return t


def _semiplano_junta(lado):
    """Junta a 45°: plano medio Y + Z = k (T-S arriba, T-P abajo).
    lado -1: quita lo de T-S (deja T-P); +1: quita lo de T-P (deja T-S)."""
    x0, x1, y0, y1, zt, zb = _tr_dims()
    k = (y0 + y1) / 2 + (zt + zb) / 2
    off = TR_JUNTA_HOLG * math.sqrt(2)
    z0, z1 = -5.0, 30.0
    if lado < 0:   # quitar Y + Z > k - off
        pts = [(k - off - z0, z0), (k - off - z1, z1), (200, z1), (200, z0)]
    else:          # quitar Y + Z < k + off
        pts = [(k + off - z0, z0), (k + off - z1, z1), (-200, z1), (-200, z0)]
    return cq.Workplane("YZ").polyline(pts).close().extrude(300).translate((-150, 0, 0))


def trampilla_TP():
    return trampilla_entera().cut(_semiplano_junta(-1))


def trampilla_TS():
    return trampilla_entera().cut(_semiplano_junta(1))


def postizo():
    L = TR_POST_Y[1] - TR_POST_Y[0] - 0.4
    zb = B_PIV_Z - TR_BAJO
    xc = B_PIV_X + TR_NERVIO_X
    return _bx(xc - TR_POST / 2, xc + TR_POST / 2, TR_POST_Y[0] + 0.2, TR_POST_Y[0] + 0.2 + L, zb + 0.1, zb + 0.1 + TR_POST)


def acople_servo():
    x0, x1, y0, y1, zt, zb = _tr_dims()
    ya = B_T + B_INT + B_T + AC_Y0_SEP
    a = _bx(B_PIV_X + AC_X[0], B_PIV_X + AC_X[1], ya, ya + AC_T, B_PIV_Z - AC_H / 2, B_PIV_Z + AC_H / 2)
    a = a.union(_d_solido(TR_EJE_D, y1 - AC_EJE_DENTRO, ya + 0.01, TR_PLANO_D))
    yb = ya + AC_T - BRAZO_T
    a = a.cut(cyl(BRAZO_HUB_D, (B_PIV_X, yb, B_PIV_Z), (0, 1, 0), BRAZO_T + 1))
    a = a.cut(_bx(B_PIV_X, B_PIV_X + BRAZO_L, yb, ya + AC_T + 1, B_PIV_Z - BRAZO_W / 2, B_PIV_Z + BRAZO_W / 2))
    a = a.cut(_bx(B_PIV_X + TORN_R[0], B_PIV_X + TORN_R[1], ya - 1, yb + 0.01, B_PIV_Z - TORN_W / 2, B_PIV_Z + TORN_W / 2))
    return a

# ---------------- posicion en la maquina ----------------
H0 = 352.0      # altura del punto de referencia (suelo del canal en la entrada) sobre el suelo de la maquina


def maquina_A(p):
    """marco pieza A -> (profundidad desde la cara exterior del frontal, altura, distancia a la pared)"""
    x, y, z = p
    d = T_PLACA + (x - DATUM[0]) * ca + (z - DATUM[2]) * sa
    h = H0 - (x - DATUM[0]) * sa + (z - DATUM[2]) * ca
    return d, h, y


FIN_CARRIL = maquina_A(P(0, 0, L))
B_TOP_H = FIN_CARRIL[1] - 10.0        # el cubilete queda 10 mm por debajo del final del suelo
B_D0 = FIN_CARRIL[0] - 12.0           # empieza 12 mm antes del final del carril


def maquina_B(p):
    x, y, z = p
    return B_D0 + x, B_TOP_H - B_H + z, y


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out, exist_ok=True)
    # Version pared IZQUIERDA (la de los planos): simetria respecto al plano XZ.
    # Para montar en la pared derecha, quitad .mirror("XZ").
    mir = lambda w: cq.Workplane(obj=w.val().mirror("XZ"))
    parts = {"A_carril": mir(cuerpo_A()), "A-F_pared_foto": mir(pared_AF()), "A-T_tapa": mir(tapa_AT()), "A-S_portasensor": portasensor_AS(), "B_cubilete": mir(cubilete_B()),
             "B-TP_trampilla_pared": mir(trampilla_TP()), "B-TS_trampilla_servo": mir(trampilla_TS()),
             "B-PZ_postizo": postizo(), "B-AC_acople_servo": mir(acople_servo())}
    for n, s in parts.items():
        cq.exporters.export(s, f"{out}/{n}.step")
        cq.exporters.export(s, f"{out}/{n}.stl", tolerance=0.02, angularTolerance=0.1)
        bb = s.val().BoundingBox()
        print(n, "valid", s.val().isValid(), "bbox", round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1), "vol cm3", round(s.val().Volume() / 1000, 1))
    print("fin carril (prof, alt)", [round(c, 1) for c in FIN_CARRIL])
