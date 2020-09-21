import os

from dotenv import load_dotenv
from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField

load_dotenv()
db = SqliteDatabase(os.environ.get('DB_FILE_PATH'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    telegram_id = CharField(unique=True)
    authorized = IntegerField()
    status = CharField()


class Equipment(BaseModel):
    it_id = CharField(unique=True)
    invent_num = CharField()
    type = CharField()
    mark = CharField()
    model = CharField()
    serial_num = CharField()


class Movement(BaseModel):
    it_id = ForeignKeyField(Equipment, backref='equipment')
    korpus = CharField()
    room = CharField()


def initialize_db():
    db.connect()
    db.create_tables([
        User,
        Equipment,
        Movement
    ], safe=True)
