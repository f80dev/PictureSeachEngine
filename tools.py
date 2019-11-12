"""
Librarie réunissant des fonctions de lecture du fichier de paramétrage,
les fonctions d'interrogation des bibliothéques d'images et les fonctions
de gestion des tokens
"""

import urllib
import yaml
from flask import json, request
import jwt
from functools import wraps

def settings(field=""):
    """
    Lecture des paramètres du fichier YAML de paramétrage
    :param field:
    :return:
    """
    with open('settings.yaml') as json_file:
        if field=="":
            return yaml.load(json_file)
        else:
            return yaml.load(json_file)[field]



def queryPixabay(query:str,limit:int=10,quality:bool=False):
    """
    Interrogation de pixabay pour obtenir les images demandées via query
    :param query: contient le mot clé à utiliser pour rechercher les images
    :param limit: nombre d'images retournées
    :param quality: permet de restreindre la recherche aux photos de l'éditeur
    :return: liste au format json des urls des photos correspondantes à la requête
    """
    pixabay_settings=settings("sources")["pixabay"]
    url=pixabay_settings["endpoint"]+"?per_page="+str(limit)+"&image_type=photo&key=" + pixabay_settings["key"] + "&q=" + query
    if quality:url=url+"&editors_choice=true"

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc



def queryUnsplash(query,limit=10):
    """
    Interrogation de pixabay pour obtenir les images demandées via query
    voir https://unsplash.com/documentation#search-photos
    :param query:  contient le mot clé à utiliser pour rechercher les images
    :return: liste au format json des urls des photos correspondant à la requête
    """
    unsplash_settings = settings("sources")["unsplash"]
    url = unsplash_settings["endpoint"] + "search/photos?query="+query+"&per_page="+str(limit)+"&client_id=" + unsplash_settings["key"]

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["results"]:
        rc.append(image["urls"]["raw"])

    return rc



#Gestion des token _____________________________________________________________________________________________________
def token_required(dao):
    """
    Décorateur en charge de vérifier la présence d'un token dans les appels
    :param dao:
    :return:
    """
    def decorated(f):
        def wrapper(*args,**kwargs):
            token=None
            if 'access_token' in request.headers:
                token=request.headers["access_token"]
                #On vérifie que le couple contenu dans le token est présent en base
                if dao.get_user(token=token) is None:
                    return {"message": "token unknown"}, 401

            if not token:
                return {"message":"token is missing"},401

            return f(*args, **kwargs)

        return wrapper
    return decorated


def createToken(username:str,password:str):
    """
    Création d'un token contenant un user / mot de passe
    :param username:
    :param password:
    :return: le token d'accès à l'api correspondant au couple user/mot de passe précédent
    """
    return str(jwt.encode({'username': username,'password':password}, 'mon_super_secret', algorithm='HS256'),"utf-8")



def decodeToken(token:str):
    """
    Décodage du token créé par createToken
    :param token:
    :return: couple user/password contenus dans le token
    """
    return jwt.decode(token, 'mon_super_secret', algorithms=['HS256'])
