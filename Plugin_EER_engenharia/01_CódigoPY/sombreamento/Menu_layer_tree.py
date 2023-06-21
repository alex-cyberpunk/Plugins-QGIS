from qgis.gui import *
import time
from qgis.core import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qgis.utils import *
#######abre caixa de seleção de layer#############
'''
Essa parte captura apenas um layer selecionado e retorna para o main 
'''
class MyMenuProvider:
    
    def __init__(self):
        self.iface = iface
        self.click=False
        self.layer_clicados=[]
        self.root = QgsProject.instance().layerTreeRoot()
        self.model = QgsLayerTreeModel(self.root)
        self.view = QgsLayerTreeView()
    def waitUntil(self): #defines function
        wU = True
        while wU == True:
            print(wU)
            if self.click==True: #checks the condition
                wU = False
            if(wU==True):self.spin(5) #waits 60s for preformance
    def spin(self,seconds):
        """Pause for set amount of seconds, replaces time.sleep so program doesn't stall"""
        time_end = time.time() + seconds
        while time.time() < time_end:
            QApplication.processEvents()
    def select_layer(self,layer):
      #QMessageBox.information(None, "Change", "Current Layer: "+str(layer))
      print("clicou")
      self.layer_clicados.append(layer)
      if(len(self.layer_clicados)>1):
          #print("EAE")
          self.click=True
    def menu_layer_tree(self):
        self.view.setModel(self.model)
        # connect to the signal
        self.view.currentLayerChanged.connect(self.select_layer)
        self.view.show()
        # change selection to the top-most layer (onChange will be also called)
        self.view.setCurrentLayer( self.iface.mapCanvas().layers()[0] )
        self.waitUntil() #último layer capturado
#################################################