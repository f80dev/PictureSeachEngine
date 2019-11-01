import ssl
import sys

from flask_jwt import jwt_required, JWT
from flask_restplus import Resource, Api,reqparse
from flask_cors import CORS
from werkzeug.security import safe_str_cmp

import dao
import user
import tools

from flask import Flask, jsonify


app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SECRET_KEY'] = 'hh4280!!'

parser = reqparse.RequestParser()

users = [user.User(1, 'hhoareau', 'hh4271'),user.User(2, 'paul.dudule', 'hh4271')]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

#Fixer les paramétres du parser
parser.add_argument('limit', type=int, help='Images return')
parser.add_argument('quality', type=bool, help='Best quality')

#Initier les utilisateurs
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

#http://localhost:5000/images/dogs?limit=10&quality=true
#https://server.f80.fr:5600/dogs/10/true

jwt = JWT(app, authenticate, identity)

@api.route('/images/<string:query>')
@api.doc(params={'query': "Requête pour intérroger les bases de données d'image"})
class Image(Resource):
    @jwt_required()
    @api.doc(responses={
        200: 'Liste des urls des photos correspondant à la requête',
        404: 'Aucune image disponible par rapport à la requête'
    })
    @api.expect(parser)
    def get(self,query):
        args = parser.parse_args() #va nous permettre de parser automatiquement les paramètres
        key=query+str(args["limit"])+str(args["quality"])
        rc=dao.read_query(key)
        if rc is None:
            rc=tools.queryPixabay(query,args["limit"],args["quality"])
            dao.save_query(key,rc)

        return jsonify(rc)



if __name__ == '__main__':
    _port=5600
    if "debug" in sys.argv:
        app.run(host="0.0.0.0",port=_port,debug=True)
    else:
        #Le serveur peut être déployé en mode non sécurisé
        #cela dit la plus part des front-end ne peuvent être hébergés quand mode https
        #ils ne peuvent donc appeler que des serveurs en https. Il est donc préférable
        #de déployer l'API sur un serveur sécurisé
        if "ssl" in sys.argv:
            print("Activation du ssl")
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain("/app/certs/fullchain.pem", "/app/certs/privkey.pem")
            app.run(host="0.0.0.0", port=_port, debug=False, ssl_context=context)
        else:
            app.run(host="0.0.0.0", port=_port, debug=False)



