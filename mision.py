from foto import Foto
from datetime import datetime
from time import time

class Mision():
    def __init__(self, rec, idm=None, fecha=None, umbral=-1, resolucion=-1, bateriaini=-1, bateriafin=-1, tiempo=-1, disttotal=-1, demora=0, movfotos=0, altitud=0, fotos=None, persistencia=None):
        self.recorrido=rec
        self.fotos=[]
        ##Se usa para tener referencia a la ultima foto para mostrarla mas facil
        self.fotoact=None
        self.totalFotos=0
        self.distini=0
        self.distactual=0
        self.umbral=umbral
        self.resolucion=resolucion
        self.bateriaini=bateriaini
        self.demora=demora
        self.movfotos=movfotos
        self.bateriafin=bateriafin
        self.tiempo=tiempo
        self.disttotal=disttotal
        self.altitud=altitud
        self.persistencia=persistencia
        if idm!=None:
            self.idm=idm
            self.fecha=fecha
            self.fotos=fotos
            self.totalFotos=len(self.fotos)
        else:
            self.fecha = datetime.now()
            # contador de tiempo actual de mision
            self.tiempoini = time()
            # inicializamos el contador de disttotal
            self.disttotal=0
            self.idm=persistencia.guardarMision(rec.getId(),self.fecha,self.umbral,self.resolucion,self.bateriaini, self.demora, self.movfotos)

    def terminarMision(self,bateriafin):
        #todo
        self.tiempo=round(time()-self.tiempoini,2)
        self.bateriafin=bateriafin
        self.disttotal=round(self.disttotal,2)
        self.persistencia.actualizarMision(self.idm,self.bateriafin,self.tiempo,self.disttotal)
        return self.tiempo

    def getTipo(self):
        return self.recorrido.getTipo()

    def getId(self):
        return self.idm

    def getTiempoIni(self):
        return self.tiempoini

    def getUmbral(self):
        return self.umbral

    def getTiempo(self):
        return self.tiempo

    def getDistTotal(self):
        return self.disttotal

    def getConsumoBateria(self):
        return self.bateriaini-self.bateriafin

    def getBateriaFinal(self):
        return self.bateriafin

    def getDemora(self):
        return self.demora

    def getResolucion(self):
        return self.resolucion

    def getAltitud(self):
        return self.altitud

    def esEstacas(self):
        return self.recorrido.esEstacas()

    def crearFoto(self, x,y,h,p):
        nomparcialf =str(self.idm)+"-"+str(self.recorrido.getPadron())
        f=Foto(x,y,h,p,None,self.idm,None,None,None,None,self.persistencia,nomparcialf)
        self.fotos.append(f)
        #self.fotoact=f
        return f.getDatosEXIF(True)

    def getTotalFotos(self):
        #return len(self.fotos)
        ##Recien ahi comenzamos con el procesamiento si no la foto no esta sacada
        return self.totalFotos

    def getRutaFoto(self,i):
        #comentar esto
        #print '2016-07-24-08-10-18.jpg'
        #return '2016-07-24-08-10-18.jpg'
        #descomentar esto
        # A veces cuando se hace un land o se corta bruscamente la mision o se cambia par otra, se va a acceder a una foto que no existe.
        if i < self.getTotalFotos():
            return self.fotos[i].getRuta()
        else:
            return None

    def setCalifFoto(self,i, regiones, score):
        #A veces cuando se hace un land o se corta bruscamente la mision o se cambia par otra, se va a acceder a una foto que no existe.
        if i<self.getTotalFotos():
            self.fotos[i].setCalifFoto(regiones, score)

    def setFotoActual(self):
        self.fotoact=self.fotos[-1]
        ##Recien ahi comenzamos con el procesamiento si no la foto no esta sacada
        self.totalFotos+=1

    def setDistIni(self, dist_ini):
        self.distini=dist_ini
        self.disttotal=self.disttotal+self.distini

    def setDistAct(self, dist_actual):
        self.distactual=dist_actual

    def getDatosRecorrido(self):
        return self.recorrido.getDataRecorrido()

    def getDataMision(self, pcantai, alturaestaca, alturafranja):
        dataFotos = []
        scoreAi = {}
        maxScoreAi={}
        #maxRegionesAi={}
        alturas={}
        #regionesAi={}
        scoreTot=0
        cantRegionesTot=0
        contFotos=0

        #PARA TERMINAR EL DESARROLLOO EN FUNCION DE pcantai deberian limitarse el total de fotos a mostrar
        #AL MOMENTO A PARTIR DE LA LINEA 179 SE LIMITA mostrar solo un total de datos de ai que no sobrepase pero los datos de fotos van por otro lado
        #PERO POR LO MENOS SIRVE PARA QUE AGARREMOS MISIONES TODAS CON L MISMA CANTIDAD DE ESTACAS PARA VER Y QUE NO QUEDE FIJO EL PARAMETRO
        #PODRIA SER ALGO DE LA VISTA NOMAS

        print "ARRANCAMOS A TRAER EL DATA MISION"
        for f in self.fotos:
            dataFoto=f.getDataFoto(alturaestaca,alturafranja)
            dataFotos.append(dataFoto)
            altPasFoto=float(dataFoto["altoPasto"])
            regFoto=int(dataFoto["regiones"])
            scoFoto=float(dataFoto["score"])
            idAiFoto=int(dataFoto["idai"])
            #print "regiones q me da: "+str(regFoto)
            #Acumulando regiones por Ai
            #regionesAi[idAiFoto]=regionesAi.get(idAiFoto,0) + regFoto
            if regFoto>0:
                #regionesAi[idAiFoto] = regionesAi.get(idAiFoto, 0) + 1
                cantRegionesTot += 1
                auxScore=maxScoreAi.get(idAiFoto, 0.0)
                #si el score de la ai por ahora es 0... 0 encontramos foto con score mayor a la actual y la altura de pasto no dio error
                if auxScore==0 or (auxScore < scoFoto and altPasFoto>=0):
                    maxScoreAi[idAiFoto]=scoFoto
                    #maxRegionesAi[idAiFoto]=regFoto
                    alturas[idAiFoto]=altPasFoto
            #print "el id de foto es: "+str(f.getId()) + " id de la Ai: "+str(idAiFoto)
            #print "las regiones del idAi: " + str(regionesAi.get(idAiFoto,0))
            scoreAi[idAiFoto] = scoreAi.get(idAiFoto, 0.0) + scoFoto
            scoreTot += scoFoto
            contFotos+=1

        #Pedirle al recorrido la cantidad de fotosxestaca para hacer el promedio
        fotoxestaca=self.recorrido.getCantPuntos()
        print fotoxestaca
        promScoreAi={}
        alturasTot=0
        for key in scoreAi:
            promScoreAi[key]=round(scoreAi[key]/fotoxestaca,2)
            #Si alguna region no tiene su valor aun ponerle 0
            #regionesAi[key] = regionesAi.get(key, 0)
            #Lo mismo para las alturas
            alturas[key] = alturas.get(key, 0)
            alturasTot+=alturas[key]
            #print "clave "+ str(key) + " valor: "+str(promScoreAi[key])
        promScoreTot=0
        promAlturas=0
        if contFotos==0:
            print contFotos
        else:
            promScoreTot = round(scoreTot / contFotos, 2)
            promAlturas=round(alturasTot)/len(promScoreAi)

        #Hay que ordenar los diccionarios
        promScoreAiOrd = [valor for (clave, valor) in sorted(promScoreAi.items())]
        #regionesAiOrd = [valor for (clave, valor) in sorted(regionesAi.items())]
        # En el lugar de las regionesAi vamos a mandar las altura
        alturasOrd = [valor for (clave, valor) in sorted(alturas.items())]

        #Achicamos la cantidad de areas de interes si no es cualquiera
        mcantai=len(promScoreAi)
        if mcantai>pcantai:
            mcantai=pcantai

        return {"idm":self.idm,"umbral":self.umbral, "demora":self.demora, "resolucion":self.resolucion, "tiempo":self.tiempo,
                "disttotal":self.disttotal,"bateria":self.getConsumoBateria(), "recorrido":self.getDatosRecorrido(), "fotos":dataFotos,
                "promScoreAi":promScoreAiOrd,"promScoreTot":promScoreTot,"alturasAi":alturasOrd,"cantRegionesTot":cantRegionesTot,
                "cantAi":mcantai, "cantFotos":contFotos, "promAlturas":promAlturas}


    def getDatosMision(self):
        idf=0
        xf=0
        yf=0
        hf=0
        ruta=None
        tipom=self.recorrido.getTipo()
        if self.fotoact!=None:
            [idf, xf, yf, hf, ruta]=self.fotoact.getDatosFotoActual()
        return [self.idm,tipom,self.distactual,self.distini,idf,xf,yf,hf,ruta]


