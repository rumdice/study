# -*- coding: utf-8 -*-
import ast
import csv
import os
import random
import time
from datetime import datetime, timedelta

from dateutil import parser

#region CSV 테이블 파싱
path = os.path.dirname(os.path.abspath(__file__)) + "/../../gamedata/"
def load_csvfile(self, filename):
    table = []
    with open(path + filename + ".csv", encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table.append(row)

    return table
#endregion


#region 랜덤
# 하루가 지나면 새로운 렌덤 시드 발급
random_time = datetime.now()
shop_random = random.Random()
shop_random_seed = random.randint(1, 100000000)
shop_random.seed(shop_random_seed)
def util_shop_rand(min, max):
    if random_time.day != datetime.now().day:
        shop_random_seed = random.randint(1, 100000000)
        shop_random.seed(shop_random_seed)

    return shop_random.randint(min, max)

data_random = random.Random()
data_random_seed = random.randint(1, 100000000)
data_random.seed(data_random_seed)
def util_get_rand_range(min, max):
    if random_time.day != datetime.now().day:
        seed = random.randint(1, 100000000)
        data_random.seed(seed)

    return data_random.randint(min, max)
#endregion


#region JSON 필터 클래스
class StringFilter(object):
    def __init__(self, stream):
        self.stream = stream
    def __getattr__(self, attr_name):
        return getattr(self.stream, attr_name)
    def write(self, data):
        self.stream.flush()
    def flush(self):
        self.stream.flush()

class JsonFilter(object):
    def __init__(self, stream):
        self.stream = stream
    def __getattr__(self, attr_name):
        return getattr(self.stream, attr_name)
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def flush(self):
        self.stream.flush()
#endregion


#region 시간
def day_diff(dt):
    if not dt:
        return 0
    if not isinstance(dt, datetime):
        dt = parser.parse(dt)
    today_date_only = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    datetime_date_only = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (datetime_date_only - today_date_only)
    return delta.days

def time_diff_in_seconds(time):
    if not time:
        return 0
    if not isinstance(time, datetime):
        time = parser.parse(time)

    now = datetime.now()
    delta = time - now if time >= now else now - time
    return delta.days * 86400 + delta.seconds

def calc_time_to_seconds(start_time, end_time):
    if not isinstance(start_time, datetime):
        start_time = parser.parse(start_time)

    if not isinstance(end_time, datetime):
        end_time = parser.parse(end_time)

    delta = end_time - start_time
    return delta.days * 86400 + delta.seconds

def get_pass_time(day, hour, second):
    return datetime.now() + timedelta(days=day, seconds=second, hours=hour)

def time_diff_in_day(time):
    if not time:
        return 0
    if not isinstance(time, datetime):
        time = parser.parse(time)

    now = datetime.now()
    delta = time - now
    return int(delta.days)

def convert_date_to_utc(date):
    return time.mktime(date.timetuple())

def convert_utc_to_date(time):
    return datetime.fromtimestamp(float(time))

#endregion


#region 문자열
def convert_string_to_array(str):
    try:
        if isinstance(str, bytes):
            encode_str = str.decode('utf-8')
            return ast.literal_eval(encode_str)

        return ast.literal_eval(str)
    except:
        return []

def convert_string_to_dict(str):
    try:
        if isinstance(str, bytes):
            encode_str = str.decode('utf-8')
            return ast.literal_eval(encode_str)
        return ast.literal_eval(str)
    except:
        return {}

def convert_string_to_set(str):
    if isinstance(str, bytes):
        encode_str = str.decode('utf-8')
        return set(ast.literal_eval(encode_str))
    return set(ast.literal_eval(str))

def convert_set_to_string(set):
    return str(set) if set else '{}'

#endregion


#region PrintBar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
#endregion