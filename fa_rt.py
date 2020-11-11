import os
import datetime
import tushare as ts
import pandas as pd
from numpy import *
import time
import numpy as np

path_root = 'H:/'
st_code_str = 'sh000827'
period = 'M'
base_delta_value = 313.4953
file_path = path_root + st_code_str + "_" + period + ".xlsx"

dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')


def get_ta_real_data(st_code_str, df, base_delta_value):
    global dt_now_str
    # df_real = ts.get_realtime_quotes(st_code_str[:-3])
    # price_now = df_real.loc[0, 'price']
    # time_now = df_real.loc[0, 'time']
    price_now = 1712
    time_now = dt_now_str
    print(time_now)
    print(price_now)

    # print(type(df_real.loc[0, 'price']))
    ma3 = float(price_now)
    i = 0
    while i < 2:
        ma3 += df.loc[i, 'close']
        i += 1
    ma3 /= 3

    ma5 = float(price_now)
    i = 0
    while i < 4:
        ma5 += df.loc[i, 'close']
        i += 1
    ma5 /= 5

    delta_real = float(ma3 - ma5)
    print(str(delta_real) + " <---> " + str(base_delta_value))
    if delta_real >= base_delta_value:
        print(time_now + ' delta is ' + str(delta_real) + " bigger than " + str(round((delta_real - base_delta_value) * 100 / base_delta_value, 3)) + "%")
        if delta_real < df.loc[0, 'delta']:
            print(dt_now_str + ' is hot: ' + str(delta_real) + ' and beichi')



if __name__ == '__main__':

    # sheet_name='Sheet1'
    df_data = pd.read_excel(file_path, converters={'trade_date': str})
    # print(datetime.datetime.now().hour)
    # print(datetime.datetime.now().minute)
    # real ta
    if (datetime.datetime.now().hour <= 16) and (datetime.datetime.now().hour >= 9):
        count = 0
        while count < 2:
            get_ta_real_data(st_code_str, df_data, base_delta_value)
            time.sleep(2)
            count += 1