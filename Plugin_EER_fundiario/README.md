Introducao
  A empresa tinha atuacao no campo fundiario e controlava de maneira interna os status ,documentacao e outras informacoes 
relevantes para a propriedade . Mas o software mais usado era o google earth nesse campo e dentro dos arquivos geograficos da engenharia (em .shp) 
continha apenas as informacoes geograficas. Dessa forma era necessario implementar uma solucao em codigo aberto que cruza-se as informacoes dos .shp 
e do controle interno num arquivo em .kmz de forma que usuarios da engenharia pudessem ter uma rotina rapida que gerasse os .kmz quando necessario.
Muitos dos colaboradores precisavam desse .kmz atualizado para realizar suas atividades diariamente. 
Outra rotina implementada nesse plugin porem nao totalmente desenvolvida foi um cruzamento de interseccao entre aerogeradores e propriedades para metricas internas,
porem nao foi totalmente desenvolvido pois logo depois entrou outras metricas as quais eu mesmo contribui para desenvolver.

 O Plugin tinha como objetivo original ter duas rotinas: 
  1-Rotina que combina os status de controle interno com itens gerograficos do qgis e gera . kmz 
  2-Cruza as informacoes de interseccao de aerogeradores e propriedades

Nessa implementacao usou-se a a barra de  menu  do qgis :

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/cfadcac1-196c-40fb-8705-4c80059e5032)

E implementou-se o menu qtdesing do qgis:

1)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/ed5c0420-1c5c-479b-bc45-e2bb1a959f4f)

Exemplo de saida do .kmz:
**A cor e de um dos status do controle interno 
2)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/7676fe12-65dc-450c-bb62-340d80c6d730)
