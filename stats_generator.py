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
    results['top_day'] = top_day
    results['projected_signals'] = len(data) + days_remaining * avg_per_day

    return results

def generate_date_stats(data, date):
    data_on_date = [x for x in data if tuple(x[0].split())[0] == date]

    results = { 'signals_on_date' : len(data_on_date) }
    results['date'] = date
    results['signals_per_min_on_date'] = len(data_on_date) / 50.0

    return results
