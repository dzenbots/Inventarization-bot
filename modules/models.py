from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField

from modules.settings import DB_FILE_PATH

db = SqliteDatabase(DB_FILE_PATH)


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
    is_modified = CharField()


class Movement(BaseModel):
    it_id = ForeignKeyField(Equipment, backref="movements")
    korpus = CharField()
    room = CharField()


def initialize_db():
    db.connect()
    db.create_tables([
        User,
        Equipment,
        Movement
    ], safe=True)
