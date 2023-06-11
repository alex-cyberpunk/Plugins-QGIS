from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
from qgis.gui import QgsMapTool
from PyQt5.QtWidgets import (QMenu,QApplication, QWidget, QPushButton, 
QLineEdit, QInputDialog)
import os
import sys
import subprocess

######################
########entrada#######
#####################
class SaveAttributesPlugin:
    
    def __init__(self, iface):
        self.iface = iface

    def importa_librarys(self):
        sys.path.insert(0, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))+'\scripts')
        from get_pip import installer_func
        installer_func()

    def run1(self):
        sys.path.insert(0, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))+'\dialogue_box')
        from run_dlg_box import run_gera_base
        gpd,kmz,layer=run_gera_base(self.iface)
        sys.path.insert(0, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))+'\scripts\Gerador de bases')
        from _init_ import main
        main(gpd,kmz,layer)

    def run2(self):
        sys.path.insert(0, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))+'\dialogue_box')
        from run_dlg_box import run
        layer_Prop,layer_Aero,r,saida=run(self.iface)
        sys.path.insert(0, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))+'\scripts\Alocador de Aerogeradores')
        from codigo_final import main
        main(r,layer_Prop,layer_Aero,saida)

    def initGui(self):
        self.importa_librarys()
        self.menu = QMenu( "&EER-Fundiario", self.iface.mainWindow().menuBar() )
        
        
        self.action1 = QAction('Gerador de bases')
        self.action1.triggered.connect(self.run1)
        self.menu.addSeparator()
        self.menu.addAction(self.action1)
        
        
        self.action2 = QAction('Alocador de Aerogeradores')
        self.action2.triggered.connect(self.run2)
        self.menu.addSeparator()
        self.menu.addAction(self.action2)
       
        
        self.iface.mainWindow().menuBar().insertMenu(self.action1,self.menu)
        
        
    def unload(self):
        self.iface.messageBar().pushMessage('Plugin removido')
    def run(self):
        self.iface.messageBar().pushMessage('Hello from Plugin')