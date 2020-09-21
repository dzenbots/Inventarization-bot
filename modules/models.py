import os

from dotenv import load_dotenv
from peewee import Model, SqliteDatabase, CharField, IntegerField
load_dotenv()
db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    telegram_id = CharField(unique=True)
    authorized = IntegerField()
    status = CharField()


def initialize_db():
    db.connect()
    db.create_tables([
        User
    ], safe=True)
