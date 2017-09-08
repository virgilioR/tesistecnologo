from picamera import PiCamera
from time import sleep

camera = PiCamera()
#VERSION 1
#camera.resolution = (2592, 1944)
#VERSION 2 8 MP 
camera.resolution= (3280, 2464)
#camera.framerate = 15
camera.start_preview()
sleep(5)
camera.capture('/var/www/html/prueba.jpg')
camera.stop_preview()
