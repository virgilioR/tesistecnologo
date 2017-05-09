from datetime import datetime
from math import trunc

class Foto():
	def __init__(self, x,y,h,punto, idf=None, idm=None, fecha=None, ruta=None, rdetect=None, sdetect=None, persistencia=None, nomparcialf=None):
		self.x=x
		self.y=y
		self.h=h
		self.p=punto
		self.persistencia=persistencia
		if idf!=None:
			self.idf = idf
			self.ruta = ruta
			self.fecha = fecha
			self.rdetect=rdetect
			self.sdetect=sdetect
		else:
			self.fecha = datetime.now()
			nomparcialf2=self.p.getNomParcialF()
			self.ruta=nomparcialf+'-'+nomparcialf2+"-"+self.fecha.strftime('%Y-%m-%d')+".jpg"
			self.idf = persistencia.guardarFotos(self.x, self.y, self.h, self.fecha, self.ruta, idm, self.p.getId())
			self.rdetect = -1
			self.sdetect = -1
			#persistencia.actualizarFoto(self.idf,self.ruta)

	def getId(self):
		return self.idf

	def gradodecAEXIF(self,dd, camara=True):
		deg = trunc(dd)
		ddAbs = abs(dd)
		degAbs = abs(deg)
		mnt = trunc((ddAbs - degAbs) * 60)
		sec = round((ddAbs - degAbs - float(mnt) / 60) * 3600, 2)
		formato="%d %d %.2f"
		sen = 0
		if deg < 0:
			sen = 1

		if camara:
			sec=sec*100
			formato='%d/1,%d/1,%d/100'

		#SOLUCIONAR EN CONTROLADOR CAMARA LA PASADA DE DATOS
		return [sen, formato % (ddAbs, mnt, sec) ]

	def getXEXIF(self, camara=True):
		latRefs = ['N', 'S']
		[sen, latexif]=self.gradodecAEXIF(self.x, camara)
		return [latRefs[sen],latexif]

	def getYEXIF(self, camara=True):
		lonRefs = ['E', 'W']
		[sen, lonexif] = self.gradodecAEXIF(self.y, camara)
		return [lonRefs[sen], lonexif]

	def getHEXIF(self, camara=True):
		if camara:
			return '%d/100' % (self.h*100)
		else:
			return '%.2f' % self.h

	def getDatosEXIF(self, camara=True):
		return [self.getRuta(),self.getXEXIF(camara),self.getYEXIF(camara),self.getHEXIF(camara)]

	def getRuta(self):
		return self.ruta

	def getScore(self):
		return self.sdetect

	def getIdAi(self):
		return self.p.getIdAi()

	def getRegiones(self):
		return self.rdetect

	def setCalifFoto(self, regiones, score):
		# Cambio efecutado 22/01, si la calificacion mejora
		if score>=self.getScore() and regiones>=self.getRegiones() and not (self.getRegiones()>0 and regiones>6):
			self.rdetect=regiones
			self.sdetect=score
			self.persistencia.actualizarFoto(self.idf, score,regiones)
		else:
			regiones=self.getRegiones()
			score=self.getScore()
		#Salar si hay buena foto
		# DECISIONES DINAMICAS
		return self.p.calificarArea(regiones,score)

	def getDataFoto(self,alturaestaca,alturafranja):

		return {"idf":self.idf, "x":self.x, "y":self.y, "h":self.h, "ruta":self.getRuta(),
				"score":self.getScore(),"regiones":self.getRegiones(),"idp":self.p.getId(),"idai":self.getIdAi(),
				"altoPasto":self.getAltoPasto(alturaestaca,alturafranja)}

	def getAltoPasto(self, alturaestaca,alturafranja):
		regFoto=self.getRegiones()
		# el error aparece con un resultado -1
		#if regFoto > 6:
		#	return "Error"
		if regFoto <= 0:
			return 0
		else:
			# cuenta de disponibilidad
			return round(alturaestaca - 2 * regFoto * alturafranja,2)

	def getDatosFotoActual(self):
		return [self.idf, self.x, self.y, self.h, self.getRuta()]
