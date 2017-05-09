import psycopg2

class Conexion():
    def __init__(self, config):
        cadena = "host='"+config.dbhost+"' dbname='"+config.db+"' user='"+config.dbuser+"' password='"+config.dbpass+"'"
        #print "Conectando a la base de datos\n	->%s" % (cadena)
        # get a connection, if a connect cannot be made an exception will be raised here
        self.conexion = psycopg2.connect(cadena)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conexion.cursor()
        pass

    def getCursor(self):
        return self.cursor

    def commit(self):
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()