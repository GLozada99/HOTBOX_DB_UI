import datetime
import tempfile

from decouple import config
from faker import Faker

from box.data_save import write_data
from db.client import MongoDBClient

client = MongoDBClient(
    config("MONGO_USERNAME"),
    config("MONGO_PASSWORD"),
    config("MONGO_DBNAME"),
    "measurements",
)
fake = Faker()
with client, tempfile.NamedTemporaryFile() as tmp:
    for _ in range(500):
        write_data(
            datetime.datetime.now(),
            [fake.pyfloat(left_digits=2, right_digits=1, positive=True,
                          min_value=69.5, max_value=71.2) for _ in range(10)],
            fake.pyfloat(left_digits=3, right_digits=2, positive=True,
                         min_value=250, max_value=300),
            fake.pyfloat(left_digits=3, right_digits=2, positive=True,
                         min_value=250, max_value=300),
            fake.pyfloat(left_digits=3, right_digits=2, positive=True,
                         min_value=100, max_value=115),
            fake.pyfloat(left_digits=0, right_digits=5, positive=True,
                         min_value=0.3, max_value=0.5),
            tmp.name,
            client,
        )
