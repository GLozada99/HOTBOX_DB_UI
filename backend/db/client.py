from typing import Iterable, Mapping

from pymongo import MongoClient


class MongoDBClient:

    def __init__(self, username: str, password: str, db_name: str,
                 collection_name: str):
        self.db_name = db_name
        self.collection_name = collection_name

        self.connection_string = (
            "mongodb://"
            f"{username}:{password}@localhost:27017"
            f"/{db_name}?authSource=admin&retryWrites=true&w=majority")

    def persist_data_db(self, data: dict):
        collection = self.connection[self.collection_name]
        collection.insert_one(data)

    def get_data_db(self, quantity: int) -> Iterable[Mapping]:
        collection = self.connection[self.collection_name]
        data = collection.find().sort("_id", -1).limit(quantity)

        return data

    def __enter__(self):
        self.connection = MongoClient(self.connection_string)[self.db_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.client.close()
