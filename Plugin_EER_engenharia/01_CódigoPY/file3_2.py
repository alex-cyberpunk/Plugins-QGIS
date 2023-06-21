import qgis
from qgis.core import *
from PyQt5.QtWidgets import *
registry = QgsProject.instance()
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
    for i in range(len(layer_principal)):
        for feat in layer_principal[i].getFeatures():
            geom = feat.geometry()
            if geom.type() == QgsWkbTypes.PolygonGeometry:
                layer_parques.append(layer_principal[i])
                layer_names_parques.append(layers_names[i])
    return(layer_parques,layer_names_parques)
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
                print()
            j=j+1
        j=0
def main():
    print("EU SOU O SOBREPSOICAO DE PARQUE")
    (layers_names,layer_principal)=leitor_de_layer()
    (layer_parques,layer_names_parques)=leitor_de_parques(layers_names,layer_principal)
    print()
    comparador()