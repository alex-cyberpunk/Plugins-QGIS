**Introducao**

Eu percebi que poderia ajudar no dia-a-dia da engenharia com algumas rotinas de Python, principalmente quando fui designado para cuidar das atividades do validador EOL. Então, eu desenvolvi uma implementação de um submenu que executa códigos file1_1, file1_2, ..., file4_1. A ideia por trás disso era a seguinte: a empresa tem o SharePoint para compartilhar arquivos, então, se eu colocasse os arquivos em uma pasta compartilhada, qualquer alteração feita nos códigos individuais seria sincronizada pelo SharePoint e lida no diretório local do usuário.

Uma das tarefas de muitas empresas de energia é validar linhas de transmissão, propriedades, aerogeradores, cones de interferência, etc. A ANEEL, órgão regulador, valida isso em seu site: https://sigel.aneel.gov.br/validadoreol/.

As rotinas desenvolvidas que sao executadas pelo plugin sao : 

1)Operações com planilha visando ler ou inserir nas planilhas do validador EOL (Interface QGIS e Validador EOL)
Lê as planilhas geradas pelo validador EOL e insere para entrega, o que era uma tarefa importante, gerando as propriedades, aerogeradores, linhas de transmissão, cones de interferência.
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/a1d47a7d-d22e-41a2-aa5a-9ec4fde2730b)

file1_1:
"Excel para QGIS"

Coleta as informações da planilha do validador EOL.
file1_2:
"QGIS para Excel"

Transforma as coordenadas dos polígonos do QGIS em uma planilha com o compilado de coordenadas.

2)Operações com arquivos .shp (Carrega e Salva feições)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/b0d7cc43-2563-4831-9659-d77404801470)

-Le os arquivos de pastas e subpastas e 
file2_1:
"Leitura de arquivos .shp"
file2_2:
"Gera arquivos .shp"

3)Operacoes com sobreposicoes
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/aaf2d063-c83d-4e90-8ccb-7caab98be023)

A ANEEL não permite nenhuma sobreposição entre os polígonos e não permite o envio de buffers fora das propriedades. Dessa forma, era necessário verificar quais polígonos e buffers precisavam ser ajustados.
file3_1:
"Verifica buffers"

Verifica quais sobreposições de buffers e polígonos existem.
file3_2:
"Verifica sobreposições de parques"

Verifica quais sobreposições existem entre os polígonos.

4)Operacao de sombreamento
-No site do validador EOL pode-se observar os cones de interferencia , porem ele constroe esses cones apenas quando os aerogeradores foram inseridos no sistema
dessa forma seria muito benefico ter essa informacao antes (para enviar os aerogeradores na posicao correta etc..)
O que sao cones de interferencia ? Na iteracao de fluidos como o vento , existe um efeito chamado "wake effect" https://en.wikipedia.org/wiki/Wake_(physics) o que gera uma zona na qual a turbulencia de ventos e muito alta inutilzando a presenca de aerogeradores nessa zona. Essa zona e denominada "cones de interferencia" e estipulada pela aneel como uma zona a qual nao pode haver outros aerogeradores tem as caracteristicas:

"Cones de sombreamento"

Nivel de complexidade 
Simples: file1_1,file1_2,file2_1,file2_2
Medio:file3_1,file4_1
