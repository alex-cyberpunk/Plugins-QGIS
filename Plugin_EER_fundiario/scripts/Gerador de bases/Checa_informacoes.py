
import pandas
import os
import time
import xlrd


def le_excel(path,aba,header_init,lista_colunas):
            '''
            Entradas:
            path: caminho do arquivo excel
            aba: nome da aba do excel
            header_init: linha do cabeçalho
            lista_colunas: lista de colunas que deseja ler
            
            Saidas:
            matriz: matriz com os dados do excel
            '''
            #como as planilhas GPD sao protegidas por senha , a leitura da mesma e feita num dataframe so
            matriz=[]
            Excel_desejado=False
            wb = pandas.ExcelFile(path)
            #filtra a aba do excel
            if aba in wb.sheet_names:
                df = pandas.read_excel(path, sheet_name=None)
                #filtra as colunas desejadas
                for i in range(len(lista_colunas)):
                    if lista_colunas[i] in df[aba].columns:
                        matriz.append(df[aba][lista_colunas[i]].tolist())
                        print(df[aba][lista_colunas[i]])
                    else:print(lista_colunas[i])
            
            return(matriz)
def release_list(a):
   del a[:]
   del a

def info(data,path_gpd):
    Heading =["Proprietário principal","Imóvel","Matrícula", "Contrato", "Área (ha) - matrícula", "Possui topografia?",
              "Sujeita a distrato?", "Distratada?", "Contratada por concorrente?", "Concorrente Contratante",
              "Situação do imóvel jan/23","Situação do imóvel fev/23", "Situação do imóvel mar/23", "Situação do imóvel abr/23",
              "Situação do imóvel mai/23","Situação do imóvel jun/23", "Situação do imóvel jul/23", "Situação do imóvel ago/23",
              "Situação do imóvel set/23","Situação do imóvel out/23", "Situação do imóvel nov/23", "Situação do imóvel dez/23"]
    (matriz)=le_excel(path_gpd,'Áreas',0,Heading)#use o nome escrito na aba do excel
    prop=[data [i][0] for i in range(len(data)) ]
    coord=[data [i][1] for i in range(len(data)) ]
    release_list(data)
    matriz_final=[prop,coord]#props relacionadas com as coordenadas do shape
    (lista_propriedades_GPD)=le_excel(path_gpd,'Áreas',0,["AREA_CODE"])#lista props do excel
    for j in range(len(matriz)):matriz_final.append([])
    #print(prop)
    for i in range(len(prop)):
        index = lista_propriedades_GPD[0].index(prop[i]) #index da prop na lista de propriedades do GPD
        for j in range(len(matriz)):
            matriz_final[j+2].append(matriz[j][index])

    
    '''
    #Agora retira-se um '0' do codigo para ficar igual ao codigo do sistema fundiario
    for i in range(len(matriz_final[0])):
        if (int(matriz_final[0][i].split('-')[2])<1000):
            matriz_final[0][i]=matriz_final[0][i].replace('0','',1)

    '''
    
    Heading.insert(0, "Coordenadas")
    Heading.insert(0, "# Área")
    #print(Heading) 
    df = pandas.DataFrame (matriz_final).transpose()
    df.columns = Heading
    
    print(df)
    return df




