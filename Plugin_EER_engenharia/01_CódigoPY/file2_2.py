import qgis
from qgis.core import *
import processing
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import QVariant
'''
bibliotecas do python
'''
import os
import io
import osr
from pathlib import Path
#######################################
#mudar a variavel pasta para a pasta desejeda onde ira procurar os shapes
##################################################
def main():
    (answer,bool) = QInputDialog().getText(None, "Digite onde esta os shapefiles","caminho da pasta")
    pasta=answer
    #str(input('digite o caminho da pasta dos shapefiles desejados :'))
    #print("digite os filtro separados por ,")
    bool=True
    filtro=[]
    while bool==True:
        (answer,bool) = QInputDialog().getText(None, "Digite as letras iniciais do arquivo","\n Quando já tiver digitado todas as iniciais clique em cancel")
        if bool==True : filtro.append(answer)
    ##############################################
    quantidade = 0
    camadaParques = []
    nome_dos_arquivos=[]
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.endswith(".shp"):
                for j in range(len(filtro)):
                            if arquivo.startswith(filtro[j]):
                                diretorioParques = os.path.join(diretorio, arquivo)
                                camadaParques.append(QgsVectorLayer(diretorioParques,str(Path(diretorioParques).stem),"ogr"))
                                if camadaParques[quantidade].isValid():
                                    print("Camada vetorial Carregada com sucesso")
                                    # iface.addVectorLayer(diretorioParques,'Parques','ogr')
                                    QgsProject.instance().addMapLayer(camadaParques[quantidade])
                                else:
                                    print ('Impossível carregar camada vetorial , favor verificar problemas')
                                quantidade=quantidade+1
