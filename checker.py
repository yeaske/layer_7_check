import os

from flask import Flask, request, render_template, jsonify
from flaskext.mysql import MySQL

# Create a flask app object using a unique name. In this case we are
# using the name of the current file
app = Flask(__name__)

# Generate a secret random key for the session
app.secret_key = os.urandom(24)


def checkDb(xyz):
    """Check DB."""
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'sthom02'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'kmart1234'
    app.config['MYSQL_DATABASE_DB'] = 'go_service_layer'
    app.config['MYSQL_DATABASE_HOST'] = 'gomcdn301p.dev.ch3.s.com'
    mysql.init_app(app)
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from assoc_details limit 1")
    data = cursor.fetchall()
    if data is None:
        print 111
#         return "fail"
    else:
        print 222
        print data
        print 222
#         return "success"
    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = ''
    if request.method == "GET":
        # dbname = request.form['name'].strip()
        name = "Test"
        status = "Active"
        b = checkDb("xxx")
        print b
        if not errors:
            data = {'name': name,
                    'status': status
                    }
            return render_template("status.html", data=data)


@app.route('/check/db/<dbname>')
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
