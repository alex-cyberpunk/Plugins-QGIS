import pandas as pd
from qgis.core import *
from PyQt5.QtWidgets import *
registry = QgsProject.instance()
(answer,bool) = QInputDialog().getText(None, "Digite onde deseja salvar os pontos dos Vertices","caminho da pasta")
path=answer
print("Programa Qgis para Excel")
def Salvar_no_excel(pontosX,pontosY,pontosX_linha,pontosY_linha,nome):
    name='\ ' +str(nome)
    d={'x': pontosX,'y': pontosY}
    d_LT={'x': pontosX_linha,'y': pontosY_linha}
    dados =pd.DataFrame(data=d)
    dados1 =pd.DataFrame(data=d_LT)
    index_temp=[]
    index_temp_LT=[]
    count=0
    for i in range(len(pontosX)):
        if (pontosX[i]== ' '):
            index_temp.append(' ')
            count=-1
        else: 
            count=count+1
            index_temp.append(count) #faz index começar com 1
    dados.index=index_temp
    for i in range(len(pontosX_linha)):
        if (pontosX_linha[i]== ' '):
            index_temp_LT.append(' ')
            count=-1
        else: 
            count=count+1
            index_temp_LT.append(count) #faz index começar com 1
    dados1.index=index_temp_LT
    with pd.ExcelWriter(str(path) +str(name)+'.xls') as writer:  # doctest: +SKIP
        dados.to_excel(writer,index=True, sheet_name='Parques_e_Subestações')
        dados1.to_excel(writer, sheet_name='LT')
def leitor_de_layer():
    layers_names = []
    layer1=[]
    for layer in QgsProject.instance().mapLayers().values():
        layers_names.append(layer.name())
    for i in range(len(layers_names)):
        name=layers_names[i]
        layer1.append(registry.mapLayersByName( name )[0])
    return(layers_names,layer1)
def leitor_de_parques(layers_names,layer_principal):
    layer_parques=[]
    layer_names_parques=[]
    layer_LT=[]
    layer_names_LT=[]
    for i in range(len(layer_principal)):
        for feat in layer_principal[i].getFeatures():
            geom = feat.geometry()
            if geom.type() == QgsWkbTypes.PolygonGeometry:
                layer_parques.append(layer_principal[i])
                layer_names_parques.append(layers_names[i])
            elif geom.type() == QgsWkbTypes.LineGeometry:
                layer_LT.append(layer_principal[i])
                layer_names_LT.append(layers_names[i])
    return(layer_parques,layer_names_parques,layer_LT,layer_names_LT)
def main():
    (layers_names,layer_principal)=leitor_de_layer()
    (layer_parques,layer_names_parques,layer_LT,layer_names_LT)=leitor_de_parques(layers_names,layer_principal)
    pontosX=[]
    pontosY=[]
    pontosX.append(' ')
    pontosY.append(' ')
    pontosX_LT=[]
    pontosY_LT=[]
    pontosX_LT.append(' ')
    pontosY_LT.append(' ')
    print("parques cuja coordenadas foram salvas")
    for i in range (len(layer_parques)): 
        pontosX.append(layer_names_parques[i])
        print(layer_names_parques[i])
        pontosY.append(layer_names_parques[i])
        for feat in layer_parques[i].getFeatures():
            #print(layer_parques)
            geom = feat.geometry()
            for part in geom.parts():
                    for v in part.vertices():
                        pontosX.append(v.x())#pontos X
                        pontosY.append(v.y())#ponto Y
        pontosX.append(' ')
        pontosY.append(' ')
    for i in range (len(layer_LT)): 
        for feature in layer_LT[i].getFeatures():
            for part in feature.geometry().parts():
                pontosX_LT.append(layer_names_LT[i])
                pontosY_LT.append(layer_names_LT[i])
                for pnt in part:
                    pontosX_LT.append(pnt.x())
                    pontosY_LT.append(pnt.y())
            pontosX_LT.append(' ')
            pontosY_LT.append(' ')
    Salvar_no_excel(pontosX,pontosY,pontosX_LT,pontosY_LT,'coordenadas')
main()
        