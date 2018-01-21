from flask import Flask, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

from datetime import datetime
from datetime import date

eng = create_engine('sqlite:///signals.db')
app = Flask(__name__)
api = Api(app)

@app.route('/signals/counter', methods=['GET', 'POST'])
def signals_counter():
    conn = eng.connect()
    if(request.method == 'POST'):
        class_days = [0, 2, 4]
        if(datetime.now().hour == 15 and date.today().weekday() in class_days):
            conn.execute("create table if not exists datetime (d1 text);")
            conn.execute("insert into datetime (d1) values (datetime('now', 'localtime'));")

    month_day_str = date.today().strftime("%m-%d")
    query = conn.execute("select d1 from datetime where d1 like '%{}%'".format(month_day_str))
    todays_data = query.cursor.fetchall()

    conn.close()
    return render_template("signals_counter.html", signals_count=len(todays_data))

if __name__ == '__main__':
    app.run()
