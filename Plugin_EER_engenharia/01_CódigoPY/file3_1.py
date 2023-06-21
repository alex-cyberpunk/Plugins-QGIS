import qgis
import processing
from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from PyQt5.QtWidgets import *

'''
Nota : o algoritmo só funciona caso:
1)verifica se o layout de aeros digitado esta no padrão , se não tiver , coneverte.
2) o padrão usado no código é o SIRGAS 2000 UTM 23 S ou 24S
3)caso não esta no epsg , ele converte os layers e coloca _Reproject no fim de cada layer
4) após isso ele verifica se os parques estão sobrepostos por intersecção
5) verifica se os buffers estão dentro do parque através do seguinte processo:
    Primeiro: separa os pontos do layout escolhido dentro do parque por intersecção
              Depois faz um buffer desses pontos, está seria a "situação ideal" desses buffers
    Segundo :faz a intersecção dos buffers de todos os pontos do layout com o parque
            (Caso o buffer esteja fora do parque o resultado será buffers cortados)
    Terceiro : faz a diferença de buffer ideal e real um a um verificando se existe ou não diferença
               se houver diferença , o buffer ta pra fora 
6)Casos não abragentes: além de possiveis problemas de tipo de arquivo (se é shapefile ou não)
  o código não trara resultados bons caso os pontos de layout não estejam no seu parque correspondente
  Se o código ler arquivos que não seja os parques (como bordeada) ele não vai apresentar erros grotescos ,
  porém ira demorar mais pra rodar. Além disso vale observar que poligonos do validor EOL ou arquivos .wps
  podem apresentar problemas.(arquivos de validor EOL podem ter sobreposições de parques , ver caso a caso)

'''
#################################
# Intersection
def leitor_de_layer():
    layers_names = []
    layer1=[]
    for layer in QgsProject.instance().mapLayers().values():
        layers_names.append(layer.name())
    for i in range(len(layers_names)):
        name=layers_names[i]
        booleano=filtra_SRC_diferentes(name,EPSG)
        if booleano==1:
            layer1.append(registry.mapLayersByName( str(name)+'_Reprojected' )[0])
            layers_names[i] = str(name)+'_Reprojected'
        else: layer1.append(registry.mapLayersByName( name )[0])
    return(layers_names,layer1)
def remove_layer(lyrname):
    qinst = QgsProject.instance()
    qinst.removeMapLayer(qinst.mapLayersByName(lyrname)[0].id())
def reprojet_layer(nome):
    layer=registry.mapLayersByName( nome )[0]
    epsg1 = layer.crs().postgisSrid()
    parameter = {'INPUT': layer, 'TARGET_CRS': 'EPSG:'+str(EPSG),
                     'OUTPUT': 'memory:'+str(nome)+'_Reprojected'}
    result = processing.run('native:reprojectlayer', parameter)
    QgsProject.instance().addMapLayer(result['OUTPUT'])
def filtra_SRC_diferentes(nome,EPSG):
    registry = QgsProject.instance()
    layer=registry.mapLayersByName( nome )[0]
    #print(layer)
    if layer.crs().postgisSrid()!= EPSG:
        print("O layer "+str(nome))
        print("não está no epsg correto , convertendo...")
        reprojet_layer(nome)
        remove_layer(nome)
        return 1
    else: return 0
def leitor_de_parques(layers_names,layer_principal):
    layer_parques=[]
    layer_names_parques=[]
    for i in range(len(layer_principal)):
        for feat in layer_principal[i].getFeatures():
            geom = feat.geometry()
            if geom.type() == QgsWkbTypes.PolygonGeometry:
                layer_parques.append(layer_principal[i])
                layer_names_parques.append(layers_names[i])
    return(layer_parques,layer_names_parques)
def tem_intersecao_entre_parques(area1,area2):#retorna 0 se houver intersecção 
    #index = QgsSpatialIndex(area1.getFeatures())
    for feat in area1.getFeatures():
        geom1 = feat.geometry()
    for feat in area2.getFeatures():
        geom2 = feat.geometry()
    for p in area1.getFeatures():
        for i in area2.getFeatures():
            if p.geometry().intersects(i.geometry()):
                    return 1
            else:
                return 0
def comparador():
    (layers_names,layer_principal)=leitor_de_layer()
    parada=False
    auxiliar=0
    valor=[]
    quantidade=len(layers_names)
    j=0
    for i in range(quantidade):
        j=i+1
        parada=False
        while j<quantidade and parada==False:
            valor=(tem_intersecao_entre_parques(layer_principal[i],layer_principal[j]))
            if valor ==1:
                auxiliar=j
                parada=True
                print("O Parque "+str(layers_names[i])+" tem sobreposição")
                print("O Parque "+str(layers_names[auxiliar])+" tem sobreposição")
                #print()
            j=j+1
        j=0
def interccao(tipo,nome1,nome2):
    layerPoints=registry.mapLayersByName( nome1 )[0]
    layerPolygon=registry.mapLayersByName( nome2 )[0]
    featureList = []
    #print(layerPoints)
    for i in layerPoints.getFeatures():
        for p in layerPolygon.getFeatures():
            if i.geometry().intersects(p.geometry()):
                if(tipo=='Poligono'):
                    intersection = i.geometry().intersection(p.geometry())
                    featureList.append(intersection)
                else :featureList.append(i.geometry())
                #print(i.geometry().intersects(p.geometry()))
    epsg = layerPoints.crs().postgisSrid()
    # Create layer with result
    if(tipo=='Poligono'):
        name='polygons1'
        uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
        layer = QgsVectorLayer(uri,
                               'polygons1',
                               'memory')
    if(tipo=='Ponto'):
        name='intersection_points1'
        uri = "Point?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
        layer = QgsVectorLayer(uri,
                               'intersection_points1',
                               'memory')
    prov = layer.dataProvider()
    feats = [ QgsFeature() for i in range(len(featureList)) ]
    for i, feat in enumerate(feats):
        feat.setAttributes([i])
        feat.setGeometry(featureList[i])
    prov.addFeatures(feats)
    registry.addMapLayer(layer)
    return name
def buffer(nome_layer,raio):
    layer = registry.mapLayersByName( nome_layer )[0]
    feats = [ feat for feat in layer.getFeatures() ]
    epsg = layer.crs().postgisSrid()
    uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
    name='buffer '+str(nome_layer)
    mem_layer = QgsVectorLayer(uri,
                               name,
                               'memory')
    prov = mem_layer.dataProvider()
    for i, feat in enumerate(feats):
        new_feat = QgsFeature()
        new_feat.setAttributes([i])
        tmp_feat = feat.geometry().buffer(raio, 5)
        new_feat.setGeometry(tmp_feat)
        prov.addFeatures([new_feat])
    registry.addMapLayer(mem_layer)
    return name
def diferenca(name1,name2):
    count=0
    layerPoints=registry.mapLayersByName( name1 )[0]
    layerPolygon=registry.mapLayersByName( name2 )[0]
    for i in layerPoints.getFeatures():
        for p in layerPolygon.getFeatures():
            if i.geometry().intersects(p.geometry()):
                diferenca=i.geometry().difference(p.geometry())
                #print(diferenca.isEmpty())
                if diferenca.isEmpty()==False:
                    count=count+1
    print("há "+str(count)+" buffer(s) fora desse parque")
    print()
def verifica_buffer_em_poligonos(filtro1,filtro2,raio):
    interccao('Ponto',filtro1,filtro2)
    nome=buffer('intersection_points1',raio)
    nome_buffer_principal=buffer(filtro1,raio)
    #print(nome_buffer_principal)
    nome_interseccao_polygono=interccao('Poligono',nome_buffer_principal,filtro2)
    diferenca(nome,nome_interseccao_polygono)#ordem , primeiro buffer cheio , depois buffer cortado
    remove_layer('intersection_points1')
    remove_layer('polygons1')
    remove_layer(nome_buffer_principal)
    remove_layer(nome)
#####################################
def main():
    print("Código Verifica Buffers")
    (answer,bool) = QInputDialog().getText(None, "Escolha o epsg SIRGAS 2000 digitando:", " : (1) 24S  (2) 23 S")
    if int(answer)==1: 
        EPSG=31984
        print("o epsg usado é SIRGAS 2000/UTM 24S")
    elif int(answer)==2:
        EPSG=31983
        print("o epsg usado é SIRGAS 2000/UTM 23S")
    else:print("não foi digitado uma das duas opções")
    (answer,bool) = QInputDialog().getText(None, "Input", "Entre com o valor dos raios dos buffers:")
    raio=float(answer) #raio dos buffers
    (answer1,bool) = QInputDialog().getText(None, "Input", "Entre com a entrada do nome do layout dos aeros reprojetado:")
    booleano=filtra_SRC_diferentes(answer1,EPSG)
    if booleano == 1: filtro1=answer1+'_Reprojected'
    else: filtro1=answer1
    ####################################
    print("Não esqueça de verificar o epsg do seu projeto , coloque o mesmo do parque 24S/23S")
    (layers_names,layer_principal)=leitor_de_layer()
    (layer_parques,layer_names_parques)=leitor_de_parques(layers_names,layer_principal)
    print()
    comparador()
    print()
    for i in range (len(layer_parques)): 
        print("No Parque "+str(layer_names_parques[i])) 
        verifica_buffer_em_poligonos(filtro1,layer_names_parques[i],raio)
    nome=buffer(str(filtro1),raio)