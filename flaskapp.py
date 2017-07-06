import os
import json
from flask import Flask, request, \
     render_template, send_file
from pymongo import MongoClient

app = Flask(__name__, static_folder='statics')
app.config.from_pyfile('flaskapp.cfg',)
#CLIENT = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
#DB = CLIENT.robocompdit

@app.route("/")
def index():
    ''' Retorna la pagina principal '''
    return render_template("index.html")

def main():
    '''Metodo principal'''
    app.run()

if __name__ == '__main__':
    main()
