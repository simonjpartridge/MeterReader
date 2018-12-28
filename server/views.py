import datetime
import time
import os
import _strptime

from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from peewee import fn

from constants import PIP_WH, KWH_CONSUMPTION_PRICE, KWH_GENERATION_PRICE
from models import pips_db, Pip

app = Flask(__name__, static_url_path='/static',
            static_folder='../frontend/dist/')

CORS(app)


@app.before_request
def _db_connect():
    pips_db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not pips_db.is_closed():
        pips_db.close()


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
        Pip.created.between(midnight, now)
    ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy": wh})


@app.route("/api/historical/last24")
def get_pips_last_24():
    now = datetime.datetime.now()

    day_ago = now - datetime.timedelta(days=1)

    pips_in_day = Pip.select().where(
        Pip.created.between(day_ago, datetime.datetime.now())
    ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy": wh})


@app.route("/api/historical/hourly")
def get_pips_hourly():
    now = datetime.datetime.now()

    midnight = datetime.date.today()

    query = Pip.select(fn.COUNT(Pip.created).alias('count'), Pip.created).where(
        Pip.created.between(midnight, now)).group_by(fn.date_trunc('hour', Pip.created))

    # print(query)

    result = {}
    for pip in query:
        count = pip.count
        pip_hour = pip.created.hour

        result[str(pip_hour)] = count * PIP_WH

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
        all_pips[pip.id] = pip.created

    return jsonify(all_pips)


@app.route("/api/instantaneous")
def get_instantaneous():
    most_recent_2 = Pip.select().order_by(Pip.created.desc()).limit(2)

    # most_recent_2 = Pip.select()

    if len(most_recent_2) > 1:
        recent = most_recent_2[0]
        prev = most_recent_2[1]

        delta = recent.created - prev.created

        hours = delta.total_seconds() / (60 * 60)

        try:
            power = 1 / hours  # power in watts
        except: #div 0
            power = 0 

        time_since_last_pip = (datetime.datetime.now() - recent.created).total_seconds()

        #TODO: work out power when no update for a while

        if time_since_last_pip > 60:
            power = 0

        result = {"power": power, "seconds_since_update": time_since_last_pip}

        return jsonify(result)

    else:
        return jsonify({"error": "not enough pips registered"})


@app.route("/api/pip")
@app.route("/api/pip/<string:pip_time>")
def pip(pip_time=None):
    if not pip_time:
        return jsonify({"success":"false", "error":"no time supplied"})

    try:
        pip_time = datetime.datetime.fromtimestamp(float(pip_time))
    except:
        return jsonify({"success":"false", "error":"couldn't convert to unix epoch time"})
    
    new_pip = Pip(created = pip_time)
    new_pip.save()
    return jsonify({"success": "true"})


# def aggregate():



if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0',port=80)
