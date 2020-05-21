import random
import datetime
import collections

import variables
# log.configure_logging(variables.VOLUME_GENERATOR_LOGFILE)
from common.mongo import db, server

today_volume_coll = db.get_collection(variables.MONGO_TODAY_VOLUME_COLL)
hist_volume_coll = db.get_collection(variables.MONGO_HISTORY_VOLUME_COLL)

RANDOM_MINUTE_RANGE=720
mixers = [2.5, 3, 3, 3, 3, 3, 5, 5, 5, 5, 7]
low_volume = 180
max_volume = 280
start_hour_ = 8
TIMEZONE = 7

start_hour = start_hour_ - TIMEZONE


def _volume_generate(today_date):
    random_total_volume = random.uniform(low_volume, max_volume)

    data = {}
    mixer_cnt = 0
    total_volume = 0

    def random_date(start):
        return start + datetime.timedelta(minutes=random.randrange(RANDOM_MINUTE_RANGE))

    today = datetime.date.today()
    startDate = datetime.datetime(today.year, today.month, today.day, start_hour, 0, 0)

    while random_total_volume/2.5 > 1:
        mixer_vol = random.choice(mixers)
        random_total_volume -= mixer_vol

        date = random_date(startDate)
        date = datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
        if data.get(date) is None:
            data[date] = {
                'volume':0,
                'mixer_cnt':0
            }

        data[date]['volume'] += mixer_vol
        data[date]['mixer_cnt'] += 1
        total_volume += mixer_vol
        mixer_cnt += 1

    if random_total_volume != 0:
        mixer_vol = round(random_total_volume, 1)
        if mixer_vol >= 0.9:
            if data.get(date) is None:
                data[date] = {
                    'volume':0,
                    'mixer_cnt':0
                }
            data[date]['volume'] += mixer_vol
            data[date]['mixer_cnt'] += 1
            total_volume += mixer_vol
            mixer_cnt += 1

    od = collections.OrderedDict(sorted(data.items()))

    result = {}
    prev_key = list(od.keys())[0]
    result[str(prev_key.time())] = {
                    'volume':0,
                    'mixer_cnt':0
                }

    for (key, item) in od.items():
        result[str(key.time())] = {
            'volume': result[str(prev_key.time())]['volume'] + item['volume'],
            'mixer_cnt': result[str(prev_key.time())]['mixer_cnt'] + item['mixer_cnt']
        }
        result[str(key.time())]['mean'] = result[str(key.time())]['volume']/result[str(key.time())]['mixer_cnt']
        prev_key = key

    first_time = 0
    str_last_time = ''
    last_time = 0

    for i in range(start_hour, 24):
        tmp_time = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        str_time = str(tmp_time.time())
        if result.get(str_time) is not None:
            first_time = i
            break

    for i in range(23, start_hour, -1):
        tmp_time = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        str_time = str(tmp_time.time())
        if result.get(str_time) is not None:
            str_last_time = str_time
            last_time = i
            break

    for i in range(0, 24):
        tmp_time = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        str_time = str(tmp_time.time())
        if i < first_time or i > 23 - abs(8 - TIMEZONE-start_hour_) :
            result[str_time] = {
                'volume': 0,
                'mixer_cnt': 0,
                'mean': 0
            }
        if last_time < i <= 23 - abs(8 - TIMEZONE - start_hour_):
            result[str_time] = result[str_last_time]

    tmp_time = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
    prev_time = str(tmp_time.time())

    for i in range(1, 24):
        tmp_time = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        cur_time = str(tmp_time.time())
        if result.get(cur_time) is None:
            result[cur_time] = result[prev_time]
        prev_time = cur_time

    result['day_total'] = {
        'date': today_date.strftime(variables.DATE_FORMAT),
        'total_volume': total_volume,
        'total_mixers': mixer_cnt,
        'total_mean': total_volume/mixer_cnt
    }

    return result


def volume_generate(today):
    if today_volume_coll.find_one() is not None:
        record = today_volume_coll.find_one()
        hist_volume_coll.insert(record['day_total'])
        today_volume_coll.drop()

    volume_today = _volume_generate(today)
    today_volume_coll.insert(volume_today)
    if variables.LOCAL:
        server.close()
    return volume_today


if __name__ == '__main__':
    hist_volume_coll.drop()
    for i in range(15, 0, -1):
        today_date = datetime.date.today() - datetime.timedelta(days=i)
        if today_volume_coll.find_one() is not None:
            record = today_volume_coll.find_one()
            hist_volume_coll.insert(record['day_total'])
            today_volume_coll.drop()

    # today_date = str(datetime.date.today().strftime("%d.%m.%y"))
        today_volume_coll.insert(_volume_generate(today_date))
    if variables.LOCAL:
        server.close()

