import datetime
import time
import os
import _strptime

from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from peewee import fn

from server import app, db
from server.constants import PIP_WH, KWH_CONSUMPTION_PRICE, KWH_GENERATION_PRICE
from server.models import Pip, Minute, Hour, Day




@app.before_request
def _db_connect():
    db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.route("/")
def hello():
    return redirect("/static/index.html", code=302)

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory('../frontend/dist/css', path)


@app.route("/js/<path:path>")
def js(path):
    return send_from_directory('../frontend/dist/js', path)


@app.route("/api/historical/today")
def get_pips_today():
    now = datetime.datetime.now()
    midnight = datetime.date.today()

    # day_ago = now - datetime.timedelta(days=1)
    pips_in_day = Pip.select().where(
        Pip.time.between(midnight, now)
    ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy": wh})


@app.route("/api/historical/last24")
def get_pips_last_24():
    now = datetime.datetime.now()

    day_ago = now - datetime.timedelta(days=1)

    pips_in_day = Pip.select().where(
        Pip.time.between(day_ago, datetime.datetime.now())
    ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy": wh})


@app.route("/api/historical/hourly/today")
def get_pips_hourly():
    now = datetime.datetime.now()

    midnight = datetime.date.today()

    query = Hour.select().where(
        Hour.time.between(midnight, now)
    )

    result = {}
    for item in query:
        pips = item.pips

        hour = item.time.hour

        result[str(hour)] = pips * PIP_WH
    
    times = []
    values = []

    for i in range(0, now.hour+1):
        times.append(str(i))
        if str(i) not in result:
            values.append(0)
        else:
            values.append(result[str(i)])

    return jsonify({"times": times, "values": values})


@app.route('/api/price/consumption')
def get_consumption_price():
    return jsonify({"price": KWH_CONSUMPTION_PRICE})


@app.route('/api/price/generation')
def get_generation_price():
    return jsonify({"price": KWH_GENERATION_PRICE})


@app.route("/api/get_all_pips")
def get_all_pips():
    all_pips = {}
    for pip in Pip.select():
        all_pips[pip.id] = {"time":pip.time}

    return jsonify(all_pips)


@app.route("/api/get_all_minutes")
def get_all_minutes():
    all_minutes = {}
    for minute in Minute.select():
        all_minutes[minute.id] = {"time": minute.time,
                            "pips": minute.pips}

    return jsonify(all_minutes)


@app.route("/api/get_all_hours")
def get_all_hours():
    all_hours = {}
    for hour in Hour.select():
        all_hours[hour.id] = {"time": hour.time,
                                  "pips": hour.pips}

    return jsonify(all_hours)


@app.route("/api/instantaneous")
def get_instantaneous():
    most_recent_2 = Pip.select().order_by(Pip.time.desc()).limit(2)

    if len(most_recent_2) > 1:
        recent = most_recent_2[0]
        prev = most_recent_2[1]

        delta = recent.time - prev.time

        hours = delta.total_seconds() / (60 * 60)

        try:
            power = 1 / hours  # power in watts
        except: #div 0
            power = 0 

        time_since_last_pip = (datetime.datetime.now() - recent.time).total_seconds()

        #TODO: work out power when no update for a while

        if time_since_last_pip > 60:
            power = 0

        result = {"power": power, "seconds_since_update": time_since_last_pip}

        return jsonify(result)

    else:
        return jsonify({"error": "not enough pips registered"})


@app.route("/api/pip/<string:pip_time>")
def pip(pip_time=None):
    if not pip_time:
        return jsonify({"success":"false", "error":"no time supplied"})
    try:
        pip_time = datetime.datetime.fromtimestamp(float(pip_time))
    except:
        return jsonify({"success":"false", "error":"couldn't convert to unix epoch time"})

    with db.atomic():
        new_pip = Pip(time=pip_time)
        new_pip.save()

        #add pips to hourly and minutely and daily database
        add_pip_minute(pip_time)
        add_pip_hour(pip_time)
        add_pip_day(pip_time)

    return jsonify({"success": "true"})


def add_pip_minute(pip_time):
    pip_minute = pip_time.replace(second=0, microsecond=0)

    result = Minute.select().where(Minute.time==pip_minute).limit(1)
    if len(result) == 1:
        minute = result[0]
        minute.pips += 1
        minute.save()
    else:
        new_minute = Minute(time=pip_minute)
        new_minute.save()

def add_pip_hour(pip_time):
    pip_hour = pip_time.replace(minute=0, second=0, microsecond=0)

    result = Hour.select().where(Hour.time==pip_hour).limit(1)
    if len(result) == 1:
        hour = result[0]
        hour.pips += 1
        hour.save()
    else:
        new_hour = Hour(time=pip_hour)
        new_hour.save()

def add_pip_day(pip_time):
    pip_day = pip_time.replace(hour=0, minute=0, second=0, microsecond=0)

    result = Day.select().where(Day.time==pip_day).limit(1)
    if len(result) == 1:
        day = result[0]
        day.pips += 1
        day.save()
    else:
        new_Day = Day(time=pip_day)
        new_Day.save()












if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0',port=80)
