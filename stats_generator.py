import matplotlib as mpl
mpl.use('Agg')
# There is no X server in production, so this allows us to use Matplotlib
import matplotlib.pyplot as plt
import os.path
from datetime import datetime, timedelta
from collections import defaultdict

def generate_alltime_stats(data):
    days = defaultdict(int)

    # Defaults - data[0][0].split()[0] is an ugly hardcoded way
    # to get the date of the very first datapoint in data
    top_day_count = -1;
    cur_day = data[0][0].split()[0]

    for datetime in data:
        # Example datetime: (u'2018-02-28 15:14:23',)
        # Here we take the first member of this 1-tuple, then split
        # by whitespace. Finally, take the 1st member of that, the date
        date = datetime[0].split()[0]
        days[date] += 1

    for day, count in days.iteritems():
        if(count > top_day_count):
            top_day_count = count
            top_day_avg = top_day_count / 50.0
            top_day = day

    # Hardcoded at the time of writing - there are 30 days of lecture
    days_remaining = 30 - len(days)
    total_signals = len(data)
    avg_per_day = total_signals / float(len(days))

    # Results dictionary, for the jinja2 template
    results = {
        'total_signals' : total_signals,
        'avg_per_day' : avg_per_day,
        'avg_per_min' : avg_per_day / 50.0,
        'top_day_count' : top_day_count,
        'top_day_avg' : top_day_avg,
        'top_day' : top_day,
        'projected_signals' : len(data) + days_remaining * avg_per_day
    }

    return results

def generate_date_stats(data, date):
    data_on_date = [x for x in data if tuple(x[0].split())[0] == date]

    results = { 'signals_on_date' : len(data_on_date) }
    results['date'] = date
    results['signals_per_min_on_date'] = len(data_on_date) / 50.0

    return results

def generate_elems_per_min_over_time_img(data, right_now, resolution, path, recreate):
    month_day = right_now.date().strftime("%m-%d")
    filename = '{}spm_over_time_{}_reso{}.png'.format(path, month_day, resolution)

    if os.path.isfile(filename) and not recreate:
        return filename

    datetimes = [ datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S') for x in data ]

    todays_data = list(filter(lambda x: x.day == right_now.day and x.month == right_now.month, datetimes))

    if right_now.hour == 15 and right_now.minute <= 50:
        upper_limit = right_now.minute * 60 + right_now.second
    else:
        upper_limit = 3000

    seconds_to_check = range(resolution, upper_limit+1, resolution);

    signals_per_min = []
    for seconds in seconds_to_check:
        signals_this_far = list(filter(lambda x: (x.minute * 60 + x.second) <= seconds, todays_data))
        signals_per_min.append(len(signals_this_far) / float(seconds/60.0))

    plt.scatter(map(lambda x: x/60.0, seconds_to_check), signals_per_min)
    plt.title('Signals Per Minute Over Time ({} second resolution)'.format(resolution))
    plt.ylabel('Signals Per Minute')
    plt.xlabel('Minutes Into Class')
    plt.savefig(filename)
    plt.clf()

    return filename

def generate_images(data):
    class_days = []

    cur_day = datetime.today()
    year = cur_day.year

    i = 0
    while year == cur_day.year:
        if cur_day.date().weekday() in [0, 2, 4]:
            class_days.append(cur_day)
        cur_day = datetime.today() - timedelta(i)
        i += 1

    filenames = []
    # Create images for main page
    for day in class_days:
        filenames.append(generate_elems_per_min_over_time_img(data, day, 60, 'static/gallery/', False))

    return filenames
