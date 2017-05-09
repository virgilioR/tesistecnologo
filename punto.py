from math import cos, pi

class Punto():
	def __init__(self,x,y,h,ai,idp=None,persistencia=None, esExacto=None):
		self.x=x
		self.y=y
		self.h=h
		self.ai=ai

		if idp!=None:
			self.idp=idp
		else:
			self.idp=persistencia.guardarPunto(x,y,h,ai.getId(),esExacto)
		pass

	def getId(self):
		return self.idp
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getH(self):
		return self.h

	def getIdAi(self):
		return self.ai.getId()
	def esEstaca(self):
		return self.ai.esEstaca()
	def esReferencia(self):
		return self.ai.esReferencia()

	# DECISIONES DINAMICAS
	def calificarArea(self,regiones,score):
		return self.ai.calificar(regiones,score)
	def saltarPuntos(self):
		return self.ai.saltarPuntos(self.getId())

	def getNomParcialF(self):
		return str(self.ai.getId())+"-"+str(self.getId())
	def sosVos(self, id):
		return id==self.idp

	def getDataPuntos(self):
		return {"data":{"idp":self.idp,"x":self.x,"y":self.y,"h":self.h},"obj":self}	
	
	def convertirAbsolutas(self,xinicial,yinicial):
		#Radio de la "esfeera" de la Tierra	
		earth_radius = 6378137.0 
		#Coordinate offsets in radians
		#latitud
		xnuevo = self.x/earth_radius
		#longitud
		ynuevo = self.y/(earth_radius*cos(pi*xinicial/180))		
		
		#Nuevas posiciones en grados decimales
		xnuevo = xinicial + (xnuevo * 180/pi)
		ynuevo = yinicial + (ynuevo * 180/pi)	
		
		#conversion de coordenadas relativas a absolutas
		return [xnuevo, ynuevo, self.h, self.ai.esEstaca(),self.x,self.y]
	
	def ver(self):
		salida=str(self.idp)+":("+str(self.x) +","+ str(self.y)+")\n"
		return salida
