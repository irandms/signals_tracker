from flask import Flask, request, render_template
from sqlalchemy import create_engine
from json import dumps

from datetime import datetime
from datetime import date

from stats_generator import generate_alltime_stats

eng = create_engine('sqlite:///signals.db')
app = Flask(__name__)

@app.route('/signals/counter', methods=['GET', 'POST'])
def signals_counter():
    conn = eng.connect()
    if(request.method == 'POST'):
        class_days = [0, 2, 4]
        if(datetime.now().hour == 15 and date.today().weekday() in class_days):
            conn.execute("create table if not exists datetime (d1 text);")
            conn.execute("insert into datetime (d1) values (datetime('now', 'localtime'));")

    month_day_str = "'%" + date.today().strftime("%m-%d") + "%'"
    query = conn.execute("select d1 from datetime where d1 like ?", (month_day_str,))
    todays_data = query.cursor.fetchall()

    conn.close()
    return render_template("signals_counter.html", signals_count=len(todays_data))

@app.route('/signals/stats')
def signals_stats():
    conn = eng.connect()
    query = conn.execute("select d1 from datetime;")
    data = query.cursor.fetchall()

    content = generate_alltime_stats(data)

    conn.close()

    return render_template("signals_stats.html", **content)

@app.route('/signals/stats/<int:month>/<int:day>')
def signals_stats_m_d(month, day):
    conn = eng.connect()
    datetime = '2018-{}-{} 23:59:59'.format(str(month).zfill(2), str(day).zfill(2))
    query = conn.execute("select d1 from datetime where d1 < ?", (datetime,))
    data = query.cursor.fetchall()

    content = generate_alltime_stats(data)

    conn.close()

    return render_template("signals_stats.html", **content)

if __name__ == '__main__':
    app.run()
