#!/usr/bin/env python

import detection as dron
import settings as config
from PIL import Image
from time import time

#folder = 'fotos_dron'
#file = 'min-46-51-125-212-2016-10-24.jpg'

tinicial=time()

#file = '2016-07-24-08-10-18.jpg'
#file = '130-132-258-408-2016-11-06.jpg'
file='82-52-127-219-2016-11-05.jpg'
#file='82-52-127-214-2016-11-05.jpg'
#file='82-52-127-219-2016-11-05.jpg'

#file='foo3280rapida-2.jpg'
#file='foo1300rapida.jpg'

#rutamin = "min-" + file
#i=Image.open("fotos_dron/"+file)
#i.thumbnail((1300,1000), Image.ANTIALIAS)
#i.save("fotos_dron/"+rutamin, i.format)
#file=rutamin


is_folder = 0

# initialize configuration settings (needs to be done just once)
config.initConfig()
#config.setExclusionMargin(10)
config.setDebugMode(2)
#config.setResize(0.6)
config.setMinAreaSize(8)
config.setSourceFolderName('fotos_dron')
config.setResize(0.5)
#config.setThreshold([(0,255), (0,255), (80,255)])
config.setThreshold([(50,85), (60,125), (105,175)])

#initialize log
config.initLog('dron')

# para carpeta
# dron.run(folder, is_folder)
dron.run(file, is_folder)

# close current log
config.closeLog()

tfinal=time()

print str(round(tfinal-tinicial,2))
