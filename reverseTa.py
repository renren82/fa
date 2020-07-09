import os
import datetime
import tushare as ts
import pandas as pd
from numpy import *
import numpy as np

#  002714.SZ '.SH'
st_code_str = '000559'
ts_code_str = st_code_str + '.SZ'

path_root = 'H:/'
path_data = path_root + 'sz000559_30m_20200620.xlsx'
path_result = path_root + ts_code_str + '_result.xlsx'

# dt_now = datetime.datetime.now().date()
dt_now = datetime.datetime.now()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d%H%M%S')
# dt_tst = datetime.datetime.strptime('20150119', '%Y%m%d%H%M%S').date()

# D W M
freq_label = 'D'
dt_baseDeltaValue_start_str = '20200611133000'
dt_baseDeltaValue_end_str = '20200612110000'
# dt_baseDeltaValue_start_str = '20140110'
# dt_baseDeltaValue_end_str = '20140306'
# dt_baseDeltaValue_end =datetime.datetime.strptime(dt_baseDeltaValue_end_str,'%Y%m%d%H%M%S').date()
dt_baseDeltaValue_end =datetime.datetime.strptime(dt_baseDeltaValue_end_str,'%Y%m%d%H%M%S')
print('base date end is ')
print(dt_baseDeltaValue_end)

low_price_list = []
df_result = pd.DataFrame()


def file_exist(path):
    # return 0
    if os.path.exists(path):
        return 1
    else:
        return 0


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


def delta_base_3ma_5ma(filepath, dt_base_delta_start_str, dt_base_delta_end_str):
    """
    get base delta 
    """
    df_data = pd.read_excel(filepath, sheet_name='Data', converters={'trade_date': str})
    print(df_data.head())
    if 'ma3' not in list(df_data):
        return 0

    # dt_base_delta_start = datetime.datetime.strptime(dt_base_delta_start_str, '%Y%m%d').date()
    # dt_base_delta_end = datetime.datetime.strptime(dt_base_delta_end_str, '%Y%m%d').date()
    # n_days = (dt_base_delta_end - dt_base_delta_start).days

    l_low_list = []

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
                l_low_list.append(df_data.loc[k+i, 'low'])
                i += 1

            return df_data, min(delta_value_list)
    return df_data, 0


def reverse_ta_process(df_data, dt_str):
    global base_delta_value, low_price_list, df_result
    # df_data = pd.read_excel(filepath, sheet_name='Data',converters={'trade_date': str})

    if 'ma3' not in list(df_data):
        return 0
    v_reverse_flag = 0
    for k in df_data.index.values:
        # print(type(df_data.loc[k, 'trade_date']))
        if df_data.loc[k, 'trade_date'] == dt_str:
            print(dt_str)
            low_price_list.append(df_data.loc[k, 'low'])
            delta_now = float(df_data.loc[k, 'ma3'] - df_data.loc[k,'ma5'])

            if delta_now < 0:
                i = 1
                while float(df_data.loc[k+i, 'ma3'] - df_data.loc[k+i,'ma5']) < 0:
                    i += 1
                j = i
                while float(df_data.loc[k + j, 'ma3'] - df_data.loc[k + j, 'ma5']) >= 0:
                    j += 1
                delta_pre = 0
                while float(df_data.loc[k + j, 'ma3'] - df_data.loc[k + j, 'ma5']) < delta_pre:
                    delta_pre = float(df_data.loc[k + j, 'ma3'] - df_data.loc[k + j, 'ma5'])

                if (base_delta_value < 0) and (delta_now < 0) and (delta_pre < 0 )and (delta_now < delta_pre) and (base_delta_value < delta_now):
                    v_reverse_flag = 1

            if v_reverse_flag == 1:
                if min(low_price_list) == df_data.loc[k, 'low']:
                    if df_data.loc[k+1, 'delta'] < df_data.loc[k, 'delta']:
                        df_result = df_result.append(df_data.loc[k], ignore_index=True)
                        v_reverse_flag = 0


if __name__ == '__main__':
    get_ta_data(path_data)

    df_data, base_delta_value = delta_base_3ma_5ma(path_data, dt_baseDeltaValue_start_str, dt_baseDeltaValue_end_str)
    print('base delta is ' + str(base_delta_value))

    dt_tst = dt_baseDeltaValue_end

    while dt_tst <= dt_now:
        dt_tst_str = dt_tst.strftime('%Y%m%d%H%M%S')
        # print(dt_tst_str)
        reverse_ta_process(df_data, dt_tst_str)

        # dt_tst = dt_tst + datetime.timedelta(days=1)
        dt_tst = dt_tst + datetime.timedelta(hours=0.5)

    writer_result = pd.ExcelWriter(path_result)
    df_result.to_excel(writer_result)
    writer_result.save()