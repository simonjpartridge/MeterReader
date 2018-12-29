import os
from flask import Flask
from flask_cors import CORS 
from peewee import SqliteDatabase

app = Flask(__name__, static_url_path='/static',
            static_folder='../frontend/dist/')

CORS(app)

production_db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'pips.db')
db_path = os.getenv('METER_DATABASE_PATH', production_db_path)

print("Database at " + db_path)
db = SqliteDatabase(db_path)


from server import views