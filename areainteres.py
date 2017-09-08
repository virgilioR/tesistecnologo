from punto import Punto
from math import sqrt

class AreaInteres():
	def __init__(self, tipo, idai=None, idr=None, x=None, y=None, h=None, xant=None, yant=None, dist=None, cantpuntos=None, umbral=0, persistencia=None):
		self.tipo = tipo
		self.persistencia=persistencia
		self.cantpuntos=cantpuntos
		# DECISIONES DINAMICAS
		self.fotosbuenas=0
		self.numbuenas=2

		print "estoy en AreaInteres"
		if idai!=None:
			self.idai=idai
		else:
			self.idai = persistencia.guardarAInteres(self.tipo, idr)
			self.puntos=[]
			#Si es estaca, creamos ademas el anterior
			if self.esEstaca():
				pAnterior=self.generarPunto(xant,yant,x,y,h,dist,umbral, True,True)
				self.puntos.append(pAnterior)
				self.actual=pAnterior
				if cantpuntos!=None and cantpuntos>=5:
					pAnterior = self.generarPunto(xant, yant, x, y, h, dist, umbral, True, False)
					self.puntos.append(pAnterior)

			print "antes de guardar el punto"
			#Para cualquier caso siempre creamos un punto.
			self.exacto=Punto(x,y,h,self,None,persistencia, True)
			self.puntos.append(self.exacto)

			if not self.esEstaca():
				self.actual=self.exacto


	def esEstaca(self):
		return self.tipo==0
	def esReferencia(self):
		return self.tipo==2

	def obtenerPunto(self,idp):
		i=0
		punto=None
		while (i<len(self.puntos)) and not self.puntos[i].sosVos(idp):
			i+=1
		if (i<len(self.puntos)):
			punto=self.puntos[i]
		return punto

	def setPuntos(self,puntos):
		self.puntos=puntos
		self.actual=puntos[0]
		self.exacto=self.actual
		self.cantpuntos=len(self.puntos)
		if self.esEstaca():
			#Cambiado el algoritmos ahora generamos 4 puntos
			if self.cantpuntos>=5:
				self.exacto=puntos[2]
			else:
				#con 3 o 4 puntos
				self.exacto=puntos[1]
		pass

	def getCantPuntos(self):
		return self.cantpuntos

	def calcularm(self,x0,y0,x1,y1):
		return (y1-y0)/(x1-x0)
	
	def encontrarPuntoRecta(self,m,d):
		return d/sqrt(1+(m**2))

	def getId(self):
		return self.idai
	def getX(self):
		return self.exacto.getX()
	def getY(self):
		return self.exacto.getY()

	#DECISIONES DINAMICAS
	def calificar(self,regiones,score):
		if regiones >= 1:
			self.fotosbuenas+=1
		return self.fotosbuenas>=self.numbuenas

	def saltarPuntos(self,idp):
		if self.fotosbuenas<self.numbuenas:
			return 0
		else:
			posicionpunto=0
			for i in range(len(self.puntos)):
				if self.puntos[i].getId()==idp:
					posicionpunto=i+1
					break
			#Reiniciar el contador par la otra mision
			self.fotosbuenas=0
			#print str(self.cantpuntos-posicionpunto)
			return self.cantpuntos-posicionpunto+1

	def generarPuntoSig(self,xsig,ysig,dist, umbral):
		#Si es estaca, creamos ademas el siguiente
		e=self.exacto
		if self.esEstaca():
			if self.cantpuntos != None and self.cantpuntos >= 4:
				pSiguiente=self.generarPunto(e.getX(),e.getY(),xsig,ysig,e.getH(),dist,umbral,False,True)
				self.puntos.append(pSiguiente)
			pSiguiente = self.generarPunto(e.getX(), e.getY(), xsig, ysig, e.getH(), dist, umbral, False, False)
			self.puntos.append(pSiguiente)
			#self.ultidp+=1

	def generarPunto(self,xant,yant,x,y,h,dist,umbral, esAnterior,esPrimero):
		x0=0
		y0=0
		x1=x-xant
		y1=y-yant
		#print str(xant)+str(yant)+","+str(x)+str(y)


		if (esAnterior):
			#Ajustes del umbral
			if esPrimero:
				dist=dist-umbral
			else:
				dist =dist + umbral
		else:
			# Ajustes del umbral
			dist = dist + umbral
		##El incremento por defecto
		inc = dist

		#print "inc antes:" + str(inc)


		##si y costante = recta vertical
		if (y0!=y1) and (x0!=x1):
			m=self.calcularm(x0,y0,x1,y1)
			inc=self.encontrarPuntoRecta(m,dist)
		##Si no es una recta con x constante, por defecto va a cambiar x
		varCambiar=x
		varRefAnt=xant
		##Si es recta con x constatne entonces cambiar y
		if (x0==x1):
			varCambiar=y
			varRefAnt=yant


		#print "inc antes:"+str(inc)
		if (esAnterior):
			#Ajustes del umbral
		#	if esPrimero:
		#		inc=inc-umbral
		#	else:
		#		inc = inc + umbral

			#CAMBIO PARA VER DE OBTENER FOTOS EN DOS PUNTOS MAS
			if ((varCambiar>varRefAnt) and esPrimero) or (not (varCambiar>varRefAnt) and not esPrimero):
				varF=varCambiar-inc
			else:
				varF=varCambiar+inc

		else:
			# Ajustes del umbral
			#inc = inc + umbral

			# CAMBIO PARA VER DE OBTENER FOTOS EN DOS PUNTOS MAS
			if ((varCambiar>varRefAnt) and not esPrimero) or (not (varCambiar>varRefAnt) and esPrimero):
				varF=varRefAnt+inc
			else:
				varF=varRefAnt-inc


		#print "umbral" + str(umbral) + "-anterior:" + str(esAnterior) + "-primero" + str(esPrimero) + "-varF" + str(varF)
		#print "inc despues:" + str(inc)
		if (x0==x1):
			yf=varF
			xf=x
		elif (y0==y1):
			xf=varF
			yf=y
		else:
			xf=varF
			yf=m*(xf-xant)+yant
		return Punto(xf,yf,h,self,None,self.persistencia)


	def getDataPuntos(self):
		resDat=[{"id":self.idai,"tipo":self.tipo,"x":self.exacto.x,"y":self.exacto.y,"h":self.exacto.h}]
		#for p in self.puntos:
		#	auxData=p.getDataPuntos()
		#	resDat.append(auxData)
			#resObj.append(aux["obj"])
		return [resDat,self.puntos]


	def ver(self):
		salida=str(self.idai)+"-"+str(self.tipo) +"\npuntos:"
		for ps in self.puntos:
			salida+=ps.ver()
		return salida
