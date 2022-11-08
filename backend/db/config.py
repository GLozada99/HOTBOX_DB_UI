from typing import Mapping

from decouple import config

from db.client import MongoDBClient


def get_config() -> Mapping:
    client_config = MongoDBClient(
        config('MONGO_USERNAME'), config('MONGO_PASSWORD'),
        config('MONGO_DB_NAME'), 'config',
    )
    with client_config:
        if config_data := list(client_config.get_data_db(1)):
            return config_data[0]
        data = {
            'SETO_POINTO': config('SETO_POINTO', float),
            'TIME': config('TIME', int),
        }
        client_config.persist_data_db(data)
        return data


def set_config(seto_pointo: float, time: int) -> Mapping:
    client_config = MongoDBClient(
        config('MONGO_USERNAME'), config('MONGO_PASSWORD'),
        config('MONGO_DB_NAME'), 'config',
    )
    with client_config:
        data = {
            'SETO_POINTO': seto_pointo,
            'TIME': time,
        }
        client_config.persist_data_db(data)
        return data
