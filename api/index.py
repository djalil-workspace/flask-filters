from flask import Flask, jsonify, request, render_template
from sqlite3 import connect
from datetime import date, timedelta, datetime


app = Flask(__name__)


def get_seq() -> int:
    with connect('db.sqlite3') as c:
        data = c.execute("SELECT seq FROM sqlite_sequence WHERE name='customers'").fetchall()

    return int(data[0][0]) + 1


@app.route('/', methods=['POST', 'GET'])
def AddCustomer():
    try:
        user_id = get_seq()

        form_fullname = request.form['fullname']
        form_date = date.fromisoformat(request.form['date'])  # Convert string to date object
        form_category = request.form['category']
        form_address = request.form['address']
        form_mobile = request.form['mobile']
        form_comment = request.form['comment']

        filter1 = form_date + timedelta(days=60) if form_category == '2-4 ay' else form_date + timedelta(days=180)
        filter2 = form_date + timedelta(days=120) if form_category == '2-4 ay' else form_date + timedelta(days=180)

        with connect('db.sqlite3') as c:
            c.execute(
                f"INSERT INTO customers VALUES ({user_id}, '{form_fullname}', '{form_date}', '{form_category}', '{form_address}', '{form_mobile}', '{form_comment}', '{filter1}', '{filter2}')"
            )
    except Exception as e:
        print(e)

    return render_template('add_customer.html')


@app.route('/All')
def All():
    with connect('db.sqlite3') as c:
        data = c.execute("SELECT * FROM customers").fetchall()
        json = []

        for user in data:
            json.append(
                {
                    'id': user[0],
                    'fullname': user[1],
                    'date': user[2],
                    'category': user[3],
                    'address': user[4],
                    'mobile': user[5],
                    'comment': user[6],
                    'filter1': user[7],
                    'filter2': user[8],
                }
            )

    return jsonify(json)


@app.route('/Today')
def Today():
    today = datetime.now().date()

    with connect('db.sqlite3') as c:
        data = c.execute("SELECT * FROM customers WHERE filter_1 = ? OR filter_2 = ?", (today, today)).fetchall()
        json = []

        for user in data:
            json.append(
                {
                    'id': user[0],
                    'fullname': user[1],
                    'date': user[2],
                    'category': user[3],
                    'address': user[4],
                    'mobile': user[5],
                    'comment': user[6],
                    'filter1': user[7],
                    'filter2': user[8],
                }
            )

    return jsonify(json)


@app.route('/Tomorrow')
def Tomorrow():
    today = datetime.now().date() + timedelta(days=1)

    with connect('db.sqlite3') as c:
        data = c.execute("SELECT * FROM customers WHERE filter_1 = ? OR filter_2 = ?", (today, today)).fetchall()
        json = []

        for user in data:
            json.append(
                {
                    'id': user[0],
                    'fullname': user[1],
                    'date': user[2],
                    'category': user[3],
                    'address': user[4],
                    'mobile': user[5],
                    'comment': user[6],
                    'filter1': user[7],
                    'filter2': user[8],
                }
            )

    return jsonify(json)


@app.route('/Past')
def Past():
    today = datetime.now().date()

    with connect('db.sqlite3') as c:
        data = c.execute("SELECT * FROM customers WHERE filter_1 < ? OR filter_2 < ?", (today, today)).fetchall()
        json = []

        for user in data:
            json.append(
                {
                    'id': user[0],
                    'fullname': user[1],
                    'date': user[2],
                    'category': user[3],
                    'address': user[4],
                    'mobile': user[5],
                    'comment': user[6],
                    'filter1': user[7],
                    'filter2': user[8],
                }
            )

    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True)
