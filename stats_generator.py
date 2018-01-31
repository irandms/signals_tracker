import matplotlib.pyplot as plt
from datetime import datetime
from sets import Set

def generate_alltime_stats(data):
    top_day_val = -1;
    days = Set()
    cur_val = 0;
    cur_day = u''
    for datetime in data:
        timestamp = datetime[0]
        pieces = tuple(timestamp.split())

        if(pieces[0] != cur_day):
            if(cur_val > top_day_val):
                top_day_val = cur_val
                top_day_avg = top_day_val / 50.0
                top_day = cur_day
            cur_val = 0

        cur_day = pieces[0]
        cur_time = pieces[1]

        year, month, day = cur_day.split('-')
        hour, minute, second = cur_time.split(':')

        days.add(day)
        cur_val += 1

    days_remaining = 29 - len(days)
    total_signals = len(data)
    avg_per_day = len(data) / float(len(days))

    results = { 'total_signals' : total_signals }
    results['avg_per_day'] = avg_per_day
    results['avg_per_min'] = len(data) / float(len(days)) / 50.0
    results['top_day_val'] = top_day_val
    results['top_day_avg'] = top_day_avg
    results['top_day'] = top_day
    results['projected_signals'] = len(data) + days_remaining * avg_per_day

    return results

def generate_date_stats(data, date):
    data_on_date = [x for x in data if tuple(x[0].split())[0] == date]

    results = { 'signals_on_date' : len(data_on_date) }
    results['date'] = date
    results['signals_per_min_on_date'] = len(data_on_date) / 50.0

    return results

def generate_elems_per_min_over_time_image(data):
    right_now = datetime.now()
    datetimes = [ datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S') for x in data ]

    todays_data = list(filter(lambda x: x.day == right_now.day, data))

    if right_now.minute < 50:
        upper_limit = right_now.minute
    else:
        upper_limit = 50

    signals_per_min = []
    for minute in range(1, upper_limit):
        signals_this_far = list(filter(lambda x: x.minute <= minute, todays_data))
        signals_per_min.append(len(signals_this_far) / float(minute))

    plt.scatter(range(1, upper_limit), signals_per_min)
    plt.title('Signals Per Minute Over Time')
    plt.ylabel('Signals Per Minute')
    plt.xlabel('Minutes Into Class')
    plt.savefig('static/spm_over_time.png')
