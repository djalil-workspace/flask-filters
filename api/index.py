from flask import Flask, jsonify, request, redirect
from datetime import date, timedelta, datetime
from sqlite3 import connect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


def get_seq() -> int:
    with connect('db.sqlite3') as c:
        data = c.execute("SELECT seq FROM sqlite_sequence WHERE name='customers'").fetchall()

    return int(data[0][0]) + 1


@app.route('/')
def home():
    return redirect('/All')


@app.route('/post', methods=['POST', 'GET'])
def add_customer():
    try:
        user_id = get_seq()

        form_fullname  =  request.args.get('fullname')
        form_date      =  date.fromisoformat(request.args.get('date'))
        form_category  =  request.args.get('category')
        form_address   =  request.args.get('address')
        form_mobile    =  request.args.get('mobile')
        form_comment   =  request.args.get('comment')

        filter1 = form_date + timedelta(days=60) if form_category == '2-4 ay' else form_date + timedelta(days=180)
        filter2 = form_date + timedelta(days=120) if form_category == '2-4 ay' else form_date + timedelta(days=180)

        with connect('db.sqlite3') as c:
            c.execute(
                f"""INSERT INTO customers VALUES (
                    '{user_id}','{form_fullname}','{form_date}',
                    '{form_category}','{form_address}','{form_mobile}',
                    '{form_comment}','{filter1}','{filter2}'
                    )
                """
            )
    except Exception as e:
        return {'exception': e}

    return redirect('/All')


@app.route('/check/<string:fullname>')
def check(fullname):
    try:
        with connect('db.sqlite3') as c:
            user = c.execute(f'SELECT * FROM customers WHERE fullname="{fullname}"').fetchall()
            user = user[len(user)-1]
            
            user_id      =  get_seq()
            filter_date  =  user[2]
            category     =  user[3]
            address      =  user[4]
            mobile       =  user[5]
            comment      =  user[6]
            filter_1     =  user[7]
            filter_2     =  user[8]

            if category == '2-4 ay':
                if filter_1 == filter_2:
                    filter_1 = date.fromisoformat(filter_1) + timedelta(days=60)
                    filter_2 = date.fromisoformat(filter_2) + timedelta(days=120)
                else:
                    filter_1 = date.fromisoformat(filter_1) + timedelta(days=60)

            if category == '6 ay':
                filter_1 = date.fromisoformat(filter_1) + timedelta(days=180)
                filter_2 = date.fromisoformat(filter_2) + timedelta(days=180)

            c.execute(
                f'''
                    INSERT INTO customers VALUES (
                        {user_id}, "{fullname}", "{filter_date}",
                        "{category}", "{address}", "{mobile}",
                        "{comment}", "{filter_1}", "{filter_2}"
                    )
                '''
            )

            print(user)
            
            return {'error': None}
            
    except Exception as e:
        return {'exception': f"{e}"}


@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    result = []

    with connect('db.sqlite3') as c:
        all_users = c.execute('SELECT * FROM customers').fetchall()
        for user in all_users:
            if q.lower() in [str(i).lower() for i in user]:
                result.append(user)

    return jsonify(result)


@app.route("/<string:time>")
@cross_origin()
def api(time):
    if time == "All":
        with connect('db.sqlite3') as c:
            data = c.execute("SELECT * FROM customers").fetchall()      
    elif time == "Today":
        with connect('db.sqlite3') as c:
            today = datetime.now().date()
            data = c.execute("SELECT * FROM customers WHERE filter_1 = ? OR filter_2 = ?", (today, today)).fetchall()
    elif time == "Tomorrow":
        with connect('db.sqlite3') as c:
            tomorrow = datetime.now().date() + timedelta(days=1)
            data = c.execute("SELECT * FROM customers WHERE filter_1 = ? OR filter_2 = ?", (tomorrow, tomorrow)).fetchall()
    elif time == "Past":
        with connect('db.sqlite3') as c:
            past = datetime.now().date()
            data = c.execute("SELECT * FROM customers WHERE filter_1 < ? OR filter_2 < ?", (past, past)).fetchall()
    else:
        return redirect('/All')

    users = {user[1] for user in data}

    clean_data = []
    for user in users:
        clean_data.append(c.execute(f'SELECT * FROM customers WHERE fullname="{user}"').fetchall()[-1])

    api_data = [
        {
            'id'        :  user[0],
            'fullname'  :  user[1],
            'date'      :  user[2],
            'category'  :  user[3],
            'address'   :  user[4],
            'mobile'    :  user[5],
            'comment'   :  user[6],
            'filter1'   :  user[7],
            'filter2'   :  user[8],
        } for user in clean_data
    ]

    return jsonify(api_data)


@app.route('/delete/<string:fullname>')
def delete_user(fullname):
    try:
        with connect('db.sqlite3') as c:
            c.execute(f'DELETE FROM customers WHERE fullname="{fullname}"')

        return {'error': None}

    except Exception as e:
        return {'exception': str(e)}


@app.route('/list')
def user_list():
    with connect('db.sqlite3') as c:
        users = c.execute('SELECT * FROM customers').fetchall()

        return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
