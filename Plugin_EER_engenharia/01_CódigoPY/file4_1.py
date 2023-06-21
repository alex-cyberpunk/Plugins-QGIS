from qgis.core import *
from qgis.utils import iface
import sys
import processing
from math import *
from PyQt5.QtWidgets import *
import os

#to get the current working directory
#import os
#f = open('file.txt')
#os.path.realpath(f.name)
(answer,bool) = QInputDialog().getText(None, "Digite onde esta as planilhas de Entrada","caminho da pasta")
path=answer
#Path = r"C:\Users\alex.matias\PEC Energia\Engenharia - Planejamento\Sharepoint 2022\ESTRUTURA\05_Base de Dados\GIS\01_CódigoPY"
#Path=os.getcwd()
#path = Path + str("\sombreamento")
sys.path.append(path)
from convert_utm_dd import to_latlon

#path_le_excel = Path + str("\sombreamento")
sys.path.append(path)
#print(path_le_excel)
from excel_de_entrada import main_num_parques
from excel_de_entrada import main_input


####constantes usadas#########
Raio_da_Terra = 6372.795477598
Rad_conv = pi / 180
registry = QgsProject.instance()
##############################


def inicia(N_parques):
    """
    inicia os parametros
    """
    ################entrada de pontos ou do excel#################
    (answer, bool) = QInputDialog().getText(
        None, "Existe um layer de pontos?", "escolha opção (1) existe (2) n existe"
    )
    if answer == "1":
        existe_layer_pontos = "existe"
        (answer1, bool) = QInputDialog().getText(None, "Digite o nome da camada", " ")
        # nome_layout=answer
    if answer == "2":
        existe_layer_pontos = "n existe"
    #############################################################
    registry = QgsProject.instance()
    # inicia a leitura do excel
    (
        Zone,
        Hemisphere,
        HH,
        D,
        angulo_inicial_graus,
        angulo_final_graus,
        poligono,
        letter,
    ) = main_input(path,N_parques)
    Raio_pa = D / 2
    raio = 20 * (Raio_pa + HH) / 1000
    # usa pontos da planilha ou de um layer existente
    if existe_layer_pontos == "existe":
        nome_layout = answer1
        layout=retornar_layer(answer1)
        EPSG = layout.crs().postgisSrid()
        if EPSG == 31984:
            Zone = 24
            letter = "L"
        if EPSG == 31983:
            Zone = 23
            letter = "L"
    else:
        sys.path.append(path)
        from excel_de_entrada import main_excel
        nome = main_excel(path,N_parques)
        nome_layout = nome
        if int(Zone) == 24:
            EPSG = 31984
        if int(Zone) == 23:
            EPSG = 31983
    # da a opção de interferência ou incidencia
    if poligono == "Interferência":
        adiciona = 180
    else:
        adiciona = 0

    angulo_interferencia_inicial = angulo_inicial_graus + adiciona
    angulo_interferencia_final = angulo_final_graus + adiciona

    angulo_inicial = angulo_interferencia_inicial * Rad_conv
    angulo_final = angulo_interferencia_final * Rad_conv
    return nome_layout, angulo_inicial, angulo_final, raio, EPSG, letter, Zone


def rename_layer(nome_layer, novo_nome_layer):
    """
    renomeia um layer
    """
    registry = QgsProject.instance()
    layer = registry.mapLayersByName(nome_layer)[0]
    layer.setName(novo_nome_layer)


def reprojet_layer(nome, EPSG):
    """
    essa função reprojeta um layer de um SRC para outro
    Entradas:
    nome: nome do layer a se reprojetar
    EPSG: SRC de destino
    """
    layer = registry.mapLayersByName(nome)[0]
    parameter = {
        "INPUT": layer,
        "TARGET_CRS": "EPSG:" + str(EPSG),
        "OUTPUT": "memory:" + str(nome) + "_Reprojected",
    }
    result = processing.run("native:reprojectlayer", parameter)
    QgsProject.instance().addMapLayer(result["OUTPUT"])


def union_polygon(layer1, layer2, tipo, epsg, nome_union):
    """
    essa função une dois layers
    Entradas:
    layer1 e layer 2: os dois layer que deseja unir
    tipo : se é do tipo poligono e linha
    nome_union: nome do layer a ser criado
    """
    featureList = []
    # une os features dos dois layers num vetor
    for i in layer1.getFeatures():
        for p in layer2.getFeatures():
            union_1 = i.geometry().combine(p.geometry())
            featureList.append(union_1)
    # cria um memory layer de um tipo ou outro
    if tipo == "linha":
        layer_union = QgsVectorLayer(
            "Linestring?crs=epsg:" + str(epsg), str(nome_union), "memory"
        )
    if tipo == "poligono":
        uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer" "&index=yes"
        layer_union = QgsVectorLayer(uri, str(nome_union), "memory")
    prov = layer_union.dataProvider()
    # adiciona os features unidos ao memory layer
    feats = [QgsFeature() for i in range(len(featureList))]
    for i, feat in enumerate(feats):
        feat.setAttributes([i])
        feat.setGeometry(featureList[i])
    prov.addFeatures(feats)
    registry.addMapLayer(layer_union)
    return layer_union


def remove_layer(lyrname):
    """
    essa função remove layers do qgis pelo nome do layer
    """
    qinst = QgsProject.instance()
    qinst.removeMapLayer(qinst.mapLayersByName(lyrname)[0].id())

def retornar_layer(nome):
    '''
    retorna o layer pelo nome
    '''
    registry = QgsProject.instance()
    return registry.mapLayersByName( nome )[0]

def calcula_lat_long(lonA, latA, theta, d):
    """
    Calculo da latitude e longitude considerando deslocamento num plano curvo terrestre
    Entradas :
    lonA:longitude atual
    latA: latitude atual
    theta: angulo deslocado
    d: distância deslocada
    """
    latB = (
        asin(
            sin(latA * Rad_conv) * cos(d / Raio_da_Terra)
            + cos(latA * Rad_conv) * sin(d / Raio_da_Terra) * cos(theta)
        )
        * 180
        / pi
    )
    lonB = (
        lonA
        + atan2(
            sin(theta) * sin(d / Raio_da_Terra) * cos(latA * Rad_conv),
            cos(d / Raio_da_Terra) - sin(latA * Rad_conv) * sin(latB * Rad_conv),
        )
        * 180
        / pi
    )
    return (lonB, latB)


def cria_arcos(
    pontoX_centro,
    pontoY_centro,
    angulo_ponto_inicial,
    angulo_ponto_final,
    d,
    epsg,
    EPSG,
):
    """
    essa função cria um arcos no qgis em um ponto central , tendo como entradas:
    pontoX_centro: coordenada X (abscissas) da coordenada
    pontoY_centro:coordenada Y (ordenadas) da coordenada
    angulo_ponto_inicial(rad): ponto em que se inicial o arco
    angulo_ponto_final(rad): ponto em que se finaliza o arco
    d(unidades do mapa): raio do arco
    epsg: referentes ao decimal degrees , é 4672 porém é bom deixar como variavel n
    EPSG: SRC(sistemas de referencias de coordenadas) desejado

    O processo da função se da em 3 etapas :
    1-criação do curva
    2-criação das arestas do arco (duas arestas)
    3-união
    4-poligonize

    """
    """
    1)Processo de criação de curvas no Qgis:
    O qgis usa três pontos de referência para contruir um curva
    dseta forma se garantirmos que os 3 pontos pertencem a mesma circuferência , então pode-se
    criar o arco de um circuferência , a maneira mais fácil de se obter isso é com dois pontos de circuferência 
    e um ponto médio entre eles , fonte:
    https://webgeodatavore.com/create-qgis-curve-from-python-api.html
    """
    # Conversão do pontos X e Y para decimal degrees
    # Calculado apartir de uma coordenada (X_centro,Y_centro) é obtido 3 pontos : um no angulo inicial , outro no angulo final e o último no angulo médio entre eles
    (pointX1, pointY1) = calcula_lat_long(
        pontoX_centro, pontoY_centro, angulo_ponto_inicial, d
    )
    (pointX3, pointY3) = calcula_lat_long(
        pontoX_centro, pontoY_centro, angulo_ponto_final, d
    )
    angulo = (angulo_ponto_final - angulo_ponto_inicial) / 2 + angulo_ponto_inicial
    (pointX2, pointY2) = calcula_lat_long(pontoX_centro, pontoY_centro, angulo, d)
    # cria-se a variavel de circulo qgis
    circularRing = QgsCircularString()
    # Setar primeiro ponto, ponto intermediario para a  curvatura e o ponto final
    circularRing.setPoints(
        [
            QgsPoint(pointX1, pointY1),
            QgsPoint(pointX2, pointY2),
            QgsPoint(pointX3, pointY3),
        ]
    )
    # Checa se a geometria tem curvas
    print(circularRing.hasCurvedSegments())
    # Cria geometria usando instancias do QgsCircularStringV2
    geom_from_curve = QgsGeometry(circularRing)
    # Cria um feature
    fet = QgsFeature()
    # Assign the geometry
    fet.setGeometry(geom_from_curve)
    # Cria um memory layer de pontos
    layer = QgsVectorLayer(
        "Linestring?crs=epsg:" + str(epsg), "temporary_points", "memory"
    )
    # Adiciona o layer
    QgsProject.instance().addMapLayer(layer)
    # Adiciona to feature para o  layer provider
    pr = layer.dataProvider()
    pr.addFeatures([fet])
    # Update extent
    layer.updateExtents()
    feat = QgsFeature()

    # 2)criação das arestas do arco
    listX = [pointX1, pontoX_centro, pointX3]
    listY = [pointY1, pontoY_centro, pointY3]
    points = []
    # Cria um memory layer de linhas
    layer_triangulo = QgsVectorLayer(
        "Linestring?crs=epsg:" + str(epsg), "nome", "memory"
    )
    prov = layer_triangulo.dataProvider()
    # adiciona-se os pontos as duas linhas criadas
    for i in range(len(listX)):
        points.append(QgsPointXY(listX[i], listY[i]))
    feat.setGeometry(QgsGeometry.fromPolylineXY(points))
    prov.addFeatures([feat])
    # adiciona-se ao qgis
    QgsProject.instance().addMapLayer(layer_triangulo)
    # 3) união das duas linhas com a curva criando-se o perimetro do arco
    layer_union = union_polygon(layer, layer_triangulo, "linha", epsg, "UNIAO")
    # 4) processo de poligonoze(transformar em poligono) do perimetro criado
    result = processing.run(
        "qgis:linestopolygons",
        {
            "INPUT": layer_union,
            "BAND": 1,
            "FIELD": "DN",
            "EIGHT_CONNECTEDNESS": False,
            "OUTPUT": "memory:",
        },
    )["OUTPUT"]
    QgsProject.instance().addMapLayer(result)

    # reprojeta o arco criado em UTM
    reprojet_layer("output", EPSG)
    # remoção de todos os itens exceto o arco
    remove_layer("UNIAO")
    remove_layer("nome")
    remove_layer("output")
    remove_layer("temporary_points")


def le_pontos(nome1, angulo_inicial, angulo_final, raio, EPSG, letter, zona):
    """
    le os pontos de um layer, converte em decimal degrees e cria os arcos no SRC dado
    entradas:
    angulo_ponto_inicial(rad): ponto em que se inicial o arco
    angulo_ponto_final(rad): ponto em que se finaliza o arco
    raio(unidades do mapa): raio do arco
    letter: letra do SRC
    zona: zona do SRC
    EPSG : SRC
    """
    registry = QgsProject.instance()
    layerPoints = registry.mapLayersByName(nome1)[0]
    epsg = layerPoints.crs().postgisSrid()
    for item in layerPoints.getFeatures():
        geometry = item.geometry()
        # pega as geometria do pontos
        geo = QgsGeometry.asPoint(item.geometry())
        pxy = QgsPointXY(geo)
        # convert as coordenadas x e y para latitude e longitude decimal degrees
        lat, lon = to_latlon(pxy.x(), pxy.y(), int(zona), letter)
        # cria arcos
        cria_arcos(lon, lat, angulo_inicial, angulo_final, raio, 4674, EPSG)


def cria_interferencias(N_parques):
    """
    Cria as interferências para um parque
    """
    nome_layout, angulo_inicial, angulo_final, raio, EPSG, letter, zona = inicia(N_parques)
    # pega os parametros da planilha
    # cria o arco
    le_pontos(nome_layout, angulo_inicial, angulo_final, raio, EPSG, letter, zona)
    # união dos arcos
    layer_arco = registry.mapLayersByName("output_Reprojected")[0]
    layer_union = registry.mapLayersByName("output_Reprojected")[0]
    count = 0
    # uniao varios arcos criando layers
    while len(QgsProject.instance().mapLayersByName("output_Reprojected")) != 0:
        count = count + 1
        layer_union = union_polygon(
            layer_union, layer_arco, "poligono", EPSG, "UNIAO" + str(count)
        )
        # remove os arcos unitarios
        remove_layer("output_Reprojected")
        if len(QgsProject.instance().mapLayersByName("output_Reprojected")) != 0:
            layer_arco = registry.mapLayersByName("output_Reprojected")[0]
    # remove todas as uniões feitas exceto layer desejado(o último formado)
    for i in range(1, count):
        remove_layer("UNIAO" + str(i))
    rename_layer("UNIAO" + str(count), "Interferencias_" + str(nome_layout))

def main():
   # le quantos parques tem na planilha
    parques = int(str(main_num_parques(path))[0])
    # cria o sombreamento dos parques
    for i in range(parques):
        print(i)
        cria_interferencias(i)

#main()