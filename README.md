# jfsOtterVIS
## General Info
The software is an extention of the [pyCCDGUI.py](https://tcd1304.wordpress.com/downloads/) from Esben Rossel and is based on his spectrophotometer ([OtterVIS LGL](https://hackaday.io/project/10738-ottervis-lgl-spectrophotometer)) which uses the TCD1304 chip. 
In order to use the software you should have already build Rosssel's spectrophometer. For more information, visit [Leaves of Science](https://science.jefro.de/).
## Features of the software
* the calibration of the instrument in nm
* the use of the spectrophometer as a photometer
* the survey of simple kinetics

##  Branches
* CalibrationByArray: Now its possible to calibrate the instrument by an csv-file for example non_linear_calibarray_HgCd.csv
## Installation
Recomendation: it is best to run the python program under the anaconda framework.
* Install anaconda [optional]
* run under the anaconda-shell: conda install -c anaconda pyserial
* download the software from github jfsCDDGUI.zip and unpack to /your_choice/
* go to /your_choice/ and run under anaconda-shell: python jfCCDGUI.py
## Licences
All software in source or binary form on this site are under the FreeBSD-license.

I would very much appreciate a short message with a brief introduction of your project, if you use the material presented here.

For the use of the TCD1304 material please refer to Esben Rossel 

Be aware that the STM32 Nucleo F401RE  is under ST’s evaluation license.


