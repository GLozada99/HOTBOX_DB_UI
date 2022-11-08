from typing import Iterable, Mapping

from decouple import config
from pymongo import MongoClient

COLLECTION_NAME = "measurements"


class MongoDBClient:

    def __init__(self):
        DB_USERNAME = config('MONGO_USERNAME')
        DB_PASSWORD = config('MONGO_PASSWORD')
        self.DB_NAME = config('MONGO_DBNAME')

        self.connection_string = (
            "mongodb://"
            f"{DB_USERNAME}:{DB_PASSWORD}@localhost:27017"
            f"/{self.DB_NAME}?authSource=admin&retryWrites=true&w=majority")

    def persist_data_db(self, data: dict):
        collection = self.connection[COLLECTION_NAME]
        collection.insert_one(data)

    def get_data_db(self, quantity: int) -> Iterable[Mapping]:
        collection = self.connection[COLLECTION_NAME]
        data = collection.find().sort("_id", -1).limit(quantity)

        return data

    def __enter__(self):
        self.connection = MongoClient(self.connection_string)[self.DB_NAME]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.client.close()
