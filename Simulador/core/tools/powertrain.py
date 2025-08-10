import math
import numpy as np
from scipy.interpolate import interp1d
from shapely.geometry import LineString

#Criacao das curvas de potncia em funcao da marcha e da velocidade:
def powercurve(Ps, ns, relacaoFinal, relacoesMarcha, rw):

    Ps = np.asarray(Ps)
    ns = np.asarray(ns)
    relacoesMarcha = np.asarray(relacoesMarcha)

    # Cria função potência em função do RPM
    P = interp1d(ns, Ps, fill_value='extrapolate')

    # Inicializa listas de saída
    Vs = []
    Plist = []
    Vlist = []

    # Velocidade mínima da 1ª marcha
    Vs.append((ns[0] * math.pi * rw) / (30 * relacoesMarcha[0] * relacaoFinal))

    # Para cada troca de marcha
    for i in range(len(relacoesMarcha) - 1):
        # Velocidades inicial e final das marchas i e i+1
        Vs1 = (ns[0] * math.pi * rw) / (30 * relacoesMarcha[i] * relacaoFinal)
        Vf1 = (ns[-1] * math.pi * rw) / (30 * relacoesMarcha[i] * relacaoFinal)
        Vs2 = (ns[0] * math.pi * rw) / (30 * relacoesMarcha[i + 1] * relacaoFinal)
        Vf2 = (ns[-1] * math.pi * rw) / (30 * relacoesMarcha[i + 1] * relacaoFinal)

        # Curva Potência vs Velocidade em cada marcha
        v1 = np.linspace(Vs1, Vf1, 1000)
        p1 = P((v1 * 30 * relacaoFinal * relacoesMarcha[i]) / (math.pi * rw))

        v2 = np.linspace(Vs2, Vf2, 1000)
        p2 = P((v2 * 30 * relacaoFinal * relacoesMarcha[i + 1]) / (math.pi * rw))

        # Interseção das curvas para troca de marcha
        line1 = LineString(np.column_stack((v1, p1)))
        line2 = LineString(np.column_stack((v2, p2)))
        intersec = line1.intersection(line2)

        if intersec.is_empty:
            Vtroca = (Vf1 + Vs2) / 2  # Chute conservador
        else:
            Vtroca = intersec.x  # Velocidade onde a troca acontece

        Vs.append(Vtroca)

    # Última velocidade máxima da última marcha
    Vs.append((ns[-1] * math.pi * rw) / (30 * relacoesMarcha[-1] * relacaoFinal))

    # Construindo a curva final completa
    for i in range(len(Vs) - 1):
        v = np.linspace(Vs[i] + 1e-4, Vs[i + 1], 100)
        Vlist = np.concatenate((Vlist, v))
        Plist = np.concatenate((Plist, P((v * 30 * relacaoFinal * relacoesMarcha[i]) / (math.pi * rw))))

    return Plist, Vlist, Vs
