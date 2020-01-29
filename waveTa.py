import os
import datetime
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ts_code_str = '601989.SH'
st_code_str = '601989'
path_root = 'H:/'
path_file = path_root + ts_code_str + '.xlsx'

dt_now = datetime.datetime.now().date()
# dt_now = datetime.datetime.strptime('20160101', '%Y%m%d').date()
dt_now_str = dt_now.strftime('%Y%m%d')
dt_data_start = dt_now - datetime.timedelta(days=365)
dt_data_start_str = dt_data_start.strftime('%Y%m%d')


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
        df = ts.pro_bar(ts_code=ts_code_str, adj='qfq', start_date=dt_data_start_str,
                        end_date=dt_now_str, ma=[3, 5, 8, 13, 21, 34, 55, 89, 144, 233])
        # print(df.head())
        writer = pd.ExcelWriter(path_data)
        # print(type(df).__name__)
        if type(df).__name__ == 'DataFrame':
            df.to_excel(writer, sheet_name='history', index=False)
            writer.save()


get_ta_data(path_file)

df = pd.read_excel(path_file, sheet_name='history', converters={'trade_date': str})

df['trade_date'] = pd.to_datetime(df['trade_date'])
# x = df.loc[:, 'signal_date'].values
#
# y = df.loc[:, 'delta_%'].values

df = df.set_index('trade_date')

df['delta'] = df['ma3'] - df['ma5']
df['close_%'] = df['close']

plt.subplot(211)
df['delta'].plot()
plt.grid(True)
plt.ylabel('delta', size=15)
plt.subplot(212)
df['close_%'].plot()

plt.grid(True)
plt.ylabel('price', size=15)
# plt.title('title name')
# plt.rcParams['savefig.dpi'] = 1024
plt.show()
# plt.savefig('./a.png', dpi=1000)
# plt.savefig('./a.png')


