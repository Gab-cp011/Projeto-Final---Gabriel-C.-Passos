
# 🏎️ Simulador Automotivo em Python

Este projeto é um **simulador de dinâmica veicular**, desenvolvido em Python, que permite calcular e visualizar o comportamento longitudinal e lateral de um veículo sobre uma trajetória definida.

O simulador considera:
- Dados geométricos da pista (incluindo altitude opcional).
- Dados físicos do veículo (massa, aerodinâmica, atrito, distribuição de peso).
- Curvas de potência e transmissão (opcional).
- Modelagem do círculo de aderência (Círculo de Kamm).

---

## 📦 Estrutura do Projeto

```plaintext
simulador/
├── core/
│   ├── dynamics.py            # Pré-processamento físico
│   ├── postprocessing.py      # Geração dos resultados (DataFrame)
│   ├── solver/                # Solver de dinâmica
│   ├── tools/                 # Funções auxiliares (geometria, filtros, plots, gps)
│   └── logger/                # Prints e logs
├── loop.py                    # Loop principal da simulação
├── main.py                    # Ponto de entrada do simulador
├── README.md                  # Este arquivo
```

---

## 🚀 Funcionalidades
- Simulação longitudinal e lateral.
- Cálculo de acelerações (`Ax`, `Ay`), forças, velocidades e tempo.
- Modelagem de inclinação (altitude).
- Cálculo de marchas, relações e RPM (opcional).
- Geração automática de gráficos:
  - Velocidade vs Distância
  - Acelerações
  - Curvatura do trajeto colorida por velocidade
  - Histograma de velocidades
  - Dispersão Ax vs Ay (círculo de aderência)

---

## ⚙️ Dependências

Instale os requisitos básicos:

```bash
pip install numpy pandas matplotlib scipy
```

---

## 🚗 Como Executar

1. Clone este repositório ou baixe os arquivos.
2. Acesse a pasta do projeto.
3. Execute o simulador:

```bash
python main.py
```

4. O resultado será salvo em `resultado_simulacao.csv` e os gráficos serão exibidos.

---

## 📄 Entrada da Simulação

### 📍 Trajetória
- Pode ser inserida de três formas:
  - Arquivo `.csv` contendo colunas `x`, `y`, `z`.
  - Inserção manual no próprio `main.py`.

### 🚙 Parâmetros do Veículo
- Massa (`m`)
- Altura do centro de massa (`h`)
- Área frontal (`Af`)
- Coeficientes aerodinâmicos (`Cd`, `Cl`)
- Coeficiente de rolamento (`Crr`)
- Distâncias entre eixos (`lt`, `ld`)
- Tipo de tração (`Tracao`: `'D'` dianteira ou `'T'` traseira)

### 🔥 Potência e Transmissão (opcional)
- Potência (`P`)
- Lista de potências por marcha (`Ps`)
- Rotações máximas (`ns`)
- Relações de marchas (`gearslist`)
- Relação do diferencial (`finaldrive`)
- Raio da roda (`rw`)

---

## 📈 Saída da Simulação
- Arquivo `resultado_simulacao.csv` contendo:
  - `Distance` — distância acumulada
  - `Speed` — velocidade (m/s)
  - `Ax` — aceleração longitudinal (m/s²)
  - `Ay` — aceleração lateral (m/s²)
  - `CurvatureRadius` — raio de curva
  - `Time` — tempo acumulado
  - `Force` — força longitudinal (N)
  - (Opcional) `Gears`, `GRatios`, `RPM`

- Gráficos automáticos via função `graph()`:
  - Visualização do trajeto com coloração por velocidade
  - Curvas de velocidade, aceleração, força e dispersão Ax vs Ay

---

## 🧠 Referências Físicas
- Segunda Lei de Newton
- Círculo de Kamm (ou Elipse de Tração) para aderência
- Modelagem de resistência aerodinâmica e rolamento
- Equação de Torricelli para correções retroativas

---

## 🔥 Melhorias Futuras
- Interface gráfica com Streamlit ou Dash
- Geração de relatórios automáticos (PDF)
- Exportação para telemetria em arquivos `.json` ou `.mat`
- Validação contra dados reais

---

## 👨‍🔬 Autor
Desenvolvido por **Gabriel Cândido Passos**, como parte do projeto final de graduação — **Desenvolvimento de um Software de Simulação da Dinâmica de Motocicletas**, de 2025, que tem sua base e fundamentos no projeto final de **João Marcos Cavalcante** - **Desenvolvimento de um Simulador Automotivo em Python**. 

---

## 🏁 Licença
Este projeto é acadêmico e livre para uso educacional. Direitos reservados.
