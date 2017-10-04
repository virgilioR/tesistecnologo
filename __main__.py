#!/usr/bin/env python
# coding=utf-8
import shlex, subprocess
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from Queue import Queue
from os import system
from flask import Flask, jsonify, Response, request, send_file, render_template, send_from_directory
import json
import os
from commands import *
import socket
from threading import Thread, Event, Lock
from datetime import datetime
import dateutil.parser
from math import pi,cos, sqrt,sin, atan2, radians
from controladorcamara import ControladorCamara
#from config import Config
from time import time,sleep

import gpxpy 
import gpxpy.gpx

vehicle = None
xlimizq=0
xlimder=0
salir=False
conectado=False
listeners_location = []
controlador=None
#configuracion=None
fechaSeteada = False

def imprimir(texto):
	print (texto) 
	with open("/tmp/torreap", "a") as myfile:
		myfile.write(str(texto)+ "\n")

# Allow us to reuse sockets after the are bound.
# http://stackoverflow.com/questions/25535975/release-python-flask-port-when-script-is-terminated
socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)
socket.socket.bind = my_socket_bind

def sse_encode(obj, id=None):
    return "data: %s\n\n" % json.dumps(obj)

# Es un microfram work de python
app = Flask(__name__)

@app.route("/")
def home():
	global controlador
	global fechaSeteada
	cadenaconexion=controlador.getConfig().cadenaconexion
	print cadenaconexion
	return render_template('index.html', cadenaconexion=cadenaconexion, fechaseteada=fechaSeteada, branding=False)

@app.route("/demo")
def demo():
	return render_template('demo.html', branding=False)

@app.route("/api/cambiarfecha", methods=['POST'])
def cambiarfecha():
	global fechaSeteada
	try:
		fechastr=str(request.json['fecha'])
		#fecha=datetime.da(request.json['fecha'])
		print fechastr
		print "seteamos la fecha en el sistema"
		system("date -s '"+fechastr+"'")
		fechaSeteada = True
		return jsonify(ok=True)
	except Exception as e:
		imprimir(str(e))
		return jsonify(ok=False)

@app.route("/administracion",methods=['GET'])
def administracion():
	return render_template('administracion.html', branding=False)

@app.route("/api/restartweb",methods=['GET', 'POST'])
def api_restartweb():
        p = subprocess.call(shlex.split('supervisorctl restart torreap'))
        return p

@app.route("/api/restartrasp",methods=['GET', 'POST'])
def api_restartrasp():
        reboot = subprocess.call(shlex.split('shutdown -r -t 1'))
        return reboot

@app.route("/api/shutdownrasp",methods=['GET', 'POST'])
def api_shutdownrasp():
        shutd = subprocess.call(shlex.split('shutdown -h 1'))
        return shutd

@app.route("/api/consolelog",methods=['GET','POST'])
def api_consolelog():
        #retorno = subprocess.check_output(shlex.split('tail /var/log/supervisor/supervisor.err.log'))
        retorno = ""
        with open("/tmp/torreap") as myfile:
		for line in myfile:
                        retorno = retorno + line + "<br>"
        return retorno

@app.route("/gestionmision")
def gestionmision():
	return render_template('gestionmision.html', branding=False)

@app.route("/listadofotos", methods=['GET','POST'])
def listadofotos():
	global controlador
	mision=None
	recorrido=None
	try:
		mindex = request.form.get('mision')
		calif = request.form.get('calif')
		print "calif: "+str(calif)
		if mindex!=None:
			#print mindex
			mision=controlador.getMisiones()[int(mindex)]
			print mision.getId()
			if calif!=None:
				controlador.calificarMision(mision)
			recorrido = mision.getDatosRecorrido()
		return render_template('listadofotos.html', misiones=controlador.getMisiones(), msel=mision, recorrido=recorrido)
	except Exception as e:
		imprimir(str(e))
		return jsonify(ok=False)

@app.route("/listadomisiones", methods=['GET','POST'])
def listadomisiones():
        imprimir("entrandoalafuncion")
	global controlador
	dataMisiones=[]
	tipoint=0
	cantaiint=0
	resizeint=0.6
	aminint=6
	try:
		mindex1 = request.form.get('mision1')
		mindex2 = request.form.get('mision2')
		tipo = request.form.get('tipo')
		calif = request.form.get('calif')
		#cantai = request.form.get('cantai')
		rangoc = request.form.get('rangoc')
		amin = request.form.get('amin')
		#resize = request.form.get('resize')
		if mindex1!=None and mindex2!=None:
			imprimir("onomeatropella")
			mindex1=int(mindex1)
			print ("2")
			mindex2=int(mindex2)
			print ("3")
			tipoint=1
			print ("4")
			cantaiint=0
			#resizeint=float(resize)
			resizeint=0
			#aminint=int(amin)
			aminint=0
			#print mindex
			imprimir("antesdedatamisiones")
			dataMisiones=controlador.getDataMisiones(mindex1, mindex2,tipoint, cantaiint, calif,rangoc,resizeint,aminint)
		return render_template('listadomisiones.html', misiones=controlador.getMisiones(),
							   dataMisiones=dataMisiones, msel1=mindex1, msel2=mindex2,tipo=tipoint,
							   cantai=cantaiint, resize=resizeint, amin=aminint)
	except Exception as e:
		imprimir(str(e))
		return jsonify(ok=False)


@app.route('/grande/<ruta>')
def get_image_g(ruta):
	global controlador
	#try:
	#rutaabs="/var/www/html/"+ruta

	rutamin=controlador.getConfig().dirfotos+ruta
	#i=Image.open(rutaabs)
	#i.thumbnail((200,150), Image.ANTIALIAS)
	#i.save(rutamin, i.format)

	return send_file(rutamin, mimetype='image/jpeg')

@app.route('/imgchica/<ruta>')
def get_image(ruta):
	global controlador
	#try:
	#rutaabs="/var/www/html/"+ruta
	#rutamin=controlador.getConfig().dirfotos+"min-"+ruta
	try:
		#descomentar
		rutamin = controlador.generarMiniatura(ruta)
		#pequeño hack para probar
		#comentar
		#rutamin = controlador.generarMiniatura("2016-07-24-08-10-18.jpg")
		#i=Image.open(rutaabs)
		#i.thumbnail((200,150), Image.ANTIALIAS)
		#i.save(rutamin, i.format)
		return send_file(rutamin, mimetype='image/jpeg')
	except Exception as e:
		imprimir(str(e))

def tomarfoto():
	global controlador
	controlador.sacarfoto()
	return True

@app.route("/api/unafoto", methods=['POST', 'PUT'])
def unafoto():
    if request.method == 'POST' or request.method == 'PUT':
        try:
	    res=tomarfoto()    
	    return jsonify(ok=res)
        except Exception as e:
            imprimir(str(e))
            return jsonify(ok=False)


@app.route("/api/datosrecorrido", methods=['POST', 'PUT'])
def selrec():
	#global coordenadas
	global controlador
	if request.method == 'POST' or request.method == 'PUT':
		try:
			selrec=float(request.json['recorrido'])
			#umbral = float(request.json['umbral'])
			#resolucion = int(request.json['resolucion'])
			datosRecorrido=controlador.seleccionarRecorrido(selrec)
			return jsonify(datosRecorrido)
		except Exception as e:
			imprimir(str(e))
			return jsonify(ok=False)

@app.route("/api/guardarrecorrido", methods=['POST', 'PUT'])
def guardarrec():
	global controlador
	if request.method == 'POST' or request.method == 'PUT':
		try:
			padron=str(request.json['padron'])
			alt=float(request.json['alt'])
			vel=float(request.json['vel'])
			tipo=int(request.json['tipo'])
#			cantpuntos = int(request.json['cantpuntos'])
			cantpuntos = 0
			coordaux=request.json['coordenadas']
			relativas=bool(request.json['rel'])
			xrel=float(request.json['xrel'])
			yrel=float(request.json['yrel'])
			#dist = float(request.json['dist'])
			dist = 0
			umbral = float(request.json['umbral'])
			solapamiento = float(request.json['sol'])
			#coordenadas.append([x,y,h])
			r=controlador.altaRecorrido(padron,alt,vel,tipo,coordaux,relativas,xrel,yrel,cantpuntos,dist,umbral,solapamiento)
			
			imprimir(r.ver())
			return jsonify(ok=True)
		except Exception as e:
			imprimir(str(e))
			return jsonify(ok=False)

def calcular_distancias(x1,y1,x2,y2):
	#return ceil(sqrt((x1-x2)**2+(y1-y2)**2)* 1.113195e5*100)/100

	# http://www.movable-type.co.uk/scripts/latlong.html
	# http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
	# https://es.wikipedia.org/wiki/F%C3%B3rmula_del_haversine
	R = 6378137.0
	dLat = radians(x2 - x1)
	dLon = radians(y2 - y1)
	lat1 = radians(x1)
	lat2 = radians(x2)

	a = sin(dLat / 2) * sin(dLat / 2) + sin(dLon / 2) * sin(dLon / 2) * cos(lat1) * cos(lat2);
	c = 2 * atan2(sqrt(a), sqrt(1 - a));
	d = R * c;
	return d
	
def resolverEqDist(x1,x0,y0,m):
	return sqrt((m/1.113195e5)**2 - (x1-x0)**2) + y0	

def resolverEqDist2(x1,x0,y1,m):
	return y1 - sqrt((m/1.113195e5)**2 - (x1-x0)**2)

def armar(estado):
	global vehicle
	#global xinicial
	#global yinicial
	global controlador
	#vehicle.parameters['ARMING_CHECK']=0
	try:
		#imprimir(vehicle.parameters['BRD_SAFETYENABLE'])

		if (vehicle.armed==False):
			imprimir("Chequeo basico de pre armado")
			# Don't try to arm until autopilot is ready
		    #while not vehicle.is_armable:
			if vehicle.mode.name == "INITIALISING":
				imprimir("Waiting for vehicle to initialise")
				sleep(1)
			while vehicle.gps_0.fix_type < 2:
				imprimir("Waiting for GPS...:", vehicle.gps_0.fix_type)
				sleep(1)

		imprimir("Pasando a modo GUIDED")
		vehicle.mode = VehicleMode("GUIDED")
		vehicle.flush()

		vehicle.armed = estado
		vehicle.flush()

		#Hay que esperar a que el vehiculo se arme antes de despegar
		while vehicle.armed!=estado and not salir:
			imprimir("Esperando para que se arme/desarme..." + str(estado) + "-"+vehicle.mode.name)
			sleep(2)

		#Luego de armar nos quedamos con la posicion original
		imprimir("LA POSICION INICIAL DE DONDE SALE ES" + str(vehicle.location.global_relative_frame.lat) + "," + str(vehicle.location.global_relative_frame.lon))
		controlador.setPosInicial(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
		return True

	except Exception as e:
		imprimir(str(e))
		return False


@app.route("/api/arm", methods=['POST', 'PUT'])
def api_armar():
    if request.method == 'POST' or request.method == 'PUT':
	estado=bool(int(request.json['arm']))
        res=armar(estado)
	return jsonify(ok=res)

def despegar(altura,velocidad):
	global vehicle
	#global xinicial
	#global yinicial
	global controlador
	global xlimizq
	global xlimder
	#global configuracion
	try:
		res=armar(1)
		if res:
			##TOMAR POSICION INICIAL
			earth_radius = 6378137.0 #Radius of "spherical" earth

			#El offset de la latitud de ir hacia 2 metros en radianes
			configuracion=controlador.getConfig()
			dLat = configuracion.topeMetros/earth_radius

			##Agregado para el demo
			#Limites izquierdos y derechos de la posicion en grados decimales
			[xinicial,yinicial]=controlador.getPosInicial()
			xlimder= xinicial - (dLat * 180/pi)
			xlimizq= xinicial + (dLat * 180/pi)

			imprimir("Despeque! ")
			imprimir("Le ponemos la velocidad groundspeed a "+str(velocidad) + "m/s" + str(altura) + str(salir))
			vehicle.groundspeed=velocidad
			vehicle.simple_takeoff(altura) # Take off to target altitude

			#SALIR PARA ATRAS SI NO ESTAMOS EN GUIDED
			while vehicle.mode.name=="GUIDED" and not salir:
				imprimir(" Altura: " + str(vehicle.location.global_relative_frame.alt) )
				#Break and return from function just below target altitude.
				if vehicle.location.global_relative_frame.alt>=altura*0.95:
					imprimir("Altura prevista Alcanzada")
					imprimir("***********posicion en el AIRE es*********" + str(vehicle.location.global_relative_frame.lat) + "," + str(vehicle.location.global_relative_frame.lon))
					break
				sleep(1)
		return res
	except Exception as e:
		imprimir(str(e))
		return False

def aterrizar():
	#Si hace RTL dejarlo
	if vehicle.mode.name!="RTL":
		vehicle.mode = VehicleMode('LAND')
		vehicle.flush()


def irHasta(origen,destino,sacoFoto):
	#Variable para tener en cuenta cuando sacar la foto del palo y cuando no
	#global configuracion
	global controlador
	xactual=origen.lat
	yactual=origen.lon
	x=destino.lat
	y=destino.lon
	#configuracion=controlador.getConfig()
	##CALCULAR DISTANCIAS PARA IR AL LUGAR
	dist_ini=calcular_distancias(xactual,yactual,x,y)
	controlador.setDistIniMision(dist_ini)
	tinicial=controlador.getTiempoIini()
	#tinicial=time()

	#if vehicle.mode.name!="GUIDED": break;
	#imprimir ("PUNTO DE PARTIDA: " + str(xactual) + "," + str(yactual))
	#imprimir ("Posicion global INICIAL: lat:" + str(xactual) + ", lon:" + str(yactual) + "--- inicial:"+str(dist_ini) + ", 1%:" + str(dist_ini * 0.01))
	#imprimir ("LLendo al punto:" + str(x) + "," + str(y))

	vehicle.simple_goto(destino)
	
	while vehicle.mode.name=="GUIDED" and not salir: #Stop action if we are no longer in guided mode.
		xactual=vehicle.location.global_relative_frame.lat
		yactual=vehicle.location.global_relative_frame.lon
		hactual=vehicle.location.global_relative_frame.alt
		dist_actual=calcular_distancias(xactual,yactual,x,y)
		controlador.setDistActMision(dist_actual)
		imprimir ("Posicion global actual: lat:" + str(xactual) + " lon:" + str(yactual) + " dist:" + str(dist_actual) + " inicial:"+str(dist_ini * 0.01))
		#if margen==None:
		#margen=configuracion.umbralA
		margen=controlador.getUmbral()
		#demora=controlador.getDemora()
		#print margen
		if (dist_actual<=dist_ini * 0.01) or (dist_actual<margen) :
			#imprimir ("Se alcanzo la posicion")
			#imprimir("LLEGO")
			tactual = time()
			imprimir("LLEGÓ AL PUNTO A: "+str(round(tactual-tinicial,2))+"s")
			#descomentar
			if (sacoFoto):
				mxCamara.acquire()
				#imprimir ("EL PRINCIPAL quiere sacar una foto nueva")
				#if demora>0:
				#	sleep(demora)

				#Sacar Fotos
				hglobal=vehicle.location.global_frame.alt
				imprimir("Alturas de la foto relativa: "+ str(hactual) +" - absoluta: "+ str(hglobal))
				hguardar=hactual
				if controlador.getAltitud()>=1:
					hguardar=hglobal

				controlador.sacarfotopalo(xactual,yactual,hguardar)
				tactual = time()
				imprimir("SACO FOTO A: "+str(round(tactual-tinicial,2))+"s")
				mxCamara.release()
				#pass
			#comentar
			#sleep(2)
			#imprimir("bateria:"+str(vehicle.battery.level)+"%-satelites:"+str(vehicle.gps_0))
			#imprimir("Despues de Sleep estoy en:" + str(xactual) + "," + str(yactual))
			#imprimir("SIGO")
			break
		sleep(0.3)

	#Comentar esto
	#if segunda==None:
	#	imprimir("***ALINEACION CON EL PUNTO***")
	#	irHasta(origen,destino,sacoFoto,0.3,True)

@app.route("/api/mover", methods=['POST', 'PUT'])
def api_mover():
	global controlador
	direccion=float(request.form['direccion'])
	imprimir("mover "+str(direccion))
	posactual=vehicle.location.global_relative_frame		
	x0=posactual.lat
	y0=posactual.lon
	y1=y0
	x1=x0
	configuracion=controlador.getConfig()
	metrosAMover=configuracion.movMetros
	#controlar si nos vamos FUERA de los limites
	if direccion<0 :
		#IR HACIA la izquierda
		distrest=calcular_distancias(xlimizq,y0,x1,y1)		
		if metrosAMover>distrest:
			#metrosAMover=distrest
			x1=xlimizq
		else:		
			x1=resolverEqDist(y1,y0,x0,metrosAMover)
		#imprimir(str(x1) + str(xlimizq))
		if x1>xlimizq:
			imprimir("Salimos afuera de los límites")
			x1=x0
	elif direccion>0 :
		#imprimir("hola")
		#IR HACIA la derecha
		distrest=calcular_distancias(xlimder,y0,x1,y1)		
		if metrosAMover>distrest:
			x1=xlimder
		else:
			x1=resolverEqDist2(y0,y1,x0,metrosAMover)
		
		if x1<xlimder:
			imprimir("Salimos afuera de los límites")
			imprimir(str(x1) + str(xlimder))
			x1=x0
	#y si es cero como frena?	
	#if x0=x1 frenarlo como?

	#if vehicle.mode.name!="GUIDED": break;
	imprimir ("PUNTO DE PARTIDA: " + str(x0) + "," + str(y0))
	imprimir ("Yendo hacia un punto ..." + str(x1) + "," + str(y1))
	destino=LocationGlobalRelative(x1, y1, posactual.alt)
	vehicle.simple_goto(destino)
	return jsonify(ok=True)


@app.route("/api/flotar", methods=['POST', 'PUT'])
def api_flotar():
	global controlador
	if request.method == 'POST' or request.method == 'PUT':
		altura=float(request.json['altura'])
		velocidad=float(request.json['velocidad'])
		res=despegar(altura,velocidad)
		##Lo hacemos aterrizar ahi mismo
		if res:
			##IR HACIA LA POSICION INICIAL PARA REUBICARLO
			origen = vehicle.location.global_relative_frame
			##COMO USAMOS RELATVIAS DIRECTAMENTE CAPTURAMOS LA POSICION
			[xinicial,yinicial]=controlador.getPosInicial()
			destino=LocationGlobalRelative(xinicial, yinicial, altura)
			#imprimir("Llendo a :"+str(xinicial)+","+str(yinicial))
			irHasta(origen,destino)	
		##NO ES NECESARIO BUCLE PARA CAPTURAR LAS SEÑALES
		return jsonify(ok=res)

@app.route("/api/despegar", methods=['POST', 'PUT'])
def api_despegar():
    if request.method == 'POST' or request.method == 'PUT':
	altura=float(request.json['altura'])
	velocidad=float(request.json['velocidad'])
	res=despegar(altura,velocidad)
	##Lo hacemos aterrizar ahi mismo
	if res:	
		aterrizar()
	return jsonify(ok=res)
	

def Deteccion(arg1,evento_parada):
	global salir
	global paradaDeteccion
	global controlador
	# Empezamos a recorrer siempre desde la 1era foto
	i = 0
	sleep(2)
	while (not salir and not paradaDeteccion.is_set()):
		try:
			if (i<controlador.getTotalFotosMision()):
				imprimir("quiere calificar a:"+str(i))
				[regiones, score,tiempocalif]=controlador.calificarFoto(i)
				imprimir ('Califique foto:' + str(i) +"-regiones:" +str(regiones)+"-score:" + str(score)+"- al tiempo:"+str(tiempocalif))
				i+=1
			sleep(0.1)
		except Exception as e:
			imprimir("ERROR EN MODEULO DETECTION" + str(e))


##AGREGADO FOTOS EN MOVIMIENTO
def FotosMovimiento(arg1,evento_parada):
	global salir
	#global paradaDemMovimiento

	global controlador
	global coordFotosMovimiento

	global conthilos
	conthilos+=1
	miid=conthilos

	##Varible para ver si tengo trabajo
	#tengoTrabajo=False

	# Empezamos a recorrer siempre desde la 1era foto
	i = 0
	##para que el sleep no vuelva a desperatar el proceso
	evento_parada.wait(1)
	#sleep(0.5)
	proxCoordenada=None
	tinicial = controlador.getTiempoIini()
	#print("NI SI QUIERA NOS LLAMARON")
	while (not salir and not evento_parada.is_set()):
		try:

			#imprimir("Estoy AQUI esperando")

			#Si no tengo trabajo actual, veo si hay trabajo
			#if proxCoordenada==None:
			# Obtengo la primera coordenada, la remueve y libero enseguida el mutex
			mxMovFotos.acquire()
			#imprimir("El largo es: "+str(len(coordFotosMovimiento)))
			if len(coordFotosMovimiento)>0:
				proxCoordenada=coordFotosMovimiento[i]
				#imprimir ("la prox coordenada: "+str(proxCoordenada))
				#coordFotosMovimiento.remove(proxCoordenada)
			mxMovFotos.release()
			#Si ya tenia trabajo o lo consegui ahora
			if proxCoordenada!=None and vehicle.mode.name == "GUIDED" and not salir and not evento_parada.is_set():

				# Espero hasta alcanzar las distancias y saco la foto
				[x, y, h, sacofoto,xrel,yrel,pCuestion]=proxCoordenada
				#imprimir("tengo que volar a: " + str(xrel)+ ", "+str(yrel))
				#cambiamos el while por el if
				#while vehicle.mode.name == "GUIDED" and not salir and not evento_parada.is_set():
				xactual = vehicle.location.global_relative_frame.lat
				yactual = vehicle.location.global_relative_frame.lon
				hactual = vehicle.location.global_relative_frame.alt
				dist_actual = calcular_distancias(xactual, yactual, x, y)
				#imprimir ("Posicion global actual: lat:" + str(xactual) + " lon:" + str(yactual) + " dist:" + str(dist_actual) )

				#sumamos un umbral de 0.5 para que comience a sacar antes a la foto
				margen = controlador.getUmbral()+0.5
				if (dist_actual < margen):
					#tactual = time()
					#imprimir("LLEGÓ AL PUNTO A: " + str(round(tactual - tinicial, 2)) + "s")
					mxCamara.acquire()
					imprimir( "Yo tambien quiero sacar foto")
					hglobal = vehicle.location.global_frame.alt
					imprimir("Alturas de la foto relativa: " + str(hactual) + " - absoluta: " + str(hglobal))
					hguardar = hactual
					if controlador.getAltitud() >= 1:
						hguardar = hglobal

					controlador.sacarfotopalo(xactual, yactual, hguardar, pCuestion)
					#tactual = time()
					#imprimir("SACO FOTO A: " + str(round(tactual - tinicial, 2)) + "s")
					imprimir("ID: "+str(miid)+"****saca foto desde adentro****: " + str(proxCoordenada))
					mxCamara.release()

					#Me quede sin laburo de nuevo
					antCoordenada=proxCoordenada
					proxCoordenada = None
					mxMovFotos.acquire()
					# imprimir("El largo es: "+str(len(coordFotosMovimiento)))
					if len(coordFotosMovimiento) > 0:
						coordFotosMovimiento.remove(antCoordenada)
						#if len(coordFotosMovimiento) > 0:
						#	proxCoordenada = coordFotosMovimiento[i]
						# imprimir ("la prox coordenada: "+str(proxCoordenada))
						# coordFotosMovimiento.remove(proxCoordenada)
					mxMovFotos.release()
				#sleep(0.2)
				#evento_parada.wait(0.5)
			#sleep(0.2)
			#medio segundo es mucho, le baje
			evento_parada.wait(0.3)
		except Exception as e:
			#Liberar para que no se produzca deadlock
			mxMovFotos.release()
			imprimir("ERROR EN THREAD DE FOTOS EN MOVIMIENTO" + str(e))


@app.route("/api/iniciarmision", methods=['POST', 'PUT'])
def api_iniciar():
	global vehicle
	global controlador
	global demonioDeteccion
	global paradaDeteccion
	global paradaDemMovimiento
	global demonioMovimiento
	global coordFotosMovimiento
	global mxMovFotos
	if request.method == 'POST' or request.method == 'PUT':
		try:
			#altura=float(request.json['altura'])
			#velocidad=float(request.json['velocidad'])
			umbral = float(request.json['umbral'])
			resolucion = int(request.json['resolucion'])
			movfotos = int(request.json['movfotos'])
			altitud = int(request.json['altitud'])
			demora = float(request.json['demora'])
			bateriaini=int(vehicle.battery.level)

			##AGREGADO DETECCION ESTACA
			if controlador.getConfig().procImg == True:
				##Detenemos el demonio bruscamente
				paradaDeteccion.set()
				##Lo volvemos a iniciar para la nueva mision
				paradaDeteccion=Event()
				demonioDeteccion = Thread(target=Deteccion, args=(1,paradaDeteccion))
				demonioDeteccion.daemon = True
				demonioDeteccion.start()


			print "valor de movfotos "+ str(movfotos)
			##AGREGADO FOTOS EN MOVIMIENTO

			##Estemos en mision de movimiento o no, siempre detener el demonio en segundo plano porque genera complicaciones

			if not paradaDemMovimiento.is_set():
				##Detenemos el demonio bruscamente
				paradaDemMovimiento.set()
			
			if movfotos==1:
				#Se vacian las coordenas a esperar
				mxMovFotos.acquire()
				coordFotosMovimiento = []
				mxMovFotos.release()

				print "VAMOS A DESPERTAR EL MUERTO"
				##Lo volvemos a iniciar para la nueva mision
				paradaDemMovimiento = Event()
				demonioMovimiento = Thread(target=FotosMovimiento, args=(1,paradaDemMovimiento))
				demonioMovimiento.daemon = True
				demonioMovimiento.start()

			# A veces cuando se hace un land o se corta bruscamente la mision o se cambia par otra, se va a acceder a una foto que no existe.
			cantcoord=controlador.iniciarMision(umbral,resolucion,bateriaini,demora,movfotos, altitud)

			if cantcoord<=0:
				imprimir("salimos por aqui")
				return jsonify(ok=False)
			else:
				datosRecorrido=controlador.getDatosRecorridoActual()
				altura=datosRecorrido["alt"]
				velocidad=datosRecorrido["vel"]
				res=despegar(altura,velocidad)
				#luego de despegar empezar a ajustar las condiciones de luz de la cámara y recuperar las coordenadas de la mision
				controlador.comenzarPreview()
				coordsAntFMovimiento=[]
				coordenada=controlador.getSigCoordenada(movfotos)
				while coordenada:
					##AGREGADO FOTOS EN MOVIMIENTO
					[x,y,h,siFoto,xr,yr,coordsNueFMovimiento] = coordenada

					mxMovFotos.acquire()
					coordFotosMovimiento = coordsAntFMovimiento
					#imprimir( "coordFotosMovimiento: "+str(coordFotosMovimiento))
					mxMovFotos.release()
					#Las que obtuve las dejo para despues
					coordsAntFMovimiento=coordsNueFMovimiento

					origen = vehicle.location.global_relative_frame
					destino = LocationGlobalRelative(x,y, h)
					#imprimir("Llendo a :" + str(xr) + "," + str(yr))
					irHasta(origen,destino,siFoto)
					coordenada=controlador.getSigCoordenada(movfotos)
				
				imprimir ('Ahora pasamos a modo land')
				aterrizar()

				bateriafin = int(vehicle.battery.level)
				tiempo=controlador.terminarMision(bateriafin)
				imprimir("TIEMPO TOTAL DE LA MISION: "+str(tiempo)+ "s")
				imprimir ("Posicion global actual: %s" + str(vehicle.location.global_relative_frame) + "-" + str(vehicle.home_location))

				return jsonify(ok=res)
		except Exception as e:
			imprimir("INICIAR MISION"+ str(e))
			return jsonify(ok=False)


@app.route("/api/mode", methods=['POST', 'PUT'])
def api_mode():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            vehicle.mode = VehicleMode(request.json['mode'].upper())
            vehicle.flush()
            return jsonify(ok=True)
        except Exception as e:
            imprimir(str(e))
            return jsonify(ok=False)



@app.route("/api/descargar/<nombreArchivo>", methods=['GET', 'POST'])
def api_descargar(nombreArchivo):
	ruta = 'fotos/'

	if nombreArchivo:
		return send_file(ruta + nombreArchivo, as_attachment=True)

@app.route("/api/comprimir/<nombreArchivo>", methods=['GET', 'POST', 'PUT'])
def api_comprimir(nombreArchivo):
	ruta = 'fotos/'
	archivos = ""
	
	for file in os.listdir(ruta):
		if file.startswith(nombreArchivo):
			archivos = archivos + " " + os.path.join(ruta, file)

	if archivos:
		nombreArchivo = "fotos_" + nombreArchivo + ".tar.gz"
		try:
				text = getstatusoutput("tar -zcvf " + ruta + nombreArchivo + archivos)	
				#return send_from_directory(directory=ruta, filename=nombreArchivo, as_attachment=True)
				return jsonify(ok=True, nombre=nombreArchivo)
		except Exception as e:
			return jsonify(ok=False, nombre=str(e))
	return jsonify(ok=False, nombre="No hay ninguna foto de la mision")

@app.route("/api/versihayfotos/<nombreArchivo>", methods=['GET', 'POST', 'PUT'])
def api_versihayfotos(nombreArchivo):
	ruta = 'fotos/'
	archivos = ""
	
	for file in os.listdir(ruta):
		if file.startswith(nombreArchivo):
			archivos = archivos + " " + os.path.join(ruta, file)

	if archivos:
		return jsonify(ok=False) 
	return jsonify(ok=False, nombre="No hay ninguna foto de la mision")

@app.route("/api/descargarlogs", methods=['GET', 'POST'])
def api_descargarlogs():
       return send_file("/tmp/torreap", as_attachment=True)	

@app.route("/api/descargarbd", methods=['GET', 'POST'])
def api_descargarbd():
       return send_file("bd.backup", as_attachment=True)

@app.route("/api/limpiarbd", methods=['PUT', 'POST'])
def api_limpiarbd():
        global controlador
        controlador.borrarBD()
        p = subprocess.call(shlex.split('supervisorctl restart torreap'))
        return p

       
		
@app.route("/api/cargargpx", methods=['POST', 'PUT'])
def api_cargargpx():
    if request.method == 'POST' or request.method == 'PUT':
        
        fechaMin = request.json['fechaMin']
        fechaMax = request.json['fechaMax']

        
        if not fechaMin:
                minFecha = dateutil.parser.parse('1950-01-01')
        else:
                minFecha = dateutil.parser.parse(fechaMin)
                
        if not fechaMax:
                maxFecha = dateutil.parser.parse('2030-01-01')
        else:
                maxFecha = dateutil.parser.parse(fechaMax)

                
        archivo = ''
        hayPendrive = False
        hayCarpetaCoor = False
        ruta = "/media/pi"
        #ruta = "C:/wamp64/"

        for file in os.listdir(ruta):
            if file: 
                hayPendrive = True
                path = os.path.join(ruta, file)
                if os.path.isdir(path):
                    for carpetaPendrive in os.listdir(path):
                        if carpetaPendrive.startswith("coordenadasDron"):
                            hayCarpetaCoor = True
                            nuevoPath =  os.path.join(path, carpetaPendrive)
                            if os.path.isdir(nuevoPath):
                                for filePendrive in os.listdir(nuevoPath):
                                    if filePendrive.endswith(".gpx"):
                                        print(os.path.join(nuevoPath, filePendrive))
                                        archivo = os.path.join(nuevoPath, filePendrive)
                                        break

		if not hayPendrive:
			return 'No hay pendrive'
		if not hayCarpetaCoor:
			return 'No hay carpeta'
        if not archivo:
                return 'No hay archivo'
        gpx_file =open(archivo,'r') 
        gpx=gpxpy.parse(gpx_file)

        stri = "{"
        cont = 0
        for waypoint in gpx.waypoints:
                fecha = waypoint.time
                if not fecha:
                        fecha = waypoint.description
                        if fecha:
                                nueva = fecha    
                else :
                        nueva = fecha

                parseada = ''
                if fecha:
                        parseada = get_date(fecha)
                if parseada:
                        if cumplen_condiciones(parseada, minFecha, maxFecha):
                                if not waypoint.name:
                                        waypoint.name = '' + str(cont)
                                stri = stri+"{nombre:'"+waypoint.name+"', latitud: '"+str(waypoint.latitude)+"',longitud: '"+str(waypoint.longitude)+"'}," 
                                cont += 1
         
        if cont > 0:    
                s = stri[:len(stri) -1]
                s = s+"}"
        else:
                s = '0'
        return s

def get_date(stringFecha):
  try:
    fechaNueva = dateutil.parser.parse(stringFecha)
    fechaNueva = fechaNueva.replace(hour=0 , minute = 0 ,second = 0)
    return fechaNueva
  except:
    pass
  return None

@app.route("/api/borrarfotos/<idMision>", methods=['GET', 'POST', 'PUT'])
def api_borrarfotos(idMision):
        global controlador
	ruta = 'fotos/'
	archivos = ""
	
	archivos = ruta+"fotos_" + idMision + ".tar.gz"
	if(idMision != '0'):
                for file in os.listdir(ruta):
                        if (file.startswith(idMision) or file.startswith("min-" + idMision)) and (file.endswith(".png") or file.endswith('.jpg') or file.endswith('.jpeg')):
                                archivos = archivos + " " + os.path.join(ruta, file)
        else:
               for file in os.listdir(ruta):
                        if file.endswith(".png") or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.tar.gz'):
                                archivos = archivos + " " + os.path.join(ruta, file) 
	try:	
                controlador.borrarFotosBD(idMision)
		if archivos:
			text = getstatusoutput("rm " + archivos)
			#return send_from_directory(directory=ruta, filename=nombreArchivo, as_attachment=True)
		return jsonify(ok=True)
	except Exception as e:
		return jsonify(ok=False, nombre=str(e))

@app.route("/api/exportarbd", methods=['POST', 'PUT'])
def api_exportarbd():
	global controlador
	bdname = controlador.getConfig().db
	bduser = controlador.getConfig().dbuser
	bdpass = controlador.getConfig().dbpass
	host = controlador.getConfig().dbhost

	try:
		comando = "set PGPASSWORD=[" + bdpass + "] pg_dump -U " + bduser + " -h " + host + " " + bdname + " > bd.backup"
		text = getstatusoutput(comando)	
		
		return jsonify(ok=True)
	except Exception as e:
		return jsonify(ok=False, nombre=str(e))


def cumplen_condiciones(fecha, minFecha, maxFecha):
  retorno = True
  if fecha:
    if minFecha:
      if fecha < minFecha:
        retorno = False
    if maxFecha:
      if fecha > maxFecha:
        retorno = False
  else: 
    retorno = False

  return retorno

def state_msg():
	global t_parada
	global controlador
	if (not t_parada.is_set()):
		if vehicle.location.global_relative_frame.lat == None:
			   raise Exception('no position info')
		if vehicle.armed == None:
			   raise Exception('no armed info')
	    	[idm,tipom,distact,distini,idf,xf,yf,hf,ruta]=controlador.getDatosMision()
	    	recorridos=controlador.getDatosRecorridos()
		return {
			"conectado" : conectado,
			"armed": vehicle.armed,
			"alt": vehicle.location.global_relative_frame.alt,
			"mode": vehicle.mode.name,
			"heading": vehicle.heading or 0,
			"lat": vehicle.location.global_relative_frame.lat,
			"lon": vehicle.location.global_relative_frame.lon,
			"idm":idm,
			"tipom":tipom,
			"distact":distact,
			"distini":distini,
			"idf":idf or 0,
			"xf":xf or 0,
			"yf":yf or 0,
			"hf":hf or 0,
			"ruta":ruta or 0,
			"recorridos":recorridos,
			"bateria":vehicle.battery.level,
			"satelites":str(vehicle.gps_0)
    	}

def tcount(arg1,evento_parada):
    global salir
    global t_parada
    while (not salir and not t_parada.is_set()):
        ##sleep(4)
	##para que el sleep no vuelva a desperatar el proceso
	t_parada.wait(5)
        try:
		if (not t_parada.is_set()):
			msg = state_msg()
			for x in listeners_location:
				x.put(msg)
        except Exception as e:
		imprimir("actualizacion" + str(e))
		pass
    return "chau"

@app.route("/api/sse/state")
def api_sse_location():
    def gen():
        q = Queue()
        listeners_location.append(q)
        try:
            while not salir:
                result = q.get()
                ev = sse_encode(result)
		#http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            listeners_location.remove(q)

    return Response(gen(), mimetype="text/event-stream")


@app.route("/api/conectar", methods=['POST', 'PUT'])
def conectar():
	if request.method == 'POST' or request.method == 'PUT':
		try:
			cadena=request.json['cadena']
			sim=request.json['sim']
			ok=connect_to_drone(cadena,sim)
			return jsonify(ok=ok)
		except Exception as e:
			imprimir(str(e))
			return jsonify(ok=False)

def connect_to_drone(cadena,sim):
	global t_parada
	global t
	global vehicle
	global conectado
	global salir
	global controlador
	try:
		imprimir ('Conectando con el dron...')
		while not vehicle:
			#imprimir('************Entre a ver si me puedo conectar la drone**********************')
			try:
				vehicle = connect(cadena, wait_ready=True, rate=10)
			except Exception as e:
				imprimir ('Esperando para la conexion... (%s)' % str(e))
				sleep(2)
			##Desactivar el salir para que se activen los procesos
			salir=False
			#activado por el simulador
			if sim==True:
				vehicle.parameters['ARMING_CHECK'] = 0
			vehicle.flush()
			t_parada=Event()
			t = Thread(target=tcount, args=(1,t_parada))
			t.daemon = True
			t.start()
			#controlador.conectarBase()
			conectado=True
			imprimir("conectado!")
			return True
	except Exception as e:
		imprimir ('No fue posible conectarse con el dron (%s)' % str(e))
		return False


@app.route("/api/desconectar", methods=['POST', 'PUT'])
def desconectar():
	global salir
	global vehicle
	global t_parada
	global conectado
	global controlador
	if request.method == 'POST' or request.method == 'PUT':
		try:
			t_parada.set()
			vehicle.close()
			##Volver las variables a su estado original para que sea posible la reconexion
			salir=True
			vehicle = None
			conectado=False
			#controlador.desconectarBase()
			imprimir("Se descconecto!")
			return jsonify(ok=True)
		except Exception as e:
			imprimir(str(e))
			return jsonify(ok=False)

# Never cache
@app.after_request
def never_cache(response):
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def main():
	global controlador
	global paradaDeteccion
	global paradaDemMovimiento
	global mxMovFotos
	global mxCamara
	global conthilos
	conthilos=0
	#global configuracion
	#Llamamos a una fábrica que nos cree una instancia del dron para independizar

	##AGREGADO DETECCION ESTACA
	controlador=ControladorCamara()
	configuracion=controlador.getConfig()
	if configuracion.procImg==True:
		paradaDeteccion = Event()
	##AGREGADO FOTOS EN MOVIMIENTO
	mxMovFotos = Lock()
	mxCamara = Lock()
	paradaDemMovimiento = Event()
	app.run(threaded=True, host='0.0.0.0', port=configuracion.httpport, debug=False)

if __name__ == "__main__":
	main()
