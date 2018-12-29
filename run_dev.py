from server import app
import os
import argparse

parser = argparse.ArgumentParser(description='Dev Settings')
parser.add_argument('--reset', dest='reset', action='store_true', default=False)
args = parser.parse_args()

# del os.environ["METER_DATABASE_PATH"]

if args.reset:
    print("Resetting DB")
    db_file = "server/pips.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Removed database file")
else:
    app.debug = True
    app.run(host = '0.0.0.0',port=80)
