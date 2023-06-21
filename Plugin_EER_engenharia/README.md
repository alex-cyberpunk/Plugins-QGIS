**Introducao**

  Eu percebi que poderia ajudar no dia-a-dia da engenharia com algumas rotinas de python , principalmente quando fui designado para cuidar das atividades do validador EOL ,entao eu desenvolvi uma implementacao de um submenu que executa codigos file1_1,file1_2....,file4_1 . 
A ideia por tras disso era: a empresa tem o sharepoint para compartilhar arquivos entao , se eu coloca-se
os arquivos numa pasta compartilhada qualquer alteracao feita nos codigos individuais seriam sincronizados pelo sharepoint e lidos no diretorio local do usuario.
Uma das tarefas de muitas empresas de energia e validar Linhas de transmissao , propriedades,aerogeradores ,cones de interferencia...
e a aneel , orgao regulador validada isso em seu site:
https://sigel.aneel.gov.br/validadoreol/

1)Operacoes com planilha visando ler ou inserir nas planilhas do validador EOL (Interface Qgis e Validador EOL)
-Le as planilhas geradas pelo validador EOL e inserir para entrega era uma tarefa importante 
gerando as propriedades,aerogeradores,linhas de tranmissao , cones de interferencia.
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/a1d47a7d-d22e-41a2-aa5a-9ec4fde2730b)
file1_1:
"Excel para Qgis"
- Coleta as informacoes da planilha do validador EOL
file1_2:
"Qgis para Excel"
-Transforma as coordenadas dos poligonos do qgis numa planilha com o compilado de coordenadas. 

2)Operacoes com arquivos .shp (Carrega e Salva feicoes)
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/b0d7cc43-2563-4831-9659-d77404801470)

-Le os arquivos de pastas e subpastas e 
file2_1:
"Leitura de arquivos .shp"
file2_2:
"Gera arquivos .shp"

3)Operacoes com sobreposicoes
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/aaf2d063-c83d-4e90-8ccb-7caab98be023)

-A aneel nao permite nenhuma sobreposicao entre os poligonos e nao permite envio de buffers fora das propriedades,
dessa forma era necessario verificar quais poligonos e buffers precisavam ser ajustados. 
file3_1:
"Verifica buffers"
- verifica quais a sobreposicoes de buffers e poligonos
file3_2:
"Verifica sobreposicoes de parques"
- verifica quais a sobreposicoes entre os poligonos

4)Operacao de sombreamento
-No site do validador EOL pode-se observar os cones de interferencia , porem ele constroe esses cones apenas quando os aerogeradores foram inseridos no sistema
dessa forma seria muito benefico ter essa informacao antes (para enviar os aerogeradores na posicao correta etc..)
O que sao cones de interferencia ? Na iteracao de fluidos como o vento , existe um efeito chamado "wake effect" https://en.wikipedia.org/wiki/Wake_(physics) o que gera uma zona na qual a turbulencia de ventos e muito alta inutilzando a presenca de aerogeradores nessa zona. Essa zona e denominada "cones de interferencia" e estipulada pela aneel como uma zona a qual nao pode haver outros aerogeradores tem as caracteristicas:

"Cones de sombreamento"

Nivel de complexidade 
Simples: file1_1,file1_2,file2_1,file2_2
Medio:file3_1,file4_1
