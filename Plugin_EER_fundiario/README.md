# Plugin EER fundiario
## Context

  The company operated in the land field and internally managed the status, documentation, and other relevant information for the property. However, the most used software in this field was Google Earth, and within the engineering geographic files (.shp), it only contained geographical information. Therefore, it was necessary to implement an open-source solution that would cross-reference the information from .shp files and the internal control into a .kmz file so that engineering users could have a quick routine to generate .kmz files when needed. Many of the employees needed these updated .kmz files to carry out their daily activities. Another routine implemented in this plugin, although not fully developed, was an intersection crossing between wind turbines and properties for internal metrics. However, it was not fully developed because soon after, other metrics were implemented, which I myself contributed to developing.

## Implementation
 
 ### The original goal of the plugin was to have two routines: 
  
  1- A routine that combines internal control statuses with geographic items from QGIS and generates .kmz files.

  2- Crosses the intersection information of wind turbines and properties.

In this implementation, the QGIS menu bar was used.

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/cfadcac1-196c-40fb-8705-4c80059e5032)

And the QDesign menu of QGIS was implemented.

1)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/ed5c0420-1c5c-479b-bc45-e2bb1a959f4f)

### Here is an example of the output .kmz file:
![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/c4bd2c33-9aa5-43cc-a010-f1e176aea7a8)

**The colors in the .kmz file represent different statuses from the internal control system, and the information provided is essential for the company's operations in the land field.

2)

![image](https://github.com/alex-cyberpunk/Plugins-QGIS/assets/80361639/7676fe12-65dc-450c-bb62-340d80c6d730)

Note: As the statuses are part of the company's internal control, they have been concealed in the code, but the implementation logic can still be seen.
