import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors


def plot_speed_vs_distance(df, distance_range=None, downsampling=None):
    df_plot = aplicar_slicing(df, distance_range, downsampling)

    plt.figure(figsize=(10, 5))
    plt.plot(df_plot['Distance'] / 1000, df_plot['Speed'] * 3.6, 'r')
    plt.xlabel('Distância (km)')
    plt.ylabel('Velocidade (km/h)')
    plt.title('Velocidade vs Distância')
    plt.grid()
    plt.show()


def plot_accelerations(df, distance_range=None, downsampling=None):
    df_plot = aplicar_slicing(df, distance_range, downsampling)

    plt.figure(figsize=(10, 5))
    plt.plot(df_plot['Distance'] / 1000, df_plot['Ay'], 'b:', label='Ay (m/s²)')
    plt.plot(df_plot['Distance'] / 1000, df_plot['Ax'], 'g--', label='Ax (m/s²)')
    plt.xlabel('Distância (km)')
    plt.ylabel('Aceleração (m/s²)')
    plt.title('Acelerações vs Distância')
    plt.legend()
    plt.grid()
    plt.show()


def plot_trajectory_colored_by_speed(df, x, y, distance_range=None, downsampling=None):
    df_plot = aplicar_slicing(df, distance_range, downsampling)

    step = downsampling if downsampling else 1
    x_plot = x[::step]
    y_plot = y[::step]

    plt.figure(figsize=(8, 8))
    sc = plt.scatter(x_plot[:-1], y_plot[:-1], c=3.6 * df_plot['Speed'], cmap='jet', s=10)
    cmap = cm.get_cmap("jet")
    norm = colors.Normalize(vmin=3.6 * df_plot['Speed'].min(), vmax=3.6 * df_plot['Speed'].max())
    cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), orientation='horizontal')
    cbar.set_label('Velocidade (km/h)')
    plt.axis('off')
    plt.title('Velocidade no Trajeto')
    plt.show()


def plot_speed_histogram(df, distance_range=None, downsampling=None):
    df_plot = aplicar_slicing(df, distance_range, downsampling)

    plt.figure(figsize=(8, 5))
    plt.hist(3.6 * df_plot['Speed'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Velocidade (km/h)')
    plt.ylabel('Frequência')
    plt.title('Histograma de Velocidade')
    plt.grid()
    plt.show()


def plot_ax_vs_ay(df, distance_range=None, downsampling=None):
    df_plot = aplicar_slicing(df, distance_range, downsampling)

    plt.figure(figsize=(8, 8))
    plt.scatter(df_plot['Ax'], df_plot['Ay'], c=3.6 * df_plot['Speed'], cmap='jet', s=10)
    plt.xlabel('Ax (m/s²)')
    plt.ylabel('Ay (m/s²)')
    plt.title('Ax vs Ay')
    cbar = plt.colorbar(label='Velocidade (km/h)')
    plt.grid()
    plt.show()


def graph(df, x, y, distance_range=None, downsampling=None):
    """
    Gera todos os gráficos principais da simulação.
    
    Parameters:
    - df: DataFrame da simulação
    - x, y: coordenadas do trajeto
    - distance_range: tupla (min_km, max_km) para slicing opcional
    - downsampling: inteiro para reduzir número de pontos (ex.: 10 plota 1 a cada 10)
    """
    if df.empty:
        print('⚠️ DataFrame está vazio. Nenhum gráfico gerado.')
        return

    print('Gerando gráficos...')
    plot_speed_vs_distance(df, distance_range, downsampling)
    plot_accelerations(df, distance_range, downsampling)
    plot_trajectory_colored_by_speed(df, x, y, distance_range, downsampling)
    plot_speed_histogram(df, distance_range, downsampling)
    plot_ax_vs_ay(df, distance_range, downsampling)
    print('✅ Gráficos gerados.')


def aplicar_slicing(df, distance_range=None, downsampling=None):
    """
    Função auxiliar para aplicar filtros de distância e downsampling.

    Parameters:
    - distance_range: tupla (min_km, max_km) ou None
    - downsampling: inteiro ou None

    Returns:
    - df_plot: DataFrame filtrado
    """
    df_plot = df.dropna(subset=["Distance"]).copy()

    if distance_range:
        min_km, max_km = distance_range
        df_plot = df_plot[(df_plot['Distance'] / 1000 >= min_km) &
                           (df_plot['Distance'] / 1000 <= max_km)]

    if downsampling:
        df_plot = df_plot.iloc[::downsampling]

    return df_plot
