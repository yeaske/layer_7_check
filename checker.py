import os
import gc

from flask import Flask, request, render_template, jsonify
import MySQLdb

app = Flask(__name__)
app.config.from_pyfile('app.cfg')


def checkDb(dbx):
    """Check DB."""
    db_connect = None
    try:
        db_connect = MySQLdb.connect(host=dbx['HOST'], port=dbx['PORT'],
                                     user=dbx['USER'], passwd=dbx['PASS'],
                                     db=dbx['DB'])
        cursor = db_connect.cursor()
        cursor.execute("show databases")
        data = cursor.fetchall()
#         print data
        if data is None:
            db_connect.close()
            return dbx['HOST'], 'FAILURE'
        else:
            db_connect.close()
            return dbx['HOST'], 'OK'
    except Exception, e:
        print e
        return dbx['HOST'], 'EXCEPTION'


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = ''
    if request.method == "GET":
        try:
            databases = app.config['DB_BIND']
            state_list = []
            count = 0
            for database in databases:
                name, status = checkDb(database)
                db_state = {}
                db_state['name'] = name
                db_state['status'] = status
                state_list.insert(count, db_state)
                count = count + 1
            if not errors:
                return render_template("status.html", data=state_list)
        except Exception, e:
            return render_template("fallback.html", None)
            print e


@app.route('/dbcheck/db/<dbname>')
def check_db(dbname):
    lst = [
        {'dbname': dbname, 'values': {'a': 66, 'b': 222}},
        {'dbname': dbname, 'values': {'a': 33, 'b': 111}},
        ]
    return jsonify(result=lst)

if __name__ == '__main__':
        app.run(
            host="0.0.0.0",
            port=int("8003")
            )
