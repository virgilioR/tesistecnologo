#!/usr/bin/env python
# coding=utf-8
from areainteres import AreaInteres
from math import cos, pi, sqrt, tan, radians
from tspgenetico import TourManager, City, Population, GA

class Recorrido():
	#angulocamancho=None,angulocamlargo=None,overlapping=None
	def __init__(self, padron, alt, vel, tipo, idr=None, cantpuntos=None, dist=-1, umbral=0, solapamiento=0, areasinteres=None,coords=None,config=None,persistencia=None, esrel=None, xrel=None, yrel=None):
		self.idr=idr
		self.padron=padron
		self.alt=alt
		self.vel=vel
		self.tipo=tipo
		self.fotosxestaca=cantpuntos
		self.calculodist=dist
		self.umbral=umbral
		self.solapamiento=solapamiento

		if idr!=None:
			self.areasinteres=areasinteres
		else:
			#Se registra en la base de datos
			self.areasinteres = []
			# Si hay un umbral, mandar un porcentaje del mismo para generar los puntos internos
			self.umbral = umbral * 0.5

			# Si el overlapping llegara a venir nulo
			if self.solapamiento == None:
				self.solapamiento = config.overlapping
			self.idr = persistencia.guardarRecorrido(padron, alt, vel, tipo,self.fotosxestaca,self.calculodist,self.umbral, self.solapamiento)
			coordsguardar=self.procInicialCoords(coords,esrel,xrel,yrel)
			##DEPENDIENDO DEL TIPO DE RECORRIDO LLAMO GENERAR RECORRIDO ESTACAS O NO
			if self.esEstacas():
				self.genererRecorridoEstacas(coordsguardar, config.angulocamlargo, config.alturaestacavisible, cantpuntos, dist, self.umbral, persistencia)
			else:
				self.genererRecorridoMapping(coordsguardar, config.angulocamancho, config.angulocamlargo, self.solapamiento, self.umbral, persistencia)
			print("guarda4")
			#else:
			#self.genererRecorridoMapping(coordsguardar, dist, persistencia)

		if len(self.areasinteres)>0:
			self.actual = self.areasinteres[0]
		pass

	def esEstacas(self):
		return self.tipo==0

	#Acomodar, quedo mediofeito le pido a la primera Ai la cant de puntos con cuantos la cree
	def getCantPuntos(self):
		#return self.areasinteres[0].getCantPuntos()
		#ACOMODADO
		return self.fotosxestaca

	def getPadron(self):
		return self.padron

	##Antigua aplicación de un algoritmo de fuerza Bruta
	"""
	def elegircoords(self, resparciales):
	# print resparciales
		valores = resparciales[0]
		conjuntos = resparciales[1]
		conjmin = conjuntos[0]
		minim = valores[0]
		# print valores
		for i in range(1, len(valores)):
			# print i
			if valores[i] < minim:
				conjmin = conjuntos[i]
				minim = valores[i]
			#print "Minimo: "+str(minim)
		return (minim, conjmin)

		def ordenarcoords(self, inicio, conjunto):
			resparciales = ([], [])

			if len(conjunto) <= 0:
				#return (matriz[inicio][0], [inicio])
				return (0,[inicio])
			# ,[inicio])
			# recorrer conjunto
			for i in range(0, len(conjunto)):
				# distanciap=calculardistancia(inicio, punto)
				punto = conjunto[i]
				subconjunto = conjunto[:]
				# print i+1,inicio
				#distanciap = matriz[inicio][i + 1]
				distanciap=self.calcularDistancia(inicio, punto)
				# subconjunto=conjunto-punto
				#print "subc"+str(subconjunto)
				#print "i"+str(i)
				subconjunto.remove(punto)

				resauxiliares = self.ordenarcoords(punto, subconjunto)
				resparciales = (resparciales[0] + [distanciap + resauxiliares[0]], resparciales[1] + [[inicio] + resauxiliares[1]])

			# return min(resparciales)
			return self.elegircoords(resparciales)
			# return (min(resparciales[0]),resparciales[1])


	# matriz = [[0, 1, 15, 6], [2, 0, 7, 3], [9, 6, 0, 12], [10, 4, 8, 0]]  # print func(0,[1,2,3],matriz)
	# coordsguardar = [7, 8, 9, 10]
	# func(coordsguardar[0], coordsguardar[1:], matriz)
	"""

	def genererRecorridoMapping(self,coordsordenadas,angulocamancho,angulocamlargo, solapamiento, umbral, persistencia):
		dist=None
		posicioncamara = 0.2
		alturareal = self.alt - 0.5 - posicioncamara

		angulolargones = radians(float(90) - (angulocamlargo / float(2)))
		anguloanchones = radians(float(90) - (angulocamancho / float(2)))
		mitadfotolargo = round(alturareal / tan(angulolargones), 2)
		mitadfotoancho = round(alturareal / tan(anguloanchones), 2)

		##Agregado NUEVO (Había que agregar la parte del Overlapping)
		# Generar el incremento en funcion del overlapping
		mitadfotolargo = (mitadfotolargo * 2) * (1 - solapamiento)
		mitadfotoancho = (mitadfotoancho * 2) * (1 - solapamiento)

		print "ANCHO mitad de la foto es" + str(mitadfotoancho)
		print "LARGO mitad de la foto es" + str(mitadfotolargo)
		##AGREGADO NUEVO

		##Calcular la distancia en un sentido
		#anchoTotal=self.calcularDistancia(coordsordenadas[0],coordsordenadas[1])
		#largoTotal=self.calcularDistancia(coordsordenadas[1],coordsordenadas[2])

		##En que dirección nos vamos a mover
		##La primera coordenada solo se usa como referencia y peude ser para colocar bien en lugar el dron antes de arrancar.
		[xdes, ydes, hdes, tipodes] = coordsordenadas[0]

		#De la primera coordenada se saca la esquina "inferior izquierdo": lat y lon
		[x0,y0,h0,tipo0]=coordsordenadas[1]
		#De la segunda coordenada se saca el limite "derecho": el limite en longitud
		[x1, y1, h1, tipo1] = coordsordenadas[2]
		#De la tercera se saca el límite en latitud o "superior"
		[x2, y2, h2, tipo2] = coordsordenadas[3]
		#coordsres = []
		print "coordenadas 0, 1, 2,3"
		print coordsordenadas[0]
		print coordsordenadas[1]
		print coordsordenadas[2]
		print coordsordenadas[3]
		print "VEmos que se genera en el recorrido *********************"

		varx = x0
		vary = y0
		inix=x0
		iniy=y0
		topex = x1
		topey = y1

		#Siempre nos vamos a mover en el eje X
		#if x0==x1:
			#Nos movemos en eje y
			##TOPE X HAY QUE DEFINIRLO ACA CON LA OTRA COORDENADA
		topex=x2
		topes=[topex,topey]
		inis = [inix, iniy]
		vars = [varx, vary]
		ix=0
		iy=1
		#elif y0==y1:
			# en x
		#	topey = y2
		#	topes = [topey, topex]
		#	inis = [iniy, inix]
		#	vars = [vary, varx]
		#	ix = 1
		#	iy = 0

		while vars[0]+mitadfotoancho<topes[0]:
			vars[0]=round(vars[0]+mitadfotoancho,2)

			##AGREGADO FOTOS EN MOVIMIENTO
			#Agrego una estaca por si el vuelo es en movimiento
			vars[1] = round(vars[1] + mitadfotolargo, 2)
			ai = AreaInteres(2, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral, persistencia)
			print "estaca: "+ str(vars[ix]) + "," + str(vars[iy])
			self.areasinteres.append(ai)

			while vars[1]+mitadfotolargo<topes[1]:
				vars[1]=round(vars[1]+mitadfotolargo,2)
				if vars[1]+mitadfotolargo<topes[1]:
					ai = AreaInteres(1, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral, persistencia)
					print str(vars[ix]) + "," + str(vars[iy])
					self.areasinteres.append(ai)

			##AGREGADO FOTOS EN MOVIMIENTO
			ai = AreaInteres(2, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral,persistencia)
			print "estaca: "+str(vars[ix]) + "," + str(vars[iy])
			self.areasinteres.append(ai)

			# Recorrimos toda la linea ahora avanzamos una
			if vars[0]+mitadfotoancho<topes[0]:
				vars[0] = round(vars[0]+ mitadfotoancho,2)
				##AGREGADO FOTOS EN MOVIMIENTO
				ai = AreaInteres(2, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral, persistencia)
				self.areasinteres.append(ai)
				print "estaca: "+str(vars[ix]) + "," + str(vars[iy])

				##Recorremos toda la lina hacia atras ahora
				while vars[1]-mitadfotolargo > inis[1]:
					vars[1]=round(vars[1]-mitadfotolargo,2)
					if vars[1] - mitadfotolargo > inis[1]:
						ai = AreaInteres(1, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral, persistencia)
						print str(vars[ix]) + "," + str(vars[iy])
						self.areasinteres.append(ai)

				##AGREGADO FOTOS EN MOVIMIENTO
				ai = AreaInteres(2, None, self.idr, vars[ix], vars[iy], self.alt, 0, 0, dist, None, umbral,persistencia)
				print "estaca: "+ str(vars[ix]) + "," + str(vars[iy])
				self.areasinteres.append(ai)
				##Me salgo para afuera para volver a generar bien
				vars[1] = round(vars[1] - mitadfotolargo, 2)

		ai = AreaInteres(1, None, self.idr, 0, 0, self.alt, 0, 0, dist, None, umbral, persistencia)
		print "0,0"
		self.areasinteres.append(ai)

		print "Termina el recorrido *********************"

		#while vary+mitadfotoancho<topey:
		#		while varx+mitadfotolargo<topex:
		#			varx+=mitadfotolargo
		#coordsres.append([varx, vary])
		#Recorrimos toda la linea ahora avanzamos una
		#		vary+=mitadfotoancho
		#coordsres.append([varx, vary])
		##Recorremos toda la lina hacia atras ahora
		#		while varx-mitadfotolargo >= inix:
		#			varx-=mitadfotolargo
		#coordsres.append([varx, vary])

		#xactual=0
		#while (anchoRec<anchoTotal):
		#	anchoRec+mitadfoto

	def imprimir(self,coordactual,minc,distmin):
		[x, y, h, tipo] = coordactual
		[x2, y2, h2, tipo2] = minc
		if x==10.43 and y==-18.77:
			print "distmin: "+str(distmin)+" el comparado:"+str(minc)

	def genererRecorridoEstacas(self, coordsguardar, angulocamlargo, alturaestacavisible, cantpuntos, calculodist, umbral, persistencia):
		#def genererRecorridoEstacas(self,coordsguardar,dist,cantpuntos, persistencia):
		#Si hay que hacer la cuenta la hacemos
		
		if calculodist==0:
			##Definición de la distancia adecuado de la estaca donde tomar la foto
			alfa = radians(float(90) - (angulocamlargo / float(2)))
			margenestaca=round(alturaestacavisible / tan(alfa), 2)
			#El dron se posiciona en cada foto casi en la altura solicitada
			alturareal=self.alt-0.5
			#Errores de posicionamiento, umbrales definidos, LA POSicion de la camara
			#errores=0.5
			#Cambio efecutado 22/01
			errores = 0
			#Hay una inclinacion de la cámara al ir rapido
			#posicioncamara=0.3
			posicioncamara = 0.2
			##No quedar tan arriba de la estaca
			#dist=round(self.alt/tan(alfa)-0.95*margenestaca,2)
			dist = round(alturareal / tan(alfa) - margenestaca-posicioncamara-errores, 2)
		else:
			dist=calculodist

		##Creación de áreas y conversion de coordenadas
		##APLICAR UN DIJKSTRA PARA ORDENAMIENTO
		xant = 0
		yant = 0
		coordactual = coordsguardar[0]
		# Crear la primera Area

		[x, y, h, tipo] = coordactual
		#coordsordenadas=[]

		# Cambiamos el SEUDO disjkstra y el Held-Karp para camino hamiltoneano mas corto por un GENETICO
		#descomentar esto
		coordsordenadas = self.ordenarcoords(coordsguardar)
		#print coordsordenadas
		print "ordena"
		# PEQUEÑO HACK PORQUE DEMORA MUCHO
		# coordsordenadas = [[0, 0, 5.0, 1], [6.16, 10.23, 5.0, 0], [15.5, 6.49, 5.0, 0], [13.98, -4.78, 5.0, 0],
		# [-1.31, -15.49, 5.0, 0], [10.43, -18.77, 5.0, 0], [22.07, -21.72, 5.0, 0],
		# [27.14, -10.34, 5.0, 0], [41.06, -11.9, 5.0, 0], [45.68, 1.35, 5.0, 0], [32.27, 4.23, 5.0, 0]]

		#coordsordenadas=[[0, 0, 5.0, 1], [-1.31, -15.49, 5.0, 0], [10.43, -18.77, 5.0, 0], [22.07, -21.72, 5.0, 0],
		# [27.14, -10.34, 5.0, 0], [41.06, -11.9, 5.0, 0], [45.68, 1.35, 5.0, 0], [32.27, 4.23, 5.0, 0], [13.98, -4.78, 5.0, 0],
		# [15.5, 6.49, 5.0, 0], [6.16, 10.23, 5.0, 0]]

		ai=None
		#Completar el pedazo de la dada de alta de areas de interes
		for coordactual in coordsordenadas:
			print "estoy en el for"
			##Crear la nueva area
			[x, y, h, tipo] = coordactual
			auxai = ai
			print "antes de ir a AreaInteres"
			ai = AreaInteres(tipo, None, self.idr, x, y, h, xant, yant, dist, cantpuntos, umbral, persistencia)
			print "vuelvo de AreaInteres"
			self.areasinteres.append(ai)
			xant = x
			yant = y
			if auxai!=None:
				auxai.generarPuntoSig(ai.getX(), ai.getY(), dist, umbral)
		##AGREGAMOS SIEMPRE EL PUNTO COMUN DE RETORNO 0,0
		auxai = ai
		ai = AreaInteres(1, None, self.idr, 0, 0, h, xant, yant, dist,cantpuntos, umbral, persistencia)
		self.areasinteres.append(ai)
		auxai.generarPuntoSig(ai.getX(), ai.getY(), dist, umbral)

	def getAtribCoords(self,coords,i):
		c = coords[i]
		x = float(c["x"])
		y = float(c["y"])
		h = float(c["h"])
		tipo = int(c["tipo"])
		return [x,y,h,tipo]

	def ordenarcoords(self, cordsguardar):

		tourmanager = TourManager()
		print "cuantas ciudades destino:"
		#por mas que se crea una objeto nuevo, los hijos siguen pegados
		del tourmanager.destinationCities[:]
		print tourmanager.destinationCities
		for e in cordsguardar:
			# Create and add our cities
			city = City(e[0], e[1], e[2], e[3])
			tourmanager.addCity(city)

		# Initialize population
		pop = Population(tourmanager, 50, True);
		#print "Initial distance: " + str(pop.getFittest().getDistance())

		# Evolve population for 50 generations
		ga = GA(tourmanager)
		pop = ga.evolvePopulation(pop)
		for i in range(0, 1000):
			pop = ga.evolvePopulation(pop)

		# Print final results
		#print "Finished"
		print "Distancia final:" + str(pop.getFittest().getDistance())
		#print "Solution:"
		# print pop.getFittest()
		solbruto = pop.getFittest().damela()

		# print "solucion en bruto"
		# print solbruto
		posini = 0
		for i in range(0, len(solbruto)):
			aux = solbruto[i]
			posini = i
			if aux[0] == 0 and aux[1] == 0:
				break;
		fin = solbruto[:posini]
		ini = solbruto[posini:]
		print "Solucion posta"

		solfinal = ini + fin
		print solfinal
		print len(solfinal)
		return solfinal


	def procInicialCoords(self, coords, esrel, xrel, yrel):
		##LA PRIMERA INGRESADA ES EL PUNTO INCIAL PRIMERO
		##SE APROVECHA A HACER CONVERSION DE COORDENADAS
		[x, y, h, tipo]=self.getAtribCoords(coords,0)
		radio = 6378137.0
		coordsguardar = []
		xabs0 = 0
		yabs0 = 0
		if esrel is False:
			xabs0 = x - ((xrel * 180) / (radio * pi))
			ypreabs1 = yrel / (radio * cos(pi * xabs0 / 180))
			yabs0 = y - (ypreabs1 * 180 / pi)
			coordsguardar.append([xrel, yrel, h, tipo])
		else:
			# print "enro aca"
			coordsguardar.append([x, y, h, tipo])

		print "Vamo a ver que coordenada da*****************"
		print coordsguardar[0]
		if esrel is False:
			for i in range(1, len(coords)):
				[x, y, h, tipo] = self.getAtribCoords(coords, i)
				xpreabs2 = (x - xabs0) * pi / 180
				ypreabs2 = (y - yabs0) * pi / 180
				xrel2 = round(xpreabs2 * radio,2)
				yrel2 = round(ypreabs2 * (radio * cos(pi * xabs0 / 180)),2)
				print [xrel2, yrel2, h, tipo]
				coordsguardar.append([xrel2, yrel2, h, tipo])
		else:
			for i in range(1, len(coords)):
				[x, y, h, tipo] = self.getAtribCoords(coords, i)
				#print [x, y, h, tipo]
				coordsguardar.append([x, y, h, tipo])
		print "FIN Vamo a ver que coordenada da*****************"
		print coordsguardar
		return coordsguardar

	def getId(self):
		return self.idr

	def getTipo(self):
		return self.tipo

	def getDataRecorrido(self):
		return {"idr":self.idr,"padron":self.padron,"vel":self.vel,"alt":self.alt,"tipo":self.tipo,
				"cantpuntos":self.getCantPuntos(),"calculodist":self.calculodist, "umbral":self.umbral}

	def getDataPuntos(self):
		resDat=[]
		resObj=[]
		for ai in self.areasinteres:
			[auxDat,auxObj]=ai.getDataPuntos()
			resDat+=auxDat
			resObj+=auxObj
		return [resDat,resObj]

	def getDataRecPuntos(self):
		return [self.getDataRecorrido()]+self.getDataPuntos()

	def calcularDistancia(self, c1, c2):
		[x1, y1, h1, t1] = c1
		[x2, y2, h2, t2] = c2
		return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

	def obtenerPunto(self,idp):
		i=0
		punto=self.areasinteres[i].obtenerPunto(idp)
		while (i<len(self.areasinteres)) and punto==None:
			punto = self.areasinteres[i].obtenerPunto(idp)
			i+=1
		return punto

	def ver(self):
		salida=str(self.idr)+"-"+str(self.padron)+"-"+str(self.alt)+"-"+str(self.vel)+"-"+str(self.tipo)+"\nareas:"
		for ai in self.areasinteres:
			salida+=ai.ver()
		#salida+="\n"
		return salida
