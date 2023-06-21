import sys
import os
import shapefile
import pandas as pd

def ordena_lista(x,y):
    # ordene os índices em vez dos elementos em si
    indices = list(range(len(x)))
    indices.sort(key=lambda i: x[i]) # ordene os índices com relação ao seu respectivo valor em x

    # crie as listas baseado na ordem dos índices
    new_x = [x[i] for i in indices]
    new_y = [y[i] for i in indices]
    return new_x,new_y
def coordenadas(diretorio,file_atual):
        sf = shapefile.Reader(file_atual[1])
        pol = sf.shapes()
        #le as coordenadas do shapefile e coloca em uma lista
        data = []
        prop=[]
        pontos=[]
        for s in range(len(pol)):
            #data_pol = [sf.record(s)['area_code'], pol[s].points
            prop.append(sf.record(s)['area_code'])
            pontos.append(pol[s].points)
        (new_prop,new_pontos)=ordena_lista(prop,pontos)
        for i in range (len(new_prop)):
            data.append([new_prop[i],new_pontos[i]])
        return data
