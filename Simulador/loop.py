import numpy as np
import pandas as pd
import math
from scipy.interpolate import interp1d
from core.preprocessamento import preprocessar_condicoes_iniciais
from core.posprocessamento import construir_dataframe_simulacao, adicionar_dados_de_marcha
from core.solver.roots import Roots
from core.solver.velocity_correction import corrigir_velocidade

def loop(fx,fy,x,y,z,P,m,Cl,Cd,Af,Crr,ld,lt,h,Tracao,Vo,
        Frenagem,Vmax,mu,nu,marcha=False,Ps=0,ns=0,finaldrive=0,
        gearslist=0,rw=0, use_z=False):
    
        # ⇨ PRÉ-PROCESSAMENTO MODULARIZADO
    dados = preprocessar_condicoes_iniciais(
        P=P, Ps=Ps, marcha=marcha, ns=ns, finaldrive=finaldrive,
        gearslist=gearslist, rw=rw,
        x=x, y=y, z=z, Vo=Vo, Vmax=Vmax, m=m,
        Cl=Cl, Cd=Cd, Af=Af, Crr=Crr,
        use_z=use_z
    )

    # ⇨ VARIÁVEIS EXTRAÍDAS DO DICIONÁRIO
    P = dados["P"]
    Pv = dados["Pv"]
    pcurve = dados["pcurve"]
    g = dados["g"]
    R = dados["R"]
    D = dados["D"]
    angle = dados["angle"]
    V = dados["V"]
    Vmax = dados["Vmax"]
    meq = dados["meq"] # não usado
    kl = dados["kl"]
    ka = dados["ka"] # não usado
    k = dados["k"]
    slope = dados["slope"]

    
    Axmin = Frenagem * g * fx
    AxmaxL, AymaxL = [], []


    contagem_metodo = {
        "Correção por Torricelli Modificado": 0,
        "Correção por fórmula V1": 0
    }

    contagem_sucesso = {
        "Correção local (j=0) ": 0,
        "Correção retroativa (j>0) ": 0
    }



    for i in range(len(R)):
        Aymax = fy * (nu * g * math.cos(angle[i]) - kl * V[i]**2 / m)

        if Tracao == 'D':
            Axmax = lt * fx * ((mu * g * math.cos(angle[i]) - mu * kl * V[i]**2 / m) / (ld + h * mu + lt))
        else:
            Axmax = ld * fx * ((mu * g * math.cos(angle[i]) - mu * kl * V[i]**2 / m) / (ld - h * mu + lt))

        AxmaxL.append(Axmax)
        AymaxL.append(Aymax)

        resultado_roots = Roots(V[i], D[i], R[i], AxmaxL[i], Axmin, AymaxL[i], slope[i], g, k, pcurve, m, Pv, marcha, P, verbose=False)

        #print_iteration_info(i, V[i], D[i], R[i], slope[i], Axmax, Aymax, resultado_roots)

        if resultado_roots != False:

            Viplus1 = resultado_roots[1][1]

            if Viplus1 > Vmax:
                Viplus1 = Vmax

            V.append(Viplus1)
            
        else:
            V = corrigir_velocidade(i, V, R, D, slope, AxmaxL, Axmin, AymaxL, k, g,
                pcurve, m, Pv, marcha, P,mu, contagem_metodo, contagem_sucesso) 
                

    df = construir_dataframe_simulacao(V, D, R, x, y, m)

    if marcha:
        df = adicionar_dados_de_marcha(df, pcurve, gearslist, finaldrive, rw)

    return df