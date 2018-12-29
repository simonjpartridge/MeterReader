import os
from peewee import DateTimeField, BooleanField, IntegerField, Model
import datetime

from server import db


class Pip(Model):
    time = DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        database = db


class Minute(Model):
    time = DateTimeField(index=True, unique=True)
    pips = IntegerField(default=1)

    class Meta:
        database = db


class Hour(Model):
    time = DateTimeField(index=True, unique=True)
    pips = IntegerField(default=1)

    class Meta:
        database = db


class Day(Model):
    time = DateTimeField(index=True, unique=True)
    pips = IntegerField(default=1)

    class Meta:
        database = db




db.create_tables([Pip, Minute, Hour, Day])
db.close()


