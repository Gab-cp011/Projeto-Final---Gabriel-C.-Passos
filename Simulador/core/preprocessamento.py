# core/preprocessamento.py

import math
import numpy as np
from scipy.interpolate import interp1d
from tools.geometria import radiusXYZ, distanceXYZ, grading
from tools.powertrain import powercurve

def preprocessar_condicoes_iniciais(P, Ps, marcha, ns, finaldrive, gearslist, rw,
                                     x, y, z, Vo, Vmax, m, Cl, Cd, Af, Crr,
                                     use_z):
    
    # Conversão de potência para Watts
    P = P * 735.499

    if marcha:
        Ps = [i * 735.499 for i in Ps]
        pcurve = powercurve(Ps, ns, finaldrive, gearslist, rw)
        Pv = interp1d(pcurve[1], pcurve[0], fill_value='extrapolate')
    else:
        pcurve = []
        Pv = []

    # Constantes
    g = 9.81
    x, y, z = [float(i) for i in x], [float(i) for i in y], [float(i) for i in z]


    # Geometria
    R = radiusXYZ(x, y, z)
    D = distanceXYZ(x, y, z=z, use_z=True) if use_z else distanceXYZ(x, y, use_z=False)
    angle = grading(z, D) if use_z else [0] * len(R)


    # Velocidades iniciais
    V = [Vo / 3.6 + 0.0001]
    Vmax = Vmax / 3.6

    # Massa equivalente
    meq = m * 1.05

    # Coeficientes aerodinâmicos
    rhoAR = 1.25
    kl = Cl * Af * rhoAR / 2
    ka = Cd * Af * rhoAR / 2
    k = (ka - kl * Crr) / meq

    # Inclinação efetiva
    if use_z:
        slope = [(i + Crr * math.cos(i)) * m / meq for i in angle]
    else:
        slope = [0] * len(angle)

    return {
        "P": P, "Pv": Pv, "pcurve": pcurve, "g": g,
        "R": R, "D": D, "angle": angle,
        "V": V, "Vmax": Vmax, "meq": meq,
        "kl": kl, "ka": ka, "k": k,
        "slope": slope
    }
