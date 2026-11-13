"""Proyecciones con eliminacion de lineas ocultas (OCC HLR) -> polilineas 2D en mm."""
import numpy as np
import cadquery as cq
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.BRepLib import BRepLib
from OCP.TopoDS import TopoDS


def _edges(compound, defl=0.02):
    out = []
    if compound is None or compound.IsNull():
        return out
    BRepLib.BuildCurves3d_s(compound)
    ex = TopExp_Explorer(compound, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current())
        c = BRepAdaptor_Curve(e)
        d = GCPnts_QuasiUniformDeflection(c, defl)
        if d.IsDone() and d.NbPoints() > 1:
            pts = [(d.Value(i).X(), d.Value(i).Y()) for i in range(1, d.NbPoints() + 1)]
            out.append(pts)
        ex.Next()
    return out


def proyectar(shape, ver_hacia, xdir):
    """ver_hacia: direccion hacia el observador (normal al plano de dibujo). xdir: eje x del dibujo.
    Devuelve (visibles, ocultas) en coordenadas del dibujo (x, y) con y = ver_hacia x xdir."""
    s = shape.val().wrapped if hasattr(shape, "val") else shape.wrapped
    algo = HLRBRep_Algo()
    algo.Add(s)
    ax = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*ver_hacia), gp_Dir(*xdir))
    algo.Projector(HLRAlgo_Projector(ax))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    vis = _edges(h.VCompound()) + _edges(h.OutLineVCompound()) + _edges(h.Rg1LineVCompound())
    hid = _edges(h.HCompound()) + _edges(h.OutLineHCompound())
    return vis, hid


def ejes(ver_hacia, xdir):
    n = np.array(ver_hacia, float); n /= np.linalg.norm(n)
    x = np.array(xdir, float); x = x - n * (x @ n); x /= np.linalg.norm(x)
    y = np.cross(n, x)
    return x, y


def p2(p, ver_hacia, xdir):
    x, y = ejes(ver_hacia, xdir)
    p = np.array(p, float)
    return float(p @ x), float(p @ y)
