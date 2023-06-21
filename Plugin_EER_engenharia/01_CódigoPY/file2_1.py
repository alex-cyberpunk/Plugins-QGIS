import os
from PyQt5.QtWidgets import *
from qgis.core import *
registry = QgsProject.instance()
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
def main():
    print("Salva em .shp")
    (answer,bool) = QInputDialog().getText(None, "Digite onde deseja salvar os pontos dos Vertices","caminho da pasta")
    path=answer
    (layers_names,layer_principal)=leitor_de_layer()
    (layer_parques,layer_names_parques)=leitor_de_parques(layers_names,layer_principal)
    for i in range(len(layer_parques)):
        outFile= os.path.join(path, str(layer_names_parques[i])+'.shp')
        fields = layer_parques[i].fields()
        feats = layer_parques[i].getFeatures()
        writer = QgsVectorFileWriter(outFile, 'UTF-8', fields, \
        QgsWkbTypes.Polygon, layer_parques[i].sourceCrs(), 'ESRI Shapefile')
        for feat in feats:
            writer.addFeature(feat)
        print('done')
        del(writer)

    