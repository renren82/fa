import os
import datetime
import tushare as ts
import pandas as pd
from numpy import *
import numpy as np

ts_code_str = '000559.SZ'
st_code_str = '000559'

dt_start = datetime.datetime.strptime('20181009', '%Y%m%d').date()
dt_start_str = dt_start.strftime('%Y%m%d')
dt_end = datetime.datetime.strptime('20190131', '%Y%m%d').date()
dt_end_str = dt_end.strftime('%Y%m%d')

path_root = 'H:/'
path_data = path_root + ts_code_str + '.xlsx'
path_result = path_root + ts_code_str + '_result.xlsx'

dt_now = datetime.datetime.now().date()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d')


def file_exist(path):
    if os.path.exists(path):
        return 1
    else:
        return 0


def get_ta_data(path_data):
    """
    get base delta value for ma3-ma5
    """
    if file_exist(path_data) == 0:
        df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_start_str,
                        end_date=dt_now_str, ma=[3, 5, 8, 13, 21, 34, 55, 89, 144, 233])
        # print(df.head())
        writer = pd.ExcelWriter(path_data)
        # print(type(df).__name__)
        if type(df).__name__ == 'DataFrame':
            df.to_excel(writer, sheet_name='history', index=False)
            writer.save()


def v_ta(file_path):
    df_data = pd.read_excel(file_path, sheet_name='history', converters={'trade_date': str})

    if 'ma3' not in list(df_data):
        return 0

    # find sector high and low
    flag_find = 0
    high_price_list = []
    low_price_list = []
    price_date_list = []
    for k in df_data.index.values:
        # print(type(df_data.loc[k, 'trade_date']))
        if df_data.loc[k, 'trade_date'] == dt_end_str:
            flag_find = 1
        if flag_find == 1:
            high_price_list.append(df_data.loc[k, 'high'])
            low_price_list.append(df_data.loc[k, 'low'])
            price_date_list.append(df_data.loc[k, 'trade_date'])

    low_price = float(min(low_price_list))
    high_price = float(max(high_price_list))
    high_price_date_str = price_date_list[high_price_list.index(high_price)]

    if (high_price - low_price)*100/low_price < 25:
        return 0

    # bigger 25% is v
    vol_up = 0
    vol_down = 0
    v_low_price_list = []
    for k in df_data.index.values:
        # print(type(df_data.loc[k, 'trade_date']))
        if df_data.loc[k, 'trade_date'] == high_price_date_str:
            for i in range(0, k):
                vol_up += df_data.loc[k, 'vol']
            while 1:
                if df_data.loc[k, 'trade_date'] == dt_end_str:
                    break
                k -= 1
                v_low_price = float(df_data.loc[k, 'low'])
                v_close_price = float(df_data.loc[k, 'close'])
                vol_down += df_data.loc[k, 'vol']

                # price is lower
                if (high_price - v_low_price)*100/v_low_price > 15:
                    # is lower vol
                    if vol_up/vol_down > 1.0:
                        flag_lower = 0
                        for j in range(1, 800):
                            ma_str = 'ma' + str(j)
                            if ma_str not in list(df_data):
                                continue
                            if v_close_price > df_data.loc[k, ma_str]:
                                flag_lower = 1
                        if flag_lower == 0:
                            print(df_data.loc[k, 'trade_date'])





"""
main start
"""
# ts.set_token('2e2ec7b610512cc2704e3aa692711794ad9cacf7a2cae31ee0a769bf')

get_ta_data(path_data)

v_ta(path_data)




