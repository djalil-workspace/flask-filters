from flask import Flask, jsonify, request, render_template
from sqlite3 import connect
from datetime import date, timedelta

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


if __name__ == '__main__':
    app.run(debug=True)
