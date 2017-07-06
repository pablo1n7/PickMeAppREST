import os
from pymongo import MongoClient

''' Configuración de la base '''
CLIENT = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
#CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT.pickmeapp
''' ----------------------- '''

class Lugar(object):
    '''
        Clase Lugar, representa un punto de interes en el mapa
    '''
    nombre = ""
    descripcion = ""
    latlng = ""
    usuario = None

    @classmethod
    def get_lugares(cls, filtro_usuario=None):
        '''
            Obtiene todos los lugares de la base, si es filtro_usuario != None
            obtiene los lugares agregados por ese usuario.
        '''
        if  filtro_usuario != None:
            filtro  = {"usuario":filtro_usuario}
        else:
            filtro = {}
        return [Lugar(r).diccionarizar() for r in list(DB.lugares.find(filtro))]

    @classmethod
    def get_lugar(cls, filtro_nombre):
        '''
            Obtiene el lugar que tiene el nombre ingresado
        '''
        
        return [Lugar(r).diccionarizar() for r in list(DB.lugares.find({"nombre":filtro_nombre}))]

    def __init__(self, data):
        '''
         Constructor de la clase, recibe un diccionario
        '''
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.latlng = data["latlng"]
        self.usuario = data["usuario"]

    def guardar(self):
        '''
            Guarda un lugar en la base de datos
        '''
        return DB.lugares.insert_one(self.__dict__).inserted_id

    def diccionarizar(self):
        d_lugar = self.__dict__
        d_lugar['_id'] = ""
        return d_lugar


class Usuario(object):
    '''
        Clase Usuario representa un usuario de la app
    '''
    nombre = ""

    @classmethod
    def get_usuario(cls, nombre_usuario):
        '''
            Obtiene un usuario de la base
        '''
        return nombre_usuario