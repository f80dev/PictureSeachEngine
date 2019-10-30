import urllib

from flask import json


def queryPixabay(query:str):
    pixabay_key = "5489947-2039fe3621c0de1cbb91d08c6"
    url="https://pixabay.com/api/?per_page=50&image_type=photo&key=" + pixabay_key + "&q=" + query
    with urllib.request.urlopen(url) as response:
        result=json.load(response)

    rc=list()
    for image in result["hits"]:
        rc.append(image["largeImageURL"])

    return rc

