import time

from decouple import config

from db.client import MongoDBClient


def main():
    data = ({"bla": 1212, "blabla": time.time()} for _ in range(5))

    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "test",
    )
    with client:
        for d in data:
            client.persist_data_db(d)

        for a in client.get_data_db(200):
            print(a)


if __name__ == "__main__":
    main()
