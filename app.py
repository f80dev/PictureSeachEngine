"""
Fichier principal d'installation et d'éxécution des APIs
"""

import ssl
import sys
from flask_restplus import Resource, Api, reqparse
from flask_cors import CORS
import dao
from flask import Flask, jsonify, request
from tools import token_required, createToken, settings, queryUnsplash, queryPixabay

authorizations={
    "apikey":{
        "type":"apiKey",
        "in":"header",
        "name":"access_token"
    }
}

#Initialisation du moteur d'execution de l'API
app = Flask(__name__)
CORS(app)
api = Api(app,authorizations=authorizations)
#Instanciation de la couche de données
#Les paramètres seront passés à l'installation de l'image Docker

#L'ensemble des paramètres d'accès à la base de données sont passés dans la commande
#docker qui lance le serveur
dao=dao.dao(server=sys.argv[2],username=sys.argv[3],password=sys.argv[4])

#http://localhost:8090/index.html?server=http://localhost&port=5800
#Mise en place de l'API d'obtention du token sur base d'un couple user/mot de passe_____________________________________
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', required=True,type=str, help='username to use the API')
auth_parser.add_argument('password', required=True,type=str, help='password to use the API')
@api.route("/auth")
class Developer(Resource):
    """
    Classe représentant les comptes développeurs habilités à utiliser les API
    """
    @api.expect(auth_parser)
    @api.response(200, 'Access Token à utiliser pour interroger le moteur PSE')
    def get(self):
        """
        Inscrit l'utilisateur dans la base de données et retourne un token d'accès
        :return:
        """
        args = auth_parser.parse_args()
        dao.add_user(args["username"],args["password"])
        return jsonify(dict({"access_token":createToken(args["username"],args["password"])}))



#Paramétrage des API ___________________________________________________________________________________________________
#Fixer les paramétres du parser
#Le parser va permètre d'analyser les paramètres supplémentaire de la requete d'interogration des moteurs
parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, help='Number of images return')
parser.add_argument('quality', type=bool, help='Ask for best quality')

@api.route(settings("api")["endpoint"]+"/<string:query>",endpoint=settings("api")["endpoint"])
@api.param('query', "Requête pour intérroger les bases de données d'image")
@api.doc(security="apikey")
class Image(Resource):
    """
    Représentation des photos retournées par l'API
    """
    @api.response(200,'Liste des urls des photos correspondant à la requête')
    @api.response(500,'Erreur technique du serveur')
    @api.expect(parser)
    @token_required(dao)
    def get(self,query):
        """
        API principale d'interrogation des plateformes
        :param query: contient le mot clé à transmettre aux plateformes de photos
        :return: liste consolidée d'urls
        """
        args = parser.parse_args()
        #va nous permettre de parser automatiquement les paramètres

        #Ici on appel le service pixabay pour récupérer des images
        rc=queryPixabay(query,args["limit"]/2,args["quality"])

        limit=len(rc)-args["limit"]
        #On ajoute les images de unspash
        for pict in queryUnsplash(query,limit):
            rc.append(pict)

        #Chaque requête est enregistrée pour la gestion des quotas et d'une éventuelle facturation
        dao.write_query(query,request.headers["access_token"])

        return jsonify(rc)


if __name__ == '__main__':
    #La fonction principale se charge de lancer l'instance Flask en tenant compte
    #des options passées via la commande docker

    #Le passage du port en paramètre permet de choisir celui-ci via la commande docker de lancement
    #du serveur
    _port=sys.argv[1]
    if "debug" in sys.argv:
        app.run(host="0.0.0.0",port=_port,debug=True)
    else:
        if "ssl" in sys.argv:
            #Le context de sécurisation est chargé avec les certificats produit par "Let's Encrypt"
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain("/app/certs/fullchain.pem", "/app/certs/privkey.pem")
            app.run(host="0.0.0.0", port=_port, debug=False, ssl_context=context)

        else:
            # Le serveur peut être déployé en mode non sécurisé
            # cela dit la plus part des front-end ne peuvent être hébergés qu'en mode https
            # ils ne peuvent donc appeler que des serveurs en https. Il est donc préférable
            # de déployer l'API sur un serveur sécurisé
            app.run(host="0.0.0.0", port=_port, debug=False)
