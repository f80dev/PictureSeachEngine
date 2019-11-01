import urllib

from flask import json

def settings():
    with open('settings.json') as json_file:
        return json.load(json_file)

def queryPixabay(query:str,limit:int=20,quality:bool=False):
    pixabay_key = "5489947-2039fe3621c0de1cbb91d08c6"
    url="https://pixabay.com/api/?per_page="+str(limit)+"&image_type=photo&key=" + pixabay_key + "&q=" + query
    if quality:url=url+"&editors_choice=true"

    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc

