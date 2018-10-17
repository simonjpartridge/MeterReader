from peewee import *
from flask import Flask, jsonify, request, send_from_directory

from flask_cors import CORS


import datetime

pips_db = SqliteDatabase('pips.db')
app = Flask(__name__, static_url_path='/static', 
            static_folder='../frontend/dist/')


CORS(app)

#watt hours per pip
PIP_WH = 1


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
    return app.send_static_file('../frontend/dist/index.html')

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



@app.route("/api/get_all_pips")
def get_all_pips():
    all_pips = {}
    for pip in Pip.select():
        all_pips[pip.id] = pip.created

    return jsonify(all_pips)


@app.route("/api/instantaneous")
def get_instantaneous():
    most_recent_2 = Pip.select().order_by(Pip.created.desc()).limit(2)


    print(most_recent_2)

    # most_recent_2 = Pip.select()

    if len(most_recent_2) > 1:
        recent = most_recent_2[0]
        prev = most_recent_2[1]

        delta = recent.created - prev.created
        hours = delta.total_seconds() / (60 * 60)


        power = 1 / hours  #power in watts


        result = {"power": power, "last_update" : recent.created}

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
    app.run(host = '0.0.0.0',port=5005)








    