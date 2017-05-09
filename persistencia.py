# coding=utf-8
from recorrido import Recorrido
from areainteres import AreaInteres
from punto import Punto
from mision import Mision
from foto import Foto
from conexion import Conexion

class Persistencia():
    def __init__(self, config):
        ##Esta es la conexión para las inserts
        #self.conexion=Conexion(config)
        self.config=config
        pass

    def iniciarConexion(self):
        self.conexion = Conexion(self.config)
    def getCursor(self):
        return self.conexion.getCursor()
    def commit(self):
        self.conexion.commit()
    def cerrarConexion(self):
        self.conexion.cerrar()

    def correrInsert(self, consulta, valores):
        #print consulta
        #print valores
        cursor=self.getCursor()
        cursor.execute(consulta,valores)
        id=int(cursor.fetchone()[0])
        self.commit()
        return id
        #return 0

    def guardarRecorrido(self, padron, alt, vel, tipo, fotosxestaca, calculodist, umbral,solapamiento):
        consulta="INSERT INTO recorrido (padron, altura, velocidad, tipo, fotosxestaca, calculodist, umbral, solapamiento) values (%s,%s,%s,%s, %s, %s, %s, %s) RETURNING ID"
        valores = (padron, alt, vel, tipo, fotosxestaca, calculodist, umbral, solapamiento)
        return self.correrInsert(consulta, valores)

    def guardarAInteres(self, tipo, idrec):
        consulta = "INSERT INTO areainteres (tipo, idrec) values (%s,%s) RETURNING ID"
        valores = (tipo, idrec)
        return self.correrInsert(consulta, valores)

    def guardarPunto(self, x, y, h, idai, esExacto):
        consulta = "INSERT INTO puntos (x,y,h,idai) values (%s,%s,%s,%s) RETURNING ID"
        valores = (x,y,h,idai)
        idp = self.correrInsert(consulta, valores)
        if esExacto is True:
            consulta ="UPDATE areainteres SET idpexacto=%s WHERE id=%s RETURNING ID"
            valores=(idp,idai)
            self.correrInsert(consulta, valores)
        return idp

    def guardarMision(self, idrec, fecha, umbral, resolucion, bateriaini, demora, movfotos):
        consulta = "INSERT INTO mision (idrec, fecha, umbral, resolucion, bateriaini, demora, movfotos) values (%s,%s,%s,%s,%s, %s, %s) RETURNING ID"
        valores = (idrec, fecha, umbral, resolucion, bateriaini, demora, movfotos)
        return self.correrInsert(consulta, valores)

    def actualizarMision(self, idm,bateriafin,tiempo,disttotal):
        consulta = "UPDATE mision SET bateriafin=%s, tiempo=%s, disttotal=%s WHERE id=%s RETURNING ID"
        #print "score:" + str(sdetect)
        valores = (bateriafin,tiempo,disttotal,idm)
        return self.correrInsert(consulta, valores)


    def actualizarFoto(self, idf,sdetect,rdetect):
        consulta = "UPDATE foto SET sdetect=%s, rdetect=%s WHERE id=%s RETURNING ID"
        #print "score:" + str(sdetect)
        valores = (sdetect,rdetect,idf)
        return self.correrInsert(consulta, valores)

    def guardarFotos(self, x ,y ,h, fecha, ruta, idm, idp):
        consulta = "INSERT INTO foto (x,y,h,fecha, url, idm,idp) values (%s,%s,%s, %s, %s,%s,%s) RETURNING ID"
        valores = (x,y,h,fecha, ruta, idm,idp)
        return self.correrInsert(consulta, valores)


    def cargarFotos(self, idm, r):
        ##Para la carga de datos se abren otras conexiones que solo se usan para eso
        conexion=Conexion(self.config)
        cursor=conexion.getCursor()
        fotos=[]
        cursor.execute("SELECT id,x,y,h,url,fecha, idp, rdetect, sdetect from foto where idm="+str(idm)+" ORDER BY id")
        for id,x,y,h,url,fecha, idp, rdetect,sdetect in cursor.fetchall():
            fotos.append(Foto(x,y,h,r.obtenerPunto(idp),id,None,fecha,url,rdetect,sdetect,self))
        conexion.cerrar()
        return fotos

    def cargarPuntos(self, idai, ai):
        conexion=Conexion(self.config)
        cursor=conexion.getCursor()
        puntos=[]
        cursor.execute("SELECT id,x,y,h from puntos where idai="+str(idai)+ " ORDER BY id")
        for id,x,y,h in cursor.fetchall():
            puntos.append(Punto(x,y,h,ai,id))
        conexion.cerrar()
        return puntos

    def cargarAreas(self, idrec):
        conexion=Conexion(self.config)
        cursor=conexion.getCursor()
        areasinteres = []
        cursor.execute("SELECT id, tipo, idpexacto from areainteres where idrec="+str(idrec)+" ORDER BY id")
        for id, tipo, idpexacto in cursor.fetchall():
            ai=AreaInteres(tipo,id)
            ai.setPuntos(self.cargarPuntos(id,ai))
            areasinteres.append(ai)
        conexion.cerrar()
        return areasinteres

    def cargarMisiones(self, idrec, r):
        conexion=Conexion(self.config)
        cursor=conexion.getCursor()
        misiones = []
        cursor.execute("SELECT id, fecha, umbral, resolucion, bateriaini, bateriafin, tiempo, disttotal, demora, movfotos from mision WHERE idrec="+str(idrec)+" ORDER BY id")
        for id, fecha, umbral, resolucion, bateriaini, bateriafin, tiempo, disttotal, demora, movfotos in cursor.fetchall():
            misiones.append(Mision(r,id,fecha, umbral, resolucion, bateriaini, bateriafin, tiempo, disttotal, demora, movfotos, 0, self.cargarFotos(id, r)))
        conexion.cerrar()
        return misiones

    def cargarMisionesRecorridos(self):
        conexion=Conexion(self.config)
        cursor=conexion.getCursor()
        recorridos=[]
        misiones=[]
        cursor.execute("SELECT id, tipo, velocidad, altura, padron, fotosxestaca, calculodist, umbral, solapamiento from recorrido ORDER BY id")
        for id, tipo, velocidad, altura, padron, fotosxestaca, calculodist, umbral, solapamiento in cursor.fetchall():
            r=Recorrido(padron,altura,velocidad,tipo,id, fotosxestaca, calculodist, umbral, solapamiento, self.cargarAreas(id))
            misiones+=self.cargarMisiones(id, r)
            recorridos.append(r)
        conexion.cerrar()
        return [recorridos,misiones]