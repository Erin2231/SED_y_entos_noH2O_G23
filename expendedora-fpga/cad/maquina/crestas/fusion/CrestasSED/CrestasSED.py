"""SED 2026-27 · Máquina expendedora · Crestas en U y canal de no válidas
Script de Fusion 360 que crea las piezas de la hoja "crestas.pdf":
  CR-1 cresta 1 (bajo el cubilete B): carril en U, rampas a 30°, 3 lengüetas M3 por debajo
  CR-2 cresta 2 (bajo el cubilete C): igual, más larga
  CR-3 caja de 3 lados del canal de no válidas (el 4º lado es la pared de la máquina), 4 lengüetas M3

Uso: Utilidades > Complementos > Scripts y complementos > "+" > añadir esta carpeta > Ejecutar.
Crea un diseño nuevo con un componente por pieza, ya colocadas en su sitio de la máquina
(x = fondo desde la cara exterior del frontal, y = desde la pared lateral, z = desde el suelo).
Para cambiar cotas: editad los PARÁMETROS y volved a ejecutar. Cotas en mm (el script convierte a cm).
"""
import math
import traceback

try:
    import adsk.core
    import adsk.fusion
except ImportError:  # permite probar la geometría fuera de Fusion
    adsk = None

# =====================================================================
# PARÁMETROS (mm y grados) — mismos valores que crestas.py y el plano del corte 1
# =====================================================================
PARED = "izquierda"   # igual que en MonedasSED: "izquierda" o "derecha" (simetría)
T = 3.0               # grosor de pared, suelo y lengüetas (= cubiletes)
D_M3 = 3.5
LENG_W, LENG_OUT, LENG_AG = 14.0, 13.0, 6.5
ANCHO = 46.0          # ancho lateral (= cubiletes)
H_U = 15.0            # altura de las paredes de la U sobre el suelo del carril
ANG = 30.0
CRESTAS = {
    "CR-1_cresta1": dict(vert=(162.721, 255.953), x0=128.0, x1=200.0),
    "CR-2_cresta2": dict(vert=(223.0, 163.0), x0=70.0, x1=280.0),
}
CAN_F = (97.0, 100.0, 118.0, 262.0)   # chapa delantera: x0, x1, z0, z1
CAN_B_Z0 = 137.0                      # la trasera va de x0 de la cresta 1 a +3, desde z 137 hasta 0,5 bajo la cresta
LENG_CAN = ((-1, (135.0, 245.0)), (1, (150.0, 215.0)))   # lengüetas del canal: lado (-1 delante, +1 detrás), alturas
VOL_ESPERADO = {"CR-1_cresta1": 20.9, "CR-2_cresta2": 57.3, "CR-3_canal": 45.0}   # cm3

tg, c30 = math.tan(math.radians(ANG)), math.cos(math.radians(ANG))


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def cyl(d, p0, direc, length):
    return ("cyl", p0, direc, d, length)


def z_sup(cr, x):
    xv, zv = cr["vert"]
    return zv - abs(x - xv) * tg


def perfil(cr, dz_top, dz_bot):
    x0, x1 = cr["x0"], cr["x1"]
    xv = cr["vert"][0]
    top = [(x, 0.0, z_sup(cr, x) + dz_top) for x in (x0, xv, x1)]
    bot = [(x, 0.0, z_sup(cr, x) + dz_bot) for x in (x1, xv, x0)]
    return top + bot


# Operaciones (mismo formato que MonedasSED):
#   ("nuevo", nombre, eje, puntos, c0, c1) · ("boceto", nombre, op, eje, puntos, c0, c1) · ("herramientas", nombre, op, [cyl...])
def pieza_cresta(nombre):
    cr = CRESTAS[nombre]
    tv, hv = T / c30, H_U / c30
    ops = [("nuevo", "Suelo del carril", "y", perfil(cr, 0.0, -tv), 0.0, ANCHO),
           ("boceto", "Pared U (lado máquina)", "unir", "y", perfil(cr, hv, -tv), 0.0, T),
           ("boceto", "Pared U (lado interior)", "unir", "y", perfil(cr, hv, -tv), ANCHO - T, ANCHO)]
    xv = cr["vert"][0]
    agujeros = []
    for k, xc in enumerate((xv, (cr["x0"] + xv) / 2, (xv + cr["x1"]) / 2)):
        xa, xb = xc - LENG_W / 2, xc + LENG_W / 2
        zb = min(z_sup(cr, xa), z_sup(cr, xb)) - tv - LENG_OUT
        pts = [(xa, 0.0, z_sup(cr, xa) - tv / 2), (xb, 0.0, z_sup(cr, xb) - tv / 2), (xb, 0.0, zb), (xa, 0.0, zb)]
        if xa < xv < xb:
            pts.insert(1, (xv, 0.0, z_sup(cr, xv) - tv / 2))
        ops.append(("boceto", ("Lengüeta del vértice", "Lengüeta rampa delantera", "Lengüeta rampa trasera")[k], "unir", "y", pts, 0.0, T))
        agujeros.append(cyl(D_M3, (xc, -1.0, zb + LENG_AG), (0, 1, 0), T + 2))
    for k, a in enumerate(agujeros):
        ops.append(("herramientas", f"Agujero M3 {k + 1}", "cortar", [a]))
    return ops


def pieza_canal():
    cr = CRESTAS["CR-1_cresta1"]
    xf0, xf1, zf0, zf1 = CAN_F
    xb0, xb1 = cr["x0"], cr["x0"] + T
    zb1 = round(min(z_sup(cr, xb0), z_sup(cr, xb1)) - T / c30 - 0.5, 1)
    rect = lambda x0, x1, z0, z1: [(x0, 0.0, z0), (x1, 0.0, z0), (x1, 0.0, z1), (x0, 0.0, z1)]
    # Orden importante: cada "unir" tiene que tocar el cuerpo que ya existe. Si la chapa trasera se crea
    # antes que la pared del fondo, no toca a la delantera y Fusion la deja como cuerpo aparte
    # (y luego los agujeros de sus orejas no cortan nada).
    ops = [("nuevo", "Chapa delantera", "y", rect(xf0, xf1, zf0, zf1), 0.0, ANCHO),
           ("boceto", "Pared del fondo", "unir", "y", [(xf0, 0.0, zf0), (xf0, 0.0, zf1), (xb0, 0.0, zb1), (xb1, 0.0, zb1), (xb1, 0.0, CAN_B_Z0)], ANCHO - T, ANCHO),
           ("boceto", "Chapa trasera", "unir", "y", rect(xb0, xb1, CAN_B_Z0, zb1), 0.0, ANCHO)]
    agujeros = []
    for lado, zs in LENG_CAN:
        xe = xf0 if lado < 0 else xb1
        xo = xe + LENG_OUT * lado
        xin = xe + T if lado < 0 else xe - T
        for zc in zs:
            nom = f"{'delantera' if lado < 0 else 'trasera'} z{zc:.0f}"
            ops.append(("boceto", "Lengüeta " + nom, "unir", "y", rect(min(xo, xin), max(xo, xin), zc - LENG_W / 2, zc + LENG_W / 2), 0.0, T))
            agujeros.append(cyl(D_M3, (xe + (LENG_OUT - LENG_AG) * lado, -1.0, zc), (0, 1, 0), T + 2))
    for k, a in enumerate(agujeros):
        ops.append(("herramientas", f"Agujero M3 {k + 1}", "cortar", [a]))
    return ops


def piezas():
    sy = -1.0 if PARED == "izquierda" else 1.0
    return [("CR-1_cresta1", pieza_cresta("CR-1_cresta1"), sy, (0, 0, 0)),
            ("CR-2_cresta2", pieza_cresta("CR-2_cresta2"), sy, (0, 0, 0)),
            ("CR-3_canal", pieza_canal(), sy, (0, 0, 0))]


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
                      "Crestas SED")
    except Exception:
        if ui:
            ui.messageBox(f"Error en el paso: {paso}\n\n{traceback.format_exc()}", "Crestas SED")
