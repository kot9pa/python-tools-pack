import argparse
from collections import namedtuple
from datetime import datetime
from statistics import mean, median
from itertools import groupby


''' 
Script for parsing text log files in format: 
start_time | end_time | req_path | resp_code | resp_body

usage: 1_logfiles_parser.py [-h] file [file ...]

positional arguments:
  file        path to logfile(s), e.g. '1_logfile1.log'

options:
  -h, --help  show this help message and exit
'''

Log = namedtuple('Log', ['start_time','end_time','req_path','resp_code','resp_body'])
logs = []
datetime_format = '%d.%m.%Y %H:%M:%S'

def main():
    ap = argparse.ArgumentParser(add_help="Logfile parser")
    ap.add_argument("file",  
                    nargs='+', 
                    type=argparse.FileType('r', encoding='utf-8'), 
                    help="path to logfile(s), e.g. '1_logfile1.log'")
    args = vars(ap.parse_args())

    for file in args['file']:
        with file as f:
            for line in f:
                logs.append(Log(*line.split("|")))

    '''
    Статистические характеристики времени обработки сервером всех запросов 
    (минимум, максимум, среднее арфиметическое, медиана)
    '''
    response_time_seconds = list(map(lambda log: (datetime.strptime(log.end_time.strip(), datetime_format) -
                        datetime.strptime(log.start_time.strip(), datetime_format)).seconds, logs))
    response_time_min = min(response_time_seconds)
    response_time_max = max(response_time_seconds)
    response_time_mean = mean(response_time_seconds)
    response_time_median = median(response_time_seconds)
    print(f"{response_time_min=!s}\n{response_time_max=!s}")
    print(f"{response_time_mean=:2f}\n{response_time_median=:2f}")

    '''
    Процент ошибочных запросов 
    (ошибочные – если код вышее 400 или в теле присутствует подстрока “error”)
    '''
    response_failed = filter(lambda log: int(log.resp_code) > 400 or 
                             "error" in log.resp_body, logs)
    response_failed_procent = 100*len(list(response_failed)) / len(logs)
    print(f"{response_failed_procent=:.2f}\n")

    '''
    Распределение числа вызовов по страницам 
    (т.е. какую страницу сколько раз вызывали)
    '''
    for page, groups in groupby(sorted(map(lambda log: log.req_path.strip(), logs))):
        print(f"Page {page} was called {len(list(groups))} times")

if __name__ == '__main__':
    main()