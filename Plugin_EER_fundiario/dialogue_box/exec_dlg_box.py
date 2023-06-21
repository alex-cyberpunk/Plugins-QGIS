import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qgis.core import QgsProject, Qgis

#duas classes de dialogo , uma para o alocador de aeros e outra para o gerador de bases

#alocador de aeros
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'aloc_aero.ui'))
class AlocAeroDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(AlocAeroDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        #liga os elementos do menu a funcao de saida de cada campo
        #layer = layer parque
        #layer2=layer layout
        self.outputButton.clicked.connect(self.outFile)#saida de arquivo
        self.layerCombo.currentIndexChanged.connect(self.updateFields)#saida layer
        self.layerCombo_2.currentIndexChanged.connect(self.updateFields2)#saida layer
        self.doubleSpinBox.valueChanged.connect(self.getDoubleSpinBox)#saida numerica
    def outFile(self):
        # Mostra a caixa de dialogo para escolher o arquivo de saida xlsx
        self.outputLine.clear()
        fileDialog = QtWidgets.QFileDialog()
        outFileName = fileDialog.getSaveFileName(self, "Save as", ".",
                                                 "xlsx (*.xlsx)")[0]
        if outFileName:
            if outFileName[-5:].lower() != ".xlsx":#limita a extensao do arquivo (5 caracteres)
                outFileName += ".xlsx"
            self.outputLine.clear()
            self.outputLine.insert(outFileName)

    #um vector layer para cada layer de saida
    def getVectorLayer(self):
        return(str(self.layerCombo.currentText()))
    def getVectorLayer2(self):
        return(str(self.layerCombo_2.currentText()))
    def getDoubleSpinBox(self):
        #print(self.doubleSpinBox.value())
        return (self.doubleSpinBox.value())
    def getOutFile(self):
        return(self.outputLine.text())

    def updateLayerCombo(self, items):
        #atualiza os layer das caixas de selecionar layers
        if len(items) > 0:
            self.layerCombo.clear()
            self.layerCombo_2.clear()
            for item in items:
                self.layerCombo.addItem(item)
                self.layerCombo_2.addItem(item)
    #duas funcoes , uma para cada campo de layer
    def updateFields(self):
        #coloca os layers na combo de saida 
        layer = self.getVectorLayer()
        if layer != "":
            layerTree = QgsProject.instance().layerTreeRoot().findLayers()
            allLayers = [lyr.layer() for lyr in layerTree]
            allLyrNames = [lyr.name() for lyr in allLayers]
            if layer in allLyrNames:
                lyr = allLayers[allLyrNames.index(layer)]
                fields = lyr.fields()
    def updateFields2(self):
        #coloca os layers na combo de saida
        layer2 = self.getVectorLayer2()
        if layer2 != "":
            layerTree = QgsProject.instance().layerTreeRoot().findLayers()
            allLayers = [lyr.layer() for lyr in layerTree]
            allLyrNames = [lyr.name() for lyr in allLayers]
            if layer2 in allLyrNames:
                lyr = allLayers[allLyrNames.index(layer2)]
                fields = lyr.fields()
    def setProgressBar(self, main, text, maxVal=100):
        self.widget = self.iface.messageBar().createMessage(main, text)
        self.prgBar = QtWidgets.QProgressBar()
        self.prgBar.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.prgBar.setValue(0)
        self.prgBar.setMaximum(maxVal)
        self.widget.layout().addWidget(self.prgBar)
        self.iface.messageBar().pushWidget(self.widget, Qgis.Info)

    def showMessage(self, main, txt):
        self.widget.setTitle(main)
        self.widget.setText(txt)

    def ProgressBar(self, value):
        self.prgBar.setValue(value)
        if (value == self.prgBar.maximum()):
            self.iface.messageBar().clearWidgets()
            self.iface.mapCanvas().refresh()

    def emitMsg(self, main, text, type):
        # Emite mensagens para QGIS.
        msg = self.iface.messageBar().createMessage(main, text)
        self.iface.messageBar().pushWidget(msg, type)

#gerador de bases
FORM_CLASS_gera, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'gera_bases.ui'))
class GeraBasesDialog(QtWidgets.QDialog, FORM_CLASS_gera):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(GeraBasesDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
         #liga os elementos do menu a funcao de saida de cada campo
        self.outputButton.clicked.connect(self.InputFile)
        self.outputButton_2.clicked.connect(self.outFile)
        self.layerCombo.currentIndexChanged.connect(self.updateFields)
    def InputFile(self):
        # Caixa file dialogue input
        #seleciona macro GPD de entrada
        self.outputLine.clear()
        fileDialog = QtWidgets.QFileDialog()
        filename = fileDialog.getOpenFileName(
            None, "Input File", ".",
            "xlsm (*.xlsm)")[0]
        if filename:
            if filename[-5:].lower() != ".xlsm":
                filename += ".xlsm"
            self.outputLine.clear()
            self.outputLine.insert(filename)
    def outFile(self):
        # Caixa file dialogue for output
        #seleciona apenas diretorio para saida
        self.outputLine_2.clear()
        fileDialog = QtWidgets.QFileDialog()
        outFileName = fileDialog.getExistingDirectory(self,"Open a folder", ".", QtWidgets.QFileDialog.ShowDirsOnly)
        if outFileName:
            self.outputLine_2.clear()
            self.outputLine_2.insert(outFileName)
    def getOutFile(self):
        return(self.outputLine_2.text())
    def getInputFile(self):
        return(self.outputLine.text())
    def getVectorLayer(self):
        return(str(self.layerCombo.currentText()))
    def updateLayerCombo(self, items):
        if len(items) > 0:
            self.layerCombo.clear()
            for item in items:
                self.layerCombo.addItem(item)

    def updateFields(self):
        #coloca os layers na combo de saida
        layer = self.getVectorLayer()
        if layer != "":
            layerTree = QgsProject.instance().layerTreeRoot().findLayers()
            allLayers = [lyr.layer() for lyr in layerTree]
            allLyrNames = [lyr.name() for lyr in allLayers]
            if layer in allLyrNames:
                lyr = allLayers[allLyrNames.index(layer)]
                fields = lyr.fields()
    def setProgressBar(self, main, text, maxVal=100):
        self.widget = self.iface.messageBar().createMessage(main, text)
        self.prgBar = QtWidgets.QProgressBar()
        self.prgBar.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.prgBar.setValue(0)
        self.prgBar.setMaximum(maxVal)
        self.widget.layout().addWidget(self.prgBar)
        self.iface.messageBar().pushWidget(self.widget, Qgis.Info)

    def showMessage(self, main, txt):
        self.widget.setTitle(main)
        self.widget.setText(txt)

    def ProgressBar(self, value):
        self.prgBar.setValue(value)
        if (value == self.prgBar.maximum()):
            self.iface.messageBar().clearWidgets()
            self.iface.mapCanvas().refresh()

    def emitMsg(self, main, text, type):
        # Emite mensagens para QGIS.
        msg = self.iface.messageBar().createMessage(main, text)
        self.iface.messageBar().pushWidget(msg, type)