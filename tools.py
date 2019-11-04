import urllib
import yaml
from flask import json

#Fonction de récupération des paramètres du serveur
def settings(field=""):
    with open('settings.yaml') as json_file:
        if field=="":
            return yaml.load(json_file)
        else:
            return yaml.load(json_file)[field]


#retourne un user par le username et password
def getUser(username="",password="",id=""):
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


def queryUnsplash(query):
    unsplash_settings = settings("sources")["unsplash"]
    url = unsplash_settings["endpoint"] + "search/photos?query="+query+"&client_id=" + unsplash_settings["key"]

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["results"]:
        rc.append(image["urls"]["raw"])

    return rc