import os
import datetime
import tushare as ts
import pandas as pd
from numpy import *
import time
import numpy as np

path_root = 'H:/'
path_param = 'fa.xlsx'

dt_now = datetime.datetime.now().date()
dt_now_str = dt_now.strftime('%Y%m%d')

row_dic = {'high_price_date': ' ','sell_signal_date': ' ', 'delta': 0.0, 'delta_base': 0.0,'delta_%': 0.0, 'high': 0.0, 'high_base': 0.0, 'high_%': 0.0}
df_result = pd.DataFrame()

def get_ta_data(path_data, k, df_param):
    """
    get base delta value for ma3-ma5
    """
    if os.path.exists(path_data):
        return 1

    df = ts.pro_bar(ts_code=df_param.loc[k, 'code'], adj='qfq', start_date=df_param.loc[k, 'start'],
                    end_date=dt_now_str,  freq=df_param.loc[k, 'period'], ma=[3, 5, 55])
    # print(df.head())

    df['delta'] = round((df['ma3'] - df['ma5']), 4)

    writer = pd.ExcelWriter(path_data)
    # print(type(df).__name__)
    if type(df).__name__ == 'DataFrame':
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()


def delta_base_3ma_5ma(filepath, type, dt_base_delta_start_str, dt_base_delta_end_str):
    """
    get base delta and base high
    """
    # sheet_name='Sheet1'
    df_data = pd.read_excel(filepath, converters={'trade_date': str})

    if 'ma3' not in list(df_data):
        return 0

    # dt_base_delta_start = datetime.datetime.strptime(dt_base_delta_start_str, '%Y%m%d').date()
    # dt_base_delta_end = datetime.datetime.strptime(dt_base_delta_end_str, '%Y%m%d').date()
    # n_days = (dt_base_delta_end - dt_base_delta_start).days

    l_price_list = []

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
                delta = round(delta, 4)
                delta_value_list.append(delta)
                if type == 'up':
                    l_price_list.append(df_data.loc[k+i, 'high'])
                else:
                    l_price_list.append(df_data.loc[k + i, 'low'])
                i += 1
            if type == 'up':
                return df_data, float(max(delta_value_list)),  float(max(l_price_list))
            else:
                return df_data, float(min(delta_value_list)), float(min(l_price_list))
    return df_data, 0, 0


def ta_process(i, df_param, df_data, base_delta_value, base_price):
    dt_tst = datetime.datetime.strptime(df_param.loc[i, 'cur_start'], '%Y%m%d').date()
    delta_max = 0
    delta_max_rate = 0
    delta_max_date = ''
    delta_rate_max = 0
    high_low_price = 0
    high_low_price_date =''
    if df_param.loc[i, 'type'] == 'up':
        df_param.loc[i, 'status'] = 'not hot'
    else:
        df_param.loc[i, 'status'] = 'not cold'

    while dt_tst <= dt_now:
        dt_tst_str = dt_tst.strftime('%Y%m%d')

        global df_result

        for k in df_data.index.values:
            # print(type(df_data.loc[k, 'trade_date']))
            if df_data.loc[k, 'trade_date'] == dt_tst_str:
                delta_pre = float(df_data.loc[k + 1, 'ma3'] - df_data.loc[k + 1, 'ma5'])
                delta_now = float(df_data.loc[k, 'ma3'] - df_data.loc[k, 'ma5'])

                if df_param.loc[i, 'type'] == 'up':

                    if delta_max <= delta_now:
                        delta_max = delta_now
                        delta_max_date = dt_tst_str
                        delta_rate = round((delta_now - base_delta_value) * 100 / base_delta_value, 4)
                    if delta_now >= base_delta_value:
                        print(df_param.loc[i, 'name'] + " " + dt_tst_str + ' is hot: ' + str(delta_rate) + '% delta')
                        df_param.loc[i, 'status'] = 'hot'

                    if delta_pre >= base_delta_value and delta_now < delta_pre :
                        signal_price_list = [df_data.loc[k, 'high']]
                        j = 1
                        while float(df_data.loc[k + j, 'ma3'] - df_data.loc[k + j, 'ma5']) >= base_delta_value:
                            #　signal_price_list.append(df_data.loc[k + i, 'high'])
                            if high_low_price <= df_data.loc[k + j, 'high']:
                                high_low_price = df_data.loc[k + j, 'high']
                                high_low_price_date = df_data.loc[k + j, 'trade_date']
                            j += 1
                        print(df_param.loc[i, 'name'] + " " + dt_tst_str + ' is hot and beichi， high price ' + str(high_low_price))
                        df_param.loc[i, 'status'] = 'hot and beichi'
                       #  high = max(signal_price_list)
                        if high_low_price >= base_price:
                            row_dic['sell_signal_date'] = dt_tst_str
                            row_dic['delta'] = delta_pre
                            row_dic['delta_base'] = base_delta_value
                            row_dic['delta_%'] = (delta_pre - base_delta_value) * 100 / base_delta_value
                            row_dic['high'] = high_low_price
                            row_dic['high_base'] = base_price
                            row_dic['high_%'] = (high_low_price - base_price) * 100 / base_price
                            df_result = df_result.append(row_dic, ignore_index=True)

                if df_param.loc[i, 'type'] == 'down':

                    if delta_max >= delta_now:
                        delta_max = delta_now
                        delta_max_date = dt_tst_str
                        delta_rate = round((delta_now - base_delta_value) * 100 / (base_delta_value), 4)
                        # print(str(delta_rate))
                    if delta_now <= base_delta_value:
                        print(df_param.loc[i, 'name'] + " " + dt_tst_str + ' is cold: ' + str(delta_rate) + '% delta')
                        df_param.loc[i, 'status'] = 'cold'

        dt_tst = dt_tst + datetime.timedelta(days=1)

    # print(delta_rate_max_date + ' is max hot: ' + str(delta_rate_max) + '% delta')
    df_param.loc[i, 'cur_max_delta_date'] = delta_max_date
    df_param.loc[i, 'cur_max_delta'] = delta_max
    df_param.loc[i, 'cur_max_delta_rate'] = str(delta_rate) + "%"

    # df_param.loc[i, 'cur_high_low_price'] = high_low_price
    # df_param.loc[i, 'cur_high_low_price_date'] = high_low_price_date
    print('end')


if __name__ == '__main__':
    df_param = pd.read_excel(path_root + path_param, dtype=str)
    for k in df_param.index.values:
        path_data = path_root + df_param.loc[k, 'code'] + '_' + df_param.loc[k, 'period'] + ".xlsx"
        get_ta_data(path_data, k, df_param)
        dt_baseDeltaValue_start_str = df_param.loc[k, 'compare_start']
        dt_baseDeltaValue_end_str = df_param.loc[k, 'compare_end']
        df_data, base_delta_value, base_price = delta_base_3ma_5ma(path_data, df_param.loc[k, 'type'], dt_baseDeltaValue_start_str,
                                                                   dt_baseDeltaValue_end_str)
        print(df_param.loc[k, 'name'] + " " + 'base delta is ' + str(base_delta_value) + ' base price is ' + str(base_price))
        df_param.loc[k, 'compare_delta'] = base_delta_value
        df_param.loc[k, 'compare_price'] = base_price
        ta_process(k, df_param, df_data, base_delta_value, base_price)

    writer_result = pd.ExcelWriter(path_root + path_param)
    df_param.to_excel(writer_result, index=False)
    writer_result.save()
