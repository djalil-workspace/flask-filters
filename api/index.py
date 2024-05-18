from flask import Flask, jsonify
from sqlite3 import connect

app = Flask(__name__)


@app.route('/')
def index():
    return '<a href="/api" style="font-size: 35px;">API</a>'


@app.route('/api')
def api():
    with connect('db.sqlite3') as c:
        json = []
        data = c.execute('SELECT * FROM users').fetchall()

        for user in data:
            json.append({'fullname': user[0], 'age': user[1]})

    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True)
