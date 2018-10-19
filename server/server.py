import _strptime
from peewee import *
from flask import Flask, jsonify, request, send_from_directory, redirect
import os

from flask_cors import CORS


import datetime

pips_db = SqliteDatabase(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'pips.db'))
app = Flask(__name__, static_url_path='/static', 
            static_folder='../frontend/dist/')


CORS(app)

#watt hours per pip
PIP_WH = 1
KWH_CONSUMPTION_PRICE = 0.13
KWH_GENERATION_PRICE = 0.52

@app.before_request
def _db_connect():
    pips_db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not pips_db.is_closed():
        pips_db.close()



class Pip(Model):
    created = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = pips_db


pips_db.create_tables([Pip])



@app.route("/")
def hello():
    return redirect("/static/index.html", code=302)

@app.route("/css/<path:path>")
def css(path):
    print("lalala")
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
            Pip.created.between(midnight, datetime.datetime.now())
        ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy":wh})


@app.route("/api/historical/last24")
def get_pips_last_24():
    now = datetime.datetime.now()

    day_ago = now - datetime.timedelta(days=1)

    pips_in_day = Pip.select().where(
            Pip.created.between(day_ago, datetime.datetime.now())
        ).count()

    wh = pips_in_day * PIP_WH

    return jsonify({"energy" :wh})

@app.route("/api/historical/hourly")
def get_pips_hourly():
    now = datetime.datetime.now()

    day_ago = now - datetime.timedelta(days=1)

    query = Pip.select(fn.COUNT(Pip.created).alias('count'), Pip.created).group_by(fn.date_trunc('hour', Pip.created))

    result = {}
    for pip in query:
        count = pip.count
        pip_hour = pip.created.replace(minute=0, second=0, microsecond=0)

        result[str(pip_hour)] = count * PIP_WH
    return jsonify(result)


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


        power = 1 / hours  #power in watts

        time_since_last_pip = (datetime.datetime.now() - recent.created).total_seconds()

        if time_since_last_pip > 60:
            power = 0

        result = {"power": power, "seconds_since_update" : time_since_last_pip}

        return jsonify(result)

    else:
        return jsonify({"error": "not enough pips registered"})




@app.route("/api/pip")
def pip():
    new_pip = Pip()
    new_pip.save()
    return jsonify({"success":"true"})   


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=80)








    