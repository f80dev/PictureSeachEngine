"""
Librairie contenant la classe DAO d'accès à la base de données
"""
import datetime
import pymongo as pymongo
from bson import ObjectId

from tools import decodeToken

class dao:
    """
    Couche d'accès à la base de données MongoDB
    Dans l'exemple, la base MongoDB permet de tracer les appels à l'API
    """
    db=None

    def __init__(self,server,username,password,port=27017):
        """
        le constructeur recoit les paramètres pour se connecter à la base au lancement de docker
        :param server:  doit contenir uniquement le domaine du serveur mongoDB
        :param username: d'un user déclarer dans la base
        :param password:
        :param port: le port par défaut est le 27017
        """
        url_base = "mongodb://" + username+":"+password+"@"+server + ":"+str(port)+"/"
        self.db=pymongo.MongoClient(url_base)["PSE_db"]

    def add_user(self,username,password):
        """
        Ajoute un utilisateur à la base de données
        :param username: peut être un email ou n'importe quelle chaine de caractères
        :param password:
        :return: l'utilisateur est retourné sous forme d'un dictionnaire
        """
        user=dict({
            "username":username,
            "password":password
        })
        self.db["users"].insert_one(user)
        return user

    def get_user(self,token):
        """
        Décrypte le token pour en extraire le user et mot de passe et interroge la base de données pour s'assurer que
        l'utilisateur est présent
        :param token:
        :return:
        """
        username,password=decodeToken(token)
        return self.db["users"].find({"username":username,"password":password})


    def write_query(self,query:str,token):
        """
        Ecrit une requête dans la base, pour y envisager un suivi et/ou une facturation
        :param query:
        :param token:
        :return:
        """
        record=dict({
            "_id":ObjectId(),
            "query":query,
            "user":token,
            "dtCreate":datetime.datetime.now().timestamp()
        })
        print("Ecriture en base")
        self.db["queries"].insert_one(record)
