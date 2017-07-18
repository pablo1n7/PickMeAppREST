# -*- coding: utf-8 -*-
import json
from models.models import Usuario, Lugar
from flask import Flask, request,\
     render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__, static_folder='statics')
app.config.from_pyfile('flaskapp.cfg',)
socketio = SocketIO(app)

clients = {}

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

@app.route("/getusuarios")
def get_usuarios():
    '''
        Retorna los usuarios    
    '''
    usuarios = Usuario.get_usuarios()
    return json.dumps(usuarios)


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

@app.route("/guardarusuario",methods=['POST'])
def guardar_usuario():
    '''
        Guardar usuario en la base de datos. Devuelve error

        El json que se envia por POST tiene la siguiente forma:
            {"nombre": "usuario1n7", "id_usuario": "33778434611"}

    '''
    try:
        usr = Usuario(request.get_json())
        usr.guardar()
    except Exception:
        return json.dumps({'estado': 'ERROR', 'descripcion':'Usuario en uso'})
    return json.dumps({'estado':'OK'})


@socketio.on('message')
def enviar_mensaje(origen, destinatorio, mensaje):
    '''
        Mensajeria por socketIO. Evento "message".
    '''
    emit("message", {"origen":origen,"mensaje":mensaje}, room=clients[destinatorio])

@socketio.on('connect')
def connect():
    '''
        Metodo de conexion, que ademas registra las conexiones activas.
    '''
    user_id = request.args.get('user_id', '')
    clients[user_id] = request.sid
    print('Client Connect {}'.format(user_id))

@socketio.on('disconnect')
def disconnect():
    '''
        Metodo de desconeccion, elimina la conexion de la lista de conexiones activas.
    '''
    for key in list(clients.keys()):
        if clients[key] == request.sid:
            print('Client disconnected')
            del clients[key]

def main():
    '''Metodo principal'''
    socketio.run(app,port=5000)

if __name__ == '__main__':
    main()
