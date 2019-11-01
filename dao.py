import pymongo as pymongo

import tools

def create_database(domain:str,port:str="27017",username="admin",password="admin_password",dbname="PSE_db"):
    if not "localhost" in domain:
        domain="admin:hh4271@"+domain

    url_base = "mongodb://" + domain + ":"+port+"/"
    print("ouverture de la base sur " + url_base)

    return pymongo.MongoClient(url_base)[dbname]


db_settings=tools.settings()["database"]
db:pymongo.mongo_client=create_database(
    db_settings["server"],
    db_settings["port"],
    db_settings["username"],
    db_settings["password"]
)

def write_query(query:str,result:str):
    record=dict({"_id":query,"result":result})
    #On pourrait faire une sauvegarde mais l'usage de replace_one permet également de faire des update
    db["queries"].replace_one(filter={"_id":record["_id"]},replacement=record,upsert=True)

def read_query(query:str):
    return db["queries"][query]
