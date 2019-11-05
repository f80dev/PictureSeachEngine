import urllib
import yaml
from flask import json, request
import jwt
from functools import wraps


#Fonction de récupération des paramètres du serveur
def settings(field=""):
    with open('settings.yaml') as json_file:
        if field=="":
            return yaml.load(json_file)
        else:
            return yaml.load(json_file)[field]


#retourne un user par le username et password
def getUser(username:str="",password:str="",id=""):
    for c in settings("api_users"):
        if len(username)>0 and len(password)>0:
            if c["username"]==username and password==c["password"]:return c
        else:
            if c["id"]==id: return c

    return None



#Interrogation de pixabay pour obtenir les images demandées via query
def queryPixabay(query:str,limit:int=10,quality:bool=False):
    pixabay_settings=settings("sources")["pixabay"]
    url=pixabay_settings["endpoint"]+"?per_page="+str(limit)+"&image_type=photo&key=" + pixabay_settings["key"] + "&q=" + query
    if quality:url=url+"&editors_choice=true"

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc


#Appel de l'API de unplash : voir https://unsplash.com/documentation#search-photos
def queryUnsplash(query):
    unsplash_settings = settings("sources")["unsplash"]
    url = unsplash_settings["endpoint"] + "search/photos?query="+query+"&per_page=20&client_id=" + unsplash_settings["key"]

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["results"]:
        rc.append(image["urls"]["raw"])

    return rc



#Gestion des token _____________________________________________________________________________________________________
#Décorateur pour s'assurer que le token est présent dans l'API décorée
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if 'access_token' in request.headers:
            token=request.headers["access_token"]
            json=decodeToken(token)
            #On vérifie que le couple (user,password) est présent dans le fichier de configuration
            #On aurait pu aussi utiliser un base de données
            if getUser(username=json["username"],password=json["password"]) is None:
                return {"message": "token unknown"}, 401

        if not token:
            return {"message":"token is missing"},401

        return f(*args,**kwargs)

    return decorated

#Création d'un token contenant un user / mot de passe
def createToken(username:str,password:str):
    return str(jwt.encode({'username': username,'password':password}, 'mon_super_secret', algorithm='HS256'),"utf-8")

#Décodage du token créer par createToken
def decodeToken(token:str):
    return jwt.decode(token, 'mon_super_secret', algorithms=['HS256'])
