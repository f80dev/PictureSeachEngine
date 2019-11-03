import datetime

import pymongo as pymongo
from bson import ObjectId

import tools

db:pymongo.mongo_client=None

def init_database(server=None):
    if server is None:server=db_settings["server"]
    db:pymongo.mongo_client=create_database(
        server,db_settings["port"],
        db_settings["username"],db_settings["password"]
    )

def create_database(domain:str,port:str="27017",username="admin",password="admin_password",dbname="PSE_db"):
    if not "localhost" in domain:
        domain="admin:hh4271@"+domain

    url_base = "mongodb://" + domain + ":"+port+"/"
    print("ouverture de la base sur " + url_base)

    db=pymongo.MongoClient(url_base)[dbname]
    db["queries"]

    return db


#chargement des paramètres liés à la base de données
db_settings=tools.settings("database")



def write_query(query:str,identity):
    record=dict({
        "_id":ObjectId(),
        "query":query,
        "user":identity["username"],
        "dtCreate":datetime.datetime.now()
    })
    #On pourrait faire une sauvegarde mais l'usage de replace_one permet également de faire des update
    db["queries"].replace_one(filter={"_id":record["_id"]},replacement=record,upsert=True)
