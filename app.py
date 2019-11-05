import ssl
import sys
from flask_restplus import Resource, Api, reqparse
from flask_cors import CORS

import dao
from flask import Flask, jsonify, request
from tools import token_required, createToken, settings, queryUnsplash, queryPixabay

app = Flask(__name__)
CORS(app)

authorizations={
    "apikey":{
        "type":"apiKey",
        "in":"header",
        "name":"access_token"
    }
}

api = Api(app,authorizations=authorizations)
dao=dao.dao(sys.argv[2],sys.argv[3],sys.argv[4])


#Fonctions de gestion des token ________________________________________________________________

#def authenticate(username, password):
#    return user.User(tools.getUser(username=username,password=password))

#def identity(payload):
#    return tools.getUser(id=payload['identity'])

#Mise en place des fonctions
#jwt = JWT(app, authorizations, identity)


#http://localhost:8090/index.html?server=http://localhost&port=5800

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', required=True,type=str, help='username to use the API')
auth_parser.add_argument('password', required=True,type=str, help='password to use the API')
@api.route("/auth")
class Developer(Resource):
    @api.expect(auth_parser)
    @api.doc(responses={200: 'Access token correspondant'})
    def get(self):
        args = auth_parser.parse_args()
        return jsonify(dict({"access_token":createToken(args["username"],args["password"])}))

#Paramétrage des API _________________________________________________________________________
#Fixer les paramétres du parser
parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, help='Number of images return')
parser.add_argument('quality', type=bool, help='Ask for best quality')
@api.route("/<string:query>",endpoint=settings("api")["endpoint"])
@api.doc(params={'query': "Requête pour intérroger les bases de données d'image"})
@api.doc(security="apikey")
class Image(Resource):
    @api.doc(responses={
        200: 'Liste des urls des photos correspondant à la requête',
        404: 'Aucune image disponible par rapport à la requête'
    })

    @api.expect(parser)
    @token_required
    def get(self,query):
        args = parser.parse_args() #va nous permettre de parser automatiquement les paramètres

        #Ici on appel le service pixabay pour récupérer des images
        rc=queryPixabay(query,args["limit"],args["quality"])

        #On ajoute les images de unspash
        for pict in queryUnsplash(query):
            rc.append(pict)

        #Chaque requête est enregistrée pour la gestion des quotas et d'une éventuelle facturation
        dao.write_query(query,request.headers["access_token"])

        return jsonify(rc)



if __name__ == '__main__':
    _port=sys.argv[1]
    if "debug" in sys.argv:
        app.run(host="0.0.0.0",port=_port,debug=True)
    else:
        #Le serveur peut être déployé en mode non sécurisé
        #cela dit la plus part des front-end ne peuvent être hébergés quand mode https
        #ils ne peuvent donc appeler que des serveurs en https. Il est donc préférable
        #de déployer l'API sur un serveur sécurisé
        if "ssl" in sys.argv:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain("/app/certs/fullchain.pem", "/app/certs/privkey.pem")
            app.run(host="0.0.0.0", port=_port, debug=False, ssl_context=context)
        else:
            #Le serveur peut fonctionner en mode non sécurisé, dans ce cas aucun certificat n'est nécéssaire
            app.run(host="0.0.0.0", port=_port, debug=False)



