import os, argparse
from PyQt5.QtWidgets import *
from qgis.core import *
def deleteShapefile(aDir, aFile):

    fnameNoExt = os.path.splitext(aFile)[0]

    extensions = ["shp", "shx", "dbf", "prj", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "ixs", "mxs", "atx", "xml", "cpg", "qix"]

    theFiles = [f for f in os.listdir(aDir) if os.path.isfile(os.path.join(aDir, f))] # get list of all files in that directory
    
    #print(fnameNoExt)
    for f in theFiles:
        theFile = os.path.basename(f)
        name, extension = os.path.splitext(f)
        # If the name matches the input file and the extension is in that list, delete it:
        if (name == fnameNoExt and extension.split(".")[1] in extensions): # handles the foo.shp.xml case too.
            print(os.path.join(aDir,f))
            os.remove (os.path.join(aDir,f))
def salva_shp(layer2,path):
    outFile= os.path.join(path, str(layer2.name())+'.shp')
    fields = layer2.fields()
    feats = layer2.getFeatures()
    writer = QgsVectorFileWriter(outFile, 'UTF-8', fields, \
    QgsWkbTypes.Polygon, layer2.sourceCrs(), 'ESRI Shapefile')
    for feat in feats:
        writer.addFeature(feat)
    print('done')
    return outFile
def le_todos_os_layers():
        '''
        lê todos os layers do painel do QGIS
        e retorna os ids e nomes
        '''
        registry = QgsProject.instance()
        layers_names = []
        layers=[]
        for layer in QgsProject.instance().mapLayers().values():
            layers_names.append(layer.name())
        for i in range(len(layers_names)):
            name=layers_names[i]
            layers.append(registry.mapLayersByName( name )[0])
        return(layers_names,layers)
def retornar_layer(nome):
        '''
        retorna o layer pelo nome
        '''
        registry = QgsProject.instance()
        return registry.mapLayersByName( nome )[0]
def reprojetar(layer):
    source_crs = QgsCoordinateReferenceSystem(layer.crs().authid())
    target_crs = QgsCoordinateReferenceSystem("EPSG: 4326")

    with edit(layer):
        for feat in layer.getFeatures():
            # you need to store the geometry in a variable to reproject it; you can not reproject without doing so
            geom = feat.geometry() 
            # transform the geometry
            geom.transform(QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance()))
            # now update the features geometry
            feat.setGeometry(geom)
            # dont forget to update the feature, otherwise the changes will have no effect
            layer.updateFeature(feat)
        # finally simply set the layers crs to the new one
        layer.setCrs(target_crs)
    return layer
def cria_shp(path,layer):
    #registry = QgsProject.instance()
    #layer_do_post_gis='postgres://dbname=\'postgres\' host=192.168.0.63 port=5432 sslmode=disable key=\'id\' srid=4326 type=MultiPolygonZ checkPrimaryKeyUnicity=\'1\' table="BASES"."Spa" (geom)'
    Layer=retornar_layer(layer)
    result = reprojetar(Layer)
    saida_shp=salva_shp(result,path)
    return saida_shp 
    