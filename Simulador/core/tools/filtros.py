import numpy as np
from scipy.signal import butter, filtfilt

# Talvez colocar mais alguns filtros possíveis para processamento de sinal futuramente 

def aplicar_butterworth(x, y, z=None, use_z=False, butter_cutoff=0.1, butter_order=4, fs=None):
    """
    Aplica o filtro Butterworth em x, y (e z se fornecido).

    Args:
        x, y, z (array-like): Coordenadas.
        use_z (bool): Considerar z na filtragem.
        butter_cutoff (float): Frequência de corte.
        butter_order (int): Ordem do filtro.
        fs (float): Frequência de amostragem.

    Returns:
        tuple: (x_filtrado, y_filtrado, z_filtrado)

        ## Frequência de Corte Recomendada para o Filtro Butterworth
s
    A escolha da frequência de corte (`cutoff`) depende diretamente do espaçamento entre os pontos interpolados (`deltaD`). 

    A tabela abaixo sugere valores típicos para projetos de análise e simulação de trajetórias baseadas em dados GPS/KML:

    | deltaD (Espaçamento dos pontos) | Frequência de Amostragem fs = 1/deltaD (Hz) | Frequência de Corte sugerida (cutoff) | Comentário |
    |---------------------------------|----------------------------------------------|----------------------------------------|------------|
    | 0.1 m                           | 10 Hz                                       | 0.5 a 1 Hz                             | Dados muito detalhados, remove apenas ruído fino |
    | 0.5 m                           | 2 Hz                                        | 0.2 a 0.5 Hz                           | Caminhos detalhados, com leve suavização |
    | 1.0 m                           | 1 Hz                                        | 0.1 a 0.3 Hz                           | Uso geral para dados KML / GPS urbanos |
    | 2.0 m                           | 0.5 Hz                                      | 0.05 a 0.2 Hz                          | Grandes trajetos urbanos ou mistos |
    | 5.0 m                           | 0.2 Hz                                      | 0.03 a 0.1 Hz                          | Estradas, rodovias, percursos longos |
    | 10.0 m                          | 0.1 Hz                                      | 0.02 a 0.05 Hz                         | Mapas de longa distância, macro trajetos |

    ---

    ### Regras gerais:

    - Frequência de Amostragem:
    ```python
    fs = 1 / deltaD

    """
    x, y = np.asarray(x), np.asarray(y)
    if use_z:
        z = np.asarray(z)

    if fs is None:
        fs = len(x) / (x[-1] - x[0])

    nyq = 0.5 * fs
    normal_cutoff = butter_cutoff / nyq
    b, a = butter(butter_order, normal_cutoff, btype='low', analog=False)

    x_f = filtfilt(b, a, x)
    y_f = filtfilt(b, a, y)
    z_f = filtfilt(b, a, z) if use_z else np.zeros_like(x_f)

    return x_f, y_f, z_f
