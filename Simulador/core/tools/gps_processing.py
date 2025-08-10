import numpy as np
from geopy.distance import geodesic
from pyproj import Transformer

def calcular_utm_epsg(lat, lon):
    """
    Calcula o código EPSG UTM automaticamente baseado na latitude e longitude.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        str: Código EPSG adequado para a zona UTM.
    """
    zona = int((lon + 180) / 6) + 1
    hemisferio = 326 if lat >= 0 else 327
    epsg_code = f"EPSG:{hemisferio}{zona:02d}"
    return epsg_code


def latlon_to_xy(lat, lon, method='haversine', utm_epsg=None):
    """
    Converte latitude e longitude para coordenadas em metros.

    Args:
        lat (array-like): Vetor de latitudes.
        lon (array-like): Vetor de longitudes.
        method (str): Método de conversão. Opções:
                      'haversine', 'geopy', 'utm'
        utm_epsg (str, optional): Código EPSG UTM. Se None e method='utm', calcula automaticamente.

    Returns:
        tuple: (x, y) em metros
    """
    lat = np.asarray(lat)
    lon = np.asarray(lon)

    if method == 'haversine':
        R = 6378137
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        x = (lon_rad - lon_rad[0]) * R * np.cos(lat_rad[0])
        y = (lat_rad - lat_rad[0]) * R

    elif method == 'geopy':
        x = [0]
        y = [0]
        lat_ref, lon_ref = lat[0], lon[0]
        for i in range(1, len(lat)):
            dx = geodesic((lat_ref, lon_ref), (lat_ref, lon[i])).meters
            dy = geodesic((lat_ref, lon_ref), (lat[i], lon_ref)).meters

            if lon[i] < lon_ref:
                dx *= -1
            if lat[i] < lat_ref:
                dy *= -1

            x.append(x[-1] + dx)
            y.append(y[-1] + dy)

        x = np.array(x)
        y = np.array(y)

    elif method == 'utm':
        if utm_epsg is None:
            utm_epsg = calcular_utm_epsg(lat[0], lon[0])
        transformer = Transformer.from_crs("EPSG:4326", utm_epsg, always_xy=True)
        x, y = transformer.transform(lon, lat)
        x, y = np.array(x), np.array(y)

    else:
        raise ValueError("method deve ser 'haversine', 'geopy' ou 'utm'")

    return x, y
