import numpy as np
from scipy.interpolate import interp1d
from math import sqrt, asin
from scipy.interpolate import interp1d, splprep, splev, splrep
from filtros import aplicar_butterworth

def interpolar_trajetoria(x, y, z, deltaD, use_z=False, method='quadratic', butter_params=None, s=20, auto_fs=True):
    """
    Interpola pontos ao longo de uma trajetória.

    Args:
        x, y, z (array-like): Coordenadas da trajetória.
        deltaD (float): Distância desejada entre os novos pontos (m).
        use_z (bool): Considerar ou não a coordenada z na interpolação.
        method (str): 'quadratic', 'cubic' ou 'splineS'.
        butter_params (dict, optional): Parâmetros do filtro Butterworth:
            {'cutoff': frequência de corte, 'order': ordem do filtro, 'fs': freq. de amostragem (opcional)}
        s (float): Parâmetro de suavização da splineS (default = 20)
        auto_fs (bool): Se True, calcula automaticamente fs como 1/deltaD. Se False, espera butter_params['fs']

    Returns:
        tuple: x_interp, y_interp, z_interp (arrays interpolados)
    """

    x, y, z = np.asarray(x), np.asarray(y), np.asarray(z)

    # Cria pontos 2D ou 3D conforme configuração
    points = np.column_stack((x, y, z)) if use_z else np.column_stack((x, y))

    # Distância incremental e total
    segment_dist = np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1))
    total_dist = np.sum(segment_dist)

    # Distância acumulada normalizada
    distance = np.insert(np.cumsum(segment_dist), 0, 0)
    distance /= distance[-1]

    num_points = int(total_dist / deltaD) + 1
    alpha = np.linspace(0, 1, num_points)

    # Interpolação
    if method in ['quadratic', 'cubic']:
        interpolator = interp1d(distance, points, kind=method, axis=0)
        interp_points = interpolator(alpha)

    elif method == 'splineS':
        tck, _ = splprep([x, y, z] if use_z else [x, y], s=s)
        res = splev(np.linspace(0, 1, num_points), tck)
        x_s, y_s = res[0], res[1]
        z_s = res[2] if use_z else np.zeros_like(x_s)
        interp_points = np.column_stack((x_s, y_s, z_s))

    else:
        raise ValueError("method must be 'quadratic', 'cubic' or 'splineS'")

    if not use_z:
        z_col = np.zeros((interp_points.shape[0], 1))
        interp_points = np.hstack((interp_points[:, :2], z_col))

    x_interp, y_interp, z_interp = interp_points.T

    # Aplica filtro Butterworth após interpolar
    if butter_params:
        if auto_fs:
            fs = 1 / deltaD
        else:
            if 'fs' not in butter_params:
                raise ValueError("Frequência de amostragem 'fs' deve ser fornecida em butter_params se auto_fs=False")
            fs = butter_params['fs']

        x_interp, y_interp, z_interp = aplicar_butterworth(x_interp, y_interp, z_interp, use_z,
                                                            fs=fs,
                                                            butter_cutoff=butter_params['cutoff'],
                                                            butter_order=butter_params['order'])

    return x_interp, y_interp, z_interp


def distanceXYZ(x, y, z=None, use_z=False):
    """
    Calcula distância entre pontos consecutivos.
    Se use_z=True, inclui a componente de altitude (z).
    """
    D = []
    for i in range(0, len(x) - 1):
        dx = (x[i + 1] - x[i]) ** 2
        dy = (y[i + 1] - y[i]) ** 2
        if use_z and z is not None:
            dz = (z[i + 1] - z[i]) ** 2
        else:
            dz = 0
        D.append((dx + dy + dz) ** 0.5)
    return D

def radiusXYZ(x, y, z=None):
    """
    Calcula o raio de curvatura baseado em três pontos consecutivos.
    """
    R = []
    for i in range(0, len(x) - 2):
        a = sqrt((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2 + ((z[i + 1] - z[i]) ** 2 if z is not None else 0))
        b = sqrt((x[i + 2] - x[i + 1]) ** 2 + (y[i + 2] - y[i + 1]) ** 2 + ((z[i + 2] - z[i + 1]) ** 2 if z is not None else 0))
        c = sqrt((x[i + 2] - x[i]) ** 2 + (y[i + 2] - y[i]) ** 2 + ((z[i + 2] - z[i]) ** 2 if z is not None else 0))

        p = (a + b + c) / 2
        A2 = p * (p - a) * (p - b) * (p - c)

        if A2 <= 0:
            r = 1e10
            R.append(r)
        else:
            A = sqrt(A2)
            r = a * b * c / (4 * A)
            R.append(r)

    return R

#Inclinacao da pista:
def grading(altitude,distanceseg):
    angle = []
    for i in range(1,len(distanceseg)):
        anglei = asin((altitude[i+1]-altitude[i])/(distanceseg[i]))
        angle.append(anglei)
    for i in range(0, len(angle) - 1): # limitando a inclinacao em 0.2 rad
        if abs(angle[i]) > 0.2:
            if angle[i] > 0:
                angle[i] = 0.2
            elif angle[i] < 0:
                angle[i] = -0.2
    return angle

#Identificacao da direcao da curva (-1 para esquerda, 1 para direita):
def curva(x,y):
    c = []
    l = list(zip(y, x))
    for i in range(0, len(l) - 2):
        A = [[l[i][0], l[i][1], 1], [l[i + 1][0], l[i + 1][1], 1], [l[i +2][0], l[i + 2][1], 1]] # alteração feita no sinal da curva, era 1 e -1 
        if np.linalg.det(A) > 0: # originalmente é -1
            c.append(1)
        elif np.linalg.det(A) < 0: # originalmente é 1 
            c.append(-1)
        else:
            c.append(0)
    return c
