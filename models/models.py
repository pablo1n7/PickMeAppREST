# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient

''' Configuración de la base '''
if 'OPENSHIFT_APP_NAME' in os.environ:
    CLIENT = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
else:
    CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT.pickmeapp
''' ----------------------- '''

class Lugar(object):
    '''
        Clase Lugar, representa un punto de interes en el mapa
    '''
    id_lugar = 0
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
        '''
            Prepara los objetos para enviar.
        '''
        d_lugar = self.__dict__
        d_lugar['_id'] = ""
        return d_lugar


class Usuario(object):
    '''
        Clase Usuario representa un usuario de la app
    '''
    nombre = ""
    id_usuario = ""

    @classmethod
    def get_usuario(cls, nombre_usuario):
        '''
            Obtiene un usuario de la base segun su nombre de usuario.
        '''
        usuario = [Usuario(r) for r in list(DB.usuarios.find({"nombre":nombre_usuario}))]
        return usuario[0]    

    @classmethod
    def get_usuarios(cls):
        '''
            Obtiene todos los usuarios de la base.
        '''
        usuarios = [Usuario(r).diccionarizar() for r in list(DB.usuarios.find({}))]
        return usuarios


    @classmethod
    def check_usuario(cls, nombre_usuario,id_usuario):
        '''
           Check_usuario comprueba que el nombre de usuario sea unico.
           Devuelve True si esta disponible para usar.
        '''
        if len(list(DB.usuarios.find({"nombre":nombre_usuario}))) == 0:
            if len(list(DB.usuarios.find({"id_usuario":id_usuario}))) == 0:
                return True

        return False


    def __init__(self, data):
        '''
            Contructor de la clase Usuario.
        '''
        self.nombre = data["nombre"]
        self.id_usuario = data["id_usuario"]

    def guardar(self):
        '''
            Guarda un lugar en la base de datos
        '''
        if not Usuario.check_usuario(self.nombre,self.id_usuario):
            raise Exception
        return DB.usuarios.insert_one(self.__dict__).inserted_id

    def diccionarizar(self):
        '''
            Prepara los objetos para enviar.
        '''
        d_usuario = self.__dict__
        d_usuario['_id'] = ""
        return d_usuario
