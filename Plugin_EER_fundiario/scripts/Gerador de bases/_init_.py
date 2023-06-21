#inicia todos os codigos
import os
import sys
from PyQt5.QtWidgets import *

#importa todos os arquivos .py para execucao da rotina
from Salva_shp import cria_shp,deleteShapefile
from Coordenadas import coordenadas
from Checa_informacoes import info
from Bases import cria_kmz

def main(diretorio_GPD,diretorio_kmz,Lyr):
   
   #cria um shapefile com o layer escolhido e salva no mesmo lugar onde esta o .kmz
    saida_shp=cria_shp(diretorio_kmz,Lyr)
    
    #faz lista com os arquivos shapefiles existentes
    file_list = []
    for file in os.listdir(diretorio_kmz):
        if file.endswith(".shp"):
            file_list.append([file[0:3],os.path.join(diretorio_kmz,file)])
    #separa os caminhos do excel gpd e onde salvar o kmz
    path_gpd=diretorio_GPD
    path_kmz=diretorio_kmz+'\ '
    
    print(file_list)
    #loop para cada arquivo .shp da lista
    for n in range(len(file_list)):
        #leitura do arquivo shapefile e de seus shapes
        dados=coordenadas(diretorio_kmz,file_list[n])
        #para varios layers , descomente abaixo
        #caminho= os.path.join(os.path.realpath(path_gpd), file_list[n][0]+'.xlsm')
        
        caminho= os.path.realpath(path_gpd)
        #coleta as informacoes da planilha GPD
        df=info(dados,caminho)
        #cria o kmz
        cria_kmz(df,file_list[n],path_kmz)
        #deleta os arquivos shapefile criados apartir do layer escolhido
        theDir, theFile = os.path.split(saida_shp)
        #deleteShapefile(theDir, theFile)
        #mensagem de sucesso
        msg = QMessageBox()
        msg.setText("O arquivo .kmz foi criado.")
        msg.exec()
