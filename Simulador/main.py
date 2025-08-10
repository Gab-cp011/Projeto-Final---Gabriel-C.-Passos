import pandas as pd
from loop import loop
from core.tools.plots import graph


def carregar_trajetoria(csv_path=None):
    """
    Carrega a trajetória a partir de KML, CSV ou manual.

    Retorna:
    - x, y, z: listas de coordenadas
    """


    if csv_path: 
        df = pd.read_csv(csv_path)
        x, y, z = df['x'].tolist(), df['y'].tolist(), df['z'].tolist()

    else:
        # Inserção manual de exemplo
        x = []  # Preencher lista de X
        y = []  # Preencher lista de Y
        z = []  # Preencher lista de Z (altitude)

    return x, y, z


def main():
    """
    Template geral do simulador automotivo.
    Preencha os parâmetros abaixo.
    """

    # === Trajetória ===
    x, y, z = carregar_trajetoria(
        csv_path=None      # Exemplo: 'trajetoria.csv'
    )

    # === Parâmetros do Veículo ===
    m = None           # Massa [kg]
    Cl = None          # Coef. sustentação
    Cd = None          # Coef. arrasto
    Af = None          # Área frontal [m²]
    Crr = None         # Coef. rolamento
    lt = None          # Distância eixo traseiro ao CM [m]
    ld = None          # Distância eixo dianteiro ao CM [m]
    h = None           # Altura do CM [m]
    Tracao = None      # 'D' dianteira ou 'T' traseira

    # === Parâmetros físicos ===
    fx = None
    fy = None
    mu = None
    nu = None
    Frenagem = None

    Vo = None          # Velocidade inicial [km/h]
    Vmax = None        # Velocidade máxima [km/h]
    use_z = True       # Usa inclinação (altitude) se True

    # === Potência e transmissão ===
    marcha = False     # True para simular com marchas
    P = None           # Potência máxima [cv]
    Ps = []            # Lista de potências por marcha [cv]
    ns = []            # Lista de rotações máximas por marcha [rpm]
    finaldrive = None  # Relação do diferencial
    gearslist = []     # Relações de marcha
    rw = None          # Raio da roda [m]

    # === Executa a Simulação ===
    df = loop(
        fx, fy, x, y, z, P, m, Cl, Cd, Af, Crr,
        ld, lt, h, Tracao, Vo, Frenagem, Vmax,
        mu, nu, marcha, Ps, ns, finaldrive,
        gearslist, rw, use_z=use_z
    )

    # === Exporta resultado ===
    df.to_csv('resultado_simulacao.csv', index=False)
    print('✅ Resultado salvo em resultado_simulacao.csv')

    # === Geração de Gráficos ===
    graph(
        df, x, y,
        distance_range=None,   # Exemplo: (0, 5) para 0 a 5 km, ou None para tudo
        downsampling=None      # Exemplo: 10 para subamostrar, ou None
    )


if __name__ == '__main__':
    main()
