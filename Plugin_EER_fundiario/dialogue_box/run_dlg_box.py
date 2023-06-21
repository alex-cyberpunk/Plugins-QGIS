import os
from qgis.core import QgsProject, Qgis
from exec_dlg_box import AlocAeroDialog
def run(iface):
        dlg = AlocAeroDialog(iface)
        # atualiza os combos
        layerTree = QgsProject.instance().layerTreeRoot().findLayers()
        layers = [lyr.layer() for lyr in layerTree]
        ## mostra todos os layer no combobox
        allLayers = [lyr for lyr in layers if lyr.type() == 0]
        dlg.updateLayerCombo([lyr.name() for lyr in allLayers])

        # mostra a caixa de dialogo
        dlg.show()
        # executa a caixa de dialogo
        result = dlg.exec_()
        # verifica se passou
        if result:
            layerName = dlg.getVectorLayer()#layer parque
            layerName2= dlg.getVectorLayer2()#layer layout
            raio=dlg.getDoubleSpinBox()
            outFile = dlg.getOutFile()

            # Pega apenas os layer ativos
            canvas = iface.mapCanvas()
            shownLayers = [x.name() for x in canvas.layers()]
            layer = canvas.layer(shownLayers.index(layerName))

            #emite mensagens de erro caso alum dos campos nao esteja preenchido
            if layerName not in shownLayers:
                dlg.emitMsg("Layer nao encontrado ou nao visivel!", layerName,
                             Qgis.Warning)
            elif layerName2 not in shownLayers:
                dlg.emitMsg("Layer nao encontrado ou nao visivel! ", layerName,
                             Qgis.Warning)
            elif outFile == "":
                dlg.emitMsg("Escolha um caminho para salvar o excel", "", Qgis.Warning)
            elif raio == 0:
                dlg.emitMsg("Escolha um raio para o buffer", "", Qgis.Warning)
        return layerName,layerName2,raio,outFile

from exec_dlg_box import GeraBasesDialog
def run_gera_base(iface):
        dlg = GeraBasesDialog(iface)
        # atualiza combos
        layerTree = QgsProject.instance().layerTreeRoot().findLayers()
        layers = [lyr.layer() for lyr in layerTree]
        ## todos os layers no  combobox
        allLayers = [lyr for lyr in layers if lyr.type() == 0]
        dlg.updateLayerCombo([lyr.name() for lyr in allLayers])
        # mostra a caixa de dialogo
        dlg.show()
        # executa a caixa de dialogo
        result = dlg.exec_()
        # verifica se passou
        if result:
            inputFile = dlg.getInputFile()
            outFile = dlg.getOutFile()
            layerName = dlg.getVectorLayer()#layer parque

            # Pega apenas os layer ativos
            canvas = iface.mapCanvas()
            shownLayers = [x.name() for x in canvas.layers()]
            layer = canvas.layer(shownLayers.index(layerName))

            #emite mensagens de erro caso alum dos campos nao esteja preenchido
            if layerName not in shownLayers:
                dlg.emitMsg("Layer nao encontrado ou nao visivel!", layerName,
                             Qgis.Warning)
            elif inputFile == "":
                dlg.emitMsg("Escolha um caminho para salvar o excel", "", Qgis.Warning)
            elif outFile == "":
                dlg.emitMsg("Escolha um caminho para salvar o excel", "", Qgis.Warning)
        print (inputFile)
        return inputFile,outFile,layerName

