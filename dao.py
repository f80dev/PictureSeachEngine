import datetime

import pymongo as pymongo
from bson import ObjectId

import tools

class dao:
    db=None
    #chargement des paramètres liés à la base de données
    db_settings=tools.settings("database")

    def __init__(self,server=None,username=None,password=None):
        if server is None:server=self.db_settings["server"]
        if username is None:username=self.db_settings["username"]
        if password is None:password=self.db_settings["password"]

        url_base = "mongodb://" + username+":"+password+"@"+server + ":"+str(self.db_settings["port"])+"/"
        self.db=pymongo.MongoClient(url_base)["PSE_db"]
        self.db["queries"]


    def write_query(self,query:str,identity):
        record=dict({
            "_id":ObjectId(),
            "query":query,
            "user":identity["username"],
            "dtCreate":datetime.datetime.now()
        })
        #On pourrait faire une sauvegarde mais l'usage de replace_one permet également de faire des update
        self.db["queries"].replace_one(filter={"_id":record["_id"]},replacement=record,upsert=True)
