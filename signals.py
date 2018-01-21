from flask import Flask, request, render_template
from sqlalchemy import create_engine

from datetime import datetime, date

from stats_generator import generate_alltime_stats

eng = create_engine('sqlite:///signals.db')
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    conn = eng.connect()
    auth=''
    if(request.method == 'POST' and request.form['password'] == 'big beefy taco with long don sauce'):
	class_days = [0, 2, 4]
        auth="ya"
	if(datetime.now().hour == 15 and date.today().weekday() in class_days):
	    conn.execute("create table if not exists datetime (d1 text);")
	    conn.execute("insert into datetime (d1) values (datetime('now', 'localtime'));")

    month_day_str = "'%" + date.today().strftime("%m-%d") + "%'"
    query = conn.execute("select d1 from datetime where d1 like ?", (month_day_str,))
    todays_data = query.cursor.fetchall()

    conn.close()
    return render_template("counter.html", signals_count=len(todays_data))

@app.route('/increment', methods=['GET', 'POST'])
def increment():
    password = request.form['password']
    if password == "test":
        return redirect(url_for('index'))
    else:
        return redirect("https://google.com")

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
    datetime = '2018-{}-{} 23:59:59'.format(str(month).zfill(2), str(day).zfill(2))
    query = conn.execute("select d1 from datetime where d1 < ?", (datetime,))
    data = query.cursor.fetchall()

    content = generate_alltime_stats(data)

    conn.close()

    return render_template("stats.html", **content)

if __name__ == '__main__':
    app.run()
