**Introducao**

Eu percebi que poderia ajudar no dia-a-dia da engenharia com algumas rotinas de Python, principalmente quando fui designado para cuidar das atividades do validador EOL. Então, eu desenvolvi uma implementação de um submenu que executa códigos file1_1, file1_2, ..., file4_1. A ideia por trás disso era a seguinte: a empresa tem o SharePoint para compartilhar arquivos, então, se eu colocasse os arquivos em uma pasta compartilhada, qualquer alteração feita nos códigos individuais seria sincronizada pelo SharePoint e lida no diretório local do usuário.

Uma das tarefas de muitas empresas de energia é validar linhas de transmissão, propriedades, aerogeradores, cones de interferência, etc. A ANEEL, órgão regulador, valida isso em seu site: https://sigel.aneel.gov.br/validadoreol/.

As rotinas desenvolvidas que sao executadas pelo plugin sao : 

1)Operações com planilha visando ler ou inserir nas planilhas do validador EOL (Interface QGIS e Validador EOL)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/a1d47a7d-d22e-41a2-aa5a-9ec4fde2730b)

Descricao : Lê as planilhas geradas pelo validador EOL e insere para entrega, o que era uma tarefa importante, gerando as propriedades, aerogeradores, linhas de transmissão, cones de interferência.

file1_1:
"Excel para QGIS"

Modo de uso : insira o caminho da pasta onde estao as planilhas do validador EOL e o sirgas

Saida: poligonos no qgis

file1_2:
"QGIS para Excel"

Modo de uso : insira o caminho da pasta onde deseja salvar o excel

Saida: Uma planilha com o compliado de  Parques e subestacoes (poligonos) , LT (linhas)

2)Operações com arquivos .shp (Carrega e Salva feições)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/b0d7cc43-2563-4831-9659-d77404801470)

Descricao: Le .shps de pastas e subapastas e salva shps em pastas

-Le os arquivos de pastas e subpastas e 

file2_1:
"Leitura de arquivos .shp"

Modo de uso : insira o caminho da pasta onde deseja ler os .shps de pastas e subpastas

Saida: poligonos no qgis

file2_2:
"Gera arquivos .shp"

Modo de uso : insira o caminho da pasta onde deseja salvar os .shps de pastas e subpastas

Saida: Arquivos .shps dos poligonos do qgis

3)Operacoes com sobreposicoes

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/aaf2d063-c83d-4e90-8ccb-7caab98be023)

Descricao:A ANEEL não permite nenhuma sobreposição entre os polígonos e não permite o envio de buffers fora das propriedades. Dessa forma, era necessário verificar quais polígonos e buffers precisavam ser ajustados.

file3_1:
"Verifica buffers"
Modo de uso : insira o sirgas UTM dos pontos de aeros , o nome do layout de aeros no qgis
Saida: print no prompt do python do qgis das sobreposicoes de buffers e poligonos

file3_2:
"Verifica sobreposições de parques"
Modo de uso : sem entradas apenas execute a rotina
Saida: print no prompt do python do qgis das sobreposicoes de poligonos

4) Operação de Sombreamento

 Descricao :No site do validador EOL, é possível observar os cones de interferência. No entanto, esses cones são construídos apenas quando os aerogeradores são inseridos no sistema. Dessa forma, seria muito benéfico ter essa informação antecipadamente (para enviar os aerogeradores na posição correta, etc.). Mas afinal, o que são cones de interferência? Na interação de fluidos, como o vento, existe um efeito chamado "efeito de arrasto" (wake effect) [Fonte: Wikipedia - Wake (physics)], que gera uma zona de alta turbulência de vento, tornando a presença de aerogeradores nessa zona inutilizável. Essa zona é denominada "cones de interferência" e é estipulada pela ANEEL como uma área na qual não pode haver outros aerogeradores.

file4_1
"Cones de sombreamento"
Subrotinas: as subrotinas desse arquivo estao na pasta 'sombreamento' 
Modo de uso : insira o caminho onde se encontra a planilha chamada 'Planilha de entrada.xlsx' , essa e uma planilha padrao que contem as informacoes necessarias
para o calculo dos cones de interferencia. Essas informacoes podem ser encontradas na propria aneel. E possivel ainda escolher entre inserir os pontos na planilha 
ou usar um layout do qgis.
Saida:cones de interferencia no qgis dos pontos de turbinas

