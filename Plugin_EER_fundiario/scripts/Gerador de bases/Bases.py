from cmath import nan
import pandas as pd
import lxml.etree as ET
from lxml.builder import ElementMaker
from xml.dom import minidom
import xlrd 
import math
import time
import locale
import os 


def retorna_mes():
	from datetime import datetime
	currentMonth = datetime.now().month
	currentYear= datetime.now().year
	x=[]
	for i in range(1,12):x.append(i)
	y=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
	for i in range(len(x)):
		if(currentMonth==x[i]):mesAno=y[i]+'/'+str(currentYear)[2:4]
	return mesAno
locale.setlocale(locale.LC_TIME, "pt_BR.utf-8")

mesAno = 'mai/23'


def makeSimpleFieldSchema(name, text):
	simplefield = ET.Element('SimpleField')
	simplefield.set('type', 'string')
	simplefield.set('name', name)
	ET.SubElement(simplefield, 'displayName').text = text
	return simplefield
	

# Cria os estilos (ballão, cores de linha e cor do poligono)
def makeStyle(idStyle, lineStyleSpecs, polyStyle):
    style = ET.Element('Style')
    style.set('id', idStyle)
    BalloonStyle = ET.SubElement(style, 'BalloonStyle')
    text = ET.SubElement(BalloonStyle, 'text')
    text.text = ET.CDATA('<table border="0"><tr><td><b>Área</b></td><td>$[teste/AREA]</td></tr><tr><td><b>Proprietário</b></td><td>$[teste/PROPRIETARIO]</td></tr><tr><td><b>Matrícula</b></td><td>$[teste/MATRICULA]</td></tr><tr><td><b>Contrato</b></td><td>$[teste/CONTRATO]</td></tr><tr><td><b>Status</b></td><td>$[teste/STATUS]</td></tr><tr><td><b>Area (ha)</b></td><td>$[teste/AREA_UTM]</td></tr><tr><td><b>Nome Imovel</b></td><td>$[teste/NOME_IMOVEL]</td></tr></table>')
    linestyle = ET.SubElement(style, 'LineStyle')
    if lineStyleSpecs['width'] != None:
        ET.SubElement(linestyle, 'width').text = lineStyleSpecs['width']
    if lineStyleSpecs['color'] != None:
        ET.SubElement(linestyle, 'color').text = lineStyleSpecs['color']
    polystyle = ET.SubElement(style, 'PolyStyle')
    ET.SubElement(polystyle, 'color').text = polyStyle['color']
    return style

# Cria a legenda com o link fixo
def makeLegenda():
	return ET.fromstring('<ScreenOverlay><name>LEGENDA</name><open>1</open><Icon><href>https://i.ibb.co/DLTttZg/Legenda-v2.png</href></Icon><overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/><screenXY x="30" y="50" xunits="pixels" yunits="pixels"/><rotationXY x="0.5" y="0.5" xunits="fraction" yunits="fraction"/><size x="0" y="0" xunits="pixels" yunits="pixels"/></ScreenOverlay>')

# Cria uma pasta
def makeFolder(folderName):
	folder = ET.Element('Folder')
	name = ET.SubElement(folder, 'name').text = folderName
	return folder

#modifica as coordenadas para ficar no padrao que seja aceitado pelo kml
def normalizeCoords(coords):
		coords = coords.strip('[]')
		coords = coords.split(",")
		final = []
		for i in range(0, len(coords), 2):
			final.append(coords[i].strip(' ()') + "," + coords[i+1].strip(' ()')+",0")
		s = "\n"
		return s.join(final)

# Cria a marcação do poligono com os dados e estilo
def makePlacemark (dados, style):
	placemark = ET.Element('Placemark')
	ET.SubElement(placemark, 'name').text = dados["# Área"]
	ET.SubElement(placemark, 'styleUrl').text = '#'+style
	extendedData = ET.SubElement(placemark, 'ExtendedData')
	schemaData = ET.SubElement(extendedData, 'SchemaData')
	schemaData.set('schemaUrl', '#S_teste_SSSSSD')

	simpledata = ET.SubElement(schemaData, 'SimpleData')
	simpledata.text = str(dados['# Área']) if str(dados['# Área']) != 'nan' else ""
	simpledata.set('name', 'AREA')
	simpledata = ET.SubElement(schemaData, 'SimpleData')

	simpledata.set('name', "PROPRIETARIO")
	simpledata.text = str(dados['Proprietário principal']) if str(dados['Proprietário principal']) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')
	
	simpledata.set('name', "MATRICULA")
	simpledata.text = str(dados['Matrícula']) if str(dados['Matrícula']) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')
	
	simpledata.set('name', "CONTRATO")
	simpledata.text = str(dados['Contrato']) if str(dados['Contrato']) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')
	
	simpledata.set('name', "STATUS")
	simpledata.text =  str(dados['Situação do imóvel '+ mesAno]) if str(dados['Situação do imóvel '+ mesAno]) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')
	
	simpledata.set('name', "AREA_UTM")
	simpledata.text = str(dados['Área (ha) - matrícula']) if str(dados['Área (ha) - matrícula']) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')

	simpledata.set('name', "NOME_IMOVEL")
	simpledata.text = str(dados['Imóvel']) if str(dados['Imóvel']) != 'nan' else ""
	simpledata = ET.SubElement(schemaData, 'SimpleData')

	polygon = ET.SubElement(placemark, 'Polygon')
	outerboundaryis = ET.SubElement(polygon, 'outerBoundaryIs')
	lineraring = ET.SubElement(outerboundaryis, "LinearRing")
	coordinates = ET.SubElement(lineraring, 'coordinates')
	coordinates.text = normalizeCoords(str(dados['Coordenadas']))

	return placemark	

# Verifica se uma subpasta ja foi criada
def verifySubfolder(folder, name, element = False):
	if (folder['subfolder'] and len(folder['subfolder']) > 0):
		for i in range(0, len(folder['subfolder'])):
			if (folder['subfolder'][i]['name'] == name):
				if (element == False):
					return folder['subfolder'][i]['element']
				else:
					return folder['subfolder'][i]	
	return False

# Cria subpasta dentro de uma pasta específica
def createSubFolder(document,folder, dados, texto = None):
	
	if (texto != None):
		subfolderelement = verifySubfolder(folder, texto)
		if (subfolderelement != False):
			if dados['Possui topografia?'].strip() == "SEM TOPOGRAFIA":
				subfolderelement.append(makePlacemark(dados, folder['name'].replace(" ", "").lower()+"_sem_topo"));
			else:
				if("concorrente" in folder['idColor']):
					subfolderelement.append(makePlacemark(dados, 'concorrentes'));				
				else:
					subfolderelement.append(makePlacemark(dados, folder['name'].replace(" ", "").lower()));

		else:
			folderAux = makeFolder(texto)
			colorAux = ''
			if dados['Possui topografia?'].strip() == "SEM TOPOGRAFIA":
				document.append(makeStyle(folder['name'].replace(" ", "").lower()+"_sem_topo", {'width':'2', 'color': 'FF000000'}, folder['colors']['polyStyle'])), 
				colorAux = folder['name'].replace(" ", "").lower()+"_sem_topo"
				
			else:
				colorAux = folder['idColor']
			folderAux.append(makePlacemark(dados, colorAux))
			folder['subfolder'].append({'name': texto, 'element': folderAux, 'idColor': colorAux })
	else:
		folder['element'].append(makePlacemark(dados, folder['idColor']))

#cria um kmz apartir do caminho onde ira se criar , o nome do parque(file_atual) e o dataframe com os dados(exportados do-excel GPD - df)
def cria_kmz(df,file_atual,pathz):
	
	print(mesAno)

	#Cria matriz com nome de projeto e seu código
	project_name = [["projeto","nome do projeto"]]
	projeto=""
	codigo_projeto=""
	#Descobre qual projeto está sendo analisado
	for i in range(	len(project_name)):
		if file_atual[0].lower() == project_name[i][0].lower():
			projeto = project_name[i][1]
			#file_path = file_atual[1]
			codigo_projeto = project_name[i][0]
			break

	# Cria cabeçalho de especificação KML
	orig_xml = '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"></kml>'
	kml = ET.fromstring(orig_xml)

	#Pastas de nível 1 do sistema
	folders = [{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'660d00fc'}}, 'subfolder':[]},
			{'name': "ITEM DE SUBPASTA", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ff00ffff"}, 'polyStyle':{'color':'99898988'}}, 'subfolder':[]},
			{'name': "ITEM DE SUBPASTA", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66000000'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'6600ffff'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'660055ff'}}, 'subfolder': []},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'ccffffff'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66ffff00'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66ffcf30'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66ffa855'}}, 'subfolder': []},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66ff0000'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'66ff00aa'}}, 'subfolder':[]},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': "ffffffff"}, 'polyStyle':{'color':'667f00aa'}}, 'subfolder': []},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': 'ffffffff'}, 'polyStyle':{'color':'6600aa00'}}, 'subfolder': []},
			{'name': "NOME STATUS", 'element':[], 'idColor':None, 'colors':{'lineStyle':{'width': '2', 'color': 'ffffffff'}, 'polyStyle':{'color':'6600aa00'}}, 'subfolder': []}
			]

	# Cria root e configurações basicas do documento 
	document = ET.SubElement(kml, "Document")
	ET.SubElement(document, "name").text = projeto
	ET.SubElement(document, "open").text = "1"

	# Cria o SCHEMA do Balão
	schema = ET.SubElement(document, 'Schema')
	schema.set('name', 'teste')
	schema.set('id', 'S_teste_SSSSSD')
	schema.append(makeSimpleFieldSchema("Area","&lt;b&gt;Area&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Proprietario", "&lt;b&gt;Proprietario&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Matricula", "&lt;b&gt;Matricula&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Contrato", "&lt;b&gt;Contrato&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Status", "&lt;b&gt;Status&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Area (ha)", "&lt;b&gt;Area (ha)&lt;/b&gt;"))
	schema.append(makeSimpleFieldSchema("Nome Imovel", "&lt;b&gt;Nome Imovel&lt;/b&gt;"))


	for folder in folders:
		folder['element'] = makeFolder(folder['name'])
		folder['idColor'] = folder['name'].replace(" ", "").lower()
		document.append(makeStyle(folder['name'].replace(" ", "").lower(), folder['colors']['lineStyle'], folder['colors']['polyStyle'])), 

	# aloca os elementos do dataframe nas subpastas do kmz
	data = df.to_dict('index')
	numberline = 0
	for row in data:
		print(row)
		numberline = numberline+1
		if(data[row]['ITEM DE SUBPASTA'] == 'SIM'):
			if isinstance(data[row]['Possui topografia?'], str):
				createSubFolder(document,folders[1], data[row], data[row]['Possui topografia??'])
			else: 
				createSubFolder(document,folders[1], data[row])
		elif(data[row]['ITEM DE SUBPASTA'] == 'SIM'):
			if isinstance(data[row]['Possui topografia?'], str):
				createSubFolder(document,folders[2], data[row], data[row]['Possui topografia?'])
			else: 
				createSubFolder(document,folders[2], data[row])
		elif(data[row]['ITEM DE SUBPASTA'] == 'SIM'):
			hasSubfolder = verifySubfolder(folders[0], data[row]['ITEM DE SUBPASTA'], True)
			if hasSubfolder == False:
				folderElement = makeFolder(data[row]['ITEM DE SUBPASTA'])
				folderAux = {'name': data[row]['Concorrente Contratante'], 'element': folderElement, 'colors': folders[0]['colors'],'idColor': folders[0]['idColor'], 'subfolder':[] }
				if isinstance(data[row]['Possui topografia?'], str):
					createSubFolder(document,folderAux, data[row], data[row]['Possui topografia?'])
				else: 
					createSubFolder(document,folderAux, data[row])
				folders[0]['subfolder'].append(folderAux)
			else:
				if isinstance(data[row]['Possui topografia?'], str):
					createSubFolder(document,hasSubfolder, data[row], data[row]['Possui topografia?'])
				else: 
					createSubFolder(document,hasSubfolder, data[row])
		else:
			if isinstance(data[row]['Situação do imóvel '+ mesAno], str):
				encontrou = False
				for i in range(3, len(folders)):
					if (data[row]['Situação do imóvel '+ mesAno].replace(" ", "").lower() == folders[i]['name'].replace(" ","").lower()):
						encontrou = True
						if isinstance(data[row]['Possui topografia?'], str):
							createSubFolder(document,folders[i], data[row], data[row]['Possui topografia?'])
						else: 
							createSubFolder(document,folders[i], data[row])
						break
				if (encontrou == False):
					print("Não tem pasta para "+data[row][mesAno])

			else: 
				print("Existe algum erro aqui: "+ str(data[row][mesAno]))

	document.append(makeLegenda())

	for i in range(len(folders)-1, -1, -1):
		for j in range(0, len(folders[i]['subfolder'])):
			if ('subfolder' in folders[i]['subfolder'][j]):
				for k in range(0, len(folders[i]['subfolder'][j]['subfolder'])):
					folders[i]['subfolder'][j]['element'].append(folders[i]['subfolder'][j]['subfolder'][k]['element'])
			folders[i]['element'].append(folders[i]['subfolder'][j]['element'])
		folder = document.append(folders[i]['element'])

	# salva o arquivo kmz de acordo com o nome do arquivo de entrada e a data de hoje
	tree = ET.ElementTree(kml)
	tree.write(pathz+ codigo_projeto + "_" + time.strftime("%y_%m_%d") + ".kmz")
	print('Arquivo gerado com sucesso!')




