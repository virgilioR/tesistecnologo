class Config():
	def __init__(self):
		#Configuraciones done y estacas
		#cambiamos 1 por 2
		#self.distfotoCua=1
		self.cadenaconexion="/dev/serial0,57600"
		#self.cadenaconexion= "udp:127.0.0.1:14550"
		self.topeMetros=3
		self.movMetros=1
		#cambiamos....
		self.umbralA=0.5
		self.alturaestacavisible=0.6
		self.alturafranja = 0.05

		#Configuracion camaras e imagenes
		self.activarcamara = True
		self.resoluciones=[(1300, 975),(2592, 1944),(3280, 2464)]
		self.framerate=40
		self.overlapping=0.5
		self.angulocamancho=62.2
		self.angulocamlargo = 48.8
		#self.cantfotos=3
		self.dirfotos = "/srv/torreap/fotos/"

		#No procesamos en vuelo sino luego
		self.procImg = False


		# Configurado para fotos de 1300x900, que las deja en 250x1..
		#Sacamos fotos de mas altura ahora
		#self.procResize=0.2
		#self.procResize = 0.5
		#Muy chica, vamo a ver sin resize
		self.procResize = 0.6

		#self.procMinArea=20
		#en NGB anda bien 8 pero mejor el 6
		# Muy chica, vamo a ver sin resize
		self.procMinArea = 6

		# Umbral de colores RGB
		#self.umbralColores = [(0, 51), (0, 255), (80, 255)]
		#El nuevo el q anda MUCHO mejor
		#self.umbralColores = [(50, 85), (85, 160), (150, 255)]
		#Otro ajuste mas
		#self.umbralColores = [(50,100), (85,160), (150,255)]

		#Umbral de colores NGB
		self.umbralColores = [(50,85), (60,125), (105,175)]

		#No basamos la decision de movimiento en funcion del procesamiento de fotos
		self.decisionestiemporeal=False

		#Puertos y base de datos
		self.httpport=20000
		self.db="ecarpi"
		self.dbuser="torreap"
		self.dbpass="6aUKpOCW0Tsj"
		self.dbhost="localhost"
