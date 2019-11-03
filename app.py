import ssl
import sys
import flask_jwt
from flask_jwt import jwt_required, JWT
from flask_restplus import Resource, Api,reqparse
from flask_cors import CORS

import dao
import user
import tools

from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'hh4280!!'
api = Api(app)
dao.init_database(sys.argv[1])

parser = reqparse.RequestParser()

#Fixer les paramétres du parser
parser.add_argument('limit', type=int, help='Images return')
parser.add_argument('quality', type=bool, help='Best quality')

def authenticate(username, password):
    return user.User(tools.getUser(username=username,password=password))

def identity(payload):
    return tools.getUser(id=payload['identity'])

#http://localhost:5000/images/dogs?limit=10&quality=true
#https://server.f80.fr:5600/dogs/10/true

jwt = JWT(app, authenticate, identity)

@api.route("/"+tools.settings("api")["endpoint"]+"/<string:query>")
@api.doc(params={'query': "Requête pour intérroger les bases de données d'image"})
class Image(Resource):
    @api.doc(responses={
        200: 'Liste des urls des photos correspondant à la requête',
        404: 'Aucune image disponible par rapport à la requête'
    })

    @api.expect(parser)
    @jwt_required()
    def get(self,query):
        args = parser.parse_args() #va nous permettre de parser automatiquement les paramètres

        #Ici on appel le service pixabay pour récupérer des images
        rc=tools.queryPixabay(query,args["limit"],args["quality"])

        #Chaque requête est enregistrée pour la gestion des quotas et d'une éventuelle facturation
        dao.write_query(query,flask_jwt.current_identity)

        return jsonify(rc)



if __name__ == '__main__':
    _port=sys.argv[2]
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
            #Le serveur peut fonctionner en mode non sécurisé, dans ce cas aucun certificat n'est nécéssaire
            app.run(host="0.0.0.0", port=_port, debug=False)



