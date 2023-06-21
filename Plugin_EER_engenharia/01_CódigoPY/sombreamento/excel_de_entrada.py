import os
import pandas 
from qgis.core import *
from qgis.PyQt.QtCore import QVariant
import processing
from PyQt5.QtWidgets import *

(answer,bool) = QInputDialog().getText(None, "Digite onde esta a Planilhas de Entrada","caminho da pasta")
path=answer

registry = QgsProject.instance()
def retorna_lista_entrada(path,aba,coluna):
    excel_data_df = pandas.read_excel(path, sheet_name=aba,header=1)
    #print(excel_data_df)
    excel_data_df.filter(like='East')
    excel_data_df.filter(like='North')
    excel_data_df.filter(like='Aero')
    lista=(excel_data_df[coluna].dropna().tolist())
    return lista
def covert_string(lista):
    temp=[]
    for i in range(len(lista)):
        temp2=str(lista[i]).replace(',', '.')
        temp.append(temp2)
    return temp

def le_arquivo_excel(path,nome_planilha,aba,coluna):
    lista_entrada=[]
    dirs = os.listdir(path)
    for file in dirs:
            if file.endswith(".xlsx"):
                #print(file)
                if file == nome_planilha+str('.xlsx'):
                    diretorioParques1 = os.path.join(path, file)
                    #print(diretorioParques1)
                    lista_entrada=retorna_lista_entrada(str(diretorioParques1),aba,coluna)
    return lista_entrada
def adiciona_atributos(layer,campo_atributo,lista):
    with edit(layer):
    # use enumerate to iterate the features
        for i,feature in enumerate(list(layer.getFeatures())):
            feature.setAttribute(campo_atributo,lista[i])
            layer.updateFeature(feature)
def main_excel(path,num_parque):
    if(num_parque==0):
        E='East'
        N='North'
        Aero='Aeros'
    else:
        E='East.'+str(num_parque)
        N='North.'+str(num_parque)
        Aero='Aeros.'+str(num_parque)
    pontos_E=le_arquivo_excel(path, 'Planilha de entrada','Coordenadas',E)
    pontos_N=le_arquivo_excel(path, 'Planilha de entrada','Coordenadas',N)
    nome=str(le_arquivo_excel(path, 'Planilha de entrada','Inputs','Nome')[num_parque])
    epsg = 32724
    featureList=[]
    featureList=[QgsPoint(pontos_E[i],pontos_N[i]) for i in range(len(pontos_E))]
    
    # Create layer with result
    uri = "Point?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

    mem_layer = QgsVectorLayer(uri,
                               str(nome),
                               'memory')
    prov = mem_layer.dataProvider()

    feats = [ QgsFeature() for i in range(len(featureList)) ]

    for i, feat in enumerate(feats):
        feat.setAttributes([i])
        feat.setGeometry(featureList[i])
    prov.addFeatures(feats)
    ##################adicionando atributos ao layer#################
    nome_aeros=le_arquivo_excel(path, 'Planilha de entrada','Coordenadas',Aero)
    prov.addAttributes([QgsField("Aeros", QVariant.String),
                  QgsField("Coordenada E (m)",  QVariant.Double),
                  QgsField("Coordenada N (m)", QVariant.Double)])#nomeia campo de atributos
    mem_layer.updateFields()
    adiciona_atributos(mem_layer,'Aeros',nome_aeros)
    adiciona_atributos(mem_layer,'Coordenada E (m)',pontos_E)
    adiciona_atributos(mem_layer,'Coordenada N (m)',pontos_N)

    registry.addMapLayer(mem_layer)
    
    return nome
def main_input(path,num_parque):
    ang_init=le_arquivo_excel(path, 'Planilha de entrada','Inputs','Angulo inicial')[num_parque]
    ang_end=le_arquivo_excel(path, 'Planilha de entrada','Inputs','Angulo final')[num_parque]
    poligono=le_arquivo_excel(path, 'Planilha de entrada','Inputs','Poligono')[num_parque]
    zone_letter=le_arquivo_excel(path, 'Planilha de entrada','Inputs','Zone Letter')[num_parque]
    Zone=int(le_arquivo_excel(path, 'Planilha de entrada','Inputs','Zone')[num_parque])
    Hemisphere=le_arquivo_excel(path, 'Planilha de entrada','Inputs','Hemisphere')[num_parque]
    HH=int(le_arquivo_excel(path, 'Planilha de entrada','Inputs','HH')[num_parque])
    D=int(le_arquivo_excel(path, 'Planilha de entrada','Inputs','Diametro da pa')[num_parque])
    return Zone,Hemisphere,HH,D,ang_init,ang_end,poligono,zone_letter

def main_num_parques(path):
    return le_arquivo_excel(path, 'Planilha de entrada','Inputs','Numero de parques')[0]
