import datetime
import pymongo as pymongo
from bson import ObjectId

#Implémentation de la couche d'accès à la base de données
#Dans l'exemple, la base MongoDB permet de tracer les appels à l'API
class dao:
    db=None

    def __init__(self,server,username,password,port=27017):
        url_base = "mongodb://" + username+":"+password+"@"+server + ":"+str(port)+"/"
        self.db=pymongo.MongoClient(url_base)["PSE_db"]


    def write_query(self,query:str,identity):
        record=dict({
            "_id":ObjectId(),
            "query":query,
            "user":identity["username"],
            "dtCreate":datetime.datetime.now().timestamp()
        })
        print("Ecriture en base")
        self.db["queries"].insert_one(record)