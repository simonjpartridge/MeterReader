import os
from peewee import DateTimeField, BooleanField, SqliteDatabase, Model
import datetime
# import 

pips_db = SqliteDatabase(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'pips.db'))


class Pip(Model):
    created = DateTimeField(default=datetime.datetime.now, index=True)
    # created = FloatField(index=True)
    summarised = BooleanField(default=False, index=True)
    # device_id = IntegerField(index=True)

    class Meta:
        database = pips_db


# class Minutely(Model):
#     time = DateTimeField(index=True, unique=True)
#     pips = IntegerField(default=0)

#     class Meta:
#         database = pips_db


# class Hourly(Model):
#     time = DateTimeField(index=True, unique=True)
#     pips = IntegerField(default=0)

#     class Meta:
#         database = pips_db


pips_db.create_tables([Pip])
pips_db.close()


