# activar
from picamera import PiCamera
from mision import Mision
from datetime import datetime
from recorrido import Recorrido
from config import Config
from PIL import Image
from persistencia import Persistencia
import procImg.detection as modDeteccion
import procImg.settings as configDeteccion
from time import time, sleep
from os import path

class ControladorCamara():
        def imprimir(self,texto):
                print (texto) 
                with open("/tmp/torreap", "a") as myfile:
                        myfile.write(str(texto)+ "\n")
        
	def __init__(self):
		self.config = Config()
		self.persistencia=Persistencia(self.config)
		self.misiones=[]
		self.misionact=None
		self.recorridos=[]
		self.recsel=None
		self.puntossel=[]
		self.puntosact=[]
		self.xinicial=None
		self.yinicial=None
		self.p=None
		self.resoluciones=self.config.resoluciones

		# Que sean datos de la mision
		#self.umbral=self.config.umbralA

		##leer todo desde la base de datos
		self.conectarBase()
		self.cargarDatos()
		if self.config.activarcamara:
			#activar
			self.camara = PiCamera()
			#menos consumo de memoria
			#self.camara.framerate = self.config.framerate
			#Activamos una resolucion por defecto
			self.camara.resolution = (1300, 975)
		pass

		##AGREGADO DETECCION ESTACA
		# initialize configuration settings (needs to be done just once)
		configDeteccion.initConfig()
		# config.setExclusionMargin(10)
		configDeteccion.setDebugMode(2)
		#configDeteccion.setMinAreaSize(350)
		configDeteccion.setMinAreaSize(self.config.procMinArea)
		##DEJAMOS QUE EL ALGORITMO GENERE INTERNAMENTE LAS MINIATURAS GANAMOS AL MENOS 2 S
		configDeteccion.setResize(self.config.procResize)
		##A BUENO... QUIEN HABIA COMENTADO ESTO??
		configDeteccion.setThreshold(self.config.umbralColores)
		configDeteccion.setSourceFolderName(self.config.dirfotos)

	def getTiempoIini(self):
		return self.misionact.getTiempoIni()

	def setPosInicial(self,x,y):
		self.xinicial=x
		self.yinicial=y
	
	def getPosInicial(self):
		return [self.xinicial,self.yinicial]

	def getConfig(self):
		return self.config

	def getUmbral(self):
		return self.misionact.getUmbral()

	def getDemora(self):
		return self.misionact.getDemora()

	def getAltitud(self):
		return self.misionact.getAltitud()

	def comenzarPreview(self):
		##AGREGADO DETECCION ESTACA
		# initialize log
		configDeteccion.initLog('dron')
		#activar
		if self.config.activarcamara:
			self.camara.start_preview()
		pass

	def sacarfoto(self):
		#activar
		if self.config.activarcamara:
			self.camara.start_preview()
			sleep(2)
			fecha=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
			#activar
			self.camara.capture(self.config.dirfotos+fecha+".jpg")
			self.camara.annotate_text = fecha
			print "Saquefoto"
			#activar
			self.camara.stop_preview()

	def altaRecorrido(self,padron,alt,vel,tipo,coords, esrel, xrel, yrel,cantpuntos,dist,umbral, solapamiento):
		print("altaRecorrido")
		r=Recorrido(str(padron),float(alt),float(vel),int(tipo),None, cantpuntos,dist,umbral, solapamiento, None, coords,self.config, self.persistencia, esrel, xrel, yrel)
		print("Fin Recorrido")
		self.recorridos.append(r)
		return r

	def borrarBD(self):
                self.persistencia.borrarBD()

        def borrarFotosBD(self, idMision):
                self.persistencia.borrarFotos(idMision)
	
	def getDatosRecorridos(self):
		res=[]
		for r in self.recorridos:
			res.append(r.getDataRecorrido())
		return res
	
	def getDatosRecorridoActual(self):
		return self.misionact.getDatosRecorrido()
		
	def seleccionarRecorrido(self,selrec):
		#buscar recorrido
		for r in self.recorridos:
			if r.getId()==selrec:
				self.recsel=r
				break
		
		if self.recsel!=None:
			[dataRec,dataPuntos,puntos]=self.recsel.getDataRecPuntos()
			self.puntossel=puntos
			
		return {"ok":True, "recorrido":dataRec,"puntos":dataPuntos}

	def conectarBase(self):
		self.persistencia.iniciarConexion()

	def iniciarMision(self,umbral,resolucion,bateriaini,demora, movfotos,altitud):
		# Ajustamos parametros de la mision
		#self.umbral = umbral
		if self.config.activarcamara:
			self.camara.resolution = self.resoluciones[resolucion]
		nuevaM=Mision(self.recsel, None, None, umbral, resolucion, bateriaini, -1, -1, -1, demora, movfotos, altitud, None, self.persistencia)
		self.misiones.append(nuevaM)
		self.misionact=nuevaM
		self.puntosact=self.puntossel
		self.contpunto=0
		self.p=None
		#self.tiempo=time()

		##RESPONDER SIN COORDENADAS
		return len(self.puntosact)
	
	def getSigCoordenada(self, movFotos=0):
		if self.contpunto<len(self.puntosact):
			# DECISIONES DINAMICAS
			#print "entrada"+str(self.contpunto)
			self.p = self.puntossel[self.contpunto]

			if self.getConfig().decisionestiemporeal:
				contsalto=self.p.saltarPuntos()
				if contsalto>0:
					self.contpunto+=contsalto
					if self.contpunto >= len(self.puntosact):
						#return None
						#el ultimo punto para volver a la base
						self.contpunto=len(self.puntosact)-1
					self.p = self.puntossel[self.contpunto]
					#print "salida:" + str(self.contpunto)

			self.contpunto += 1

			##AGREGADO FOTOS EN MOVIMIENTO
			coordsFotosMovimiento=[]
			#Si es una mision de mapping y hay que sacar fotos en movimiento y si el punto actual es de referencia
			#Si el siguiente no es el ultimo tambien
			if self.contpunto<len(self.puntosact)-1 and movFotos!=None and movFotos==1 and not self.misionact.esEstacas() and self.p.esReferencia():
				while (not self.puntossel[self.contpunto].esReferencia() and self.contpunto<len(self.puntosact)):
					#Le agrego el punto en si para poder llamarlo desde afuera
					coordsFotosMovimiento.append(self.puntossel[self.contpunto].convertirAbsolutas(self.xinicial,self.yinicial)+[self.puntossel[self.contpunto]])
					self.contpunto += 1

			##PASARLE DE ACA ALGO INDICANDO EL TIPO DE RECORRIDO EN EL QUE ESTA PARA QUE NO SAQUE FOTOS
			[xabs, yabs, habs, sacofoto, xrel, yrel] = self.p.convertirAbsolutas(self.xinicial,self.yinicial)
			##Si es mapping sacar fotos
			if not self.misionact.esEstacas():
				sacofoto=True
			return [xabs, yabs, habs, sacofoto, xrel, yrel,coordsFotosMovimiento]
		else:
			return None

	# A veces cuando se hace un land o se corta bruscamente la mision o se cambia par otra, se va a acceder a una foto que no existe.
	def getTotalFotosMision(self):
		if self.misionact!=None:
			return self.misionact.getTotalFotos()
		else:
			return 0

	def calificarFoto(self,i):
		#comentar esto
		#rutaFoto='2016-07-24-08-10-18.jpg'
		rutaFoto=self.misionact.getRutaFoto(i)
		regiones=-1
		score=-1
		if rutaFoto!=None:
			##DEJAMOS QUE EL ALGORITMO GENERE INTERNAMENTE LAS MINIATURAS GANAMOS AL MENOS 2 S
			#rutaFoto = "min2-" + self.misionact.getRutaFoto(i)
			resultado=modDeteccion.run(rutaFoto, 0)
			regiones=resultado.getRegionsN()
			score=resultado.getScore()
			self.misionact.setCalifFoto(i,regiones,score)
		tiempo_califfin=time()
		tiempo_calif=tiempo_califfin-self.getTiempoIini()
		return [regiones,score,tiempo_calif]

	def calificarMision(self,mision):

		for i in range (mision.getTotalFotos()):
			print("quiere calificar a:" + str(i))
			#[regiones, score, tiempocalif] = controlador.calificarFoto(i)
			# comentar esto
			# rutaFoto='2016-07-24-08-10-18.jpg'
			rutaFoto = mision.getRutaFoto(i)
			regiones = -1
			score = -1
			if rutaFoto != None:
				##DEJAMOS QUE EL ALGORITMO GENERE INTERNAMENTE LAS MINIATURAS GANAMOS AL MENOS 2 S
				# rutaFoto = "min2-" + self.misionact.getRutaFoto(i)
				print "el area minima esta en:"
				print configDeteccion.getMinAreaSize()

				resultado = modDeteccion.run(rutaFoto, 0)
				regiones = resultado.getRegionsN()
				score = resultado.getScore()
				mision.setCalifFoto(i, regiones, score)
			#return [regiones, score, tiempo_calif]
			print ('Califique foto:' + str(i) + "-regiones:" + str(regiones) + "-score:" + str(score))


	def sacarfotopalo(self, x,y,h, p=None):
		##PASARLE ACA EL PUNTO ACTUAL
		pCuestion = self.p
		# Si el segundo proceso me manda el punto
		if p != None:
			pCuestion = p
		##PASARLE ACA EL PUNTO ACTUAL
		[nombre, lat, lon, alt] = self.misionact.crearFoto(x, y, h, pCuestion)
		#[nombre,lat,lon,alt]=self.misionact.crearFoto(x,y,h,self.p)
		rutaFoto=self.config.dirfotos+nombre
		demora=self.getDemora()

		#Usar el puerto de video solo para resolucion inferiores a 3000x2000...
		#usarpuertovideo=self.misionact.getResolucion()<2
		if self.config.activarcamara:
			#Comentar esto es para ver lo que da nomas
			comando = "exiftool -GPSAltitudeRef='Above Sea Level' " \
					  "-GPSLongitudeRef=%s -GPSLongitude='%s' -GPSLatitudeRef=%s -GPSLatitude='%s' -GPSAltitude='%s' %s" % (
					  lon[0], lon[1], lat[0], lat[1], alt, rutaFoto)
			print comando

			#Georeferrenciacion de la foto
			self.camara.exif_tags['GPS.GPSAltitudeRef'] = '0'
			self.camara.exif_tags['GPS.GPSLongitudeRef'] = lon[0]
			self.camara.exif_tags['GPS.GPSLongitude'] = lon[1]
			self.camara.exif_tags['GPS.GPSLatitudeRef'] = lat[0]
			self.camara.exif_tags['GPS.GPSLatitude'] = lat[1]
			self.camara.exif_tags['GPS.GPSAltitude'] = alt

			#con capture la foto sale lenta
			if demora<0:
				self.camara.capture(rutaFoto)
			else:
				#foto mas rapida
				if demora>0:
					sleep(demora)
				#use_video_port=usarpuertovideo
				self.camara.capture_sequence([rutaFoto])

			#self.camara.annotate_text = nombre

			##Evitamos perder tiempo en generar la miniatura si es de mapping al menos
			#if self.misionact.esEstacas():
				#activar
				#Generar miniatura
			#	rutamin = self.config.dirfotos+"min-" + nombre
			#	i=Image.open(rutaFoto)
			#	i.thumbnail((200,150), Image.ANTIALIAS)
			#	i.save(rutamin, i.format)

			##DEJAMOS QUE EL ALGORITMO GENERE INTERNAMENTE LAS MINIATURAS GANAMOS AL MENOS 2 S
			##Agregar la otra minatura
			#rutamin2 = self.config.dirfotos + "min2-" + nombre
			#i = Image.open(rutaFoto)
			#i.thumbnail((1300, 1000), Image.ANTIALIAS)
			#i.save(rutamin2, i.format)

		#PRIMERA PRUEBA DE MANERA SECUENCIAL
		#[regiones,score]=self.calificarFoto(rutaFoto)
		#self.misionact.setFotoActual([regiones,score])

		##Despues que sacamos la foto y generamos la miniatura seteamos la nueva foto actual
		##Recien ahi comenzamos con el procesamiento si no la foto no esta sacada
		self.misionact.setFotoActual()

		#print "Saquefoto"

	def generarMiniatura(self,ruta):
		#Si no existe creamos una miniatura
		rutamin=self.getConfig().dirfotos+"min-"+ruta
		if not path.isfile(rutamin):
			rutaabs=self.getConfig().dirfotos+ruta
			i=Image.open(rutaabs)
			i.thumbnail((120,70), Image.ANTIALIAS)
			i.save(rutamin, i.format)
		return rutamin

	def getDatosMision(self):
		idm=0
		tipom=None
		distact=0
		distini=0
		idf=0
		xf=0		
		yf=0
		hf=0
		ruta=None
		if self.misionact!=None:
			[idm,tipom,distact,distini,idf,xf,yf,hf,ruta]=self.misionact.getDatosMision()
			if ruta!=None:
				ruta = "/imgchica/"+ str(ruta)
		return [idm,tipom,distact,distini,idf,xf,yf,hf,ruta]


	def getMision(self, mid):
		for m in self.misiones:
			if m.getId()==mid:
				return m

	def getMisiones(self):
		return self.misiones

	def getDataMisiones(self, mindex1, mindex2,tipo, cantai, calif, rangocstring,resize,amin):
		print "cantidad de estacas "+ str(cantai)
                self.imprimir("entrandoalafuncion")
		if calif!=None:
			print "rango colores" + rangocstring
			self.imprimir("calif distinto none")
			##configuracion del threshold de colores, el rangoc
			rangoc = []
			for e in rangocstring.split(";"):
				resp = tuple(map(int, e.replace("(", "").replace(")", "").split(",")))
				print resp
				rangoc += [resp]
			print rangoc
			configDeteccion.setThreshold(rangoc)
			configDeteccion.setMinAreaSize(amin)
			configDeteccion.setResize(resize)

		dataMisiones=[]
		for m in self.misiones:
                        self.imprimir("tres")
			if m.getTipo()==tipo and m.getId()>=mindex1 and m.getId()<=mindex2:
				#Si hay que calificarla la califico
				if calif!=None:
					self.calificarMision(m)
				dataMisiones.append(m.getDataMision(cantai,self.config.alturaestacavisible,self.config.alturafranja))
		#print dataMisiones
		return dataMisiones

	def setDistIniMision(self,dist_ini):
		if self.misionact!=None:
			self.misionact.setDistIni(dist_ini)
	def setDistActMision(self, dist_actual):
		if self.misionact!=None:
			self.misionact.setDistAct(dist_actual)	
			
	def terminarMision(self,bateriafin):
		#activar
		if self.config.activarcamara:
			self.camara.stop_preview()
		#pass
		# close current log
		configDeteccion.closeLog()
		tiempo = self.misionact.terminarMision(bateriafin)
		return tiempo

	def desconectarBase(self):
		self.persistencia.cerrarConexion()

	def cargarDatos(self):
		#self.persistencia.iniciarConexion()
		[self.recorridos,self.misiones]=self.persistencia.cargarMisionesRecorridos()
		pass
