from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from qgis.gui import QgsMapTool
from PyQt5.QtWidgets import (QMenu,QApplication, QWidget, QPushButton, 
QLineEdit, QInputDialog)
import os
import sys
import subprocess

######################
########entrada#######
#####################
path=r''#inserir caminho onde se encontram os codigos
path_code=r''#inserir caminho onde se encontram os icones do submenu

#codigo com a capacidade de alocar 10 itens de menu com 3 submenus cada

class SaveAttributesPlugin:
    
    def __init__(self, iface):
        self.iface = iface
    def importa_librarys(self):
        self.file_code_lib='import library.txt'
        self.the_code_lib = os.path.join(path_code, self.file_code_lib)
        loc = {}
        with open(self.the_code_lib,"r") as rnf_lib:
            exec(rnf_lib.read(), globals(), loc)
        self.return_library = loc['library']
        if self.return_library!='':
            subprocess.check_call(['python', '-m', 'pip', 'install', self.return_library])
    def run1_1(self):
        sys.path.append(self.path)
        from file1_1 import main
        main()
    def run1_2(self):
        sys.path.append(self.path)
        from file1_2 import main
        main()
    def run1_3(self):
        sys.path.append(self.path)
        from file1_3 import main
        main()
    def run2_1(self):
        sys.path.append(self.path)
        from file2_1 import main
        main()
    def run2_2(self):
        sys.path.append(self.path)
        from file2_2 import main
        main()
    def run2_3(self):
        sys.path.append(self.path)
        from file2_3 import main
        main()
    def run3_1(self):
        sys.path.append(self.path)
        from file3_1 import main
        main()
    def run3_2(self):
        sys.path.append(self.path)
        from file3_2 import main
        main()
    def run3_3(self):
        sys.path.append(self.path)
        from file3_3 import main
        main(self)
    def run4_1(self):
        sys.path.append(self.path)
        from file4_1 import main
        main()
    def run4_2(self):
        sys.path.append(self.path)
        from file4_2 import main
        main()
    def run4_3(self):
        sys.path.append(self.path)
        from file4_3 import main
        main()
    def run5_1(self):
        sys.path.append(self.path)
        from file5_1 import main
        main()
    def run5_2(self):
        sys.path.append(self.path)
        from file5_2 import main
        main()
    def run5_3(self):
        sys.path.append(self.path)
        from file5_3 import main
        main()
    def run6_1(self):
        sys.path.append(self.path)
        from file6_1 import main
        main()
    def run6_2(self):
        sys.path.append(self.path)
        from file6_2 import main
        main()
    def run6_3(self):
        sys.path.append(self.path)
        from file6_3 import main
        main()
    def run7_1(self):
        sys.path.append(self.path)
        from file7_1 import main
        main()
    def run7_2(self):
        sys.path.append(self.path)
        from file7_2 import main
        main()
    def run7_3(self):
        sys.path.append(self.path)
        from file7_3 import main
        main()
    def run8_1(self):
        sys.path.append(self.path)
        from file8_1 import main
        main()
    def run8_2(self):
        sys.path.append(self.path)
        from file8_2 import main
        main()
    def run8_3(self):
        sys.path.append(self.path)
        from file8_3 import main
        main()
    def run9_1(self):
        sys.path.append(self.path)
        from file9_1 import main
        main()
    def run9_2(self):
        sys.path.append(self.path)
        from file9_2 import main
        main()
    def run9_3(self):
        sys.path.append(self.path)
        from file9_3 import main
        main()
    def run10_1(self):
        sys.path.append(self.path)
        from file10_1 import main
        main()
    def run10_2(self):
        sys.path.append(self.path)
        from file10_2 import main
        main()
    def run10_3(self):
        sys.path.append(self.path)
        from file10_3 import main
        main()
    def initGui(self):
        self.importa_librarys()
        self.path=path
        self.path_code=path_code
        
        self.icon_path=os.path.join(self.path_code, 'icone.png')
        self.toolbar = self.iface.addToolBar('PEC Energia')
        self.toolbar.setObjectName('PEC Energia')
        self.Menu1 = QMenu('&PEC Energia',self.iface.mainWindow())

        dirs = os.listdir( self.path )
        total=[]
        nome_arquivos=[]
        nome_rotina=[]
        nome_submenus=[]
        count=0
        for file in dirs:
                if file.endswith(".py"):
                        runfile = os.path.join(self.path, file)
                        basename = os.path.basename(str(runfile))
                        file_name = os.path.splitext(basename)[0]
                        if file_name!='indice':
                           nome_arquivos.append(file_name)
        file_code='indice.txt'
        the_code = os.path.join(self.path_code, file_code)
        loc = {}
        with open(the_code,"r") as rnf:
                exec(rnf.read(), globals(), loc)
        return_workaround = loc['return_list']
        return_subemenus_names=loc['return_name_of_submenus']

        for i in range (len(return_workaround)):
            nome_rotina.append('')

        for i in range(len(nome_arquivos)):
            if nome_arquivos[i]=='file1_1':nome_rotina[0]= return_workaround[0]
            if nome_arquivos[i]=='file1_2':nome_rotina[1]= return_workaround[1]
            if nome_arquivos[i]=='file1_3':nome_rotina[2]= return_workaround[2]
            if nome_arquivos[i]=='file2_1':nome_rotina[3]= return_workaround[3]
            if nome_arquivos[i]=='file2_2':nome_rotina[4]= return_workaround[4]
            if nome_arquivos[i]=='file2_3':nome_rotina[5]= return_workaround[5]
            if nome_arquivos[i]=='file3_1':nome_rotina[6]= return_workaround[6]
            if nome_arquivos[i]=='file3_2':nome_rotina[7]= return_workaround[7]
            if nome_arquivos[i]=='file3_3':nome_rotina[8]= return_workaround[8]
            if nome_arquivos[i]=='file4_1':nome_rotina[9]= return_workaround[9]
            if nome_arquivos[i]=='file4_2':nome_rotina[10]= return_workaround[10]
            if nome_arquivos[i]=='file4_3':nome_rotina[11]= return_workaround[11]
            if nome_arquivos[i]=='file5_1':nome_rotina[12]= return_workaround[12]
            if nome_arquivos[i]=='file5_2':nome_rotina[13]= return_workaround[13]
            if nome_arquivos[i]=='file5_3':nome_rotina[14]= return_workaround[14]
            if nome_arquivos[i]=='file6_1':nome_rotina[15]= return_workaround[15]
            if nome_arquivos[i]=='file6_2':nome_rotina[16]= return_workaround[16]
            if nome_arquivos[i]=='file6_3':nome_rotina[17]= return_workaround[17]
            if nome_arquivos[i]=='file7_1':nome_rotina[18]= return_workaround[18]
            if nome_arquivos[i]=='file7_2':nome_rotina[19]= return_workaround[19]
            if nome_arquivos[i]=='file7_3':nome_rotina[20]= return_workaround[20]
            if nome_arquivos[i]=='file8_1':nome_rotina[21]= return_workaround[21]
            if nome_arquivos[i]=='file8_2':nome_rotina[22]= return_workaround[22]
            if nome_arquivos[i]=='file8_3':nome_rotina[23]= return_workaround[23]
            if nome_arquivos[i]=='file9_1':nome_rotina[24]= return_workaround[24]
            if nome_arquivos[i]=='file9_2':nome_rotina[25]= return_workaround[25]
            if nome_arquivos[i]=='file9_3':nome_rotina[26]= return_workaround[26]
            if nome_arquivos[i]=='file10_1':nome_rotina[27]= return_workaround[27]
            if nome_arquivos[i]=='file10_2':nome_rotina[28]= return_workaround[28]
            if nome_arquivos[i]=='file10_3':nome_rotina[29]= return_workaround[29]

        nome_arquivos_em_ordem=[]

        for i in range (len(return_workaround)):
            nome_arquivos_em_ordem.append('')

        for i in range(len(nome_arquivos)):
            if nome_arquivos[i]=='file1_1':nome_arquivos_em_ordem[0]= 'file1_1'
            if nome_arquivos[i]=='file1_2':nome_arquivos_em_ordem[1]= 'file1_2'
            if nome_arquivos[i]=='file1_3':nome_arquivos_em_ordem[2]= 'file1_3'
            if nome_arquivos[i]=='file2_1':nome_arquivos_em_ordem[3]= 'file2_1'
            if nome_arquivos[i]=='file2_2':nome_arquivos_em_ordem[4]= 'file2_2'
            if nome_arquivos[i]=='file2_3':nome_arquivos_em_ordem[5]= 'file2_3'
            if nome_arquivos[i]=='file3_1':nome_arquivos_em_ordem[6]= 'file3_1'
            if nome_arquivos[i]=='file3_2':nome_arquivos_em_ordem[7]= 'file3_2'
            if nome_arquivos[i]=='file3_3':nome_arquivos_em_ordem[8]= 'file3_3'
            if nome_arquivos[i]=='file4_1':nome_arquivos_em_ordem[9]= 'file4_1'
            if nome_arquivos[i]=='file4_2':nome_arquivos_em_ordem[10]= 'file4_2'
            if nome_arquivos[i]=='file4_3':nome_arquivos_em_ordem[11]= 'file4_3'
            if nome_arquivos[i]=='file5_1':nome_arquivos_em_ordem[12]= 'file5_1'
            if nome_arquivos[i]=='file5_2':nome_arquivos_em_ordem[13]= 'file5_2'
            if nome_arquivos[i]=='file5_3':nome_arquivos_em_ordem[14]= 'file5_3'
            if nome_arquivos[i]=='file6_1':nome_arquivos_em_ordem[15]= 'file6_1'
            if nome_arquivos[i]=='file6_2':nome_arquivos_em_ordem[16]= 'file6_2'
            if nome_arquivos[i]=='file6_3':nome_arquivos_em_ordem[17]= 'file6_3'
            if nome_arquivos[i]=='file7_1':nome_arquivos_em_ordem[18]= 'file7_1'
            if nome_arquivos[i]=='file7_2':nome_arquivos_em_ordem[19]= 'file7_2'
            if nome_arquivos[i]=='file7_3':nome_arquivos_em_ordem[20]= 'file7_3'
            if nome_arquivos[i]=='file8_1':nome_arquivos_em_ordem[21]= 'file8_1'
            if nome_arquivos[i]=='file8_2':nome_arquivos_em_ordem[22]= 'file8_2'
            if nome_arquivos[i]=='file8_3':nome_arquivos_em_ordem[23]= 'file8_3'
            if nome_arquivos[i]=='file9_1':nome_arquivos_em_ordem[24]= 'file9_1'
            if nome_arquivos[i]=='file9_2':nome_arquivos_em_ordem[25]= 'file9_2'
            if nome_arquivos[i]=='file9_3':nome_arquivos_em_ordem[26]= 'file9_3'
            if nome_arquivos[i]=='file10_1':nome_arquivos_em_ordem[27]= 'file10_1'
            if nome_arquivos[i]=='file10_2':nome_arquivos_em_ordem[28]= 'file10_2'
            if nome_arquivos[i]=='file10_3':nome_arquivos_em_ordem[29]= 'file10_3'

        sub_menu_item=[]
        menu_item=[]
        self.total_menus=[]
        self.icon_menu=''
        for i in range(0,len(nome_rotina),3):
            if nome_rotina[i]!='' and nome_rotina[i+1]=='':
                #é menu
                action = QAction(nome_rotina[i])
                if nome_arquivos_em_ordem[i]=='file1_1':action.triggered.connect(self.run1_1)
                if nome_arquivos_em_ordem[i]=='file2_1':action.triggered.connect(self.run2_1)
                if nome_arquivos_em_ordem[i]=='file3_1':action.triggered.connect(self.run3_1)
                if nome_arquivos_em_ordem[i]=='file4_1':action.triggered.connect(self.run4_1)
                if nome_arquivos_em_ordem[i]=='file5_1':action.triggered.connect(self.run5_1)
                if nome_arquivos_em_ordem[i]=='file6_1':action.triggered.connect(self.run6_1)
                if nome_arquivos_em_ordem[i]=='file7_1':action.triggered.connect(self.run7_1)
                if nome_arquivos_em_ordem[i]=='file8_1':action.triggered.connect(self.run8_1)
                if nome_arquivos_em_ordem[i]=='file9_1':action.triggered.connect(self.run9_1)
                if nome_arquivos_em_ordem[i]=='file10_1':action.triggered.connect(self.run10_1)
                self.total_menus.append(ction)
                
            else:
                self.first_menu = self.Menu1.addMenu(QIcon(''), return_subemenus_names[count])
                for j in range(i,i+3):
                    if nome_arquivos_em_ordem[j]!='':
                        self.SetupSubMenu = QAction((QIcon('')), nome_rotina[j],self.iface.mainWindow())
                        if nome_arquivos_em_ordem[j]=='file1_1':self.SetupSubMenu.triggered.connect(self.run1_1)
                        if nome_arquivos_em_ordem[j]=='file1_2':self.SetupSubMenu.triggered.connect(self.run1_2)
                        if nome_arquivos_em_ordem[j]=='file1_3':self.SetupSubMenu.triggered.connect(self.run1_3)
                        if nome_arquivos_em_ordem[j]=='file2_1':self.SetupSubMenu.triggered.connect(self.run2_1)
                        if nome_arquivos_em_ordem[j]=='file2_2':self.SetupSubMenu.triggered.connect(self.run2_2)
                        if nome_arquivos_em_ordem[j]=='file2_3':self.SetupSubMenu.triggered.connect(self.run2_3)
                        if nome_arquivos_em_ordem[j]=='file3_1':self.SetupSubMenu.triggered.connect(self.run3_1)
                        if nome_arquivos_em_ordem[j]=='file3_2':self.SetupSubMenu.triggered.connect(self.run3_2)
                        if nome_arquivos_em_ordem[j]=='file3_3':self.SetupSubMenu.triggered.connect(self.run3_3)
                        if nome_arquivos_em_ordem[j]=='file4_1':self.SetupSubMenu.triggered.connect(self.run4_1)
                        if nome_arquivos_em_ordem[j]=='file4_2':self.SetupSubMenu.triggered.connect(self.run4_2)
                        if nome_arquivos_em_ordem[j]=='file4_3':self.SetupSubMenu.triggered.connect(self.run4_3)
                        if nome_arquivos_em_ordem[j]=='file5_1':self.SetupSubMenu.triggered.connect(self.run5_1)
                        if nome_arquivos_em_ordem[j]=='file5_2':self.SetupSubMenu.triggered.connect(self.run5_2)
                        if nome_arquivos_em_ordem[j]=='file5_3':self.SetupSubMenu.triggered.connect(self.run5_3)
                        if nome_arquivos_em_ordem[j]=='file6_1':self.SetupSubMenu.triggered.connect(self.run6_1)
                        if nome_arquivos_em_ordem[j]=='file6_2':self.SetupSubMenu.triggered.connect(self.run6_2)
                        if nome_arquivos_em_ordem[j]=='file6_3':self.SetupSubMenu.triggered.connect(self.run6_3)
                        if nome_arquivos_em_ordem[j]=='file7_1':self.SetupSubMenu.triggered.connect(self.run7_1)
                        if nome_arquivos_em_ordem[j]=='file7_2':self.SetupSubMenu.triggered.connect(self.run7_2)
                        if nome_arquivos_em_ordem[j]=='file7_3':self.SetupSubMenu.triggered.connect(self.run7_3)
                        if nome_arquivos_em_ordem[j]=='file8_1':self.SetupSubMenu.triggered.connect(self.run8_1)
                        if nome_arquivos_em_ordem[j]=='file8_2':self.SetupSubMenu.triggered.connect(self.run8_2)
                        if nome_arquivos_em_ordem[j]=='file8_3':self.SetupSubMenu.triggered.connect(self.run8_3)
                        if nome_arquivos_em_ordem[j]=='file9_1':self.SetupSubMenu.triggered.connect(self.run9_1)
                        if nome_arquivos_em_ordem[j]=='file9_2':self.SetupSubMenu.triggered.connect(self.run9_2)
                        if nome_arquivos_em_ordem[j]=='file9_3':self.SetupSubMenu.triggered.connect(self.run9_3)
                        if nome_arquivos_em_ordem[j]=='file10_1':self.SetupSubMenu.triggered.connect(self.run10_1)
                        if nome_arquivos_em_ordem[j]=='file10_2':self.SetupSubMenu.triggered.connect(self.run10_2)
                        if nome_arquivos_em_ordem[j]=='file10_3':self.SetupSubMenu.triggered.connect(self.run10_3)
                        self.first_menu.addAction(self.SetupSubMenu)
                count=count+1
        for i in range(len(self.total_menus)):
            self.Menu1.addAction(self.total_menus[i])
        self.toolButton = QToolButton()
        self.toolButton.setIcon(QIcon(self.icon_path))
        self.toolButton.setMenu(self.Menu1)
        self.toolButton.setPopupMode(QToolButton.InstantPopup)
        self.toolbar.addWidget(self.toolButton)
        #self.iface.addPluginToMenu('&PEC', action)
    def unload(self):
        self.iface.messageBar().pushMessage('Plugin removido')
        #self.iface.removeToolBarIcon(action)
        #self.iface.removePluginMenu('&PEC')  
        #del action
    def run(self):
        self.iface.messageBar().pushMessage('Hello from Plugin')
