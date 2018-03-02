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

    cur_datetime = datetime.now()
    # Validate the user trying to change the db
    if(request.method == 'POST' and request.form['password'] == config.password):
        cur_hour = cur_datetime.hour
        cur_weekday = cur_datetime.date().weekday()
        auth = 'authenticated'
        # Validate that right now is a time when the db may be altered
        if(cur_hour == config.class_hour and cur_weekday in config.class_days):
            conn.execute("create table if not exists datetime (d1 text);")
            conn.execute("insert into datetime (d1) values (datetime('now', 'localtime'));")

    # Gather data from the database from today
    month_day_str = '%' + cur_datetime.date().strftime("%m-%d") + '%'
    result = conn.execute("select d1 from datetime where d1 like ?;", (month_day_str,))
    todays_data = result.cursor.fetchall()
    conn.close()

    # Create images for main page
    img1 = generate_elems_per_min_over_time_img(todays_data, cur_datetime, 60, 'static/', True)
    img2 = generate_elems_per_min_over_time_img(todays_data, cur_datetime, 15, 'static/', True)

    # Use unix timestamp to force browsers to make unique requests on images
    # this is kinda hacky
    unixtime = datetime.now().strftime('%s')
    content = {
        'auth': auth,
        'signals_count': len(todays_data),
        'img1': img1,
        'img2': img2,
        'time': unixtime
    }

    return render_template("counter.html", **content)

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
    conn.close()

    content = generate_alltime_stats(data)
    content.update(generate_date_stats(data, date))

    return render_template("stats.html", **content)

@app.route('/about')
def about():
    return redirect("https://github.com/irandms/signals_tracker")

@app.route('/gallery')
def gallery():
    content = dict()

    conn = eng.connect()
    query = conn.execute("select d1 from datetime")
    data = query.cursor.fetchall()
    conn.close()

    content['images'] = generate_images(data)

    return render_template("gallery.html", **content)

if __name__ == '__main__':
    app.run()
