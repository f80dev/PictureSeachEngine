import urllib

from flask import json

def settings():
    with open('settings.json') as json_file:
        return json.load(json_file)

set_sources=settings()["sources"]

#retourne un user par le username et password
def getUser(username="",password="",id=""):
    for c in settings()["api_users"]:
        if len(username)>0 and len(password)>0:
            if c["username"]==username and password==c["password"]:return c
        else:
            if c["id"]==id: return c

    return None




def queryPixabay(query:str,limit:int=20,quality:bool=False):
    url=set_sources["pixabay"]["endpoint"]+"?per_page="+str(limit)+"&image_type=photo&key=" + set_sources["pixabay"]["key"] + "&q=" + query
    if quality:url=url+"&editors_choice=true"

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc

