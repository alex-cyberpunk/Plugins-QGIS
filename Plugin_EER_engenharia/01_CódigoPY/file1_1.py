import pandas 
import os
from qgis.PyQt.QtCore import QVariant
from qgis.core import *
import numpy as np
from PyQt5.QtWidgets import *

registry = QgsProject.instance()
def le_excel(path,aba):
    listX=[]
    listY=[]
    validador_EOL=False
    wb = pandas.ExcelFile(path)
    if aba in wb.sheet_names:
        excel_data_df = pandas.read_excel(path, sheet_name=aba,header=5)
        if 'Coordenada E (m)' in excel_data_df.columns:
            listX=excel_data_df['Coordenada E (m)'].tolist()
            validador_EOL=True
        if 'Coordenada N (m)' in excel_data_df.columns:
            listY=excel_data_df['Coordenada N (m)'].tolist()
            validador_EOL=True
    return(listX,listY,validador_EOL)
def transforma_pontos_em_layer(listX,listY,nome,aba,EPSG):
    # Specify the geometry type
    if (aba=='Linha de Transmissão'):layer = QgsVectorLayer('Linestring?crs=epsg:'+ str(EPSG), str(nome)+'_'+str(aba) , 'memory')
    else:layer = QgsVectorLayer('Polygon?crs=epsg:'+ str(EPSG), str(nome)+'_'+str(aba) , 'memory')
    # Set the provider to accept the data source
    prov = layer.dataProvider()
    points=[]
    indice=[]
    for i in range(len(listX)):
        points.append(QgsPointXY(listX[i],listY[i]))
    for i in range(len(listX)):
        indice.append(i)
    #points = [QgsPointXY(100,100), QgsPointXY(100,200), QgsPointXY(200,200), QgsPointXY(200,100)]
    # Add a new feature and assign the geometry
    feat = QgsFeature()
    if (aba=='Linha de Transmissão'):
        #feat = QgsFeature(layer.fields()) 
        feat.setGeometry(QgsGeometry.fromPolylineXY(points))
    else:
        #feat.setAttributes([atributos])
        feat.setGeometry(QgsGeometry.fromPolygonXY([points]))
    prov.addFeatures([feat])
    prov.addAttributes([QgsField("index", QVariant.Int),
                  QgsField("Coordenada E (m)",  QVariant.Double),
                  QgsField("Coordenada N (m)", QVariant.Double)])#nomeia campo de atributos
    layer.updateFields()#atualiza campo de atributos
    #print(feat)
    feats = [ QgsFeature() for i in range(len(listX)) ]
    #print(listX)
    #res = layer.dataProvider().deleteFeatures(dfeats)
    #layer.triggerRepaint()
    feats = [ QgsFeature() for i in range(len(listX)) ]
    for i, feat in enumerate(feats):
            #feat.deleteFeature()
            #print(i)
            feat.setAttributes([indice[i],listX[i],listY[i]])
            prov.addFeatures([feat])
    # Update extent of the layer
    layer.updateExtents()
    # Add the layer to the Layers panel
    registry.addMapLayer(layer)
#(listX,listY)=le_excel(path)
#transforma_pontos_em_layer(listX,listY)
#caps = layer.dataProvider().capabilities()
def main():
    print("Programa Validador EOL para Excel")
    (answer,bool) = QInputDialog().getText(None, "Digite onde esta as planilhas do validador EOL","caminho da pasta")
    path=answer
    (answer,bool) = QInputDialog().getText(None, "Escolha o epsg SIRGAS 2000 digitando:", " :(1) 24S  \n (2) 23 S")
    if int(answer)==1: 
        EPSG=31984
        print("o epsg usado é SIRGAS 2000/UTM 24S")
    elif int(answer)==2:
        EPSG=31983
        print("o epsg usado é SIRGAS 2000/UTM 23S")
    (answer1,bool) = QInputDialog().getText(None, "Entre com a aba desejada","aba:\n (1)Parque Eólico \n (2)Subestação',\n (3)Linha de Transmissão")
    if int(answer1)==1: 
        aba='Parque Eólico'
    elif int(answer1)==2:
        aba='Subestação'
    elif int(answer1)==3:
        aba='Linha de Transmissão'
    print("a opção "+str(aba) + " foi escolhida")

    dirs = os.listdir( path )
    # Ele puxa as planilhas só da pasta (ignorando subpastas)
    #caso queira puxar validador EOL de várias pastas , basta usar outros códigos 
    print("Planilhas carregadas:")
    print()
    for file in dirs:
            if file.endswith(".xlsx"):
                    diretorioParques1 = os.path.join(path, file)
                    (listX,listY,validador_EOL)=le_excel(str(diretorioParques1),aba)
                    basename = os.path.basename(str(diretorioParques1))
                    file_name = os.path.splitext(basename)[0]
                    print(file_name)
                    if validador_EOL == True:
                        transforma_pontos_em_layer(listX,listY,file_name,aba,EPSG)
                    else: print("não é uma planilha de validador EOL")
                    print()

