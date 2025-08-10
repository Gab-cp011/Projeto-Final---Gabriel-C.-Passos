import numpy as np
import pandas as pd
import math
from tools.geometria import curva

def construir_dataframe_simulacao(V, D, R, x, y, m):
    Ay = [V[i + 1] ** 2 / R[i] for i in range(0, len(R))]
    Ax = [(V[i + 1] ** 2 - V[i] ** 2) / (2 * D[i]) for i in range(0, len(R))]

    Dcum = np.cumsum(D[:])

    c = curva(x, y)
    Ay = [i1 * i2 for i1, i2 in zip(Ay, c)]

    Ax = [0] + Ax
    Ay = [0] + Ay

    R_alinhado = [np.nan, np.nan] + R

    N = len(V)

    if len(Ay) < N:
        Ay.append(np.nan)
    if len(Ax) < N:
        Ax.append(np.nan)

    Dcum = Dcum[:N]
    Ay = Ay[:N]
    Ax = Ax[:N]
    R_alinhado = R_alinhado[:N]

    df = pd.DataFrame({
        'Distance': Dcum,
        'Speed': V,
        'Ay': Ay,
        'Ax': Ax,
        'CurvatureRadius': R_alinhado
    })

    t = []
    for i in range(len(Ax) - 2):
        if Ax[i + 1] == 0:
            t.append(D[i] / V[i])
        else:
            t.append((V[i + 1] - V[i]) / Ax[i + 1])

    t = list(np.cumsum(t))
    t += [0] + [np.nan]
    df['Time'] = t

    df['Force'] = m * df.Ax

    return df

def adicionar_dados_de_marcha(df, pcurve, gearslist, finaldrive, rw):
    gears = []
    Vs = pcurve[2]
    Vs = Vs[1:-1]
    print(Vs)

    for i in df.Speed:
        gear = False
        for j in list(range(0, len(Vs)))[::-1]:
            if i > Vs[j]:
                gear = j + 2
                break
        if gear == False:
            gear = 1
        gears.append(gear)

    df['Gears'] = gears

    gr = []
    listgear = list(range(1, len(gearslist) + 1))

    for i in gears:
        gr.append(gearslist[listgear.index(i)])

    df['GRatios'] = gr
    enginerotation = []

    for i in range(0, len(df.Speed)):
        omega = df.Speed[i] * df.GRatios[i] * finaldrive * 30 / (rw * math.pi)
        if omega < 1000:
            omega = 1000
        enginerotation.append(omega)

    df['RPM'] = enginerotation

    return df
