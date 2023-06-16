**Introducao**

  Eu percebi que poderia ajudar no dia-a-dia da engenharia com algumas rotinas de python , principalmente quando fui designado para cuidar das atividades do validador EOL 
das entao eu desenvolvi uma implementacao de um submenu que executa codigos file1_1,file1_2....,file4_1 . 
A ideia por tras disso era: a empresa tem o sharepoint para compartilhar arquivos entao , se eu coloca-se
os arquivos numa pasta compartilhada qualquer alteracao feita nos codigos individuais seriam sincronizados pelo sharepoint e lidos no diretorio local do usuario.
Uma das tarefas de muitas empresas de energia e validar Linhas de transmissao , propriedades,aerogeradores ,cones de interferencia...
e a aneel , orgao regulador validada isso em seu site:
https://sigel.aneel.gov.br/validadoreol/

1)Operacoes com planilha visando ler ou inserir nas planilhas do validador EOL
-Le as planilhas geradas pelo validador EOL e inserir para entrega era uma tarefa importante 
gerando as propriedades,aerogeradores,linhas de tranmissao , cones de interferencia..
file1_1:
"Le planilhas do validador EOL"

file1_2:
"Gera compilado de coordenadas de planilhas para o validador EOL"

2)Operacoes com arquivos .shp
-Le os arquivos de pastas e subpastas e 
file2_1:
"Leitura de arquivos .shp"
file2_2:
"Gera arquivos .shp"

3)Operacoes com sobreposicoes
-A aneel nao permite nenhuma sobreposicao entre os poligonos e nao permite envio de buffers fora das propriedades,
dessa forma era necessario verificar quais precisavam ser ajustados. 
file3_1:
"Verifica interseccoes dos buffers com propriedades"

4)Operacao de sombreamento
-No site do validador EOL pode-se observar os cones de interferencia , porem ele constroe esses cones apenas quando os aerogeradores foram inseridos no sistema
dessa forma era muito benefico ter essa informacao antes (para enviar os aerogeradores na posicao correta etc..)
Na iteracao de fluidos como o vento , existe um efeito chamado "wake effect" https://en.wikipedia.org/wiki/Wake_(physics) o que gera uma zona na qual a turbulencia
de ventos e muito alta inutilzando a presenca de aerogeradores nessa zona. Essa zona e denominada "cones de interferencia" e estipulada pela aneel como uma zona
a qual nao pode haver outros aerogeradores tem as caracteristicas:
raio=
angulo=diametralmente oposto a zona de maior incidencia de vento 
file4_1:
"Cones de sombreamento"

Nivel de complexidade 
Simples: file1_1,file1_2,file2_1,file2_2
Medio:file3_1,file4_1
