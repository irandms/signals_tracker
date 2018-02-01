from flask import Flask, request, render_template, redirect
from sqlalchemy import create_engine
from datetime import datetime, date

from stats_generator import *
import config

eng = create_engine('sqlite:///signals.db')
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    conn = eng.connect()
    auth = ''
    if(request.method == 'POST' and request.form['password'] == config.password):
        cur_hour = datetime.now().hour
        cur_weekday = date.today().weekday()
        auth = 'authenticated'
        if(cur_hour == config.class_hour and cur_weekday in config.class_days):
            conn.execute("create table if not exists datetime (d1 text);")
            conn.execute("insert into datetime (d1) values (datetime('now', 'localtime'));")

    month_day_str = '%' + date.today().strftime("%m-%d") + '%'
    result = conn.execute("select d1 from datetime where d1 like ?;", (month_day_str,))
    todays_data = result.cursor.fetchall()
    generate_elems_per_min_over_time_image(todays_data)

    unixtime = datetime.now().strftime('%s')

    conn.close()
    return render_template("counter.html", signals_count=len(todays_data), auth=auth, time=unixtime)

@app.route('/stats')
def stats():
    conn = eng.connect()
    query = conn.execute("select d1 from datetime;")
    data = query.cursor.fetchall()

    content = generate_alltime_stats(data)

    conn.close()

    return render_template("stats.html", **content)

@app.route('/stats/<int:month>/<int:day>')
def stats_upto_date(month, day):
    conn = eng.connect()
    date = '2018-{}-{}'.format(str(month).zfill(2), str(day).zfill(2))
    datetime = date + ' 23:59:59'
    query = conn.execute("select d1 from datetime where d1 < ?", (datetime,))
    data = query.cursor.fetchall()

    content = generate_alltime_stats(data)
    content.update(generate_date_stats(data, date))

    conn.close()

    return render_template("stats.html", **content)

@app.route('/about')
def about():
    return redirect("https://github.com/irandms/signals_tracker")

if __name__ == '__main__':
    app.run()
