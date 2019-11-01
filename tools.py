import urllib

from flask import json

def settings():
    with open('settings.json') as json_file:
        return json.load(json_file)

def queryPixabay(query:str,limit:int=20,quality:bool=False):
    sets=settings()["sources"]["pixabay"]
    url=sets["endpoint"]+"?per_page="+str(limit)+"&image_type=photo&key=" + sets["key"] + "&q=" + query
    if quality:url=url+"&editors_choice=true"

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc

