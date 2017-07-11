# -*- coding: utf-8 -*-
import json
from models.models import Usuario, Lugar
from flask import Flask, request,\
     render_template 

app = Flask(__name__, static_folder='statics')
app.config.from_pyfile('flaskapp.cfg',)

@app.route("/")
def index():
    ''' Retorna la pagina principal '''
    return render_template("index.html")


@app.route("/getlugares/<usuario_nombre>")
@app.route("/getlugares")
def get_lugares(usuario_nombre=None):
    '''
        Retorna los lugares agregados por un usuario
            si usuario_nombre!=None regresa todos  los lugares
    '''
    lugares = Lugar.get_lugares(usuario_nombre)
    return json.dumps(lugares)


@app.route("/getlugar/<nombre_lugar>")
def get_lugar(nombre_lugar=None):
    '''
        TODO: capaz que se prodia agregar nombre_usuario tambien,
            para que el filtro se mas exacto

        Retorna el lugar con nombre = nombre_lugar
    '''
    lugar = Lugar.get_lugar(nombre_lugar)
    return json.dumps(lugar)


@app.route("/guardarlugar",methods=['POST'])
def guardar_lugar():
    '''

        TODO: si vamos a hacer un login en el dispositivo, el metodo 'guardarlugar'
            recibiría un id en vez de un nombre o algo asi. Me parece excesivo igual

        Metodo que guarda un lugar. El json que se envia por POST tiene la siguiente forma:
            {"nombre": "CASA", "latlng": "2222/222", "descripcion": "es mi lugar", "usuario":"pablo1n7"}

    '''
    lugar = Lugar(request.get_json())
    lugar.guardar()
    return json.dumps({'status':'OK'})

def main():
    '''Metodo principal'''
    app.run()

if __name__ == '__main__':
    main()
