import matplotlib.pyplot as plt  # for plotting
from trafico.clases.TiposDispositivos import TiposDispositivos
import copy
import numpy as np
from scipy.stats import expon
import pandas as pd

def graficaralarmas(archivoEventos, archivoAlarmas, archivodispositivos,archivoconfig, tipodisp,alarmanum):

    numAlarma=alarmanum
    if(tipodisp==TiposDispositivos.TIPO1):
        tipo=1
    elif(tipodisp==TiposDispositivos.TIPO2):
        tipo=2
    elif(tipodisp==TiposDispositivos.TIPO3):
        tipo=3
    elif (tipodisp == TiposDispositivos.TIPO4):
        tipo = 4
    elif (tipodisp == TiposDispositivos.TIPO5):
        tipo = 5
    elif (tipodisp == TiposDispositivos.TIPO6):
        tipo = 6
    else:
        tipo=7


    df_eventos_rec = pd.read_csv(archivoEventos, index_col=0)
    # Convertir de DataFrame a Lista
    ListaEventos = df_eventos_rec.values.tolist()

    df_alarmas_rec = pd.read_csv(archivoAlarmas, index_col=0)
    # Convertir de DataFrame a Lista
    ListaAlarmas = df_alarmas_rec.values.tolist()

    df_dispositivos_rec = pd.read_csv(archivodispositivos, index_col=0)
    # Convertir de DataFrame a Lista
    ListaDispositivos = df_dispositivos_rec.values.tolist()

    df_config_rec = pd.read_csv(archivoconfig, index_col=0)
    # Convertir de DataFrame a Lista
    ListaConfig = df_config_rec.values.tolist()

    fig, ax = plt.subplots(1, 1)
    titulo='UEs de tipo '+str(tipodisp)+' activados por una alarma'
    fig.canvas.set_window_title(titulo)

    for alarma in ListaAlarmas:
        if (alarma[0]==tipo and alarma[1]==numAlarma):
            xxalarma=alarma[3]
            yyalarma = alarma[4]

    dispEnAlarma=[]
    xxdispEnAlarma=[]
    yydispEnAlarma=[]
    numDispEnAlarma=0

    for evento in ListaEventos:
        if evento[0]==numAlarma and evento[3]==tipodisp:
            indice=evento[2]-1
            dispEnAlarma.append(ListaDispositivos[indice])
            xxdispEnAlarma.append(ListaDispositivos[indice][2])
            yydispEnAlarma.append(ListaDispositivos[indice][3])
            numDispEnAlarma=numDispEnAlarma+1

    heatmap, xedges, yedges = np.histogram2d(xxdispEnAlarma, yydispEnAlarma, bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    titulo2=str(numDispEnAlarma)+' dispositivos entraron en alarma'
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.scatter(xxalarma, yyalarma, s=20, label='alarma', edgecolors="r", facecolor='r', marker="*")
    plt.title(titulo2)
    plt.legend(loc='upper right')
    plt.show()

    #if(modeloespacial==0): # Decaying exponential

    #else: # rised-cosine window

def graficardispositivos(archivoDispositivosTodos,archivoConfig):
    df_dispositivos_rec = pd.read_csv(archivoDispositivosTodos, index_col=0)
    # Convertir de DataFrame a Lista
    ListaDispositivos = df_dispositivos_rec.values.tolist()

    df_config_rec = pd.read_csv(archivoConfig, index_col=0)
    # Convertir de DataFrame a Lista
    ListaConfig = df_config_rec.values.tolist()

    fig, ax = plt.subplots(1, 1)
    fig.canvas.set_window_title('Ubicación de UEs en la célula')
    # Graficando en el círculo
    #xx = [dispositivo[2] for dispositivo in ListaDispositivos]
    #yy = [dispositivo[3] for dispositivo in ListaDispositivos] , TiposDispositivos.tiponumero(dispositivo[1])
    ax.scatter(0, 0,s=100,label='Control de iluminacion', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Control de iluminacion'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Monitoreo de agua y elect.', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Monitoreo de agua y electricidad'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Deteccion de terremotos', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Deteccion de terremotos'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Semaforos inteligentes', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Semaforos inteligentes'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Contaminacion del aire', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Contaminacion del aire'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Otros dispositivos mMTC', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Otros dispositivos mMTC'), alpha=1, marker=".")
    ax.scatter(0, 0,s=100, label='Dispositivos URLLC', edgecolor='w',
               facecolor=TiposDispositivos.tipocolor('Dispositivos URLLC'), alpha=1, marker=".")


    for dispositivo in ListaDispositivos:
        ax.scatter(dispositivo[2], dispositivo[3], s=100, edgecolor='w', facecolor=TiposDispositivos.tipocolor(dispositivo[1]), alpha=1, marker=".")
    ax.scatter(0,0, s=100, label='eNB',edgecolors="k", facecolor='k', marker="1")
    ax.legend(loc='upper right')
    titulo="Ubicación de "+ str(len(ListaDispositivos)) +" UEs. Célula de radio= "+ str(ListaConfig[0][1]) + " m"
    plt.title(titulo)
    plt.ylabel('Eje vertical')
    plt.xlabel('Eje Horizontal')
    plt.axis('equal')


def histogramatodoseventos(archivoEventos,archivoConfig):
    df_eventos_rec = pd.read_csv(archivoEventos, index_col=0)
    # Convertir de DataFrame a Lista
    ListaEventos = df_eventos_rec.values.tolist()

    df_config_rec = pd.read_csv(archivoConfig, index_col=0)
    # Convertir de DataFrame a Lista
    ListaConfig = df_config_rec.values.tolist()

    fig, ax2 = plt.subplots(1, 1)
    fig.canvas.set_window_title('Histograma de eventos')

    tiempoEvento= [evento[1] for evento in ListaEventos]

    ax2.hist(tiempoEvento, density=False, range=(0,ListaConfig[0][2]), bins=int(ListaConfig[0][3])+1  ) #rwidth=1 range=(0,tiempofinal)
    plt.title("Histograma de eventos en el tiempo, todos los UEs")
    plt.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
    plt.ylabel('Eventos')
    plt.xlabel('Tiempo (s)')
    plt.axhline()

def graficareventosportipodispositivo(archivoEventos,archivoConfig,archivoAlarmas, tipodisp):
    df_eventos_rec = pd.read_csv(archivoEventos, index_col=0)
    # Convertir de DataFrame a Lista
    ListaEventos = df_eventos_rec.values.tolist()

    df_config_rec = pd.read_csv(archivoConfig, index_col=0)
    # Convertir de DataFrame a Lista
    ListaConfig = df_config_rec.values.tolist()

    df_alarmas_rec = pd.read_csv(archivoAlarmas, index_col=0)
    # Convertir de DataFrame a Lista
    ListaAlarmas = df_alarmas_rec.values.tolist()

    # simulación
    tiempofinal = ListaConfig[0][2]
    bins= int(ListaConfig[0][3])
    dispositivos = [ disp[0] for disp in ListaConfig]

    if (tipodisp == TiposDispositivos.TIPO1):
        ## Tipo 1
        if 1 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 1:
                    indice_Tipo1=x
            fig1=plt.figure()
            ax11 = fig1.add_subplot(121)
            ax12 = fig1.add_subplot(122)
            periodico_Tipo1 = int(ListaConfig[indice_Tipo1][1])
            tasaEventos_Tipo1 = ListaConfig[indice_Tipo1][2]
            tasaAlarmas_Tipo1 = ListaConfig[indice_Tipo1][3]
            color_Tipo1 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO1)

    elif (tipodisp == TiposDispositivos.TIPO2):
        ## Tipo 2
        if 2 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 2:
                    indice_Tipo2=x
            fig2 = plt.figure()
            ax21 = fig2.add_subplot(121)
            ax22 = fig2.add_subplot(122)
            periodico_Tipo2 = int(ListaConfig[indice_Tipo2][1])
            tasaEventos_Tipo2 = ListaConfig[indice_Tipo2][2]
            tasaAlarmas_Tipo2 = ListaConfig[indice_Tipo2][3]
            color_Tipo2 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO2)

    elif (tipodisp == TiposDispositivos.TIPO3):
        ## Tipo 3
        if 3 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 3:
                    indice_Tipo3=x
            fig3 = plt.figure()
            ax31 = fig3.add_subplot(121)
            ax32 = fig3.add_subplot(122)
            periodico_Tipo3 = int(ListaConfig[indice_Tipo3][1])
            tasaEventos_Tipo3 = ListaConfig[indice_Tipo3][2]
            tasaAlarmas_Tipo3 = ListaConfig[indice_Tipo3][3]
            color_Tipo3 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO3)

    elif (tipodisp == TiposDispositivos.TIPO4):
        ## Tipo 4
        if 4 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 4:
                    indice_Tipo4=x
            fig4 = plt.figure()
            ax41 = fig4.add_subplot(121)
            ax42 = fig4.add_subplot(122)
            periodico_Tipo4 = int(ListaConfig[indice_Tipo4][1])
            tasaEventos_Tipo4 = ListaConfig[indice_Tipo4][2]
            tasaAlarmas_Tipo4 = ListaConfig[indice_Tipo4][3]
            color_Tipo4 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO4)

    elif (tipodisp == TiposDispositivos.TIPO5):
        ## Tipo5
        if 5 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 5:
                    indice_Tipo5=x
            fig5 = plt.figure()
            ax51 = fig5.add_subplot(121)
            ax52 = fig5.add_subplot(122)
            periodico_Tipo5 = int(ListaConfig[indice_Tipo5][1])
            tasaEventos_Tipo5 = ListaConfig[indice_Tipo5][2]
            tasaAlarmas_Tipo5 = ListaConfig[indice_Tipo5][3]
            color_Tipo5 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO5)

    elif (tipodisp == TiposDispositivos.TIPO6):
        ## Tipo 6
        if 6 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 6:
                    indice_Tipo6=x
            fig6 = plt.figure()
            ax61 = fig6.add_subplot(121)
            ax62 = fig6.add_subplot(122)
            periodico_Tipo6 = int(ListaConfig[indice_Tipo6][1])
            tasaEventos_Tipo6 = ListaConfig[indice_Tipo6][2]
            tasaAlarmas_Tipo6 = ListaConfig[indice_Tipo6][3]
            color_Tipo6 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO6)
    else:
        ## Tipo 7
        if 7 in dispositivos:
            for x in range(0,len(dispositivos)):
                if dispositivos[x]== 7:
                    indice_Tipo7=x
            fig7 = plt.figure()
            ax71 = fig7.add_subplot(121)
            ax72 = fig7.add_subplot(122)
            periodico_Tipo7 = int(ListaConfig[indice_Tipo7][1])
            tasaEventos_Tipo7 = ListaConfig[indice_Tipo7][2]
            tasaAlarmas_Tipo7 = ListaConfig[indice_Tipo7][3]
            color_Tipo7 = TiposDispositivos.tipocolor(TiposDispositivos.TIPO7)

    dispTipo1 = []
    alarmasTipo1 = []
    dispTipo2 = []
    alarmasTipo2 = []
    dispTipo3 = []
    alarmasTipo3 = []
    dispTipo4 = []
    alarmasTipo4 = []
    dispTipo5 = []
    alarmasTipo5 = []
    dispTipo6 = []
    alarmasTipo6 = []
    dispTipo7 = []
    alarmasTipo7 = []

    for dispositivo in ListaEventos:
        if dispositivo[3] == TiposDispositivos.TIPO1:
            dispTipo1.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO2:
            dispTipo2.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO3:
            dispTipo3.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO4:
            dispTipo4.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO5:
            dispTipo5.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO6:
            dispTipo6.append(dispositivo[1])
        elif dispositivo[3] == TiposDispositivos.TIPO7:
            dispTipo7.append(dispositivo[1])

    for alarma in ListaAlarmas:
        if alarma[0] == 1:
            alarmasTipo1.append(alarma[2])
        elif alarma[0] == 2:
            alarmasTipo2.append(alarma[2])
        elif alarma[0] == 3:
            alarmasTipo3.append(alarma[2])
        elif alarma[0] == 4:
            alarmasTipo4.append(alarma[2])
        elif alarma[0] == 5:
            alarmasTipo5.append(alarma[2])
        elif alarma[0] == 6:
            alarmasTipo6.append(alarma[2])
        elif alarma[0] == 7:
            alarmasTipo7.append(alarma[2])
######
    if (tipodisp == TiposDispositivos.TIPO1):
        ## Tipo 1
        if 1 in dispositivos:

            c1, b1, _ = ax11.hist(dispTipo1, color=color_Tipo1,label='paquetes',density=False, range=(0, tiempofinal), bins=bins + 1)
            ax11.vlines(alarmasTipo1, 0, max(c1),label='alarmas', colors='r', lw=2, alpha=0.2)
            ax11.legend(loc='upper right')
            fig1.canvas.set_window_title(TiposDispositivos.TIPO1)
            titulo = "Histograma de eventos en el tiempo"
            ax11.title.set_text(titulo)
            ax11.set_ylabel('Eventos')
            ax11.set_xlabel('Tiempo')
            ax11.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos1 = graficarlambdaeventos(ListaEventos,TiposDispositivos.TIPO1)
            lambdaAlarmas1=[]
            if(periodico_Tipo1==0):
                count1, bins1, _ = ax12.hist(lambdaEventos1, color=color_Tipo1,label='histograma eventos (normalizado)', density=True, bins=30,alpha=0.4)
                x = np.linspace(0, max(bins1), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo1)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo1)
                ax12.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas1 = graficarlambdaalarmas(alarmasTipo1)
                cnt1, bin1, _ = ax12.hist(lambdaAlarmas1, color='grey', label='histograma alarmas (normalizado)',
                                             density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin1), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo1)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo1)
                ax12.plot(x, y, "-.", color='r', label=label)
                #
                ax12.legend(loc='upper right')
                ax12.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax12.vlines(lambdaEventos1, 0, lambdaEventos1, colors=color_Tipo1, lw=5, alpha=0.5)
            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos1))+") y alarmas ("+str(len(lambdaAlarmas1))+")"
            ax12.title.set_text(titulo)
            ax12.set_ylabel('Función de Densidad de Probabilidad')
            ax12.set_xlabel('Tiempo (s)')


####
    elif (tipodisp == TiposDispositivos.TIPO2):
        ## Tipo 2
        if 2 in dispositivos:


            c2, b2, _ = ax21.hist(dispTipo2, color=color_Tipo2, label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax21.vlines(alarmasTipo2, 0, max(c2), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax21.legend(loc='upper right')
            fig2.canvas.set_window_title(TiposDispositivos.TIPO2)
            titulo = "Histograma de eventos en el tiempo"
            ax21.title.set_text(titulo)
            ax21.set_ylabel('Eventos')
            ax21.set_xlabel('Tiempo')
            ax21.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos2 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO2)
            lambdaAlarmas2 = []
            if (periodico_Tipo2 == 0):
                count2, bins2, _ = ax22.hist(lambdaEventos2, color=color_Tipo2, label='histograma eventos (normalizado)',
                                             density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins2), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo2)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo2)
                ax22.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas2 = graficarlambdaalarmas(alarmasTipo2)
                cnt2, bin2, _ = ax22.hist(lambdaAlarmas2, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin2), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo2)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo2)
                ax22.plot(x, y, "-.", color='r', label=label)
                #
                ax22.legend(loc='upper right')
                ax22.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax22.vlines(lambdaEventos2, 0, lambdaEventos2, colors=color_Tipo2, lw=5, alpha=0.5)

            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos2))+") y alarmas ("+str(len(lambdaAlarmas2))+")"
            ax22.title.set_text(titulo)
            ax22.set_ylabel('PDF')
            ax22.set_xlabel('tiempo')


####
    elif (tipodisp == TiposDispositivos.TIPO3):
        ## Tipo 3
        if 3 in dispositivos:

            c3, b3, _ = ax31.hist(dispTipo3,color=color_Tipo3, label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax31.vlines(alarmasTipo3, 0, max(c3), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax31.legend(loc='upper right')
            fig3.canvas.set_window_title(TiposDispositivos.TIPO3)
            titulo = "Histograma de eventos en el tiempo"
            ax31.title.set_text(titulo)
            ax31.set_ylabel('Eventos')
            ax31.set_xlabel('Tiempo')
            ax31.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos3 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO3)
            lambdaAlarmas3 = []
            if (periodico_Tipo3 == 0):
                count3, bins3, _ = ax32.hist(lambdaEventos3, color=color_Tipo3,label='histograma eventos (normalizado)', density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins3), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo3)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo3)
                ax32.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas3 = graficarlambdaalarmas(alarmasTipo3)
                cnt3, bin3, _ = ax32.hist(lambdaAlarmas3, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin3), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo3)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo3)
                ax32.plot(x, y, "-.", color='r', label=label)
                #
                ax32.legend(loc='upper right')
                ax32.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax32.vlines(lambdaEventos3, 0, lambdaEventos3, colors=color_Tipo3, lw=5, alpha=0.5)
            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos3))+") y alarmas ("+str(len(lambdaAlarmas3))+")"
            ax32.title.set_text(titulo)
            ax32.set_ylabel('PDF')
            ax32.set_xlabel('tiempo')


###
    elif (tipodisp == TiposDispositivos.TIPO4):
        ## Tipo 4
        if 4 in dispositivos:

            c4, b4, _ = ax41.hist(dispTipo4,color=color_Tipo4, label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax41.vlines(alarmasTipo4, 0, max(c4), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax41.legend(loc='upper right')
            fig4.canvas.set_window_title(TiposDispositivos.TIPO4)
            titulo = "Histograma de eventos en el tiempo"
            ax41.title.set_text(titulo)
            ax41.set_ylabel('Eventos')
            ax41.set_xlabel('Tiempo')
            ax41.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos4 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO4)
            lambdaAlarmas4 = []
            if (periodico_Tipo4 == 0):
                count4, bins4, _ = ax42.hist(lambdaEventos4,color=color_Tipo4, label='histograma eventos (normalizado)', density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins4), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo4)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo4)
                ax42.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas4 = graficarlambdaalarmas(alarmasTipo4)
                cnt4, bin4, _ = ax42.hist(lambdaAlarmas4, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin4), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo4)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo4)
                ax42.plot(x, y, "-.", color='r', label=label)
                #
                ax42.legend(loc='upper right')
                ax42.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax42.vlines(lambdaEventos4, 0, lambdaEventos4, colors=color_Tipo4, lw=5, alpha=0.5)

            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos4))+") y alarmas ("+str(len(lambdaAlarmas4))+")"
            ax42.title.set_text(titulo)
            ax42.set_ylabel('PDF')
            ax42.set_xlabel('tiempo')


###
    elif (tipodisp == TiposDispositivos.TIPO5):
        ## Tipo 5
        if 5 in dispositivos:

            c5, b5, _ = ax51.hist(dispTipo5,color=color_Tipo5, label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax51.vlines(alarmasTipo5, 0, max(c5), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax51.legend(loc='upper right')
            fig5.canvas.set_window_title(TiposDispositivos.TIPO5)
            titulo = "Histograma de eventos en el tiempo"
            ax51.title.set_text(titulo)
            ax51.set_ylabel('Eventos')
            ax51.set_xlabel('Tiempo')
            ax51.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos5 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO5)
            lambdaAlarmas5 = []
            if (periodico_Tipo5 == 0):
                count5, bins5, _ = ax52.hist(lambdaEventos5,color=color_Tipo5, label='histograma eventos (normalizado)', density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins5), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo5)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo5)
                ax52.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas5 = graficarlambdaalarmas(alarmasTipo5)
                cnt5, bin5, _ = ax52.hist(lambdaAlarmas5, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin5), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo5)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo5)
                ax52.plot(x, y, "-.", color='r', label=label)
                #
                ax52.legend(loc='upper right')
                ax52.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax52.vlines(lambdaEventos5, 0, lambdaEventos5, colors=color_Tipo5, lw=5, alpha=0.5)

            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos5))+") y alarmas ("+str(len(lambdaAlarmas5))+")"
            ax52.title.set_text(titulo)
            ax52.set_ylabel('PDF')
            ax52.set_xlabel('tiempo')


###
    elif (tipodisp == TiposDispositivos.TIPO6):
        ## Tipo 6
        if 6 in dispositivos:

            c6, b6, _ = ax61.hist(dispTipo6, color=color_Tipo6,label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax61.vlines(alarmasTipo6, 0, max(c6), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax61.legend(loc='upper right')
            fig6.canvas.set_window_title(TiposDispositivos.TIPO6)
            titulo = "Histograma de eventos en el tiempo"
            ax61.title.set_text(titulo)
            ax61.set_ylabel('Eventos')
            ax61.set_xlabel('Tiempo')
            ax61.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos6 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO6)
            lambdaAlarmas6 = []
            if (periodico_Tipo6 == 0):
                count6, bins6, _ = ax62.hist(lambdaEventos6,color=color_Tipo6, label='histograma eventos (normalizado)', density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins6), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo6)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo6)
                ax62.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas6 = graficarlambdaalarmas(alarmasTipo6)
                cnt6, bin6, _ = ax62.hist(lambdaAlarmas6, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin6), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo6)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo6)
                ax62.plot(x, y, "-.", color='r', label=label)
                #
                ax62.legend(loc='upper right')
                ax62.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax62.vlines(lambdaEventos6, 0, lambdaEventos6, colors=color_Tipo6, lw=5, alpha=0.5)

            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos6))+") y alarmas ("+str(len(lambdaAlarmas6))+")"
            ax62.title.set_text(titulo)
            ax62.set_ylabel('PDF')
            ax62.set_xlabel('tiempo')


###
    else:
        ## Tipo 7
        if 7 in dispositivos:

            c7, b7, _ = ax71.hist(dispTipo7,color=color_Tipo7, label='paquetes', density=False, range=(0, tiempofinal), bins=bins + 1)
            ax71.vlines(alarmasTipo7, 0, max(c7), label='alarmas', colors='r', lw=2, alpha=0.2)
            ax71.legend(loc='upper right')
            fig7.canvas.set_window_title(TiposDispositivos.TIPO7)
            titulo = "Histograma de eventos en el tiempo"
            ax71.title.set_text(titulo)
            ax71.set_ylabel('Eventos')
            ax71.set_xlabel('Tiempo')
            ax71.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)

            lambdaEventos7 = graficarlambdaeventos(ListaEventos, TiposDispositivos.TIPO7)
            lambdaAlarmas7 = []
            if (periodico_Tipo7 == 0):
                count7, bins7, _ = ax72.hist(lambdaEventos7,color=color_Tipo7, label='histograma eventos (normalizado)', density=True, bins=30, alpha=0.4)
                x = np.linspace(0, max(bins7), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaEventos_Tipo7)
                label = 'expon lambda eventos= ' + str(tasaEventos_Tipo7)
                ax72.plot(x, y, "--", color='k', label=label)
                #
                lambdaAlarmas7 = graficarlambdaalarmas(alarmasTipo7)
                cnt7, bin7, _ = ax72.hist(lambdaAlarmas7, color='grey', label='histograma alarmas (normalizado)',
                                          density=True, bins=10, alpha=0.4)
                x = np.linspace(0, max(bin7), 500)
                # Varying positional arguments
                y = expon.pdf(x, 0, 1 / tasaAlarmas_Tipo7)
                label = 'expon lambda alarmas= ' + str(tasaAlarmas_Tipo7)
                ax72.plot(x, y, "-.", color='r', label=label)
                #
                ax72.legend(loc='upper right')
                ax72.grid(b=True, color='grey', alpha=0.3, linestyle='-.', linewidth=1)
            else:
                ax72.vlines(lambdaEventos7, 0, lambdaEventos7, colors=color_Tipo7, lw=5, alpha=0.5)

            titulo = "Tiempo entre eventos ("+str(len(lambdaEventos7))+") y alarmas ("+str(len(lambdaAlarmas7))+")"
            ax72.title.set_text(titulo)
            ax72.set_ylabel('PDF')
            ax72.set_xlabel('tiempo')



def graficarlambdaeventos(ListaEventos,tipoDispositivo):

        Eventos = copy.deepcopy(ListaEventos)
        Eventosaux = copy.deepcopy(ListaEventos)

        diferencias=[]
        for evento in Eventos:
            if evento in Eventosaux:
                if evento[0] == 0 and evento[3]==tipoDispositivo: # si se trata de un evento del tipo dado
                    if evento[6]==0: # si no se trata de un evento periodico
                        diferencias.append(evento[2])
                    eventoActual=evento
                    Eventosaux.remove(evento)
                    for eventoaux in Eventos: # se recorre la lista ahora sin el primer evento
                        if eventoaux in Eventosaux:
                            # si se trata de un evento normal, y tienen el mismo id y son del mismo tipo se calcula su diferencia
                            if eventoaux[1]!=eventoActual[1] and eventoaux[0]==0 and eventoaux[2]==eventoActual[2] and eventoActual[3]==tipoDispositivo :
                                diferencias.append(eventoaux[1]-eventoActual[1])
                                eventoActual = eventoaux
                                Eventosaux.remove(eventoaux)

                else:
                    Eventosaux.remove(evento)



        return diferencias

def graficarlambdaalarmas(ListaAlarmasTipox):

    tiempoactual=0
    diferencias=[]
    for tiempo in ListaAlarmasTipox:
        diferencias.append(tiempo-tiempoactual)
        tiempoactual=tiempo

    return diferencias
