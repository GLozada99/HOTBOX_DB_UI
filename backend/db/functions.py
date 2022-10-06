from pymongo import MongoClient
from decouple import config

COLLECTION_NAME = "measurements"


def persist_data_db(data: dict):
    dbname = get_database()
    collection = dbname[COLLECTION_NAME]
    collection.insert_one(data)


def get_database():
    DB_USERNAME = config('MONGO_USERNAME')
    DB_PASSWORD = config('MONGO_PASSWORD')
    DB_NAME = config('MONGO_DBNAME')

    CONNECTION_STRING = ("mongodb://" 
                         f"{DB_USERNAME}:{DB_PASSWORD}@localhost:27017"
                         f"/{DB_NAME}?authSource=admin&retryWrites=true&w"
                         f"=majority")

    client = MongoClient(CONNECTION_STRING)

    return client[DB_NAME]
