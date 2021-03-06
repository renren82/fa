import os
import datetime
import tushare as ts
import pandas as pd
from numpy import *
import time
import numpy as np

code_name = 'cyb'
period_type = 'D'

#  002714.SZ
ts_code_str = '300059.SZ'
st_code_str = ts_code_str[:-2]


path_root = 'H:/'
path_data = path_root + ts_code_str + '.xlsx'
path_result = path_root + ts_code_str + '_result.xlsx'

dt_now = datetime.datetime.now().date()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_tst = datetime.datetime.strptime('20150119', '%Y%m%d').date()

# D W M
freq_label = 'D'
dt_baseDeltaValue_start_str = '20121031'
dt_baseDeltaValue_end_str = '20160729'
# dt_baseDeltaValue_start_str = '20140110'
# dt_baseDeltaValue_end_str = '20140306'
dt_baseDeltaValue_end =datetime.datetime.strptime(dt_baseDeltaValue_end_str,'%Y%m%d').date()
# print('base date end is ')
# print(dt_baseDeltaValue_end)

delta_rate_max = 0
delta_rate_max_date = dt_baseDeltaValue_end_str

delta_3_list = []
delta_5_list = []

row_dic = {'sell_signal_date': ' ', 'delta': 0.0, 'delta_base': 0.0,'delta_%': 0.0, 'high': 0.0, 'high_base': 0.0, 'high_%': 0.0}
df_result = pd.DataFrame()
# df_result.to_excel(path_result)


def file_exist(path):
    # return 0
    if os.path.exists(path):
        return 1
    else:
        return 0


def delta_base_3ma_5ma(filepath, dt_base_delta_start_str, dt_base_delta_end_str):
    """
    get base delta and base high
    """
    df_data = pd.read_excel(filepath, sheet_name='Data',converters={'trade_date': str})

    if 'ma3' not in list(df_data):
        return 0

    # dt_base_delta_start = datetime.datetime.strptime(dt_base_delta_start_str, '%Y%m%d').date()
    # dt_base_delta_end = datetime.datetime.strptime(dt_base_delta_end_str, '%Y%m%d').date()
    # n_days = (dt_base_delta_end - dt_base_delta_start).days

    l_high_list = []

    delta_value_list = []

    # df_data.fillna(np.nan)
    for k in df_data.index.values:
        if df_data.loc[k, 'trade_date'] == dt_base_delta_end_str:
            i = 0
            # print(dt_base_delta_start_str)
            while df_data.loc[k+i, 'trade_date'] != dt_base_delta_start_str:
                # print(df_data.loc[k + i, 'ma5'])
                # if df_data.loc[k+i, 'ma5'].isna:
                #     return 0
                delta = df_data.loc[k+i, 'ma3'] - df_data.loc[k+i, 'ma5']
                delta_value_list.append(delta)
                l_high_list.append(df_data.loc[k+i, 'high'])
                i += 1

            return df_data, float(max(delta_value_list)),  float(max(l_high_list))
    return df_data, 0, 0


def delta_pre_3ma_5ma(filepath):
    df_data = pd.read_excel(filepath, sheet_name='Data')

    if 'ma3' not in list(df_data):
        return 0

    for i in range(0, 1):
        delta_3_list.append(df_data.loc[i, 'close'])

    for i in range(0, 3):
        delta_5_list.append(df_data.loc[i, 'close'])

    return float(df_data.loc[0, 'ma3'] - df_data.loc[0, 'ma5'])


def tend_ta_tst(df_data, dt_str):
    global base_delta_value, base_high_price, df_result, delta_rate_max, delta_rate_max_date

    for k in df_data.index.values:
        # print(type(df_data.loc[k, 'trade_date']))
        if df_data.loc[k, 'trade_date'] == dt_str:
            delta_pre = float(df_data.loc[k+1, 'ma3'] -df_data.loc[k+1, 'ma5'])
            delta_now = float(df_data.loc[k, 'ma3'] - df_data.loc[k,'ma5'])

            if delta_now >= base_delta_value:
                delta_rate = round((delta_now - base_delta_value) * 100 / base_delta_value, 3)
                print(dt_str + ' is hot: ' + str(delta_rate) + '% delta')
                if delta_rate_max < delta_rate:
                    delta_rate_max = delta_rate
                    delta_rate_max_date = dt_str

            if delta_pre >= base_delta_value and delta_now <delta_pre:
                signal_price_list = [df_data.loc[k, 'high']]
                i = 1
                while float(df_data.loc[k+i, 'ma3'] - df_data.loc[k+i,'ma5']) >= base_delta_value:
                    signal_price_list.append(df_data.loc[k+i, 'high'])
                    i += 1

                high = max(signal_price_list)
                if high >= base_high_price:
                    row_dic['sell_signal_date'] = dt_str
                    row_dic['delta'] = delta_pre
                    row_dic['delta_base'] = base_delta_value
                    row_dic['delta_%'] = (delta_pre -base_delta_value)*100/base_delta_value
                    row_dic['high'] = high
                    row_dic['high_base'] = base_high_price
                    row_dic['high_%'] = (high -base_high_price)*100/base_high_price
                    df_result = df_result.append(row_dic,ignore_index=True)


# def tend_ta(dt_pre_now_str):
#     """
#     get pre delta
#     """
#     if file_exist(path_data) == 0:
#         df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_baseDeltaValue_end_str,
#                         end_date=dt_pre_now_str, ma=[3, 5, 55])
#         writer = pd.ExcelWriter(path_data)
#         # print(type(df).__name__)
#         if type(df).__name__ == 'DataFrame':
#             df.to_excel(writer, sheet_name='Data', index=False)
#             writer.save()
#
#     delta_value = delta_pre_3ma_5ma(path_data)
#     print(delta_value)
#
#     df = ts.get_realtime_quotes(st_code_str)
#     df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
#     print(df)
#     delta_3_list.append(df.loc[0, 'price'])
#     delta_5_list.append(df.loc[0, 'price'])
#     delta_now = mean(delta_3_list) - mean(delta_5_list)
#
#     if delta_value >= base_delta_value:
#         print(dt_pre_now_str + 'is hot')
#         if delta_now < delta_value:
#             print('now is warn')


def get_ta_real_data(df, base_delta_value):
    global dt_now_str
    # df_real = ts.get_realtime_quotes(st_code_str)
    # print(df_real.loc[0, 'high'])
    # print(df_real.loc[0, 'price'])
    # price_now = df_real.loc[0, 'price']
    # time_now = df_real.loc[0, 'time']
    price_now = 2612
    time_now = dt_now_str

    # print(type(df_real.loc[0, 'price']))
    ma3 = float(price_now)
    for i in range(0, 2):
        ma3 += df.loc[i, 'close']
    ma3 /= 3

    ma5 = float(price_now)
    for i in range(0, 4):
        ma5 += df.loc[i, 'close']
    ma5 /= 5

    delta_real = float(ma3 - ma5)
    print(delta_real)
    if delta_real >= base_delta_value:
        print(time_now + ' delta is ' + str(delta_real) + " bigger than " + str(round((delta_real - base_delta_value) * 100 / base_delta_value, 3)) + "%")
        if delta_real < df.loc[0, 'delta']:
            print(dt_now_str + ' is hot: ' + str(delta_real) + ' and beichi')


def get_ta_data(path_data):
    """
    get base delta value for ma3-ma5
    """
    if file_exist(path_data) == 0:
        df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_baseDeltaValue_start_str,
                        end_date=dt_now_str,  freq=freq_label, ma=[3, 5, 55])
        # print(df.head())

        df['delta'] = df['ma3'] - df['ma5']
        writer = pd.ExcelWriter(path_data)
        # print(type(df).__name__)
        if type(df).__name__ == 'DataFrame':
            df.to_excel(writer, sheet_name='Data', index=False)
            writer.save()


"""
main start
"""
df = pd.read_excel('E:/Project/Python/fa_parameters.xlsx', dtype=str)
for k in df.index.values:
    if df.loc[k, 'name'] == code_name:
        ts_code_str = df.loc[k, 'code']
        st_code_str = ts_code_str[:-3]
        print(st_code_str)
        path_data = path_root + ts_code_str + '.xlsx'
        path_result = path_root + ts_code_str + '_result.xlsx'
        freq_label = period_type
        if period_type == 'BM':
            freq_label = 'M'
        if period_type == 'ZD':
            freq_label = 'D'
        dt_baseDeltaValue_start_str = df.loc[k, period_type + '_start']
        # print(dt_baseDeltaValue_start_str)
        dt_baseDeltaValue_end_str = df.loc[k, period_type + '_end']
        # dt_baseDeltaValue_start_str = '20140110'
        # dt_baseDeltaValue_end_str = '20140306'
        dt_baseDeltaValue_end = datetime.datetime.strptime(dt_baseDeltaValue_end_str, '%Y%m%d').date()
        print('base date end is ')
        print(dt_baseDeltaValue_end)
        delta_rate_max_date = dt_baseDeltaValue_end_str

get_ta_data(path_data)

df, base_delta_value, base_high_price = delta_base_3ma_5ma(path_data, dt_baseDeltaValue_start_str, dt_baseDeltaValue_end_str)
print('base delta is ' + str(base_delta_value) + ' base high is ' + str(base_high_price))

# dt_tst_end = datetime.datetime.strptime('20150811', '%Y%m%d').date()
dt_tst = dt_baseDeltaValue_end

# while dt_tst <= dt_tst_end:

# df_data = pd.read_excel(path_data, sheet_name='Data', converters={'trade_date': str})
# if 'ma3' not in list(df_data):

while dt_tst <= dt_now:
    dt_tst_str = dt_tst.strftime('%Y%m%d')

    tend_ta_tst(df, dt_tst_str)

    dt_tst = dt_tst + datetime.timedelta(days=1)

print(delta_rate_max_date + ' is max hot: ' + str(delta_rate_max) + '% delta')
writer_result = pd.ExcelWriter(path_result)
df_result.to_excel(writer_result)
writer_result.save()

# print(datetime.datetime.now().hour)
# print(datetime.datetime.now().minute)
if (freq_label == "M") or (freq_label == "W") or ((datetime.datetime.now().hour <= 16) and (datetime.datetime.now().hour >= 9)):
    count = 0
    while count < 2:
        get_ta_real_data(df, base_delta_value)
        time.sleep(2)
        count += 1

#　os.system('d:/催眠曲莫扎特.mp3')
